from collections import defaultdict
import tkinter as tk
from pdb import set_trace
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
DARKRED_BUTTON_PROPS = {"bg": "darkred", "fg": "white", "font": NORMAL_FONT}
LIGHTBLUE_BUTTON_PROPS = {"bg": "lightblue", "fg": "black", "font": NORMAL_FONT}

MONTHS = {1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho", 7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"}


# --------------------------------------------------------------------------------------------


players_data = defaultdict(lambda: {
    "Sexo": str,
    "País": str,
    "Estado": str,
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
    ICON_URL = "https://www.flyordie.com/favicon.ico"
    MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT = 380, 300
    SCREEN_WIDTH, SCREEN_HEIGHT = 480, 580

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
        favicon = get(self.ICON_URL).content
        self.title("FlyorDie - Fernando Sobral")
        self.geometry(f"{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")
        self.iconphoto(True, ImageTk.PhotoImage(Image.open(BytesIO(favicon))))
        self.minsize(self.MIN_SCREEN_WIDTH, self.MIN_SCREEN_HEIGHT)

    def show_frame(self, page_name: str) -> None:
        self.frames[page_name].tkraise()

    def add_player_input_field(self, frame: tk.Frame, placeholder: str = "Nome do Jogador", can_delete: bool = False, **kwargs) -> tk.Entry:
        entry = tk.Entry(frame, fg="gray", width=20, font=NORMAL_FONT, **kwargs)
        entry.insert(0, placeholder)
        if can_delete is True:
            def destroy_entry():
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
        entry.pack(pady=10, padx=10, **kwargs)
        if can_delete is True:
            # attach the button position to the entry
            delete_entry_button.place(x=entry.winfo_x()+entry.winfo_width()+5, y=entry.winfo_y())
            delete_entry_button.pack(padx=2)
        return entry


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
    LIMIT_PLAYERS = 4

    def __init__(self, parent: tk.Frame, controller: Window):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Dados dos Jogadores", **TITLE_PROPS)
        label.pack(side=tk.TOP, pady=10)
        
        controller.add_player_input_field(self)

        button_back = tk.Button(self, text="Voltar", font=NORMAL_FONT, command=lambda: controller.show_frame("MainMenu"))
        button_back.pack(side=tk.BOTTOM, pady=10)
        
        export_button = tk.Button(self, text="Exportar", **LIGHTBLUE_BUTTON_PROPS, command=lambda: export_players_data(players_data))
        export_button.pack(side=tk.BOTTOM, padx=10, pady=5)
        
        button_plus = tk.Button(self, text="+", **GREEN_BUTTON_PROPS, command=lambda: controller.add_player_input_field(self, can_delete=True))
        button_plus.pack(side=tk.BOTTOM, pady=10)


class ResultSimulator(tk.Frame):
    SERIES_OF_GAMES = { 1: 16, 2: 24, 3: 28, 4: 30, 5: 31, "6+": 32 }

    def __init__(self, parent: tk.Frame, controller: Window):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Simulador de Resultados", **TITLE_PROPS)
        label.pack(side=tk.TOP, padx=10, pady=5)
        
        controller.add_player_input_field(self)
        vs = tk.Label(self, text="VS", **TEXT_PROPS)
        vs.pack()
        controller.add_player_input_field(self, "Nome do Oponente")
        
        generate_button = tk.Button(self, text="Gerar Resultado", **GREEN_BUTTON_PROPS, command=lambda: self.generate_result())
        generate_button.pack(side=tk.TOP, padx=10, pady=5)

        results_label = tk.Label(self, **TEXT_PROPS, name="results_label")
        results_label.pack(side=tk.TOP, padx=10, pady=5)
        
        button_back = tk.Button(self, text="Voltar", font=NORMAL_FONT, command=lambda: controller.show_frame("MainMenu"))
        button_back.pack(side=tk.BOTTOM, pady=10)

    def generate_result(self) -> None:
        player_name = self.__dict__["children"]["!entry"].get().strip()
        opponent_name = self.__dict__["children"]["!entry2"].get().strip()
        if not player_name or player_name == "Nome do Jogador":
            print_errors("O nome do jogador não pode ser vazio")
        elif not opponent_name or opponent_name == "Nome do Oponente":
            print_errors("O nome do oponente não pode ser vazio")
        else:
            global players_data
            if players_data.get(player_name, None) is None:
                players_data[player_name] = get_player_data(player_name)
            if players_data.get(opponent_name, None) is None:
                players_data[opponent_name] = get_player_data(opponent_name)
            set_trace()
    
    # Prof. Arpad Elo"s Formula - https://www.flyordie.com/games/help/rating_system.html

    def calculate_winning_probability(self, player_rating: int, oponent_rating: int) -> int:
        rating_difference = abs(player_rating - oponent_rating)
        result_factor = 100 * rating_difference / (player_rating - oponent_rating)
        if rating_difference >= 800:
            return 0.99 * result_factor
        elif rating_difference >= 400:
            return 0.91 * result_factor
        elif rating_difference >= 200:
            return 0.76 * result_factor
        elif rating_difference >= 100:
            return 0.64 * result_factor
        return 0.50 * result_factor

    def getK(self, rating: int, games_played: int = 1) -> int:
        k = 24
        if rating <= 2099:
            k = 32
        elif rating >= 2400:
            k = 16
        return min(int(k * (2 - (1 / 2**(games_played - 1 )))), self.SERIES_OF_GAMES[games_played if games_played < 6 else "6+"])

    def calculate_expected_score(self, player_rating: int, oponent_rating: int) -> float:
        return 1 / (1 + 10 ** (-abs(player_rating - oponent_rating) / 400))

    def calculate_new_rating(self, old_rating: int, oponent_rating: int) -> int:
        return {
            "W": old_rating + self.getK(1- self.calculate_expected_score(old_rating, oponent_rating)),
            "D": old_rating + self.getK(0.5 - self.calculate_expected_score(old_rating, oponent_rating)),
            "L": old_rating + self.getK(0 - self.calculate_expected_score(old_rating, oponent_rating)),
        }



def clear_int(value: str) -> int:
    if not value:
        return None
    try:
        return int(value.replace(",", "").replace(",", "").replace("(", "").replace(")", ""))
    except ValueError:
        return None

def clear_float(value: str) -> float:
    try:
        return float(value.split(" ")[-1].replace("rotate", "").replace("(", "").replace(")", "").replace("deg", "").replace(";", "").replace(" ", ""))
    except ValueError:
        return None


def export_players_data(players_results: dict, export: bool = False) -> None:
    file_result = None
    if export is True:
        file_name = ""
        for player_name in players_results.keys():
            file_name += player_name.replace(" ", "_")+"-"
        file_name = file_name[:-1] + ".txt"
        file_result = open(file_name, mode="w", encoding="utf-8")
    for player, player_games in players_results.items():
        print(f"Jogador: {player}\n", file=file_result)
        for game, game_results in player_games.items():
            print(f"  Jogo: {game}:", file=file_result)
            for result, counter in game_results.items():
                print(f"    {result} - {counter}", file=file_result)
        print("\n", file=file_result)
    if export is True:
        file_result.close()

def print_errors(display_message: str, error_message: str = "") -> None:
    global logger
    logger.error(f"{error_message} | {error_message}")
    messagebox.showerror("Erro", display_message)


def get_player_data(player_name: str) -> dict:
    gamelist_response = get(f"https://games.flyordie.com/players/{player_name}")
    if gamelist_response.status_code != 200:
        print_errors(f"Erro ao obter dados acerca do jogador {player_name}", f"{gamelist_response.status_code}-{gamelist_response.url}")
        return
    gamelist_response = BeautifulSoup(gamelist_response.text, "html.parser")

    game_list = gamelist_response.find("div", class_="F C gameListCenter gameList gameList-wide gameListTab initial-tab")
    if not getattr(game_list, "children", None):
        print_errors(f"Erro ao ler a lista de jogos do jogador {player_name}")
        return

    global players_data
    possible_status_references = (
        gamelist_response.find("div", class_="w currently-online-caption H"),
        gamelist_response.findAll("div", class_="w H")[2],
    )
    players_data[player_name]["Sexo"] = getattr(gamelist_response.find("div", class_="w gender H"), "text", None)
    players_data[player_name]["País"] = getattr(gamelist_response.find("div", class_="w c-l H"), "text", None)
    for ref in possible_status_references:
        players_data[player_name]["Estado"] = getattr(ref, "text", None)
        if players_data[player_name]["Estado"]: break

    for game_name in game_list.children:
        sleep(0.1)
        game_name = game_name.attrs["href"].split("/")[-1]
        gamedata_response = get(f"https://games.flyordie.com/players/{player_name}/{game_name}")
        if gamedata_response.status_code != 200:
            print_errors(f"Erro ao obter os dados do jogo {game_name} do jogador {player_name}", f"{gamedata_response.status_code}-{gamedata_response.url}")
            continue
        
        gamedata_response = BeautifulSoup(gamedata_response.text, "html.parser")

        category = getattr(gamedata_response.find("div", class_="l ratingCategoryName"), "text", None)
        rating = clear_int(getattr(gamedata_response.find("div", class_="w H"), "text", None))
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


if __name__ == "__main__":
    Window().mainloop()
