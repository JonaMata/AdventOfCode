# Day 4 of Advent of Code 2025
import timeit
from aoc.helpers import *
import numpy as np

def process_input():
    vals = get_input("\n", example=False)
    vals = np.array([[1 if y=='@' else 0 for y in x] for x in vals])
    return vals

def part1(vals):
    roll_count = 0
    print(vals.shape)
    for x in range(vals.shape[0]):
        for y in range(vals.shape[1]):
            if vals[x,y] == 0:
                continue
            test_vals = vals[max(0,x-1):min(x+2,vals.shape[0]),max(0,y-1):min(y+2,vals.shape[1])]
            if np.count_nonzero(test_vals) < 5:
                roll_count += 1

    star1 = roll_count
    return star1

def remove_rolls(vals):
    remove = []
    for x in range(vals.shape[0]):
        for y in range(vals.shape[1]):
            if vals[x,y] == 0:
                continue
            test_vals = vals[max(0,x-1):min(x+2,vals.shape[0]),max(0,y-1):min(y+2,vals.shape[1])]
            if np.count_nonzero(test_vals) < 5:
                remove.append((x,y))
    for item in remove:
        vals[item[0],item[1]] = 0
    return len(remove)

def part2(vals):
    total = 0
    prev = 1
    while prev > 0:
        prev = remove_rolls(vals)
        total += prev
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
