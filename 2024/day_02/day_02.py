# Day 2 of Advent of Code 2024
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("\n", example=False)
    reports = [[int(num) for num in line.split(' ')] for line in inputs]
    star1 = sum([1 if report_is_safe(rep) else 0 for rep in reports])
    print(f"Star 1: {star1}")
    star2 = sum([1 if check_combinatinos(rep) else 0 for rep in reports])
    print(f"Star 2: {star2}")


def report_is_safe(rep):
    asc = (rep[0] - rep[1]) < 0
    for i in range(len(rep)-1):
        diff = rep[i] - rep[i+1]
        if ((diff < 0) != asc) or abs(diff) < 1 or abs(diff) > 3:
            return False
    return True

def check_combinatinos(rep: list):
    for i in range(len(rep)):
        rep_copy = rep.copy()
        del rep_copy[i]
        if report_is_safe(rep_copy):
            return True
    return False


def report_is_safe_with_dampener(rep):
    print(rep)
    fault_index = -1
    asc = (rep[0] - rep[1]) < 0
    for i in range(len(rep)-1):
        start = i if i != fault_index else fault_index-1
        end = i+1
        print(f"Comparing {start} and {end}")
        diff = rep[start] - rep[end]
        if ((diff < 0) != asc) or abs(diff) < 1 or abs(diff) > 3:
            if fault_index == -1:
                if i == 0:
                    asc = (rep[0] - rep[2]) < 0
                fault_index = i+1
                continue
            return False
    if fault_index >= 0:
        print(f"Had fault at {fault_index}")
    return True


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
