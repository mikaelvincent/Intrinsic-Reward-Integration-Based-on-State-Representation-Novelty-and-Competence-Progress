#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build"
OUTPUT_FILE = BUILD_DIR / "thesis_combined.md"


def is_section_file(path: Path) -> bool:
    return path.suffix == ".md" and path.name != OUTPUT_FILE.name and path.parent == ROOT


def rewrite_local_links(text: str) -> str:
    pattern = re.compile(r"(!?\[[^\]]*\]\()([^\)]+)(\))")

    def repl(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        trimmed = target.strip()
        if trimmed.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        if trimmed.startswith("resources/"):
            return f"{prefix}../{trimmed}{suffix}"
        return match.group(0)

    return pattern.sub(repl, text)


def main() -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    section_files = sorted(p for p in ROOT.glob("*.md") if is_section_file(p))

    chunks: list[str] = []
    for path in section_files:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        chunks.append(rewrite_local_links(content))

    OUTPUT_FILE.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} using {len(chunks)} source files.")


if __name__ == "__main__":
    main()
