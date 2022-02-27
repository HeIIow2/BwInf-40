---
Inhaltsverzeichnis
-

1. Lösungsidee
2. Umsetzung
3. Beispiele
4. Quellcode


---
Lösungsidee
-

- Ich speicher den Parkplatzt in einer gridbasierten zweidimensionalen
  Liste ab.
- Ich schaue für jedes Auto (hintere Reihe), ob ein Auto davorsteht
- wenn dann versuche ich die Autos nach rechts und nach links zu fahren
  und nehme dass, das am wenigsten Züge brauchte


---
Umsetzung
-

- Der Parkplatz its so gespeichert:
  ```python
  cars = [
    ["A", ""],
    ["B", ""],
    ["C", "H"],
    ["D", "H"],
    ["E", ""],
    ["F", "I"],
    ["G", "I"],
  ]
  ```
- laufe einmal durch die Liste durch `A -> B -> C ...`
  - hole die nötigen Schritte von links und rechts
    - **rekursiv:** prüfe, ob der Weg frei ist
    - wenn, dann gebe die Züge zurück
    - sonst bewege das blockierende Auto nach `links/rechts`
      - **rekursiv:** prüfe, ob ein Auto die `links/rechts` bewegung blockiert ist
      - wenn dann wiederhole dies mit dem blockierendem Auto in die gleiche richtung 
      - sonst bewege nach `links/rechts` und füge das zu der Liste hinzu 
    - wiederhole dies
  - formatiere die Listen und speicher die schrittanzahl
  - gebe die formatierte Liste mit den wenigsten Elementen aus `entweder links oder rechts`



---
Beispiele
-


Parkplatz 0
````
A: 
B: 
C: H 1 rechts
D: H 1 links
E: 
F: I 1 links, H 1 links, I 1 links
G: I 1 links
````
Parkplatz 1
````
A: 
B: P 1 rechts, O 1 rechts
C: O 1 links
D: P 1 rechts
E: O 1 links, P 1 links
F: 
G: Q 1 rechts
H: Q 1 links
I: 
J: 
K: R 1 rechts
L: R 1 links
M: 
N:
````
Parkplatz 2
````
A: 
B: 
C: O 1 rechts
D: O 1 links
E: 
F: R 1 rechts, Q 1 rechts, P 1 rechts
G: P 1 links
H: R 1 rechts, Q 1 rechts
I: P 1 links, Q 1 links
J: R 1 rechts
K: P 1 links, Q 1 links, R 1 links
L: 
M: S 1 links, P 1 links, Q 1 links, R 1 links, S 1 links
N: S 1 links
````
Parkplatz 3
````
A: 
B: O 1 rechts
C: O 1 links
D: 
E: P 1 rechts
F: P 1 links
G: 
H: 
I: Q 2 links
J: Q 1 links
K: Q 1 links, R 1 links, Q 1 links, R 1 links
L: Q 1 links, R 1 links
M: Q 1 links, R 1 links, S 1 links, Q 1 links, R 1 links, S 1 links
N: Q 1 links, R 1 links, S 1 links
````
Parkplatz 4
````
A: R 1 rechts, Q 1 rechts
B: R 1 rechts, Q 1 rechts, R 1 rechts, Q 1 rechts
C: R 1 rechts
D: R 2 rechts
E: 
F: 
G: S 1 rechts
H: S 1 links
I: 
J: 
K: T 1 rechts
L: T 1 links
M: 
N: U 1 rechts
O: U 1 links
P: 
````
Parkplatz 5
````
A: R 1 rechts, Q 1 rechts
B: R 1 rechts, Q 1 rechts, R 1 rechts, Q 1 rechts
C: R 1 rechts
D: R 2 rechts
E: 
F: 
G: S 1 rechts
H: S 1 links
I: 
J: 
K: T 1 rechts
L: T 1 links
M: 
N: U 1 rechts
O: U 1 links
P: 
````
  

---
Quellcode
-

````python
import sys


def read_file(path: str):
    with open(path, 'r') as park_file:
        park_str = park_file.read()
        park_list = park_str.split('\n')

        other_cars = park_list[2:-1]

        # get askii of start and stop
        start_stop = park_list[0].split(' ')
        start_char, stop_char = ord(start_stop[0]), ord(start_stop[1])

        cars = []
        while (start_char <= stop_char):
            cars.append([chr(start_char), ""])
            start_char += 1

        for other_car in other_cars:
            car_info = other_car.split(' ')
            cars[int(car_info[1])][1] = car_info[0]
            cars[int(car_info[1]) + 1][1] = car_info[0]

        return cars


def left(local_car_list_lookup_ref: iter, car: str, moves: list):
    local_car_list_lookup = list(local_car_list_lookup_ref)
    local_car_list = list(local_car_list_lookup)

    # loops through the whole list searching for the letter car
    for i, car_elem_local in enumerate(local_car_list):
        if car_elem_local[1] == car:

            # if the element left to found letter is in bounds
            if 0 <= i - 1 < len(local_car_list):

                # if element is not occupied
                if local_car_list[i - 1][1] == '':
                    # move left
                    local_car_list[i][1] = ''
                    local_car_list[i - 1][1] = car

                # if element is occupied
                else:
                    # move the car on this element left first
                    # recursive
                    result = left(local_car_list_lookup, local_car_list[i - 1][1], moves)
                    if result == -1:
                        return -1

                    # then move the actual car
                    result = left(result[0], car, result[1])
                    return result
            else:
                return -1

    moves.append(car)
    return local_car_list, moves


def right(local_car_list_lookup_ref: iter, car: str, moves: list):
    local_car_list_lookup = list(local_car_list_lookup_ref)
    local_car_list = list(local_car_list_lookup)

    # loops through the whole list searching for the letter car
    for n, car_elem_local in enumerate(reversed(local_car_list)):
        i = len(local_car_list) - n - 1

        if car_elem_local[1] == car:
            # if the element left to found letter is in bounds
            if 0 <= i + 1 < len(local_car_list):

                # if element is not occupied
                if local_car_list[i + 1][1] == '':
                    # move right
                    local_car_list[i][1] = ''
                    local_car_list[i + 1][1] = car

                # if element is occupied
                else:
                    # move the car on this element left first
                    # recursive
                    result = right(local_car_list_lookup, local_car_list[i + 1][1], moves)
                    if result == -1:
                        return -1

                    # then move the actual car
                    result = right(result[0], car, result[1])
                    return result
            else:
                return -1

    moves.append(car)
    return local_car_list, moves


def check_left(index: int, car_tuple: iter, moves=[]):
    car_list = list(car_tuple)
    if car_list[index][1] == '':
        return moves

    # tries to move the car in front once
    result = left(car_list, car_list[index][1], moves)
    if result == -1:
        return -1

    car_list, moves = result

    # if the horizontal car still cant move try again
    # recursive
    return check_left(index, car_list, moves)


def check_right(index: int, car_tuple: iter, moves=[]):
    car_list = list(car_tuple)
    if car_list[index][1] == '':
        return moves

    # tries to move the car in front once
    result = right(car_list, car_list[index][1], moves)
    if result == -1:
        return -1

    car_list, moves = result

    # if the horizontal car still cant move try again
    # recursive
    return check_right(index, car_list, moves)

def format_mov(moves: iter, label: str):
    if moves == -1:
        return '', sys.maxsize

    new_moves = []
    prev = ''
    for single_move in moves:
        if single_move != prev:
            new_moves.append([single_move, 1])
            prev = single_move
        else:
            new_moves[-1][1] += 1

    new_mov_str = []
    for new_move in new_moves:
        new_mov_str.append(f'{new_move[0]} {new_move[1]} {label}')

    return ', '.join(new_mov_str), len(moves)


# read file and convert it to 2d list
PATH = 'parkplatz0.txt'

CAR_LIST = read_file(PATH)
print(str(CAR_LIST) + '\n')

# iterate through every horizontally parking Car
for i, car_elem in enumerate(CAR_LIST):
    # tries and saves every necessary step if u want to go left
    CAR_LIST = read_file(PATH)
    left_moves = check_left(i, CAR_LIST, [])
    left_moves, left_weight = format_mov(left_moves, 'links')

    # tries and saves every necessary step if u want to go right
    CAR_LIST = read_file(PATH)
    right_moves = check_right(i, CAR_LIST, [])
    right_moves, right_weight = format_mov(right_moves, 'rechts')

    # compares the number of turns between left and right and displays
    # the one with less turns
    if left_weight < right_weight:
        print(f'{car_elem[0]}: {left_moves}')
    else:
        print(f'{car_elem[0]}: {right_moves}')



````