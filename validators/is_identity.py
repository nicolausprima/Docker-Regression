def is_identity(matrix):
    """
    Mengecek apakah sebuah matriks adalah matriks identitas.
    Matriks identitas adalah matriks persegi dengan:
      - semua elemen diagonal = 1
      - semua elemen non-diagonal = 0
    """
    if matrix.rows != matrix.cols:
        return False

    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if i == j: 
                if matrix.data[i][j] != 1:
                    return False
            else:      
                if matrix.data[i][j] != 0:
                    return False

    return True
