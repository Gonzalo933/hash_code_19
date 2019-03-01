import numpy as np
from symmetric_matrix import SymmetricMatrix

# Test size in memory of matrices of different sizes
sm = SymmetricMatrix(int(7), dtype=np.int8, mem_limit=3000)
print(sm.matrix_size_in_memory())
import pdb

pdb.set_trace()
sm = SymmetricMatrix(int(80000), dtype=np.int8, mem_limit=3000)

# Slow method
"""
start = time.process_time()
for row in range(size_each_group):
    for col in range(size_each_group):
        if row == col or photos_matrix_groups[0][row, col] != -1:
            continue
        # Row represents the current photo
        # Col represents the id to which calculate the score
        photos_matrix_groups[0].set_value(
            row, col, score(horizontal_photos[row], horizontal_photos[col])
        )
        current_id = row * size_each_group + col
    # print(f"Progress {row / size_each_group * 100:.2f}%")
end = time.process_time()
time_1 = end - start
"""
# less slow, not fastest but saves memory
"""
start = time.process_time()
num_elems_in_matrices = photos_matrix_groups[0].num_matrix_elements(
    size_each_group, False
)
for pos in range(num_elems_in_matrices):
    row, col = photos_matrix_groups[0].get_coordinates(pos, False)
    photos_matrix_groups[0].set_value(
        row, col, score(horizontal_photos[row], horizontal_photos[col])
    )
    # print(f"Progress {pos / num_elems_in_matrices * 100:.2f}%")
end = time.process_time()
time_3 = end - start
"""
# Fastest one, but requires creating a big list indices_to_iterate which causes memory problems
"""
start = time.process_time()
indices_to_iterate = np.stack(np.triu_indices(size_each_group, 1), 1)
# Probably faster
for index in range(len(indices_to_iterate)):
    row, col = tuple(indices_to_iterate[index])
    photos_matrix_groups[0].set_value(
        row, col, score(horizontal_photos[row], horizontal_photos[col])
    )
    print(f"Progress {index / len(indices_to_iterate) * 100:.2f}%")
end = time.process_time()
time_2 = end - start
# print(f"{time_1} vs {time_2} vs {time_3}")
pdb.set_trace()
"""
