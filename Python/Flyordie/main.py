import tkinter as tk
from datetime import timedelta, datetime
from collections import defaultdict
from tkinter import messagebox
from PIL import Image, ImageTk
from requests import get
from io import BytesIO
from bs4 import BeautifulSoup
from math import floor
from time import sleep
from logging import basicConfig, getLogger, INFO

basicConfig(filename="erros.log", filemode="w", level=INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = getLogger(__name__)


# --------------------------------------------------------------------------------------------


NORMAL_FONT, TITLE_FONT = ("Arial", 12), ("Arial", 24)
BG_COLOR = "#282c34"

TEXT_PROPS = {"bg": BG_COLOR, "fg": "white", "font": NORMAL_FONT}
TITLE_PROPS = {"bg": BG_COLOR, "fg": "white", "font": TITLE_FONT}

GREEN_BUTTON_PROPS = {"bg": "green", "fg": "white", "font": NORMAL_FONT}
ORANGE_BUTTON_PROPS = {"bg": "orange", "fg": "black", "font": NORMAL_FONT}
DARKRED_BUTTON_PROPS = {"bg": "darkred", "fg": "white", "font": NORMAL_FONT}
LIGHTBLUE_BUTTON_PROPS = {"bg": "lightblue", "fg": "black", "font": NORMAL_FONT}


# --------------------------------------------------------------------------------------------


players_data = defaultdict(lambda: {
    "Sexo": str,
    "País": str,
    "Idade": str,
    "Estado": str,
    "Sala": str,
    "Jogos": defaultdict(lambda: {
        "Categoria": str,
        "Pontuação": int,
        "Total de Partidas": int,
        "Vitórias": {"Total": int, "Percentagem": int},
        "Empates": {"Total": int, "Percentagem": int},
        "Derrotas": {"Total": int, "Percentagem": int}
    })
})

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.custom_window()
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in (MainMenu, PlayersData, ResultSimulator):
            self.frames[frame.__name__] = frame(parent=container, controller=self)
            self.frames[frame.__name__].grid(row=0, column=0, sticky=tk.NSEW)
        
        self.show_frame("MainMenu")

    def custom_window(self) -> None:
        favicon = get("https://www.flyordie.com/favicon.ico").content
        self.title("FlyorDie - Fernando Sobral")
        self.geometry(f"{480}x{600}")
        self.iconphoto(True, ImageTk.PhotoImage(Image.open(BytesIO(favicon))))
        self.minsize(380, 300)

    def show_frame(self, page_name: str) -> None:
        self.frames[page_name].tkraise()

    def add_player_input_field(self, frame: tk.Frame, placeholder: str = "Nome do Jogador", can_delete: bool = False) -> None:
        players_to_search = getattr(frame, "PLAYERS_TO_SEARCH", None)
        limit_players = getattr(frame, "LIMIT_PLAYERS", None)
        if players_to_search is not None and limit_players is not None:
            if len(players_to_search) >= limit_players: return

        entry = tk.Entry(frame, fg="gray", width=20, font=NORMAL_FONT)
        entry.insert(0, placeholder)
        if can_delete is True:
            def destroy_entry():
                players_to_search.remove(entry)
                delete_entry_button.destroy()
                entry.destroy()
            frame.grid_columnconfigure(63, weight=1)
            delete_entry_button = tk.Button(frame, text="X", **DARKRED_BUTTON_PROPS, command=destroy_entry)
            # frame.grid_columnconfigure(0, weight=1)

        def on_click(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")
        def on_focusout(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="gray")

        entry.bind("<Button-1>", on_click)
        entry.bind("<FocusOut>", on_focusout)
        entry.pack(pady=10, padx=10)
        if can_delete is True:
            # attach the button position to the entry
            delete_entry_button.pack(padx=2)
        if players_to_search is not None:
            players_to_search.append(entry)

    def add_option_section(self, frame: tk.Frame, options: list[str], default_option: str) -> tk.OptionMenu:
        if getattr(frame, "GAMES_PLAYED", None) is not None:
            frame.GAMES_PLAYED = tk.StringVar(frame)
            frame.GAMES_PLAYED.set(default_option)
            option_menu = tk.OptionMenu(frame, frame.GAMES_PLAYED, *options)
            option_menu.pack(side=tk.TOP, pady=5)
            return option_menu


class MainMenu(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: Window):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Menu Principal", **TITLE_PROPS)
        label.pack(side=tk.TOP, pady=10)

        button_players = tk.Button(self, text="Dados Jogadores", font=NORMAL_FONT, command=lambda: controller.show_frame("PlayersData"))
        button_players.pack(side=tk.TOP, pady=10)
        
        button_results = tk.Button(self, text="Simulador de Resultados", font=NORMAL_FONT, command=lambda: controller.show_frame("ResultSimulator"))
        button_results.pack(side=tk.TOP, pady=10)
        
        button_exit = tk.Button(self, text="Sair", **DARKRED_BUTTON_PROPS, command=self.quit)
        button_exit.pack(side=tk.BOTTOM, pady=10)


class PlayersData(tk.Frame):
    PLAYERS_TO_SEARCH = []
    LIMIT_PLAYERS = 4

    def __init__(self, parent: tk.Frame, controller: Window):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        title = tk.Label(self, text="Dados dos Jogadores", **TITLE_PROPS)
        title.pack(side=tk.TOP, pady=10)
        
        controller.add_player_input_field(self)

        button_back = tk.Button(self, text="Voltar", font=NORMAL_FONT, command=lambda: controller.show_frame("MainMenu"))
        button_back.pack(side=tk.BOTTOM, pady=5)
        
        export_button = tk.Button(self, text="Exportar Dados", **LIGHTBLUE_BUTTON_PROPS, command=lambda: self.export_players_data())
        export_button.pack(side=tk.BOTTOM, padx=10, pady=10)
 
        button_plus = tk.Button(self, text="+", **ORANGE_BUTTON_PROPS, command=lambda: controller.add_player_input_field(self, can_delete=True))
        button_plus.pack(side=tk.BOTTOM, pady=10)

    def export_players_data(self) -> None:
        players_names, file_name = [], ""
        for player_input in self.PLAYERS_TO_SEARCH:
            name = player_input.get().strip()
            if name != "" and name != "Nome do Jogador":
                players_names.append(name)

        global players_data
        get_players_data(*players_names)
        for name in players_names:
            if name not in players_data: return
            file_name += name.replace(" ", "_")+"-"
        
        with open(file_name[:-1]+".txt", mode="w", encoding="utf-8") as file:
            for name in players_names:
                player_data = players_data[name]
                file.write(f"Jogador: {name}\n")
                for data, value in player_data.items():
                    if data != "Jogos":
                        file.write(f"  {data}: {value}\n")
                    else:
                        file.write(f"  {data}:\n")
                        for game_name, game_data in value.items():
                            file.write(f"\t{game_name}:\n")
                            for game_data_name, game_data_value in game_data.items():
                                if game_data_name in ("Vitórias", "Empates", "Derrotas"):
                                    file.write(f"\t  {game_data_name}: {game_data_value['Total']}, {game_data_value['Percentagem']}%\n")
                                else:
                                    file.write(f"\t  {game_data_name}: {game_data_value}\n")
                file.write("\n")
        messagebox.showwarning("Exportação Dados", "Dados exportados com sucesso!")


class ResultSimulator(tk.Frame):
    SERIES_OF_GAMES = { 1: 16, 2: 24, 3: 28, 4: 30, 5: 31, "6+": 32 }
    GAMES_PLAYED = 1

    def __init__(self, parent: tk.Frame, controller: Window):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Simulador de Resultados", **TITLE_PROPS)
        label.pack(side=tk.TOP, padx=10, pady=5)
        
        controller.add_player_input_field(self)
        vs = tk.Label(self, text="VS", **TEXT_PROPS)
        vs.pack()
        controller.add_player_input_field(self, "Nome do Oponente")
        controller.add_player_input_field(self, "Jogo")
        controller.add_option_section(self, list(self.SERIES_OF_GAMES.keys()), "Número de Jogos")
        
        generate_button = tk.Button(self, text="Gerar Resultado", **GREEN_BUTTON_PROPS, command=lambda: self.generate_result())
        generate_button.pack(side=tk.TOP, padx=10, pady=5)

        button_back = tk.Button(self, text="Voltar", font=NORMAL_FONT, command=lambda: controller.show_frame("MainMenu"))
        button_back.pack(side=tk.BOTTOM, pady=5)
        
        results_label = tk.Label(self, **TEXT_PROPS)
        results_label.pack(side=tk.BOTTOM, padx=10, pady=5)

    def generate_result(self) -> None:
        player_name = self.__dict__["children"]["!entry"].get().strip()
        opponent_name = self.__dict__["children"]["!entry2"].get().strip()
        game_name = self.__dict__["children"]["!entry3"].get().strip()
        games_played = self.GAMES_PLAYED.get()
        games_played = 1 if games_played == "Número de Jogos" else clear_int(games_played)
        if not player_name or player_name == "Nome do Jogador":
            print_errors("Indique o nome do jogador")
            return
        elif not opponent_name or opponent_name == "Nome do Oponente":
            print_errors("Indique o nome do oponente")
            return
        elif not game_name or game_name == "Jogo":
            print_errors("Indique o nome do jogo")
            return
        
        get_players_data(player_name, opponent_name)
        
        global players_data
        if player_name not in players_data or opponent_name not in players_data:
            return
        if game_name not in players_data[player_name]["Jogos"]:
            print_errors(f"{player_name} não joga {game_name}")
            return
        elif game_name not in players_data[opponent_name]["Jogos"]:
            print_errors(f"{opponent_name} não joga {game_name}")
            return
        player_game_data = players_data[player_name]["Jogos"][game_name]
        opponent_game_data = players_data[opponent_name]["Jogos"][game_name]
        predictions = {
            player_name: {
                "Pontuação atual": player_game_data["Pontuação"],
                "Probabilidade de Vitória": self.calculate_winning_probability(player_game_data["Pontuação"], opponent_game_data["Pontuação"]),
                **self.calculate_new_rating(player_game_data["Pontuação"], opponent_game_data["Pontuação"], games_played),
                "Chega aos 0 pontos em": self.calculate_days_until_zero_points(player_game_data["Pontuação"]),
            },
            opponent_name: {
                "Pontuação atual": opponent_game_data["Pontuação"],
                "Probabilidade de Vitória": self.calculate_winning_probability(opponent_game_data["Pontuação"], player_game_data["Pontuação"]),
                **self.calculate_new_rating(opponent_game_data["Pontuação"], player_game_data["Pontuação"], games_played),
                "Chega aos 0 pontos em": self.calculate_days_until_zero_points(opponent_game_data["Pontuação"]),
            },
        }
        display_text = ""
        for player, data in predictions.items():
            display_text += f"{player}:\n"
            for key, value in data.items():
                display_text += f"{key}: {value}\n"
            display_text += "\n"
        self.__dict__["children"]["!label3"].config(text=display_text)


    # Prof. Arpad Elo"s Formula - https://www.flyordie.com/games/help/rating_system.html
    def calculate_winning_probability(self, player_rating: int, oponent_rating: int) -> str:
        rating_difference = abs(player_rating - oponent_rating)
        if rating_difference >= 800:
            return f"{99 if player_rating > oponent_rating else 1}%"
        elif rating_difference >= 400:
            return f"{91 if player_rating > oponent_rating else 9}%"
        elif rating_difference >= 200:
            return f"{76 if player_rating > oponent_rating else 24}%"
        elif rating_difference >= 100:
            return f"{64 if player_rating > oponent_rating else 36}%"
        return "50%"

    def getK(self, rating: int, games_played: int = 1) -> int:
        k = 24
        if rating <= 2099:
            k = 32
        elif rating >= 2400:
            k = 16
        return min(int(k * (2 - (1 / 2**(games_played - 1 )))), self.SERIES_OF_GAMES[games_played if games_played < 6 else "6+"])

    def calculate_expected_score(self, player_rating: int, oponent_rating: int) -> float:
        return 1 / (1 + 10 ** (-abs(player_rating - oponent_rating) / 400))

    def calculate_new_rating(self, player_rating: int, oponent_rating: int, games_played: int = 1) -> int:
        if player_rating is None or oponent_rating is None:
            return {"Pontuação em caso de Vitória": None, "Pontuação em caso de Empate": None, "Pontuação em caso de Derrota": None}

        results = {
            "Pontuação em caso de Vitória": int(round(player_rating + self.getK(player_rating, games_played)*(1- self.calculate_expected_score(player_rating, oponent_rating)), 0)),
            "Pontuação em caso de Empate": int(round(player_rating + self.getK(player_rating, games_played)*(0.5 - self.calculate_expected_score(player_rating, oponent_rating)), 0)),
            "Pontuação em caso de Derrota": int(round(player_rating + self.getK(player_rating, games_played)*(0 - self.calculate_expected_score(player_rating, oponent_rating)), 0)),
        }
        return results
    
    def calculate_days_until_zero_points(self, rating: int) -> str:
        days_left = 0
        while rating >= 0:
            rating -= 1 if rating <= 353 else int(round(rating**2 / 125000, 0))
            days_left += 1
        return f"{days_left} dias ({(datetime.today() + timedelta(days=days_left)).strftime('%d/%m/%Y')})"



def clear_int(value: str) -> int:
    if not value:
        return None
    try:
        return int(value.replace(",", "").replace(",", "").replace("(", "").replace(")", "").replace("~", "").replace("+", ""))
    except ValueError:
        return None

def clear_float(value: str) -> float:
    try:
        return float(value.split(" ")[-1].replace("rotate", "").replace("(", "").replace(")", "").replace("deg", "").replace(";", "").replace(" ", ""))
    except ValueError:
        return None

def print_errors(display_message: str, error_message: str = "") -> None:
    global logger
    logger.error(f"{error_message} | {error_message}")
    messagebox.showerror("Erro", display_message)


def get_player_data(players_data: dict, player_name: str) -> None:
    gamelist_response = get(f"https://games.flyordie.com/players/{player_name}")
    if gamelist_response.status_code != 200:
        print_errors(f"Erro ao obter dados acerca do jogador {player_name}", f"{gamelist_response.status_code}-{gamelist_response.url}")
        return
    gamelist_response = BeautifulSoup(gamelist_response.text, "html.parser")

    game_list = gamelist_response.find("div", class_="F C gameListCenter gameList gameList-wide gameListTab initial-tab")
    if not getattr(game_list, "children", None):
        print_errors(f"Erro ao ler a lista de jogos do jogador {player_name}")
        return

    possible_status_references = (
        gamelist_response.find("div", class_="w currently-online-caption H"),
        gamelist_response.findAll("div", class_="w H"),
    )
    players_data[player_name]["Sexo"] = getattr(gamelist_response.find("div", class_="w gender H"), "text", None)
    players_data[player_name]["Idade"] = getattr(gamelist_response.find("div", class_="w age H"), "text", None)
    players_data[player_name]["Sala"] = getattr(gamelist_response.find("div", class_="w current-room-caption H"), "text", None)
    players_data[player_name]["País"] = getattr(gamelist_response.find("div", class_="w c-l H"), "text", None)
    for ref in possible_status_references:
        ref = ref[2] if isinstance(ref, list) else ref
        players_data[player_name]["Estado"] = getattr(ref, "text", None)
        if players_data[player_name]["Estado"]: break

    for game_name in game_list.children:
        sleep(0.1)
        game_name = game_name.attrs["href"].split("/")[-1]
        gamedata_response = get(f"https://games.flyordie.com/players/{player_name}/{game_name}")
        if gamedata_response.status_code != 200:
            print_errors(f"Erro ao obter os dados do jogo {game_name} do jogador {player_name}", f"{gamedata_response.status_code}-{gamedata_response.url}")
            return
        
        gamedata_response = BeautifulSoup(gamedata_response.text, "html.parser")
        category = getattr(gamedata_response.find("div", class_="l ratingCategoryName"), "text", None)
        rating = clear_int(getattr(gamedata_response.findAll("div", class_="w H")[3], "text", None))
        total_matches = clear_int(getattr(gamedata_response.find("td", class_="w matchCount"), "text", None))
        
        loss_degree, loss_tag = 0, gamedata_response.find("div", class_="pieSegmentInner lossesItem") or None
        if loss_tag:
            loss_degree = 360 - clear_float(loss_tag.parent.attrs["style"])
        draw_degree, draw_tag = 0, gamedata_response.find("div", class_="pieSegmentInner drawsItem") or None
        if draw_tag:
            if loss_degree == 0:
                draw_degree = 360 - clear_float(draw_tag.parent.attrs["style"])
            else:
                draw_degree = clear_float(loss_tag.parent.attrs["style"]) - clear_float(draw_tag.parent.attrs["style"])

        wins = clear_int(gamedata_response.find("div", class_="w winCount H").text)
        draws = floor((draw_degree * total_matches) / 360)
        losses = floor((loss_degree * total_matches) / 360)
        players_data[player_name]["Jogos"][game_name]["Categoria"] = category
        players_data[player_name]["Jogos"][game_name]["Pontuação"] = rating
        players_data[player_name]["Jogos"][game_name]["Total de Partidas"] = total_matches
        players_data[player_name]["Jogos"][game_name]["Vitórias"]["Total"] = wins
        players_data[player_name]["Jogos"][game_name]["Empates"]["Total"] = draws
        players_data[player_name]["Jogos"][game_name]["Derrotas"]["Total"] = losses
        players_data[player_name]["Jogos"][game_name]["Vitórias"]["Percentagem"] = round(wins / total_matches * 100, 2)
        players_data[player_name]["Jogos"][game_name]["Empates"]["Percentagem"] = round(draws / total_matches * 100, 2)
        players_data[player_name]["Jogos"][game_name]["Derrotas"]["Percentagem"] = round(losses / total_matches * 100, 2)


def get_players_data(*players_names: str) -> bool:
    if players_names:
        global players_data
        for name in players_names:
            if name not in players_data:
                get_player_data(players_data, name)

if __name__ == "__main__":
    Window().mainloop()
