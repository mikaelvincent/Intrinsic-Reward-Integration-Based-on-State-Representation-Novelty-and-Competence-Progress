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

LEGEND_GROUP_GAP_PT: float = 1.5
LEGEND_ROW_MAX_USAGE_FRAC: float = 1.0
LEGEND_COL_SPACING_EM: float = 1.2
LEGEND_GROUP_COL_GAP_PT: float = 60.0

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


def legend_ncol(n_items: int, *, max_cols: int = 20) -> int:
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
    max_row_usage_frac: float = LEGEND_ROW_MAX_USAGE_FRAC,
    legend_col_spacing_em: float = LEGEND_COL_SPACING_EM,
    legend_group_col_gap_pt: float | None = None,
) -> float:
    fs = int(LEGEND_FONTSIZE) if fontsize is None else int(fontsize)

    try:
        fig_h_pt = 72.0 * float(fig.get_figheight())
    except Exception:
        fig_h_pt = 0.0

    try:
        fig_w_pt = 72.0 * float(fig.get_figwidth())
    except Exception:
        fig_w_pt = 0.0

    def _pt_to_fig_y(pt: float) -> float:
        if not (fig_h_pt > 0.0):
            return 0.0
        return float(pt) / float(fig_h_pt)

    def _pt_to_fig_x(pt: float) -> float:
        if not (fig_w_pt > 0.0):
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

    try:
        max_frac = float(max_row_usage_frac)
    except Exception:
        max_frac = float(LEGEND_ROW_MAX_USAGE_FRAC)
    if not math.isfinite(max_frac):
        max_frac = float(LEGEND_ROW_MAX_USAGE_FRAC)
    max_frac = float(max(0.05, min(1.0, max_frac)))

    try:
        col_spacing = float(legend_col_spacing_em)
    except Exception:
        col_spacing = float(LEGEND_COL_SPACING_EM)
    if not math.isfinite(col_spacing) or col_spacing <= 0.0:
        col_spacing = float(LEGEND_COL_SPACING_EM)

    if legend_group_col_gap_pt is None:
        col_gap_pt = float(LEGEND_GROUP_COL_GAP_PT)
    else:
        try:
            col_gap_pt = float(legend_group_col_gap_pt)
        except Exception:
            col_gap_pt = float(LEGEND_GROUP_COL_GAP_PT)
    if not math.isfinite(col_gap_pt) or col_gap_pt < 0.0:
        col_gap_pt = float(LEGEND_GROUP_COL_GAP_PT)
    col_gap_fig = _pt_to_fig_x(col_gap_pt)

    base_leg_kwargs: dict[str, object] = {
        "frameon": False,
        "fontsize": fs,
        "handlelength": 2.2,
        "columnspacing": float(col_spacing),
        "handletextpad": 0.6,
    }
    if isinstance(legend_kwargs, dict):
        for k, v in legend_kwargs.items():
            if v is None:
                continue
            base_leg_kwargs[str(k)] = v

    groups: list[dict[str, object]] = []
    for handles, labels, ncol in rows:
        hs = list(handles) if isinstance(handles, (list, tuple)) else []
        ls = list(labels) if isinstance(labels, (list, tuple)) else []

        n = int(min(int(len(hs)), int(len(ls))))
        if n <= 0:
            continue

        hs = hs[:n]
        ls = [str(s) for s in ls[:n]]

        try:
            cap = int(ncol)
        except Exception:
            cap = n
        cap = int(max(1, min(int(n), int(cap))))

        groups.append({"handles": hs, "labels": ls, "max_cols": cap})

    if not groups:
        return 1.0

    def _legend_size(
        hs: list[object],
        ls: list[str],
        *,
        ncol: int,
    ) -> tuple[float, float]:
        if not hs or not ls:
            return 0.0, 0.0

        n = int(min(int(len(hs)), int(len(ls))))
        if n <= 0:
            return 0.0, 0.0

        leg = fig.legend(
            handles=hs[:n],
            labels=ls[:n],
            loc="upper left",
            bbox_to_anchor=(0.0, float(y_top)),
            ncol=int(max(1, ncol)),
            **base_leg_kwargs,
        )

        w = 0.0
        h = 0.0
        try:
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()
            bb = leg.get_window_extent(renderer=renderer)
            bb_fig = bb.transformed(fig.transFigure.inverted())
            w = float(getattr(bb_fig, "width", 0.0))
            h = float(getattr(bb_fig, "height", 0.0))
        except Exception:
            w = 0.0
            h = 0.0

        try:
            leg.remove()
        except Exception:
            try:
                fig.legends.remove(leg)
            except Exception:
                pass

        return float(w), float(h)

    def _pack_group(
        hs: list[object],
        ls: list[str],
        *,
        max_cols: int,
    ) -> list[dict[str, object]]:
        n = int(min(int(len(hs)), int(len(ls))))
        if n <= 0:
            return []

        cap = int(max_cols)
        cap = int(max(1, min(int(n), int(cap))))

        out: list[dict[str, object]] = []
        i = 0
        while i < n:
            rem = int(n - i)
            k_max = int(min(int(cap), int(rem)))

            chosen_k = 1
            chosen_w = 0.0
            chosen_h = 0.0

            for k in range(int(k_max), 0, -1):
                w, h = _legend_size(hs[i : i + k], ls[i : i + k], ncol=int(k))
                if not (math.isfinite(w) and w > 0.0 and math.isfinite(h) and h > 0.0):
                    continue

                if float(w) <= float(max_frac) or int(k) == 1:
                    chosen_k = int(k)
                    chosen_w = float(w)
                    chosen_h = float(h)
                    if float(w) <= float(max_frac):
                        break

            if chosen_k <= 0:
                chosen_k = 1

            out.append(
                {
                    "handles": hs[i : i + chosen_k],
                    "labels": ls[i : i + chosen_k],
                    "width": float(chosen_w),
                    "height": float(chosen_h),
                }
            )
            i += int(chosen_k)

        return out

    blocks: list[dict[str, object]] = []
    for g in groups:
        hs = list(g.get("handles", []))
        ls = list(g.get("labels", []))
        try:
            cap = int(g.get("max_cols", len(hs)))
        except Exception:
            cap = len(hs)

        row_specs = _pack_group(hs, ls, max_cols=int(cap))
        if not row_specs:
            continue

        widths = [float(r.get("width", 0.0)) for r in row_specs]
        heights = [float(r.get("height", 0.0)) for r in row_specs]

        w = float(max(widths)) if widths else 0.0
        h_sum = float(sum(heights))
        h = float(h_sum + float(group_gap_fig) * float(max(0, len(row_specs) - 1)))

        blocks.append({"rows": row_specs, "width": float(w), "height": float(h)})

    if not blocks:
        return 1.0

    lines: list[dict[str, object]] = []
    cur: list[dict[str, object]] = []
    cur_w = 0.0
    cur_h = 0.0

    for blk in blocks:
        try:
            bw = float(blk.get("width", 0.0))
        except Exception:
            bw = 0.0
        try:
            bh = float(blk.get("height", 0.0))
        except Exception:
            bh = 0.0

        if not cur:
            cur = [blk]
            cur_w = float(bw)
            cur_h = float(bh)
            continue

        proposed = float(cur_w) + float(col_gap_fig) + float(bw)
        if float(proposed) <= float(max_frac) or not (cur_w > 0.0):
            cur.append(blk)
            cur_w = float(proposed)
            cur_h = float(max(float(cur_h), float(bh)))
            continue

        lines.append({"blocks": cur, "width": float(cur_w), "height": float(cur_h)})
        cur = [blk]
        cur_w = float(bw)
        cur_h = float(bh)

    if cur:
        lines.append({"blocks": cur, "width": float(cur_w), "height": float(cur_h)})

    if not lines:
        return 1.0

    legends: list[object] = []
    y = float(y_top)

    for line in lines:
        b_list = line.get("blocks", [])
        if not isinstance(b_list, list) or not b_list:
            continue

        try:
            line_w = float(line.get("width", 0.0))
        except Exception:
            line_w = 0.0
        try:
            line_h = float(line.get("height", 0.0))
        except Exception:
            line_h = 0.0

        if not math.isfinite(line_w) or line_w <= 0.0:
            line_w = 0.0
        if not math.isfinite(line_h) or line_h < 0.0:
            line_h = 0.0

        start_x = float(0.5 - 0.5 * float(line_w))
        if not math.isfinite(start_x):
            start_x = 0.0
        start_x = float(max(0.0, start_x))

        x = float(start_x)

        for blk in b_list:
            try:
                bw = float(blk.get("width", 0.0))
            except Exception:
                bw = 0.0

            row_specs = blk.get("rows", [])
            if not isinstance(row_specs, list) or not row_specs:
                x = float(x) + float(bw) + float(col_gap_fig)
                continue

            y_row = float(y)

            for ri, r in enumerate(row_specs):
                hs = r.get("handles", [])
                ls = r.get("labels", [])
                if not isinstance(hs, list) or not isinstance(ls, list) or not hs or not ls:
                    continue

                k = int(min(int(len(hs)), int(len(ls))))
                if k <= 0:
                    continue

                try:
                    row_w = float(r.get("width", 0.0))
                except Exception:
                    row_w = 0.0
                try:
                    row_h = float(r.get("height", 0.0))
                except Exception:
                    row_h = 0.0

                row_x = float(x)
                if (
                    math.isfinite(bw)
                    and math.isfinite(row_w)
                    and float(bw) > 0.0
                    and float(row_w) > 0.0
                    and float(bw) > float(row_w)
                ):
                    row_x = float(x) + 0.5 * float(float(bw) - float(row_w))

                leg = fig.legend(
                    handles=hs[:k],
                    labels=[str(s) for s in ls[:k]],
                    loc="upper left",
                    bbox_to_anchor=(float(row_x), float(y_row)),
                    ncol=int(k),
                    **base_leg_kwargs,
                )
                legends.append(leg)

                if ri < int(len(row_specs) - 1):
                    y_row = float(y_row) - float(row_h) - float(group_gap_fig)
                else:
                    y_row = float(y_row) - float(row_h)

            x = float(x) + float(bw) + float(col_gap_fig)

        y = float(y) - float(line_h) - float(group_gap_fig)

    if not legends:
        return 1.0

    min_y0 = None
    try:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        bottoms: list[float] = []
        for leg in legends:
            bb = leg.get_window_extent(renderer=renderer)
            bb_fig = bb.transformed(fig.transFigure.inverted())
            bottoms.append(float(getattr(bb_fig, "y0", 0.0)))

        if bottoms:
            min_y0 = float(min(bottoms))
    except Exception:
        min_y0 = None

    if min_y0 is None:
        min_y0 = float(y)

    top = float(min_y0) - float(block_pad_fig) + float(tight_pad_fig)
    return float(max(0.0, min(1.0, top)))
