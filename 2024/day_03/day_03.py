# Day 3 of Advent of Code 2024
import re
import timeit
from functools import reduce

from aoc.helpers import *


def main():
    inputs = get_input(example=False)
    muls = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)",inputs)
    star1 = sum([reduce(lambda a, b: int(a)*int(b),mul[4:-1].split(",")) for mul in muls])
    print(f"Star 1: {star1}")

    muls = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)",inputs)
    enable = True
    star2 = 0
    for match in muls:
        if match == "do()":
            enable = True
        elif match == "don't()":
            enable = False
        elif enable:
            star2 += reduce(lambda a, b: int(a)*int(b),match[4:-1].split(","))
    print(f"Star 2: {star2}")

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
