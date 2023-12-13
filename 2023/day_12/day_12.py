# Day 12 of Advent of Code 2023
import itertools
import math
import timeit
from aoc.helpers import *

memory_dict = dict()


def rec_check_configs(row, config):
    global memory_dict

    if (row, tuple(config)) in memory_dict:
        return memory_dict[(row, tuple(config))]

    if calc_config(row) == config:
        # print(f"Row: {row}, Config: {config}, Return: {1}")
        return 1

    if len(config) == 0:
        if '#' in row:
            # print(f"Row: {row}, Config: {config}, Return: {0}")
            return 0
        else:
            # print(f"Row: {row}, Config: {config}, Return: {1}")
            return 1

    num = config[0]
    seqs = list(re.finditer("[?#]+", row))

    first_seq = seqs[0] if len(seqs) > 0 else None
    seqs = list(filter(lambda x: len(x[0]) >= num, seqs))

    if len(seqs) == 0:
        # print(f"Row: {row}, Config: {config}, Return: {0}")
        return 0

    seq = seqs[0]

    if (first_seq[0] != seq[0]) and ('#' in first_seq[0]):
        # print(f"{first_seq[0]} | {seq[0]} | {'#' in first_seq[0]}")
        return 0

    seq = {
        'string': seq[0],
        'start': seq.start(),
        'end': seq.end()
    }

    options = 0

    if '#' in seq['string']:
        first_broken = seq['string'].index('#')
        seq['string'] = seq['string'][:first_broken+num+1]
        seq['end'] = seq['start']+len(seq['string'])
    else:
        options += rec_check_configs(row[seq['end'] + 1:], config)

    # options = 0
    runs = 0
    success_runs = 0
    for i in range(len(seq['string'])-num+1):
        runs += 1
        split = seq['start'] + i + num + 1
        if '#' not in row[:split-num-1]:
            if split-1 == len(row) or (split-1 < len(row) and row[split-1] != '#'):
                success_runs += 1
                options += rec_check_configs(row[split:], config[1:])

    # print(f"Row: {row}, Config: {config}, Num: {num}, Seq: {seq['string']}, Return: {options}, Runs: {runs}, Success runs: {success_runs}")
    memory_dict[(row, tuple(config))] = options
    return options


def check_configs(row, config):
    unknown_matches = re.finditer(r"\?", row)
    broken_count = len(re.findall(r"#", row))
    broken_sum = sum(config)

    configs = 0

    unknowns = [r.start() for r in unknown_matches]

    options = list(itertools.combinations(unknowns, broken_sum-broken_count))

    print(f"Options: {len(options)}")

    for option in options:
        check_row = [x for x in row]
        for index in option:
            check_row[index] = '#'
        if config == calc_config(check_row):
            configs += 1

    print(f"Configs: {configs}")

    return configs


def calc_config(row):
    broken_ranges = re.findall(r"#+", ''.join(row))
    return [len(r) for r in broken_ranges]


def main():
    inputs = get_input("\n", example=False)
    pos_sum = 0
    row_count = 0

    for row in inputs[::]:
        row, config = row.split(' ')
        config = [int(x) for x in config.split(',')]
        configs = rec_check_configs(row, config)
        pos_sum += configs
        # print(f"{row_count/len(inputs)*100}%")

    print(f"Part 1: {pos_sum}")

    pos_sum = 0
    row_count = 0
    for row in inputs:
        row, config = row.split(' ')
        row += 4 * ('?'+row)
        config = [int(x) for x in config.split(',')]
        config = 5 * config
        configs = rec_check_configs(row, config)
        pos_sum += configs
        row_count += 1
        print(f"{row_count/len(inputs)*100}%")

    print(f"Part 2: {pos_sum}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
