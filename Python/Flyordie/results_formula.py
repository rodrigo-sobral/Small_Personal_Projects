#!/usr/bin/env python
from math import floor
from time import sleep
from sys import argv
from bs4 import BeautifulSoup
from requests import get
from utils import clear_int, clear_float

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

def print_errors(errors: list) -> None:
    if not errors:
        return
    print('Ocorreram os seguintes erros:')
    for error in errors:
        print(f"  {error}")


def get_player_game_results(player_name: str, game_name: str, total_matches: int, errors: list = []) -> dict:
    if total_matches == 0:
        return {'Vitórias': '0, 0%', 'Empates': '0, 0%', 'Derrotas': '0, 0%'}
    
    response = get(f'https://games.flyordie.com/players/{player_name}/{game_name}')
    sleep(0.1)
    if response.status_code >= 500:
        errors.append(f'Erro interno do servidor ao procurar os resultados do jogo {game_name} do jogador {player_name}')
        return
    if response.status_code == 404:
        errors.append(f'Jogo {game_name} do jogador {player_name} não encontrado')
        return
    elif response.status_code == 200:
        soup_response = BeautifulSoup(response.text, 'html.parser')
        if not soup_response:
            errors.append(f'Erro ao ler a lista de jogos do jogador {player_name}')
            return

        wins = clear_int(soup_response.find("div", class_="w winCount H").text)
        
        loss_tag = soup_response.find("div", class_="pieSegmentInner lossesItem") or None
        draw_tag = soup_response.find("div", class_="pieSegmentInner drawsItem") or None
        
        loss_degree = 0
        if loss_tag:
            loss_degree = 360 - clear_float(loss_tag.parent.attrs["style"])
        
        draw_degree = 0
        if draw_tag:
            if loss_degree == 0:
                draw_degree = 360 - clear_float(draw_tag.parent.attrs["style"])
            else:
                draw_degree = clear_float(loss_tag.parent.attrs["style"]) - clear_float(draw_tag.parent.attrs["style"])

        draws = floor((draw_degree * total_matches) / 360)
        losses = floor((loss_degree * total_matches) / 360)
            
        return {
            'Vitórias': f"{wins}, {round(wins / total_matches * 100, 2)}%",
            'Empates': f"{draws}, {round(draws / total_matches * 100, 2)}%",
            'Derrotas': f"{losses}, {round(losses / total_matches * 100, 2)}%"
        }
    else:
        errors.append(f'Erro desconhecido ao buscar os resultados do jogo {game_name} do jogador {player_name}')
        return


if __name__ == '__main__':
    errors = {}
    if len(argv) != 3:
        errors.append('Execute o programa da seguinte forma: python3 results_formula.py <nome do jogador1> <nome do jogador2>')
        print_errors(errors)
        exit()
    my_points, enemie_points = argv[1:3]

    print_errors(errors)
