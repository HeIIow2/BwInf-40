import find_keys


def read_file(number: int):
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

    return n, k, card_len, cards


def xor_2_cards(card1, card2):
    return [card1[i] ^ card2[i] for i in range(len(card1))]

def print_card_as_bits(card):
    # print false as 0 and true as 1
    for i in range(len(card)):
        if card[i]:
            print("1", end="")
        else:
            print("0", end="")
    print("")


if __name__ == "__main__":
    n, k, card_len, cards = read_file(2)
    find_keys.File(n, k, card_len, cards)

