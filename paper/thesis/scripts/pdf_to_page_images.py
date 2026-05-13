#!/usr/bin/env python3
# Usage: python paper/thesis/scripts/pdf_to_page_images.py path/to/file.pdf
from __future__ import annotations

import sys
from pathlib import Path


DPI = 200
POINTS_PER_INCH = 72


def _fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def _read_pdf_path(argv: list[str]) -> Path:
    if len(argv) != 1:
        _fail("usage: pdf_to_page_images.py path/to/file.pdf")

    pdf_path = Path(argv[0]).expanduser().resolve()
    if not pdf_path.exists():
        _fail(f"PDF file does not exist: {pdf_path.as_posix()}")
    if not pdf_path.is_file():
        _fail(f"path is not a file: {pdf_path.as_posix()}")
    if pdf_path.suffix.lower() != ".pdf":
        _fail(f"expected a PDF file: {pdf_path.as_posix()}")
    return pdf_path


def _import_fitz():
    try:
        import fitz
    except ImportError:
        _fail("PyMuPDF is required. Install with: python -m pip install pymupdf")
    return fitz


def _render_pages(pdf_path: Path) -> tuple[int, Path]:
    fitz = _import_fitz()
    output_dir = pdf_path.with_suffix("")
    if output_dir.exists() and not output_dir.is_dir():
        _fail(f"output path exists and is not a directory: {output_dir.as_posix()}")

    output_dir.mkdir(parents=True, exist_ok=True)
    scale = DPI / POINTS_PER_INCH
    matrix = fitz.Matrix(scale, scale)

    with fitz.open(str(pdf_path)) as document:
        page_count = len(document)
        for page_index in range(page_count):
            page = document.load_page(page_index)
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            output_path = output_dir / f"page_{page_index + 1:03d}.png"
            pixmap.save(output_path)

    return page_count, output_dir


def main(argv: list[str]) -> int:
    pdf_path = _read_pdf_path(argv)
    page_count, output_dir = _render_pages(pdf_path)
    print(f"Converted {page_count} page(s) to {output_dir.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))