# Day 3 of Advent of Code 2023

from aoc.helpers import *


def check_valid(n):
    indexes = [(n[0], n[1][0]-1), (n[0], n[1][1])]
    for i in range(-1, len(n[2])+1):
        indexes.extend([(n[0]+1, n[1][0]+i), (n[0]-1, n[1][0]+i)])

    for index in indexes:
        if 0 <= index[0] < len(inputs) and 0 <= index[1] < len(inputs[index[0]]):
            char = inputs[index[0]][index[1]]
            if char == '*':
                if not index in gears:
                    gears[index] = set()
                gears[index].add(n)

            if char != '.':
                return True

    return False


if __name__ == "__main__":
    inputs = get_input("\n", example=False)

    numbers = []
    gears = dict()

    for y, line in enumerate(inputs):
        results = re.finditer(r"\d+", line)
        for m in results:
            numbers.append((y, m.span(), m[0]))

    numbers = filter(check_valid, numbers)

    part1 = sum([int(n[2]) for n in numbers])

    print(f"Part 1: {part1}")
    gear_ratios = [int(list(g)[0][2]) * int(list(g)[1][2]) for g in gears.values() if len(g) == 2]

    part2 = sum(gear_ratios)

    print(f"Part 2: {part2}")