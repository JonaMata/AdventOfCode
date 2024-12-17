# Day 13 of Advent of Code 2024
import math
import re
import numpy as np
from sympy import *
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("\n\n", example=False)
    cost = 0
    for machine in inputs:
        a, b, prize = (np.array([[int(num)] for num in re.findall(r"\d+", x)]) for x in machine.split("\n"))
        m = np.array(np.hstack((a,b)))
        sol = np.linalg.lstsq(m, prize)
        if all([math.isclose(x, int(round(x))) for x in sol[0][:,0]]):
            cost += 3*int(round(sol[0][0,0])) + int(round(sol[0][1,0]))

    star1 = cost
    print(f"Star 1: {star1}")



    cost = 0
    for machine in inputs:
        a, b, prize = (np.array([[int(num)] for num in re.findall(r"\d+", x)]) for x in machine.split("\n"))
        prize += 10000000000000
        m = np.array(np.hstack((a,b)))
        sol = np.linalg.solve(m, prize)
        rounded = np.array([[int(round(x))] for x in sol[:,0]])
        if np.array_equal(np.matmul(m,rounded), prize):
            cost += 3*rounded[0,0] + rounded[1,0]

    star2 = cost
    print(f"Star 2: {star2}")

    # 154818567295614 -- Too high
    # 2479629041151 -- Too low

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
