# Day 9 of Advent of Code 2024
import timeit
from aoc.helpers import *


def main():
    inputs = get_input("", example=False)
    inputs = [int(num) for num in inputs]
    checksum = 0
    start_id = 0
    end_id = len(inputs)-1
    if end_id % 2 != 0:
        end_id -= 1
    left_end = []
    cur_block = 0

    while start_id <= end_id:
        if start_id % 2 == 0:
            for i in range(inputs[start_id]):
                checksum += cur_block * int(start_id/2)
                cur_block += 1
        else:
            for i in range(inputs[start_id]):
                if len(left_end) == 0:
                    if end_id <= start_id:
                        break
                    left_end = [int(end_id/2)] * inputs[end_id]
                    end_id -= 2
                addon = left_end.pop()
                checksum += cur_block * addon
                cur_block += 1

        start_id += 1
    for num in left_end:
        checksum += cur_block * num
        cur_block += 1
    star1 = checksum
    print(f"Star 1: {star1}")

    filesystem = []
    last_block = id
    for i in range(len(inputs)):
        if inputs[i] == 0:
            continue
        if i % 2 == 0:
            filesystem.append([int(i/2), inputs[i]])
            last_id = int(i/2)
        else:
            filesystem.append(["free", inputs[i]])

    cur_id = last_id

    for i in range(cur_id, -1, -1):
        cur = len(filesystem)-1
        while filesystem[cur][0] != i:
            cur -= 1
        search = 0
        found = False
        while search < cur:
            if filesystem[search][0] == "free" and filesystem[search][1] >= filesystem[cur][1]:
                found = True
                break
            search += 1
        if found:
            filesystem.insert(search, filesystem[cur].copy())
            filesystem[cur+1][0] = "free"
            filesystem[search+1][1] -= filesystem[cur+1][1]

    checksum = 0
    cur_block = 0
    for file in filesystem:
        for i in range(file[1]):
            checksum += file[0]*cur_block if file[0] != "free" else 0
            cur_block += 1

    star2 = checksum
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
