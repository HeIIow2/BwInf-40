from anytree import Node, RenderTree, PostOrderIter
from anytree.exporter import DotExporter

print("die 5. hotelliste braucht eine weile um zu laufen,\n"
      "deshalb habe ich kleine progress debug ausgaben eingebaut.")

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
        current_rating = branch_exif[RATING]
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
                if current_rating > hotel[1]:
                    new_rating = hotel[1]
                else:
                    new_rating = current_rating

                possible_branches.append(
                    {HOTEL: i, TIME: hotel[0], RATING: new_rating, STOPS: used_stops + 1})

        return possible_branches


# dictionary keys
NEXT_STOPS = 'next stops'
STOPS = 'stops'
RATING = 'rating'
TIME = 'time'
HOTEL = 'hotel'

# run through all hotel-lists
for t in range(1, 6, 1):
    print(f'\n\nhotels{t}.txt\n')
    # create class for all of the work with the provided data
    hotels = Hotels(f'hotels{t}.txt')
    # initialize the root of the data tree
    travel_tree = Node({HOTEL: -1, TIME: 0, RATING: 9999.0, STOPS: 0})
    for i in range(hotels.max_stops):
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
                if counter % 15000 == 0:
                    print(f'progress {counter}')

    # find the leave with the highest rating
    max = 0.0
    max_node = None
    leaves = travel_tree.leaves
    for leave in leaves:
        if max < leave.name[RATING]:
            max = leave.name[RATING]
            max_node = leave

    # prints out the best path in the required format
    path = max_node.path
    for i in range(1, len(path), 1):
        stop_dict = path[i].name
        print(f'stop: {stop_dict[STOPS]}; hotel: {stop_dict[HOTEL]}; time: {stop_dict[TIME]}; rating: {stop_dict[RATING]}')
