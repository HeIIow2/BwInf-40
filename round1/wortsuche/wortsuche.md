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

Als erstes versuchte ich zufällige Positionen der gegebenen Wörter zu generieren und 
überprüfte dann, ob diese sich überschneiden, und wenn, dann wurden neue Positionen generiert.
Das funktionierte auch so weit, nur hat es bei beispiel 4 deutlich zu lang gedauert. 
Deshalb dachte ich, man könnte ein Datenbaum nutzen, der sich merkt, was nicht funktioniert,
und was funktioniert.

---
Umsetzung
-

**Die Wörter in ein leeres Grid platzieren**

Die Wortliste wird nach länge der Wörter sortiert (das größte zuerst). Dies macht den Algorythmus
schneller, da die längsten Worte am meisten Platz wegnehmen

Um die Wörter ins grid zu setzen, wird ein Datenbaum erstellt. 


Jede Node enthält:
- das jeweilige Wort (*hat sich als unnötig herausgestellt*)
- die Position des Wortes *hoizontal oder vertikal; zeile; spalte*
- alle noch nicht belegten Zellen
- Werte um die Daten des nächsten Wortes zu bekommen
	- alle möglichen Positionen für das nächste Wort
	- das jeweilige Wort (*hat sich als unnötig herausgestellt*)
	
Der Root des Trees besteht nur aus den Werten um die Daten des nächsten Wortes zu bekommen.

Von dort aus wird eine zufällige Position aus der Liste aller möglichen Positionen gewählt,
welches die Position des nächsten Wortes bestimmt.

Wenn das nächste Wort keine möglichen neuen Positionen generieren kann, 
wird eine andere Position gewählt, und es wird nochmal ausprobiert. Wenn keine
neue Position mehr übrig ist, geht man eine Node zurück im Baum und erstellt ein
neuen Ast mit einer anderen zufälligen Position.

Dies wiederholt sich bis Positionen für alle Worter gefunden wurden.

*Schwachstellen meines Algorythmus*
- Ich hätte nicht die library anytree nutzten müssen eine simple Liste als Datenstruktur hätte gereicht.
- Wenn keine mögliche Positionen für alle Wörter existieren, läuft das Programm unendlich lang und stoppt nicht.

**Die zufälligen Buchstaben in das Grid einfügen**

Die Schwierigkeit ist eine Zahl zwischen 0-100.

Das Programm geht durch jedes Element des Grids. Wenn es leer ist, generiert es
eine Zufallszahl zwischen 0 und 100, und wenn diese niedriger als die Schwierigkeit ist,
setzt es das Element auf ein zufälligen Buchstaben aus einer Liste. In dieser Liste ist 
jeder Buchstabe aller Wörter aus dem Vorherigen Grid enthalten (wenn ein Buchstabe mehrmals in den Wörtern ist, ist er auch mehrmals in der Liste)

	Wenn in der Zeile und Spalte in der der Buchstabe eingefügt wird, eine unterschiedliche
	Anzahl von Wörtern ist, als bevor dieser eingefügt wurde, dann wird ein anderer Buchstabe aus der Liste genommen.
	
	Wenn kein Buchstabe mehr in der Liste übrig ist, wird ein Zufälliger Buchstabe im Alphabet genommen.

Wenn die Zufallszahl höher ist als die Schwierigkeit, dann wird ein zufälliger
Buchstabe aus dem Alphabet dort eingefügt.

*Schwachstellen meines Algorythmus*
- Wenn nur ein zufälliger Buchstabe erzeugt wird, ist es möglich, wenn auch unwarscheinlich, dass es ein neues Wort erzeugt.

---
Beispiele
-


*die Beispiele sind in den Dateien "word grid <number>.xlsx"*.

*ganz links am rand stehen die jeweils gesuchten wörter und dann kommen die Wordgrids in aufsteigender Schwierigkeit.*
*Dies sind nur die nicht ausführlichen Beispiele*

worte 0
```
TORF; VOR; RAD; EVA
Z A E O F
T O R F R
R R V S E
E A O A V
L D R Q A
```

worte 1
```
INFO; EIN; UND; DA; ER; DU
U I Q I E I
N Y P N U X
D E O F K N
E I N O E C
E D I U O I
E U D A E R
```

worte 2
```
BILDSCHIRM; FESTPLATTE; TASTATUR; COMPUTER; MAUS; USB
S T E B C E C F M U
C A A I R L O E A K
S S B L E A M S U M
I T R D P N P T S A
P A T S U T U P C E
T T W C W X T L C A
Q U R H I P E A M E
P R V I T E R T F P
R S U R C F U T C E
U S B M B Z S E R B
```

worte 3
```
LEGITIMATION; REVOLUTION; KONJUNKTUR; DEKORATION; INTUITION; INFEKTION; MONOGRAMM; EMISSION; EMPATHIE; CHRONIK; REFERAT; VERS
H I H I R N Z M I N O S E N N P O R R E T H
Z V E U L O O Y N I T O F N L T E E K Q V H
R F E T E I N R Y V F O Y G M N F F O K G V
I Q I N G U P M A O V Q W P C O O E K R D M
O K H G I I H N T R O N V U H U O R W I H V
J O A O T K O N J U N K T U R M O A A G S M
A K I M I W O T R M T I B M R O T T C O R M
T H N T M B R H Z E I J T E P E T E E E J O
O K F M A D U P P E M P A T H I E L N C J N
W D E J T T I I N K U I A L I K E M O F N O
N O K E I N P B M R Z C R T J U Y E V Z J G
L I T B O R Z O V E R S S U W O N R T I T R
N V I X N L X N O Z N H I E K S A R J R K A
T P O X U B O E M I S S I O N O D H O X K M
U N N C L S H D K N N T I Y R N N U K C A M
I V M H V K N E Q E N P T C J R E N V U N U
E T R R D A T K R V E R E V O L U T I O N T
S V I O I R R O M E N N W O N N C M S N R D
T A E N V T F R K F D E W O T J I F E E J E
X F W I C O A A U J K I I N T U I T I O N N
Q G I K Y A I T E M E A E I U V Z C F U W L
R T Z S O D T I I H I T I S X Z T J O T O Q
O W U H T F L O L M O A H D G M J Y K X Z K
X R O T I I Y N T L A I O X I Z R N U O L F
```

worte 4
```
BEGRIFFSKLÄRUNGSHINWEIS; NAVIGATIONSLEISTE; ÖSTERREICHBEZOGEN; DISKUSSIONSSEITE; LIZENZUMSTELLUNG; MEDAILLENSPIEGEL; BEGRIFFSKLÄRUNG; INTERNETQUELLE; KATEGORIEGRAPH; PERSONENLEISTE; POSITIONSKARTE; COORDINATEMAP; FUSSBALLDATEN; ARCHIVIERUNG; FOLGENLEISTE; KALENDERSTIL; MULTILINGUAL; FARBLEGENDE; INFORMATION; MUSIKCHARTS; WAPPENRECHT; ABRUFDATUM; AUTOARCHIV; COMMONSCAT; COORDINATE; WIKISOURCE; WIKTIONARY; ARCHIVBOT; BAUSTELLE; BIBRECORD; GEOQUELLE; LITERATUR; NOCOMMONS; WEBARCHIV; ALLMUSIC; BENUTZER; ERLEDIGT; NAVFRAME; WIKIDATA; ZITATION; ACHTUNG; BOOLAND; COMMONS; TAXOBOX; ABSATZ; ARCHIV; BELEGE; CENTER; CHARTS; KASTEN; SMILEY; BABEL; BBKL; FILM; GNIS; HÖHE; IMDB; INFO; LANG; PING; SORT; TEXT; AUS; AUT; BEL; BGR; CAN; COL; DDB; DEU; DOI; FNZ; FRA; GER; IPA; PRO; FN
O V H C A Q I M O I P N F R A I R O G T T P X B N A W I K T D U Y W S D O I D N
J O Y X B A N W L E R A X S L I T E R A T U R T C R P P A M I S P T N B O C T M
O C D E T R N I I J O I A D G S E A H A C H T U N G O A B S S I E Z A E C G M J
M F Z R L C B K Z L A T N M A E G N X K A S T E N M S G Q I K O R C V G N C U Z
K N R A H H V I E B U S T M U S I K C H A R T S Q A I N K C U T S E I R T O L O
W R E L C I X D N L T T Z I A B A U S T E L L E I K T I B O S I O N G I M M T B
S I T L G V G A Z B O A R D R W J E S O X H C E M A I S D M S I N T A F Y M I E
T J F M O S B T U G A X T N G M V N O B B W E U U L O T O M I X E E T F R O L N
A W K U T U U A M R R O E I I H F M R B R B J A R E N S K O O X N R I S Y N I U
Q S M S I O A L S J C B N I I N F O T M E T G R N N S M G N N V L F O K W S N T
T T B I I O E Q T A H O Q R P Z I T A T I O N F O D K E I S S F E L N L E C G Z
R M L C N S B T E Q I X L L E R L E D I G T L D C E A L E E S N I C S Ä L A U E
S N B K T U E I L C V B E N G U Q T A U H Y T L O R R A B I E Z S E L R S T A R
Ö K Y V E A L E L H H C O O R D I N A T E M A P M S T K O H I L T T E U E A L C
B L W M R N M L U A P S E A A X M W R B F H V L M T E E B L T E E K I N Z A Q U
S C I E N T L G N R A T N A V F R A M E B C P U O I A C O B E A H E S G I A I Z
M A K D E E E V G T H Ö H E R K J S C R F F N A N L F L O W R O I N T K E F M T
I R I A T X C T A S A O D F A B R U F D A T U M S I B E L N O E F P E A I O D B
K C S I Q L A N G L V L E G X A X K I C A N E C D R D N A W R Z I A L T O R B A
D H O L U F R G O V P W A P P E N R E C H T B R P A D D N U O U L Z P E I R Q B
O I U L E Ö S T E R R E I C H B E Z O G E N T W M N B I D H R H M I C G V X B E
B V R E L X E I T W B E G R I F F S K L Ä R U N G S H I N W E I S D E O A M S L
E I C N L W E B A R C H I V K F A R B L E G E N D E O P Z E E J S L B R L C P W
L E E S E T M C K W A B S A T Z T A U S H E E T D B I B R E C O R D M I R R C I
E R H P T M R B D H P T U Z O S T E X T Z R Y O K L F T V X L K Q N R E W X O K
G U O I S O K V I N F O R M A T I O N E U K U L U I O G S Ö I H A L B G N G L T
E N C E P S M I L E Y J A A O R A R C H I V B O T U O E Z M I L G R L R D M E I
P G A G F O L G E N L E I S T E K G G B B K L I A G E O Q U E L L E J A E U Q O
N I X E N M I N W R S C E D G T E N U M S O C T Ö F E A U T P H Y E E P U D Z N
F S S L L N E E A N N A X S E K L R M X E P K P O K L C N F S F L I T H T P U A
F U S S B A L L D A T E N R R E I S P I N G R N Y I I C O O R D I N A T E A W R
C R A D B C N P M N H E R M U L N F C K C N E Y O G E M J K W Z O A E T H R F Y
```

worte 5
```
DAS
T T K D E T E A J Q D J S M S R Y T D C S D S S D D S V A S
I D D H C A X S C A D Y I L D S A S C S W O A S S K S A K A
L S A S S D V W I S S K S M A P S A C A X I G J D P D S S D
J O T A S S D E D B D D A K L W S A O D R A B A D R A S S C
S M S D S S A J D L D A D D G D A S S Z A A Z S V R K D D D
S E A P F E S Z D S L J H Y L P A Q E J S A D E S X E S V F
I R D Y Q A R D D D I C A C Z Q A D S W S A J R S F F Q S S
S W D F A A S A H E R A S S I J G X F K D A A G W V B A A S
N A A I O A L A D D A P N A D U M Q A D D D H V B D A X F D
W S A D D A A V A Z S U S S Y C H G L A A D A R S S G A N A
A R A S Y M D S A H J M P D S E D G D N A D D I E C S S S Q
S D V S A D I A D A D D D F M P A T S D G S D D C D W Q S D
D B A A G D D D D S D U J Q X D A C D T D S D G S U V A A D
F S W P U S S S B D S U P U Q D X P D D A D L A R M W S H D
S I R F W S I D S A C S W A P D A D D A H D D S W F S S S B
L A D A A N D Q S D D A C C Q G D N S D S Q O S S S U A D M
D C L S B D G S D C G G A T W I A S G D S S A Q K K U F A J
S A D A K X A I A B L Q A D G A N U E A D B D O N A D T D W
D X Q S S S V J S A D E A S D Y S D A A J D S N X G C I W X
D S A A Y W A F D Q P Q S M S S S D S S G A D D D I A A A G
Z S A U S D A X S D D G A D L A A S D A Q J D L A E S S S Y
P S A S D Y A S D A A A D D V E S S S A D O D S A I A A Q D
R D R D S D Z D D X I I X Y X D C Y D S S D D S A D S S A A
S H S W Y A G G A X H V D Z A T D A Q S A X J A D W S A D A
K M P A C A B S U D S A S D S P D A B F Y S B Q P A D S C S
A C A A Q Z A I A F D S A C S S A Y A A A V V B D W K U A K
A D U D Z X P D X I V X B I H G P D A A D Z S E C S S H A S
Q G D S F O D T G L M P X T Y D D J E B G I S D A A X S A P
D F A I R X S S D D A A A A A D X S K T S S S D S J V S D C
B A A H A D S S U S I C F H S Z E T A R D S S T D Y S D D A
```

---
Quellcode
-

````python
import random
from anytree import Node


class WordData:
    def __init__(self, path: str):
        # read and declaring some variables
        with open(path, 'r', encoding='utf-8') as words_file:
            word_list_raw = words_file.read().split('\n')[:-1]

            self.GRID_SIZE = tuple(map(int, word_list_raw[0].split(' ')))
            self.GRID_X, self.GRID_Y = self.GRID_SIZE
            self.WORD_LIST = sorted(word_list_raw[2:], key=len, reverse=True)

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

        # iterates through word list
        i = 0
        while i < len(self.WORD_LIST):
            word = self.WORD_LIST[i]
            self.current_node.name[self.EXIF_KEY][self.CURRENT_WORD_KEY] = word
            if self.POSSIBLE_GUESSES_KEY not in self.current_node.name[self.EXIF_KEY]:
                possible_pos = self.get_possible_positions(word, self.current_node.name[self.EMPTY_CELLS_KEY])
                self.current_node.name[self.EXIF_KEY][self.POSSIBLE_GUESSES_KEY] = possible_pos
            else:
                possible_pos = self.current_node.name[self.EXIF_KEY][self.POSSIBLE_GUESSES_KEY]

            # if no remaining places to put word then go one node back in tree
            if len(possible_pos['x']) <= 0 and len(possible_pos['y']) <= 0:
                i += -1
                self.current_node = self.current_node.parent
                continue
            else:
                # go to random position and get all possible positions from this node on
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

    # get the row and column to check for new words
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

    # compare the frequency of words
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

    # iterates through whole list, filling every empty elem with rand letters
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] is None:

                # either fill in letter, that is is contained in the words or spawn one that isn't
                if random.randint(0, 100) < difficulty:

                    possible_letters = randomize_list(letters)

                    for letter in possible_letters:
                        # checks if it creates a new word if letter is placed here
                        if letter_is_valid(words, letter, row, column, grid):
                            # place letter
                            grid[row][column] = letter
                            break

                    if grid[row][column] is None:
                        # spawn random letter
                        grid[row][column] = chr(random.randrange(65, 91))

                else:
                    # try to spawn random letter
                    grid[row][column] = chr(random.randrange(65, 91))

    return grid


DIFFICULTY = 50
FILE = 5
PATH_INPUT = f'worte{FILE}.txt'

# get the grid
word_data = WordData(PATH_INPUT)
# fill remaining spaces with random letters
grid = fill_empty_cells(word_data, DIFFICULTY)

# print results
print('; '.join(word_data.WORD_LIST))
for row in grid:
    print(' '.join(row))

````