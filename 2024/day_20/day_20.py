# Day 20 of Advent of Code 2024
import bisect
import timeit
from multiprocessing import Pool

from aoc.helpers import *

def get_neighbours(spot):
    return [
        (spot[0], spot[1]+1),
        (spot[0], spot[1]-1),
        (spot[0]+1, spot[1]),
        (spot[0]-1, spot[1])
    ]

def get_cheat_neighbours_after(spot):
    return [
        ((spot[0], spot[1]+1), (spot[0], spot[1]+2)),
        ((spot[0]+1, spot[1]), (spot[0]+2, spot[1])),
    ]

def get_cheats(spots, size):
    cheats = []
    for y in range(size[1]):
        for x in range(size[0]):
            if (x, y) not in spots:
                continue
            for cheat_neighbour in get_cheat_neighbours_after((x, y)):
                if cheat_neighbour[1] in spots and cheat_neighbour[0] not in spots:
                    cheat_val = abs(spots[(x, y)]-spots[cheat_neighbour[1][0], cheat_neighbour[1][1]])-2
                    cheats.append(cheat_val)

    return cheats

def find_cheats_from_spot(spot, spots, size, time_left, visited):
    if time_left == 0:
        return set()
    visited.append(spot)
    res = set()
    for neighbour in get_neighbours(spot):
        if not (0 <= neighbour[0] < size[0] and 0 <= neighbour[1] < size[1]):
            continue
        if neighbour in spots:
            res.add((neighbour, time_left))
            continue
        if neighbour not in visited:
            res.update(find_cheats_from_spot(neighbour, spots, size, time_left-1, visited.copy()))

    return res

def get_cheats_for_spot(inp):
    spot, spots = inp
    cheats = []
    for x_diff in range(-20, 21):
        for y_diff in range(-20, 21):
            time = abs(x_diff) + abs(y_diff)
            if time == 0 or time > 20:
                continue
            x, y = spot[0] + x_diff, spot[1] + y_diff
            if (x, y) in spots:
                val = spots[(x, y)] - spots[spot] - time
                if val > 0:
                    cheats.append(val)
    return cheats

def get_cheats_extended(spots):
    cheats = []
    search_spots = sorted(spots.keys(), key=lambda x: spots[x])
    with Pool(10) as p:
        for cheat_set in p.map(get_cheats_for_spot, [(spot, spots) for spot in search_spots]):
            cheats.extend(cheat_set)

    return cheats


def process_input():
    vals = get_input("\n", example=False)
    start = None
    end = None
    spot_pos = set()
    for y in range(len(vals)):
        for x in range(len(vals[0])):
            match vals[y][x]:
                case "S":
                    start = (x, y)
                case "E":
                    spot_pos.add((x, y))
                    end = (x, y)
                case ".":
                    spot_pos.add((x, y))

    cur = start
    spots = {start: 0}
    while True:
        if cur == end:
            break
        for neighbour in get_neighbours(cur):
            if neighbour in spot_pos and neighbour not in spots:
                spots[neighbour] = spots[cur]+1
                cur = neighbour
                break

    return start, end, spots, (len(vals[0]), len(vals))


def part1(vals):
    start, end, spots, size = vals
    cheats = get_cheats(spots, size)
    star1 = len(list(filter(lambda x: x >= 100, cheats)))
    return star1


def part2(vals):
    start, end, spots, size = vals
    cheats = get_cheats_extended(spots)
    star2 = len(list(filter(lambda x: x >= 100, cheats)))
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
