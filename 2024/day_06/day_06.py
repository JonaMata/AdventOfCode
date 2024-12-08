# Day 6 of Advent of Code 2024
import timeit
from multiprocessing import Pool

from aoc.helpers import *
import numpy as np

def main():
    inputs = get_input("\n", example=True)
    maze = np.array([[char for char in line] for line in inputs])
    start_pos = find_pos(maze)
    pos = start_pos.copy()
    start_dir = np.array([-1,0])
    cur_dir = start_dir.copy()
    visited = set()
    visited_with_dir = []
    exited = False
    while not exited:
        if tuple(pos) not in visited:
            visited_with_dir.append((pos, cur_dir.copy()))
        visited.add(tuple(pos))
        next_pos = pos + cur_dir
        if next_pos[0] < 0 or next_pos[0] >= len(maze) or next_pos[1] < 0 or next_pos[1] >= len(maze[0]):
            exited = True
        elif maze[next_pos[0],next_pos[1]] == '#':
            old_dir = cur_dir.copy()
            cur_dir[0] = old_dir[1]
            cur_dir[1] = -old_dir[0]
        else:
            pos = next_pos

    print(f"Star 1: {len(visited)}")

    queue = []
    for obstacle in visited_with_dir:
        if obstacle[0][0] == start_pos[0] and obstacle[0][1] == start_pos[1]:
            continue
        new_maze = maze.copy()
        new_maze[obstacle[0][0], obstacle[0][1]] = '#'
        queue.append((new_maze, obstacle[0]-obstacle[1], obstacle[1]))

    with Pool(10) as p:
        result = sum(p.map(check_loop, queue))


    print(f"Star 2: {result}")


def check_loop(args):
    maze, start_pos, start_dir = args
    pos = start_pos.copy()
    cur_dir = start_dir.copy()
    visited = set()
    while True:
        cur_hash = (tuple(pos), tuple(cur_dir))
        if cur_hash in visited:
            return 1
        visited.add(cur_hash)
        next_pos = pos + cur_dir
        if next_pos[0] < 0 or next_pos[0] >= len(maze) or next_pos[1] < 0 or next_pos[1] >= len(maze[0]):
            return 0
        elif maze[next_pos[0], next_pos[1]] == '#':
            old_dir = cur_dir.copy()
            cur_dir[0] = old_dir[1]
            cur_dir[1] = -old_dir[0]
        else:
            pos = next_pos


def find_pos(maze):
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x,y] == '^':
                maze[x,y] = '.'
                return np.array([x, y])

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
