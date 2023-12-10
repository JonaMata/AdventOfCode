# Day 6 of Advent of Code 2023
import math

from aoc.helpers import *


def calculate_race(time, dist):
    b = time
    c = -dist
    max_val = math.floor((b + math.sqrt(b ** 2 + 4 * c)) / 2)
    max_dist = (times[i] - max_val) * max_val
    if max_dist == -c: max_val -= 1
    min_val = math.ceil((b - math.sqrt(b ** 2 + 4 * c)) / 2)
    min_dist = (times[i] - min_val) * min_val
    if min_dist == -c: min_val += 1
    return max_val - min_val + 1


if __name__ == "__main__":
    inputs = get_input("\n", example=False)

    times = [int(n) for n in re.findall(r"\d+", inputs[0])]
    distances = [int(n) for n in re.findall(r"\d+", inputs[1])]

    part1 = 1

    for i in range(len(times)):
        pos = calculate_race(times[i], distances[i])
        part1 *= pos

    print(f"Part 1: {part1}")

    time = int(''.join(re.findall(r"\d+", inputs[0])))
    dist = int(''.join(re.findall(r"\d+", inputs[1])))

    print(f"Part 2: {calculate_race(time, dist)}")
