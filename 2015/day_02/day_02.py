# Day 2 of Advent of Code 2015
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)
    packages = [sorted(map(lambda x: int(x), input_.split("x"))) for input_ in inputs]
    total_wrapping_paper = 0
    for package in packages:
        l, w, h = package
        total_wrapping_paper += 2*l*w + 2*w*h + 2*h*l + l*w
    print(f"Part 1: {total_wrapping_paper}")

    ribbon = 0
    for package in packages:
        l, w, h = package
        ribbon += 2*l + 2*w + l*w*h
    print(f"Part 2: {ribbon}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
