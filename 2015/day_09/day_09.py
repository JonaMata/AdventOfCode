# Day 9 of Advent of Code 2015
import math
import timeit
from aoc.helpers import *


def rec_find_shortest(dist, city, cities, distances):
    if len(cities) == 0:
        return dist
    distance = []
    for i in range(len(cities)):
        if city in distances and cities[i] in distances[city]:
            distance.append(rec_find_shortest(dist+distances[city][cities[i]], cities[i], cities[:i]+cities[i+1:], distances))
    if len(distance) == 0:
        return math.inf
    return min(distance)


def find_shortest(cities, distances):
    distance = min([rec_find_shortest(0, cities[i], cities[:i]+cities[i+1:], distances) for i in range(len(cities))])
    return distance


def rec_find_longest(dist, city, cities, distances):
    if len(cities) == 0:
        return dist
    distance = []
    for i in range(len(cities)):
        if city in distances and cities[i] in distances[city]:
            distance.append(rec_find_longest(dist+distances[city][cities[i]], cities[i], cities[:i]+cities[i+1:], distances))
    if len(distance) == 0:
        return 0
    return max(distance)


def find_longest(cities, distances):
    distance = max([rec_find_longest(0, cities[i], cities[:i]+cities[i+1:], distances) for i in range(len(cities))])
    return distance


def main():
    inputs = get_input("\n", example=False)
    distances = dict()
    cities = set()
    for route in inputs:
        x = route.split(' = ')
        src, dest, distance = (*x[0].split(' to '), int(x[1]))
        cities.add(src)
        cities.add(dest)
        if src not in distances:
            distances[src] = dict()
        if dest not in distances:
            distances[dest] = dict()
        distances[src][dest] = distance
        distances[dest][src] = distance

    shortest_distance = find_shortest(list(cities), distances)

    print(f"Part1: {shortest_distance}")

    longest_distance = find_longest(list(cities), distances)

    print(f"Part2: {longest_distance}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
