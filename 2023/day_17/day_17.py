# Day 17 of Advent of Code 2023
import bisect
import timeit
from aoc.helpers import *


def construct_path(goal, parents, cost):
    current = goal
    path = [current]
    while current in parents:
        current = parents[current]
        path.insert(0, current)
    return path, cost


def find_neighbours(node, grid, turn_range):
    dirs = {'up': (-1, 0), 'right': (0, 1), 'down': (1, 0), 'left': (0, -1)}
    neighbours = []
    for i, direction in dirs.items():
        neighbour = (node[0][0] + direction[0], node[0][1] + direction[1])
        if 0 <= neighbour[0] < len(grid) and 0 <= neighbour[1] < len(grid[0]):
            if (i != node[1] and node[2] >= turn_range[0]) or (i == node[1] and node[2] < turn_range[1]):
                neighbours.append((neighbour, i, node[2] + 1 if i == node[1] else 1))

    return neighbours


def f_score(node, goal, g_score):
    return g_score + abs(goal[0] - node[0][0]) + abs(goal[1] - node[0][1])


def find_path(start, goal, grid, turn_range):
    starts = [(start, 'down', 0), (start, 'right', 0)]
    search = starts

    parents = dict()
    g_scores = {node: 0 for node in starts}
    f_scores = {node: f_score(node, goal, 0) for node in starts}

    while len(search) > 0:
        node = search.pop(0)
        current, prev_dir, last_turn = node

        if current == goal:
            path, cost = construct_path(node, parents, g_scores[node])

            char_map = {'up': '^', 'right': '>', 'down': 'v', 'left': '<'}
            grid = [[x for x in line] for line in grid]
            for node in path:
                grid[node[0][0]][node[0][1]] = char_map[node[1]]

            return path, cost

        for neighbour in find_neighbours(node, grid, turn_range):
            if node in parents and neighbour[0] == parents[node][0]:
                continue
            new_g_score = g_scores[node] + int(grid[neighbour[0][0]][neighbour[0][1]])
            if neighbour not in g_scores or new_g_score < g_scores[neighbour]:
                parents[neighbour] = node
                g_scores[neighbour] = new_g_score
                f_scores[neighbour] = f_score(neighbour, goal, new_g_score)
                if neighbour in search:
                    search.remove(neighbour)
                bisect.insort(search, neighbour, key=lambda x: f_scores[x])

    return [], 0


def main():
    inputs = get_input("\n", example=False)
    start = (0, 0)
    goal = (len(inputs) - 1, len(inputs[0]) - 1)

    best_path, cost = find_path(start, goal, inputs, (0, 3))

    print(f"Part1: {cost}")

    best_path, cost = find_path(start, goal, inputs, (4, 10))

    print(f"Part2: {cost}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer() - start}s")
