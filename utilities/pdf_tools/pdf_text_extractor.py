"""Command-line utility for extracting text from a PDF file.

This script reads a PDF file specified by the --input argument, extracts all text from each page, and writes the combined text to the file specified by the --output argument.

Usage:
    pdf_text_extractor.py --input /path/to/input.pdf --output /path/to/output.txt
"""

import argparse
import sys
import PyPDF2


def extract_text_from_pdf(input_path: str, output_path: str) -> None:
    """Extract all text from the specified PDF file and write it to a text file.

    Args:
        input_path: The path to the source PDF file.
        output_path: The path to the output text file.
    """
    try:
        with open(input_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)

            with open(output_path, "w", encoding="utf-8") as txt_file:
                for page in reader.pages:
                    text = page.extract_text() or ""
                    txt_file.write(text)
                    txt_file.write("\n")

    except FileNotFoundError:
        print(f"Error: The file '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    except PyPDF2.errors.PdfReadError:
        print(f"Error: Failed to read the PDF file '{input_path}'.", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Parse command-line arguments and extract text from the input PDF to the output file."""
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file and write it to a text file."
    )
    parser.add_argument("--input", required=True, help="Path to the input PDF file.")
    parser.add_argument("--output", required=True, help="Path to the output text file.")
    args = parser.parse_args()

    extract_text_from_pdf(args.input, args.output)


if __name__ == "__main__":
    main()
