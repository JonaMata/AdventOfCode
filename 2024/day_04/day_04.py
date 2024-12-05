# Day 4 of Advent of Code 2024
import timeit
from aoc.helpers import *
import regex as re


def main():
    inputs = get_input("\n", example=False)
    width = len(inputs[0])+1
    height = len(inputs)
    hor_pattern = r"XMAS|SAMX"
    ver_pattern = rf"X.{'{'+str(width-1)+'}'}M.{'{'+str(width-1)+'}'}A.{'{'+str(width-1)+'}'}S|S.{'{'+str(width-1)+'}'}A.{'{'+str(width-1)+'}'}M.{'{'+str(width-1)+'}'}X"
    diag1_pattern = rf"X.{'{'+str(width)+'}'}M.{'{'+str(width)+'}'}A.{'{'+str(width)+'}'}S|S.{'{'+str(width)+'}'}A.{'{'+str(width)+'}'}M.{'{'+str(width)+'}'}X"
    diag2_pattern = rf"X.{'{'+str(width-2)+'}'}M.{'{'+str(width-2)+'}'}A.{'{'+str(width-2)+'}'}S|S.{'{'+str(width-2)+'}'}A.{'{'+str(width-2)+'}'}M.{'{'+str(width-2)+'}'}X"
    inputstring = str.join("Q", inputs)
    matches_hor = re.findall(hor_pattern, inputstring, overlapped=True)
    matches_ver = re.findall(ver_pattern, inputstring, overlapped=True)
    matches_diag1 = re.findall(diag1_pattern, inputstring, overlapped=True)
    matches_diag2 = re.findall(diag2_pattern, inputstring, overlapped=True)
    print(f"Hor: {len(matches_hor)}, Ver: {len(matches_ver)}, Diag1: {len(matches_diag1)}, Diag2: {len(matches_diag2)}")
    print(f"Star 1: {len(matches_hor)+len(matches_ver)+len(matches_diag1)+len(matches_diag2)}")

    # 2556 -- Too high

    x_pattern1 = rf"M.M.{'{'+str(width-2)+'}'}A.{'{'+str(width-2)+'}'}S.S|"
    x_pattern2 = rf"M.S.{'{'+str(width-2)+'}'}A.{'{'+str(width-2)+'}'}M.S|"
    x_pattern3 = rf"S.M.{'{'+str(width-2)+'}'}A.{'{'+str(width-2)+'}'}S.M|"
    x_pattern4 = rf"S.S.{'{'+str(width-2)+'}'}A.{'{'+str(width-2)+'}'}M.M"
    matches = re.findall(x_pattern1+x_pattern2+x_pattern3+x_pattern4, inputstring, overlapped=True)
    print(f"Star 2: {len(matches)}")

    # 622 -- Too low

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
