# Day 7 of Advent of Code 2015
import timeit
from aoc.helpers import *

coms = {
    'AND': '&',
    'OR': '|',
    'LSHIFT': '<<',
    'RSHIFT': '>>',
    'NOT': '~',
}

def run_sequence(instructions, wires, fixed=[]):
    for inst in instructions:
        src, dest = inst.split(' -> ')

        if dest in fixed:
            continue

        src = src.split(' ')
        wait = False
        for i in range(len(src)):
            if not src[i].isnumeric():
                if src[i] in coms:
                    src[i] = coms[src[i]]
                elif src[i] in wires:
                    src[i] = str(wires[src[i]])
                else:
                    wait = True
        if wait:
            instructions.append(inst)
            continue
        wires[dest] = eval(''.join(src))

def main():
    inputs = get_input("\n", example=False)
    wires = dict()
    run_sequence(inputs, wires)
    print(f"Part1: {wires['a']}")

    wires = {'b': wires['a']}
    run_sequence(inputs, wires, ['b'])
    print(f"Part2: {wires['a']}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
