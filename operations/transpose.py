from matrix import Matrix

def transpose_matrix(matrix):
    """
    Melakukan operasi transpose pada sebuah objek matriks.
    Transpose dilakukan dengan menukar baris menjadi kolom dan sebaliknya.
    """
    result_data = [
        [matrix.data[j][i] for j in range(matrix.rows)]
        for i in range(matrix.cols)
    ]

    return Matrix(result_data)
