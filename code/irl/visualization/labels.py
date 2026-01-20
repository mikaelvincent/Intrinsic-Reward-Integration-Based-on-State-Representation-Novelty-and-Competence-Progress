from __future__ import annotations

import math
import re
from statistics import median
from typing import Iterable

from irl.visualization.style import LEGEND_FONTSIZE

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

LEGEND_GROUP_GAP_PT: float = 2
LEGEND_BLOCK_TO_CONTENT_PAD_EXTRA_PT: float = 6.0
LEGEND_BLOCK_TO_CONTENT_PAD_PT: float = (
    float(ROW_LABEL_DY_PT) + float(LEGEND_FONTSIZE) + float(LEGEND_BLOCK_TO_CONTENT_PAD_EXTRA_PT)
)

LEGEND_TIGHT_LAYOUT_PAD_MULT: float = 1.08

# If set, overrides tight_layout h_pad/w_pad (multiples of font size).
TIGHT_LAYOUT_H_PAD_MULT: float | None = None
TIGHT_LAYOUT_W_PAD_MULT: float | None = None


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


def legend_ncol(n_items: int, *, max_cols: int = 6) -> int:
    n = int(max(1, n_items))
    return int(min(max_cols, n))


def add_row_label(ax, label: str, *, fontsize: int | None = None) -> None:
    # Point-based offset keeps the label-to-axes gap consistent across subplot sizes.
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


def _median_subplot_row_gap(fig) -> float | None:
    axes = [ax for ax in getattr(fig, "axes", []) if getattr(ax, "get_visible", lambda: True)()]
    if len(axes) < 2:
        return None

    unique: dict[tuple[float, float, float, float], object] = {}
    for ax in axes:
        try:
            pos = ax.get_position()
        except Exception:
            continue
        x0, y0, x1, y1 = float(pos.x0), float(pos.y0), float(pos.x1), float(pos.y1)
        if not all(map(math.isfinite, (x0, y0, x1, y1))):
            continue
        if (x1 - x0) <= 1e-4 or (y1 - y0) <= 1e-4:
            continue
        key = (round(x0, 4), round(y0, 4), round(x1, 4), round(y1, 4))
        unique[key] = pos

    if len(unique) < 2:
        return None

    rows: dict[float, dict[str, float]] = {}
    for pos in unique.values():
        y_key = round(float(pos.y1), 3)
        rec = rows.get(y_key)
        if rec is None:
            rows[y_key] = {"top": float(pos.y1), "bottom": float(pos.y0)}
        else:
            rec["top"] = max(float(rec["top"]), float(pos.y1))
            rec["bottom"] = min(float(rec["bottom"]), float(pos.y0))

    if len(rows) < 2:
        return None

    row_list = sorted(rows.values(), key=lambda r: float(r["top"]), reverse=True)
    gaps: list[float] = []
    for upper, lower in zip(row_list[:-1], row_list[1:]):
        g = float(upper["bottom"]) - float(lower["top"])
        if math.isfinite(g) and g > 0.0:
            gaps.append(g)

    if not gaps:
        return None
    return float(median(gaps))


def _split_legend_group_even_rows(
    handles: list[object],
    labels: list[str],
    *,
    max_cols: int,
) -> list[tuple[list[object], list[str], int]]:
    n = int(len(handles))
    if n <= 0 or n != int(len(labels)):
        return [(handles, labels, int(max(1, max_cols)))]

    cols = int(max(1, int(max_cols)))
    if cols <= 1 or n <= cols:
        return [(handles, labels, int(min(cols, n)))]

    n_rows = int(math.ceil(float(n) / float(cols)))
    n_rows = int(max(1, n_rows))

    base = n // n_rows
    rem = n % n_rows

    out: list[tuple[list[object], list[str], int]] = []
    i = 0
    for r in range(n_rows):
        k = int(base + (1 if r < rem else 0))
        if k <= 0:
            continue
        out.append((handles[i : i + k], labels[i : i + k], k))
        i += k

    if i < n:
        out.append((handles[i:], labels[i:], int(n - i)))

    return out


def add_legend_rows_top(
    fig,
    rows: Iterable[tuple[list[object], list[str], int]],
    *,
    y_top: float = 0.995,
    row_gap: float = 0.012,
    fontsize: int | None = None,
    pad_axes_pt: float | None = None,
    legend_kwargs: dict[str, object] | None = None,
) -> float:
    fs = int(LEGEND_FONTSIZE) if fontsize is None else int(fontsize)

    fig_h_in = 0.0
    try:
        fig_h_in = float(fig.get_figheight())
    except Exception:
        fig_h_in = 0.0
    fig_h_pt = 72.0 * fig_h_in if fig_h_in > 0.0 else 0.0

    fig_w_in = 0.0
    try:
        fig_w_in = float(fig.get_figwidth())
    except Exception:
        fig_w_in = 0.0
    fig_w_pt = 72.0 * fig_w_in if fig_w_in > 0.0 else 0.0

    def _pt_to_fig_y(pt: float) -> float:
        if fig_h_pt <= 0.0:
            return 0.0
        return float(pt) / float(fig_h_pt)

    def _pt_to_fig_x(pt: float) -> float:
        if fig_w_pt <= 0.0:
            return 0.0
        return float(pt) / float(fig_w_pt)

    group_gap_pt = float(LEGEND_GROUP_GAP_PT)
    try:
        req_gap_pt = float(row_gap) * float(fig_h_pt)
        if math.isfinite(req_gap_pt) and req_gap_pt > 0.0:
            group_gap_pt = float(min(float(LEGEND_GROUP_GAP_PT), float(req_gap_pt)))
    except Exception:
        group_gap_pt = float(LEGEND_GROUP_GAP_PT)
    group_gap_fig = _pt_to_fig_y(group_gap_pt)

    block_pad_pt = float(LEGEND_BLOCK_TO_CONTENT_PAD_PT)
    if pad_axes_pt is not None:
        try:
            req_pad = float(pad_axes_pt)
            if math.isfinite(req_pad) and req_pad > 0.0:
                block_pad_pt = float(max(block_pad_pt, req_pad))
        except Exception:
            pass
    block_pad_fig = _pt_to_fig_y(block_pad_pt)

    base_fs = float(fs)
    try:
        import matplotlib as mpl

        base_fs = float(mpl.rcParams.get("font.size", base_fs))
    except Exception:
        base_fs = float(fs)

    tight_pad_fig = _pt_to_fig_y(float(LEGEND_TIGHT_LAYOUT_PAD_MULT) * float(base_fs))

    base_leg_kwargs: dict[str, object] = {
        "frameon": False,
        "fontsize": fs,
        "handlelength": 2.2,
        "columnspacing": 1.2,
        "handletextpad": 0.6,
    }
    if isinstance(legend_kwargs, dict):
        for k, v in legend_kwargs.items():
            if v is None:
                continue
            base_leg_kwargs[str(k)] = v

    groups: list[tuple[list[object], list[str], int]] = []
    for handles, labels, ncol in rows:
        hs = list(handles) if isinstance(handles, (list, tuple)) else []
        ls = list(labels) if isinstance(labels, (list, tuple)) else []

        n = int(min(int(len(hs)), int(len(ls))))
        if n <= 0:
            continue

        hs = hs[:n]
        ls = [str(s) for s in ls[:n]]

        try:
            cols = int(ncol)
        except Exception:
            cols = n

        cols = int(max(1, cols))
        groups.append((hs, ls, cols))

    if not groups:
        return 1.0

    if len(groups) == 1:
        handles, labels, ncol = groups[0]
        expanded: list[tuple[list[object], list[str], int]] = []

        if int(ncol) >= 2 and int(len(handles)) > int(ncol):
            expanded.extend(_split_legend_group_even_rows(handles, labels, max_cols=int(ncol)))
        else:
            expanded.append((handles, labels, int(min(int(ncol), int(len(handles))) if handles else 1)))

        y = float(y_top)
        legends: list[object] = []
        renderer = None

        for h, l, c in expanded:
            if not h or not l:
                continue

            leg = fig.legend(
                handles=h,
                labels=l,
                loc="upper center",
                bbox_to_anchor=(0.5, y),
                ncol=int(max(1, c)),
                **base_leg_kwargs,
            )
            legends.append(leg)

            try:
                fig.canvas.draw()
                renderer = fig.canvas.get_renderer()
                bbox = leg.get_window_extent(renderer=renderer)
                bbox_fig = bbox.transformed(fig.transFigure.inverted())
                y = float(bbox_fig.y0) - float(group_gap_fig)
            except Exception:
                y = float(y) - float(group_gap_fig)

        if not legends:
            return 1.0

        min_y0 = None
        try:
            if renderer is None:
                fig.canvas.draw()
                renderer = fig.canvas.get_renderer()

            bottoms: list[float] = []
            for leg in legends:
                bbox = leg.get_window_extent(renderer=renderer)
                bbox_fig = bbox.transformed(fig.transFigure.inverted())
                bottoms.append(float(bbox_fig.y0))

            if bottoms:
                min_y0 = float(min(bottoms))
        except Exception:
            min_y0 = None

        if min_y0 is None:
            min_y0 = float(y)

        top = float(min_y0) - float(block_pad_fig) + float(tight_pad_fig)
        return float(max(0.0, min(1.0, top)))

    # Multiple legend groups are placed side-by-side to keep per-group formatting intact.
    y = float(y_top)
    legends: list[object] = []
    renderer = None

    for handles, labels, ncol in groups:
        leg = fig.legend(
            handles=handles,
            labels=labels,
            loc="upper left",
            bbox_to_anchor=(0.0, y),
            ncol=int(max(1, ncol)),
            **base_leg_kwargs,
        )
        legends.append(leg)

    try:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
    except Exception:
        return 1.0

    bboxes_fig: list[object] = []
    widths: list[float] = []
    bottoms: list[float] = []

    for leg in legends:
        try:
            bb = leg.get_window_extent(renderer=renderer)
            bb_fig = bb.transformed(fig.transFigure.inverted())
        except Exception:
            continue

        bboxes_fig.append(bb_fig)
        widths.append(float(getattr(bb_fig, "width", 0.0)))
        bottoms.append(float(getattr(bb_fig, "y0", 0.0)))

    if not widths or not bottoms:
        return 1.0

    col_gap_pt = float(max(10.0, 1.1 * float(base_fs)))
    col_gap_fig = _pt_to_fig_x(col_gap_pt)

    sum_w = float(sum(widths))
    k = int(len(widths))
    if k >= 2:
        avail = float(max(0.0, 1.0 - sum_w))
        max_gap = float(avail) / float(k - 1) if (k - 1) > 0 else 0.0
        if not (math.isfinite(max_gap) and max_gap >= 0.0):
            max_gap = 0.0
        col_gap_fig = float(min(float(col_gap_fig), float(max_gap)))

    total_w = float(sum_w + float(col_gap_fig) * float(max(0, k - 1)))
    start_x = 0.5 - 0.5 * total_w
    if not math.isfinite(start_x):
        start_x = 0.0
    start_x = float(max(0.0, start_x))

    x = float(start_x)
    for leg, w in zip(legends, widths):
        try:
            leg.set_bbox_to_anchor((float(x), float(y)), transform=fig.transFigure)
        except Exception:
            pass
        x = float(x) + float(w) + float(col_gap_fig)

    min_y0 = float(min(bottoms))
    top = float(min_y0) - float(block_pad_fig) + float(tight_pad_fig)
    return float(max(0.0, min(1.0, top)))
