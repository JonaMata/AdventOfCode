# Day <DAY> of Advent of Code <YEAR>
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)
    print(inputs)


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
