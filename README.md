# doc_analyzer

A Python tool that analyzes PDF and text files using the Gemini API. Returns a structured breakdown with four labeled sections. Runs as a web app or from the command line — both modes generate a downloadable report.

**No data retention** — uploaded files are deleted from the server immediately after analysis. Nothing is stored between requests.

## Output

- **Summary** — 2-3 sentence overview of the document
- **Key Data Points** — names, dates, dollar amounts, and important figures
- **Action Items** — tasks, deadlines, and next steps
- **Red Flags** — concerns, risks, or missing information

## Requirements

- Python 3.12+
- A free Gemini API key from [aistudio.google.com](https://aistudio.google.com)

## Setup

```bash
git clone https://github.com/petetorres375-glitch/doc-analyzer.git
cd doc-analyzer

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your Gemini API key
```

## Usage

**Web app:**

```bash
python app.py
```

Open `http://localhost:5000`, upload a file, and view results in the browser. Download the report as a PDF or TXT file directly from the results page. The uploaded file is deleted from the server as soon as the analysis completes.

**CLI:**

```bash
python doc_analyzer.py path/to/file.pdf
python doc_analyzer.py path/to/file.txt
python doc_analyzer.py path/to/notes.md
```

Supports `.pdf`, `.txt`, and `.md` files. PDF text is extracted using PyMuPDF.

## Example

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

## Model

Uses `gemini-2.5-flash` as the primary model. Automatically falls back to `gemini-2.5-flash-lite` on a 503 (model overload) before giving up.

## Live Demo

[https://web-production-b4dc1.up.railway.app/](https://web-production-b4dc1.up.railway.app/)

## Deploy to Railway

1. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
2. Select this repository
3. Add environment variables: `GEMINI_API_KEY` and `SECRET_KEY`
4. Railway detects the `Procfile` and deploys automatically
