# Day 11 of Advent of Code 2023
import timeit
from bisect import bisect

from aoc.helpers import *


def calc_distances(galaxies, extra):
    distance_sum = 0
    pairs = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            g1 = galaxies[j]
            g2 = galaxies[i]
            dist = abs((g2[0]+g2[2]*extra)-(g1[0]+g1[2]*extra))+abs((g2[1]+g2[3]*extra)-(g1[1]+g1[3]*extra))
            distance_sum += dist
            pairs += 1
    return distance_sum


def main():
    inputs = get_input("\n", example=False)
    grid = [[x for x in line] for line in inputs]
    add_rows = []
    add_columns = []

    for y in range(len(grid)):
        line = grid[y]
        if '#' not in line:
            add_rows.append(y)
    for x in range(len(grid[0])):
        line = [line[x] for line in grid]
        if '#' not in line:
            add_columns.append(x)

    galaxies = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '#':
                extra_y = bisect(add_rows, y)
                extra_x = bisect(add_columns, x)
                galaxies.append((y, x, extra_y, extra_x))

    print(f"Part 1: {calc_distances(galaxies, 1)}")
    print(f"Part 2: {calc_distances(galaxies, 1000000-1)}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
