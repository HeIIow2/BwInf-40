import json
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

# read hex.json and store as hex matrix
"""
hex matrix: list of all states of the seven segment display for every hex number
hex sticks: a dictionary with the key being the value of the hex number and the value the number of sticks
"""
with open('hex.json') as f:
    hex_matrix = json.load(f)
    hex_sticks = {}

    # count sticks and save as in dictionary
    for i, number in enumerate(hex_matrix):
        hex_sticks[i] = np.sum(number)
    hex_sticks = dict(sorted(hex_sticks.items(), key=lambda x: x[1]))

    logging.info(hex_matrix)
    logging.info(hex_sticks)

def print_hex_list(hex_list: list):
    print(''.join([f"{digit:x}" for digit in hex_list]))

def get_sticks(hex_str: str):
    sticks = 0
    for digit in hex_str:
        sticks += hex_sticks[int(digit, 16)]
    return sticks


def get_biggest_hex_infinite(sticks: int, hex_length: int):
    # get biggest hex number with infinite moves
    leftovers = sticks

    min_sticks = hex_sticks[list(hex_sticks)[0]]
    max_sticks = hex_sticks[list(hex_sticks)[-1]]

    # list with integers for each digit
    hex_number = []
    for i in range(hex_length):
        leftover_digits = hex_length - i - 1

        for j in reversed(range(16)):
            possible_leftovers = leftovers - hex_sticks[j]

            if possible_leftovers == 0 and leftover_digits == 0:
                hex_number.append(j)
                break

            if leftover_digits == 0:
                continue

            if possible_leftovers < 0:
                continue
            sticks_per_digit = possible_leftovers / leftover_digits

            if sticks_per_digit < min_sticks:
                continue
            if sticks_per_digit > max_sticks:
                continue

            leftovers = possible_leftovers
            hex_number.append(j)
            break

    if len(hex_number) != hex_length:
        raise Exception('Numbers dont match while generating the biggest hex number with infinite moves')

    return hex_number


def execute_file(file_number: int = 0):
    # read example file
    with open(f'examples/hexmax{file_number}.txt') as f:
        hex_str, moves = f.read().splitlines()
        moves = int(moves)
        logging.info(f'Moves: {moves}')
        logging.info(f'Hex: {hex_str}')

    hex_length = len(hex_str)
    stick_count = get_sticks(hex_str)

    logging.info(f'hex length: {hex_length}')
    logging.info(f'Sticks: {stick_count}')

    with_infinite_moves = get_biggest_hex_infinite(stick_count, hex_length)
    print_hex_list(with_infinite_moves)


if __name__ == '__main__':
    execute_file(5)
