# Day 3 of Advent of Code 2015
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("", example=False)
    visited = {(0,0)}
    x = 0
    y = 0
    for i in inputs:
        if i == '^':
            y -= 1
        elif i == 'v':
            y += 1
        elif i == '<':
            x -= 1
        else:
            x += 1
        visited.add((x,y))

    print(f"Part1: {len(visited)}")


    visited = {(0,0)}
    x = [0, 0]
    y = [0, 0]
    for i, j in enumerate(inputs):
        if j == '^':
            y[i%2] -= 1
        elif j == 'v':
            y[i%2] += 1
        elif j == '<':
            x[i%2] -= 1
        else:
            x[i%2] += 1
        visited.add((x[i%2],y[i%2]))

    print(f"Part2: {len(visited)}")



if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
