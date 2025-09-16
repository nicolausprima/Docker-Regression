# matriks/sparsematrix.py
from matrix import Matrix
class SparseMatrix(Matrix):
 """
 Representasi matriks jarang (sparse) yang lebih efisien.
 Mematuhi LSP karena dapat menggantikan Matrix biasa.
 """
 def __init__(self, data):
 # Baris ini memanggil konstruktor kelas induk (Matrix)
  super().__init__(data)
  self._sparse_data = {}
  for r, row in enumerate(data):
   for c, val in enumerate(row):
    if val != 0:
     self._sparse_data[(r, c)] = val

 def get_value(self, row, col):
  return self._sparse_data.get((row, col), 0)

def __str__(self):
 print(f"Debug: rows={self.rows}, cols={self.cols}")
 output = ""
 for r in range(self.rows):
  row_str = []
  for c in range(self.cols):
   row_str.append(str(self.get_value(r, c)))
  output += " ".join(row_str) + "\n"
 return str(self.data)

def multiply_sparse_matrices(A: SparseMatrix, B: SparseMatrix) -> SparseMatrix:
    if A.cols != B.rows:
        raise ValueError("Dimensi matriks tidak cocok untuk perkalian.")

    result_data = [[0] * B.cols for _ in range(A.rows)]

    # Hanya loop elemen non-nol dari A
    for (i, k), val_a in A._sparse_data.items():
        for j in range(B.cols):
            val_b = B.get_value(k, j)
            if val_b != 0:
                result_data[i][j] += val_a * val_b

    return SparseMatrix(result_data)

