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

Ich berechne für jedes Windrad den Abstand zu jedem Haus.
Dann finde ich den Abstand von dem nächsten Haus und teile ihn durch 10.
Somit habe ich dann die maximale Höhe in meter, die das Windrad haben kann.


---
Umsetzung
-

- Als Erstes lese ich die Daten aus den gegebenen .txt files aus.
  - Ich teile den string mit `.split('\n')` am umbruch und speicher dieses in einer Liste.
  - Ich lese die Häuseranzahl `n` und die Windräderanzahl `m` aus dem ersten Element der liste aus
  - Ich splice die Liste in eine Häuser- und Windräder-liste.
- Ich loope durch die Windrad-liste und berechne für jedes windrad den Abstand zum nächsten Haus.
  - ich erstelle `nearest_house` mit der größtmöglichen Zahl
  - ich loope durch jedes Haus
    - ich berechne den Abstand des Hauses und des Windrades
    - wenn dieser kleiner als `nearest_house` ist, setze ich nearest house auf den Abstand

      ```python
      import math
      # den Abstand 2er Punkte berechnen 
    
      def get_distance_between_points(a: iter, b: iter):
        c = a[0] - b[0], a[1] - b[1]
        distance = math.sqrt(math.pow(c[0], 2) + math.pow(c[1], 2))

        return distance
      ```
  - Ich setzte den Abstand des nächsten Hauses auf `distance` und hänge ihn an eine Liste an.
- Ich habe jetzt eine Liste mit den Abständen zu jeweils dem nächsten Haus von jedem Windrat
- ich loope durch die liste und teile jedes Element durch 10



---
Beispiele
-


*die maximale höhe der Windräder ist mit `int(x)` gerundet*

*Hier stehen nur die Koordinaten der Windräder und nicht die der Häuser da dies sonst zu lang werden würde.*
- **Landkreis 1**
  - x: 1242, y: -593,  max height: 48
  - x: -1223, y: -1479,  max height: 158
  - x: 1720, y: 401,  max height: 72

- **Landkreis 2**
  - x: 359, y: 20,  max height: 115
  - x: 2, y: -773,  max height: 201
  - x: 315, y: -213,  max height: 138
  - x: -629, y: -532,  max height: 209
  - x: 97, y: -69,  max height: 132
  - x: -392, y: -418,  max height: 186
  - x: 87, y: -384,  max height: 161
  - x: -597, y: 612,  max height: 133
  - x: -13, y: -32,  max height: 133
  - x: -57, y: 49,  max height: 128
  - x: 276, y: 292,  max height: 91
  - x: 156, y: 55,  max height: 118
  - x: -423, y: -93,  max height: 161
  - x: 202, y: -219,  max height: 142
  - x: -340, y: -343,  max height: 177

- **Landkreis 3**
  - x: 0, y: 0,  max height: 451
  - x: 180, y: 570,  max height: 393
  - x: 360, y: 1140,  max height: 336
  - x: 540, y: 1710,  max height: 280
  - x: 360, y: -120,  max height: 444
  - x: 540, y: 450,  max height: 385
  - x: 720, y: 1020,  max height: 327
  - x: 900, y: 1590,  max height: 269
  - x: 720, y: -240,  max height: 440
  - x: 900, y: 330,  max height: 381
  - x: 1080, y: 900,  max height: 321
  - x: 1260, y: 1470,  max height: 262
  - x: 1080, y: -360,  max height: 440
  - x: 1260, y: 210,  max height: 380
  - x: 1440, y: 780,  max height: 320
  - x: 1620, y: 1350,  max height: 261

- **Landkreis 4**
  - x: -4147, y: 8575,  max height: 0
  - x: -6453, y: 14307,  max height: 179
  - x: -8370, y: 5831,  max height: 107
  - x: 13045, y: -5404,  max height: 151
  - x: -8361, y: 8131,  max height: 115
  - x: -6963, y: -371,  max height: 71
  - x: 9772, y: -3239,  max height: 42
  - x: -5102, y: -1726,  max height: 58
  - x: 13454, y: 11822,  max height: 67
  - x: -7427, y: 1720,  max height: 112
  - x: -7816, y: 12396,  max height: 63
  - x: -11095, y: 603,  max height: 251
  - x: 8314, y: 16301,  max height: 155
  - x: 15283, y: -2961,  max height: 118
  - x: 7082, y: 18552,  max height: 336
  - x: 16743, y: 2687,  max height: 109
  - x: 17511, y: -730,  max height: 260
  - x: -10767, y: 12860,  max height: 350
  - x: 1508, y: -8030,  max height: 135
  - x: -7767, y: 982,  max height: 68
  - x: 1277, y: -11294,  max height: 139
  - x: -8724, y: 3575,  max height: 50
  - x: 7033, y: -7766,  max height: 72
  - x: 2720, y: -10910,  max height: 110
  - x: 20589, y: 7265,  max height: 532
  - x: -3214, y: 15263,  max height: 94
  - x: 6887, y: 17263,  max height: 209
  - x: -3944, y: 13584,  max height: 28
  - x: 6576, y: 15697,  max height: 76
  - x: -12074, y: 5974,  max height: 425
  

---
Quellcode
-

````python
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
hauser, windrader = get_landkereis('landkreis4.txt')


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
````