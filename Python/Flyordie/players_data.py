#!/usr/bin/env python

from requests import get
from bs4 import BeautifulSoup
from sys import argv
from math import floor
from time import sleep
from utils import clear_int, clear_float


def get_player_games(player_name: str, errors: list = []) -> dict:
    response = get(f'https://games.flyordie.com/players/{player_name}')
    if response.status_code >= 500:
        errors.append('Erro interno do servidor ao buscar os jogos do jogador')
        return
    elif response.status_code == 404:
        errors.append(f'Jogador {player_name} não encontrado')
        return
    elif response.status_code == 200:
        game_data = {}
        soup_response = BeautifulSoup(response.text, 'html.parser')
        if not soup_response:
            errors.append(f'Erro ao ler a lista de jogos do jogador {player_name}')
            return

        game_list = soup_response.find("div", class_="F C gameListCenter gameList gameList-wide gameListTab initial-tab")
        if getattr(game_list, "children", None) is None:
            errors.append(f'Erro ao ler a lista de jogos do jogador {player_name}')
            return
        for result in game_list.children:
            game_name = result.attrs["href"].split("/")[-1]
            points, matches = result.text.split('\n')[1:]
            game_data[game_name] = {
                'Pontos': clear_int(points.split(' ')[0]),
                'Partidas': clear_int(matches.split(' ')[0])
            }
        return game_data

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

def print_errors(errors: list) -> None:
    if not errors:
        return
    print('Ocorreram os seguintes erros:')
    for error in errors:
        print(f"  {error}")


if __name__ == '__main__':
    players_results, errors = {}, []
    players_names = argv[1:]
    export_result = False
    if "export" in players_names:
        export_result = True
        players_names.remove("export")

    if not players_names:
        errors.append('Informe os nomes dos jogadores')
        print_errors(errors)
        exit()

    for name in players_names:
        player_games = get_player_games(name, errors)
        if player_games:
            players_results[name] = player_games
    
    for name, games in players_results.items():
        for game in games:
            results = get_player_game_results(name, game, games[game]['Partidas'], errors)
            if results:
                players_results[name][game].update(results)
    
    print_errors(errors)
    print_results(players_results, export_result)