# Day 13 of Advent of Code 2023
import timeit
from aoc.helpers import *


def calc_before_mirror(arr):
    arr_len = len(arr)
    for i in range(1, arr_len):
        left = arr[max(0, i*2-arr_len):i]
        right = arr[i:min(arr_len, 2*i)]
        if left == right[::-1]:
            return i
    return 0


def could_have_smudge(left, right):
    differences = 0
    for i in range(len(left)):
        if left[i] != right[i]:
            differences += 1
            if differences > 1:
                return False
    return differences == 1


def calc_smudged_mirror(arr):
    arr_len = len(arr)

    for i in range(1, arr_len):
        left = arr[max(0, i*2-arr_len):i]
        right = arr[i:min(arr_len, 2*i)]
        right = right[::-1]

        smudged = []
        equal = []
        for j in range(len(left)):
            if left[j] != right[j]:
                if could_have_smudge(left[j], right[j]):
                    smudged.append(j)
            else:
                equal.append(j)
        if len(smudged) == 1 and len(equal) + len(smudged) == len(left):
            return i
    return 0


def main():
    inputs = get_input("\n\n", example=False)
    part1 = 0
    for grid in inputs:
        hor = grid.splitlines()
        ver = [''.join(y[x] for y in hor) for x in range(len(hor[0]))]
        hor_num = calc_before_mirror(hor)
        ver_num = calc_before_mirror(ver)

        part1 += ver_num + 100 * hor_num

    print(f"Part 1: {part1}")

    part2 = 0
    for grid in inputs:
        hor = grid.splitlines()
        ver = [''.join(y[x] for y in hor) for x in range(len(hor[0]))]
        hor_num = calc_smudged_mirror(hor)
        ver_num = calc_smudged_mirror(ver)
        part2 += ver_num + 100 * hor_num

    print(f"Part 2: {part2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
