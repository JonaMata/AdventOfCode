# Day 1 of Advent of Code 2024
import timeit
from functools import reduce

from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)
    list1 = [int(line.split('   ')[0]) for line in inputs]
    list2 = [int(line.split('   ')[1]) for line in inputs]
    list1.sort()
    list2.sort()
    star1 = sum([abs(list1[i] - list2[i]) for i in range(len(list1))])
    print(f"Star 1: {star1}")

    list2_rev = list2.copy()
    list2_rev.reverse()

    star2 = sum([num * len(list(filter(lambda x: x == num, list2))) for num in list1])

    print(f"Star 2: {star2}")

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
