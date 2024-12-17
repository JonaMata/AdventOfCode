import os
import sys
import re
import pathlib


def get_input(split: str = None, example: bool = False):
    path = 'input.txt' if not example else 'example.txt'
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Input file does not exist at {path}")
    inputs = open(path)
    if split is not None:
        if split == "":
            inputs = [char for char in inputs.read()]
        else:
            inputs = inputs.read().split(split)
        return inputs
    else:
        return inputs.read()
