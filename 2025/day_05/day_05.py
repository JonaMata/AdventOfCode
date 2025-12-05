# Day 5 of Advent of Code 2025
import timeit
from aoc.helpers import *

def process_input():
    vals = get_input("\n\n", example=False)
    vals[0] = [ [int(y) for y in x.split('-')] for x in vals[0].split('\n')]
    vals[1] = [int(x) for x in vals[1].split('\n')]
    return vals

def part1(vals):
    fresh = 0
    for ingredient in vals[1]:
        for fresh_range in vals[0]:
            if fresh_range[0] <= ingredient <= fresh_range[1]:
                fresh += 1
                break
    star1 = fresh
    return star1

def merge_ranges(ranges):
    new_ranges = []
    for i in range(len(ranges)):
        cur_range = ranges[i]
        merged = False
        for new_range in new_ranges:
            if cur_range[0] <= new_range[1] and new_range[0] <= cur_range[1]:
                new_range[0] = min(new_range[0], cur_range[0])
                new_range[1] = max(new_range[1], cur_range[1])
                merged = True
                break
        if not merged:
            new_ranges.append(cur_range)
    return new_ranges


def part2(vals):
    ranges = merge_ranges(vals[0])
    new_ranges = merge_ranges(ranges)
    newer_ranges = merge_ranges(new_ranges)
    total = 0
    for rang in newer_ranges:
        total += rang[1]-rang[0]+1
    star2 = total
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
