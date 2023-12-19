# Day 19 of Advent of Code 2023
import timeit
from functools import reduce
from operator import lt, gt
from aoc.helpers import *


def process_condition(condition, for_range):
    if ':' not in condition:
        if for_range:
            return None, condition
        return lambda x: True, condition
    condition, target = condition.split(':')

    operator_map = {
        '<': lt,
        '>': gt,
    }

    var = condition[0]
    operator = condition[1]
    comp = operator_map[operator]
    val = int(condition[2:])
    if for_range:
        return (var, operator, val), target
    return lambda x: comp(x[var], val), target


def process_map(map_item, for_range=False):
    name, conditions = map_item[:-1].split('{')
    conditions = conditions.split(',')
    conditions = list(map(lambda x: process_condition(x, for_range), conditions))
    return name, conditions


def process_part(part, maps, map_name='in'):
    part_map = maps[map_name]
    for condition in part_map:
        if condition[0](part):
            if condition[1] == 'R':
                return False
            elif condition[1] == 'A':
                return True
            else:
                return process_part(part, maps, condition[1])


def process_part_range(part, maps, map_name='in'):
    if map_name == 'R':
        return 0
    if map_name == 'A':
        options = reduce(lambda x, y: x * y, [x[1] - x[0] + 1 for x in part.values()])
        return options
    part_map = maps[map_name]
    processed = 0
    for condition in part_map:
        if condition[0] is None:
            processed += process_part_range(part, maps, condition[1])
            return processed
        var, operator, val = condition[0]
        map_val = part[var]
        if operator == '<':
            if map_val[1] < val:
                processed += process_part_range(part, maps, condition[1])
                return processed
            if map_val[0] < val:
                new_part = part.copy()
                new_part[var] = (map_val[0], val-1)
                part[var] = (val, map_val[1])
                processed += process_part_range(new_part, maps, condition[1])
        else:
            if map_val[0] > val:
                processed += process_part_range(part, maps, condition[1])
                return processed
            if map_val[1] > val:
                new_part = part.copy()
                new_part[var] = (val+1, map_val[1])
                part[var] = (map_val[0], val)
                processed += process_part_range(new_part, maps, condition[1])


def main():
    maps, inputs = get_input("\n\n", example=False)
    normal_maps = map(lambda x: process_map(x), maps.splitlines())
    normal_maps = {x[0]: x[1] for x in normal_maps}

    parts = [{var[0]: int(var[2:]) for var in x[1:-1].split(',')} for x in inputs.splitlines()]

    accepted_parts = filter(lambda x: process_part(x, normal_maps), parts)

    total = sum([sum(x.values()) for x in accepted_parts])
    print(f"Part 1: {total}")

    range_maps = map(lambda x: process_map(x, True), maps.splitlines())
    range_maps = {x[0]: x[1] for x in range_maps}

    ranged_part = {
        'x': (1, 4000),
        'm': (1, 4000),
        'a': (1, 4000),
        's': (1, 4000),
    }

    options = process_part_range(ranged_part, range_maps)

    print(f"Part 2: {options}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
