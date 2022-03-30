import copy


SOLUTIONS = 1, 2, 4, 6, 7, 9, 11, 14, 16


class Combinations:
    def __init__(self, n: int, k: int):
        self.n = n
        self.k = k

    def __iter__(self):
        self.indices = list(range(self.k))

        self.maximums = []
        for i in range(self.k):
            self.maximums.append(self.n-self.k+i)

        return self

    def next_indice(self, i: int):
        self.indices[i] += 1

        is_possible = True
        if self.indices[i] >= self.maximums[i]:
            if not i:
                return False, self.indices, self.indices[i]

            # call self
            is_possible, indices_, last_val = self.next_indice(i - 1)

            self.indices[i] = last_val + 1

        return is_possible, self.indices, self.indices[i]

    def __next__(self):
        possible, indices, p = self.next_indice(self.k-1)
        if not possible:
            raise StopIteration

        return indices


def xor_at(to_xor: list, xor_at: int):
    xored = to_xor[0][xor_at]
    for element in to_xor[1:]:
        xored = xored ^ element[xor_at]
    return xored

class File:
    def __init__(self, n: int, k: int, length: int, cards: list) -> None:
        self.n = n
        self.k = k
        self.length = length
        self.cards = cards

        print(f"n: {self.n}; k: {self.k}")

        # einteilen der binary in listen
        self.sorted_by_bits = [
            [],
            []
        ]

        for i, card in enumerate(self.cards):
            self.sorted_by_bits[card[0]].append(i)

        print(f"sortet by bits: {self.sorted_by_bits}")

        self.number_of_bits = []

        for i in range(0, self.k+1):
            # i ist die nummer an 1en
            self.number_of_bits.append((self.k - i, i))

        # sort number of bits by the max
        self.number_of_bits.sort(key=lambda x: max(x))


        print("number of zeroes: ", self.number_of_bits[0])
        print("number of ones: ", self.number_of_bits[1])

        for i, card in enumerate(self.cards):
            is_key, self.key_indices = self.check_card(i, card, debug=True)
            if is_key:
                print("found")
                print(self.key_indices)
                for i in self.key_indices:
                    print(File.card_to_string(self.cards[i]))
                return
        print("something went wrong")

    @staticmethod
    def card_to_string(card: list) -> str:
        string = ""
        for bit in card:
            if bit:
                string += "1 "
            else:
                string += "0 "

        return string

    def check_card(self, index: int, card: list, debug=False):
        if debug:
            print(f"\nchecking card: {index} -> {card}\n")

        current_sorted_bits = copy.deepcopy(self.sorted_by_bits)
        current_sorted_bits[card[0]].remove(index)
        print(f"current sorted bits: {current_sorted_bits}")

        for zeroes, ones in self.number_of_bits:
            new_cards = self.check_bit(zeroes, current_sorted_bits[True], debug=debug)
            is_key, indices = self.check_with_card(new_cards, ones, current_sorted_bits[False], debug=debug)

            if is_key:
                return True, indices

        return False, []

    def check_with_card(self, next_cards: list, count: int, indices_pool: list, debug=False):
        if not count:
            return True, indices_pool

        if debug:
            print(f"checking bit with count {count} and pool {indices_pool}")

        n = len(indices_pool)
        if count > n:
            return False, []

        combinations = iter(Combinations(len(indices_pool), count))
        for indices in combinations:
            # print(indices)
            cards_indices = []
            cards = []
            for index in indices:
                cards_indices.append(indices_pool[index])
                cards.append(self.cards[cards_indices[-1]])

            def compare_cards(cards_: list, start_at=1):
                candidates = next_cards[start_at][xor_at(cards_, start_at)]

                for j in range(start_at + 1, self.length):
                    new_candidates = []

                    for candidate in candidates:
                        if candidate in next_cards[j][xor_at(cards_, j)]:
                            new_candidates.append(candidate)

                    if len(new_candidates):
                        candidates = list(new_candidates)
                    else:
                        return False, []

                return True, candidates

            is_valid, candidates = compare_cards(cards)

            if is_valid:
                print(cards_indices, candidates)
                cards_indices.extend(candidates)
                return True, cards_indices

        return False, []

    def check_bit(self, count: int, indices_pool: list, debug=False):
        n = len(indices_pool)

        if debug:
            print(f"checking bit with count {count} and pool {indices_pool}")

        next_cards = []
        for i in range(self.length):
            next_cards.append([[], []])

        if not count:
            for j, card in enumerate(self.cards):
                for i in range(self.length):
                    next_cards[i][card[i]].append(j)

            return next_cards

        if count > n:
            return next_cards

        combinations = iter(Combinations(n, count))
        for indices in combinations:
            cards_indices = []
            cards = []
            for index in indices:
                cards_indices.append(indices_pool[index])
                cards.append(self.cards[cards_indices[-1]])

            for j in range(0, self.length):
                next_cards[j][xor_at(cards, j)].append(list(cards_indices))

        return next_cards



if __name__ == "__main__":
    combinations = iter(Combinations(20, 3))
    for i in combinations:
        print(i)

