import hex3
import json
from PIL import Image
import numpy as np
import timeit
import random

import matplotlib.pyplot as plt

with open('hex.json') as f:
    hex_matrix = json.load(f)

print(hex_matrix)

def draw_digits(img, hex_number: list, move: int, total_moves: int, length: int = 10, gap: int = 5, thickness: int = 2):
    height = move * (gap + length + length) + gap
    digits = len(hex_number)

    first_pos = gap
    for i, digit in enumerate(hex_number):
        if digit[0]:    img.paste(Image.new('RGB', (length, thickness), color='black'),
                                  (first_pos + i * (length + gap), height))
        if digit[1]:    img.paste(Image.new('RGB', (length, thickness), color='black'),
                                  (first_pos + i * (length + gap), height + length))
        if digit[2]:    img.paste(Image.new('RGB', (length, thickness), color='black'),
                                  (first_pos + i * (length + gap), height + length * 2))
        if digit[3]:    img.paste(Image.new('RGB', (thickness, length), color='black'),
                                  (first_pos + i * (length + gap), height))
        if digit[4]:    img.paste(Image.new('RGB', (thickness, length), color='black'),
                                  (first_pos + i * (length + gap) + length, height))
        if digit[5]:    img.paste(Image.new('RGB', (thickness, length), color='black'),
                                  (first_pos + i * (length + gap), height + length))
        if digit[6]:    img.paste(Image.new('RGB', (thickness, length), color='black'),
                                  (first_pos + i * (length + gap) + length, height + length))

    return img

def is_valid_number(hex_data: list) -> bool:
    for hex_digit in hex_data:
        if hex_digit not in hex_matrix:
            return False
    return True

def save_in_text(hex_data: list, example: int):
    if not is_valid_number(hex_data):
        return

    with open(f'solutions/hexmax{example}.txt', "a") as f:
        for hex_digit in hex_data:
            digit = hex_matrix.index(hex_digit)
            f.write(f"{digit:x}")
        f.write("\n")

def draw(hex_number: list, sollution: list, moves: int, example: int):
    with open(f'solutions/hexmax{example}.txt', "w") as f:
        pass

    length = 20
    gap = 10
    thickness = 1
    digits = len(hex_number)
    # create pillow image
    img = Image.new('RGB', ((length + gap) * digits + gap, (length + length + gap) * (moves + 1) + gap), color='white')

    start_hex = [hex_matrix[i].copy() for i in hex_number]
    end_hex = [hex_matrix[i].copy() for i in sollution]

    save_in_text(start_hex, example)

    img = draw_digits(img, start_hex, 0, moves + 1, length=length, gap=gap, thickness=thickness)
    for i in range(moves):
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

        save_in_text(start_hex, example)
        img = draw_digits(img, start_hex, i + 1, moves + 1, length=length, gap=gap, thickness=thickness)

    img.save(f'solutions/hexmax{example}.png')

def plot_runtime(x_axis: list, y_axis: list, std: list):
    plt.plot(x_axis, y_axis, "-o", linewidth=1, label="data")

    plt.errorbar(x_axis, y_axis, yerr=std, linestyle='None', markersize=0,
                 label=f"Standart Deviation\navr: {round(np.average(std), 3)}")

    plt.grid(visible=True, which='major', axis='both')


    plt.title(f"Hex Max")
    plt.xlabel('operators in therm')
    plt.ylabel('time in s')
    plt.legend(loc='upper left')
    plt.savefig("laufzeit/Laufzeit.svg")
    plt.savefig("laufzeit/Laufzeit.png")
    plt.show()

def get_random_exercise(n: int):
    hex_number = [random.randint(0, 15) for _ in range(n)]

    return hex_number, n

if __name__ == '__main__':
    x_axis = []
    y_axis = []
    std = []
    for i in range(10, 1000, 50):
        times = []
        for j in range(100):
            hex_number, moves = get_random_exercise(i)
            start_time = timeit.default_timer()
            hex_number, moves, solution, meta = hex3.execute_moves(hex_number, moves)
            end_time = timeit.default_timer()
            times.append(end_time - start_time)

        n = len(hex_number)
        avr_time = np.average(times)
        x_axis.append(n)
        y_axis.append(avr_time)
        std.append(np.std(times))
        print(i)
    plot_runtime(x_axis, y_axis, std)

    with open("laufzeit/laufzeit.json", "w") as f:
        json.dump({"x_axis": x_axis, "y_axis": y_axis, "std": std}, f)

