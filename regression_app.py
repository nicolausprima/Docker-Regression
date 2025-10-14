import pandas as pd
from statsmodels.api import OLS, add_constant

from operations.inverse import inverse_matrix
from operations.transpose import transpose_matrix
from operations.multiplier import multiply_matrices


class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0


def load_and_preprocess(filepath, target_column):
    # Baca dataset
    df = pd.read_csv(filepath)
    print("\n=== DATA AWAL ===")
    print(df.head())

    # Pisahkan X dan y
    X = df.drop(columns=[target_column]).values.tolist()
    y = df[target_column].values.tolist()

    # Tambahkan kolom bias
    X = [[1] + row for row in X]
    X_matrix = Matrix(X)

    # Transpose dan Inverse
    X_T = transpose_matrix(X_matrix)
    XTX = multiply_matrices(X_T, X_matrix)
    XTX_inv = inverse_matrix(XTX)

    print("\n=== HASIL TRANSPOSE (Xᵀ) ===")
    for row in X_T.data[:5]:
        print(row)

    print("\n=== HASIL INVERSE (XᵀX)⁻¹ ===")
    for row in XTX_inv.data[:5]:
        print(row)

    # Transformasi akhir
    X_transformed = multiply_matrices(X_matrix, XTX_inv)
    X_ready = pd.DataFrame(X_transformed.data)
    return X_ready, y


if __name__ == "__main__":
    filepath = "data/rumah.csv"  # Ganti path dataset kamu
    target = "Harga"             # Ganti dengan kolom target

    X_ready, y = load_and_preprocess(filepath, target)

    # Regresi OLS
    X_ready_const = add_constant(X_ready)
    model = OLS(y, X_ready_const).fit()

    print("\n=== HASIL REGRESI OLS ===")
    print(model.summary())

