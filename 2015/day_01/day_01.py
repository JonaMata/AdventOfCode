# Day 1 of Advent of Code 2015
import timeit
from collections import Counter

from aoc.helpers import *


def main():
    inputs = get_input("", example=False)
    count = Counter(inputs)
    print(f"Part 1: {count['(']-count[')']}")

    floor = 0
    pos = 0
    while floor >= 0:
        if inputs[pos] == '(':
            floor += 1
        else:
            floor -= 1
        pos += 1

    print(f"Part 2: {pos}")

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
