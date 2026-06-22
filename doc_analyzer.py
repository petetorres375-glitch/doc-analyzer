#!/usr/bin/env python3
"""doc_analyzer — Analyze PDF and text files using the Gemini API."""

import argparse
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


def read_file(path: Path) -> str:
    if path.suffix == ".pdf":
        return read_pdf(path)
    return path.read_text(encoding="utf-8")


def read_pdf(path: Path) -> str:
    try:
        import PyPDF2
    except ImportError:
        console.print("[red]PyPDF2 not installed. Run: pip install pypdf2[/red]")
        sys.exit(1)

    text_parts = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def analyze(file_path: Path, prompt: str) -> str:
    text = read_file(file_path)
    if not text.strip():
        return "Could not extract any text from the file."

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]GEMINI_API_KEY not set in .env[/red]")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    full_prompt = (
        f"You are a helpful document analyst. "
        f"Read the provided document content and answer the user's question clearly and concisely.\n\n"
        f"Document: {file_path.name}\n\n"
        f"Content:\n{text}\n\n"
        f"Task: {prompt}"
    )

    with console.status("Analyzing...", spinner="dots"):
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=full_prompt,
        )

    return response.text


def main():
    parser = argparse.ArgumentParser(
        description="Analyze PDF and text files using the Gemini API."
    )
    parser.add_argument("file", help="Path to a PDF or text file")
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Summarize this document in a few sentences.",
        help="What to do with the file (default: summarize)",
    )
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

    console.print(Panel(f"[bold]{path.name}[/bold]\n{args.prompt}", title="doc_analyzer"))

    result = analyze(path, args.prompt)
    console.print(Panel(result, title="Result", border_style="green"))


if __name__ == "__main__":
    main()
