# Day 12 of Advent of Code 2025
import timeit
from aoc.helpers import *

def process_input():
    vals = get_input("\n", example=False)
    presents = []
    for i in range(6):
        present = vals[i*5+1:i*5+4]
        size = sum(map(lambda x: x.count('#'), present))
        presents.append((present, size))
    regions = []
    for region in vals[30:]:
        size, pres = region.split(': ')
        size = [int(x) for x in size.split('x')]
        pres = [int(x) for x in pres.split(' ')]
        regions.append((size, pres))
    return presents, regions

def part1(vals):
    presents, regions = vals
    oversized = 0
    easy_fit = 0
    for region in regions:
        pres_size = 0
        for i in range(6):
            pres_size += presents[i][1] * region[1][i]
        if pres_size > region[0][0]*region[0][1]:
            oversized += 1
            continue
        full_pres = (region[0][0] // 3) * (region[0][1] // 3)
        total_pres = sum(region[1])
        if total_pres <= full_pres:
            easy_fit += 1
            continue
    # print(oversized)
    # print(easy_fit)
    # print(len(regions))
    # print(easy_fit+oversized)
    star1 = easy_fit
    return star1

def part2(vals):
    star2 = None
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
