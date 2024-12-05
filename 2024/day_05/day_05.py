# Day 5 of Advent of Code 2024
import timeit
from functools import reduce
from itertools import chain

from aoc.helpers import *

rules = {}

def main():
    inputs = get_input("\n\n", example=False)
    for rule in inputs[0].split("\n"):
        key, num = rule.split("|")
        if key not in rules:
            rules[key] = [num]
        else:
            rules[key].append(num)
    manuals = [line.split(",") for line in inputs[1].split("\n")]
    star1 = sum([check_manual(manual) for manual in manuals])
    print(f"Star 1: {star1}")

    wrong_manuals = filter(lambda x: check_manual(x) == 0, manuals)
    sum_pages = 0
    for manual in wrong_manuals:
        this_rules = {}
        for num in manual:
            if num in rules:
                this_rules[num] = rules[num]
        fixed_manual = []
        for i in range(len(manual)):
            for num in manual:
                if num not in chain.from_iterable(this_rules.values()):
                    fixed_manual.append(num)
                    manual.remove(num)
                    if num in this_rules:
                        del this_rules[num]
                    break
        sum_pages += int(fixed_manual[int((len(fixed_manual)+1)/2)-1])

    print(f"Star 2: {sum_pages}")

def check_manual(manual):
    seen = []
    for num in manual:
        if num in rules:
            for check_num in rules[num]:
                if check_num in seen:
                    return 0
        seen.append(num)
    return int(manual[int((len(manual)+1)/2)-1])

# 6604 -- Too high


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
