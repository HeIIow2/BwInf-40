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

        change_hex[hex_1][hex_2] = {Hex.add: add, Hex.remove: remove, Hex.moves: max(add, remove),
                                    Hex.change: add - remove}


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


def get_needed_values_list(hex_from: list, hex_to: list) -> (list, list):
    added = [change_hex[digit1][digit2][Hex.add] for digit1, digit2 in zip(hex_from, hex_to)]
    removed = [change_hex[digit1][digit2][Hex.remove] for digit1, digit2 in zip(hex_from, hex_to)]

    return added, removed

def sum_except_one(list_: list, index: int) -> int:
    return sum(list_[:index]) + sum(list_[index + 1:])

def revert_illegal_moves(hex_from: list, hex_to_: list, max_moves: int) -> list:
    if len(hex_from) <= 0 or len(hex_to_) <= 0:
        raise Exception('hex_from or hex_to is empty. Thus the problem is not in revert_illegal_moves')

    hex_to = hex_to_.copy()

    timeout = 10
    iteration = 0
    # the needed_moves in the while loop is performant enough running in about 5 seconds for 5000 iterations
    current_moves = max_moves + 1
    current_change = 0

    have_been = {}
    for i in range(len(hex_from)):
        have_been[i] = []

    while current_moves > max_moves or current_change != 0:
        iteration += 1
        if iteration > timeout:
            print_hex_list(hex_to)
            raise Exception('Timeout while reverting moves')

        current_adds_list, current_removes_list = get_needed_values_list(hex_from, hex_to)
        current_adds, current_removes = sum(current_adds_list), sum(current_removes_list)
        current_change = current_adds - current_removes
        current_moves = max(current_adds, current_removes)

        # print_hex_list(hex_to)
        # print(f"{needed_adds} - {needed_removes} = {needed_change} -> {needed_moves}")

        for i, from_digit in reversed(list(enumerate(hex_to))):
            if hex_from[i] == from_digit:
                # print(hex_from, hex_to, i)
                continue

            particular_adds = sum_except_one(current_adds_list, i)
            particular_removes = sum_except_one(current_removes_list, i)


            # print(f"{i} {from_digit} move {needed_moves} change {needed_change} specific a{adds} r{removes} m{moves} c{changes}")
            new_digit = -1
            for to_digit in reversed(range(16)):
                # if to_digit == from_digit:
                #     continue
                # if to_digit in have_been[i]:
                #     have_been[i].append(to_digit)
                #     if len(have_been[i]) > 6:
                #         have_been[i].pop(0)
                #     continue
                # have_been[i].append(to_digit)
                # if len(have_been[i]) > 6:
                #     have_been[i].pop(0)

                change_adds = particular_adds + change_hex[hex_from[i]][to_digit][Hex.add]
                change_removes = particular_removes + change_hex[hex_from[i]][to_digit][Hex.remove]
                change_change = change_adds - change_removes
                change_moves = max(change_adds, change_removes)
                print()
                if 0 < current_change and current_change < change_change:
                    continue
                if 0 > current_change and current_change > change_change:
                    continue

                if current_moves == change_moves:
                    if current_adds > change_adds and current_removes == change_removes:
                        new_digit = to_digit
                        break

                    if current_adds == change_adds and current_removes > change_removes:
                        new_digit = to_digit
                        break
                    # if current_adds > change_adds:
                    #     new_digit = to_digit
                    #     break
                    # if current_removes > change_removes:
                    #     new_digit = to_digit
                    #     break
                    # if from_digit < to_digit:
                    #     new_digit = to_digit
                    #     break

                    continue

                if current_moves > change_moves >= 0:
                    new_digit = to_digit
                    break


            if new_digit != -1:
                print("current")
                print(current_adds, current_removes, current_change, current_moves)
                print("changed")
                print(change_adds, change_removes, change_change, change_moves)
                print(f"changing {from_digit} to {to_digit} at digit {i}")
                new_digit = to_digit
                break

        if new_digit == -1:
            pass
            # print_hex_list(hex_to)
            logging.warning('No digit found to revert illegal moves (if it occurs only once, it is not an error)')
        else:
            hex_to[i] = new_digit

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
    execute_file(0)
    # for elem in change_hex[15]:
    #     print(change_hex[15][elem])
