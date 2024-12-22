# Day 22 of Advent of Code 2024
import functools
import math
import timeit
from aoc.helpers import *

def process_input():
    vals = [int(val) for val in get_input("\n", example=True)]
    return vals

@functools.cache
def next_number(num):
    num = (num ^ (num*64)) % 16777216
    num = (num ^ (num//32)) % 16777216
    num = (num ^ (num*2048)) % 16777216
    return num

def part1(vals):
    total = 0
    for val in vals:
        for i in range(2000):
            val = next_number(val)
        total += val

    star1 = total
    return star1

def part2(vals):
    price_sets = []
    change_sets = []
    for val in vals:
        price = val % 10
        prices = []
        changes = []
        for i in range(2000):
            val = next_number(val)
            next_price = val % 10
            prices.append(next_price)
            changes.append(next_price-price)
            price = next_price
        price_sets.append(prices)
        change_sets.append(changes)

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
    print(f"Star 2: {part2(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part2)*1000:.2f}ms")

    print(f"\n Total time taken: {(timeit.default_timer()-start_total)*1000:.2f}ms")
