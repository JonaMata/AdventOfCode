# Day 23 of Advent of Code 2024
import timeit
from aoc.helpers import *

def process_input():
    vals = [val.split("-") for val in get_input("\n", example=False)]
    edges = {}
    for val in vals:
        edges.setdefault(val[0], set())
        edges.setdefault(val[1], set())
        edges[val[0]].add(val[1])
        edges[val[1]].add(val[0])

    return edges

def part1(vals):
    edges = vals
    threes = set()
    for edge in edges.keys():
        if edge[0] != 't':
            continue
        for x in edges[edge]:
            intersection = edges[edge].intersection(edges[x])
            for node in intersection:
                threes.add(tuple(sorted([edge, x, node])))
    star1 = len(threes)
    return star1

def part2(vals):
    edges = vals
    found = set()
    visited = set()
    for edge in edges.keys():
        for x in edges[edge]:
            sorted_edge = tuple(sorted([edge, x]))
            if sorted_edge in visited:
                continue
            visited.add(sorted_edge)
            intersection = edges[edge].intersection(edges[x])
            clique = {edge, x}
            stop = False
            for node in intersection:
                if all([y in edges[node] for y in clique]):
                    sorted_edges = [tuple(sorted([edge, node])), tuple(sorted([x, node]))]
                    if any([i in visited for i in sorted_edges]):
                        stop = True
                        break
                    visited.update(sorted_edges)
                    clique.add(node)
            if stop:
                continue
            found.add(tuple(clique))
    max_clique = 0
    res = None
    for clique in found:
        if len(clique) > max_clique:
            max_clique = len(clique)
            res = clique
    star2 = str.join(",", sorted(res))
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
