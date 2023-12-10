# Day 10 of Advent of Code 2023
import timeit

from aoc.helpers import *

mapp = {
    '|': ((1,0), (-1,0)),
    '-': ((0,1), (0,-1)),
    'L': ((-1,0), (0,1)),
    'J': ((-1,0), (0,-1)),
    '7': ((1,0), (0,-1)),
    'F': ((1,0), (0,1)),
}


def find_neighbours(loc, lines):
    return [(loc[0]+n[0], loc[1]+n[1]) for n in mapp[lines[loc[0]][loc[1]]]]


def find_first_steps(start, lines):
    neighbours = []
    neighbours_delta = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if abs(x+y) == 1:
                loc = (start[0]+y, start[1]+x)
                if 0 <= loc[0] < len(lines) and 0 <= loc[1] < len(lines[loc[0]]):
                    if lines[loc[0]][loc[1]] in mapp:
                        if start in find_neighbours(loc, lines):
                            neighbours.append(loc)
                            neighbours_delta.append((y, x))

    neighbours_hashed = tuple(sorted(neighbours_delta))
    for pipe, item in mapp.items():
        if tuple(sorted(item)) == neighbours_hashed:
            lines[start[0]][start[1]] = pipe

    return neighbours


def main():
    inputs = get_input("\n", example=False)

    lines = [[x for x in l] for l in inputs]
    start = None
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == 'S':
                start = (y, x)
                break
        if start:
            break

    prev_index = [start, start]
    index = find_first_steps(start, lines)
    steps = 1
    loop_indexes = {start, index[0], index[1]}

    while index[0] != index[1]:
        for i in range(len(index)):
            neighbours = find_neighbours(index[i], lines)
            next_index = list(filter(lambda n: n != prev_index[i], neighbours))[0]
            prev_index[i] = index[i]
            index[i] = next_index
            loop_indexes.add(next_index)
        steps += 1

    print(f"Part 1: {steps}")

    vertical_parts = ['|']
    up_parts = ['J', 'L']
    down_parts = ['7', 'F']

    inner_parts = 0
    for y in range(len(lines)):
        out = True
        in_pipe = False
        last_dir = None
        for x in range(len(lines[y])):
            if (y, x) in loop_indexes:
                pipe = lines[y][x]
                if pipe in vertical_parts:
                    out = not out
                elif pipe in up_parts:
                    in_pipe = not in_pipe
                    if not in_pipe and last_dir == 'down':
                        out = not out
                    last_dir = 'up'
                elif pipe in down_parts:
                    in_pipe = not in_pipe
                    if not in_pipe and last_dir == 'up':
                        out = not out
                    last_dir = 'down'
            elif not out:
                inner_parts += 1

    print(f"Part 2: {inner_parts}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
