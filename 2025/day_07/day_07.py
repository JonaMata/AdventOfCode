# Day 7 of Advent of Code 2025
import timeit
from copy import deepcopy

from aoc.helpers import *

def process_input():
    vals = get_input("\n", example=False)
    vals = [[int(y) if y in ['1','0'] else -1 for y in x.replace('S', '1').replace('.', '0')] for x in vals]
    return vals

def part1(vals):
    vals = deepcopy(vals)
    splits = 0

    for i in range(len(vals)-1):
        for j in range(len(vals[i])):
            if vals[i][j] == 1:
                if vals[i+1][j] == -1:
                    splits += 1
                    vals[i+1][j-1] = 1
                    vals[i+1][j+1] = 1
                else:
                    vals[i+1][j] = 1

    star1 = splits
    return star1

def calc_paths(rem):
    if len(rem) == 1:
        return 1
    i = rem[0].index('|')
    if rem[1][i] == '^':
        rem1 = deepcopy(rem[1:])
        rem1[0][i-1] = '|'
        rem2 = deepcopy(rem[1:])
        rem2[0][i+1] = '|'
        return calc_paths(rem1) + calc_paths(rem2)
    else:
        rem[1][i] = '|'
        return calc_paths(rem[1:])

def part2(vals):

    vals = deepcopy(vals)
    timelines = 1

    for i in range(len(vals)-1):
        for j in range(len(vals[i])):
            if vals[i][j] > 0:
                if vals[i+1][j] == -1:
                    timelines += vals[i][j]
                    vals[i+1][j-1] += vals[i][j]
                    vals[i+1][j+1] += vals[i][j]
                else:
                    vals[i+1][j] += vals[i][j]

    star2 = timelines
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
