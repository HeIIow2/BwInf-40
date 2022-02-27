'''
Junioraufgabe 1:

etwas trigolometrie
'''
import math
import sys


def get_landkereis(path: str):
    # warum habt ihr nicht einfach ein json file verwendet ;-;

    with open(path, 'r') as landkreis_file:
        landkreis_str = landkreis_file.read()
        landkreis_list_raw = landkreis_str.split('\n')
        landkreis_list_raw = landkreis_list_raw[:-1]
        landkreis_list = []

        for elem in landkreis_list_raw:
            elem = elem.split(' ')
            elem = int(elem[0]), int(elem[1])
            landkreis_list.append(elem)

        n, m = landkreis_list[0]

        hauser = landkreis_list[1:n + 1]
        windrader = landkreis_list[n + 1:]

        return hauser, windrader


def get_distance_between_points(a: iter, b: iter):
    c = a[0] - b[0], a[1] - b[1]
    distance = math.sqrt(math.pow(c[0], 2) + math.pow(c[1], 2))

    return distance


def get_distance_of_neares_house(windrad: iter, houses: iter):
    nearest_house = sys.float_info.max
    for house in houses:
        distance = get_distance_between_points(windrad, house)
        if distance < nearest_house:
            nearest_house = distance

    return nearest_house


# lese häuser und windräder von txt und speicher diese in listen
hauser, windrader = get_landkereis('landkreis0.txt')


# berechne die distanz zum nächsten haus
min_distances = []
for windrad in windrader:
    min_distances.append(get_distance_of_neares_house(windrad, hauser))

print(min_distances)

# teile jeden mindestabstand durch 10

max_heights = []
for min_distance in min_distances:
    max_heights.append(min_distance / 10)

# max_heights ist die liste in der alle maximalen höhen für die Windräder gespeichert werden


# output for readme

for i in range(len(max_heights)):
    print(f'- x: {windrader[i][0]}, y: {windrader[i][1]},  max height: {int(max_heights[i])}')
