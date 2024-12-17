# Day 17 of Advent of Code 2024
import timeit
from aoc.helpers import *

def get_combo(arg, regs):
    return arg if arg <= 3 else regs[arg-4]

def run_program(reg_init, program):
    regs = reg_init.copy()
    regs.append(None)
    inst_counter = 0
    output = []
    while 0 <= inst_counter < len(program):
        jumped = False
        inst = program[inst_counter]
        arg = program[inst_counter+1]
        match inst:
            case 0 | 6 | 7:
                reg = 0 if inst == 0 else inst-5
                regs[reg] = int(regs[0]/pow(2, get_combo(arg, regs)))
            case 1 | 4:
                arg2 = arg if inst == 1 else regs[2]
                regs[1] = regs[1] ^ arg2
            case 2 | 5:
                regs[1 if inst == 2 else 3] = get_combo(arg, regs) % 8
            case 3:
                if regs[0] != 0:
                    inst_counter = arg
                    jumped = True
            case _:
                break
        if regs[3] is not None:
            output.append(regs[3])
            regs[3] = None
        if not jumped:
            inst_counter += 2

    return output



def main():
    reg_init, program = get_input("\n\n", example=False)
    reg_init = [int(x) for x in re.findall(r"\d+", reg_init)]
    program = [int (x) for x in re.findall(r"\d", program)]

    output = run_program(reg_init, program)

    star1 = str.join(",", [str(x) for x in output])
    print(f"Star 1: {star1}")

    reg_init = [0, 0, 0]
    output_check = str.join(",", [str(x) for x in program])
    while True:
        output = run_program(reg_init, program)
        output = str.join(",", [str(x) for x in output])
        if output == output_check:
            break
        elif output_check.endswith(output):
            reg_init[0] *= 8
        else:
            reg_init[0] += 1


    star2 = reg_init[0]
    print(f"Star 2: {star2}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {(timeit.default_timer()-start)*1000:.2f}ms")
