# Day 4 of Advent of Code 2015
import timeit
from hashlib import md5

from aoc.helpers import *


def main():
    inputs = get_input(None, example=False).read()
    print(inputs)
    found = False
    i = 0
    while not found:

        hashed = md5((inputs+str(i)).encode()).hexdigest()
        if hashed.startswith('00000'):
            found = True
        else:
            i += 1

    print(f"Part1: {i}")

    found = False
    while not found:

        hashed = md5((inputs+str(i)).encode()).hexdigest()
        if hashed.startswith('000000'):
            found = True
        else:
            i += 1

    print(f"Part2: {i}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
