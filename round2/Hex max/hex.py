import json
import logging
import enum
from dataclasses import dataclass
import numpy as np

logging.basicConfig(level=logging.INFO)

EXAMPLE = 5
hex_number = []
MOVES = 0
FREE_ADDS = 0
FREE_REMOVES = 0
# [zahl vorher][zahl nacher][add remove]
change_hex = {}

history = []
@dataclass
class Step:
    hex_number: list
    moves_left: int
    free_adds: int
    free_removes: int
    last_move: int = 0
    possible_moves = None

    def skip_to_next_move(self):
        self.last_move += 1
        if self.possible_moves[self.last_move].digit == -1:
            return False
        return True

    def next_move(self):
        hex_number_ = self.hex_number.copy()
        if self.possible_moves is None:
            self.possible_moves = np.sort(np.array([hex_digit.best_move(self.moves_left) for hex_digit in self.hex_number]))[::-1]
        best_move = self.possible_moves[self.last_move]
        if best_move.digit == -1:
            return None
        moves_left = self.moves_left
        free_adds = self.free_adds
        free_removes = self.free_removes

        moves_left -= best_move.moves
        free_adds -= best_move.add
        free_removes -= best_move.remove

        if free_adds < 0:
            free_removes = abs(free_adds)
            free_adds = 0
        if free_removes < 0:
            free_adds = abs(free_removes)
            free_removes = 0

        self.last_move += 1

        hex_number_[best_move.digit].execute_move(best_move)
        logging.debug(f"executing {best_move} at {hex_number_[best_move.digit]}")

        return Step(hex_number_, moves_left, free_adds, free_removes)


SEGMENTS = 7

class Hex(enum.Enum):
    add = "add"
    remove = "remove"

@dataclass
class Move:
    moves: int
    add: int
    remove: int
    score: float
    from_: int
    to: int
    digit: int
    base: int = 16

    def __lt__(self, other):
        if self.digit == other.digit:
            return self.score < other.score
        if not self.score:
            return True
        if not other.score:
            return False
        return self.digit < other.digit
        # return self.score * self.base**self.digit < other.score * other.base**other.digit

# klasse einer Hex ziffer
class HexDigit:
    def __init__(self, value, digit: int, base: int=16):
        self.value = int(value, base)
        self.digit = digit
        self.base = base

    def __str__(self):
        return f"(value: {self.value}, digit: {self.digit})"

    def best_move(self, moves_left: int):
        best_move = Move(-1, -1, -1, -1, -1, -1, -1)
        for i in range(self.value+1, self.base):
            add = add_for_max = change_hex[self.value][i][Hex.add]
            remove = remove_for_max = change_hex[self.value][i][Hex.remove]

            if add > remove:
                add, remove = add-remove, 0
            else:
                add, remove = 0, remove-add

            if FREE_ADDS < add_for_max:
                add_for_max -= FREE_ADDS
            else:
                add_for_max = 0

            if FREE_REMOVES < remove_for_max:
                remove_for_max -= FREE_REMOVES
            else:
                remove_for_max = 0

            moves = max(add_for_max, remove_for_max)
            if moves > moves_left:
                continue
            if FREE_ADDS - add != 0:
                continue
            if FREE_REMOVES - remove != 0:
                continue

            # +1 weil div by 0
            score = i / (moves+1)

            move = Move(moves, add, remove, score, self.value, i, self.digit)

            if move > best_move:
                best_move = move
        return best_move

    def execute_move(self, move):
        self.value = move.to

# read example file
with open(f'examples/hexmax{EXAMPLE}.txt') as f:
    hex_str, moves = f.read().splitlines()
    MOVES = int(moves)
    logging.info(f'Moves: {MOVES}')
    logging.info(f'Hex: {hex_str}')
    for i, digit in enumerate(reversed(hex_str)):
        hex_number.append(HexDigit(digit, i))

# read hex.json and store as hex matrix
with open('hex.json') as f:
    hex_matrix = json.load(f)

logging.info(hex_matrix)

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

timeout = MOVES
iteration = 0
history.append(Step(hex_number, MOVES, FREE_ADDS, FREE_REMOVES))
while history[-1].moves_left > 0:
    new_move = history[-1].next_move()
    if new_move is None:
        while True:
            if history[-1].skip_to_next_move():
                break
            else:
                history.pop()
                timeout -= 1
        continue
    history.append(new_move)

    iteration += 1
    if iteration > timeout:
        logging.error("timeout")
        break

logging.info(f"Moves: {MOVES}")
logging.info(f"Free adds: {FREE_ADDS}")
logging.info(f"Free removes: {FREE_REMOVES}")

number = ""
for hex_digit in reversed(hex_number):
    number += f"{hex_digit.value:x}"
logging.info(f"Number: 0x{number}")
