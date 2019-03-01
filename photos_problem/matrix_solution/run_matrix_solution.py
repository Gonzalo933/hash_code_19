import sys
import os.path
from enum import Enum
import copy
import numpy as np
import utils
from symmetric_matrix import SymmetricMatrix
import pdb
import time


def main(file_path):
    # Read and load data from file
    photos_list = utils.read_file(file_path)
    horizontal_photos = list(filter(utils.is_horizontal, photos_list))
    horizontal_photos = horizontal_photos[0:1000]  # For debug, use only part of the list
    N = len(horizontal_photos)
    num_groups = 6
    size_each_group = int(N / num_groups)
    photos_matrix_groups = []
    for i in range(num_groups):
        try:
            photos_matrix_groups.append(
                SymmetricMatrix(size_each_group, dtype=np.int16, mem_limit=2000)
            )
        except Exception as e:
            print(e)
            sys.exit()
        print(
            f"Current size in memory: {photos_matrix_groups[-1].matrix_size_in_memory()} MB"
        )
    # Fill matrices
    for group_num, photos_matrix in enumerate(photos_matrix_groups):
        fill_matrix(photos_matrix, size_each_group, group_num, horizontal_photos)
    pdb.set_trace()
    # Una vez rellenas las matrices con los scores habria que buscar la manera
    # de poder calcular argmax de una columna dada.
    # Esto nos daria que foto iria la siguiente a la seleccionada.

    # actual_photo <- random de todas las fotos
    # while True
    #       next_photo <- argmax (fila[actual_photo])
    #       actual_photo <- next_photo
    # (hay que tener en cuenta que argmax te puede devolver una foto ya usada)


def fill_matrix(photos_matrix, size_each_group, group_num, horizontal_photos):
    start = time.process_time()
    num_elems_in_matrices = photos_matrix.num_matrix_elements(size_each_group, False)
    for pos in range(num_elems_in_matrices):
        row, col = photos_matrix.get_coordinates(pos, False)
        photos_matrix.set_value(
            row,
            col,
            score(
                horizontal_photos[row + size_each_group * group_num],
                horizontal_photos[col + size_each_group * group_num],
            ),
        )
        print(f"Progress {pos / num_elems_in_matrices * 100:.2f}%")
    end = time.process_time()
    time_3 = end - start
    print(f"Elapsed time {time_3}")


def score(photo1, photo2):
    set_1 = set(photo1["tags"])
    set_2 = set(photo2["tags"])
    num_common_tags_1_and_2 = len(set_1.intersection(set_2))
    num_set_1_not_set_2 = len(set_1 - set_2)
    num_set_2_not_set_1 = len(set_2 - set_1)
    return min(num_common_tags_1_and_2, num_set_1_not_set_2, num_set_2_not_set_1)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "File name to load required as argument"
    file_path = f"../datasets/{sys.argv[-1]}"
    main(file_path)
