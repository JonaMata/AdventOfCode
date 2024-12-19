# Day 19 of Advent of Code 2024
import timeit
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

def main():
    patterns, designs = get_input("\n\n", example=False)
    patterns = patterns.split(", ")
    designs = designs.split("\n")
    max_len = max([len(patt) for patt in patterns])

    star1 = sum([1 if check_design(design, patterns, max_len) else 0 for design in designs])
    print(f"Star 1: {star1}")


    star2 = sum([count_design(design, patterns, max_len) for design in designs])
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
