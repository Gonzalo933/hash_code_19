import sys
import os.path
from enum import Enum
import copy
import numpy as np


# Pizza is a matrix with values (this could be done with a enum, but...):
# T -> Tomatoe
# M -> Mushroom
# X -> Sliced (this cell is part of a slice, cannot be used again)


def main(file_path):
    # Read and load data from file
    R, C, L, H, pizza = read_file(file_path)

    dummy_find(R, C, L, H, pizza)


def dummy_find(R, C, L, H, pizza):
    # This algorithm just goes top to bottom and left to right finding slices.
    # TOTALLY SUBOPTIMAL
    slices_coordinates = []
    for row in range(R):
        for col in range(C):
            current_slice = {"T": 0, "M": 0, "coords": []}
            possible_slices = define_slice(
                copy.deepcopy(current_slice), row, col, R, C, L, H, copy.deepcopy(pizza)
            )
            # TODO:
            # Check which one/s of the possible_slices should we use
            import pdb

            pdb.set_trace()


def define_slice(current_slice, row, col, R, C, L, H, pizza):
    print(f"->{(row, col)}")
    pizza, current_slice = add_cells_into_slice(
        copy.deepcopy(current_slice), row, col, copy.deepcopy(pizza)
    )
    # print(pizza)
    valid_coordinates = find_valid_adjacent_cells(row, col, R, C, L, H, pizza)
    if not valid_coordinates or current_slice["T"] + current_slice["M"] >= H:
        # Check that the current slice is valid
        if slice_is_valid(current_slice, R, C, L, H, pizza):
            return [current_slice]
        return [None]
    # Update current slice
    slices = []
    # print(valid_coordinates)
    for coord in valid_coordinates:
        print(current_slice)
        print(slices)
        print(f"{coord}->")
        for s in define_slice(
            copy.deepcopy(current_slice), *coord, R, C, L, H, copy.deepcopy(pizza)
        ):
            if s:
                # import pdb
                # pdb.set_trace()
                slices.append(s)

    return slices


def add_cell(current_slice, row, col, pizza):
    current_slice[pizza[row, col]] += 1
    pizza[row, col] = "X"
    assert (row, col) not in current_slice["coords"], "This is not working (add cell)"

    current_slice["coords"].append((row, col))
    return current_slice


def add_cells_into_slice(current_slice, row, col, pizza):
    # This ensures that if we want to finish a slice into row, col all the cells
    # in the 'middle' are also sliced (because slices have to be in a rectangular shape)

    # number_curent_row_x = len(np.where(pizza[row, :] == "X")[0])
    # number_curent_col_x = len(np.where(pizza[:, col] == "X")[0])
    current_slice = add_cell(current_slice, row, col, pizza)
    min_row = np.argwhere(pizza == "X")[:, 0].min()
    max_row = np.argwhere(pizza == "X")[:, 0].max()

    min_col = np.argwhere(pizza == "X")[:, 1].min()
    max_col = np.argwhere(pizza == "X")[:, 1].max()

    for r in range(min_row - 1, max_row + 1):
        for c in range(min_col - 1, max_col + 1):
            if is_valid_coordinates(r, c, pizza):
                current_slice = add_cell(current_slice, r, c, pizza)
                # print((r, c))
    return pizza, current_slice


def slice_is_valid(current_slice, R, C, L, H, pizza):
    if current_slice["T"] + current_slice["M"] > H:
        return False
    if current_slice["T"] < L or current_slice["M"] < L:
        return False
    return True


def find_valid_adjacent_cells(row, col, R, C, L, H, pizza):
    # Given some coordinates row, col
    # Returns a list of valid coordinates to expand the slice
    valid_coordinates = []
    # There is at most 4 possible valid coordinates
    coordinates_to_check = [
        (row - 1, col),
        (row, col - 1),
        (row + 1, col),
        (row, col + 1),
    ]
    for tup in coordinates_to_check:
        if is_valid_coordinates(*tup, pizza):
            valid_coordinates.append(tup)
    return valid_coordinates


def is_valid_coordinates(row, col, pizza, also_check_sliced=True):
    # Checks wheter given coordinates are part of the pizza
    if row < 0 or col < 0 or row >= pizza.shape[0] or col >= pizza.shape[1]:
        return False
    if also_check_sliced and pizza[row, col] == "X":
        return False
    return True


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
    file_path = f"../{sys.argv[-1]}"
    main(file_path)
