import json
import logging
import enum

logging.basicConfig(level=logging.DEBUG)

SEGMENTS = 7

class Hex(enum.Enum):
    add = "add"
    remove = "remove"

# read hex.json and store as hex matrix
with open('hex.json') as f:
    hex_matrix = json.load(f)

logging.info(hex_matrix)

# liste wie viele striche man von jeder zu jeder zahl hinzufügen bzw. wegnehmen muss.
# [zahl vorher][zahl nacher][add remove]
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
            
        change_hex[hex_1][hex_2] = {Hex.add: add, Hex.remove: remove}
        logging.debug(f"{hex_1} {hex_2} {change_hex[hex_1][hex_2]}")



