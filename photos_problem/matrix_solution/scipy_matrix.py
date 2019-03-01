import sys
import os.path
from enum import Enum
import copy
import numpy as np
import utils
from symmetric_matrix import SymmetricMatrix
import pdb
import time
from scipy.sparse import csr_matrix, lil_matrix


def main(file_path):
    # Read and load data from file
    photos_list = utils.read_file(file_path)
    horizontal_photos = list(filter(utils.is_horizontal, photos_list))
    # horizontal_photos = horizontal_photos[0:10000]  # For debug, use only part of the list
    N = len(horizontal_photos)
    num_groups = 10
    size_each_group = int(N / num_groups)
    photos_matrix_groups = []
    for i in range(num_groups):
        try:
            photos_matrix_groups.append(
                lil_matrix((size_each_group, size_each_group), dtype=np.int16)
            )
        except Exception as e:
            print(e)
            sys.exit()

    # Fill matrices
    for group_num, photos_matrix in enumerate(photos_matrix_groups):
        fill_matrix(photos_matrix, size_each_group, group_num, horizontal_photos)
        print(f"{group_num + 1}/{len(photos_matrix_groups)}")
    pdb.set_trace()
    # Una vez rellenas las matrices con los scores habria que buscar la manera
    # de poder calcular argmax de una columna dada.
    # Esto nos daria que foto iria la siguiente a la seleccionada.

    # actual_photo <- random de todas las fotos
    # while True
    #       next_photo <- argmax (fila[actual_photo])
    #       actual_photo <- next_photo
    # (hay que tener en cuenta que argmax te puede devolver una foto ya usada)


def fill_matrix(photos_matrix, N, group_num, horizontal_photos):
    start = time.process_time()
    num_elems_in_matrices = int((N - 1) * (N) / 2)
    total_sum_scores = 0
    for pos in range(num_elems_in_matrices):
        row = int(N - 2 - int(np.sqrt(-8 * pos + 4 * N * (N - 1) - 7) / 2.0 - 0.5))
        col = int(pos + row + 1 - N * (N - 1) / 2 + (N - row) * ((N - row) - 1) / 2)
        photo_1_id = row + N * group_num
        photo_2_id = col + N * group_num
        score = utils.score(horizontal_photos[photo_1_id], horizontal_photos[photo_2_id])
        total_sum_scores += score
        # a la vez que se va rellenando se puede ir pillando el mejor
        photos_matrix[row, col] = score
        progress = pos / num_elems_in_matrices * 100
        if progress % 10 == 0:
            print(f"Progress {progress:.2f}% | score={total_sum_scores}")
    end = time.process_time()
    time_3 = end - start
    print(f"Elapsed time {time_3}")


if __name__ == "__main__":
    assert len(sys.argv) > 1, "File name to load required as argument"
    file_path = f"../datasets/{sys.argv[-1]}"
    main(file_path)
