# Day 2 of Advent of Code 2023

from aoc.helpers import *
from functools import reduce

max_set = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def check_possible(game):
    for game_set in game[1]:
        for grab in game_set:
            if int(grab[0]) > max_set[grab[1]]:
                return False
    return True


def calc_power(game):
    maxes = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    for game_set in game[1]:
        for grab in game_set:
            maxes[grab[1]] = max(int(grab[0]), maxes[grab[1]])

    return reduce(lambda x, y: x * y, maxes.values())


if __name__ == "__main__":
    inputs = get_input("\n", example=False)
    lines = [(int(line.split(': ')[0].split(' ')[1]),
              [[grab.split(' ') for grab in game_set.split(', ')] for game_set in line.split(': ')[1].split('; ')]) for
             line in inputs]

    filtered_lines = filter(check_possible, lines)

    game_nums = (line[0] for line in filtered_lines)
    part1 = sum(game_nums)
    print('Part1: ' + str(part1))

    part2 = sum([calc_power(game) for game in lines])
    print('Part2: ' + str(part2))
