# Day 12 of Advent of Code 2015
import json
import timeit
from aoc.helpers import *


def main():
    inputs = get_input(example=False)
    star1 = sum([int(num) for num in re.findall(r"-?\d+", inputs)])
    print(f"Star 1: {star1}")

    obj = json.loads(inputs)
    star2 = sum_no_red(obj)
    print(f"Star 2: {star2}")

    # 38885 -- Too low


def sum_no_red(obj):
    if isinstance(obj, dict):
        obj = obj.values()
        if 'red' in obj:
            return 0
    res =  sum([x if isinstance(x, int) else 0 if isinstance(x, str) else sum_no_red(x) for x in obj])
    return res




if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
