# Day 22 of Advent of Code 2024
import functools
import math
import timeit
from aoc.helpers import *
from ctypes import CDLL, POINTER, c_int

def process_input():
    vals = [int(val) for val in get_input("\n", example=False)]

    efficient_code = CDLL("next_num.so")
    efficient_code.next_number.restype = POINTER(c_int)

    total = 0
    price_sets = []
    change_sets = []
    for val in vals:
        price = val % 10
        prices = []
        changes = []
        res = efficient_code.next_number(val, 2000)
        nums = res[:2000]
        efficient_code.free_memory(res)
        for num in nums:
            val = num
            next_price = val % 10
            prices.append(next_price)
            changes.append(next_price-price)
            price = next_price

        total += val
        price_sets.append(prices)
        change_sets.append(changes)
    return total, price_sets, change_sets

# mod = (1<<24)-1
# def next_number(num):
#     num = (num ^ (num<<6)) & mod
#     num = (num ^ (num>>5)) & mod
#     num = (num ^ (num<<11)) & mod
#     return num

def part1(vals):
    total, price_sets, change_sets = vals

    star1 = total
    return star1

def part2_faster(vals):
    total, price_sets, change_sets = vals
    change_price_dict = {}
    for i in range(len(price_sets)):
        happened = set()
        for j in range(len(price_sets[i])-3):
            change_set = tuple(change_sets[i][j:j+4])
            if change_set not in happened:
                if change_set not in change_price_dict:
                    change_price_dict[change_set] = price_sets[i][j+3]
                else:
                    change_price_dict[change_set] += price_sets[i][j+3]
                happened.add(change_set)

    return max(change_price_dict.values())

def part2(vals):
    total, price_sets, change_sets = vals
    change_strings = [str.join("", [('+' if change >= 0 else '')+str(change)+',' for change in changes]) for changes in change_sets]

    results = set()
    start = timeit.default_timer()
    total = len(price_sets)
    print(f"Checking {total} sets")
    checked = 0
    happened = set()
    for i in range(len(price_sets)):
        max_price = max(price_sets[i])
        indexes = list(filter(lambda x: price_sets[i][x] == max_price, range(3, len(price_sets[i]))))
        for index in indexes:
            res = 0
            change_string = change_strings[i][(index-3)*3:(index+1)*3]
            if change_string in happened:
                continue
            happened.add(change_string)
            for j in range(len(price_sets)):
                found = change_strings[j].find(change_string)
                if found >= 0:
                    found = found//3+3
                    if found < len(price_sets[j]):
                        res += price_sets[j][found]
            results.add(res)
        checked += 1
        now = timeit.default_timer()
        speed = (now-start)/checked
        left = speed * (total-checked)
        mins = left // 60
        secs = left % 60
        print(f"Finished {checked}/{len(price_sets)} ETA: {mins:.0f}m{secs:.0f}s left")

    return max(results)


if __name__ == "__main__":
    start_total = timeit.default_timer()
    start_input = start_total
    inputs = process_input()
    print(f"Input processed, time taken: {(timeit.default_timer()-start_input)*1000:.2f}ms")
    start_part1 = timeit.default_timer()
    print(f"Part 1: {part1(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part1)*1000:.2f}ms")
    start_part2 = timeit.default_timer()
    print(f"Star 2: {part2_faster(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part2)*1000:.2f}ms")

    print(f"\n Total time taken: {(timeit.default_timer()-start_total)*1000:.2f}ms")
