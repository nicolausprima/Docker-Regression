import pandas as pd

# ==== gunakan modul kamu sendiri ====
from operations.inverse import inverse_matrix
from operations.transpose import transpose_matrix
from operations.multiplier import multiply_matrices


class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0


# ---------------------------
# Utilitas kecil
# ---------------------------
def to_column_matrix(vec):
    """list/Series -> Matrix kolom n×1"""
    return Matrix([[float(v)] for v in vec])

def matrix_to_list(M):
    """Matrix -> list of lists"""
    return [row[:] for row in M.data]

def dot_manual(a, b):
    """Dot untuk 1D list (untuk hitung SSE cepat)."""
    return sum(x*y for x, y in zip(a, b))


# ---------------------------
# Pipeline data
# ---------------------------
def load_and_preprocess(filepath, target_column):
    """
    Mengemas fitur X dan target y:
    - baca CSV
    - X = semua kolom selain target
    - tambah kolom bias (1) di paling depan
    - kembalikan Matrix(X), Matrix(y), dan nama fitur
    """
    df = pd.read_csv(filepath)

    # pastikan target ada
    if target_column not in df.columns:
        raise ValueError(f"Kolom target '{target_column}' tidak ditemukan. Kolom tersedia: {list(df.columns)}")

    # pisah X dan y
    X_df = df.drop(columns=[target_column])
    y_series = df[target_column]

    # tambah bias di depan
    X_data = X_df.values.tolist()
    X_with_bias = [[1.0] + [float(v) for v in row] for row in X_data]
    X_matrix = Matrix(X_with_bias)

    y_matrix = to_column_matrix(y_series.tolist())

    # nama fitur untuk laporan
    feature_names = ["bias"] + X_df.columns.tolist()

    # --- debug print (opsional)
    # print("\n=== DATA AWAL ===")
    # print(df.head())

    return X_matrix, y_matrix, feature_names


# ---------------------------
# Regresi linear manual
# ---------------------------
def manual_linear_regression(X: Matrix, y: Matrix):
    """
    Menghitung koefisien β = (XᵀX)^(-1) Xᵀ y
    dan mengembalikan:
      - beta (Matrix p×1)
      - y_hat (Matrix n×1)
      - metrics: dict(R2, MSE, RMSE, SSE, SST)
    """
    # Xᵀ
    X_T = transpose_matrix(X)

    # (XᵀX)
    XTX = multiply_matrices(X_T, X)

    # (XᵀX)^(-1)
    XTX_inv = inverse_matrix(XTX)

    # (Xᵀ y)
    XTy = multiply_matrices(X_T, y)

    # β
    beta = multiply_matrices(XTX_inv, XTy)  # p×1

    # y_hat = X β
    y_hat = multiply_matrices(X, beta)      # n×1

    # --- metrik
    y_list = [row[0] for row in y.data]
    yhat_list = [row[0] for row in y_hat.data]

    n = len(y_list)
    y_mean = sum(y_list) / n
    resid = [yi - yh for yi, yh in zip(y_list, yhat_list)]
    sse = dot_manual(resid, resid)                   # ∑(yi - ŷi)^2
    sst = sum((yi - y_mean)**2 for yi in y_list)     # ∑(yi - ȳ)^2
    r2 = 1.0 - (sse / sst if sst != 0 else 0.0)
    mse = sse / n if n > 0 else float("nan")
    rmse = mse ** 0.5

    metrics = {
        "R2": r2,
        "MSE": mse,
        "RMSE": rmse,
        "SSE": sse,
        "SST": sst,
        "n_obs": n,
        "p_params": X.cols
    }

    # objek tambahan untuk keperluan debugging (opsional)
    debug = {
        "X_T": X_T,
        "XTX": XTX,
        "XTX_inv": XTX_inv,
        "XTy": XTy,
    }

    return beta, y_hat, metrics, debug


# ---------------------------
# Formatter ringkasan
# ---------------------------
def format_summary(beta: Matrix, metrics: dict, feature_names):
    """
    Membuat ringkasan tekstual sederhana seperti summary OLS,
    tanpa menggunakan statsmodels.
    """
    lines = []
    lines.append("Manual Linear Regression (Normal Equation)")
    lines.append("=" * 72)
    lines.append(f"Observations (n) : {metrics['n_obs']}")
    lines.append(f"Parameters (p)   : {metrics['p_params']}")
    lines.append("-" * 72)
    lines.append(f"R-squared        : {metrics['R2']:.6f}")
    lines.append(f"MSE              : {metrics['MSE']:.6f}")
    lines.append(f"RMSE             : {metrics['RMSE']:.6f}")
    lines.append(f"SSE              : {metrics['SSE']:.6f}")
    lines.append(f"SST              : {metrics['SST']:.6f}")
    lines.append("-" * 72)
    lines.append("Coefficients:")
    lines.append("  {:>20}  {:>15}".format("Feature", "Coef (beta)"))
    lines.append("  " + "-"*39)

    betas = [row[0] for row in beta.data]
    for name, b in zip(feature_names, betas):
        lines.append(f"  {name:>20}  {b:>15.8f}")

    lines.append("=" * 72)
    return "\n".join(lines)


# ---------------------------
# API utama yang dipakai web
# ---------------------------
def run_manual_pipeline(filepath, target_column):
    """
    Fungsi sekali jalan:
      - load & tambah bias
      - hitung beta, prediksi, metrik
      - kembalikan DataFrame hasil transformasi (opsional),
        daftar koefisien, dan summary string.
    """
    X, y, feature_names = load_and_preprocess(filepath, target_column)
    beta, y_hat, metrics, debug = manual_linear_regression(X, y)

    # DataFrame hasil (X dengan kolom fitur + y_hat)
    X_df = pd.DataFrame(X.data, columns=feature_names)
    X_df["y_hat"] = [row[0] for row in y_hat.data]

    # Koefisien sebagai list of (feature, coef)
    coef_pairs = list(zip(feature_names, [row[0] for row in beta.data]))

    summary_text = format_summary(beta, metrics, feature_names)

    return X_df, coef_pairs, summary_text, debug


# ---------------------------
# CLI testing
# ---------------------------
if __name__ == "__main__":
    # Contoh pemakaian lokal (tanpa statsmodels)
    filepath = "data/rumah.csv"       # ganti sesuai file kamu
    target = "Harga"                  # ganti sesuai target

    X_df, coefs, summary, dbg = run_manual_pipeline(filepath, target)

    print("\n=== KOEFISIEN ===")
    for f, b in coefs:
        print(f"{f:>20}: {b: .6f}")

    print("\n=== RINGKASAN ===")
    print(summary)

    # Jika ingin lihat sebagian matriks debug:
    # print("\nXᵀ (top-left 5x5):")
    # for row in dbg["X_T"].data[:5]:
    #     print(row[:5])
