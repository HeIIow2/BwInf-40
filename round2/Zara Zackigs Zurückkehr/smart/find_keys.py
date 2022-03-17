class File:
    def __init__(self, n: int, k:int, length: int, cards: str) -> None:
        self.n = n
        self.k = k
        self.length = length
        self.cards = cards

        print(f"n: {self.n}; k: {self.k}")

        # einteilen der binary in listen
        sorted_by_bits = [
            [],     # 0
            []      # 1
        ]

        for i in range(self.length):
            sorted_by_bits[0].append([])
            sorted_by_bits[1].append([])

            for j, card in enumerate(self.cards):
                sorted_by_bits[card[i]][i].append(j)

        number_of_bits = [
            [],     # 0
            []      # 1
        ]
        for i in range(self.k+1):
            # i ist die nummer an 1en
            number_of_bits[i%2].append((i, self.k-i))

        print(number_of_bits[0])
        print(number_of_bits[1])

        




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
