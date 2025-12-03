# Day 24 of Advent of Code 2024
import itertools
import operator
import timeit
import networkx as nx
import matplotlib.pyplot as plt
from aoc.helpers import *

ops = {
    "OR": operator.ior,
    "AND": operator.iand,
    "XOR": operator.xor
}
def calc_outcome(init_vals, signals, wires):
    def calc_wire(wire):
        if wire in init_vals:
            return init_vals[wire]
        if wire in wires:
            return wires[wire]
        signal = signals[wire]
        out = ops[signal[1]](calc_wire(signal[0]),
                             calc_wire(signal[2]))
        wires[wire] = out
        return out

    total = ""
    for end in sorted(filter(lambda x: x[0] == 'z', signals.keys())):
        # total = str(calc_wire(end)) + total
        total += str(calc_wire(end))
    # return int(total, base=2)
    return total

def get_wrong_bits(val, expected):
    wrong_bits = []
    for i in range(len(wrong := str(bin(val ^ expected))[::-1])):
        if wrong[i] == '1':
            wrong_bits.append(i)
    return wrong_bits

def perform_switches(switches, signals):
    signals = signals.copy()
    for switch in switches:
        s1 = signals[switch[0]]
        s2 = signals[switch[1]]
        del signals[switch[0]]
        del signals[switch[1]]
        signals[switch[0]] = s2
        signals[switch[1]] = s1
    return signals

def verify_switches(switches, signals):
    for switch in switches:
        for node in switch:
            queue = [node]
            visited = set()
            while len(queue) > 0:
                cur = queue.pop()
                if cur[0] in 'xy':
                    continue
                visited.add(cur)
                for wir in signals[cur][::2]:
                    if wir in visited:
                        # print("bad", switch, cur, wir)
                        return False
                    queue.append(wir)
    return True

def find_bad_bits(init_vals, signals):
    errs = []
    for i in range(len(init_vals)//2):
        err_out = set()
        # print(f"Checking x{i:02}")
        for j in range(4):
            x = j%2
            y = j//2
            new_init = init_vals.copy()
            new_init[f"x{i:02}"] = x
            new_init[f"y{i:02}"] = y
            out = calc_outcome(new_init, signals, {})
            # print(f"\tx={x} y={y}",new_init)
            for k in range(2):
                if k == 0:
                    expected = x ^ y
                if k == 1:
                    expected = x & y
                # print(f"\tz{k:02}={out[k]} : {expected}")
                if int(out[i+k]) != expected:
                    err_out.add(i+k)
        if len(err_out) > 0:
            errs.append((i, tuple(err_out)))
    return errs

def find_dependent(node, signals):
    found = set()
    queue = [node]
    while len(queue) > 0:
        cur = queue.pop()
        found.add(cur)
        for key, val in signals.items():
            if cur in val[::2] and key not in found:
                queue.append(key)
    return set(filter(lambda x: x[0] not in 'xy', found))

def find_depending(node, signals):
    found = set()
    queue = [node]
    while len(queue) > 0:
        cur = queue.pop()
        found.add(cur)
        if cur in signals:
            for key in signals[cur][::2]:
                if key not in found:
                    queue.append(key)
    return set(filter(lambda x: x[0] not in 'xy', found))


def process_input():
    init_vals, signals = get_input("\n\n", example=False)
    init_vals = {init[:3]: int(init[5]) for init in init_vals.split("\n")}
    signals = {sig[-3:]: tuple(sig.split(" ->")[0].split(" ")) for sig in signals.split("\n")}
    return init_vals, signals, {}

def part1(vals):
    init_vals, signals, wires = vals
    return int(calc_outcome(init_vals, signals, wires)[::-1], base=2)

def part2_do_over_over(vals):
    init_vals, signals, wires = vals
    wrongs1 = []
    wrongs2 = []
    for key, val in signals.items():
        if key[0] == 'z':
            if key[1:] == '45':
                continue
            if val[1] != 'XOR':
                wrongs1.append(key)
                continue
        elif val[0][0] not in 'xy':
            if val[1] == 'XOR':
                wrongs2.append(key)
    print(wrongs1, wrongs2)

    wrongs3 = []
    for key, val in signals.items():
        if val[0] not in 'x00y00':
            if val[0][0] in 'xy' and val[1] == 'XOR':
                found = False
                for k, v in signals.items():
                    if v[1] == 'XOR' and key in v[::2]:
                        found = True
                        break
                if not found:
                    wrongs3.append(key)
            elif val[0][0] in 'xy' and val[1] == 'AND':
                found = False
                for k, v in signals.items():
                    if v[1] == 'OR' and key in v[::2]:
                        found = True
                        break
                if not found:
                    wrongs3.append(key)
    print(wrongs3)
    return str.join(",", list(sorted(set(wrongs1+wrongs2+wrongs3))))
    swaps = []
    for wrong in wrongs2:
        dep = find_dependent(wrong, signals)
        swap = None
        for wrong1 in wrongs1:
            next = f"z{int(wrong1[1:])+1:02}"
            if next in dep:
                swap = wrong1
                break
        swaps.append((wrong, swap))

    print(swaps)



def part2_do_over(vals):
    init_vals, signals, wires = vals

    empty_init_vals = {key: 0 for key in init_vals.keys()}
    bad_bits = find_bad_bits(empty_init_vals, signals)

    print("bad bits", len(bad_bits))

    candidate_sets = []
    for bad in bad_bits:
        x = find_dependent(f"x{bad[0]:02}", signals)
        y = find_dependent(f"y{bad[0]:02}", signals)
        ins = x.union(y)

        outs = set()
        for out in bad[1]:
            outs.update(find_depending(f"z{out:02}", signals))

        candidates = ins.intersection(outs)
        if len(candidates) > 0:
            candidate_sets.append(candidates)

        sets = set()
        for a in candidates:
            for b in candidates:
                if a != b and (a, b) not in sets and (b, a) not in sets:
                    sets.add((a, b))
        working_sets = []
        for switch in sets:
            test_signals = perform_switches([switch], signals)
            if not verify_switches([switch], test_signals):
                continue
            working_sets.append(switch)
        print("los", len(candidates))

    all_candidates = set()
    for candidates in candidate_sets:
        all_candidates.update(candidates)

    ac = list(all_candidates)
    print("candidates", len(all_candidates))

    sets = set()
    for a in all_candidates:
        for b in all_candidates:
            if a != b and (a, b) not in sets and (b, a) not in sets:
                sets.add((a, b))

    print("sets", len(sets))

    working_sets = []
    for switch in sets:
        test_signals = perform_switches([switch], signals)
        if not verify_switches([switch], test_signals):
            continue
        working_sets.append(switch)
        # res = calc_outcome(init_vals, test_signals, {})
        # test_wrong_bits = get_wrong_bits(res, expected)
        # if len(test_wrong_bits) < len(wrong_bits):
        #     better_sets.append((switch, len(test_wrong_bits)))

    # working_sets = sets
    print("working", len(working_sets))

    two_sets = []
    two_checked = set()
    for a in working_sets:
        for b in working_sets:
            if a[0] not in b and a[1] not in b and (a, b) not in two_checked and (b, a) not in two_checked:
                two_checked.add((a, b))
                test_signals = perform_switches([a, b], signals)
                if not verify_switches([a, b], test_signals):
                    continue
                two_sets.append((a, b))

    print("two sets", len(two_sets))

    full_sets = []
    full_checked = set()
    nope = 0
    for a in two_sets:
        for b in two_sets:
            if a == b or (a, b) in full_checked or (b, a) in full_checked:
                continue
            full_checked.add((a, b))
            if any([x in b[0] or x in b[1] for x in a[0] + a[1]]):
                continue
            test_signals = perform_switches([a[0], a[1], b[0], b[1]], signals)
            if not verify_switches([a[0], a[1], b[0], b[1]], test_signals):
                continue
            full_sets.append((a, b))

    print("full sets", len(full_sets))
    print(nope)

    # combinations = []
    # for a in range(len(all_candidates)):
    #     for b in range(a, len(all_candidates)):
    #         for c in range(b, len(all_candidates)):
    #             for d in range(c, len(all_candidates)):
    #                 for e in range(d, len(all_candidates)):
    #                     for f in range(e, len(all_candidates)):
    #                         for g in range(f, len(all_candidates)):
    #                             for h in range(g, len(all_candidates)):
    #                                 combination = (ac[a], ac[b], ac[c], ac[d], ac[e], ac[f], ac[g], ac[h])
    #                                 if all([any([x in combination for x in candidates]) for candidates in candidate_sets]):
    #                                     combinations.append(combination)
    #
    # print(len(combinations))


def part2(vals):
    init_vals, signals, wires = vals

    x_total = ""
    for wire in sorted(filter(lambda x: x[0] == 'x', init_vals.keys())):
        x_total = str(init_vals[wire]) + x_total
    x_res = int(x_total, base=2)

    y_total = ""
    for wire in sorted(filter(lambda x: x[0] == 'y', init_vals.keys())):
        y_total = str(init_vals[wire]) + y_total
    y_res = int(y_total, base=2)

    z_res = calc_outcome(init_vals, signals, wires)

    expected = x_res+y_res

    wrong_bits = get_wrong_bits(z_res, expected)

    print(wrong_bits)
    return

    def get_affected_wires(wire):
        if wire in init_vals:
            return []
        wires = {wire}
        for wir in signals[wire][::2]:
            wires.update(get_affected_wires(wir))
        return wires

    affected_wires = set()
    for bit in wrong_bits:
        affected_wires.update(get_affected_wires('z'+(2-len(str(bit)))*'0'+str(bit)))

    # wire_count = {wire: affected_wires.count(wire) for wire in set(affected_wires)}
    # wire_count = {k: v for k, v in sorted(wire_count.items(), key=lambda x: x[1])}
    # print(wire_count)

    sets = set()
    for a in affected_wires:
        for b in affected_wires:
            if a != b and (a, b) not in sets and (b, a) not in sets:
                sets.add((a, b))

    working_sets = []
    for switch in sets:
        test_signals = perform_switches([switch], signals)
        if not verify_switches([switch], test_signals):
            continue
        working_sets.append(switch)
        # res = calc_outcome(init_vals, test_signals, {})
        # test_wrong_bits = get_wrong_bits(res, expected)
        # if len(test_wrong_bits) < len(wrong_bits):
        #     better_sets.append((switch, len(test_wrong_bits)))

    two_sets = []
    two_checked = set()
    total = len(working_sets)*(len(working_sets)-1)
    done = 0
    for a in working_sets:
        for b in working_sets:
            done += 1
            if done % 1000 == 0:
                print(f"2-sets: {done}/{total}")
            if a[0] not in b and a[1] not in b and (a, b) not in two_checked and (b, a) not in two_checked:
                two_checked.add((a, b))
                test_signals = perform_switches([a, b], signals)
                if not verify_switches([a, b], test_signals):
                    continue
                two_sets.append((a, b))
                # print("Here")
                # res = calc_outcome(init_vals, test_signals, {})
                # test_wrong_bits = get_wrong_bits(res, expected)
                # if len(test_wrong_bits) < expected:
                #     betterer_sets.append((a, b, len(test_wrong_bits)))

    print(len(two_sets))

    full_sets = []
    full_checked = set()
    total = len(two_sets)*(len(two_sets)-1)
    done = 0
    start = timeit.default_timer()
    for a in two_sets:
        for b in two_sets:
            done += 1
            if done % 1000 == 0:
                now = timeit.default_timer()
                speed = (now-start)/done
                left = (total-done)*speed
                mins = left//60
                secs = left%60
                print(f"full-sets: {done}/{total}\tcorrect: {len(full_sets)}\tETA: {mins:2.0f}m{secs:2.0f}")
            if a == b or (a, b) in full_checked or (b, a) in full_checked:
                continue
            two_checked.add((a, b))
            if any([x in b[0] or x in b[1] for x in a[0]+a[1]]):
                continue
            test_signals = perform_switches([a[0], a[1], b[0], b[1]], signals)
            if not verify_switches([a[0], a[1], b[0], b[1]], test_signals):
                continue
            full_sets.append((a, b))

    print(full_sets)


    # working_combinations = []
    # setlen = len(working_sets)
    # total = setlen*(setlen-1)*(setlen-2)*(setlen-3)
    # done = 0
    # prev_done = 0
    # a_done = set()
    # for a in sets:
    #     a_done.add(a)
    #     b_done = set()
    #     for b in working_sets:
    #         b_done.add(b)
    #         if b in a_done:
    #             done += (setlen-2)*(setlen-3)
    #             continue
    #         c_done = set()
    #         for c in working_sets:
    #             c_done.add(c)
    #             if c in a_done or c in b_done:
    #                 done += setlen-3
    #                 continue
    #             for d in working_sets:
    #                 done += 1
    #                 if done > prev_done+1000:
    #                     prev_done = done
    #                     print(f"Checking {done}/{total}")
    #                 if d in a_done or d in b_done or d in c_done:
    #                     continue
    #                 test_signals = perform_switches([a, b, c, d], signals)
    #                 if not verify_switches([a, b, c, d], test_signals):
    #                     continue
    #                 working_combinations.append((a, b, c, d))




    # print(working_combinations)

    star2 = None
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
    print(f"Star 2: {part2_do_over_over(inputs)}")
    print(f"Time taken: {(timeit.default_timer()-start_part2)*1000:.2f}ms")

    print(f"\n Total time taken: {(timeit.default_timer()-start_total)*1000:.2f}ms")
