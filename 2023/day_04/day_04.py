# Day 4 of Advent of Code 2023
# <PUZZLE TITLE>

# <PUZZLE DESCRIPTION>

from aoc.helpers import *

if __name__ == "__main__":
    inputs = get_input("\n", example=False)

    points = 0

    card_amounts = [1 for i in range(len(inputs))]

    for i, line in enumerate(inputs):
        nums = line.split(':')[1].split('|')
        win_nums = re.findall(r"\d+", nums[0])
        card_nums = re.findall(r"\d+", nums[1])

        wins = sum(n in win_nums for n in card_nums)

        for j in range(wins):
            card_amounts[i + j + 1] += 1 * card_amounts[i]

        points += pow(2, wins - 1) if wins > 0 else 0

    print(f"Part 1: {points}")

    print(f"Part 2: {sum(card_amounts)}")