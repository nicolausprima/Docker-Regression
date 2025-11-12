from flask import Flask, render_template, request, flash, redirect, url_for
import os
import pandas as pd
from regression_app import run_manual_pipeline  # pakai versi manual kamu

app = Flask(__name__)
app.secret_key = "supersecret"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    try:
        # --- Ambil file upload
        if "file" not in request.files or request.files["file"].filename == "":
            flash("Harap pilih file CSV terlebih dahulu.", "danger")
            return redirect(url_for("index"))

        file = request.files["file"]
        target_column = request.form.get("target_column")

        # Simpan file ke folder uploads
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # --- Jalankan pipeline manual (tanpa statsmodels)
        df_result, coef_pairs, summary_text, debug = run_manual_pipeline(file_path, target_column)

        # Buat tabel untuk inverse dan transpose (opsional, jika mau ditampilkan)
        # Hasil dari debug dict:
        table_input = pd.read_csv(file_path).to_html(classes="table table-striped", index=False)
        table_inverse = pd.DataFrame(debug["XTX_inv"].data).to_html(classes="table table-striped", index=False)
        table_transpose = pd.DataFrame(debug["X_T"].data).to_html(classes="table table-striped", index=False)

        flash("Proses berhasil dilakukan!", "success")

        return render_template(
            "index.html",
            table_input=table_input,
            table_inverse=table_inverse,
            table_transpose=table_transpose,
            summary_text=summary_text,
            target_column=target_column,
        )

    except Exception as e:
        flash(f"Terjadi error saat proses: {e}", "danger")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

