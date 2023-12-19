# Day 16 of Advent of Code 2023
import sys
import timeit

import numpy as np

from aoc.helpers import *


def rec_follow_mirror(pos, direction, visited, memory, grid):
    if (pos, direction) in memory:
        val = memory[(pos, direction)]
        print(f"Hit memory, {pos=}, {direction=}, {val.sum()=}")
        return memory[(pos, direction)]
    result = np.full((len(grid), len(grid[0])), False)

    next_pos = pos[0] + direction[0], pos[1] + direction[1]
    if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])):
        return result

    result[next_pos[0]][next_pos[1]] = True
    # memory[(pos, direction)] = result

    if (pos, direction) in visited:
        return result
    visited.add((pos, direction))

    next_grid = grid[next_pos[0]][next_pos[1]]
    next_dirs = []
    if next_grid == '/':
        next_dirs.append((direction[1] * -1, direction[0] * -1))
    elif next_grid == '\\':
        next_dirs.append((direction[1], direction[0]))
    elif next_grid in '-|':
        if next_grid == '-':
            split_dirs = [(0, -1), (0, 1)]
        else:
            split_dirs = [(-1, 0), (1, 0)]
        if direction in split_dirs:
            next_dirs.append(direction)
        else:
            next_dirs.extend(split_dirs)
    else:
        next_dirs.append(direction)

    for next_dir in next_dirs:
        result = np.logical_or(result, rec_follow_mirror(next_pos, next_dir, visited, memory, grid))

    memory[(pos, direction)] = result
    return result


def find_most_energised(grid):
    memory = dict()
    maximum = 0
    for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        for j in range(len(grid)):
            if direction[0] == 0:
                start_pos = (j, -1 if direction[1] == 1 else len(grid))
            else:
                start_pos = (-1 if direction[0] == 1 else len(grid), j)
            val = rec_follow_mirror(start_pos, direction, set(), memory, grid).sum()
            print(f"{start_pos=}, {direction=}, {val=}")
            maximum = max(maximum, val)
    return maximum


def main():
    inputs = get_input("\n", example=True)

    sys.setrecursionlimit(10 ** 6)

    energised = rec_follow_mirror((0, -1), (0, 1), set(), dict(), inputs)

    print(f"Part1: {energised.sum()}")

    print(f"Part2: {find_most_energised(inputs)}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer() - start}s")
