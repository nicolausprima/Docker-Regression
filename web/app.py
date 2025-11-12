from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import numpy as np
import io
import os

from regression_app import load_and_preprocess
from statsmodels.api import OLS, add_constant

# ==== fungsi matriks dari library kamu (fallback kalau tidak ada) ====
try:
    from operations.inverse import inverse_matrix
except Exception:
    inverse_matrix = lambda M: np.linalg.inv(np.asarray(getattr(M, "data", M)))

try:
    from operations.transpose import transpose_matrix
except Exception:
    transpose_matrix = lambda M: np.asarray(getattr(M, "data", M)).T

# ==== dukungan class Matrix buatanmu (opsional) ====
try:
    from matrix import Matrix
except Exception:
    Matrix = None

def to_matrix_obj(df: pd.DataFrame):
    return Matrix(df.values.tolist()) if Matrix is not None else df.values

def from_matrix_obj(M) -> pd.DataFrame:
    data = getattr(M, "data", M)
    return pd.DataFrame(np.asarray(data))

# ==== Flask app ====
app = Flask(__name__)
app.secret_key = "change_this_secret"
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    if "file" not in request.files:
        flash("Tidak ada file yang diupload.", "warning")
        return redirect(url_for("index"))

    file = request.files["file"]
    target_column = (request.form.get("target_column") or "").strip()

    if not file or file.filename == "":
        flash("File belum dipilih.", "warning")
        return redirect(url_for("index"))
    if not target_column:
        flash("Kolom target wajib diisi.", "warning")
        return redirect(url_for("index"))

    src_path = os.path.join(UPLOAD_DIR, "uploaded.csv")
    file.save(src_path)

    try:
        df_input = pd.read_csv(src_path)
    except Exception as e:
        flash(f"Gagal membaca CSV: {e}", "danger")
        return redirect(url_for("index"))

    try:
        # Simpan nama kolom asli untuk dipulihkan setelah transformasi
        orig_cols = df_input.columns.tolist()

        # 1) INVERSE
        if df_input.shape[0] != df_input.shape[1]:
            flash("Inverse butuh matriks persegi. File tidak persegi — langkah inverse dilewati.", "warning")
            df_inv = df_input.copy()
        else:
            Min = inverse_matrix(to_matrix_obj(df_input))
            df_inv = from_matrix_obj(Min)
            # pulihkan nama kolom jika shape cocok
            if df_inv.shape[1] == len(orig_cols):
                df_inv.columns = orig_cols

        # 2) TRANSPOSE
        MT = transpose_matrix(to_matrix_obj(df_inv))
        df_trans = from_matrix_obj(MT)
        # untuk matriks persegi, jumlah kolom tetap sama → pulihkan header
        if df_trans.shape[1] == len(orig_cols):
            df_trans.columns = orig_cols

        # Pastikan target benar-benar ada; jika tidak, pakai kolom terakhir
        if target_column not in df_trans.columns:
            cols_list = ", ".join(map(str, df_trans.columns.tolist()))
            flash(f"Target '{target_column}' tidak ditemukan. Kolom tersedia: {cols_list}. "
                  f"Menggunakan kolom terakhir sebagai target.", "warning")
            target_column = df_trans.columns[-1]

        # 3) REGRESSION (pakai pipeline kamu)
        proc_path = os.path.join(UPLOAD_DIR, "processed.csv")
        df_trans.to_csv(proc_path, index=False)

        X_ready, y = load_and_preprocess(proc_path, target_column)
        X_const = add_constant(X_ready)
        model = OLS(y, X_const).fit()
        summary_text = model.summary().as_text()

        # Tabel preview
        table_input = df_input.head(10).to_html(classes="table table-striped mb-0", index=False)
        table_inverse = df_inv.head(10).to_html(classes="table table-striped mb-0", index=False)
        table_transpose = df_trans.head(10).to_html(classes="table table-striped mb-0", index=False)

        # File unduhan (hasil setelah transpose)
        out_buf = io.StringIO()
        df_trans.to_csv(out_buf, index=False)
        app.config["LAST_CSV_BYTES"] = out_buf.getvalue().encode("utf-8")

        return render_template(
            "index.html",
            table_input=table_input,
            table_inverse=table_inverse,
            table_transpose=table_transpose,
            summary_text=summary_text,
            target_column=target_column,
            download_ready=True,
        )

    except Exception as e:
        flash(f"Terjadi error saat proses: {e}", "danger")
        return redirect(url_for("index"))

@app.route("/download")
def download():
    data = app.config.get("LAST_CSV_BYTES")
    if data is None:
        data = b"Belum ada hasil untuk diunduh. Jalankan proses dulu."
    return send_file(io.BytesIO(data), as_attachment=True,
                     download_name="result.csv", mimetype="text/csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

