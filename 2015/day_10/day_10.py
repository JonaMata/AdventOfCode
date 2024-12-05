# Day 10 of Advent of Code 2015
import re
import timeit
from itertools import groupby

from aoc.helpers import *


def say_say(say):
    seqs = [''.join(k) for _, k in groupby(say)]
    return ''.join([str(len(seq)) + seq[0] for seq in seqs])

def main():
    inputs = get_input(None, example=False)
    say = inputs.read()
    for i in range(40):
        say = say_say(say)

    print(f"Part 1: {len(say)}")

    for i in range(10):
        say = say_say(say)

    print(f"Part 2: {len(say)}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
