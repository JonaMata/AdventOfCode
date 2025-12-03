# Day 3 of Advent of Code 2025
import timeit
from aoc.helpers import *

def process_input():
    vals = get_input("\n", example=False)
    return vals

def part1(vals):
    total = 0
    for bank in vals:
        best = 0
        for i in range(len(bank)-1):
            for j in range(i+1, len(bank)):
                num = int(bank[i] + bank[j])
                best = max(best, num)
        total += best

    star1 = total
    return star1

def bank_to_joltage(part, bank):
    remaining = 12 - len(part)
    if remaining == 0:
        return int(part)
    max_index = 0
    for i in range(len(bank)-remaining+1):
        if bank[i] > bank[max_index]:
            max_index = i

    new_part = part + bank[max_index]
    new_bank = bank[max_index + 1:]
    return bank_to_joltage(new_part, new_bank)

def part2(vals):
    total = 0
    banks = 0
    for bank in vals:
        banks += 1
        total += bank_to_joltage('', bank)
    star2 = total
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
