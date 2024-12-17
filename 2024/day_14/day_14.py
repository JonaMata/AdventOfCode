# Day 14 of Advent of Code 2024
import timeit
from copy import deepcopy
from functools import reduce

from aoc.helpers import *
import numpy as np


def main():
    inputs = get_input("\n", example=False)
    quadrants = [0,0,0,0]
    lines = [[int(num) for num in re.findall(r"-?\d+", line)] for line in inputs]
    size = 101, 103
    seconds = 100

    for line in lines:
        pos = np.array([line[0], line[1]]) + seconds * np.array([line[2], line[3]])
        pos[0] %= size[0]
        pos[1] %= size[1]
        quadrant = (1 if pos[0] > (size[0]-1)/2 else 0) + (2 if pos[1] > (size[1]-1)/2 else 0)
        if pos[0] != (size[0]-1)/2 and pos[1] != (size[1]-1)/2:
            quadrants[quadrant] += 1

    star1 = reduce(lambda a, b: a*b, quadrants)
    print(f"Star 1: {star1}")

    # 82531680 -- Too low

    seconds = 0
    empty_grid = [[' ' for x in range(size[0])] for y in range(size[1])]
    # while input(f"At {seconds} seconds. Is this a christmas tree?") != "y":
    #     seconds += 1
    #     grid = deepcopy(empty_grid)
    #     for line in lines:
    #         pos = np.array([line[0], line[1]]) + seconds * np.array([line[2], line[3]])
    #         pos[0] %= size[0]
    #         pos[1] %= size[1]
    #         grid[pos[1]][pos[0]] = 'X'
    #     for y in grid:
    #         print(str.join("", y))


    # x1 = 0
    # x2 = 0
    # form1 = lambda x: 27+101*x
    # form2 = lambda x: 85+13*x
    # while True:
    #     res1 = form1(x1)
    #     res2 = form2(x2)
    #     if res1 == res2:
    #         break
    #     if res1 > res2:
    #         x2 += 1
    #     else:
    #         x1 += 1

    lines = [[np.array([line[0], line[1]]), np.array([line[2],line[3]])] for line in lines]
    seconds = 0
    found = False
    while not found:
        seconds += 1
        # if seconds % 1000 == 0:
        #     print(f"Checking {seconds}")
        grid = np.zeros(size[::-1])
        quadrants = [0,0,0,0]
        for line in lines:
            line[0] += line[1]
            line[0][0] %= size[0]
            line[0][1] %= size[1]
            grid[line[0][1],line[0][0]] += 1

            # quadrant = (1 if line[0][0] > (size[0] - 1) / 2 else 0) + (2 if line[0][1] > (size[1] - 1) / 2 else 0)
            # if line[0][0] != (size[0] - 1) / 2 and line[0][1] != (size[1] - 1) / 2:
            #     quadrants[quadrant] += 1

        quadrants[0] = np.count_nonzero(grid[:int((size[1]-1)/2), :int((size[0]-1)/2)])
        quadrants[1] = np.count_nonzero(grid[:int((size[1]-1)/2), int((size[0]-1)/2+1):])
        quadrants[2] = np.count_nonzero(grid[int((size[1]-1)/2+1):, :int((size[0]-1)/2)])
        quadrants[2] = np.count_nonzero(grid[int((size[1]-1)/2+1):, int((size[0]-1)/2+1):])
        # if np.count_nonzero(np.equal(left_half, right_half)) > size[0]*size[1]*0.5:
        if max(quadrants) > len(lines)*.5:
            found = True
            break

    star2 = seconds
    print(f"Star 2: {star2}")

    # 27, 128, 229 vertical
    # 85, 188, 291 horizontal
    # 27+x1*101
    # 85+x2*103

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
