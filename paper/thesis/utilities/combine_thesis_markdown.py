#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build"
OUTPUT_FILE = BUILD_DIR / "thesis_combined.md"
BIBLIOGRAPHY_FILE = ROOT / "07_00_bibliography.md"


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


def load_parenthetical_citations(bib_path: Path) -> dict[int, str]:
    text = bib_path.read_text(encoding="utf-8")
    pattern = re.compile(r"^\[(\d+)\]\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    citations: dict[int, str] = {}

    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        paren_matches = re.findall(r"^\(([^\n]+)\)\s*$", block, flags=re.MULTILINE)
        if paren_matches:
            citations[int(match.group(1))] = f"({paren_matches[-1].strip()})"

    return citations


def expand_citation_token(token: str) -> list[int]:
    token = token.strip()
    if not token:
        return []
    if "-" in token:
        left, right = token.split("-", 1)
        if left.strip().isdigit() and right.strip().isdigit():
            a, b = int(left.strip()), int(right.strip())
            lo, hi = min(a, b), max(a, b)
            return list(range(lo, hi + 1))
    return [int(token)] if token.isdigit() else []


def rewrite_numbered_citations(text: str, citation_map: dict[int, str]) -> str:
    pattern = re.compile(r"\{\{CIT:([0-9,\-\s]+)\}\}|\[([0-9,\-\s]+)\]")

    def repl(match: re.Match[str]) -> str:
        raw = match.group(1) or match.group(2)
        ids: list[int] = []
        for token in raw.split(","):
            ids.extend(expand_citation_token(token))

        seen: set[int] = set()
        ordered_ids: list[int] = []
        for cid in ids:
            if cid not in seen:
                ordered_ids.append(cid)
                seen.add(cid)

        mapped = [citation_map[cid] for cid in ordered_ids if cid in citation_map]
        if not mapped:
            return match.group(0)
        if len(mapped) == 1:
            return mapped[0]
        return "(" + "; ".join(m.strip("()") for m in mapped) + ")"

    return pattern.sub(repl, text)


def main() -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    citation_map = load_parenthetical_citations(BIBLIOGRAPHY_FILE)

    section_files = sorted(p for p in ROOT.glob("*.md") if is_section_file(p))

    chunks: list[str] = []
    for path in section_files:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        rewritten = rewrite_local_links(content)
        rewritten = rewrite_numbered_citations(rewritten, citation_map)
        chunks.append(rewritten)

    OUTPUT_FILE.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} using {len(chunks)} source files.")


if __name__ == "__main__":
    main()
