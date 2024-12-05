# Day 24 of Advent of Code 2023
import re
import timeit

import numpy as np
import matplotlib.pyplot as plt

from aoc.helpers import *

x, y, z, dx, dy, dz = range(6)


# Custom dot product function because numpy can't handle my big numbers💪
def dot_product(v1, v2):
    product = 0
    for i in range(len(v1)):
        product += int(v1[i]) * int(v2[i])
    return product

def find_intersection(l1, l2):
    d = l1[dx] * l2[dy] - l2[dx] * l1[dy]

    if d == 0:
        return None

    t_n = (l1[x] - l2[x]) * (-l2[dy]) - (l1[y] - l2[y]) * (-l2[dx])
    u_n = (l1[x] - l2[x]) * (-l1[dy]) - (l1[y] - l2[y]) * (-l1[dx])

    t = t_n/d
    u = u_n/d

    if t >= 0 and u >= 0:
        return l1[x]+t*l1[dx], l1[y]+t*l1[dy]
    elif False and u >= 0:
        return l2[x]+u*l2[dx], l2[y]+u*l2[dy]

    return None


def main():
    example = False
    inputs = get_input("\n", example=example)
    lines = [list(map(int, re.findall(r"-?\d+", line))) for line in inputs]

    interval = (200000000000000, 400000000000000) if not example else (7, 27)

    intersections = 0

    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            intersection = find_intersection(lines[i], lines[j])
            if intersection:
                if interval[0] <= intersection[x] <= interval[1] and interval[0] <= intersection[y] <= interval[1]:
                    intersections += 1

    print(f"Part 1: {intersections}")

    ref = np.array(lines[0])

    ref_lines = [np.array([line[i]-ref[i] for i in range(6)]) for line in lines[1:4]]
    l2 = ref_lines[0]
    plane_normal = np.cross(l2[:3], l2[:3]+l2[3:])

    points = []
    for line in ref_lines[1:]:
        t1 = np.dot(-line[:3], plane_normal)
        t2 = np.dot(line[3:], plane_normal)
        t = dot_product(-line[:3], plane_normal)/ dot_product(line[3:], plane_normal)
        p = line[:3]+t*line[3:]
        p_r = p+ref[:3]+t*ref[3:]
        points.append((p, t))

    u = np.multiply((1/(points[0][1]-points[1][1])), (points[0][0]-points[1][0]))


    start = points[0][0] - points[0][1] * u + ref[:3]

    print(f"Part 2: {start[x]+start[y]+start[z]}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
