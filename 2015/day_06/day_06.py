# Day 6 of Advent of Code 2015
import re
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for inst in inputs:
        ranges = list(map(lambda x: list(map(lambda x: int(x), x.split(","))), re.findall(r"\d+,\d+", inst)))
        if inst.startswith('turn off'):
            action = 0
        elif inst.startswith('turn on'):
            action = 1
        else:
            action = 2
        for x in range(ranges[0][0], ranges[1][0]+1):
            for y in range(ranges[0][1], ranges[1][1]+1):
                grid[x][y] = 1 if action == 1 else 0 if action == 0 else ((grid[x][y] + 1) % 2)

    part1 = sum([sum(x) for x in grid])
    print(f"Part1: {part1}")


    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for inst in inputs:
        ranges = list(map(lambda x: list(map(lambda x: int(x), x.split(","))), re.findall(r"\d+,\d+", inst)))
        if inst.startswith('turn off'):
            action = -1
        elif inst.startswith('turn on'):
            action = 1
        else:
            action = 2
        for x in range(ranges[0][0], ranges[1][0]+1):
            for y in range(ranges[0][1], ranges[1][1]+1):
                grid[x][y] += action
                if grid[x][y] < 0:
                    grid[x][y] = 0

    part1 = sum([sum(x) for x in grid])
    print(f"Part2: {part1}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
