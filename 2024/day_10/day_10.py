# Day 10 of Advent of Code 2024
import timeit
from aoc.helpers import *
def get_neighbours(trailmap, pos):
    neighbours = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
    return filter(lambda x: 0 <= x[0] < len(trailmap) and 0 <= x[1] < len(trailmap[0]), neighbours)

def find_trails_rec(trailmap, pos, distinct = True):
    if trailmap[pos[0]][pos[1]] == 9:
        return {pos} if distinct else [pos]
    trails = set() if distinct else []
    for neighbour in get_neighbours(trailmap, pos):
        if trailmap[neighbour[0]][neighbour[1]] - 1 == trailmap[pos[0]][pos[1]]:
            for trail in find_trails_rec(trailmap, neighbour, distinct):
                trails.add(trail) if distinct else trails.append(trail)
    return trails


def find_trails(trailmap, distinct = True):
    trails = 0
    for x in range(len(trailmap)):
        for y in range(len(trailmap[0])):
            if trailmap[x][y] == 0:
                trails += len(find_trails_rec(trailmap, (x, y), distinct))
    return trails

def main():
    inputs = get_input("\n", example=False)
    trailmap = [[int(num) for num in line] for line in inputs]

    trails = find_trails(trailmap)

    star1 = trails
    print(f"Star 1: {star1}")

    trails = find_trails(trailmap, False)

    star2 = trails
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
