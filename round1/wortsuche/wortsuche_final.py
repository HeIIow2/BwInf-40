import random
from copy import deepcopy

class Grid:
    def __init__(self, x_size: int, y_size: int):
        self.X_SIZE = x_size
        self.Y_SIZE = y_size

        self.grid = []
        row = []
        for i in range(self.X_SIZE):
            row.append(None)

        for i in range(self.Y_SIZE):
            self.grid.append(list(row))

    def write(self, letter: str, x: int, y: int):
        if self.grid[y][x] is not None:
            return -1

        self.grid[y][x] = letter


class GridOption:
    def __init__(self, previous_grid: Grid, word: str, x_pos: int, y_pos: int, horizontal: bool):
        self.PREVIOUS_GRID = previous_grid
        self.new_grid = deepcopy(self.PREVIOUS_GRID)

        self.valid = True
        if horizontal:
            y = y_pos
            for i in range(len(word)):
                x = i + x_pos

                if self.new_grid.write(word[i], x, y) == -1:
                    self.valid = False
                    break

        else:
            x = x_pos
            for i in range(len(word)):
                y = i + y_pos

                if self.new_grid.write(word[i], x, y) == -1:
                    self.valid = False
                    break


# Klasse für die Grid Maske
class GridMask:
    def __init__(self, x_size: int, y_size: int, word_list: list):
        self.X_SIZE = x_size
        self.Y_SIZE = y_size
        self.WORD_LIST = tuple(word_list)

        # erstelle eine Grid Maske mit einem ähnlichem Algorithmus wie Vollgeladen
        # erstelle eine Liste aller Optionen deren länge so lang ist wie WORD_LIST
        self.position_options = [[Grid(x_size, y_size)]]
        for i in range(len(self.WORD_LIST)):
            self.position_options.append([])

        i = 0
        while len(self.position_options[-1]) == 0:
            results = self.get_all_positions(i, self.WORD_LIST[i])
            if type(results) == int:
                i = results
                if i == -1:
                    print("fuck")
                    break
            else:
                self.position_options[i+1] = results
                i += 1

        self.mask = self.position_options[-1][0].new_grid
        pass

    def get_all_positions(self, ref_grid_ind: int, word: str):
        # um den Algorithmus zu beschleunigen
        MAX_OPTIONS_PER_AXIS = 5

        options = []
        if ref_grid_ind == 0:
            ref_grid = self.position_options[ref_grid_ind][0]
        else:
            ref_grid = self.position_options[ref_grid_ind][0].new_grid

        # horizontally
        counter = 0
        for x in range(self.X_SIZE - (len(word)-1)):
            for y in range(self.Y_SIZE):
                option = GridOption(ref_grid, word, x, y, True)
                if option.valid:
                    counter += 1
                    options.append(option)
                    if counter > MAX_OPTIONS_PER_AXIS:
                        break

        # vertically
        counter = 0
        for x in range(self.X_SIZE):
            for y in range(self.Y_SIZE - (len(word)-1)):
                option = GridOption(ref_grid, word, x, y, False)
                if option.valid:
                    counter += 1
                    options.append(option)
                    if counter > MAX_OPTIONS_PER_AXIS:
                        break

        # wenn es keine optionen gibt, gehen ein Schritt zurück
        if len(options) == 0:
            return self.remove_last_option(index=ref_grid_ind)

        # die liste zufällig durchmischen
        options = GridMask.randomize_list(options)

        return options

    @staticmethod
    def randomize_list(ordered: iter):
        ordered = list(ordered)
        randomized = []
        while len(ordered) != 0:
            i = random.randrange(len(ordered))
            randomized.append(ordered[i])
            ordered.pop(i)

        return randomized

    def remove_last_option(self, index: int):
        # die letzte Option wird rekursiv gelöscht
        self.position_options[index] = self.position_options[index][1:]
        if len(self.position_options[index]):
            if index < 1:
                return -1
            return self.remove_last_option(index-1)

        return index



class Words:
    def __init__(self, file_path: str):
        # die Datei einlesen
        with open(file_path, 'r', encoding='utf-8') as words_file:
            word_list_raw = words_file.read().split('\n')[:-1]

            self.X_SIZE, self.Y_SIZE = map(int, word_list_raw[0].split(' '))
            self.WORD_LIST = sorted(word_list_raw[2:], key=len, reverse=True)

        # erstelle eine grid maske
        self.grid_mask = GridMask(self.X_SIZE, self.Y_SIZE, self.WORD_LIST)

        # das folgende für 4 Schwierigkeiten machen
        # fill up all empty cells
        pass


Words("worte4.txt")
for i in range(6):
    Words(f"worte{i}.txt")
