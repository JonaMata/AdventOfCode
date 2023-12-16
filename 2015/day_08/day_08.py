# Day 8 of Advent of Code 2015
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)
    diff = 0
    for string in inputs:
        diff += len(string) - len(eval(string))

    print(f"Part1: {diff}")

    diff = 0
    for string in inputs:
        diff += 2 + string.count('"') + string.count('\\')

    print(f"Part2: {diff}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
