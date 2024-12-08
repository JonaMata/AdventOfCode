# Day 11 of Advent of Code 2015
import timeit
from aoc.helpers import *


def check1(password):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return all((
        len(set(re.findall(r"(.)\1", password))) > 1,
        all([x not in 'iol' for x in password]),
        any([password[i:i+3] in alphabet for i in range(len(password)-2)])
    ))

def next_password(password):
    while True:
        result = re.findall(r"^(.+?)(z+)?$", password)[0]
        new_pass = result[0][:-1]+chr(ord(result[0][-1])+1)+'a'*len(result[1])
        password = new_pass
        if check1(password):
            break
    return password


def main():
    inputs = get_input("\n", example=False)
    password = inputs[0]

    password = next_password(password)

    print(f"Part 1: {password}")

    password = next_password(password)
    print(f"Part 2: {password}")

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
