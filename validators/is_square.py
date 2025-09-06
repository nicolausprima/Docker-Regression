def is_square(matrix):
    """
    Mengecek apakah sebuah matriks berbentuk persegi.
    """
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise TypeError("Matrix harus berupa list of lists.")

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    return rows == cols
