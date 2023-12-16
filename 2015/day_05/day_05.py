# Day 5 of Advent of Code 2015
import timeit
from functools import reduce

from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)
    vowels = 'aeiou'
    forbidden = ['ab', 'cd', 'pq', 'xy']
    nice_strings = 0
    for string in inputs:
        if any([f in string for f in forbidden]):
            continue
        if sum([string.count(v) for v in vowels]) < 3:
            continue
        if any([string[i] == string[i+1] for i in range(len(string)-1)]):
            nice_strings += 1

    print(f"Part1: {nice_strings}")

    nice_strings = 0
    for string in inputs:
        if any([string.count(string[i:i+2]) > 1 for i in range(len(string)-2)]):
            if any([string[i] == string[i+2] for i in range(len(string)-2)]):
                nice_strings += 1

    print(f"Part2: {nice_strings}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
