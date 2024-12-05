# Day 23 of Advent of Code 2023
import timeit
import bisect

from aoc.helpers import *


def construct_path(goal, parents, cost):
    current = goal
    path = [current]
    while current in parents:
        current = parents[current]
        path.insert(0, current)
    return path, cost


def find_neighbours(node, grid, slide=False):
    dirs = {'up': (-1, 0), 'right': (0, 1), 'down': (1, 0), 'left': (0, -1)}

    char_map = {'^': 'up', '>': 'right', 'v': 'down', '<': 'left'}
    neighbours = []
    for i, direction in dirs.items():
        neighbour = (node[0] + direction[0], node[1] + direction[1])
        if 0 <= neighbour[0] < len(grid) and 0 <= neighbour[1] < len(grid[0]):
            grid_char = grid[neighbour[0]][neighbour[1]]
            if grid_char == '.' or (grid_char in char_map and not slide):
                neighbours.append(neighbour)
            elif grid_char in char_map:
                neighbours.append(
                    (neighbour[0] + dirs[char_map[grid_char]][0], neighbour[1] + dirs[char_map[grid_char]][1]))

    return neighbours


def f_score(node, goal, g_score):
    return abs(goal[0] - node[0]) + abs(goal[1] - node[1])


def find_path(start, goal, grid, slide=True):
    search = [start]

    parents = dict()
    g_scores = {start: 0}
    f_scores = {start: f_score(start, goal, 0)}

    longest_path = 0

    while len(search) > 0:
        current = search.pop()

        if current == goal:
            # grid = [[x for x in line] for line in grid]
            # for node in path:
            #     if grid[node[0]][node[1]] == '.':
            #         grid[node[0]][node[1]] = 'O'
            #
            # print_2d(grid)

            return g_scores[current]

        for neighbour in find_neighbours(current, grid, slide):
            if current in parents and neighbour == parents[current]:
                continue

            new_g_score = g_scores[current] + abs(neighbour[0] - current[0]) + abs(neighbour[1] - current[1])
            if neighbour not in g_scores or new_g_score > g_scores[neighbour]:
                parents[neighbour] = current
                g_scores[neighbour] = new_g_score
                f_scores[neighbour] = f_score(neighbour, goal, new_g_score)
                if neighbour in search:
                    search.remove(neighbour)
                bisect.insort(search, neighbour, key=lambda x: f_scores[x])

    return longest_path


def maze_to_nodes(start, goal, grid):
    nodes = {start, goal}
    search_nodes = nodes.copy()
    edges = dict()
    visited = set()

    while len(search_nodes) > 0:
        node = search_nodes.pop()
        for neighbour in find_neighbours(node, grid):
            if neighbour not in visited:
                visited.add(neighbour)
                prev = node
                current = neighbour
                neighbours = find_neighbours(current, grid)
                steps = 1
                while len(neighbours) == 2:
                    for step in neighbours:
                        if step != prev:
                            prev = current
                            current = step
                            break
                    neighbours = find_neighbours(current, grid)
                    steps += 1
                visited.add(prev)
                nodes.add(current)
                search_nodes.add(current)
                if node not in edges:
                    edges[node] = dict()
                if current not in edges:
                    edges[current] = dict()
                edges[node][current] = steps
                edges[current][node] = steps

    return nodes, edges


def rec_find_longest_path(start, goal, visited, edges):
    if start == goal:
        return 0
    options = []
    cur_edges = edges[start]
    if goal in cur_edges:
        return edges[start][goal]
    for next_node in edges[start]:
        if next_node not in visited:
            new_visited = visited.copy()
            new_visited.add(next_node)
            new_longest = rec_find_longest_path(next_node, goal, new_visited, edges)
            if new_longest is not None:
                options.append(edges[start][next_node] + new_longest)
    if len(options) == 0:
        return None
    return max(options)


def main():
    inputs = get_input("\n", example=False)

    start = (0, 1)
    goal = (len(inputs) - 1, len(inputs[0]) - 2)

    cost = find_path(start, goal, inputs)

    print(f"Part 1: {cost}")

    nodes, edges = maze_to_nodes(start, goal, inputs)
    print(f"Generated {len(nodes)} nodes")
    longest = rec_find_longest_path(start, goal, {start}, edges)

    print(f"Part 2: {longest}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer() - start}s")
