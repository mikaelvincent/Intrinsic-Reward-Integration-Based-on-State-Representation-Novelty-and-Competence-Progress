"""Command-line utility for combining multiple Markdown files from a folder into a single output file.

This script scans a folder for Markdown (.md) files, parses a leading numeric prefix in their filenames (e.g., "1.2", "1.2.1", "2.1" etc.), sorts them by these numeric tokens in ascending order, and writes the concatenated contents to the file specified by --output.

Usage:
    md_combiner.py --input /path/to/md_folder --output /path/to/output.md
"""

import argparse
import os
import re
import sys
from typing import List, Tuple


def parse_section_prefix(filename: str) -> Tuple[List[int], str]:
    """Extract an initial numeric pattern (like '1.2' or '1.2.1') from the filename, converting each dot-separated segment into an integer list for sorting.

    Returns (list_of_ints, leftover_string). If no numeric prefix is found, returns ([], <basename>).
    """
    base, _ = os.path.splitext(filename)
    match = re.match(r"^([0-9]+(?:\.[0-9]+)*)(?:_|$)(.*)", base)
    if not match:
        # No numeric prefix found; return empty tokens
        return ([], base)
    numeric_part = match.group(1)
    leftover = match.group(2)
    numeric_tokens = [int(x) for x in numeric_part.split(".") if x]
    return (numeric_tokens, leftover)


def combine_markdown_files(input_dir: str, output_path: str) -> None:
    """Reads .md files in 'input_dir', sorts them by their numeric prefix, and writes concatenated contents to 'output_path'.

    Each file's content is separated by a blank line.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".md")]
    if not files:
        print(
            f"Warning: No .md files found in '{input_dir}'. Output will be empty.",
            file=sys.stderr,
        )

    parsed_files = []
    for f in files:
        tokens, leftover = parse_section_prefix(f)
        parsed_files.append((tokens, leftover, f))

    parsed_files.sort(key=lambda x: (x[0], x[1]))

    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            for tokens, leftover, filename in parsed_files:
                file_path = os.path.join(input_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as md_file:
                        outfile.write(md_file.read())
                        outfile.write("\n\n")
                except FileNotFoundError:
                    print(
                        f"Error: The file '{file_path}' does not exist.",
                        file=sys.stderr,
                    )
                except OSError as e:
                    print(f"Error reading '{file_path}': {e}", file=sys.stderr)
    except OSError as e:
        print(f"Error creating or writing to '{output_path}': {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Parse command-line arguments and combine .md files, respecting numeric prefix ordering."""
    parser = argparse.ArgumentParser(
        description="Combine multiple Markdown files into one, ordering by numeric prefixes in filenames."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the folder containing .md files."
    )
    parser.add_argument(
        "--output", required=True, help="Path to the output Markdown file."
    )
    args = parser.parse_args()

    combine_markdown_files(args.input, args.output)


if __name__ == "__main__":
    main()
