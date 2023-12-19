# Day 18 of Advent of Code 2023
import timeit
from functools import reduce

import numpy as np

from aoc.helpers import *


def get_neighbours(node):
    dirs = ((0,1), (1,0), (-1,0), (0,-1))
    neighbours = []
    for direction in dirs:
        neighbours.append((node[0]+direction[0], node[1]+direction[1]))
    return neighbours


def shoelace(points):
    points = np.array(points)
    print(points)
    i = np.arange(len(points))
    return np.abs(np.sum(points[i - 1, 0] * points[i, 1] - points[i, 0] * points[i - 1, 1]) * 0.5)


def main():
    inputs = get_input("\n", example=False)
    instructions = [line.split(' ') for line in inputs]

    current = (0, 0)
    holes = {current}

    dir_map = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1),
    }

    for direction, length, colour in instructions:
        for i in range(int(length)):
            new = (current[0]+dir_map[direction][0], current[1]+dir_map[direction][1])
            holes.add(new)
            current = new

    ver_sort = sorted(holes, key=lambda x: x[0])
    ver_range = (ver_sort[0][0], ver_sort[-1][0])
    hor_sort = sorted(holes, key=lambda x: x[1])
    hor_range = (hor_sort[0][1], hor_sort[-1][1])

    wall = False
    start = (ver_range[0], hor_range[0])

    while True:
        if start in holes:
            wall = True
        elif wall:
            break
        start = (start[0]+1, start[1]+1)

    fill = [start]

    while len(fill) > 0:
        node = fill.pop(0)
        if node not in holes:
            holes.add(node)
            for neighbour in get_neighbours(node):
                if neighbour not in holes:
                    fill.append(neighbour)

    print(f"Part1: {len(holes)}")

    current = (0, 0)
    points = [current]

    dir_map = {
        '3': (-1, 0),
        '1': (1, 0),
        '2': (0, -1),
        '0': (0, 1),
    }

    for inst in instructions:
        length = int(inst[2][2:7], 16)
        direction = inst[2][7]
        new = (current[0] + length*dir_map[direction][0], current[1] + length*dir_map[direction][1])
        points.append(new)
        current = new

    area = shoelace(points)

    print(points)
    perimeter = sum([abs(points[i][0]-points[i+1][0]) + abs(points[i][1]-points[i+1][1]) for i in range(len(points)-1)])

    print(f"{area=}, {perimeter=}")

    print(f"Part2: {area+.5*perimeter+1}")



if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
