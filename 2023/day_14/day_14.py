# Day 14 of Advent of Code 2023
import copy
import timeit
from aoc.helpers import *


def calc_weight(arr):
    last_square = -1
    last_rock = -1
    weight = 0
    for i, rock in enumerate(arr):
        if rock == '#':
            last_rock = i
        elif rock == 'O':
            new_spot = max(last_square, last_rock)+1
            weight += len(arr)-new_spot
            last_rock = new_spot
    return weight

def calc_weight_state(grid):
    weight = 0
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] == 'O':
                weight += len(grid)-y
    return weight


def move(grid, dir):
    i_len = len(grid) if dir[1] != 0 else len(grid[0])
    j_len = len(grid) if dir[0] != 0 else len(grid[0])
    reverse = sum(dir) > 0
    for i in range(i_len):
    # for i in range(0):
        last_square = -1 if not reverse else j_len
        last_rock = -1 if not reverse else j_len
        for j in (range(j_len) if not reverse else reversed(range(j_len))):
            # print(f"Dir: {dir}, i,j: {i},{j}, Coords: {(i,j) if dir[1] != 0 else (j,i)}")
            rock = grid[i][j] if dir[1] != 0 else grid[j][i]
            if rock == '#':
                # print(f"Found square at {j}")
                last_square = j
            elif rock == 'O':
                if not reverse:
                    new_spot = max(last_square, last_rock) + 1
                else:
                    new_spot = min(last_square, last_rock) - 1
                # print(f"Found round at {j}, move to {new_spot}")
                if dir[1] != 0:
                    grid[i][j] = '.'
                    grid[i][new_spot] = 'O'
                else:
                    grid[j][i] = '.'
                    grid[new_spot][i] = 'O'
                last_rock = new_spot
                # print_2d(grid)


def cycle(grid):
    grid = copy.deepcopy(grid)
    move(grid, (-1, 0))
    move(grid, (0, -1))
    move(grid, (1, 0))
    move(grid, (0, 1))
    return grid


def main():
    inputs = get_input("\n", example=False)
    ver = [[y[x] for y in inputs] for x in range(len(inputs[0]))]
    part1 = sum([calc_weight(x) for x in ver])

    print(f"Part1: {part1}")

    grid = [[x for x in line] for line in inputs]
    known_states = dict()
    tot = 1000000000
    for i in range(tot):
        new_grid = cycle(grid)
        grid = new_grid
        hashable = tuple([tuple(x) for x in new_grid])
        if hashable in known_states:
            index = known_states[hashable]
            if (tot-index-1) % (i-index) == 0:
                grid = new_grid
                break
        else:
            known_states[hashable] = i
    print(f"Part2: {calc_weight_state(grid)}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
