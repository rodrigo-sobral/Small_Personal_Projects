#!/usr/bin/env python
from sys import argv

# https://www.flyordie.com/games/help/rating_system.html

def print_errors(errors: list) -> None:
    if not errors:
        return
    print('Ocorreram os seguintes erros:')
    for error in errors:
        print(f"  {error}")


if __name__ == '__main__':
    errors = {}
    if len(argv) != 3:
        errors.append('Execute o programa da seguinte forma: python3 results_formula.py <pontos do jogador> <pontos do oponente>')
        print_errors(errors)
        exit()
    my_points, enemie_points = argv[1:3]

    print_errors(errors)
