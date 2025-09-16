# matriks/main.py
from matrix import Matrix
from operations.adder import add_matrices
from operations.multiplier import multiply_matrices
from utilities import print_matrix
from exporters.csv_exporter import export_to_csv
import time
from matrix import Matrix
from sparsematrix import multiply_sparse_matrices
from sparsematrix import SparseMatrix
from exporters.csv_exporter import export_to_csv
from exporters.json_exporter import export_to_json

def create_sparse_data(size):
 data = [[0] * size for _ in range(size)]
 data[0][0] = 1
 data[size-1][size-1] = 1
 return data

if __name__ == "__main__":
 print("\n--- Menguji Solusi dengan SparseMatrix ---")
 sparse_data_1000 = create_sparse_data(1000)
 # Perhatikan: kita instansiasi SparseMatrix
 mat_a = SparseMatrix(sparse_data_1000)
 mat_b = SparseMatrix(sparse_data_1000)
 start_time = time.time()
 # Perhatikan: fungsi multiply_matrices() tidak berubah sama sekali
 product_mat = multiply_sparse_matrices(mat_a, mat_b)
 end_time = time.time()
 print(f"Waktu yang dibutuhkan untuk perkalian: {end_time - start_time:.2f} detik")

 print("\n--- Pembuktian OCP dengan Penjumlahan ---")
 # Matriks padat (dense)
 matriks_padat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
 # Matriks jarang (sparse) yang memiliki nilai yang sama
 matriks_jarang = SparseMatrix([[1, 0, 0], [0, 5, 0], [7, 0, 9]])
 # Lakukan penjumlahan matriks padat + matriks jarang
 # Perhatikan: fungsi 'add_matrices()' tidak diubah sama sekali
 hasil_penjumlahan = add_matrices(matriks_padat, matriks_jarang)
 print("Hasil Penjumlahan Matriks Biasa dan Sparse:")
 print(str(hasil_penjumlahan))

 print("\n--- Menguji Matrix Exporters ---")
 # Buat objek matriks yang akan diekspor
 matriks_demo = Matrix([
 [1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]
 ])
 # Ekspor ke CSV
 # Perhatikan bahwa kita memanggil fungsi baru tanpa mengubah kelas Matrix
 print("Mengekspor matriks ke format CSV...")
 export_to_csv(matriks_demo, "matriks_output.csv")
 # Ekspor ke JSON
 # Ini juga membuktikan OCP karena kelas Matrix tidak perlu diubah
 print("\nMengekspor matriks ke format JSON...")
 export_to_json(matriks_demo, "matriks_output.json")
