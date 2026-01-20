from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from irl.visualization.style import AXIS_LABEL_FONTSIZE, DPI, LEGEND_FONTSIZE

_STYLE_RCPARAMS: dict[str, Any] = {
    "figure.dpi": int(DPI),
    "savefig.dpi": int(DPI),
    "font.size": 10,
    "axes.labelsize": int(AXIS_LABEL_FONTSIZE),
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": int(LEGEND_FONTSIZE),
    "axes.unicode_minus": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
}


def _disable_matplotlib_titles() -> None:
    import matplotlib.axes
    import matplotlib.figure

    if bool(getattr(matplotlib.axes.Axes, "_irl_titles_disabled", False)):
        return

    orig_set_title = matplotlib.axes.Axes.set_title
    orig_suptitle = matplotlib.figure.Figure.suptitle

    def _set_title_blank(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        txt = orig_set_title(self, "", pad=0.0)
        try:
            txt.set_visible(False)
        except Exception:
            pass
        return txt

    def _suptitle_blank(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        txt = orig_suptitle(self, "", y=1.0)
        try:
            txt.set_visible(False)
        except Exception:
            pass
        return txt

    matplotlib.axes.Axes.set_title = _set_title_blank  # type: ignore[assignment]
    matplotlib.figure.Figure.suptitle = _suptitle_blank  # type: ignore[assignment]
    setattr(matplotlib.axes.Axes, "_irl_titles_disabled", True)


def _patch_matplotlib_tight_layout_defaults() -> None:
    import matplotlib.figure

    if bool(getattr(matplotlib.figure.Figure, "_irl_tight_layout_patched", False)):
        return

    orig_tight_layout = matplotlib.figure.Figure.tight_layout

    def _tight_layout(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        if args:
            return orig_tight_layout(self, *args, **kwargs)

        from irl.visualization.labels import (
            LEGEND_TIGHT_LAYOUT_PAD_MULT,
            TIGHT_LAYOUT_H_PAD_MULT,
            TIGHT_LAYOUT_W_PAD_MULT,
        )

        rect = kwargs.pop("rect", None)

        h_pad_in = "h_pad" in kwargs
        w_pad_in = "w_pad" in kwargs

        pad = kwargs.pop("pad", None)
        h_pad = kwargs.pop("h_pad", None)
        w_pad = kwargs.pop("w_pad", None)

        if pad is None:
            pad = float(LEGEND_TIGHT_LAYOUT_PAD_MULT)
        try:
            pad_f = float(pad)
        except Exception:
            pad_f = float(LEGEND_TIGHT_LAYOUT_PAD_MULT)

        if not h_pad_in and h_pad is None and TIGHT_LAYOUT_H_PAD_MULT is not None:
            try:
                h_pad = float(TIGHT_LAYOUT_H_PAD_MULT)
            except Exception:
                h_pad = None

        if not w_pad_in and w_pad is None and TIGHT_LAYOUT_W_PAD_MULT is not None:
            try:
                w_pad = float(TIGHT_LAYOUT_W_PAD_MULT)
            except Exception:
                w_pad = None

        return orig_tight_layout(self, pad=pad_f, h_pad=h_pad, w_pad=w_pad, rect=rect)

    matplotlib.figure.Figure.tight_layout = _tight_layout  # type: ignore[assignment]
    setattr(matplotlib.figure.Figure, "_irl_tight_layout_patched", True)


def apply_rcparams_paper():
    import matplotlib

    try:
        matplotlib.use("Agg")
    except Exception:
        pass
    import matplotlib.pyplot as plt

    plt.rcParams.update(_STYLE_RCPARAMS)
    _disable_matplotlib_titles()
    _patch_matplotlib_tight_layout_defaults()
    return plt


_LABEL_GAP_PT: float = 2.0
_LABELPAD_MAX_PT: float = 200.0


def _has_text(t) -> bool:
    try:
        return bool(getattr(t, "get_visible")()) and bool(str(getattr(t, "get_text")()).strip())
    except Exception:
        return False


def _text_bbox(t, *, renderer):
    if not _has_text(t):
        return None
    try:
        return t.get_window_extent(renderer=renderer)
    except Exception:
        return None


def _union_bboxes(bboxes: list[object]):
    if not bboxes:
        return None
    try:
        import matplotlib.transforms as mtransforms

        return mtransforms.Bbox.union(bboxes)
    except Exception:
        return None


def _axis_ticklabel_bboxes(ax, *, which: str, renderer) -> list[object]:
    if which not in {"x", "y"}:
        return []
    axis = ax.xaxis if which == "x" else ax.yaxis

    out: list[object] = []
    try:
        ticks = list(axis.get_major_ticks())
    except Exception:
        ticks = []

    for tick in ticks:
        for lbl_name in ("label1", "label2"):
            lbl = getattr(tick, lbl_name, None)
            bb = _text_bbox(lbl, renderer=renderer)
            if bb is not None:
                out.append(bb)

    off = None
    try:
        off = axis.get_offset_text()
    except Exception:
        off = None

    bb_off = _text_bbox(off, renderer=renderer)
    if bb_off is not None:
        out.append(bb_off)

    return out


def _axis_decor_bbox(ax, *, which: str, renderer):
    return _union_bboxes(_axis_ticklabel_bboxes(ax, which=which, renderer=renderer))


def _px_to_pt(fig, px: float) -> float:
    try:
        dpi = float(getattr(fig, "dpi", float(DPI)))
    except Exception:
        dpi = float(DPI)
    if dpi <= 0.0:
        dpi = float(DPI)
    return float(px) * 72.0 / float(dpi)


def _bump_labelpad(axis, delta_pt: float) -> bool:
    try:
        cur = float(getattr(axis, "labelpad", 0.0))
    except Exception:
        cur = 0.0
    delta = float(delta_pt)
    if not (delta > 0.0):
        return False
    new = float(min(float(_LABELPAD_MAX_PT), cur + delta))
    if not (new > cur + 1e-6):
        return False
    try:
        setattr(axis, "labelpad", new)
        return True
    except Exception:
        return False


def _fix_xlabel(ax, *, fig, renderer, pad_px: float) -> bool:
    lbl = getattr(getattr(ax, "xaxis", None), "label", None)
    if not _has_text(lbl):
        return False

    try:
        lbl.set_fontsize(int(AXIS_LABEL_FONTSIZE))
    except Exception:
        pass

    try:
        lbl.set_horizontalalignment("center")
        lbl.set_x(0.5)
    except Exception:
        pass

    tick_bb = _axis_decor_bbox(ax, which="x", renderer=renderer)
    if tick_bb is None:
        return False

    try:
        lbl_bb = lbl.get_window_extent(renderer=renderer)
    except Exception:
        return False

    pos = "bottom"
    try:
        pos = str(ax.xaxis.get_label_position()).strip().lower()
    except Exception:
        pos = "bottom"

    if pos == "top":
        delta_px = float(tick_bb.y1) + float(pad_px) - float(lbl_bb.y0)
    else:
        delta_px = float(lbl_bb.y1) - (float(tick_bb.y0) - float(pad_px))

    if not (delta_px > 0.0):
        return False

    return _bump_labelpad(ax.xaxis, _px_to_pt(fig, float(delta_px)))


def _fix_ylabel(ax, *, fig, renderer, pad_px: float) -> bool:
    lbl = getattr(getattr(ax, "yaxis", None), "label", None)
    if not _has_text(lbl):
        return False

    try:
        lbl.set_fontsize(int(AXIS_LABEL_FONTSIZE))
    except Exception:
        pass

    try:
        lbl.set_verticalalignment("center")
        lbl.set_y(0.5)
    except Exception:
        pass

    tick_bb = _axis_decor_bbox(ax, which="y", renderer=renderer)
    if tick_bb is None:
        return False

    try:
        lbl_bb = lbl.get_window_extent(renderer=renderer)
    except Exception:
        return False

    pos = "left"
    try:
        pos = str(ax.yaxis.get_label_position()).strip().lower()
    except Exception:
        pos = "left"

    if pos == "right":
        delta_px = float(tick_bb.x1) + float(pad_px) - float(lbl_bb.x0)
    else:
        delta_px = float(lbl_bb.x1) - (float(tick_bb.x0) - float(pad_px))

    if not (delta_px > 0.0):
        return False

    return _bump_labelpad(ax.yaxis, _px_to_pt(fig, float(delta_px)))


def _fig_tick_bbox(fig, *, which: str, renderer):
    if which not in {"x", "y"}:
        return None
    bboxes: list[object] = []
    for ax in getattr(fig, "axes", []):
        try:
            if not bool(getattr(ax, "get_visible")()):
                continue
        except Exception:
            continue
        bboxes.extend(_axis_ticklabel_bboxes(ax, which=which, renderer=renderer))
    return _union_bboxes(bboxes)


def _fix_supxlabel(fig, *, renderer, tick_bb, pad_px: float) -> bool:
    sup = getattr(fig, "_supxlabel", None)
    if not _has_text(sup) or tick_bb is None:
        return False

    try:
        sup.set_fontsize(int(AXIS_LABEL_FONTSIZE))
    except Exception:
        pass
    try:
        sup.set_horizontalalignment("center")
        sup.set_x(0.5)
    except Exception:
        pass

    try:
        sup_bb = sup.get_window_extent(renderer=renderer)
    except Exception:
        return False

    delta_px = float(sup_bb.y1) - (float(tick_bb.y0) - float(pad_px))
    if not (delta_px > 0.0):
        return False

    try:
        fig_h = float(fig.bbox.height)
    except Exception:
        fig_h = 0.0
    if not (fig_h > 0.0):
        return False

    dy = float(delta_px) / float(fig_h)
    try:
        x0, y0 = sup.get_position()
        sup.set_position((float(x0), float(y0) - float(dy)))
        return True
    except Exception:
        return False


def _fix_supylabel(fig, *, renderer, tick_bb, pad_px: float) -> bool:
    sup = getattr(fig, "_supylabel", None)
    if not _has_text(sup) or tick_bb is None:
        return False

    try:
        sup.set_fontsize(int(AXIS_LABEL_FONTSIZE))
    except Exception:
        pass
    try:
        sup.set_verticalalignment("center")
        sup.set_y(0.5)
    except Exception:
        pass

    try:
        sup_bb = sup.get_window_extent(renderer=renderer)
    except Exception:
        return False

    delta_px = float(sup_bb.x1) - (float(tick_bb.x0) - float(pad_px))
    if not (delta_px > 0.0):
        return False

    try:
        fig_w = float(fig.bbox.width)
    except Exception:
        fig_w = 0.0
    if not (fig_w > 0.0):
        return False

    dx = float(delta_px) / float(fig_w)
    try:
        x0, y0 = sup.get_position()
        sup.set_position((float(x0) - float(dx), float(y0)))
        return True
    except Exception:
        return False


def _layout_axis_labels(fig) -> None:
    # Two passes: pad changes only apply after a redraw.
    for _ in range(2):
        try:
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()
        except Exception:
            return

        pad_px = float(getattr(fig, "dpi", float(DPI))) * float(_LABEL_GAP_PT) / 72.0

        any_change = False
        for ax in getattr(fig, "axes", []):
            try:
                if not bool(getattr(ax, "get_visible")()):
                    continue
            except Exception:
                continue
            any_change |= _fix_xlabel(ax, fig=fig, renderer=renderer, pad_px=float(pad_px))
            any_change |= _fix_ylabel(ax, fig=fig, renderer=renderer, pad_px=float(pad_px))

        xticks_bb = _fig_tick_bbox(fig, which="x", renderer=renderer)
        yticks_bb = _fig_tick_bbox(fig, which="y", renderer=renderer)

        any_change |= _fix_supxlabel(fig, renderer=renderer, tick_bb=xticks_bb, pad_px=float(pad_px))
        any_change |= _fix_supylabel(fig, renderer=renderer, tick_bb=yticks_bb, pad_px=float(pad_px))

        if not any_change:
            return


def save_fig_atomic(
    fig,
    path: Path,
    *,
    dpi: int = int(DPI),
    bbox_inches: str = "tight",
    format: str | None = None,
) -> None:
    from irl.utils.checkpoint import atomic_replace

    _layout_axis_labels(fig)

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")

    fmt = format
    if fmt is None:
        fmt = path.suffix.lstrip(".").lower() or "png"
    else:
        fmt = str(fmt).strip().lower() or (path.suffix.lstrip(".").lower() or "png")

    fig.savefig(str(tmp), dpi=int(dpi), bbox_inches=bbox_inches, format=fmt)
    atomic_replace(tmp, path)


_ENV_ORDER_BASE: tuple[str, ...] = (
    "mountaincar",
    "bipedalwalker",
    "halfcheetah",
    "ant",
    "carracing",
    "humanoid",
)
_ENV_RANK: dict[str, int] = {env: i for i, env in enumerate(_ENV_ORDER_BASE)}
_ENV_VERSION_RE = re.compile(r"-v\d+$", re.IGNORECASE)


def _env_base(env_id: str) -> str:
    s = str(env_id).strip().replace("/", "-")
    s = _ENV_VERSION_RE.sub("", s)
    return s.lower()


def env_sort_key(env_id: object) -> tuple[int, str, str]:
    s = str(env_id).strip()
    if not s:
        return (10_000, "", "")
    key = s.replace("/", "-")
    base = _env_base(key)
    rank = int(_ENV_RANK.get(base, 10_000))
    return (rank, base, key.lower())


def sort_env_ids(env_ids: Iterable[object]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for e in env_ids:
        s = str(e).strip()
        if not s or s in seen:
            continue
        out.append(s)
        seen.add(s)
    out.sort(key=env_sort_key)
    return out
