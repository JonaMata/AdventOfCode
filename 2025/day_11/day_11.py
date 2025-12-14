# Day 11 of Advent of Code 2025
import timeit
from aoc.helpers import *

def process_input():
    vals = [x.split(': ') for x in get_input("\n", example=True)]
    devices = {x[0]: x[1].split(' ') for x in vals}
    return devices

def find_path(path, goal, devices, cache):
    if path[-1] in path[:-1]:
        return 0
    if path[-1] in cache:
        return cache[path[-1]]
    if path[-1] == goal:
        return 1
    if path[-1] == 'out':
        return 0

    new_paths = 0
    for device in devices[path[-1]]:
        new_path = path.copy()
        new_path.append(device)
        new_paths += find_path(new_path, goal, devices, cache)
    cache[path[-1]] = new_paths
    return new_paths

def part1(devices):
    cache = dict()
    paths = find_path(['you'], 'out', devices, cache)
    star1 = paths
    return star1


def part2(devices):
    start_dac = find_path(['svr'], 'dac', devices, dict())
    start_fft = find_path(['svr'], 'fft', devices, dict())
    dac_fft = find_path(['dac'], 'fft', devices, dict())
    fft_dac = find_path(['fft'], 'dac', devices, dict())
    dac_out = find_path(['dac'], 'out', devices, dict())
    fft_out = find_path(['fft'], 'out', devices, dict())
    star2 = start_dac*dac_fft*fft_out+start_fft*fft_dac*dac_out
    return star2


if __name__ == "__main__":
    start_total = timeit.default_timer()
    start_input = start_total
    inputs = process_input()
    print(f"Input processed, time taken: {(timeit.default_timer()-start_input)*1000:.2f}ms")
    start_part1 = timeit.default_timer()
    print(f"Part 1: {part1(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part1)*1000:.2f}ms")
    start_part2 = timeit.default_timer()
    print(f"Star 2: {part2(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part2)*1000:.2f}ms")

    print(f"\n Total time taken: {(timeit.default_timer()-start_total)*1000:.2f}ms")
