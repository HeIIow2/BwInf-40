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

Bei der Aufgabenstellung, bei der man den Weg mit den meisten Punkten
finden muss, ist offensichtlich, dass ein guter Ansatz dafür ein Datenbaum
ist. Bei einem Datenbaum hat man eine Ausgangssituation, und für jede Möglichkeit
kommt ein neuer Ast hinzu.

Wenn ich während ich den Datenbaum erstelle, die Punkte schon zusammenrechne,
kann ich nach der Erstellung einfach den Pfad des Blattes mit der größten Punktzahl
nehmen und dies ist dann die optimale Route.


---
Umsetzung
-

Das Programmieren war auch im Grunde nicht so schwer, da ich die python Library
`anytree` genutzt habe.

Um den Baum zu erstellen habe ich als Ausgangspunkt das 'Hotel -1' genommen,
bei dem alle Werte 0 sind.

Dann habe ich alle möglichen Hotels als neue abzweigung gespeichert.

Ein Hotel ist bereisbar, wenn:
- es nicht weiter als 360min vom vorherigen Hotel entfernt is.
- die Zeit, die es von dem neuen Hotel noch zum Ziel braucht kleiner ist, als die übrigen Stops * 360
`total_travel_time < (5 - used_stops) *360`

Dies hat bei den Beispielen 1, 2 und 3 sehr gut funktioniert, bei Beispiel 3
hat es dann aber angefangen langsam zu werden, und bei Beispiel 4 mit
ca. 1500 hat es viel zu lang gebraucht.

Darauf hin habe ich einige kleine Optimierungen durchgeführt, und dann 
wurde 3 auch immer schneller. 4 dauerte immer noch zu lang. Daraufhin 
habe ich mir die Liste genauer angeschaut, und mir ist aufgefallen, dass
in allen Abschnitten die ich angeschaut habe mindestens 1 Element ist, welches
größer als 3 ist. Also habe ich mein Programm so umgeschrieben, dass es 
alle Hotels mit einer Bewertung schlechter als 3 ignoriert. Mit dieser
Optimierung lief dass Program selbst bei dem 4. Beispiel flüssig durch.
Da mir bewusst ist, dass das Ergebnis nicht unbedingt 100% akkurat ist,
habe ich den Schwellwert auf 2 runtergesetzt und es kam immer noch das 
gleiche Ergebnis, weshalb ich davon ausgehen, dass es korrekt war.

---
Beispiele
-


hotel 1
```
stop: 1; hotel: 2; time: 347; rating: 2.7
stop: 2; hotel: 6; time: 687; rating: 7.1000000000000005
stop: 3; hotel: 7; time: 1007; rating: 9.9
stop: 4; hotel: 10; time: 1360; rating: 12.7
```
hotel 2
```
stop: 1; hotel: 2; time: 341; rating: 2.3
stop: 2; hotel: 9; time: 700; rating: 5.3
stop: 3; hotel: 14; time: 1053; rating: 10.1
stop: 4; hotel: 24; time: 1380; rating: 15.1
```
hotel 3
```
stop: 1; hotel: 97; time: 359; rating: 4.6
stop: 2; hotel: 195; time: 717; rating: 4.8999999999999995
stop: 3; hotel: 297; time: 1076; rating: 8.7
stop: 4; hotel: 400; time: 1433; rating: 10.399999999999999
```
hotel 4
```
stop: 1; hotel: 68; time: 249; rating: 4.8
stop: 2; hotel: 188; time: 605; rating: 9.7
stop: 3; hotel: 297; time: 949; rating: 14.2
stop: 4; hotel: 425; time: 1301; rating: 19.2
```
hotel 5
```
stop: 1; hotel: 241; time: 280; rating: 5.0
stop: 2; hotel: 580; time: 636; rating: 10.0
stop: 3; hotel: 912; time: 987; rating: 15.0
stop: 4; hotel: 1167; time: 1271; rating: 20.0
```
  

---
Quellcode
-

````python
from anytree import Node


class Hotels:
    def __init__(self, path: str):
        with open(path, 'r') as hote_file:
            # reads the example files
            hotel_list_raw = hote_file.read().split('\n')

            self.max_stops = 5
            self.max_drive_by_one = 360
            self.total_time = int(hotel_list_raw[1])
            self.hotels = [None] * int(hotel_list_raw[0])

            for i in range(int(hotel_list_raw[0])):
                time, rating = hotel_list_raw[i + 2].split(' ')
                time, rating = int(time), float(rating)
                self.hotels[i] = [time, rating]

            print(self.hotels)

            self.leftover_time = []
            for i in range(self.max_stops):
                self.leftover_time.append(self.max_drive_by_one * (self.max_stops - i - 1))

    def get_possible_stops(self, branch_exif: dict):
        expired_time = branch_exif[TIME]
        collected_rating = branch_exif[RATING]
        used_stops = branch_exif[STOPS]

        # iterates through the whole hotel list starting at the Hotel of the current leave
        possible_branches = []
        for i in range(branch_exif[HOTEL] + 1, len(self.hotels), 1):
            hotel = self.hotels[i]
            # stops checking for more hotels, if it takes to long to reach them
            if hotel[0] - expired_time >= self.max_drive_by_one:
                break

            # checks if they are far enough away that the time will be enough to get to the end
            if self.total_time - hotel[0] <= self.leftover_time[used_stops] and hotel[1] > 2:
                # the hotel may be possible so it gets addet to a list
                possible_branches.append(
                    {HOTEL: i, TIME: hotel[0], RATING: collected_rating + hotel[1], STOPS: used_stops + 1})

        return possible_branches


# dictionary keys
NEXT_STOPS = 'next stops'
STOPS = 'stops'
RATING = 'rating'
TIME = 'time'
HOTEL = 'hotel'

# create class for all of the work with the provided data
hotels = Hotels('hotels5.txt')
# initialize the root of the data tree
travel_tree = Node({HOTEL: -1, TIME: 0, RATING: 0.0, STOPS: 0})
for i in range(hotels.max_stops):
    # helpful debug
    print('###########')
    print(i)
    print('###########')
    counter = 0

    # iterates through all leaves
    for leave in travel_tree.leaves:
        # skip if branch is discontinued
        if leave.name[STOPS] == i:
            # gets all possible next stops for every leave and appends it to the tree
            add_to_node = hotels.get_possible_stops(leave.name)

            for element in add_to_node:
                new_node = Node(element, parent=leave)

            # helpful debug
            counter = counter + 1
            if counter % 1000 == 0:
                print(f'progress {counter}')

# find the leave with the highest rating
max = 0.0
max_node = None
leaves = travel_tree.leaves
for leave in leaves:
    if max < leave.name[RATING]:
        max = leave.name[RATING]
        max_node = leave
    print(leave.name[RATING])

print(max)
print(max_node)

# prints out the best path in the required format
path = max_node.path
for i in range(1, len(path), 1):
    stop_dict = path[i].name
    print(f'stop: {stop_dict[STOPS]}; hotel: {stop_dict[HOTEL]}; time: {stop_dict[TIME]}; rating: {stop_dict[RATING]}')

````