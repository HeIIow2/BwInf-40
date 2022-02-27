import sys

import numpy as np


class WeightPieces:
    edit_elem = None

    def __init__(self, path, weight_list_raw=None):
        with open(path, 'r', encoding='utf-8') as weights_file:
            weight_list_raw = weights_file.read().split('\n')[1:-1]
            weight_list = list(map(lambda x: list(map(lambda y: int(y), x.split(' '))), weight_list_raw))

        self.weights_ref = []
        for elem in weight_list:
            for _ in range(elem[1]):
                self.weights_ref.append(elem[0])
        print(len(weight_list), weight_list)

        max_list = list(map(lambda x: x[1], weight_list))
        weight_ref = list(map(lambda x: x[0], weight_list))

        gcd = np.gcd.reduce(weight_ref)
        print(weight_ref)
        print(gcd)

        possible = []
        for i in range(10, 1010, 10):
            if i % gcd == 0:
                possible.append(i)

        print(possible)

        smallest_coefficient = weight_ref[0]
        for weight in weight_ref[1:]:
            if weight < smallest_coefficient:
                smallest_coefficient = weight





for i in range(6):
    new_weights = WeightPieces(f'gewichtsstuecke{i}.txt')
    print('')

