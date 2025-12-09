# Day 9 of Advent of Code 2025
import timeit
from aoc.helpers import *

def process_input():
    vals = get_input("\n", example=False)
    vals = [list(map(int, x.split(','))) for x in vals]
    return vals

def part1(vals):
    biggest = 0
    for i in range(len(vals)):
        for j in range(i+1, len(vals)):
            cur = (abs(vals[j][0]-vals[i][0])+1)*(abs(vals[j][1]-vals[i][1])+1)
            biggest = max(biggest, cur)
    star1 = biggest
    return star1


def part2(vals):
    biggest = 0
    # best = None
    sides = []
    for i in range(len(vals)):
        j = i+1
        if j == len(vals):
            j = 0
        sides.append(((vals[i][0], vals[i][1]), (vals[j][0], vals[j][1])))

    recs = []
    for i in range(len(vals)):
        for j in range(i+1, len(vals)):
            cur = (abs(vals[j][0]-vals[i][0])+1)*(abs(vals[j][1]-vals[i][1])+1)
            recs.append((cur, (i,j)))
    recs.sort(reverse=True)

    for rec in recs:
        i, j = rec[1]
        rec_sides = [
            ((vals[i][0], vals[i][1]), (vals[i][0], vals[j][1])),
            ((vals[i][0], vals[i][1]), (vals[j][0], vals[i][1])),
            ((vals[j][0], vals[j][1]), (vals[i][0], vals[j][1])),
            ((vals[j][0], vals[j][1]), (vals[j][0], vals[i][1])),
        ]
        intersected = False
        for rec_side in rec_sides:
            rec_side_left = min(rec_side[0][0], rec_side[1][0])
            rec_side_right = max(rec_side[0][0], rec_side[1][0])
            rec_side_top = min(rec_side[0][1], rec_side[1][1])
            rec_side_bottom = max(rec_side[0][1], rec_side[1][1])
            for side in sides:
                side_left = min(side[0][0], side[1][0])
                side_right = max(side[0][0], side[1][0])
                side_top = min(side[0][1], side[1][1])
                side_bottom = max(side[0][1], side[1][1])

                if side_left == side_right and rec_side_top == rec_side_bottom:
                    if rec_side_left < side_left < rec_side_right and side_top <= rec_side_top <= side_bottom:
                        intersected = True
                        break

                if side_top == side_bottom and rec_side_left == rec_side_right:
                    if rec_side_top < side_top < rec_side_bottom and side_left <= rec_side_left <= side_right:
                        intersected = True
                        break

            if intersected:
                break
        if intersected:
            continue
        biggest = rec[0]
        break

    star2 = biggest
    return star2



if __name__ == "__main__":
    start_total = timeit.default_timer()
    start_input = start_total
    inputs = process_input()
    print(f"Input processed, time taken: {(timeit.default_timer()-start_input)*1000:.2f}ms")
    start_part1 = timeit.default_timer()
    print(f"Part 1: {part1(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part1)*1000:.2f}ms")
    start_part2 = timeit.default_timer()
    print(f"Star 2: {part2(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part2)*1000:.2f}ms")

    print(f"\n Total time taken: {(timeit.default_timer()-start_total)*1000:.2f}ms")
