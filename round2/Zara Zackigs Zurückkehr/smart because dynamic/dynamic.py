import logging
import enum
import copy
import random

import read_file

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

REMOVING_CARDS = 3

class Node(enum.Enum):
    xor = "xor"
    remaining_indices = "remaining_indices"
    current_index = "current_index"
    result = "result"


n, k, card_len, cards = read_file.read_file(2)

logging.info("n: %s, k: %s, card_len: %s", n, k, card_len)
logging.info("cards: %s", cards)

probability = float(n - 0-k) / float(n)
for i in range(1, REMOVING_CARDS):
    probability *= float(n - k-i) / float(n-i)
logging.info("the propability with removing %s cards to not fail is %s", REMOVING_CARDS, probability)


# xor, used_indices
remaining_indices = list(range(n))
random.shuffle(remaining_indices)
root = {Node.xor: 0, Node.remaining_indices: remaining_indices, Node.current_index: -1, Node.result: []}
tree = [root]

depth = 0
prev_depth = 0

while True:
    if prev_depth != depth and depth < 7:
        prev_depth = depth
        logging.info(depth)
    node = tree[depth]

    new_node = {Node.current_index: node[Node.remaining_indices][0]}

    node[Node.remaining_indices].pop(0)

    new_node[Node.remaining_indices] = node[Node.remaining_indices].copy()

    new_node[Node.xor] = node[Node.xor] ^ cards[new_node[Node.current_index]]

    new_node[Node.result] = copy.copy(node[Node.result])
    new_node[Node.result].append(new_node[Node.current_index])

    if len(new_node[Node.remaining_indices]) <= k-depth:
        tree.pop(depth)
        depth -= 1
        continue

    if depth >= k-1:
        if new_node[Node.xor] in cards:
            if cards.index(new_node[Node.xor]) not in new_node[Node.result]:
                tree.append(new_node)
                break
        continue

    tree.append(new_node)
    depth += 1

logging.info("result: %s", tree[-1][Node.result])
