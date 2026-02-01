from __future__ import annotations

import math
import re
from typing import Iterable

from irl.visualization.style import (
    LEGEND_FONTSIZE,
    LEGEND_PANEL_ENTRY_HSPACE,
    LEGEND_PANEL_ENTRY_VSPACE,
    LEGEND_PANEL_GROUP_HSPACE,
    LEGEND_PANEL_POSITION,
)

_VERSION_RE = re.compile(r"-v\d+$", re.IGNORECASE)
_SLUG_RE = re.compile(r"[^a-z0-9]+", re.IGNORECASE)

_METHOD_LABELS: dict[str, str] = {
    "vanilla": "Vanilla",
    "icm": "ICM",
    "rnd": "RND",
    "ride": "RIDE",
    "riac": "RIAC",
    "glpe": "GLPE",
    "glpe_lp_only": "GLPE (LP only)",
    "glpe_impact_only": "GLPE (impact only)",
    "glpe_nogate": "GLPE (no gate)",
    "glpe_cache": "GLPE (cached)",
}

_COMPONENT_LABELS: dict[str, str] = {
    "env_step": "Environment step",
    "policy": "Policy",
    "intrinsic": "Intrinsic",
    "gae": "GAE",
    "ppo": "PPO",
    "other": "Other",
    "reward": "Extrinsic reward",
    "gate": "Gate rate",
    "impact": "Impact",
    "lp": "Learning progress",
}

ROW_LABEL_DY_PT: float = 2

LEGEND_GROUP_GAP_PT: float = 1.5
LEGEND_ROW_MAX_USAGE_FRAC: float = 1.0
LEGEND_COL_SPACING_EM: float = 1.2
LEGEND_GROUP_COL_GAP_PT: float = 60.0

LEGEND_BLOCK_TO_CONTENT_PAD_EXTRA_PT: float = 6.0
LEGEND_BLOCK_TO_CONTENT_PAD_PT: float = (
    float(ROW_LABEL_DY_PT) + float(LEGEND_FONTSIZE) + float(LEGEND_BLOCK_TO_CONTENT_PAD_EXTRA_PT)
)

LEGEND_TIGHT_LAYOUT_PAD_MULT: float = 1.08

TIGHT_LAYOUT_H_PAD_MULT: float | None = None
TIGHT_LAYOUT_W_PAD_MULT: float | None = None

_LEGEND_PANEL_SPEC_ATTR: str = "_irl_legend_panel_spec"
_LEGEND_PANEL_TL_PATCHED_ATTR: str = "_irl_legend_panel_tl_patched"


def slugify(tag: object) -> str:
    s = str(tag).strip().lower()
    s = s.replace("paper_", "")
    s = _SLUG_RE.sub("-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s or "plot"


def env_label(env_id: object) -> str:
    s = str(env_id).strip().replace("/", "-")
    s = _VERSION_RE.sub("", s)
    return s


def method_key(method: object) -> str:
    return str(method).strip().lower()


def method_label(method: object) -> str:
    k = method_key(method)
    if k in _METHOD_LABELS:
        return _METHOD_LABELS[k]
    if k.isupper():
        return k
    if len(k) <= 4 and k.isalpha():
        return k.upper()
    return k.replace("_", " ").strip()


def component_label(component: object) -> str:
    k = str(component).strip().lower()
    if k in _COMPONENT_LABELS:
        return _COMPONENT_LABELS[k]
    return k.replace("_", " ").strip().capitalize()


def legend_ncol(n_items: int, *, max_cols: int = 20) -> int:
    n = int(max(1, n_items))
    return int(min(max_cols, n))


def add_row_label(ax, label: str, *, fontsize: int | None = None) -> None:
    fs = int(LEGEND_FONTSIZE) if fontsize is None else int(fontsize)
    fig = getattr(ax, "figure", None)
    if fig is None:
        return
    try:
        import matplotlib.transforms as mtransforms
    except Exception:
        return

    trans = ax.transAxes + mtransforms.ScaledTranslation(0.0, float(ROW_LABEL_DY_PT) / 72.0, fig.dpi_scale_trans)

    ax.text(
        0.5,
        1.0,
        str(label),
        transform=trans,
        va="bottom",
        ha="center",
        fontsize=fs,
        clip_on=False,
    )


def _as_panel_position(x: object) -> str:
    s = str(x).strip().lower()
    if s in {"first", "left"}:
        return "first"
    return "last"


def _sanitize_legend_rows(
    rows: Iterable[tuple[list[object], list[str], int]],
) -> list[tuple[list[object], list[str], int]]:
    out: list[tuple[list[object], list[str], int]] = []
    for handles, labels, ncol in rows:
        hs = list(handles) if isinstance(handles, (list, tuple)) else []
        ls = list(labels) if isinstance(labels, (list, tuple)) else []

        n = int(min(len(hs), len(ls)))
        if n <= 0:
            continue

        hs = hs[:n]
        ls = [str(s) for s in ls[:n]]

        try:
            cap = int(ncol)
        except Exception:
            cap = n
        cap = int(max(1, min(n, cap)))

        out.append((hs, ls, cap))
    return out


def _axis_pos_key(ax: object) -> tuple[float, float, float, float] | None:
    try:
        pos = getattr(ax, "get_position")()
    except Exception:
        return None

    try:
        x0, y0, x1, y1 = float(pos.x0), float(pos.y0), float(pos.x1), float(pos.y1)
    except Exception:
        return None

    if not all(map(math.isfinite, (x0, y0, x1, y1))):
        return None
    if (x1 - x0) <= 1e-4 or (y1 - y0) <= 1e-4:
        return None

    return (round(x0, 4), round(y0, 4), round(x1, 4), round(y1, 4))


def _grid_cols(fig, *, exclude: set[object]) -> int:
    unique: dict[tuple[float, float, float, float], tuple[float, float, float, float]] = {}

    for ax in getattr(fig, "axes", []):
        if ax in exclude:
            continue
        try:
            if not bool(getattr(ax, "get_visible")()):
                continue
        except Exception:
            continue
        try:
            if hasattr(ax, "get_in_layout") and not bool(getattr(ax, "get_in_layout")()):
                continue
        except Exception:
            continue

        key = _axis_pos_key(ax)
        if key is None:
            continue
        unique[key] = key

    if not unique:
        return 1

    by_row: dict[float, int] = {}
    for (_x0, _y0, _x1, y1) in unique.values():
        row_key = round(float(y1), 3)
        by_row[row_key] = int(by_row.get(row_key, 0)) + 1

    return int(max(1, max(by_row.values(), default=1)))


def _fig_size_pt(fig) -> tuple[float, float]:
    try:
        w = 72.0 * float(fig.get_figwidth())
    except Exception:
        w = 0.0
    try:
        h = 72.0 * float(fig.get_figheight())
    except Exception:
        h = 0.0
    return float(w), float(h)


def _legend_rect_and_pos(
    fig,
    rect_in: object,
    *,
    grid_cols: int,
    position: str,
    fontsize: int,
) -> tuple[list[float], list[float]]:
    if rect_in is None:
        left, bottom, right, top = 0.0, 0.0, 1.0, 1.0
    else:
        try:
            left, bottom, right, top = rect_in  # type: ignore[misc]
        except Exception:
            left, bottom, right, top = 0.0, 0.0, 1.0, 1.0

    try:
        l = float(left)
        b = float(bottom)
        r = float(right)
        t = float(top)
    except Exception:
        l, b, r, t = 0.0, 0.0, 1.0, 1.0

    l = float(max(0.0, min(1.0, l)))
    b = float(max(0.0, min(1.0, b)))
    r = float(max(0.0, min(1.0, r)))
    t = float(max(0.0, min(1.0, t)))

    if r <= l:
        l, r = 0.0, 1.0
    if t <= b:
        b, t = 0.0, 1.0

    fig_w_pt, _fig_h_pt = _fig_size_pt(fig)

    gap_pt = float(LEGEND_PANEL_GROUP_HSPACE) * float(max(1, int(fontsize)))
    gap_fig = float(gap_pt / fig_w_pt) if fig_w_pt > 0.0 else 0.0
    gap_fig = float(max(0.0, min(0.1, gap_fig)))

    cols = int(max(1, int(grid_cols)))
    width = float(r - l)
    height = float(t - b)

    denom = float(cols + 1)
    slot_w = (float(width) - float(gap_fig)) / denom if denom > 0.0 else 0.0
    if not (math.isfinite(slot_w) and slot_w > 0.0):
        slot_w = float(width) / float(max(2, cols + 1))

    reserve = float(slot_w) + float(gap_fig)
    if reserve >= 0.95 * float(width):
        reserve = 0.95 * float(width)
        slot_w = float(max(0.0, float(reserve) - float(gap_fig)))

    if _as_panel_position(position) == "first":
        rect_out = [float(l + reserve), float(b), float(r), float(t)]
        leg_pos = [float(l), float(b), float(slot_w), float(height)]
    else:
        rect_out = [float(l), float(b), float(r - reserve), float(t)]
        leg_pos = [float(r - slot_w), float(b), float(slot_w), float(height)]

    rect_out[0] = float(max(0.0, min(1.0, rect_out[0])))
    rect_out[2] = float(max(0.0, min(1.0, rect_out[2])))
    if rect_out[2] <= rect_out[0] + 1e-6:
        rect_out[0] = float(l)
        rect_out[2] = float(r)

    leg_pos[0] = float(max(0.0, min(1.0, leg_pos[0])))
    leg_pos[2] = float(max(0.0, min(1.0 - leg_pos[0], leg_pos[2])))

    return rect_out, leg_pos


def _adopt_supylabel(fig, *, exclude: set[object]) -> None:
    sup = getattr(fig, "_supylabel", None)
    if sup is None:
        return

    try:
        txt = str(getattr(sup, "get_text")()).strip()
    except Exception:
        txt = ""
    if not txt:
        return

    for ax in getattr(fig, "axes", []):
        if ax in exclude:
            continue
        try:
            if not bool(getattr(ax, "get_visible")()):
                continue
        except Exception:
            continue
        try:
            if hasattr(ax, "get_in_layout") and not bool(getattr(ax, "get_in_layout")()):
                continue
        except Exception:
            continue
        try:
            pos = str(getattr(ax, "yaxis").get_label_position()).strip().lower()
        except Exception:
            pos = "left"
        if pos == "right":
            continue
        try:
            ax.set_ylabel(txt)
        except Exception:
            continue

    try:
        sup.set_text("")
        sup.set_visible(False)
    except Exception:
        return


def render_legend_panel(
    ax,
    rows: Iterable[tuple[list[object], list[str], int]],
    *,
    fontsize: int | None = None,
    legend_kwargs: dict[str, object] | None = None,
) -> None:
    keep_visible = True
    keep_in_layout = True
    try:
        keep_visible = bool(ax.get_visible())
    except Exception:
        keep_visible = True
    try:
        keep_in_layout = bool(ax.get_in_layout()) if hasattr(ax, "get_in_layout") else True
    except Exception:
        keep_in_layout = True

    try:
        ax.cla()
    except Exception:
        return

    try:
        ax.set_visible(bool(keep_visible))
    except Exception:
        pass
    if hasattr(ax, "set_in_layout"):
        try:
            ax.set_in_layout(bool(keep_in_layout))
        except Exception:
            pass

    try:
        ax.set_axis_off()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.yaxis.set_label_position("right")
    except Exception:
        pass

    rows_s = _sanitize_legend_rows(rows)
    if not rows_s:
        return

    fs = int(LEGEND_FONTSIZE) if fontsize is None else int(fontsize)

    base_leg_kwargs: dict[str, object] = {
        "frameon": False,
        "fontsize": fs,
        "handlelength": 2.2,
        "columnspacing": float(LEGEND_PANEL_ENTRY_HSPACE),
        "labelspacing": float(LEGEND_PANEL_ENTRY_VSPACE),
        "handletextpad": 0.6,
        "borderaxespad": 0.0,
    }
    if isinstance(legend_kwargs, dict):
        for k, v in legend_kwargs.items():
            if v is None:
                continue
            base_leg_kwargs[str(k)] = v

    fig = getattr(ax, "figure", None)
    if fig is None:
        return

    try:
        ax_pos = ax.get_position()
        ax_w = float(getattr(ax_pos, "width", 0.0))
        ax_h = float(getattr(ax_pos, "height", 0.0))
    except Exception:
        ax_w = 0.0
        ax_h = 0.0

    fig_w_pt, fig_h_pt = _fig_size_pt(fig)
    ax_w_pt = float(fig_w_pt) * float(ax_w) if ax_w > 0.0 else 0.0
    ax_h_pt = float(fig_h_pt) * float(ax_h) if ax_h > 0.0 else 0.0

    pad_pt = float(LEGEND_PANEL_GROUP_HSPACE) * float(max(1, fs))
    pad_x = float(pad_pt / ax_w_pt) if ax_w_pt > 0.0 else 0.02
    pad_y = float(pad_pt / ax_h_pt) if ax_h_pt > 0.0 else 0.02
    pad_x = float(max(0.0, min(0.15, pad_x)))
    pad_y = float(max(0.0, min(0.15, pad_y)))

    group_gap = float(pad_y)
    max_w = float(max(0.1, 1.0 - 2.0 * float(pad_x)))

    try:
        import matplotlib.legend as mlegend
    except Exception:
        return

    def _legend_extent_frac(hs: list[object], ls: list[str], *, ncol: int) -> tuple[float, float]:
        leg = mlegend.Legend(
            ax,
            hs,
            ls,
            loc="upper left",
            bbox_to_anchor=(0.0, 1.0),
            bbox_transform=ax.transAxes,
            ncol=int(max(1, ncol)),
            **base_leg_kwargs,
        )
        ax.add_artist(leg)

        w_out = 0.0
        h_out = 0.0
        try:
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()
            bb = leg.get_window_extent(renderer=renderer)
            bb_fig = bb.transformed(fig.transFigure.inverted())
            w_fig = float(getattr(bb_fig, "width", 0.0))
            h_fig = float(getattr(bb_fig, "height", 0.0))

            ax_pos_local = ax.get_position()
            w_out = float(w_fig / float(ax_pos_local.width)) if float(ax_pos_local.width) > 0.0 else 0.0
            h_out = float(h_fig / float(ax_pos_local.height)) if float(ax_pos_local.height) > 0.0 else 0.0
        except Exception:
            w_out = 0.0
            h_out = 0.0
        finally:
            try:
                leg.remove()
            except Exception:
                pass

        return float(w_out), float(h_out)

    y = float(1.0 - float(pad_y))

    for hs, ls, max_cols in rows_s:
        n = int(min(len(hs), len(ls)))
        if n <= 0:
            continue

        cap = int(max(1, min(n, int(max_cols))))
        chosen = 1
        chosen_h = 0.0

        for k in range(int(cap), 0, -1):
            w, h = _legend_extent_frac(hs[:n], ls[:n], ncol=int(k))
            if float(w) <= float(max_w) or int(k) == 1:
                chosen = int(k)
                chosen_h = float(h)
                break

        if chosen_h <= 0.0:
            _w2, chosen_h = _legend_extent_frac(hs[:n], ls[:n], ncol=int(chosen))

        leg = mlegend.Legend(
            ax,
            hs[:n],
            ls[:n],
            loc="upper left",
            bbox_to_anchor=(float(pad_x), float(y)),
            bbox_transform=ax.transAxes,
            ncol=int(chosen),
            **base_leg_kwargs,
        )
        ax.add_artist(leg)

        y = float(y - float(chosen_h) - float(group_gap))


def _try_reuse_hidden_subplot_axis(fig) -> object | None:
    spec = getattr(fig, "_irl_wrapped_subplots", None)
    if not isinstance(spec, dict):
        return None

    axes = spec.get("axes", None)
    if not isinstance(axes, (list, tuple)) or not axes:
        return None

    try:
        n_used = int(spec.get("n_used", 0))
    except Exception:
        return None

    if n_used < 0 or n_used >= int(len(axes)):
        return None

    ax = axes[int(n_used)]
    if ax is None:
        return None

    try:
        ax.set_visible(True)
    except Exception:
        return None

    try:
        spec["n_used"] = int(n_used) + 1
    except Exception:
        pass

    try:
        if hasattr(ax, "set_in_layout"):
            ax.set_in_layout(True)
    except Exception:
        pass

    return ax


def _create_external_legend_axis(fig):
    ax = fig.add_axes([0.0, 0.0, 0.05, 0.05])
    try:
        if hasattr(ax, "set_in_layout"):
            ax.set_in_layout(False)
    except Exception:
        pass
    return ax


def add_legend_rows_top(
    fig,
    rows: Iterable[tuple[list[object], list[str], int]],
    *,
    y_top: float = 0.995,
    row_gap: float = 0.012,
    fontsize: int | None = None,
    pad_axes_pt: float | None = None,
    legend_kwargs: dict[str, object] | None = None,
    max_row_usage_frac: float = LEGEND_ROW_MAX_USAGE_FRAC,
    legend_col_spacing_em: float = LEGEND_COL_SPACING_EM,
    legend_group_col_gap_pt: float | None = None,
) -> float:
    _ = y_top
    _ = row_gap
    _ = pad_axes_pt
    _ = max_row_usage_frac
    _ = legend_col_spacing_em
    _ = legend_group_col_gap_pt

    rows_s = _sanitize_legend_rows(rows)
    if not rows_s:
        return 1.0

    pos = _as_panel_position(LEGEND_PANEL_POSITION)
    fs = int(LEGEND_FONTSIZE) if fontsize is None else int(fontsize)

    spec_prev = getattr(fig, _LEGEND_PANEL_SPEC_ATTR, None)
    ax_prev = spec_prev.get("ax") if isinstance(spec_prev, dict) else None

    ax_leg = None
    external = False

    if ax_prev is not None:
        try:
            if getattr(ax_prev, "figure", None) is fig:
                ax_leg = ax_prev
                external = bool(spec_prev.get("external", False)) if isinstance(spec_prev, dict) else False
        except Exception:
            ax_leg = None

    if ax_leg is None and pos == "last":
        ax_reuse = _try_reuse_hidden_subplot_axis(fig)
        if ax_reuse is not None:
            ax_leg = ax_reuse
            external = False

    if ax_leg is None:
        ax_leg = _create_external_legend_axis(fig)
        external = True

    setattr(
        fig,
        _LEGEND_PANEL_SPEC_ATTR,
        {
            "ax": ax_leg,
            "external": bool(external),
            "position": str(pos),
            "rows": rows_s,
            "fontsize": int(fs),
            "legend_kwargs": legend_kwargs if isinstance(legend_kwargs, dict) else None,
        },
    )

    try:
        render_legend_panel(ax_leg, rows_s, fontsize=int(fs), legend_kwargs=legend_kwargs)
    except Exception:
        pass

    if bool(getattr(fig, _LEGEND_PANEL_TL_PATCHED_ATTR, False)):
        return 1.0

    orig_tight_layout = fig.tight_layout

    def _tight_layout_with_legend(*args, **kwargs):  # type: ignore[no-untyped-def]
        spec = getattr(fig, _LEGEND_PANEL_SPEC_ATTR, None)
        if not isinstance(spec, dict):
            return orig_tight_layout(*args, **dict(kwargs))

        ax = spec.get("ax", None)
        if ax is None:
            return orig_tight_layout(*args, **dict(kwargs))

        rows_local = spec.get("rows", [])
        fs_local = int(spec.get("fontsize", int(LEGEND_FONTSIZE)))
        legend_kwargs_local = spec.get("legend_kwargs", None)
        external_local = bool(spec.get("external", False))
        pos_local = _as_panel_position(spec.get("position", "last"))

        if external_local:
            out1 = orig_tight_layout(*args, **dict(kwargs))

            grid_cols = _grid_cols(fig, exclude={ax})
            rect_in = kwargs.get("rect", None)
            rect2, ax_pos = _legend_rect_and_pos(
                fig,
                rect_in,
                grid_cols=int(grid_cols),
                position=str(pos_local),
                fontsize=int(fs_local),
            )

            if pos_local == "first":
                _adopt_supylabel(fig, exclude={ax})

            kwargs2 = dict(kwargs)
            kwargs2["rect"] = rect2
            out2 = orig_tight_layout(*args, **kwargs2)

            try:
                ax.set_position(ax_pos)
            except Exception:
                pass

            try:
                render_legend_panel(
                    ax,
                    rows_local,
                    fontsize=int(fs_local),
                    legend_kwargs=legend_kwargs_local if isinstance(legend_kwargs_local, dict) else None,
                )
            except Exception:
                pass

            return out2

        out = orig_tight_layout(*args, **dict(kwargs))

        try:
            render_legend_panel(
                ax,
                rows_local,
                fontsize=int(fs_local),
                legend_kwargs=legend_kwargs_local if isinstance(legend_kwargs_local, dict) else None,
            )
        except Exception:
            pass

        return out

    fig.tight_layout = _tight_layout_with_legend  # type: ignore[assignment]
    setattr(fig, _LEGEND_PANEL_TL_PATCHED_ATTR, True)
    return 1.0
