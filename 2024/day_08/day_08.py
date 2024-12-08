# Day 8 of Advent of Code 2024
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)

    antenna_sets = {}

    for y in range(len(inputs)):
        for x in range(len(inputs[0])):
            pos = inputs[y][x]
            if pos != ".":
                if pos not in antenna_sets:
                    antenna_sets[pos] = []
                antenna_sets[pos].append((x,y))

    antinodes = set()
    for antennas in antenna_sets.values():
        for i in range(len(antennas)):
            for j in range(i+1, len(antennas)):
                an1 = antennas[i]
                an2 = antennas[j]
                x_diff = an1[0] - an2[0]
                y_diff = an1[1] - an2[1]
                if x_diff % 3 == 0 and y_diff % 3 == 0:
                    antinodes.add((an1[0]-x_diff/3, an1[1]-y_diff/3))
                    antinodes.add((an2[0]+x_diff/3, an2[1]+y_diff/3))
                p1 = (an2[0]-x_diff, an2[1]-y_diff)
                if 0 <= p1[0] < len(inputs[0]) and 0 <= p1[1] < len(inputs):
                    antinodes.add(p1)
                p2 = (an1[0]+x_diff, an1[1]+y_diff)
                if 0 <= p2[0] < len(inputs[0]) and 0 <= p2[1] < len(inputs):
                    antinodes.add(p2)

    star1 = len(antinodes)
    print(f"Star 1: {star1}")


    lines = []
    for antennas in antenna_sets.values():
        for i in range(len(antennas)):
            for j in range(i+1, len(antennas)):
                an1 = antennas[i]
                an2 = antennas[j]
                x_diff = an1[0] - an2[0]
                y_diff = an1[1] - an2[1]
                slope = y_diff/x_diff
                start = an1[0]#an1[1] - (slope*an1[0])
                offset = an1[1]
                lines.append((y_diff/x_diff, start, offset))

    antinodes = set()
    for y in range(len(inputs)):
        for x in range(len(inputs[0])):
            for line in lines:
                if (x-line[1])*line[0] + line[2] == y:
                    antinodes.add((x, y))
                    break



    star2 = len(antinodes)
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
