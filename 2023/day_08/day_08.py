# Day 8 of Advent of Code 2023
# <PUZZLE TITLE>
import math

# <PUZZLE DESCRIPTION>

from aoc.helpers import *


def find_exit(target='AAA', index=0, depth=0):
    if target == 'ZZZ':
        return depth
    return find_exit(mapp[target][instructions[index]], (index+1) % len(instructions), depth+1)


if __name__ == "__main__":
    inputs = get_input("\n\n", example=False)

    instructions = [1 if i == 'R' else 0 for i in inputs[0]]

    mapp = {l.split(' = ')[0]: l.split(' = ')[1][1:-1].split(', ') for l in inputs[1].splitlines()}

    target = 'AAA'
    index = 0
    depth = 0

    while target != 'ZZZ':
        target = mapp[target][instructions[index]]
        index = (index + 1) % len(instructions)
        depth += 1

    print(f"Part 1: {depth}")

    targets = [t for t in mapp.keys() if t[-1] == 'A']
    index = 0
    depth = 0

    first_end = [False for i in range(len(targets))]

    while not all(first_end):
        for i in range(len(targets)):
            if not first_end[i] and targets[i][-1] == 'Z':
                first_end[i] = depth
            targets[i] = mapp[targets[i]][instructions[index]]
        index = (index + 1) % len(instructions)
        depth += 1

    print(f"Part 2: {math.lcm(*first_end)}")
