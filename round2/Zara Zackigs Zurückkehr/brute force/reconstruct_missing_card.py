def reconstruct(example: int, missing: int):
    with open(f"examples/stapel{example}.txt", "r") as cards_file:
        cards_str = cards_file.read().split("\n")[1:-1]
        cards = []
        for card_str in cards_str:
            cards.append([])
            for byte in card_str:
                cards[-1].append(bool(int(byte)))

        print(cards)

    # get the private key
    


reconstruct(0, 0)
