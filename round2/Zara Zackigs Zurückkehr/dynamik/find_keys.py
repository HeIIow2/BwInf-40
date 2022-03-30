
import logging
import math

logging.basicConfig(level=logging.DEBUG)

CARD_START = 0
CARD_END = 16

def read_file(number: int) -> tuple:
    with open(f"examples//stapel{number}.txt", "r") as cards_file:
        cards_content = cards_file.read()
        cards_str = cards_content.split("\n")[1:-1]
        cards = []
        for card_row in cards_str:
            cards.append(int(card_row[CARD_START:CARD_END], 2))

        n, k, card_len = cards_content.split("\n")[0].split(" ")
        n = int(n)
        k = int(k)
        card_len = int(card_len)

    return n, k, card_len, cards

def subsetXOR(arr, n) -> list:
    # Maximum possible XOR value
    m = (1 << (int)(math.log2(max(arr)) + 1)) - 1

    logging.debug(f"m: {m}")
 
 
    # The value of dp[i][j] is the number
    # of subsets having XOR of their elements
    # as j from the set arr[0...i-1]
 
    # Initializing all the values
    # of dp[i][j] as 0
    dp = [[0 for i in range(m + 1)]
             for i in range(n + 1)]
    
    trace = [[0 for i in range(m + 1)]
             for i in range(n + 1)]
     
    # The xor of empty subset is 0
    dp[0][0] = 1
 
    # Fill the dp table
    for i in range(1, n + 1):
        for j in range(m + 1):
            dp[i][j] += dp[i - 1][j]
            xored = j ^ arr[i - 1]
            if xored in arr or j in arr:
                dp[i][j] += dp[i - 1][xored]
            

            """
            if trace[i - 1][xored] < k and dp[i - 1][xored] > 0:
                trace[i][j] = trace[i - 1][xored]
                dp[i][j] += dp[i - 1][xored]

            if trace[i - 1][j] < k and dp[i - 1][j] > 0:
                trace[i][j] = trace[i - 1][j]+1
                dp[i][j] += dp[i - 1][j]"""
            

 
    # The answer is the number of subset
    # from set arr[0..n-1] having XOR of
    # elements as k
    indices = []
    for i, card in enumerate(arr):
        if dp[n][card] > 0:
            # indices.append((i, dp[n][card], card))
            logging.debug(f"index: {i}, dp: {dp[n][card]}, card: {card}, trace: {trace[n][card]}")
    return indices


n, k, card_len, cards = read_file(0)

logging.info(f"n: {n}")
logging.info(f"k: {k}")
logging.info(f"card_len: {card_len}")
logging.info(f"cards: {cards}")

sollutions = subsetXOR(cards, n)
