# Day 21 of Advent of Code 2024
import bisect
import math
import re
import timeit
from multiprocessing import Pool

from aoc.helpers import *

# robo_move_map = {
#     ('<', '^'): ['>^'],
#     ('<', '>'): ['>>'],
#     ('<', 'v'): ['>'],
#     ('<', 'A'): ['>>^', '>^>']
# }

def get_neighbours(spot, maze):
    neighbours = [
        (spot[0], spot[1]-1),
        (spot[0], spot[1]+1),
        (spot[0]-1, spot[1]),
        (spot[0]+1, spot[1])
    ]
    return list(filter(lambda x: 0 <= x[0] < len(maze) and 0 <= x[1] < len(maze[0]) and maze[x[0]][x[1]] != ' ', neighbours))

def path_to_sequence(path):
    move_to_seq = {
        (0, 1): '>',
        (0, -1): '<',
        (1, 0): 'v',
        (-1, 0): '^'
    }

    seq = ""
    path.reverse()
    prev = path[0]
    for cur in path[1:]:
        seq += move_to_seq[(cur[0]-prev[0], cur[1]-prev[1])]
        prev = cur
    return seq


def reconstruct_paths(root, parents, path):
    path.append(root)
    if root not in parents:
        return [path]
    paths = []
    for parent in parents[root][0]:
        paths.extend(reconstruct_paths(parent, parents, path.copy()))
    return paths

def find_shortest_input(start, goal, maze):
    queue = [(start, 0)]
    shortest = math.inf
    visited = set()
    parents = {}
    end = None

    while len(queue) > 0:
        cur, cost = queue.pop(0)
        visited.add(cur)
        if cost > shortest:
            continue
        if maze[cur[0]][cur[1]] == goal:
            if cost < shortest:
                shortest = cost
            if not end:
                end = cur
            continue

        for neighbour in get_neighbours(cur, maze):
            if neighbour in visited:
                continue
            if neighbour in parents:
                if parents[neighbour][1] == cost:
                    parents[neighbour][0].append(cur)
                elif parents[neighbour][1] > cost:
                    parents[neighbour] = ([cur], cost)
            else:
                parents[neighbour] = ([cur], cost)


            bisect.insort(queue, (neighbour, cost+1), key=lambda x: x[1])

    return reconstruct_paths(end, parents, [])

# def code_to_sequence(code, seqmap, scoremap, use_cache = True):
#     seq = ''
#     for i in range(len(code)-1):
#         best = math.inf
#         new_seq = None
#         for extra in seqmap[(code[i], code[i+1])]:
#             test = seq+extra+'A'
#             score = sequence_score(test, scoremap)
#             if score < best:
#                 new_seq = test
#         seq = new_seq
#     return seq

cache = {}
cache_max = 0
cache_hit = 0
cache_miss = 0
def code_to_sequences(code, seqmap, use_cache = True):
    global cache_max, cache_hit, cache_miss
    if use_cache:
        if code in cache:
            cache_hit += 1
            return cache[code]
    if len(code) < 2:
        return ['']
    seqs = []
    used_cache = False
    if use_cache and cache_max > 2:
        for i in range(min(cache_max, len(code)), 2, -1):
            if code[:i] in cache:
                used_cache = True
                for cache_code in cache[code[:i]]:
                    for extra in code_to_sequences(code[i-1:], seqmap, use_cache):
                        seqs.append(cache_code+extra)
    if not used_cache:
        cache_miss += 1
        for move in seqmap[(code[0], code[1])]:
            for extra in code_to_sequences(code[1:], seqmap, use_cache):
                seqs.append(move+'A'+extra)
    else:
        cache_hit += 1
    res = set(seqs)
    if use_cache:
        cache[code] = res
        cache_max = max(cache_max, max([len(code) for code in res]))
    return res

def sequence_score(seq, scoremap):
    score = 0
    for i in range(len(seq)-1):
        score += scoremap[(seq[i], seq[i+1])]
    return score

def print_hitrate():
    global cache_hit, cache_miss
    total = cache_hit+cache_miss
    hitrate = cache_hit/total*100
    print(f"Cache hitrate: {hitrate:.0f}%")

def process_input():
    codes = get_input("\n", example=True)

    numpad = [
        '789',
        '456',
        '123',
        ' 0A'
    ]
    nums = list('1234567890A')

    keypad = [
        ' ^A',
        '<v>'
    ]
    keys = list('<v>^A')

    # Create numpad keymap
    nummap = {}
    for y in range(len(numpad)):
        for x in range(len(numpad[0])):
            num = numpad[y][x]
            if num == ' ':
                continue
            check_nums = nums.copy()
            check_nums.remove(num)
            for check_num in check_nums:
                paths = find_shortest_input((y, x), check_num, numpad)
                nummap[(num, check_num)] = set([path_to_sequence(path) for path in paths])

    # Create keypad keymap
    keymap = {}
    for y in range(len(keypad)):
        for x in range(len(keypad[0])):
            key = keypad[y][x]
            if key == ' ':
                continue
            check_keys = keys.copy()
            check_keys.remove(key)
            for check_key in check_keys:
                paths = find_shortest_input((y, x), check_key, keypad)
                keymap[(key, check_key)] = set([path_to_sequence(path) for path in paths])
    for key in keys:
        keymap[(key, key)] = ['']

    scoremap = keymap.copy()
    for key in scoremap.keys():
        scoremap[key] = len(list(scoremap[key])[0])

    for key in nummap.keys():
        lowest = min([sequence_score(path, scoremap) for path in nummap[key]])
        nummap[key] = list(filter(lambda x: sequence_score(x, scoremap) == lowest, nummap[key]))

    for key in keymap.keys():
        lowest = min([sequence_score(path, scoremap) for path in keymap[key]])
        keymap[key] = list(filter(lambda x: sequence_score(x, scoremap) == lowest, keymap[key]))

    return codes, nummap, keymap, scoremap

cache = {}

def find_length(code: str, keymap: dict, robots: int):
    if robots == 0:
        return len(code)
    lens = []
    for seq in code_to_sequences('A'+code, keymap):
        print(seq)
        lens.append(sum([find_length(part+'A', keymap, robots-1) for part in seq[:-1].split('A')]))
    return min(lens)

def create_lengths_map(keymap, robots):
    return {key: min([find_length(code+'A', keymap, robots-1) for code in val]) for key, val in keymap.items()}


def part1(vals):
    codes, nummap, keymap, scoremap = vals

    lens_map = create_lengths_map(keymap, 1)
    print(lens_map)
    complexity_sum = 0
    for code in codes:
        keys = code_to_sequences('A' + code, nummap)

        print(keys)
        lens = []
        for key in keys:
            length = 0
            for i in range(len(key)-1):
                length += lens_map[(key[i], key[i+1])]
            lens.append(length)
        num_part = int(re.findall(r"\d+", code)[0])
        complexity_sum += num_part * min(lens)
        print(code, lens)
    return complexity_sum

    complexity_sum = 0
    for code in codes:
        key = code_to_sequence('A'+code, nummap, scoremap, False)
        # shortest = min([len(key) for key in keys])
        # lowest_score = min([sequence_score(key, scoremap) for key in keys])
        for i in range(2):
            # keys = list(filter(lambda x: len(x) == shortest and sequence_score(x, scoremap) == lowest_score, keys))
            # new_keys = []
            # for key in keys:
            #     new_keys.extend(code_to_sequences('A'+key, keymap))
            key = code_to_sequence('A'+key, keymap, scoremap)
            # shortest = min([len(key) for key in new_keys])
            # lowest_score = min([sequence_score(key, scoremap) for key in new_keys])

            # keys = new_keys
        num_part = int(re.findall(r"\d+", code)[0])
        # shortest = min([len(key) for key in keys])
        complexity_sum += num_part*len(key)
    return complexity_sum

def part2(vals):
    return 0
    codes, nummap, keymap, scoremap = vals
    complexity_sum = 0
    for code in codes:
        print(f"Checking code: {code}")
        keys = code_to_sequences('A'+code, nummap, False)
        # shortest = min([len(key) for key in keys])
        # lowest_score = min([sequence_score(key, scoremap) for key in keys])
        for i in range(25):
            print_hitrate()
            print(f"\tLayer {i}/25")
            # keys = list(filter(lambda x: len(x) == shortest and sequence_score(x, scoremap) == lowest_score, keys))
            print(f"\tChecking {len(keys)} keys")
            new_keys = []
            checked = 0
            for key in keys:
                new_keys.extend(code_to_sequences('A'+key, keymap))
                checked += 1
                print(f"\t\tChecked {checked}/{len(keys)}")
            # shortest = min([len(key) for key in new_keys])
            # lowest_score = min([sequence_score(key, scoremap) for key in new_keys])
            keys = new_keys
        num_part = int(re.findall(r"\d+", code)[0])
        shortest = min([len(key) for key in keys])
        complexity_sum += num_part*shortest

    return complexity_sum


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
