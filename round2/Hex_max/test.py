import hex3
import json
from PIL import Image

with open('hex.json') as f:
    hex_matrix = json.load(f)

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


def draw(hex_number: list, sollution: list, moves: int, example):

    length = 20
    gap = 10
    thickness = 1
    digits = len(hex_number)
    # create pillow image
    img = Image.new('RGB', ((length + gap) * digits + gap, (length + length + gap) * (moves + 1) + gap), color='white')

    start_hex = [hex_matrix[i].copy() for i in hex_number]
    end_hex = [hex_matrix[i].copy() for i in sollution]

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

        img = draw_digits(img, start_hex, i + 1, moves + 1, length=length, gap=gap, thickness=thickness)

    img.save(f'examples/hexmax{example}.png')


if __name__ == '__main__':
    for i in range(6):
        hex_number, moves, solution, meta = hex3.execute_file(i)
        print("finished starting drawing")
        draw(hex_number, solution, moves, i)
        print("finished drawing")
