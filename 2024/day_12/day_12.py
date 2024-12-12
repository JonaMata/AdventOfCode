# Day 12 of Advent of Code 2024
import timeit
from aoc.helpers import *

def get_neighbours(pos, inputs, include_out_of_bounds = False):
    if include_out_of_bounds:
        return [(pos[0]-1,pos[1]), (pos[0]+1,pos[1]), (pos[0],pos[1]-1), (pos[0],pos[1]+1)]
    return list(filter(lambda x: 0 <= x[0] < len(inputs) and 0 <= x[1] < len(inputs[0]), [(pos[0]-1,pos[1]), (pos[0]+1,pos[1]), (pos[0],pos[1]-1), (pos[0],pos[1]+1)]))

def get_fence_neighbours(fence):
    return [((fence[0][0]-fence[1][1], fence[0][1]-fence[1][0]), fence[1]), ((fence[0][0]+fence[1][1], fence[0][1]+fence[1][0]), fence[1])]

def main():
    inputs = get_input("\n", example=False)
    search = []
    for x in range(len(inputs)):
        for y in range(len(inputs[0])):
            search.append((x, y))

    fence_cost = 0
    while len(search) > 0:
        start = search.pop()
        local_search = get_neighbours(start, inputs)
        area = 1
        perimeter = 4-len(local_search)
        searched = [start]
        while len(local_search) > 0:
            spot = local_search.pop()
            if spot in searched:
                continue
            if inputs[spot[0]][spot[1]] == inputs[start[0]][start[1]]:
                area += 1
                neighbours = get_neighbours(spot, inputs)
                perimeter += 4-len(neighbours)
                local_search.extend(neighbours)
                if spot in search:
                    search.remove(spot)
                searched.append(spot)
            else:
                perimeter += 1
        fence_cost += area*perimeter

    star1 = fence_cost
    print(f"Star 1: {star1}")

    search = []
    for x in range(len(inputs)):
        for y in range(len(inputs[0])):
            search.append((x, y))

    fence_cost = 0
    while len(search) > 0:
        start = search.pop()
        char = inputs[start[0]][start[1]]
        local_search = [start]
        area = 0
        sides = 0
        searched = []
        fence_sets = []
        while len(local_search) > 0:
            spot = local_search.pop()
            if spot in searched:
                continue
            area += 1
            neighbours = get_neighbours(spot, inputs, True)
            for neighbour in neighbours:
                if 0 <= neighbour[0] < len(inputs) and 0 <= neighbour[1] < len(inputs[0]) and inputs[neighbour[0]][neighbour[1]] == char:
                    local_search.append(neighbour)
                else:
                    fence = (spot, (neighbour[0]-spot[0],neighbour[1]-spot[1]))
                    fence_neighbours = get_fence_neighbours(fence)
                    found_sets = []
                    for fence_set in fence_sets:
                        if fence_neighbours[0] in fence_set or fence_neighbours[1] in fence_set:
                            found_sets.append(fence_set)
                    if  len(found_sets) == 0:
                        fence_sets.append([fence])
                    else:
                        found_sets[0].append(fence)
                        for found_set in found_sets[1:]:
                            found_sets[0].extend(found_set)
                            fence_sets.remove(found_set)

            if spot in search:
                search.remove(spot)
            searched.append(spot)
        fence_cost += area * len(fence_sets)

    star2 = fence_cost
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
