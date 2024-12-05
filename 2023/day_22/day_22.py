# Day 22 of Advent of Code 2023
import timeit

import numpy as np

from aoc.helpers import *


class Brick:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end

    def __str__(self):
        return f"Brick: {self.id}"

    def __repr__(self):
        return self.__str__()

    def place(self, grid):
        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                for z in range(self.start[2], self.end[2] + 1):
                    grid[x, y, z] = self.id

    def can_fall(self, grid):
        if self.start[2] - 1 < 0:
            return False
        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                if grid[x, y, self.start[2] - 1] is not None:
                    return False
        return True

    def can_disintegrate(self, grid, bricks):
        for supporting in self.supporting(grid):
            if len(bricks[supporting].supported_by(grid)) <= 1:
                if bricks[supporting].start[2] != 0:
                    return False
        return True

    def supporting(self, grid):
        supporting = set()
        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                if self.end[2]+1 < grid.shape[2] and grid[x, y, self.end[2] + 1] is not None:
                    supporting.add(int(grid[x, y, self.end[2] + 1]))

        return list(supporting)

    def supported_by(self, grid):
        supports = set()
        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                if self.start[2] - 1 >= 0 and grid[x, y, self.start[2] - 1] is not None:
                    supports.add(int(grid[x, y, self.start[2] - 1]))

        return list(supports)

    def fall(self, grid):
        fall = 0
        max_fall = self.start[2]
        hit_brick = False
        while not hit_brick and fall < max_fall:
            fall += 1
            for x in range(self.start[0], self.end[0] + 1):
                for y in range(self.start[1], self.end[1] + 1):
                    if grid[x, y, self.start[2] - fall - 1] is not None:
                        hit_brick = True
                        break

        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                for z in range(self.start[2], self.end[2] + 1):
                    grid[x, y, z] = None

        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                for z in range(self.start[2], self.end[2] + 1):
                    grid[x, y, z - fall] = self.id

        self.start[2] = self.start[2] - fall
        self.end[2] = self.end[2] - fall

    def count_falling(self, grid, bricks):
        # print(f"\n\n{self}")
        falling = {self.id}
        queue = [bricks[brick] for brick in self.supporting(grid)]
        # print(queue)
        # print(falling)
        while len(queue) > 0:
            brick = queue.pop(0)
            supported_by = brick.supported_by(grid)
            # print(supported_by)
            if all([support in falling for support in supported_by]):
                # print(f"Adding: {brick}")
                falling.add(brick.id)
                for supporting in brick.supporting(grid):
                    supported = bricks[supporting]
                    if supported not in queue:
                        queue.append(supported)
        return len(falling) - 1


def fall_bricks(grid, bricks):
    queue = bricks.copy()

    while len(queue) > 0:
        brick = queue.pop(0)

        if brick.can_fall(grid):
            neighbours = brick.supporting(grid)
            brick.fall(grid)
            for neighbour in neighbours:
                if neighbour not in queue:
                    queue.append(bricks[neighbour])


def main():
    inputs = get_input("\n", example=False)
    bricks_coords = [[[int(coord) for coord in coords.split(',')] for coords in line.split('~')] for line in inputs]
    bricks = [Brick(i, brick[0], brick[1]) for i, brick in enumerate(bricks_coords)]
    maxes = [1, 1, 1]
    for brick in bricks:
        for coords in (brick.start, brick.end):
            for i in range(3):
                maxes[i] = max(maxes[i], coords[i]+1)

    grid = np.full(maxes, None)

    for brick in bricks:
        brick.place(grid)

    fall_bricks(grid, bricks)

    for brick in bricks:
        print(f"ID: {brick.id}, start: {brick.start}, end: {brick.end}, supporting: {brick.supporting(grid)}, supported by: {brick.supported_by(grid)}, can disintegrate: {brick.can_disintegrate(grid, bricks)}, falling: {brick.count_falling(grid, bricks)}")
    print(f"Part 1: {sum([brick.can_disintegrate(grid, bricks) for brick in bricks])}")

    falling_bricks = [brick.count_falling(grid, bricks) for brick in bricks]

    print(f"Part 2: {sum(falling_bricks)}")

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
