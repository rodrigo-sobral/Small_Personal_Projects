import tkinter as tk
from requests import get
from bs4 import BeautifulSoup
from math import floor
from time import sleep


NORMAL_FONT, TITLE_FONT = ("Arial", 12), ("Arial", 24)
BG_COLOR = "#282c34"
TEXT_PROPS = {"bg": BG_COLOR, "fg": "white", "font": NORMAL_FONT}
TITLE_PROPS = {"bg": BG_COLOR, "fg": "white", "font": TITLE_FONT}
GREEN_BUTTON_PROPS = {"bg": "green", "fg": "white", "font": NORMAL_FONT}
DARKRED_BUTTON_PROPS = {"bg": "darkred", "fg": "white", "font": NORMAL_FONT}
LIGHTBLUE_BUTTON_PROPS = {"bg": "lightblue", "fg": "black", "font": NORMAL_FONT}

MONTHS = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}


def add_player_input_field(frame: tk.Frame, placeholder: str = "Nome do Jogador", can_delete: bool = False, **kwargs) -> None:
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

    

def clear_int(value: str) -> int:
    if not value:
        return 0
    return int(value.replace(",", "").replace(",", "").replace("(", "").replace(")", ""))

def clear_float(value: str) -> float:
    return float(value.split(" ")[-1].replace("rotate", "").replace("(", "").replace(")", "").replace("deg", "").replace(";", "").replace(" ", ""))


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

def print_errors(errors: list) -> None:
    if not errors:
        return
    print("Ocorreram os seguintes erros:")
    for error in errors:
        print(f"  {error}")


def get_player_data(player_name: str, errors: list = []) -> dict:
    gamelist_response = get(f"https://games.flyordie.com/players/{player_name}")
    if gamelist_response.status_code != 200:
        errors.append(f"Erro ao obter dados acerca do jogador {player_name} [{gamelist_response.status_code}]")
        return
    gamelist_response = BeautifulSoup(gamelist_response.text, "html.parser")

    game_list = gamelist_response.find("div", class_="F C gameListCenter gameList gameList-wide gameListTab initial-tab")
    if not getattr(game_list, "children", None):
        errors.append(f"Erro ao ler a lista de jogos do jogador {player_name}")
        return

    player_data, gender, country, status, joined_at = {}, None, None, None, None
    for game_name in game_list.children:
        sleep(0.1)
        game_name = game_name.attrs["href"].split("/")[-1]
        gamedata_response = get(f"https://games.flyordie.com/players/{player_name}/{game_name}")
        if gamedata_response.status_code != 200:
            errors.append(f"Erro ao obter os dados do jogo {game_name} do jogador {player_name} [{gamedata_response.status_code}]")
            continue
        gamedata_response = BeautifulSoup(gamedata_response.text, "html.parser")

        if gender is None:
            gender = getattr(gamedata_response.find("div", class_="w gender H"), "text", None)
        if country is None:
            country = getattr(gamedata_response.find("div", class_="w c-l H"), "text", None)
        if status is None:
            status = getattr(gamedata_response.find("div", class_="w currently-online-caption H"), "text", None)
            if status is None:
                status = getattr(gamedata_response.find("div", class_="w H"), "text", None)
        if joined_at is None:
            joined_at = getattr(gamedata_response.find("div", class_="H"), "text", None)
            if joined_at is not None:
                joined_at = joined_at.split("/")
                joined_at = f"{joined_at[1]} de {MONTHS[int(joined_at[0])]} de {joined_at[2]}"

        rating = clear_int(getattr(gamedata_response.find("div", class_="w H"), "text", None))
        total_matches = clear_int(getattr(gamedata_response.find("td", class_="w matchCount"), "text", None))
        player_data[game_name] = {
            "Pontuação": rating, "Total de Partidas": total_matches,
            "Vitórias": {}, "Empates": {}, "Derrotas": {}
        }
        
        loss_degree = 0
        loss_tag = gamedata_response.find("div", class_="pieSegmentInner lossesItem") or None
        if loss_tag:
            loss_degree = 360 - clear_float(loss_tag.parent.attrs["style"])
        
        draw_degree = 0
        draw_tag = gamedata_response.find("div", class_="pieSegmentInner drawsItem") or None
        if draw_tag:
            if loss_degree == 0:
                draw_degree = 360 - clear_float(draw_tag.parent.attrs["style"])
            else:
                draw_degree = clear_float(loss_tag.parent.attrs["style"]) - clear_float(draw_tag.parent.attrs["style"])

        wins = clear_int(gamedata_response.find("div", class_="w winCount H").text)
        draws = floor((draw_degree * total_matches) / 360)
        losses = floor((loss_degree * total_matches) / 360)
            
        player_data[game_name]["Vitórias"] = {
            "Total": wins, "Percentagem": round(wins / total_matches * 100, 2)
        }
        player_data[game_name]["Empates"] = {
            "Total": draws, "Percentagem": round(draws / total_matches * 100, 2)
        }
        player_data[game_name]["Derrotas"] = {
                "Total": losses, "Percentagem": round(losses / total_matches * 100, 2)
            }

        return {
            "Sexo": gender,
            "País": country,
            "Estado": status,
            "Data de Registo": joined_at,
            "Jogos": player_data,
        }


# Prof. Arpad Elo"s Formula - https://www.flyordie.com/games/help/rating_system.html

SERIES_OF_GAMES = { 1: 16, 2: 24, 3: 28, 4: 30, 5: 31, "6+": 32 }

def calculate_winning_probability(player_rating: int, oponent_rating: int) -> int:
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

def getK(rating: int, games_played: int = 1) -> int:
    k = 24
    if rating <= 2099:
        k = 32
    elif rating >= 2400:
        k = 16
    return min(int(k * (2 - (1 / 2**(games_played - 1 )))), SERIES_OF_GAMES[games_played if games_played < 6 else "6+"])

def calculate_expected_score(player_rating: int, oponent_rating: int) -> float:
    return 1 / (1 + 10 ** (-abs(player_rating - oponent_rating) / 400))

def calculate_new_rating(old_rating: int, oponent_rating: int) -> int:
    return {
        "W": old_rating + getK(1- calculate_expected_score(old_rating, oponent_rating)),
        "D": old_rating + getK(0.5 - calculate_expected_score(old_rating, oponent_rating)),
        "L": old_rating + getK(0 - calculate_expected_score(old_rating, oponent_rating)),
    }
