# Day 9 of Advent of Code 2023
from aoc.helpers import *


def find_next_num(nums):
    if all([num == 0 for num in nums]):
        nums.append(0)
        return nums
    next_nums = find_next_num([nums[i+1] - nums[i] for i in range(len(nums)-1)])
    nums.append(nums[-1]+next_nums[-1])
    return nums


if __name__ == "__main__":
    inputs = get_input("\n", example=False)

    lines = [[int(m) for m in re.findall(r"-?\d+", l)] for l in inputs]

    print(f"Part 1: {sum([find_next_num(line)[-1] for line in lines])}")

    for line in lines:
        line.reverse()

    print(f"Part 2: {sum([find_next_num(line)[-1] for line in lines])}")
