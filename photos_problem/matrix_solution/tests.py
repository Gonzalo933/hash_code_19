import numpy as np
from symmetric_matrix import SymmetricMatrix

# Test size in memory of matrices of different sizes
sm = SymmetricMatrix(int(7), dtype=np.int8, mem_limit=3000)
print(sm.matrix_size_in_memory())
import pdb

pdb.set_trace()
sm = SymmetricMatrix(int(80000), dtype=np.int8, mem_limit=3000)
