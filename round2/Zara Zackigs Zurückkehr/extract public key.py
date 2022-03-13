"""
In dem File ist ein publik key, k(4) private keys und 15 random keys
"""
import itertools


class Stapel:
    def __init__(self, example: int):
        def bitstring_to_bytes(s):
            return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

        with open(f"examples/stapel{example}.txt", "r") as cards_file:
            cards_content = cards_file.read()
            cards_str = cards_content.split("\n")[1:-1]
            self.cards = []
            for card_str in cards_str:
                self.cards.append(card_str)
            n, k, card_len = cards_content.split("\n")[0].split(" ")
            self.n = int(n)
            self.k = int(k)
            self.card_len = int(card_len)

        print(f"int n = {self.n};")
        print(f"int k = {self.k};")
        print(f"int card_len = {self.card_len};")
        print(f"char binary[{self.n}][{self.card_len}] = " + "{")
        for j, card in enumerate(self.cards):
            string = "  {"
            for i in range(int(self.card_len/8)):
                if i == int(self.card_len/8)-1:
                    string += f"0b{card[i*8:i*8+8]}"
                    continue
                string += f"0b{card[i*8:i*8+8]},"
            if j==len(self.cards)-1:
                string += "}"
            else:
                string += "},"
            print(string)

        print("};")

        # self.shortened = self.shorten_card()
        # print(self.shortened)
        # self.crack()

    def shorten_card(self, to_int=True):
        is_single = False
        i = 1
        shortened = []
        while not is_single:
            i += 1
            shortened = []
            for card in self.cards:
                if to_int:
                    shortened.append(int.from_bytes(card[0:i], "big"))
                else:
                    shortened.append(card[0:i])

            is_single=True
            for card in shortened:
                if shortened.count(card)-1:
                    is_single=False

        """
        if not len(shortened) % 2:
            for i, card in enumerate(shortened):
                card.append(self.cards[i][len(card)])
                shortened[i] = card
        """

        return shortened

    def crack(self):
        cards = list(reversed(self.shortened))
        k = self.k
        n = self.n

        print(cards)

        timeout = 0
        for combination in itertools.combinations(range(n), k):
            to_xor = []
            last_xor = cards[combination[0]]
            for index in combination[1:]:
                last_xor = last_xor ^ cards[index]

            if last_xor in cards:
                break

        print(last_xor, combination)






stapel = Stapel(0)
