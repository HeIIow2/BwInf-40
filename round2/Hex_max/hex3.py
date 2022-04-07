import json
import numpy as np
import logging
import enum

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Hex(enum.Enum):
    add = "add"
    remove = "remove"
    moves = "moves"
    change = "change"

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

# fill up change hex
# liste wie viele striche man von jeder zu jeder zahl hinzufügen bzw. wegnehmen muss.
change_hex = {}
for hex_1, hex_matrix_1 in enumerate(hex_matrix):
    change_hex[hex_1] = {}

    for hex_2, hex_matrix_2 in enumerate(hex_matrix):
        remove = 0
        add = 0
        for bool1, bool2 in zip(hex_matrix_1, hex_matrix_2):
            if bool1 and not bool2:
                remove += 1
            elif not bool1 and bool2:
                add += 1

        change_hex[hex_1][hex_2] = {Hex.add: add, Hex.remove: remove, Hex.moves: max(add, remove), Hex.change: add - remove}


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

def needed_value_between_hex(hex_from: list, hex_to: list) -> (int, int):
    # get needed moves between two hex numbers
    total_added = 0
    total_removed = 0

    for from_digit, to_digit in zip(hex_from, hex_to):
        total_added += change_hex[from_digit][to_digit][Hex.add]
        total_removed += change_hex[from_digit][to_digit][Hex.remove]

    return total_added, total_removed

def needed_moves_between_hex(hex_from: list, hex_to: list) -> int:
    # get needed moves between two hex numbers
    total_added, total_removed = needed_value_between_hex(hex_from, hex_to)

    if total_added != total_removed:
        logging.warning(f"{total_added} != {total_removed}")
        logging.warning(f"{hex_1} -> {hex_2}")

    return max(total_added, total_removed)

def revert_illegal_moves(hex_from: list, hex_to_: list, max_moves: int) -> list:
    if len(hex_from) <= 0 or len(hex_to_) <= 0:
        raise Exception('hex_from or hex_to is empty. Thus the problem is not in revert_illegal_moves')

    hex_to = hex_to_.copy()

    timeout = 5000
    iteration = 0
    # the needed_moves in the while loop is performant enough running in about 5 seconds for 5000 iterations
    needed_moves = 1
    needed_change = 0
    while needed_moves > 0 or needed_change != 0:
        iteration += 1
        if iteration > timeout:
            return hex_to
            print_hex_list(hex_to)
            raise Exception('Timeout while reverting moves')


        needed_adds, needed_removes = needed_value_between_hex(hex_from, hex_to)
        print(needed_adds, needed_removes)
        needed_moves = max(needed_adds, needed_removes) - max_moves
        needed_change = needed_adds - needed_removes

        # print_hex_list(hex_to)
        # print(f"{needed_adds} - {needed_removes} = {needed_change} -> {needed_moves}")

        for i, from_digit in reversed(list(enumerate(hex_to))):
            if hex_from[i] == from_digit:
                # print(hex_from, hex_to, i)
                continue

            adds = change_hex[hex_from[i]][from_digit][Hex.add]
            removes = change_hex[hex_from[i]][from_digit][Hex.remove]
            # print(f"{i} {from_digit} specific a{adds} r{removes}")

            if needed_change < 0:
                if needed_change < adds:
                    adds = 0
                else:
                    adds -= needed_change
            elif needed_change > 0:
                if needed_change > removes:
                    removes = 0
                else:
                    removes += needed_change

            moves = max(adds, removes)
            changes = adds - removes

            # print(f"{i} {from_digit} move {needed_moves} change {needed_change} specific a{adds} r{removes} m{moves} c{changes}")
            new_digit = -1
            for to_digit in reversed(range(16)):
                iter_adds = change_hex[hex_from[i]][to_digit][Hex.add]
                iter_removes = change_hex[hex_from[i]][to_digit][Hex.remove]


                if needed_change < 0:
                    if needed_change < iter_adds:
                        iter_adds = 0
                    else:
                        iter_adds -= needed_change
                elif needed_change > 0:
                    if needed_change > iter_removes:
                        iter_removes = 0
                    else:
                        iter_removes += needed_change


                iter_change = iter_adds - iter_removes
                iter_moves = max(iter_adds, iter_removes)

                # print(f"iter {i} {to_digit} add {iter_adds} remove {iter_removes} move {iter_moves} change {iter_change}")

                if changes > 0 and iter_change > changes:   continue
                if changes < 0 and iter_change < changes:   continue

                if iter_moves < moves:
                    if moves - iter_moves > needed_moves:
                        continue
                    new_digit = to_digit
                    break

            if new_digit != -1:
                break


        if new_digit == -1:
            pass
            # print_hex_list(hex_to)
            # logging.warning('No digit found to revert illegal moves (if it occurs only once, it is not an error)')
        else:   hex_to[i] = new_digit


    return hex_to


def execute_file(file_number: int = 0) -> list:
    # read example file
    with open(f'examples/hexmax{file_number}.txt') as f:
        hex_str, moves = f.read().splitlines()
        moves = int(moves)
        hex_number = [int(digit, 16) for digit in hex_str]
        logging.info(f'Moves: {moves}')
        logging.info(f'Hex: {hex_str}')

    hex_length = len(hex_str)
    stick_count = get_sticks(hex_str)

    logging.info(f'hex length: {hex_length}')
    logging.info(f'Sticks: {stick_count}')

    with_infinite_moves = get_biggest_hex_infinite(stick_count, hex_length)
    print_hex_list(with_infinite_moves)

    # get needed moves between hex numbers
    needed_moves = needed_moves_between_hex(hex_number, with_infinite_moves)
    logging.info(f'Needed moves: {needed_moves}')

    # revert the moves that arent possible
    if needed_moves <= moves:
        return with_infinite_moves

    solution = revert_illegal_moves(hex_number, with_infinite_moves, moves)
    print_hex_list(solution)
    print(needed_value_between_hex(hex_number, solution))
    return solution



if __name__ == '__main__':
    execute_file(4)
    # for elem in change_hex[15]:
    #     print(change_hex[15][elem])
