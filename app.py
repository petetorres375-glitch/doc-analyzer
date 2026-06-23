import os
import tempfile
import uuid
from io import BytesIO
from pathlib import Path

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from doc_analyzer import analyze, save_report

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-in-prod")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}
_report_store: dict = {}


def allowed_ext(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html", error=None)


@app.route("/analyze", methods=["POST"])
def analyze_file():
    def err(msg):
        return render_template("index.html", error=msg)

    f = request.files.get("file")
    if not f or f.filename == "":
        return err("Please select a file.")

    if not allowed_ext(f.filename):
        return err("Unsupported file type. Upload a PDF, TXT, or MD file.")

    filename = secure_filename(f.filename)

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / filename
            f.save(str(input_path))
            result = analyze(input_path)
            report_path = save_report(input_path, result)
            pdf_bytes = report_path.read_bytes()
    except SystemExit:
        return err("Analysis failed. Check that your file contains readable text and your API key is valid.")
    except Exception as e:
        return err(f"Unexpected error: {e}")

    report_id = str(uuid.uuid4())
    _report_store[report_id] = {
        "pdf": pdf_bytes,
        "name": f"{Path(filename).stem}_report.pdf",
    }

    return render_template("results.html", filename=filename, result=result, report_id=report_id)


@app.route("/download/<report_id>")
def download(report_id):
    entry = _report_store.get(report_id)
    if not entry:
        return "Report not found or expired.", 404
    return send_file(
        BytesIO(entry["pdf"]),
        download_name=entry["name"],
        as_attachment=True,
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
