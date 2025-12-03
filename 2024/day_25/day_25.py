# Day 25 of Advent of Code 2024
import timeit
import numpy as np
from aoc.helpers import *

def process_input():
    vals = [np.array([[y for y in x] for x in line.split("\n")]) for line in get_input("\n\n", example=False)]
    locks = list(filter(lambda x: x[0,0] == '#', vals))
    keys = list(filter(lambda x: x[-1,-1] == '#', vals))

    locks = [[list(lock[:,col]).count('#') for col in range(lock.shape[1])] for lock in locks]
    keys = [[list(key[:,col]).count('#') for col in range(key.shape[1])] for key in keys]
    print(locks)
    return locks, keys

def part1(vals):
    locks, keys = vals
    total = 0
    for lock in locks:
        for key in keys:
            fits = True
            for i in range(len(lock)):
                if lock[i]+key[i] > 7:
                    fits = False
                    break
            if fits:
                total += 1

    star1 = total
    return star1

def part2(vals):
    star2 = None
    return star2


if __name__ == "__main__":
    start_total = timeit.default_timer()
    start_input = start_total
    inputs = process_input()
    print(f"Input processed, time taken: {(timeit.default_timer()-start_input)*1000:.2f}ms")
    start_part1 = timeit.default_timer()
    print(f"Part 1: {part1(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part1)*1000:.2f}ms")
    start_part2 = timeit.default_timer()
    print(f"Star 2: {part2(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part2)*1000:.2f}ms")

    print(f"\n Total time taken: {(timeit.default_timer()-start_total)*1000:.2f}ms")
