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
