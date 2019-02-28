import sys
import os.path
from enum import Enum
import copy
import numpy as np


def main(file_path):
    # Read and load data from file
    R, C, L, H, pizza = read_file(file_path)

    dummy_find(R, C, L, H, pizza)


def read_file(file_path):
    # Read and load data from file
    with open(file_path, "r") as f:
        file_lines = f.readlines()
    # First line are variables
    R, C, L, H = tuple(map(int, file_lines[0].rstrip().split(" ")))

    pizza = np.array([list(line.rstrip()) for line in file_lines[1:]])
    # Small check in case something went bad when parsing file
    assert pizza.shape == (R, C), "File parsing failed."
    return R, C, L, H, pizza


if __name__ == "__main__":
    assert len(sys.argv) > 1, "File name to load required as argument"
    file_path = f"{sys.argv[-1]}"
    main(file_path)
