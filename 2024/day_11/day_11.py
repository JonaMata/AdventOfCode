# Day 11 of Advent of Code 2024
import timeit
from aoc.helpers import *

memory = dict()

def do_blinks(stones, blinks):
    return sum([blink_rec(stone, blinks) for stone in stones])

def blink_rec(stone, blinks_left):
    if blinks_left == 0:
        return 1
    if (stone, blinks_left) in memory:
        return memory[(stone, blinks_left)]
    if stone == 0:
        res = blink_rec(1, blinks_left-1)
    elif len(str(stone)) % 2 == 0:
        stone_string = str(stone)
        split = int(len(stone_string)/2)
        res = sum([blink_rec(int(stone_string[:split]), blinks_left-1), blink_rec(int(stone_string[split:]), blinks_left-1)])
    else:
        res = blink_rec(stone*2024, blinks_left-1)
    memory[(stone, blinks_left)] = res
    return res

def main():
    inputs = get_input(" ", example=False)
    stones = [int(num) for num in inputs]

    star1 = do_blinks(stones, 25)
    print(f"Star 1: {star1}")


    star2 = do_blinks(stones, 75)
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
