def is_symmetric(matrix):
    """
    Mengecek apakah sebuah matriks simetris.
    Matriks simetris berarti matrix[i][j] == matrix[j][i] untuk semua elemen.
    """
    if matrix.rows != matrix.cols:
        return False

    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix.data[i][j] != matrix.data[j][i]:
                return False

    return True
