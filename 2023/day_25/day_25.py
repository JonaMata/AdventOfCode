# Day 25 of Advent of Code 2023
from __future__ import annotations

import math
import random
import timeit
from collections import defaultdict
from copy import deepcopy
import networkx as nx

from aoc.helpers import *


class Cut:
    def __init__(self, s, t, weight):
        self.s = s
        self.t = t
        self.weight = weight


def merge(graph, s, t):
    for edge in graph[t]:
        if edge != s:
            graph[s][edge] += graph[t][edge]
            # graph[s].append(edge)
            graph[edge][s] += graph[edge][t]
            # graph[edge].append(s)
        del graph[edge][t]
    del graph[t]
    print("complete")


def maximum_adjacency_search(graph):
    start = list(graph.keys())[0]
    found = [start]
    cut_weight = []
    candidates = list(graph.keys())[1:]

    while len(candidates) > 0:
        max_next = None
        max_weight = -math.inf
        for next_c in candidates:
            weight_sum = 0
            for s in found:
                weight_sum += graph[next_c][s]
                # edges = graph[next_c]
                # for edge in edges:
                #     if edge == s:
                #         weight_sum += 1

            if weight_sum > max_weight:
                max_next = next_c
                max_weight = weight_sum

        candidates.remove(max_next)
        found.append(max_next)
        cut_weight.append(max_weight)

    return Cut(found[-2], found[-1], cut_weight[-1])


def stoer_wagner_cut(components):
    graph = deepcopy(components)
    current = []
    current_best = None
    current_best_cut = None
    while len(graph) > 1:
        print(f"Running Stoer Wagner: {(len(components)-len(graph))/len(components)*100}%", end="\r")
        cut_of_phase = maximum_adjacency_search(graph)
        print("biem")
        if current_best_cut is None or cut_of_phase.weight < current_best_cut.weight:
            current_best_cut = cut_of_phase
            current_best = current.copy()
            current_best.append(cut_of_phase.t)
        current.append(cut_of_phase.t)
        merge(graph, cut_of_phase.s, cut_of_phase.t)
    print("Running Stoer Wagner: 100%")
    return current_best, components.keys()-current_best, current_best_cut.weight


def karger_cut(components):
    components = deepcopy(components)
    while len(components) > 2:
        n1, n2 = random.sample(list(components.keys()), 2)
        combined = [n1, n2]
        new_node = n1+'_'+n2
        components[new_node] = [n for n in components[n1]+components[n2] if n not in combined]
        for node in components[n1]+components[n2]:
            components[node] = [new_node if n in combined else n for n in components[node]]
        del components[n1]
        del components[n2]

    groups = []#[n.split('_') for n in components.keys()]
    return len(list(components.values())[0]), groups


def use_networkx(component_names):
    g = nx.Graph()
    g.add_nodes_from([names[0] for names in component_names])
    for names in component_names:
        g.add_edges_from([(names[0], name) for name in names[1:]])

    cut = nx.stoer_wagner(g)
    print(f"Part 2: {len(cut[1][0]) * len(cut[1][1])}")


def main():
    inputs = get_input("\n", example=False)
    component_names = [re.findall(r"\w+", line) for line in inputs]
    components = {names[0]: defaultdict(int, {name: 1 for name in names[1:]}) for names in component_names}
    components_copy = deepcopy(components)
    for component in components_copy:
        for n in components_copy[component]:
            if n not in components:
                components[n] = defaultdict(int)
            components[n][component] = 1

    # g1, g2, weight = stoer_wagner_cut(components)
    #
    # print(f"Part 1: {len(g1)*len(g2)}")

    use_networkx(component_names)

    # cut_length, groups = None, None
    # while True:
    #     cut_length, groups = karger_cut(components)
    #     print(f"Found cut: {cut_length=}")
    #     if cut_length == 3:
    #         break
    #
    # print(f"Found cut of {cut_length}, with answer {len(groups[0])*len(groups[1])}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
