# Day 16 of Advent of Code 2024
import bisect
import math
import timeit

from aoc.helpers import *
import numpy as np

rot_left = lambda x: np.array([-x[1], x[0]])
rot_right = lambda x: np.array([x[1], -x[0]])

def get_neighbours(pos, dire, maze):
    neighbours = [
        (pos, rot_left(dire), 1000),
        (pos, rot_right(dire), 1000)
    ]
    next_pos = pos+dire
    if 0 <= next_pos[0] < len(maze) and 0 <= next_pos[1] < len(maze[0]) and maze[next_pos[0]][next_pos[1]] != '#':
        neighbours.append((next_pos, dire, 1))
    return neighbours


def h_score(pos, end):
    return abs(end[0]-pos[0])+abs(end[1]-pos[1])

def a_star(start_pos, end, maze):
    start_dir = np.array([0,1])

    queue = [(h_score(start_pos, end), start_pos, start_dir)]
    visited = set()

    while len(queue) > 0:
        cost, pos, dire = queue.pop(0)

        if np.array_equal(pos, end):
            return cost

        if ((pos[0], pos[1]), (dire[0], dire[1])) in visited:
            continue

        visited.add(((pos[0], pos[1]), (dire[0], dire[1])))

        cost -= h_score(pos, end)

        for neighbour, rot, edge_cost in get_neighbours(pos, dire, maze):
            if ((neighbour[0], neighbour[1]), (rot[0], rot[1])) in visited:
                continue

            neighbour_cost = cost + edge_cost + h_score(neighbour, end)
            bisect.insort(queue, (neighbour_cost, neighbour, rot), key=lambda x: x[0])

    return "Broken"

def a_star_all(start_pos, end, maze, best):
    start_dir = np.array([0,1])

    queue = []
    visited = {
        (tuple(start_pos), tuple(start_dir)): [0, []]
    }

    for neighbour, rot, edge_cost in get_neighbours(start_pos, start_dir, maze):
        neighbour_cost = edge_cost + h_score(neighbour, end)
        bisect.insort(queue, (neighbour_cost, neighbour, rot, (tuple(start_pos), tuple(start_dir))), key=lambda x: x[0])

    lowest_end_score = math.inf
    ends = []

    while len(queue) > 0:
        cost, pos, dire, parent = queue.pop(0)

        if np.array_equal(pos, end):
            if cost < lowest_end_score:
                ends = [parent]
                lowest_end_score = cost
            elif cost == lowest_end_score:
                ends.append(parent)

            continue

        if (tuple(pos), tuple(dire)) in visited:
            continue


        cost -= h_score(pos, end)

        visited[(tuple(pos), tuple(dire))] = [cost, [parent]]

        for neighbour, rot, edge_cost in get_neighbours(pos, dire, maze):
            neighbour_cost = cost + edge_cost

            if (tuple(neighbour), tuple(rot)) in visited:
                node = visited[(tuple(neighbour), tuple(rot))]
                if neighbour_cost < node[0]:
                    node[1] = [(tuple(pos), tuple(dire))]
                elif neighbour_cost == node [0]:
                    node[1].append((tuple(pos), tuple(dire)))

            neighbour_total = neighbour_cost + h_score(neighbour, end)
            bisect.insort(queue, (neighbour_total, neighbour, rot, (tuple(pos), tuple(dire))), key=lambda x: x[0])

    spots = set()
    queue = ends
    while len(queue) > 0:
        node = queue.pop()
        spots.add(node[0])
        if node in visited:
            queue.extend(visited[node][1])

    for spot in spots:
        maze[spot[0]][spot[1]] = 'O'

    return len(spots)+1

def main():
    maze = [[x for x in line] for line in get_input("\n", example=False)]

    start_pos = None
    end = None
    for y in range(len(maze)):
        if start_pos is not None and end is not None:
            break
        for x in range(len(maze)):
            if start_pos is not None and end is not None:
                break
            if maze[y][x] == 'S':
                start_pos = np.array([y, x])
            elif maze[y][x] == 'E':
                end = np.array([y, x])


    star1 = a_star(start_pos, end, maze)
    print(f"Star 1: {star1}")


    star2 = a_star_all(start_pos, end, maze, star1)
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
