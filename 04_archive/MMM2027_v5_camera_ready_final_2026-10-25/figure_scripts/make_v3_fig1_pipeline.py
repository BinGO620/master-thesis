"""Fig. 1 (v3) - where the four components attach to the MonoGS backbone.

2026-08-30 redesign (first-figure pass): all text measured to fit its box
(>= 7 pt target, fit_text shrinks only as a last resort), connector labels
removed (component boxes carry their own semantics), and L's site-2 edge routed
through the free corridor into D's bottom edge.

Topology is the audited one (results/evidence/method_attachment_audit.md):
R -> pose-solve residual; K -> keyframe gate; D -> candidate confirm/delete;
L consumed at exactly two sites (tracking residual weight + candidate
confirmation); the optional semantic mask attaches at mapping loss +
keyframe-insertion gate and never through L.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from scripts._figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=7)

fig = plt.figure(figsize=(TEXTWIDTH, 3.35 / 2.54))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12.2)
ax.set_ylim(0, 4.0)
ax.axis("off")

BLUE_BG = "#DCE9F5"
BLUE_ED = C["combined"]
ORG = "#B26B2C"
GREY_BG = "#EFEFEF"
GREY_ED = "#B9B9B9"


def box(x, y, w, h, label, face, edge, fs=7.0, lw=0.9, ls="-", z=2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.10",
        facecolor=face, edgecolor=edge, lw=lw, linestyle=ls, zorder=z))
    t = ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color=C["ink"], zorder=z + 1, linespacing=1.2)
    return t


def fit_text(text_obj, box_w_units, pad=0.86):
    """Shrink a box label until its widest line fits the box width."""
    fig.canvas.draw()
    bbox = text_obj.get_window_extent()
    inv = ax.transData.inverted()
    p0 = inv.transform((bbox.x0, bbox.y0))
    p1 = inv.transform((bbox.x1, bbox.y1))
    w_units = p1[0] - p0[0]
    if w_units > box_w_units * pad:
        text_obj.set_fontsize(text_obj.get_fontsize() * box_w_units * pad / w_units)


def arrow(x1, y1, x2, y2, color, lw=0.9, z=3):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7,
        lw=lw, color=color, zorder=z, shrinkA=1.5, shrinkB=1.5))


# ============================ backbone row (grey) ===========================
BB_Y, BB_H = 3.15, 0.60
for x, w, label in [
    (0.45, 1.20, "frame $t$"),
    (2.20, 1.60, "pose solve"),
    (4.45, 1.60, "keyframe\ngate"),
    (6.70, 1.60, "window BA"),
    (9.10, 2.45, "Gaussian map"),
]:
    fit_text(box(x, BB_Y, w, BB_H, label, GREY_BG, GREY_ED, fs=7.0), w)
for x1, x2 in [(1.65, 2.20), (3.80, 4.45), (6.05, 6.70), (8.30, 9.10)]:
    arrow(x1, BB_Y + BB_H / 2, x2, BB_Y + BB_H / 2, "#8A8A8A")
ax.text(0.05, 3.88, "MonoGS backbone", fontsize=7.5, color="#8A8A8A",
        fontweight="bold", ha="left")

# =========================== component row (blue) ===========================
CT_Y, CT_H = 1.78, 0.82
fit_text(box(1.40, CT_Y, 2.60, CT_H,
             "robust reweighting (R)\nHuber residual weight",
             BLUE_BG, BLUE_ED, fs=7.0), 2.60)
fit_text(box(4.25, CT_Y, 2.10, CT_H, "uniform keyframe\ncoverage (K)",
             BLUE_BG, BLUE_ED, fs=7.0), 2.10)
fit_text(box(8.90, 1.70, 2.70, 1.10,
             "lineage lifecycle (D)\nconfirm / delete\nnew Gaussians",
             BLUE_BG, BLUE_ED, fs=7.0), 2.70)

arrow(2.95, CT_Y + CT_H, 2.95, BB_Y, BLUE_ED, lw=1.0)      # R -> pose solve
arrow(5.30, CT_Y + CT_H, 5.30, BB_Y, BLUE_ED, lw=1.0)      # K -> keyframe gate
arrow(10.32, 2.80, 10.32, BB_Y, BLUE_ED, lw=1.0)           # D -> map

# ================ reliability signal L: exactly TWO out-edges ==============
fit_text(box(0.25, 0.20, 4.35, 0.86,
             "reliability signal (L)\n$s=(1-e_{\\mathrm{flow}})(1-vg)$",
             "#F5E3CE", ORG, fs=7.2), 4.35)

# site 1: L feeds the residual weight, joining R at the pose solve
arrow(2.95, 1.06, 2.95, CT_Y, ORG, lw=1.3)
ax.text(3.08, (1.06 + CT_Y) / 2, "site 1", fontsize=7.0, color="#8A4E17",
        ha="left", va="center", fontweight="bold")

# site 2: exits L's top at x 4.40, runs through the free corridor y 1.35
# (above the bottom band, below the component row). D sits higher than the
# R/K row, so the final rise 1.35 -> 1.70 gives the head a full shaft.
# One continuous polyline path so the head sits on a full-length shaft
# (a separate 0.2-unit head patch gets eaten by shrinkA/B and detaches).
from matplotlib.path import Path as _Path
site2 = _Path([(4.40, 1.06), (4.40, 1.35), (10.20, 1.35), (10.20, 1.70)],
              [_Path.MOVETO, _Path.LINETO, _Path.LINETO, _Path.LINETO])
ax.add_patch(FancyArrowPatch(path=site2, arrowstyle="-|>",
                             mutation_scale=7, lw=1.3, color=ORG, zorder=3,
                             shrinkA=0, shrinkB=0.5))
ax.text(7.00, 1.41, "site 2", fontsize=7.0, color="#8A4E17", ha="center",
        va="bottom", fontweight="bold")

# ==================== optional semantic mask (dashed) =======================
fit_text(box(5.10, 0.20, 4.20, 0.86,
             "optional semantic mask (person)",
             "white", "#9A9A9A", fs=7.0, ls="--", lw=0.8), 4.20)
ax.text(9.45, 0.63, "combined\nonly", fontsize=7.0, color="#8A8A8A",
        ha="left", va="center", linespacing=1.2)

# The mask's three consumers (audited topology): mapping loss (window BA),
# keyframe-insertion gate, and the tracking residual as a warm-up-only hard
# mask (the path Sec. 5.6 intervenes on). Drawn as ONE dashed bus instead of
# three meandering routes: a single trunk rises from the mask box, one
# horizontal bus runs in the corridor above the component row, and three
# short stubs enter the consumers. Same edges, a fifth of the segments.
# Stubs are SOLID grey: at 0.40 units a (4,2.5) dash phase puts its gap
# exactly at the arrowhead root, which reads as a detached floating head
# (the recurring "empty arrow" defect). The dashed identity of the mask
# route is carried by trunk+bus; the short solid stubs always connect.
from matplotlib.path import Path as _MPath
MASK = "#9A9A9A"
BUS_Y = 2.75
# horizontal bus spans ALL three stub x positions (3.30/5.65/7.80); the trunk
# joins it from the mask box at x=6.55. A bus ending at the trunk leaves the
# x=7.80 stub (window BA) dangling in space.
trunk = _MPath([(6.55, 1.06), (6.55, BUS_Y)],
               [_MPath.MOVETO, _MPath.LINETO])
ax.add_patch(FancyArrowPatch(path=trunk, arrowstyle="-", lw=1.0,
                             color=MASK, zorder=2, linestyle=(0, (4, 2.5)),
                             shrinkA=0, shrinkB=0))
hbus = _MPath([(3.30, BUS_Y), (7.80, BUS_Y)],
              [_MPath.MOVETO, _MPath.LINETO])
ax.add_patch(FancyArrowPatch(path=hbus, arrowstyle="-", lw=1.0,
                             color=MASK, zorder=2, linestyle=(0, (4, 2.5)),
                             shrinkA=0, shrinkB=0))
for x_stub in [3.30, 5.65, 7.80]:
    ax.add_patch(FancyArrowPatch(
        (x_stub, BUS_Y), (x_stub, 3.15), arrowstyle="-|>",
        mutation_scale=5, lw=1.0, color=MASK, zorder=2,
        shrinkA=0, shrinkB=0))

save(fig, "fig1_pipeline_v3")
