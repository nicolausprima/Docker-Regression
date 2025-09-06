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
