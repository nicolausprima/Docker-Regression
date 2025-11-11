from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import io
import os

from regression_app import load_and_preprocess  # pakai fungsi kamu langsung
from statsmodels.api import OLS, add_constant   # OLS untuk regresi

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
        flash("Tidak ada file yang diupload.")
        return redirect(url_for("index"))

    file = request.files["file"]
    target_column = (request.form.get("target_column") or "").strip()

    if not file or file.filename == "":
        flash("File belum dipilih.")
        return redirect(url_for("index"))
    if not target_column:
        flash("Kolom target wajib diisi.")
        return redirect(url_for("index"))

    file_path = os.path.join(UPLOAD_DIR, "uploaded.csv")
    file.save(file_path)

    try:
        # Pipeline milikmu
        X_ready, y = load_and_preprocess(file_path, target_column)

        # OLS
        X_ready_const = add_constant(X_ready)
        model = OLS(y, X_ready_const).fit()

        summary_text = model.summary().as_text()
        df_preview = pd.read_csv(file_path).head(10)

        # simpan CSV terakhir untuk tombol download
        out_buf = io.StringIO()
        df_preview.to_csv(out_buf, index=False)
        app.config["LAST_CSV_BYTES"] = out_buf.getvalue().encode("utf-8")

        return render_template(
            "index.html",
            note=f"Hasil regresi untuk kolom target '{target_column}'.",
            summary_text=summary_text,
            table_html=df_preview.to_html(classes="table", index=False),
            download_ready=True,
        )
    except Exception as e:
        flash(f"Terjadi error: {e}")
        return redirect(url_for("index"))

@app.route("/download", methods=["GET"])
def download():
    data = app.config.get("LAST_CSV_BYTES", b"Belum ada hasil. Jalankan proses dulu.")
    return send_file(
        io.BytesIO(data),
        as_attachment=True,
        download_name="result.csv",
        mimetype="text/csv",
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
