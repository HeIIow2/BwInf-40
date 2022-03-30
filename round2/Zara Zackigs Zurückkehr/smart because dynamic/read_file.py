def read_file(number: int, len=25):
    with open(f"examples//stapel{number}.txt", "r") as cards_file:
        cards_content = cards_file.read()
        cards_str = cards_content.split("\n")[1:-1]
        cards = []
        for card_row in cards_str:
            cards.append(int(card_row[:len], 2))
        n, k, card_len = cards_content.split("\n")[0].split(" ")
        n = int(n)
        k = int(k)
        card_len = int(card_len)

    return n, k, len, cards


if __name__ == "__main__":
    n, k, card_len, cards = read_file(2)
