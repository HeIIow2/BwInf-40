import json
import logging
import enum
from dataclasses import dataclass
import numpy as np
import copy

logging.basicConfig(level=logging.INFO)

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
class Step:
    hex_number: list
    moves_left: int
    free_adds: int
    free_removes: int
    last_move: int = 0
    possible_moves = None
    level: int = 0

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

    def skip_to_next_move(self):
        self.last_move += 1
        if self.last_move >= len(self.possible_moves) or self.possible_moves[self.last_move].digit == -1:
            self.level += 1
            self.possible_moves = np.sort(np.array([hex_digit.best_move(self.level, self.moves_left, self.free_adds, self.free_removes) for hex_digit in self.hex_number]))[::-1]
        return True

    def next_move(self):
        # print(self.moves_left, self.free_adds, self.free_removes)
        hex_number_ = self.hex_number.copy()
        if self.possible_moves is None:
            self.possible_moves = np.sort(np.array([hex_digit.best_move(self.level, self.moves_left, self.free_adds, self.free_removes) for hex_digit in self.hex_number]))[::-1]
        
        best_move = self.possible_moves[self.last_move]
        if best_move.digit == -1:
            return None

        moves_left = self.moves_left - best_move.moves
        """
        free_adds = best_move.free_adds
        free_removes = best_move.free_removes

        moves_left -= best_move.moves
        free_adds += best_move.remove
        free_removes += best_move.add
        """

        self.last_move += 1

        hex_number_[best_move.digit].execute_move(best_move)
        logging.debug(f"executing {best_move} at {hex_number_[best_move.digit]}")

        return Step(hex_number_, moves_left, best_move.free_adds, best_move.free_removes)

    def print_num(self):
        return "".join([f"{hex_digit.value:x}" for hex_digit in reversed(self.hex_number)])

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

    def get_move(self, i, moves_left, free_adds, free_removes):
        add = change_hex[self.value][i][Hex.add]
        remove = change_hex[self.value][i][Hex.remove]

        # substrahiere die kostenlose zuege von den gebrauchten
        if free_adds:
            add -= free_adds
            if add < 0:
                free_adds = abs(add)
                add = 0
            
        if free_removes:
            remove -= free_removes
            if remove < 0:
                free_removes = abs(remove)
                remove = 0

        moves = max(add, remove)

        if add > remove:
            free_removes += add-remove
        else:
            free_adds += remove-add

        if moves > moves_left:
            return Move(-1, -1, -1, -1, -1, -1, -1, -1, -1)

        # +1 weil div by 0
        score = i / (moves+1)

        return Move(moves, add, remove, score, self.value, i, self.digit, free_adds, free_removes)

    def best_move(self, level: int, moves_left: int, free_adds: int, free_removes: int):
        moves = np.array([self.get_move(i, moves_left, free_adds, free_removes) for i in range(self.value+1, self.base)])
        moves = np.sort(moves)[::-1] 
        return moves[level]

    def execute_move(self, move):
        self.value = move.to

def main(EXAMPLE: int = 0):
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

    FREE_ADDS = 0
    FREE_REMOVES = 0
    history = [Step(hex_number, MOVES, FREE_ADDS, FREE_REMOVES)]

    biggest_history = copy.deepcopy(history)

    # just a timeout that I dont get stuck in an infinite loop
    timeout = 1000
    iteration = 0
    while history[-1].moves_left > 0 or history[-1].free_removes > 0 or history[-1].free_adds > 0:
        new_move = history[-1].next_move()
        if new_move is None:
            while True:
                if history[-1].skip_to_next_move():
                    break
                else:
                    history.pop()
                    if not len(history):
                        print("huh")
                        break
                    iteration -= 1
            
            # wenn es keine neue mögliche Zuege gibt, dann
            # breche ab und nehme das bisher beste ergebnis
            # moegliches Problem eines lokalen minnimums.
            if not len(history):
                print("huh")
                break
            continue
        history.append(new_move)


        iteration += 1
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

    logging.info(f"Moves: {MOVES}")
    logging.info(f"Free adds: {FREE_ADDS}")
    logging.info(f"Free removes: {FREE_REMOVES}")

    number = biggest_history[-1].print_num()
    logging.info(f"biggest Number: 0x{number}")

if __name__ == "__main__":
    main(0)
