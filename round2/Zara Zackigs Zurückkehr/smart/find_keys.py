import copy


class File:
    def __init__(self, n: int, k:int, length: int, cards: str) -> None:
        self.n = n
        self.k = k
        self.length = length
        self.cards = cards

        print(f"n: {self.n}; k: {self.k}")

        # einteilen der binary in listen
        self.sorted_by_bits = [
            [], # 0
            []  # 1
        ]

        for i, card in enumerate(self.cards):
            self.sorted_by_bits[card[0]].append(i)

        print(f"sortet by bits: {self.sorted_by_bits}")

        self.number_of_bits = [
            [],     # 0
            []      # 1
        ]

        for i in range(0,self.k+1):
            # i ist die nummer an 1en
            self.number_of_bits[i%2].append((self.k-i, i))

        print("number of zeroes: ",self.number_of_bits[0])
        print("number of ones: ",self.number_of_bits[1])

        for i, card in enumerate(self.cards):
            is_key, self.key_indices = self.check_card(i, card, debug=True)
            if is_key:
                print("found")
                print(self.key_indices)
                return
        print("something went wrong")


    def check_card(self, index: int, card: list, debug=False) -> bool:
        if debug:
            print(f"\nchecking card: {index} -> {card}\n")

        current_sorted_bits = copy.deepcopy(self.sorted_by_bits)
        current_sorted_bits[card[0]].remove(index)
        print(self.sorted_by_bits)

        indices = [index]

        # ekelhafter code :)
        for zeroes, ones in self.number_of_bits[card[0]]:
            if zeroes < ones:
                is_valid, indices_ = self.check_bit(zeroes, False, card, current_sorted_bits, debug=debug)
                if is_valid:
                    indices.extend(indices_)
                    is_valid, indices_ = self.check_bit(ones, True, card, current_sorted_bits, debug=debug)
                    if is_valid:
                        indices.extend(indices_)
                        return True, indices
            else:
                is_valid, indices_ = self.check_bit(ones, True, card, current_sorted_bits, debug=debug)
                if is_valid:
                    indices.extend(indices_)
                    is_valid, indices_ = self.check_bit(zeroes, False, card, current_sorted_bits, debug=debug)
                    if is_valid:
                        indices.extend(indices_)
                        return True, indices

        return False, []


    def check_bit(self, count: int, is_one:bool, card: list, current_bits: list, debug=False) -> bool:
        if not count:
            return True, []

        indices_pool = current_bits[is_one]
        if debug:
            print(f"checking bit with count {count} and pool {indices_pool}")

        n = len(indices_pool)
        if count > n:
            return False, []
        indices = list(range(count))

        def next_indice(indices_ :list, i:int):
            indices_[i] += 1

            is_possible = True
            if indices_[i] >= n-(count-i-1):
                if not i:
                    return False, indices_, indices_[i]
                is_possible, indices_, last_val = next_indice(indices_, i-1)
                indices_[i] = last_val+1

            return is_possible, indices_, indices_[i]

        while True:
            # print(indices)
            cards_indices = []
            cards = []
            for index in indices:
                cards_indices.append(indices_pool[index])
                cards.append(self.cards[cards_indices[-1]])

            def compare_cards(card_:list, cards_:list, start_at=1) -> bool:
                for j in range(start_at, self.length):
                    addet = 0
                    for card_elem in cards_:
                        addet += card_elem[j]

                    if bool(addet%2) != card_[j]:
                        return False
                
                return True


            if compare_cards(card, cards):
                return True, cards_indices
            
            possible, indices, p = next_indice(indices, len(indices)-1)
            if not possible:
                break

        return False, []



def read_file(number: int) -> File:
    with open(f"examples//stapel{number}.txt", "r") as cards_file:
        cards_content = cards_file.read()
        cards_str = cards_content.split("\n")[1:-1]
        cards = []
        for card_row in cards_str:
            cards.append([])
            for card_bool in card_row:
                cards[-1].append(bool(int(card_bool)))
        n, k, card_len = cards_content.split("\n")[0].split(" ")
        n = int(n)
        k = int(k)
        card_len = int(card_len)

    return File(n,k,card_len,cards)

file = read_file(1)
