# Day 19 of Advent of Code 2024
import timeit
from multiprocessing import Pool

from aoc.helpers import *

cache = dict()
count_cache = dict()

def check_design(design, patterns, max_len):
    if len(design) == 0:
        return True
    if design in cache:
        return cache[design]
    for i in range(min(max_len, len(design)), 0, -1):
        if design[:i] in patterns:
            if check_design(design[i:], patterns, max_len):
                cache[design] = True
                return True
    cache[design] = False
    return False

def count_design(design, patterns, max_len):
    if len(design) == 0:
        return 1
    if design in count_cache:
        return count_cache[design]
    count = 0
    for i in range(min(max_len, len(design)), 0, -1):
        if design[:i] in patterns:
            count += count_design(design[i:], patterns, max_len)
    count_cache[design] = count
    return count

def process_input():
    patterns, designs = get_input("\n\n", example=False)
    patterns = set(patterns.split(", "))
    designs = designs.split("\n")
    max_len = max([len(patt) for patt in patterns])
    return designs, patterns, max_len

def part1(inputs):
    designs, patterns, max_len = inputs
    star1 = sum([1 if count_design(design, patterns, max_len) > 0 else 0 for design in designs])
    print(f"Star 1: {star1}")

def part2(inputs):
    designs, patterns, max_len = inputs
    star2 = sum([count_design(design, patterns, max_len) for design in designs])
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    inputs = process_input()
    start = timeit.default_timer()
    part1(inputs)
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
    start = timeit.default_timer()
    part2(inputs)
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
