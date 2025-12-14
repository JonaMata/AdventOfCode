# Day 10 of Advent of Code 2025
import timeit
from aoc.helpers import *
import numpy as np
from pulp import *

def process_input():
    vals = get_input("\n", example=False)
    machines = []
    for val in vals:
        lights = tuple([-1 if x == '.' else 1 for x in val.split("]")[0][1:]])
        button_strings = val.split("]")[1][2:].split("{")[0][:-2].split(') (')
        buttons = tuple([list(map(int, x.split(','))) for x in button_strings])
        joltage = tuple(map(int, val.split('{')[1][0:-1].split(',')))
        machines.append((lights, buttons, joltage))
    return machines

def get_button_presses(machine):
    lights, buttons, joltage = machine
    checked = set()
    queue = [(0, tuple([-1]*len(lights)))]
    while True:
        presses, state = queue.pop(0)
        if state == lights:
            return presses
        if state in checked:
            continue
        checked.add(state)
        for button in buttons:
            new_state = list(state)
            for i in button:
                new_state[i] *= -1
            queue.append((presses+1, tuple(new_state)))
        queue.sort()

def part1(machines):
    total = 0
    for machine in machines:
        total += get_button_presses(machine)
    star1 = total
    return star1


def part2(machines):
    total = 0
    count = 0
    for machine in machines:
        count += 1
        lights, buttons, joltage = machine
        button_mat = [[0 for _ in buttons] for _ in joltage]
        for i in range(len(buttons)):
            for j in buttons[i]:
                button_mat[j][i] = 1
        A = button_mat
        b = list(joltage)
        m = len(A)
        n = len(A[0])

        X_INDICES = list(range(n))
        B_INDICES = list(range(m))

        model = LpProblem("Challenge", LpMinimize)
        x = LpVariable.dict('x', X_INDICES, lowBound=0, cat=LpInteger)

        model += lpSum(x[i] for i in X_INDICES)
        for j in B_INDICES:
            LHS = lpSum(A[j][i] * x[i] for i in X_INDICES)
            model += LHS == b[j]

        model.solve(PULP_CBC_CMD(msg=0))
        total += value(model.objective)
    star2 = total
    return star2


if __name__ == "__main__":
    start_total = timeit.default_timer()
    start_input = start_total
    inputs = process_input()
    print(f"Input processed, time taken: {(timeit.default_timer()-start_input)*1000:.2f}ms")
    start_part1 = timeit.default_timer()
    print(f"Part 1: {part1(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part1)*1000:.2f}ms")
    start_part2 = timeit.default_timer()
    print(f"Star 2: {part2(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part2)*1000:.2f}ms")

    print(f"\n Total time taken: {(timeit.default_timer()-start_total)*1000:.2f}ms")
