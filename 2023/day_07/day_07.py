# Day 7 of Advent of Code 2023
from collections import Counter

from aoc.helpers import *

card_map = {
    'T': 'B',
    'J': 'C',
    'Q': 'D',
    'K': 'E',
    'A': 'F',
    'C': '1'
}

def calculate_score(hand):
    count = Counter(hand)
    jokers = count['1'] if '1' in count else 0
    if jokers == 5:
        return '6'+hand
    del count['1']
    sets = sorted(list(count.values()))
    if sets[-1]+jokers == 5:
        hand_type = '6'
    elif sets[-1]+jokers == 4:
        hand_type = '5'
    elif sets[-1]+jokers == 3:
        if sets[-2] == 2:
            hand_type = '4'
        else:
            hand_type = '3'
    elif sets[-1]+jokers == 2:
        if sets[-2] == 2:
            hand_type = '2'
        else:
            hand_type = '1'
    else:
        hand_type = '0'

    return hand_type+hand


if __name__ == "__main__":
    inputs = get_input("\n", example=False)

    hands = [l.split(' ') for l in inputs]

    for hand in hands:
        hand[0] = ''.join([card_map[x] if x in card_map else x for x in hand[0]])

    scored_hands = map(lambda x: (calculate_score(x[0]), x[1]), hands)
    scored_hands = sorted(scored_hands, key=lambda x: x[0])

    scores = [(i + 1) * int(h[1]) for i, h in enumerate(scored_hands)]

    print(f"Part 1: {sum(scores)}")

    for hand in hands:
        hand[0] = ''.join([card_map[x] if x in card_map else x for x in hand[0]])

    scored_hands = map(lambda x: (calculate_score(x[0]), x[1]), hands)
    scored_hands = sorted(scored_hands, key=lambda x: x[0])
    scores = [(i + 1) * int(h[1]) for i, h in enumerate(scored_hands)]

    print(f"Part 2: {sum(scores)}")
