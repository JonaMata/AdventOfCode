# Day 15 of Advent of Code 2023
import re
import timeit
from aoc.helpers import *


def hash_str(inst):
    result = 0
    for x in inst:
        result += ord(x)
        result *= 17
        result = result % 256
    return result


def main():
    inputs = get_input(",", example=False)
    part1 = sum([hash_str(x) for x in inputs])

    print(f"Part1: {part1}")

    boxes = [[] for _ in range(256)]

    for inst in inputs:
        split = re.split(r"[-=]", inst)
        label = split[0]
        box_num = hash_str(label)
        box = boxes[box_num]
        if '-' in inst:
            for lens in box:
                if lens[0] == label:
                    box.remove(lens)
                    break
        if '=' in inst:
            lens_f = int(split[1])
            replaced = False
            for lens in box:
                if lens[0] == label:
                    lens[1] = lens_f
                    replaced = True
                    break
            if not replaced:
                box.append([label, lens_f])

    power = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            power += (i+1) * (j+1) * lens[1]

    print(f"Part2: {power}")




if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
