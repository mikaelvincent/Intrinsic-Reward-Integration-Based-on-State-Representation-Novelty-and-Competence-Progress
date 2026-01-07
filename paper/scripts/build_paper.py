#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SUPPORTED_TARGETS: tuple[str, ...] = ("neurips", "icml", "iclr", "arxiv")

REQUIRED_TEMPLATE_FILES: dict[str, tuple[Path, ...]] = {
    "neurips": (Path("templates/neurips/neurips_2023.sty"),),
    "icml": (
        Path("templates/icml/icml2024.sty"),
        Path("templates/icml/icml2024.bst"),
    ),
    "iclr": (
        Path("templates/iclr/iclr2024_conference.sty"),
        Path("templates/iclr/iclr2024_conference.bst"),
    ),
    "arxiv": (),
}

STAGED_ROOT_ITEMS: tuple[str, ...] = (
    "content.tex",
    "content_body.tex",
    "sections",
    "figures",
    "tables",
    "references",
)


def _paper_dir() -> Path:
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


def _require_templates(paper_dir: Path, target: str) -> None:
    missing: list[Path] = []
    for rel in REQUIRED_TEMPLATE_FILES.get(target, ()):
        if not (paper_dir / rel).exists():
            missing.append(rel)

    if not missing:
        return

    lines = [
        f"missing template files for target '{target}':",
        *(f"  - {p.as_posix()}" for p in missing),
        "",
        "Place the official conference template files under:",
        f"  { (paper_dir / 'templates' / target).as_posix() }/",
    ]
    _fail("\n".join(lines))


def _latexmk_flags(engine: str) -> list[str]:
    if engine == "pdflatex":
        return ["-pdf"]
    if engine == "xelatex":
        return ["-xelatex"]
    if engine == "lualatex":
        return ["-lualatex"]
    _fail(f"unsupported engine: {engine}")
    return []


def _run_latexmk(
    latexmk: str,
    paper_dir: Path,
    target: str,
    engine: str,
    out_dir: Path,
) -> None:
    target_tex = paper_dir / "targets" / f"{target}.tex"
    if not target_tex.exists():
        _fail(f"missing target wrapper: {target_tex.as_posix()}")

    out_dir_rel = out_dir.relative_to(paper_dir).as_posix()
    target_tex_rel = target_tex.relative_to(paper_dir).as_posix()

    cmd = [
        latexmk,
        *_latexmk_flags(engine),
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={out_dir_rel}",
        target_tex_rel,
    ]
    subprocess.run(cmd, cwd=str(paper_dir), check=True)


def _stage_sources(paper_dir: Path, target: str, build_dir: Path) -> None:
    latex_dir = build_dir / "latex"
    _rm_tree(latex_dir)
    latex_dir.mkdir(parents=True, exist_ok=True)

    wrapper_src = paper_dir / "targets" / f"{target}.tex"
    _copy_file(wrapper_src, latex_dir / "main.tex")

    for name in STAGED_ROOT_ITEMS:
        src = paper_dir / name
        if not src.exists():
            continue
        if src.is_dir():
            _copy_tree(src, latex_dir / name)
        else:
            _copy_file(src, latex_dir / name)

    tmpl_src = paper_dir / "templates" / target
    if tmpl_src.exists():
        _copy_tree(tmpl_src, latex_dir / "templates" / target)


def _build_one(
    latexmk: str,
    paper_dir: Path,
    target: str,
    engine: str,
    clean: bool,
    stage: bool,
) -> None:
    build_dir = paper_dir / "build" / target
    out_dir = build_dir / "out"

    if clean:
        _rm_tree(build_dir)

    build_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    _require_templates(paper_dir, target)
    _run_latexmk(latexmk, paper_dir, target, engine, out_dir)

    pdf_src = out_dir / f"{target}.pdf"
    if not pdf_src.exists():
        _fail(f"expected PDF not found: {pdf_src.as_posix()}")

    _copy_file(pdf_src, build_dir / "paper.pdf")

    if stage:
        _stage_sources(paper_dir, target, build_dir)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="build_paper.py",
        description="Build the paper into common ML publication formats.",
        epilog=(
            "Targets:\n"
            "  neurips  -> requires templates/neurips/neurips_2023.sty\n"
            "  icml     -> requires templates/icml/icml2024.sty + icml2024.bst\n"
            "  iclr     -> requires templates/iclr/iclr2024_conference.sty + .bst\n"
            "  arxiv    -> no template files required\n\n"
            "Outputs:\n"
            "  paper/build/<target>/paper.pdf\n"
            "  paper/build/<target>/latex/  (self-contained sources)\n\n"
            "Prerequisites:\n"
            "  - A TeX distribution (TeX Live recommended)\n"
            "  - latexmk on PATH\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help=f"Build targets: {', '.join(SUPPORTED_TARGETS)}",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build all supported targets.",
    )
    parser.add_argument(
        "--engine",
        choices=("pdflatex", "xelatex", "lualatex"),
        default="pdflatex",
        help="LaTeX engine used by latexmk.",
    )
    parser.add_argument(
        "--latexmk",
        default="latexmk",
        help="latexmk executable name or path.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing build/<target>/ before building.",
    )
    parser.add_argument(
        "--no-stage",
        action="store_true",
        help="Skip staging build/<target>/latex/ sources.",
    )

    args = parser.parse_args(argv)

    if args.all:
        targets = list(SUPPORTED_TARGETS)
    else:
        targets = args.targets

    if not targets:
        parser.print_help(sys.stderr)
        return 2

    unknown = [t for t in targets if t not in SUPPORTED_TARGETS]
    if unknown:
        _fail(f"unknown targets: {', '.join(unknown)}")

    paper_dir = _paper_dir()
    latexmk = _check_tool(args.latexmk)

    for t in targets:
        _build_one(
            latexmk=latexmk,
            paper_dir=paper_dir,
            target=t,
            engine=args.engine,
            clean=args.clean,
            stage=not args.no_stage,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
