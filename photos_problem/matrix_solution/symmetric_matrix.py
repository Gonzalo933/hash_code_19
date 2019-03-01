import numpy as np
from scipy.special import factorial
import sys


class SymmetricMatrix:
    def __init__(self, N, dtype=np.int16, mem_limit=1000, store_diagonal=False):
        """Class that represents a symmetric matrix.
        The underlying representation is an array.

        Arguments:
            N {int} -- Number of rows/cols. The matrix is always square NxN

        Keyword Arguments:
            dtype {type} -- Type of the data. should be taken into account to save memory (default: {np.int16})
            mem_limit {float} -- Memory limit in MB. if mem_limit is exceeded creation will fail (default: {1000})
            store_diagonal {bool} -- If the diagonal of the symmetric matrix should be stored (default: {False})
        """

        self.store_diagonal = store_diagonal
        self.N = N
        expected_size = self.calculate_expected_size(N, dtype, store_diagonal)
        print(f"Expected size = {expected_size} MB")
        if expected_size >= mem_limit:
            raise Exception(f"Mem limit exceeded")
        matrix_size = self.num_matrix_elements(N, store_diagonal)
        # self.matrix = np.arange(matrix_size, dtype=dtype)
        self.matrix = np.ones(matrix_size, dtype=dtype) * -1

    def matrix_size_in_memory(self):
        # Returns Mbytes
        return self.matrix.nbytes / 1e6

    def calculate_expected_size(self, N, dtype, store_diagonal):
        # Returns MB
        size_type = {
            str(np.int16): 16 / 8,
            str(np.int32): 32 / 8,
            str(np.int8): 1,
            str(np.uint16): 16 / 8,
            str(np.uint8): 1,
        }
        N = self.num_matrix_elements(N, store_diagonal)
        return (N * size_type[str(dtype)]) / 1e6

    def num_matrix_elements(self, N, store_diagonal):
        if not store_diagonal:
            N -= 1
        return self.sum_n_numbers(N)

    def num_elements_in_row(self, N, row, store_diagonal):
        """Returns number of elements in a given row.
        Takes into account that
        if we are not storing the diagonal
        that's one element less in each row

        Arguments:
            N {int} -- number of row or cols of the symmetric matrix, always square(NxN)
            row {int} -- Row number to return number of elements
            store_diagonal {bool} -- if the matrix representation is storing the diagonal

        Returns:
            int -- number of elements in row.
        """
        if row < 0:
            return 0
        return N - row - (0 if store_diagonal else 1)

    def sum_n_numbers(self, N):
        # Check https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF
        return int(N * (N + 1) / 2)

    def get_position_in_array(self, N, row, col, store_diagonal):
        """
        Returns the real position in the array of an element of the matrix.
        Arguments:
            N {int} -- number of row or cols of the symmetric matrix, always square(NxN)
            row {int} -- Row index
            col {int} -- Col index
            store_diagonal {bool} -- if the matrix representation is storing the diagonal

        Returns:
            int -- Index in the list of the element [row, col]
        """

        # Accounts for the number of missing cells at the start because it's a symmetric matrix
        total_offset_from_row = row * N - self.sum_n_numbers(row)
        num_elements_removed_from_row = N - self.num_elements_in_row(
            N, row, store_diagonal
        )
        total_offset_from_col = col - num_elements_removed_from_row
        return total_offset_from_row + total_offset_from_col

    def get_coordinates(self, pos, store_diagonal):
        # The opossite of the method above.
        # Returns the row,col of a position of the underlying array
        # See: https://stackoverflow.com/questions/27086195/linear-index-upper-triangular-matrix
        # and:  https://stackoverflow.com/questions/19143657/linear-indexing-in-symmetric-matrices
        N = self.N
        if not store_diagonal:
            row = N - 2 - int(np.sqrt(-8 * pos + 4 * N * (N - 1) - 7) / 2.0 - 0.5)
            col = pos + row + 1 - N * (N - 1) / 2 + (N - row) * ((N - row) - 1) / 2
        else:
            row = int((2 * n + 1 - np.sqrt((2 * N + 1) * (2 * N + 1) - 8 * pos)) / 2)
            col = k - n * row + row * (row - 1) / 2
        return int(row), int(col)

    def check_if_valid_indexes(self, N, row, col, store_diagonal):
        """Checks if the provided row,col of the matrix is valid or out of bounds

        Arguments:
            N {int} -- number of row or cols of the symmetric matrix, always square(NxN)
            row {int} -- Row index
            col {int} -- Col index
            store_diagonal {bool} -- if the matrix representation is storing the diagonal

        Returns:
            bool -- if row and col are valid
        """

        if not store_diagonal and row == col:
            return False
        extra_elem_diagonal = 0 if store_diagonal else 1
        min_row = 0
        max_row = N - 1 - extra_elem_diagonal
        # Min index of a col given its row
        min_col = row + extra_elem_diagonal
        max_col = N - 1
        if col < min_col or col > max_col:
            return False
        if row < min_row or row > max_row:
            return False
        return True

    def set_value(self, row, col, value):
        if not self.check_if_valid_indexes(self.N, row, col, self.store_diagonal):
            # Check if swapping indexes work or fail
            row, col = (col, row)
            if not self.check_if_valid_indexes(self.N, row, col, self.store_diagonal):
                raise IndexError(f"Wrong indexes {(col, row)}")
        pos = self.get_position_in_array(self.N, row, col, self.store_diagonal)
        if pos < 0:
            raise IndexError(f"pos={pos} not valid {(row, col)}")
        self.matrix[pos] = value

    def __getitem__(self, slice_tuple):
        """Allows to use this class as a matrix.
        For example:
            N = 7
            sm = SymmetricMatrix(N)
            last_element_third_row = sm[2, N-1]
        Also takes into account that the matrix is symmetric.
        That means that calling sm[2, N-1] has the same effect as sm[2, N-1]

        Arguments:
            slice_tuple {tuple} -- tuple (row,col)

        Returns:
            int -- element corresponding to the position in the matrix (row,col)
        """
        if not type(slice_tuple) == type((1, 1)):
            raise TypeError("Use a tuple as slice")
        row, col = slice_tuple
        if not self.check_if_valid_indexes(self.N, row, col, self.store_diagonal):
            # Check if swapping indexes work or fail
            row, col = (col, row)
            if not self.check_if_valid_indexes(self.N, row, col, self.store_diagonal):
                raise IndexError(f"Wrong indexes {(col, row)}")
        pos = self.get_position_in_array(self.N, row, col, self.store_diagonal)
        if pos < 0:
            raise IndexError(f"pos={pos} not valid {(row, col)}")
        return self.matrix[pos]
