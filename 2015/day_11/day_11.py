# Day 11 of Advent of Code 2015
import timeit
from aoc.helpers import *


def check1(password):
    alphabet = 'abcdefghijklmnopqrstuvw'
    return all((
        len(set(re.findall(r"(.)\1", password))) > 1,
        all([x not in 'iol' for x in password]),
        any([password[i:i+3] in alphabet for i in range(len(password)-3)])
    ))


def main():
    inputs = get_input("\n", example=False)
    password = inputs[0]
    while not check1(password):
        result = re.findall(r"^(.+?)(z+)?$", password)[0]
        new_pass = result[0][:-1]+chr(ord(result[0][-1])+1)
        if len(result) > 0:
            new_pass += 'a'*len(result[1])
        password = new_pass

    print(f"Part 1: {password}")

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
