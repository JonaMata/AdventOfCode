# Day 1 of Advent of Code 2023

from aoc.helpers import *

words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def find_nums(line):
    with_words = [(line.find(word), index+1) for index, word in enumerate(words) if line.find(word) >= 0]
    with_nums = [(line.find(str(num)), num) for num in range(1,10) if line.find(str(num)) >= 0]
    with_all = with_words+with_nums
    with_all.sort(key=lambda x: x[0])
    first = with_all[0][1]

    line = line[::-1]
    with_words = [(line.find(word[::-1]), index+1) for index, word in enumerate(words) if line.find(word[::-1]) >= 0]
    with_nums = [(line.find(str(num)), num) for num in range(1,10) if line.find(str(num)) >= 0]
    with_all = with_words+with_nums
    with_all.sort(key=lambda x: x[0])
    second = with_all[0][1]
    return first*10+second


if __name__ == "__main__":
    inputs = get_input('\n', example=False)

    nums_only = [list(filter(lambda x: x.isdigit(), line)) for line in inputs]
    part1 = sum([int(line[0] + line[-1]) for line in nums_only])
    print('Part 1: ' + str(part1))

    part2 = sum([find_nums(line) for line in inputs])
    print('Part2: ' + str(part2))