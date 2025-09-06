# matriks/utilities.py
def print_matrix(matrix):
 """
 Mencetak isi dari objek matriks.
 """
 for row in matrix.data:
	 print(row)

def is_square(matrix):
    """
    Mengecek apakah sebuah matriks berbentuk persegi.
    """
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise TypeError("Matrix harus berupa list of lists.")

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    return rows == cols


def is_symmetric(matrix):
    """
    Mengecek apakah sebuah matriks simetris.
    """
    if not is_square(matrix):
        return False

    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


def find_determinant(matrix):
    """
    Menghitung determinan dari matriks persegi.
    """
    if not is_square(matrix):
        raise ValueError("Determinant hanya bisa dihitung untuk matriks persegi.")

    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    det = 0
    for col in range(n):
        sub_matrix = [row[:col] + row[col+1:] for row in matrix[1:]]
        cofactor = ((-1) ** col) * matrix[0][col] * find_determinant(sub_matrix)
        det += cofactor
    return det

