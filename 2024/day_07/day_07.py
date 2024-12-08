# Day 7 of Advent of Code 2024
import operator
import timeit
from aoc.helpers import *

def concat(a, b):
    return int(f"{a}{b}")

def check_equation(equation, operators):
    result, nums = equation.split(": ")
    result = int(result)
    nums = [int(num) for num in nums.split(" ")]
    return check_equation_rec(result, nums, operators)


def check_equation_rec(result, nums, operators):
    results = []
    if nums[0] > result or sum(nums) > result:
        return 0
    for op in operators:
        new_nums = [ op(*nums[:2]), *nums[2:]]
        if len(new_nums)>1:
            results.append(check_equation_rec(result, new_nums, operators))
        else:
            results.append(result if result == new_nums[0] else 0)

    return max(results)


def main():
    inputs = get_input("\n", example=False)

    operators = [
        operator.add,
        operator.mul
    ]

    star1 = sum([check_equation(line, operators) for line in inputs])
    print(f"Star 1: {star1}")

    operators.append(concat)

    star2 = sum([check_equation(line, operators) for line in inputs])
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
