# Day 2 of Advent of Code 2025
import timeit
from aoc.helpers import *

def process_input():
    vals = get_input(",", example=False)
    vals = [[y for y in x.split('-')] for x in vals]
    return vals

def check_ids(part, left, right, length):
    remaining = length-len(part)
    if remaining == 0:
        return [part+part]
    ids = []
    for i in range(10):
        new_part = part+str(i)
        test_low_part = new_part+'0'*(remaining-1)
        test_low = int(test_low_part+test_low_part)
        test_high_part = new_part+'9'*(remaining-1)
        test_high = int(test_high_part+test_high_part)
        if test_low <= int(right) and test_high >= int(left):
            ids.extend(check_ids(new_part, left, right, length))
    return ids

def part1(vals):
    invalid_ids = []
    for num_range in vals:
        left_len = len(num_range[0])
        right_len = len(num_range[1])
        left = num_range[0]
        right = num_range[1]
        for i in range(left_len, right_len+1):
            if i%2 != 0:
                continue
            length = i//2
            invalid_ids.extend(check_ids('', left, right, length))
    id_sum = sum([int(x) for x in set(invalid_ids) if x[0] != '0'])
    star1 = id_sum
    return star1

def check_ids_new(part, left, right, length, mult):
    remaining = length-len(part)
    if remaining == 0:
        return [part*mult]
    ids = []
    for i in range(10):
        new_part = part+str(i)
        test_low_part = new_part+'0'*(remaining-1)
        test_low = int(test_low_part*mult)
        test_high_part = new_part+'9'*(remaining-1)
        test_high = int(test_high_part*mult)
        if test_low <= int(right) and test_high >= int(left):
            ids.extend(check_ids_new(new_part, left, right, length, mult))
    return ids

def part2(vals):
    invalid_ids = []
    for num_range in vals:
        left_len = len(num_range[0])
        right_len = len(num_range[1])
        left = num_range[0]
        right = num_range[1]
        for i in range(left_len, right_len+1):
            for length in range(1,i):
                if i%length == 0:
                    mult = i//length
                    invalid_ids.extend(check_ids_new('', left, right, length, mult))
    id_sum = sum([int(x) for x in set(invalid_ids) if x[0] != '0'])
    star1 = id_sum
    return star1

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
