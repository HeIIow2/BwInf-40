# from turtle import *

from PIL import Image
import json
import logging
import enum
from dataclasses import dataclass
import numpy as np
import copy

logging.basicConfig(level=logging.WARNING)


class Hex(enum.Enum):
    add = "add"
    remove = "remove"


# [zahl vorher][zahl nacher][add remove]
hex_matrix = []
change_hex = {}

SEGMENTS = 7

# read hex.json and store as hex matrix
with open('hex.json') as f:
    hex_matrix = json.load(f)
    logging.info(hex_matrix)

# fill up change hex
# liste wie viele striche man von jeder zu jeder zahl hinzufügen bzw. wegnehmen muss.
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

        change_hex[hex_1][hex_2] = {Hex.add: add, Hex.remove: remove}


@dataclass
class Move:
    moves: int
    add: int
    remove: int
    score: float
    from_: int
    to: int
    digit: int
    free_adds: int
    free_removes: int
    moves_left: int
    base: int = 16

    def __lt__(self, other):
        if self.digit == other.digit:
            if self.score == other.score:
                return self.free_adds + self.free_removes > other.free_adds + other.free_removes
            return self.score < other.score
        if not self.score:
            return True
        if not other.score:
            return False
        return self.digit < other.digit
        # return self.score * self.base**self.digit < other.score * other.base**other.digit


# klasse einer Hex ziffer
class HexDigit:
    def __init__(self, value, digit: int, base: int = 16):
        self.value = int(value, base)
        self.digit = digit
        self.base = base

    def __str__(self):
        return f"(value: {self.value}, digit: {self.digit})"

    def get_move(self, i, moves_left, free_adds, free_removes):
        add = change_hex[self.value][i][Hex.add]
        remove = change_hex[self.value][i][Hex.remove]

        # substrahiere die kostenlose zuege von den gebrauchten
        if free_adds > 0:
            add -= free_adds
            if add < 0:
                free_adds = abs(add)
                add = 0
            else:
                free_adds = 0

        if free_removes > 0:
            remove -= free_removes
            if remove < 0:
                free_removes = abs(remove)
                remove = 0
            else:
                free_removes = 0

        moves = max(add, remove)

        if add > remove:
            free_removes += add - remove
        else:
            free_adds += remove - add

        moves_left -= moves

        if moves_left < 0:
            return None

        if moves_left <= 0 and free_adds > 0:
            return None
        if moves_left <= 0 and free_removes > 0:
            return None

        # +1 weil div by 0
        score = i / (moves + 1)

        return Move(moves, add, remove, score, self.value, i, self.digit, free_adds, free_removes, moves_left)

    def best_move(self, level: int, moves_left: int, free_adds: int, free_removes: int):
        moves = np.array(
            [self.get_move(i, moves_left, free_adds, free_removes) for i in range(self.value + 1, self.base)])
        moves = np.sort(moves)[::-1]
        return moves[level]

    def get_moves(self, moves_left: int, free_adds: int, free_removes: int):
        if self.value == 15:
            return np.array([])

        return_moves = []
        for i in range(self.value + 1, self.base):
            if i == self.value:
                continue
            temp_res = self.get_move(i, moves_left, free_adds, free_removes)
            if temp_res is not None:
                return_moves.append(temp_res)

        return np.array(return_moves)

    def get_worse_moves(self, moves_left: int, free_adds: int, free_removes: int):
        return_moves = []
        # for i in range(self.value + 1, self.base):
        for i in range(0, self.value):
            if i == self.value:
                continue
            temp_res = self.get_move(i, moves_left, free_adds, free_removes)
            if temp_res is not None:
                return_moves.append(temp_res)

        return np.array(return_moves)

    def execute_move(self, move):
        self.value = move.to


@dataclass
class Step:
    hex_number: list
    moves_left: int
    free_adds: int
    free_removes: int
    prev_move: int = 0
    last_move: int = 0
    possible_moves = None
    is_worse = False

    def __str__(self):
        return f"{self.print_num()} (moves: {self.moves_left}, adds: {self.free_adds}, removes: {self.free_removes})"

    def __lt__(self, other):
        if self.free_adds or self.free_removes:
            return True
        if other.free_adds or other.free_removes:
            return False

        for digit1, digit2 in zip(self.hex_number, other.hex_number):
            if digit1.digit != digit2.digit:
                raise Exception("'hex_number' in {self} and {other} is not sorted")
            if digit1.value != digit2.value:
                return digit1.value < digit2.value

    def next_move(self, prev_move: int = 0):
        # print(self.moves_left, self.free_adds, self.free_removes)
        hex_number_ = copy.deepcopy(self.hex_number)

        const = 500

        lower_bound = const
        if prev_move < const:
            lower_bound = prev_move

        if self.possible_moves is None:
            flattened_array = np.hstack(
                [hex_digit.get_moves(self.moves_left, self.free_adds, self.free_removes) for hex_digit in
                 hex_number_[prev_move-lower_bound:]])
            self.possible_moves = np.sort(flattened_array)[::-1]

        if self.last_move >= len(self.possible_moves):
            if self.is_worse:
                return None

            self.last_move = 0
            flattened_array = np.hstack(
                [hex_digit.get_worse_moves(self.moves_left, self.free_adds, self.free_removes) for hex_digit in
                 hex_number_])
            self.possible_moves = np.sort(flattened_array)[::-1]
            self.is_worse = True

            if self.last_move >= len(self.possible_moves):
                return None


        best_move = self.possible_moves[self.last_move]
        prev_move = best_move.digit

        hex_number_[best_move.digit].execute_move(best_move)
        self.last_move += 1
        
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(f"executing {best_move} at {hex_number_[best_move.digit]}")

        return Step(hex_number_, best_move.moves_left, best_move.free_adds, best_move.free_removes, prev_move)

    def print_num(self):
        return "".join([f"{hex_digit.value:x}" for hex_digit in reversed(self.hex_number)])


def main(hex_number: list, MOVES: int):
    
    FREE_ADDS = 0
    FREE_REMOVES = 0
    history = [Step(hex_number, MOVES, FREE_ADDS, FREE_REMOVES)]

    biggest_history = copy.deepcopy(history)

    # just a timeout that I dont get stuck in an infinite loop
    timeout = MOVES
    iteration = 0
    
    thing = 0
    prev_move = len(hex_number) - 1
    while history[-1].moves_left > 0 or history[-1].free_removes > 0 or history[-1].free_adds > 0:
        new_move = history[-1].next_move(prev_move)
        
        prev_move = new_move.prev_move
        print(len(history), prev_move)

        if new_move is None:
            print("is none")
            history.pop(-1)
            iteration -= 1

            if not len(history):
                break

            continue

            # wenn es keine neue mögliche Zuege gibt, dann
            # breche ab und nehme das bisher beste ergebnis
            # moegliches Problem eines lokalen minnimums.
        if not len(history):
            break

        logging.info(new_move)
        history.append(new_move)

        #iteration += 1
        if iteration > timeout:
            logging.error("timeout")
            break

        # keep the history resulting in the biggest end result
        if history[-1] > biggest_history[-1]:
            biggest_history = copy.deepcopy(history)
            logging.info(biggest_history[-1].print_num())

    MOVES = biggest_history[-1].moves_left
    FREE_ADDS = biggest_history[-1].free_adds
    FREE_REMOVES = biggest_history[-1].free_removes

    for step in history:
        print(step)

    print(f"Moves: {MOVES}")
    print(f"Free adds: {FREE_ADDS}")
    print(f"Free removes: {FREE_REMOVES}")

    number = biggest_history[-1].print_num()
    print(f"biggest Number: 0x{number}")
    return number

def execute_file(EXAMPLE: int = 0):
    # read example file
    hex_number = []
    MOVES = 0
    with open(f'examples/hexmax{EXAMPLE}.txt') as f:
        hex_str, moves = f.read().splitlines()
        MOVES = int(moves)
        logging.info(f'Moves: {MOVES}')
        logging.info(f'Hex: {hex_str}')
        for i, digit in enumerate(reversed(hex_str)):
            hex_number.append(HexDigit(digit, i))

    sollution = main(hex_number, MOVES)

    print(f"Sollution: {sollution}")

    length = 20
    gap = 10
    thickness = 1
    digits = len(hex_number)
    # create pillow image
    img = Image.new('RGB', ((length + gap) * digits + gap, (length + length + gap) * (MOVES+1) + gap), color='white')

    start_hex = [hex_matrix[int(i, 16)].copy() for i in hex_str]
    end_hex = [hex_matrix[int(i, 16)].copy() for i in sollution]

    img = draw_digits(img,start_hex, 0, MOVES+1, length=length, gap=gap, thickness=thickness)
    for i in range(MOVES):
        add = False
        remove = False
        to_break = False
        for j, (digit1, digit2) in enumerate(zip(start_hex, end_hex)):
            for k, (bit1, bit2) in enumerate(zip(digit1, digit2)):
                if bit1 and (not bit2) and not add:
                    add = True
                    start_hex[j][k] = bit2
                    if remove:
                        to_break = True
                        break
                elif (not bit1) and bit2 and not remove:
                    remove = True
                    start_hex[j][k] = bit2
                    if add:
                        to_break = True
                        break

            if to_break:
                break

        img = draw_digits(img, start_hex, i+1, MOVES+1, length=length, gap=gap, thickness=thickness)

    img.save(f'examples/hexmax{EXAMPLE}.png')


def draw_digits(img, hex_number: list, move: int, total_moves:int, length: int = 10, gap: int = 5, thickness: int = 2):
    height = move * (gap+length+length) + gap
    digits = len(hex_number)
    
    
    first_pos = gap
    for i, digit in enumerate(hex_number):
        if digit[0]:    img.paste(Image.new('RGB', (length, thickness), color='black'), (first_pos + i * (length + gap), height))   
        if digit[1]:    img.paste(Image.new('RGB', (length, thickness), color='black'), (first_pos + i * (length + gap), height+length))
        if digit[2]:    img.paste(Image.new('RGB', (length, thickness), color='black'), (first_pos + i * (length + gap), height+length*2))  
        if digit[3]:    img.paste(Image.new('RGB', (thickness, length), color='black'), (first_pos + i * (length + gap), height))  
        if digit[4]:    img.paste(Image.new('RGB', (thickness, length), color='black'), (first_pos + i * (length + gap) + length, height))   
        if digit[5]:    img.paste(Image.new('RGB', (thickness, length), color='black'), (first_pos + i * (length + gap), height+length)) 
        if digit[6]:    img.paste(Image.new('RGB', (thickness, length), color='black'), (first_pos + i * (length + gap) + length, height+length))   

    return img   

if __name__ == "__main__":
    execute_file(5)
