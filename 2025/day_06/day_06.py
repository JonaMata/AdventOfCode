# Day 6 of Advent of Code 2025
import operator
import timeit
from aoc.helpers import *

def process_input():
    vals = get_input("\n", example=False)
    return vals

def part1(vals):
    vals = [re.split(r" {1,}", x.strip()) for x in vals]
    vals[:-1] = [[int(y) for y in x] for x in vals[:-1]]
    total = 0
    for i in range(len(vals[0])):
        subtotal = vals[0][i]
        op = operator.add if vals[-1][i] == '+' else operator.mul
        for j in range(1,len(vals)-1):
            subtotal = op(subtotal, vals[j][i])
        total += subtotal
    star1 = total
    return star1

def part2(vals):
    ops = [(operator.add if x.strip() == '+' else operator.mul, len(x)) for x in re.findall(r"([+*] {1,})", re.sub(r" ([+*])", r"\1", vals[-1]))]
    nums = vals[:-1]

    total = 0
    for op in ops:
        subtotal = 0
        for i in range(op[1]):
            num = ''
            for j in range(len(nums)):
                num+=nums[j][0]
                nums[j] = nums[j][1:]
                if i == op[1]-1:
                    nums[j] = nums[j][1:]
            num = int(num)
            if subtotal == 0:
                subtotal = num
            else:
                subtotal = op[0](subtotal, num)
        total += subtotal
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
