# Day 8 of Advent of Code 2025
import math
import timeit
from aoc.helpers import *

def process_input():
    vals = get_input("\n", example=False)
    nodes = [tuple(map(int, x.split(','))) for x in vals]

    circuits = []
    for node in nodes:
        circuits.append([node])
    dist_sets = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            dist = math.sqrt((nodes[i][0] - nodes[j][0])**2 + (nodes[i][1] - nodes[j][1])**2 + (nodes[i][2] - nodes[j][2])**2)
            dist_sets.append((dist, (i, j)))
    dist_sets.sort()
    return nodes, circuits, dist_sets

def connect_circuits(circuits, node_1, node_2):
    circ_1 = None
    circ_2 = None
    for circuit in circuits:
        if node_1 in circuit:
            circ_1 = circuit
        if node_2 in circuit:
            circ_2 = circuit
        if circ_1 is not None and circ_2 is not None:
            break
    if circ_1 is not circ_2:
        circuits.remove(circ_1)
        circuits.remove(circ_2)
        circuits.append(circ_1 + circ_2)

def part1(vals):
    nodes, circuits, dist_sets = vals
    for i in range (1000):
        x, y = dist_sets[i][1]
        connect_circuits(circuits, nodes[x], nodes[y])
    star1 = math.prod(sorted(list(map(len, circuits)), reverse=True)[:3])
    return star1

def part2(vals):
    nodes, circuits, dist_sets = vals
    last_set = None
    for i in range(len(dist_sets)):
        x, y = dist_sets[i][1]
        connect_circuits(circuits, nodes[x], nodes[y])
        if len(circuits) == 1:
            last_set = (x,y)
            break
    star2 = nodes[last_set[0]][0]*nodes[last_set[1]][0]
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
