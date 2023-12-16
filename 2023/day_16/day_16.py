# Day 16 of Advent of Code 2023
import sys
import timeit

from aoc.helpers import *


def rec_follow_mirror(pos, direction, memory, visited, grid):
    if (pos, direction) in memory:
        return
    memory.add((pos, direction))
    next_pos = pos[0] + direction[0], pos[1] + direction[1]
    if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])):
        return

    visited.add(next_pos)
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

    # print(f"pos: {pos}, direction: {direction}, next_pos: {next_pos}, next_dirs: {next_dirs}, next_grid: {next_grid}")
    for next_dir in next_dirs:
        rec_follow_mirror(next_pos, next_dir, memory, visited, grid)


def main():
    inputs = get_input("\n", example=False)
    visited = set()

    sys.setrecursionlimit(10**6)

    rec_follow_mirror((0, -1), (0, 1), set(), visited, inputs)

    energised = [['#' if (y, x) in visited else '.' for x in range(len(inputs[0]))] for y in range(len(inputs))]
    # print_2d(energised)
    print(f"Part1: {len(visited)}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer() - start}s")
