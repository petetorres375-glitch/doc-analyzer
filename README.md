# doc_analyzer

A document analysis tool powered by the Gemini API. Upload a PDF, TXT, or MD file and get a structured breakdown across four sections. Available as both a web app and a CLI.

## Output

- **Summary** — 2-3 sentence overview of the document
- **Key Data Points** — names, dates, dollar amounts, and important figures
- **Action Items** — tasks, deadlines, and next steps
- **Red Flags** — concerns, risks, or missing information

Results are displayed in the browser (web) or as color-coded terminal panels (CLI). Both modes generate a downloadable PDF report.

---

## Web App

### Deploy to Railway

1. Fork or clone this repo and push to GitHub
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
3. Select this repository
4. Under **Variables**, add:
   - `GEMINI_API_KEY` — your key from [aistudio.google.com](https://aistudio.google.com)
   - `SECRET_KEY` — any random string (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`)
5. Railway auto-detects the `Procfile` and deploys

### Run locally

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
python app.py
```

Open `http://localhost:5000` in your browser.

---

## CLI

### Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Usage

```bash
python doc_analyzer.py path/to/file.txt
python doc_analyzer.py path/to/document.pdf
python doc_analyzer.py path/to/notes.md
```

Supports `.txt`, `.pdf`, and `.md` files. PDF text is extracted using PyMuPDF.

### Example output

```
python doc_analyzer.py sample_docs/sample_invoice.txt
```

```
╭─────────────────── Summary ───────────────────╮
│ This invoice from Torres Tech Solutions to... │
╰───────────────────────────────────────────────╯
╭─────────────────── Key Data Points ───────────╮
│ • Invoice Number: INV-2026-0481               │
│ • Due Date: July 15, 2026                     │
│ • Total Due: $1,300.00                        │
╰───────────────────────────────────────────────╯
╭─────────────────── Action Items ──────────────╮
│ • Pay $1,300.00 by July 15, 2026.             │
╰───────────────────────────────────────────────╯
╭─────────────────── Red Flags ─────────────────╮
│ • No explicit tax rate mentioned.             │
╰───────────────────────────────────────────────╯
```

---

## Requirements

- Python 3.12+
- A free Gemini API key from [aistudio.google.com](https://aistudio.google.com)

## Model

Uses `gemini-2.5-flash` via the [Google GenAI Python SDK](https://github.com/google-gemini/generative-ai-python). Automatically falls back to `gemini-2.5-flash-lite` on a 503 before giving up.
