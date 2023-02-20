#!/usr/bin/env python
from tkinter import Button, Tk, Entry

# https://www.flyordie.com/games/help/rating_system.html

RATING_DIFFERENCE = {
    0: 0.50,
    100: 0.64,
    200: 0.76,
    400: 0.91,
    800: 0.99,
}

def K(rating: int) -> int:
    if rating >= 0 and rating <= 2099:
        return 32
    if rating >= 2100 and rating <= 2399:
        return 24
    return 16

def calculate_expected_score(rating: int, enemie_rating: int) -> float:
    return 1 / (1 + 10 ** ((enemie_rating - rating) / 400))

def calculate_new_rating(old_rating: int, points: int, enemie_rating: int) -> int:
    return {
        "W": old_rating + K(1- calculate_expected_score(old_rating, enemie_rating)),
        "D": old_rating + K(0.5 - calculate_expected_score(old_rating, enemie_rating)),
        "L": old_rating + K(0 - calculate_expected_score(old_rating, enemie_rating)),
    }

# def calculate_off_decrease()

def print_errors(errors: list) -> None:
    if not errors:
        return
    print('Ocorreram os seguintes erros:')
    for error in errors:
        print(f"  {error}")

def print_results(players_results: dict, export: bool = False) -> None:
    file_result = None
    if export is True:
        file_name = ""
        for player_name in players_results.keys():
             file_name += player_name.replace(" ", "_")+"-"
        file_name = file_name[:-1] + ".txt"
        file_result = open(file_name, mode='w', encoding='utf-8')
    for player, player_games in players_results.items():
        print(f'Jogador: {player}\n', file=file_result)
        for game, game_results in player_games.items():
            print(f'  Jogo: {game}:', file=file_result)
            for result, counter in game_results.items():
                print(f'    {result} - {counter}', file=file_result)
        print("\n", file=file_result)
    if export is True:
        file_result.close()


def maybe_int(value: str, errors: list) -> int:
    try:
        return int(value)
    except:
        errors.append(f'Valor "{value}" não é um número válido')
        return None



if __name__ == '__main__':
    SCREEN_WIDTH, SCREEN_HEIGHT = 1420, 720
    window = Tk(className="Results Formula")
    window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    window.title("Formula de Resultados")
    input1 = Entry(window)
    input1.grid(row=0, column=0, padx=10, pady=10)
    input2 = Entry(window)
    input2.grid(row=1, column=0, padx=10, pady=10)
    generate_button = Button(window, text="Generate")
    generate_button.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
    window.mainloop()
