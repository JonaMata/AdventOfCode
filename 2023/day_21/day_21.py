# Day 21 of Advent of Code 2023
import timeit
import bisect

from aoc.helpers import *


def find_neighbours(node, grid):
    dirs = {'up': (-1, 0), 'right': (0, 1), 'down': (1, 0), 'left': (0, -1)}
    neighbours = []
    for i, direction in dirs.items():
        neighbour = (node[0] + direction[0], node[1] + direction[1])
        # if 0 <= neighbour[0] < len(grid) and 0 <= neighbour[1] < len(grid[0]):
        if grid[neighbour[0] % len(grid)][neighbour[1] % len(grid[0])] in '.S':
            neighbours.append(neighbour)

    return neighbours

def find_inf_options(start, grid, max_steps):
    search = [(start, 0)]

    memory = dict()
    visited = set()
    options = 0


def find_options(start, grid, max_steps):
    search = [(start, 0)]

    visited = set()
    options = 0

    while len(search) > 0:
        node = search.pop(0)
        coord, steps = node

        if coord in visited:
            continue

        visited.add(coord)

        if steps % 2 == max_steps % 2:
            options += 1
            if steps == max_steps:
                continue

        for neighbour in find_neighbours(coord, grid):
            neighbour_node = (neighbour, steps + 1)
            search.append(neighbour_node)

    return options


def main():
    inputs = get_input("\n", example=False)
    start = [None]
    i = 0
    while not start[0]:
        y = i // len(inputs)
        x = i % len(inputs)
        if inputs[y][x] == 'S':
            start[0] = (y, x)
            break
        i += 1

    start = start[0]

    options = find_options(start, inputs, 64)

    print(f"Part 1: {options}")

    size = len(inputs)
    edge = size // 2

    points = [find_options(start, inputs, edge + i * size) for i in range(3)]

    goal = 26501365
    num_boards = ((goal - edge) // size)
    a = (points[2] - (2 * points[1]) + points[0]) // 2
    b = points[1] - points[0] - a
    c = points[0]
    part2 = (a * num_boards ** 2) + (b * num_boards) + c

    print(f"Part 2: {part2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
