# Datenklasse für die Hotels
class Hotel:
    def __init__(self, index: int, rating: float, travel_time: int):
        self.index = index
        self.rating = rating
        self.travel_time = travel_time


# Klasse um die Hotellisten einzulesen und zu bearbeiten
class Vacation:
    def __init__(self, file_path: str):
        self.name = file_path
        with open(file_path, 'r') as hotel_file:
            raw_data = hotel_file.read().split("\n")

            # Gesamtfahrzeit
            self.total_time = int(raw_data[1])

            # liste von allen hotels (jeweils in der Datenklasse gespeichert)
            hotels_str = raw_data[2:-1]
            self.hotels = []
            for i, hotel_str in enumerate(hotels_str):
                time, rating = hotel_str.split(' ')
                self.hotels.append(Hotel(i, float(rating), int(time)))

        # Der start (zuhause)
        root = Hotel(-1, 99999, 0)

        # der Pfad
        # hier werden alle mögliche nächsten Hotels gespeichert von höchster Bewertung zu niedrigster
        # die Anzahl der Listen entspricht der Anzahl der Stoppe
        self.path = [
            [root],
            [],
            [],
            [],
            []
        ]

        self.STOPS = len(self.path)
        # 6h = 360min
        self.MAX_TIME_BEFORE_HOTEL = 360
        # die beste Bewertung eines Pfades
        # alle Hotels mit einer Bewertung unter diesem Wert werden ignoriert
        self.highest_rating = 0
        self.winning_paths = []

        # mit dem eigentlichen Algorithmus starten
        success = 0
        while success != -1:
            success = self.fill_path()
            while len(self.path[-1]) != 0:
                success = self.set_max_minimum()

        self.print_results()
        print("```")

    def print_results(self):
        # guard clauses um das Ergebnis richtig auszugeben

        print(f"**{self.name}**")

        if len(self.winning_paths) <= 0:
            # print(f"____________________{self.name}____________________")
            print("\n```\nEs wurde kein valider Pfad gefunden.")
            return

        # print(f"______________{self.name} min:{self.highest_rating}__________________")
        print(f"- {self.highest_rating}\n```")

        if len(self.winning_paths) == 1:
            if len(self.winning_paths) > 0:
                self.print_path(self.winning_paths[0])
            return

        if len(self.winning_paths) > 1:
            print(f"Es gibt {len(self.winning_paths)} Wege, die gleich gut sind.")
            for i, path in enumerate(self.winning_paths):
                print(f"\nRoute {i + 1}:")
                self.print_path(path)


    @staticmethod
    def print_path(path: list):
        for stop, hotel in enumerate(path[1:]):
            print(f'stop: {stop}; hotel: {str(hotel.index).zfill(4)}; time: {str(hotel.travel_time).zfill(4)}; rating: {hotel.rating}')

    def shorten_solutions(self):
        solutions = {}

        for solution in self.winning_paths:
            solutions[solution[-2]] = solution

        self.winning_paths = solutions.values()

    def fill_path(self):
        # füllt den pfad mit neuen optionen auf
        # finde das erste Element mit keinen Optionen
        for i, hotel_options in enumerate(self.path):
            if len(hotel_options) == 0:
                break

        if i == 0:
            return -1

        # wiederhole so lange bis alles aufgefüllt wurde
        while i < len(self.path):
            # fülle das nächste Element auf
            self.path[i] = self.get_all_possible_hotels(self.path[i-1][0], i-1)

            # wenn keine möglichen auffüllungen gefunden worden sind, gehe nicht zum nächsten element
            # und lösche der erste eintrag bei dem Referenzelement
            if len(self.path[i]) == 0:
                i = self.remove_one_elem_from_path(i-1) + 1
                if i == 0:
                    return -1
            else:
                i += 1

        return 1

    def remove_one_elem_from_path(self, i: int):
        # entfernt ein element von den Pfadoptionen
        # wenn dies dann leer ist entfernt die Funktion rekursiv weitere Elemente,
        # bis das vorherige Element nicht leer ist.
        self.path[i] = self.path[i][1:]
        if len(self.path[i]) == 0:
            if i == 1:
                return -1

            return self.remove_one_elem_from_path(i-1)

        return i

    def set_max_minimum(self):
        # speicher das neue minimum
        minimum_of_path = 99999
        current_path = []

        for element in self.path:
            current_path.append(element[0])
            if element[0].rating < minimum_of_path:
                minimum_of_path = element[0].rating

        # kontrolliert, ob man von dem letzten Hotel in 360 minuten zu dem Ziel kommt
        # (lediglich falls ich ein bug habe)
        path_works = True
        latest_stop = current_path[-1].travel_time
        if self.total_time - latest_stop > self.MAX_TIME_BEFORE_HOTEL:
            success = self.remove_one_elem_from_path(len(self.path) - 1)
            path_works = False

        if minimum_of_path > self.highest_rating:
            self.highest_rating = minimum_of_path
            self.winning_paths = [current_path]
        elif minimum_of_path == self.highest_rating:
            self.winning_paths.append(current_path)

        success = self.remove_one_elem_from_path(len(self.path)-1)
        if success == -1:
            return -1
        return 1

    def get_all_possible_hotels(self, root_hotel: Hotel, step: int):
        # diese Funktion gibt eine Liste alle Hotels zurück, die von einem Starthotel aus erreichbar sind.
        possible_hotels = []

        # berechnet den kleinsten Zeitschritt, dass die Zeit noch reichen kann.
        min_time = self.total_time - ((self.STOPS - (step + 1)) * self.MAX_TIME_BEFORE_HOTEL)
        max_time = root_hotel.travel_time + self.MAX_TIME_BEFORE_HOTEL

        # fügt jedes hotel, dessen Reisezeit innerhalb min_time und max_time ist
        # und dessen Bewertung höher gleich die beste pfadbewertung ist.
        for hotel in self.hotels[root_hotel.index + 1:]:
            if hotel.travel_time > max_time:
                break
            if min_time < hotel.travel_time and hotel.rating >= self.highest_rating:
                possible_hotels.append(hotel)

        # sortiere die Hotels nach der Bewertung
        possible_hotels = Vacation.sort_hotels(possible_hotels)

        return possible_hotels

    @staticmethod
    def sort_hotels(hotels: list):
        # sortiert eine Liste von Hotels absteigend nach ihrer Bewertung
        # nutzt insertion sort

        for hotel_index in range(1, len(hotels)):
            current_hotel = hotels[hotel_index]
            i = hotel_index - 1

            while i >= 0 and current_hotel.rating > hotels[i].rating:
                hotels[i + 1] = hotels[i]
                i -= 1

            hotels[i + 1] = current_hotel

        return hotels


# Die Schleife lässt das Programm auf allen 5 Beispielen laufen
for i in range(1, 6, 1):
    vacation = Vacation(f"hotels{i}.txt")
    print("\n")
