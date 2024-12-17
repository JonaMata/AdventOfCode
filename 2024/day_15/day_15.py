# Day 15 of Advent of Code 2024
import timeit
from copy import deepcopy

from sympy.strategies.core import switch

from aoc.helpers import *
import numpy as np

movemap = {
    '^': np.array([-1,0]),
    'v': np.array([1,0]),
    '<': np.array([0,-1]),
    '>': np.array([0,1])
}

boxmap = {
    '[': np.array([0,1]),
    ']': np.array([0,-1])
}

def do_move(pos, move, maze):
    next_pos = pos+move
    next_obj = maze[next_pos[0]][next_pos[1]]
    can_move = True
    if next_obj == '#':
        return pos, False
    if next_obj == 'O':
        can_move = do_move(next_pos, move, maze)[1]
    if can_move:
        maze[next_pos[0]][next_pos[1]] = maze[pos[0]][pos[1]]
        maze[pos[0]][pos[1]] = '.'
        return next_pos, True
    return pos, False

def do_move_special(pos, move, maze, extra = False):
    moves = []
    next_pos = pos+move
    next_obj = maze[next_pos[0]][next_pos[1]]
    this_obj = maze[pos[0]][pos[1]]
    can_move = True
    if next_obj == '#':
        return [], False
    if next_obj in ['[', ']']:
        moves, can_move = do_move_special(next_pos, move, maze)
    if can_move:
        if not extra and this_obj in ['[', ']'] and (np.array_equal(move, movemap['^']) or np.array_equal(move, movemap['v'])):
            extra_moves, can_move = do_move_special(pos+boxmap[this_obj], move, maze, True)
            if not can_move:
                return [], False
            moves.extend(extra_moves)
        scale_factor = sum(move*next_pos)
        moves.append((scale_factor, tuple(pos), tuple(move)))
        return moves, True
    return [], False

def main():
    maze_text, movements = get_input("\n\n", example=False)
    maze = [[x for x in line] for line in maze_text.split("\n")]
    movements = movements.replace('\n', '')
    pos = None
    for y in range(len(maze)):
        if pos is not None:
            break
        for x in range(len(maze)):
            if maze[y][x] == '@':
                pos = np.array([y, x])
                break

    for movement in movements:
        pos, success = do_move(pos, movemap[movement], maze)

    coord_sum = 0
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'O':
                coord_sum+=x+100*y

    star1 = coord_sum
    print(f"Star 1: {star1}")
    maze_text = maze_text.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
    maze = [[x for x in line] for line in maze_text.split("\n")]
    pos = None
    for y in range(len(maze)):
        if pos is not None:
            break
        for x in range(len(maze)):
            if maze[y][x] == '@':
                pos = np.array([y, x])
                break

    for movement in movements:
        moves, success = do_move_special(pos, movemap[movement], maze)
        if success:
            moves = list(set(moves))
            moves = sorted(moves, key=lambda x: x[0], reverse=True)
            for i in range(len(moves)):
                move = moves[i]
                move_pos = np.array(move[1])
                next_pos = move_pos+np.array(move[2])
                maze[next_pos[0]][next_pos[1]] = maze[move[1][0]][move[1][1]]
                maze[move[1][0]][move[1][1]] = '.'
            pos += movemap[movement]
    coord_sum = 0
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == '[':
                coord_sum += x + 100 * y

    star2 = coord_sum
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
