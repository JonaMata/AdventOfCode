# Day 18 of Advent of Code 2024
import timeit
import bisect
import numpy as np
from aoc.helpers import *

dirs = [
    np.array([0,1]),
    np.array([0,-1]),
    np.array([1,0]),
    np.array([-1,0])
]

def get_neighbours(pos, maze):
    neighbours = [pos+dire for dire in dirs]
    return filter(lambda x: 0 <= x[0] < maze.shape[0] and 0 <= x[1] < maze.shape[1] and maze[*x] == 0, neighbours)

def h_score(pos, end):
    return abs(end[0]-pos[0])+abs(end[1]-pos[1])

def a_star(start_pos, end, maze):

    queue = [(1+h_score(neighbour, end), neighbour, start_pos) for neighbour in get_neighbours(start_pos, maze)]
    visited = {
        tuple(start_pos): None
    }
    final = None

    while len(queue) > 0:
        cost, pos, parent = queue.pop(0)

        if np.array_equal(pos, end):
            final = tuple(parent)
            break

        if (tuple(pos)) in visited:
            continue

        visited[tuple(pos)] = tuple(parent)

        cost -= h_score(pos, end)

        for neighbour in get_neighbours(pos, maze):
            if (tuple(neighbour)) in visited:
                continue

            neighbour_cost = cost + 1 + h_score(neighbour, end)
            bisect.insort(queue, (neighbour_cost, neighbour, pos), key=lambda x: x[0])

    if final is None:
        return set()
    cur = final
    path = {tuple(end), tuple(final)}
    while cur in visited:
        cur = visited[cur]
        path.add(cur)

    return path

def bytes_to_maze(falling_bytes, maze):
    for byte in falling_bytes:
        maze[*byte] = 1

def main():
    inputs = [[int(x) for x in byte.split(",")] for byte in get_input("\n", example=False)]
    size = 71

    maze = np.zeros((size, size))
    bytes_to_maze(inputs[:1024], maze)

    start = np.array([0,0])
    end = np.array([size-1, size-1])

    path = a_star(start, end, maze)
    star1 = len(path)
    print(f"Star 1: {star1}")

    cur_byte = 1024
    while True:
        cur_byte+=1
        bytes_to_maze(inputs[cur_byte:cur_byte+1], maze)
        if tuple(inputs[cur_byte]) not in path:
            continue
        path = a_star(start, end, maze)
        if  len(path) == 0:
            break

    star2 = inputs[cur_byte]
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
