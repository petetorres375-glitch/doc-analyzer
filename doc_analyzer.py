#!/usr/bin/env python3
"""doc_analyzer — Analyze PDF and text files using the Gemini API."""

import argparse
import json
import os
import sys
from pathlib import Path

from google import genai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()

console = Console()

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}

SYSTEM_PROMPT = """\
You are a helpful document analyst. Analyze the provided document and return a JSON object with exactly these four keys:
- "summary": A 2-3 sentence overview of the document.
- "key_data_points": A list of important names, dates, amounts, or figures as bullet points.
- "action_items": A list of tasks, deadlines, or next steps. If none, return ["None identified."].
- "red_flags": A list of concerns, risks, or missing information. If none, return ["None identified."].

Return only valid JSON. No markdown fences, no extra text.
"""


def read_file(path: Path) -> str:
    if path.suffix == ".pdf":
        return read_pdf(path)
    return path.read_text(encoding="utf-8")


def read_pdf(path: Path) -> str:
    try:
        import fitz
    except ImportError:
        console.print("[red]PyMuPDF not installed. Run: pip install pymupdf[/red]")
        sys.exit(1)

    doc = fitz.open(str(path))
    return "\n".join(page.get_text() for page in doc)


def analyze(file_path: Path) -> dict:
    text = read_file(file_path)
    if not text.strip():
        console.print("[red]Could not extract any text from the file.[/red]")
        sys.exit(1)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]GEMINI_API_KEY not set in .env[/red]")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    full_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Document: {file_path.name}\n\n"
        f"Content:\n{text}"
    )

    with console.status("Analyzing...", spinner="dots"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )

    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(raw)


def print_section(title: str, content, border_style: str) -> None:
    if isinstance(content, list):
        body = "\n".join(f"• {item}" for item in content)
    else:
        body = content
    console.print(Panel(body, title=f"[bold]{title}[/bold]", border_style=border_style))


def main():
    parser = argparse.ArgumentParser(
        description="Analyze PDF and text files using the Gemini API."
    )
    parser.add_argument("file", help="Path to a PDF or text file")
    args = parser.parse_args()

    path = Path(args.file)

    if not path.exists():
        console.print(f"[red]File not found: {path}[/red]")
        sys.exit(1)

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        console.print(
            f"[red]Unsupported file type '{path.suffix}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}[/red]"
        )
        sys.exit(1)

    console.print(Panel(f"[bold]{path.name}[/bold]", title="doc_analyzer"))

    result = analyze(path)

    print_section("Summary", result.get("summary", ""), "cyan")
    print_section("Key Data Points", result.get("key_data_points", []), "blue")
    print_section("Action Items", result.get("action_items", []), "yellow")
    print_section("Red Flags", result.get("red_flags", []), "red")


if __name__ == "__main__":
    main()
