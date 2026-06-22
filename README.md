# doc_analyzer

A Python CLI tool that analyzes PDF and text files using the Gemini API. Returns a structured breakdown with four labeled sections displayed as color-coded panels in the terminal.

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
# Clone the repo
git clone https://github.com/petetorres375-glitch/doc-analyzer.git
cd doc-analyzer

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
cp .env.example .env
# Edit .env and paste your key
```

## Usage

```bash
python doc_analyzer.py path/to/file.txt
python doc_analyzer.py path/to/document.pdf
python doc_analyzer.py path/to/notes.md
```

Supports `.txt`, `.pdf`, and `.md` files. PDF text is extracted using PyMuPDF (fitz).

## Model

Uses `gemini-2.5-flash` via the [Google GenAI Python SDK](https://github.com/google-gemini/generative-ai-python).

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
