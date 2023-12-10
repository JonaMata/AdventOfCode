# Day 5 of Advent of Code 2023
# <PUZZLE TITLE>
import math
from bisect import bisect

# <PUZZLE DESCRIPTION>

from aoc.helpers import *


def find_location(seed):
    num = seed
    for m in maps:
        index = bisect(m, num, key=lambda x: x[1])
        if index-1 < 0: continue
        cur_m = m[index-1]
        num_diff = num - cur_m[1]
        num_range = cur_m[2]
        if num_diff < num_range:
            num = cur_m[0]+num_diff
    return num


def rec_find_location(map_index, num, num_range):
    if map_index == len(maps):
        return num
    m = maps[map_index]
    locs = []
    index = bisect(m, num, key=lambda x: x[1])
    left_map = m[index-1] if index-1 >= 0 else None
    right_map = m[index] if index < len(m) else None

    if left_map and left_map[1]+left_map[2]-1 >= num:
        diff = num - left_map[1]
        end = min(left_map[2] - diff, num_range)
        locs.append(rec_find_location(map_index+1, left_map[0]+diff, end))
        num += end
        num_range -= end

    if num_range > 0:
        if right_map:
            if right_map[1] <= num+num_range-1:
                if right_map[1] > num:
                    end = right_map[1] - num
                    locs.append(rec_find_location(map_index+1, num, end))
                    num += end
                    num_range -= end

                end = min(num_range, right_map[2])
                locs.append(rec_find_location(map_index+1, right_map[0], end))
                num += end
                num_range -= end
                if num_range > 0:
                    locs.append(rec_find_location(map_index, num, num_range))
            else:
                locs.append(rec_find_location(map_index+1, num, num_range))
        else:
            locs.append(rec_find_location(map_index+1, num, num_range))

    return min(locs)


if __name__ == "__main__":
    inputs = get_input("\n\n", example=False)

    seeds = [int(s) for s in re.findall(r"\d+", inputs[0])]

    maps = []

    for m in inputs[1::]:
        ranges = [[int(n) for n in re.findall(r"\d+", nums)] for nums in m.splitlines()[1::]]
        maps.append(sorted(ranges, key=lambda x: x[1]))

    locations = map(find_location, seeds)

    print(f"Part 1: {min(locations)}")

    min_loc = math.inf

    to_be_checked = sum([n for n in seeds[1::2]])
    sys.setrecursionlimit(1500000)
    for i in range(0, len(seeds), 2):
        min_loc = min(min_loc, rec_find_location(0, seeds[i], seeds[i + 1]))
        # for num in range(seeds[i], seeds[i]+seeds[i+1]):
        #     min_loc = min(min_loc, find_location(num))
        #     checks += 1
        #     if checks%1000000 == 0:
        #         print(f"Checked: {checks/to_be_checked*100}%")

    print(f"Part 2: {min_loc}")