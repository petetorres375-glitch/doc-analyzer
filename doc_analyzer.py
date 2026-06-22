#!/usr/bin/env python3
"""doc_analyzer — Analyze PDF and text files using the Anthropic API."""

import argparse
import sys
from pathlib import Path

import anthropic
from rich.console import Console
from rich.panel import Panel

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

    client = anthropic.Anthropic()

    with console.status("Analyzing...", spinner="dots"):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=(
                "You are a helpful document analyst. "
                "Read the provided document content and answer the user's question clearly and concisely."
            ),
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Document: {file_path.name}\n\n"
                        f"Content:\n{text}\n\n"
                        f"Task: {prompt}"
                    ),
                }
            ],
        )

    for block in response.content:
        if block.type == "text":
            return block.text
    return ""


def main():
    parser = argparse.ArgumentParser(
        description="Analyze PDF and text files using the Anthropic API."
    )
    parser.add_argument("file", help="Path to a PDF or text file")
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Summarize this document in a few sentences.",
        help='What to do with the file (default: summarize)',
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
