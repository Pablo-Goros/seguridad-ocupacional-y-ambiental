#!/usr/bin/env python3
"""Extract PDF text to deterministic Markdown with explicit page boundaries."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


VISUAL_WARNING = (
    "[No extractable text; inspect the original page for visual or scanned content.]"
)
LOW_TEXT_WARNING = (
    "[Very little text was extracted; inspect the original page for visual content.]"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract searchable PDF text while preserving page numbers."
    )
    parser.add_argument("input", type=Path, help="PDF file to extract")
    parser.add_argument(
        "--output", required=True, type=Path, help="UTF-8 Markdown output path"
    )
    return parser.parse_args()


def normalize_text(text: str) -> str:
    """Normalize line endings and trailing whitespace without interpreting text."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def extract(input_path: Path, output_path: Path) -> int:
    if not input_path.is_file():
        raise ValueError(f"input PDF does not exist: {input_path}")
    if input_path.suffix.lower() != ".pdf":
        raise ValueError(f"input must be a .pdf file: {input_path}")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("input and output paths must be different")

    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "missing dependency 'pypdf'; run "
            "'python -m pip install -r requirements.txt'"
        ) from exc

    try:
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            try:
                unlocked = reader.decrypt("")
            except Exception as exc:  # pypdf exposes backend-specific errors
                raise ValueError("PDF is encrypted and cannot be read") from exc
            if not unlocked:
                raise ValueError("PDF is encrypted and requires a password")

        chunks = [f"# Extracted source: {output_path.stem}", ""]
        low_text_pages = 0
        for page_number, page in enumerate(reader.pages, start=1):
            text = normalize_text(page.extract_text() or "")
            chunks.extend([f"## Page {page_number}", ""])
            visible_characters = len(re.sub(r"\s", "", text))
            if not text:
                chunks.extend([VISUAL_WARNING, ""])
                low_text_pages += 1
            else:
                chunks.extend([text, ""])
                if visible_characters < 20:
                    chunks.extend([LOW_TEXT_WARNING, ""])
                    low_text_pages += 1
    except ValueError:
        raise
    except Exception as exc:
        raise RuntimeError(f"could not extract PDF: {exc}") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8", newline="\n")
    return low_text_pages


def main() -> int:
    args = parse_args()
    try:
        low_text_pages = extract(args.input, args.output)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Extracted {args.input} to {args.output}.")
    if low_text_pages:
        print(
            f"Warning: {low_text_pages} page(s) need visual inspection.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
