import random
from anytree import Node

import openpyxl
from openpyxl import Workbook, load_workbook


class WordData:
    def __init__(self, path: str):
        with open(path, 'r', encoding='utf-8') as words_file:
            word_list_raw = words_file.read().split('\n')[:-1]
            print(word_list_raw)

            self.GRID_SIZE = tuple(map(int, word_list_raw[0].split(' ')))
            self.GRID_X, self.GRID_Y = self.GRID_SIZE
            self.WORD_LIST = sorted(word_list_raw[2:], key=len, reverse=True)

            print(self.GRID_SIZE)
            print(self.WORD_LIST)

            self.letters = []

            for word in self.WORD_LIST:
                for char in word:
                    self.letters.append(char)

        self.CURRENT_WORD_KEY = 'current word'
        self.POS_KEY = 'pos'
        self.EXIF_KEY = 'exif'
        self.NEXT_WORD_KEY = 'next word'
        self.EMPTY_CELLS_KEY = 'empty cells'
        self.POSSIBLE_GUESSES_KEY = 'possible guesses'

        self.root = Node({self.EMPTY_CELLS_KEY: list(range(self.GRID_Y * self.GRID_X)),
                          self.EXIF_KEY: {}})

        self.current_node = self.root

        i = 0
        while i < len(self.WORD_LIST):
            word = self.WORD_LIST[i]
            # print(word)
            self.current_node.name[self.EXIF_KEY][self.CURRENT_WORD_KEY] = word
            if self.POSSIBLE_GUESSES_KEY not in self.current_node.name[self.EXIF_KEY]:
                possible_pos = self.get_possible_positions(word, self.current_node.name[self.EMPTY_CELLS_KEY])
                self.current_node.name[self.EXIF_KEY][self.POSSIBLE_GUESSES_KEY] = possible_pos
            else:
                possible_pos = self.current_node.name[self.EXIF_KEY][self.POSSIBLE_GUESSES_KEY]

            if len(possible_pos['x']) <= 0 and len(possible_pos['y']) <= 0:
                i += -1
                self.current_node = self.current_node.parent
                continue
            else:
                if len(possible_pos['x']) <= 0:
                    possible_pos.pop('x')
                elif len(possible_pos['y']) <= 0:
                    possible_pos.pop('y')

                dir_keys = list(possible_pos)
                dir_key = dir_keys[random.randrange(len(dir_keys))]
                pos = possible_pos[dir_key][random.randrange(len(possible_pos[dir_key]))]

                new_cells = self.delete_cells(word, pos, dir_key, self.current_node.name[self.EMPTY_CELLS_KEY])

                node_dict = {
                    self.CURRENT_WORD_KEY: word,
                    self.POS_KEY: (dir_key, pos),
                    self.EMPTY_CELLS_KEY: new_cells,
                    self.EXIF_KEY: {}
                }

                self.current_node = Node(node_dict, parent=self.current_node)
                i += 1

        word_positions_raw = {}
        for i in range(len(self.WORD_LIST)):
            word_positions_raw[self.current_node.name[self.CURRENT_WORD_KEY]] = self.current_node.name[self.POS_KEY]
            self.current_node = self.current_node.parent

        self.grid = [[None] * self.GRID_X for _ in range(self.GRID_Y)]
        for key in word_positions_raw:
            pos_x = word_positions_raw[key][1] % self.GRID_Y
            pos_y = int(word_positions_raw[key][1] / self.GRID_Y)

            if word_positions_raw[key][0] == 'x':
                for i, char in enumerate(key):
                    self.grid[pos_x + i][pos_y] = char
            else:
                for i, char in enumerate(key):
                    self.grid[pos_x][pos_y + i] = char

    def delete_cells(self, word, pos, dir, empty_cells):
        if dir == 'x':
            for i in range(pos, pos + len(word), 1):
                empty_cells.remove(i)

        else:
            for i in range(pos, pos + (len(word) * self.GRID_Y), self.GRID_Y):
                empty_cells.remove(i)

        return empty_cells

    def get_possible_positions(self, word, empty_cells):

        x_list = []
        y_list = []

        for empty_cell in empty_cells:
            if empty_cell % self.GRID_Y + (len(word) - 1) < self.GRID_Y:
                add = True
                for i in range(empty_cell, empty_cell + len(word), 1):
                    if i not in empty_cells:
                        add = False
                        break
                if add:
                    x_list.append(empty_cell)

            if empty_cell + (self.GRID_Y * (len(word) - 1)) in empty_cells:
                add = True
                for i in range(empty_cell, empty_cell + (len(word) * self.GRID_Y), self.GRID_Y):
                    if i not in empty_cells:
                        add = False
                        break
                if add:
                    y_list.append(empty_cell)

        return {'x': x_list, 'y': y_list}


def randomize_list(ordered_list_ref: list):
    ordered_list = list(ordered_list_ref)
    random_list = []
    for i in range(len(ordered_list)):
        rand_ind = random.randrange(len(ordered_list))
        random_list.append(ordered_list[rand_ind])
        ordered_list.pop(rand_ind)

    return random_list


def get_word_count(word_list: list, grid: list):
    word_counter = 0
    for word in word_list:
        if word in grid[0] or word in grid[1]:
            word_counter += 1

    return word_counter


def letter_is_valid(word_list: list, letter: str, row_int: int, column_int: int, grid):
    current_row = ''
    current_col = ''
    after_row = ''
    after_col = ''

    for r in range(len(grid)):
        row = grid[r]

        for c in range(len(row)):
            column = row[c]
            if row_int == r and row[c] is not None:
                current_row += row[c]
                after_row += row[c]

            if column_int == c and row[c] is not None:
                current_col += row[c]
                after_col += row[c]

            if row_int == r and column_int == c:
                after_row += letter
                after_col += letter

    prev_word_count = get_word_count(word_list, (current_row, current_col))
    after_word_count = get_word_count(word_list, (after_row, after_col))

    if after_word_count != prev_word_count:
        return False
    else:
        return True


def fill_empty_cells(word_obj: WordData, difficulty: int):
    grid = []
    for row in word_obj.grid:
        grid.append(row)
    letters = word_data.letters
    words = word_data.WORD_LIST

    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] is None:
                if random.randint(0, 100) < difficulty:
                    # get current row and column

                    possible_letters = randomize_list(letters)

                    for letter in possible_letters:
                        if letter_is_valid(words, letter, row, column, grid):
                            grid[row][column] = letter
                            break

                    if grid[row][column] is None:
                        grid[row][column] = chr(random.randrange(65, 91))

                else:
                    grid[row][column] = chr(random.randrange(65, 91))

    return grid


def run_file(FILE: int):
    global word_data
    PATH_INPUT = f'worte{FILE}.txt'

    grids = []
    for difficulty in range(0, 101, 20):
        word_data = WordData(PATH_INPUT)
        grids.append(fill_empty_cells(word_data, difficulty))

    grid = grids[0]
    for i in range(1, len(grids), 1):
        for j in range(len(grid)):
            grid[j].append('')
            grid[j].extend(grids[i][j])

    for i in range(len(word_data.WORD_LIST)):
        if i >= len(grid):
            grid.append([])

        grid[i].insert(0, '')
        grid[i].insert(0, word_data.WORD_LIST[i])

    for n in range(i + 1, len(grid)):
        grid[n].insert(0, '')
        grid[n].insert(0, '')

for i in range(6):
    run_file(i)
