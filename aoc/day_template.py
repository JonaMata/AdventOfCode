# Day <DAY> of Advent of Code <YEAR>
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)

    star1 = None
    print(f"Star 1: {star1}")


    star2 = None
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
