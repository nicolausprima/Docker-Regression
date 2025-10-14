from matrix import Matrix

def inverse_matrix(matrix):
    """
    Melakukan operasi invers pada sebuah objek matriks.
    Invers hanya dapat dilakukan jika matriks berbentuk persegi (n x n)
    dan determinannya tidak sama dengan nol.
    """
    if matrix.rows != matrix.cols:
        raise ValueError("Matriks harus persegi untuk dapat di-invers.")

    n = matrix.rows

    A = [[float(matrix.data[i][j]) for j in range(n)] for i in range(n)]

    I = [[float(i == j) for j in range(n)] for i in range(n)]

    for i in range(n):
        # Jika elemen diagonal = 0, tukar baris
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    I[i], I[j] = I[j], I[i]
                    break
            else:
                raise ValueError("Matriks tidak dapat di-invers (determinannya nol).")

        diag = A[i][i]
        for j in range(n):
            A[i][j] /= diag
            I[i][j] /= diag

        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]

    return Matrix(I)
