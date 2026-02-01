from __future__ import annotations

import math
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from . import style as _style
from irl.visualization.style import AXIS_LABEL_FONTSIZE, DPI, LEGEND_FONTSIZE, scale_plot_height

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

_WRAPPED_SUBPLOTS_ATTR: str = "_irl_wrapped_subplots"


def _is_ax_visible(ax: object) -> bool:
    try:
        return bool(getattr(ax, "get_visible")())
    except Exception:
        return False


def _axes_x_span(axes: Iterable[object]) -> tuple[float, float] | None:
    x0s: list[float] = []
    x1s: list[float] = []
    for ax in axes:
        try:
            pos = getattr(ax, "get_position")()
        except Exception:
            continue
        try:
            x0 = float(getattr(pos, "x0"))
            x1 = float(getattr(pos, "x1"))
        except Exception:
            continue
        if not (math.isfinite(x0) and math.isfinite(x1) and x1 > x0):
            continue
        x0s.append(x0)
        x1s.append(x1)
    if not x0s:
        return None
    return float(min(x0s)), float(max(x1s))


def _twinned_siblings(ax: object) -> list[object]:
    tw = getattr(ax, "_twinned_axes", None)
    if tw is None:
        return [ax]
    try:
        sib = list(tw.get_siblings(ax))
    except Exception:
        return [ax]
    return sib if sib else [ax]


def _shift_axes_x(axes: Iterable[object], dx: float) -> None:
    d = float(dx)
    if not (math.isfinite(d) and abs(d) > 1e-12):
        return

    for ax in axes:
        try:
            pos = getattr(ax, "get_position")()
            x0 = float(getattr(pos, "x0")) + d
            y0 = float(getattr(pos, "y0"))
            w = float(getattr(pos, "width"))
            h = float(getattr(pos, "height"))
        except Exception:
            continue

        if not all(math.isfinite(v) for v in (x0, y0, w, h)):
            continue

        try:
            getattr(ax, "set_position")([float(x0), float(y0), float(w), float(h)])
        except Exception:
            continue


def _center_wrapped_subplot_rows(fig) -> None:
    spec = getattr(fig, _WRAPPED_SUBPLOTS_ATTR, None)
    if not isinstance(spec, dict):
        return

    try:
        grid_cols = int(spec.get("grid_cols", 0))
        grid_rows = int(spec.get("grid_rows", 0))
        n_used = int(spec.get("n_used", 0))
    except Exception:
        return

    axes = spec.get("axes")
    if grid_cols <= 1 or grid_rows <= 0 or n_used <= 0:
        return
    if not isinstance(axes, (list, tuple)) or not axes:
        return

    axes_list = list(axes)
    total = int(grid_rows) * int(grid_cols)
    if total <= 0 or len(axes_list) < int(grid_cols):
        return
    axes_list = axes_list[: int(min(total, len(axes_list)))]

    ref = _axes_x_span(axes_list[: int(grid_cols)])
    if ref is None:
        return

    grid_left, grid_right = ref
    full_w = float(grid_right - grid_left)
    if not (math.isfinite(full_w) and full_w > 0.0):
        return

    for r in range(int(grid_rows)):
        start = int(r) * int(grid_cols)
        used_in_row = int(max(0, min(int(grid_cols), int(n_used) - int(start))))
        if used_in_row <= 0 or used_in_row >= int(grid_cols):
            continue

        group = axes_list[start : start + used_in_row]
        group_vis = [ax for ax in group if _is_ax_visible(ax)]
        if not group_vis:
            continue

        group_span = _axes_x_span(group_vis)
        if group_span is None:
            continue

        group_left, group_right = group_span
        group_w = float(group_right - group_left)
        if not (math.isfinite(group_w) and group_w > 0.0 and full_w > group_w + 1e-12):
            continue

        target_left = float(grid_left) + 0.5 * float(full_w - group_w)
        dx = float(target_left - float(group_left))
        if not (math.isfinite(dx) and abs(dx) > 1e-8):
            continue

        # Axes.set_position propagates to twinned siblings; shifting both doubles the offset.
        _shift_axes_x(set(group_vis), float(dx))


def _apply_subplot_spacing(fig) -> None:
    wspace = getattr(_style, "SUBPLOT_WSPACE", None)
    hspace = getattr(_style, "SUBPLOT_HSPACE", None)
    if wspace is None and hspace is None:
        return

    kwargs: dict[str, float] = {}

    if wspace is not None:
        try:
            w = float(wspace)
        except Exception:
            w = float("nan")
        if math.isfinite(w) and w >= 0.0:
            kwargs["wspace"] = float(w)

    if hspace is not None:
        try:
            h = float(hspace)
        except Exception:
            h = float("nan")
        if math.isfinite(h) and h >= 0.0:
            kwargs["hspace"] = float(h)

    if not kwargs:
        return

    try:
        fig.subplots_adjust(**kwargs)
    except Exception:
        return


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


def _patch_matplotlib_supylabel() -> None:
    import matplotlib.figure

    if bool(getattr(matplotlib.figure.Figure, "_irl_supylabel_patched", False)):
        return

    orig_supylabel = matplotlib.figure.Figure.supylabel

    def _supylabel(self, t, *args, **kwargs):  # type: ignore[no-untyped-def]
        axes = [ax for ax in getattr(self, "axes", []) if _is_ax_visible(ax)]
        left_axes: list[object] = []
        for ax in axes:
            try:
                pos = str(getattr(ax, "yaxis").get_label_position()).strip().lower()
            except Exception:
                pos = "left"
            if pos == "right":
                continue
            left_axes.append(ax)

        if int(len(left_axes)) > 1:
            label = str(t) if t is not None else ""
            if label:
                for ax in left_axes:
                    try:
                        ax.set_ylabel(label)
                    except Exception:
                        continue

            txt = orig_supylabel(self, "", *args, **kwargs)
            try:
                txt.set_visible(False)
            except Exception:
                pass
            return txt

        return orig_supylabel(self, t, *args, **kwargs)

    matplotlib.figure.Figure.supylabel = _supylabel  # type: ignore[assignment]
    setattr(matplotlib.figure.Figure, "_irl_supylabel_patched", True)


def _patch_matplotlib_tight_layout_defaults() -> None:
    import matplotlib.figure

    if bool(getattr(matplotlib.figure.Figure, "_irl_tight_layout_patched", False)):
        return

    orig_tight_layout = matplotlib.figure.Figure.tight_layout

    def _tight_layout(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        if args:
            out = orig_tight_layout(self, *args, **kwargs)
            _apply_subplot_spacing(self)
            _center_wrapped_subplot_rows(self)
            return out

        from irl.visualization.labels import (
            LEGEND_TIGHT_LAYOUT_PAD_MULT,
            TIGHT_LAYOUT_H_PAD_MULT as _LABEL_TIGHT_LAYOUT_H_PAD_MULT,
            TIGHT_LAYOUT_W_PAD_MULT as _LABEL_TIGHT_LAYOUT_W_PAD_MULT,
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

        h_pad_mult = getattr(_style, "TIGHT_LAYOUT_H_PAD_MULT", None)
        if h_pad_mult is None:
            h_pad_mult = _LABEL_TIGHT_LAYOUT_H_PAD_MULT

        w_pad_mult = getattr(_style, "TIGHT_LAYOUT_W_PAD_MULT", None)
        if w_pad_mult is None:
            w_pad_mult = _LABEL_TIGHT_LAYOUT_W_PAD_MULT

        if not h_pad_in and h_pad is None and h_pad_mult is not None:
            try:
                h_pad = float(h_pad_mult)
            except Exception:
                h_pad = None

        if not w_pad_in and w_pad is None and w_pad_mult is not None:
            try:
                w_pad = float(w_pad_mult)
            except Exception:
                w_pad = None

        out = orig_tight_layout(self, pad=pad_f, h_pad=h_pad, w_pad=w_pad, rect=rect)
        _apply_subplot_spacing(self)
        _center_wrapped_subplot_rows(self)
        return out

    matplotlib.figure.Figure.tight_layout = _tight_layout  # type: ignore[assignment]
    setattr(matplotlib.figure.Figure, "_irl_tight_layout_patched", True)


def _scaled_figsize(figsize: object) -> object:
    try:
        w, h = figsize  # type: ignore[misc]
    except Exception:
        return figsize

    try:
        w_f = float(w)
        h_f = float(h)
    except Exception:
        return figsize

    return (w_f, scale_plot_height(h_f))


def _patch_matplotlib_figsize_height_scale() -> None:
    import matplotlib.pyplot as plt

    if bool(getattr(plt, "_irl_figsize_height_scale_patched", False)):
        return

    orig_subplots = plt.subplots
    orig_figure = plt.figure

    def _subplots(*args, **kwargs):  # type: ignore[no-untyped-def]
        nrows_in = kwargs.get("nrows", 1)
        ncols_in = kwargs.get("ncols", 1)
        if len(args) >= 1:
            nrows_in = args[0]
        if len(args) >= 2:
            ncols_in = args[1]

        try:
            nrows_i = int(nrows_in)
            ncols_i = int(ncols_in)
        except Exception:
            nrows_i = None
            ncols_i = None

        try:
            max_per_row = int(getattr(_style, "MAX_PANELS_PER_ROW", 3) or 3)
        except Exception:
            max_per_row = 3
        max_per_row = int(max(1, max_per_row))

        wrap = bool(nrows_i == 1 and ncols_i is not None and ncols_i > 1 and ncols_i != max_per_row)

        grid_rows = 1
        grid_cols = ncols_i if ncols_i is not None else 1
        if wrap:
            grid_cols = int(max_per_row)
            grid_rows = int(math.ceil(float(ncols_i) / float(grid_cols)))

        fs = kwargs.get("figsize", None)
        if fs is not None:
            if wrap and grid_rows > 1:
                try:
                    w, h = fs  # type: ignore[misc]
                    fs = (w, float(h) * float(grid_rows))
                except Exception:
                    pass
            kwargs["figsize"] = _scaled_figsize(fs)

        if not wrap:
            return orig_subplots(*args, **kwargs)

        squeeze_orig = bool(kwargs.get("squeeze", True))

        args_l = list(args)
        if len(args_l) >= 1:
            args_l[0] = int(grid_rows)
        else:
            args_l.append(int(grid_rows))
        if len(args_l) >= 2:
            args_l[1] = int(grid_cols)
        else:
            args_l.append(int(grid_cols))

        kwargs2 = dict(kwargs)
        kwargs2.pop("nrows", None)
        kwargs2.pop("ncols", None)

        fig, axes_grid = orig_subplots(*args_l, **kwargs2)

        try:
            axes_flat = axes_grid.ravel()
            axes_all = axes_flat.tolist()
        except Exception:
            try:
                axes_all = list(axes_grid)
            except Exception:
                axes_all = []

        if axes_all and ncols_i is not None:
            setattr(
                fig,
                _WRAPPED_SUBPLOTS_ATTR,
                {
                    "grid_rows": int(grid_rows),
                    "grid_cols": int(grid_cols),
                    "n_used": int(ncols_i),
                    "axes": axes_all,
                },
            )

        try:
            axes_flat = axes_grid.ravel()
        except Exception:
            return fig, axes_grid

        used = axes_flat[: int(ncols_i)]
        for ax in axes_flat[int(ncols_i) :]:
            try:
                ax.set_visible(False)
            except Exception:
                pass

        _center_wrapped_subplot_rows(fig)

        if not squeeze_orig:
            return fig, used.reshape(1, int(ncols_i))
        return fig, used

    def _figure(*args, **kwargs):  # type: ignore[no-untyped-def]
        if "figsize" in kwargs and kwargs["figsize"] is not None:
            kwargs["figsize"] = _scaled_figsize(kwargs["figsize"])
            return orig_figure(*args, **kwargs)

        if len(args) >= 2:
            args_l = list(args)
            args_l[1] = _scaled_figsize(args_l[1])
            return orig_figure(*args_l, **kwargs)

        return orig_figure(*args, **kwargs)

    plt.subplots = _subplots  # type: ignore[assignment]
    plt.figure = _figure  # type: ignore[assignment]
    setattr(plt, "_irl_figsize_height_scale_patched", True)


def apply_rcparams_paper():
    import matplotlib

    try:
        matplotlib.use("Agg")
    except Exception:
        pass
    import matplotlib.pyplot as plt

    plt.rcParams.update(_STYLE_RCPARAMS)
    _disable_matplotlib_titles()
    _patch_matplotlib_supylabel()
    _patch_matplotlib_tight_layout_defaults()
    _patch_matplotlib_figsize_height_scale()
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

    _apply_subplot_spacing(fig)
    _center_wrapped_subplot_rows(fig)
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
