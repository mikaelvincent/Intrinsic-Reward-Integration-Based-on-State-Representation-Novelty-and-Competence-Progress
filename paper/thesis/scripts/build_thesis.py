#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


STAGED_ROOT_ITEMS: tuple[str, ...] = (
    "main.tex",
    "latex_utilities.tex",
    "references",
)


def _thesis_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _fail(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(2)


def _check_tool(name: str) -> str:
    resolved = shutil.which(name)
    if not resolved:
        _fail(f"required tool not found on PATH: {name}")
    return resolved


def _rm_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def _copy_tree(src: Path, dst: Path) -> None:
    _rm_tree(dst)
    shutil.copytree(src, dst, copy_function=shutil.copy2)


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _latexmk_flags(engine: str) -> list[str]:
    if engine == "pdflatex":
        return ["-pdf"]
    if engine == "xelatex":
        return ["-xelatex"]
    if engine == "lualatex":
        return ["-lualatex"]
    _fail(f"unsupported engine: {engine}")
    return []


def _run_latexmk(latexmk: str, thesis_dir: Path, engine: str, out_dir: Path) -> None:
    main_tex = thesis_dir / "main.tex"
    if not main_tex.exists():
        _fail(f"missing thesis wrapper: {main_tex.as_posix()}")

    out_dir_rel = out_dir.relative_to(thesis_dir).as_posix()
    cmd = [
        latexmk,
        *_latexmk_flags(engine),
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={out_dir_rel}",
        "main.tex",
    ]
    res = subprocess.run(cmd, cwd=str(thesis_dir), check=False)
    if res.returncode != 0:
        log_path = (out_dir / "main.log").resolve()
        _fail(
            "\n".join(
                [
                    f"latexmk failed for thesis build (exit code {res.returncode})",
                    f"see log: {log_path}",
                ]
            )
        )


def _stage_sources(thesis_dir: Path, build_dir: Path) -> None:
    latex_dir = build_dir / "latex"
    _rm_tree(latex_dir)
    latex_dir.mkdir(parents=True, exist_ok=True)

    for name in STAGED_ROOT_ITEMS:
        src = thesis_dir / name
        if not src.exists():
            continue
        if src.is_dir():
            _copy_tree(src, latex_dir / name)
        else:
            _copy_file(src, latex_dir / name)


def _build(latexmk: str, thesis_dir: Path, engine: str, clean: bool, stage: bool) -> None:
    build_dir = thesis_dir / "build"
    out_dir = build_dir / "out"

    if clean:
        _rm_tree(build_dir)

    build_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    _run_latexmk(latexmk, thesis_dir, engine, out_dir)

    pdf_src = out_dir / "main.pdf"
    if not pdf_src.exists():
        _fail(f"expected PDF not found: {pdf_src.as_posix()}")

    _copy_file(pdf_src, build_dir / "thesis.pdf")

    if stage:
        _stage_sources(thesis_dir, build_dir)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="build_thesis.py")
    parser.add_argument(
        "--engine",
        choices=("pdflatex", "xelatex", "lualatex"),
        default="pdflatex",
    )
    parser.add_argument("--latexmk", default="latexmk")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--no-stage", action="store_true")
    args = parser.parse_args(argv)

    _build(
        latexmk=_check_tool(args.latexmk),
        thesis_dir=_thesis_dir(),
        engine=args.engine,
        clean=args.clean,
        stage=not args.no_stage,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))