# Day 1 of Advent of Code 2025
import timeit
from aoc.helpers import *

def process_input():
    vals = get_input("\n", example=False)
    vals = [int(x[1:]) * (-1 if x[0] == 'L' else 1) for x in vals]
    return vals

def part1(vals):
    zeroes = 0
    cur = 50
    for op in vals:
        cur += op
        cur %= 100
        if cur == 0:
            zeroes += 1
    star1 = zeroes
    return star1

def part2(vals):
    zeroes = 0
    cur = 50
    for op in vals:
        if cur == 0 and op < 0:
            zeroes -= 1
        cur += op
        zeroes += abs(cur // 100)
        if cur == 0 or (cur%100 == 0 and op < 0):
            zeroes += 1
        cur %= 100
    star2 = zeroes
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
