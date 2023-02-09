from pdb import set_trace
from requests import get
from bs4 import BeautifulSoup
from sys import argv
from math import floor

def clear_int(value: str) -> int:
    return int(value.replace(',', '').replace(',', '').replace('(', '').replace(')', ''))

def clear_float(value: str) -> float:
    return float(value.split(' ')[-1].replace("rotate", "").replace("(", "").replace(")", "").replace("deg", "").replace(";", "").replace(" ", ""))


def get_player_games(player_name: str, errors: list = []) -> dict:
    response = get(f'https://games.flyordie.com/players/{player_name}')
    if response.status_code == 404:
        errors.append(f'Jogador {player_name} não encontrado')
        return
    elif response.status_code == 500:
        errors.append('Erro interno do servidor ao buscar os jogos do jogador')
        return
    elif response.status_code == 200:
        game_data = {}
        soup_response = BeautifulSoup(response.text, 'html.parser')
        if not soup_response:
            errors.append(f'Erro ao ler a lista de jogos do jogador {player_name}')
            return

        for result in soup_response.find_all("a", class_="b gle"):
            game_name = result.attrs["href"].split("/")[-1]
            points, matches = result.text.split('\n')[1:]
            game_data[game_name] = {
                'Pontos': clear_int(points.split(' ')[0]),
                'Partidas': clear_int(matches.split(' ')[0])
            }
        return game_data

def get_player_game_results(player_name: str, game_name: str, total_matches: int, errors: list = []) -> dict:
    response = get(f'https://games.flyordie.com/players/{player_name}/{game_name}')
    if response.status_code == 404:
        errors.append(f'Jogo {game_name} do jogador {player_name} não encontrado')
        return
    elif response.status_code == 500:
        errors.append('Erro interno do servidor ao procurar os resultados do jogo')
        return
    elif response.status_code == 200:
        soup_response = BeautifulSoup(response.text, 'html.parser')
        if not soup_response:
            errors.append(f'Erro ao ler a lista de jogos do jogador {player_name}')
            return

        wins = clear_int(soup_response.find("div", class_="w winCount H").text)

        win_tags = soup_response.find_all("div", class_="pieSegmentInner winsItem") or None
        draw_tag = soup_response.find("div", class_="pieSegmentInner drawsItem") or None
        loss_tag = soup_response.find("div", class_="pieSegmentInner lossesItem") or None

        win_degree = 0
        if win_tags:
            for tag in win_tags:
                win_degree += clear_float(tag.attrs["style"])
        draw_degree = clear_float(draw_tag.attrs["style"]) if draw_tag else 0
        loss_degree = clear_float(loss_tag.attrs["style"]) if loss_tag else 0

        wins_2 = floor((win_degree * total_matches) / 360)
        draws = floor((draw_degree * total_matches) / 360)
        losses = floor((loss_degree * total_matches) / 360)
            
        return {
            'Vitórias': f"{wins}, {round(wins / total_matches * 100, 2)}%",
            'Vitórias_2': f"{wins_2}, {round(wins_2 / total_matches * 100, 2)}%",
            'Empates': f"{draws}, {round(draws / total_matches * 100, 2)}%",
            'Derrotas': f"{losses}, {round(losses / total_matches * 100, 2)}%"
        }


def print_results(players_results: dict, export: bool = False) -> None:
    file_result = None
    if export is True:
        file_result = open('dados_jogadores.txt', mode='w', encoding='utf-8')
    for player, player_games in players_results.items():
        print(f'Jogador: {player}', file=file_result)
        for game, game_results in player_games.items():
            print(f'  Jogo: {game}:', file=file_result)
            for result, matches_counter in game_results.items():
                print(f'    {result} - {matches_counter}', file=file_result)
    if export is True:
        file_result.close()

def print_errors(errors: list) -> None:
    if not errors:
        return
    print('Ocorreram os seguintes erros:')
    for error in errors:
        print(f"\tErro: {error}")
    print('\n\n')


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
            player_results = get_player_game_results(name, game, games[game]['Partidas'], errors)
            if player_results:
                players_results[name][game].update(player_results)
    
    print_errors(errors)
    print_results(players_results, export_result)