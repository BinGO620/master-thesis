"""Fig. 2 (v4) - the reliability signal's computation, one compact flow.

Zoom-in of Fig. 1's orange box for Sec. 3.4: from the two flow fields to the
per-pixel weight and its two consumption sites. Same visual language as
fig1_pipeline_v3 (grey backbone, orange reliability, three-row layout).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as _MPath

from scripts._figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=6.5)

fig = plt.figure(figsize=(TEXTWIDTH * 0.92, 2.75 / 2.54))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12.2)
ax.set_ylim(0, 2.75)
ax.axis("off")

ORG, ORG_BG = "#B26B2C", "#F5E3CE"
GREY_BG, GREY_ED = "#EFEFEF", "#B9B9B9"


def box(x, y, w, h, label, face, edge, fs=6.5, lw=0.9, ls="-", z=2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
        facecolor=face, edgecolor=edge, lw=lw, linestyle=ls, zorder=z))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, color=C["ink"], zorder=z + 1, linespacing=1.15)


def arrow(x1, y1, x2, y2, color, lw=1.0, z=3):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7,
        lw=lw, color=color, zorder=z, shrinkA=1.5, shrinkB=1.5))


# ---- row 1: inputs (grey) ----
box(0.10, 1.95, 1.70, 0.66, "frame $t$\ndepth, pose", GREY_BG, GREY_ED)
box(2.60, 1.95, 2.35, 0.66, "observed flow\n$f_{\\mathrm{obs}}$, frozen RAFT",
    GREY_BG, GREY_ED, fs=6.2)
box(5.30, 1.95, 2.70, 0.66, "rigid flow\n$f_{\\mathrm{static}}$, reprojection",
    GREY_BG, GREY_ED, fs=6.2)
arrow(1.80, 2.28, 2.60, 2.28, "#8A8A8A")
feed = _MPath([(1.00, 2.61), (1.00, 2.70), (6.40, 2.70), (6.40, 2.61)],
              [_MPath.MOVETO, _MPath.LINETO, _MPath.LINETO, _MPath.LINETO])
ax.add_patch(FancyArrowPatch(path=feed, arrowstyle="-|>", mutation_scale=6,
                             lw=0.9, color="#8A8A8A", zorder=2,
                             shrinkA=0, shrinkB=0))

# ---- row 2: reliability computation (orange) ----
box(3.30, 0.95, 2.10, 0.76, "disagreement\nrobust MAD\nnormalise", ORG_BG, ORG)
arrow(3.60, 1.95, 4.00, 1.71, ORG)
arrow(6.40, 1.95, 5.05, 1.71, ORG)
box(5.95, 0.95, 2.10, 0.76, "cue\n$e_{\\mathrm{flow}} \\in [0,1]$", ORG_BG, ORG)
arrow(5.40, 1.33, 5.95, 1.33, ORG)
box(8.45, 0.95, 3.15, 0.76, "static confidence $s$\nCauchy weight (floor 0.10)", ORG_BG, ORG, fs=6.2)
arrow(8.05, 1.33, 8.45, 1.33, ORG)

# geometric cue g: dashed grey edge from the frame box into the s box
# (s = (1-e_flow)(1-vg) combines the two cues; g must not point into the
# e_flow box, which is the flow-disagreement cue alone)
gpath = _MPath([(0.95, 1.95), (0.95, 1.83), (9.50, 1.83), (9.50, 1.71)],
               [_MPath.MOVETO, _MPath.LINETO, _MPath.LINETO, _MPath.LINETO])
ax.add_patch(FancyArrowPatch(path=gpath, arrowstyle="-|>", mutation_scale=6,
                             lw=0.8, color="#9A9A9A", zorder=2,
                             linestyle=(0, (3, 2)), shrinkA=0, shrinkB=0))
ax.text(2.00, 1.83, "geometric cue $g$",
        fontsize=6.0, color="#8A8A8A", ha="center", va="center", zorder=4,
        bbox=dict(facecolor="white", edgecolor="none", pad=0.5))

# ---- row 3: the two consumption sites (boxed) ----
box(4.05, 0.10, 3.50, 0.52, "site 2: lifecycle confirmation",
    "white", ORG, fs=6.2, ls=(0, (3, 2)))
box(8.95, 0.10, 3.00, 0.52, "site 1: tracking residual",
    "white", ORG, fs=6.2, ls=(0, (3, 2)))
arrow(10.40, 0.95, 10.45, 0.62, ORG)
s2 = _MPath([(8.90, 0.95), (8.90, 0.78), (5.80, 0.78), (5.80, 0.62)],
            [_MPath.MOVETO, _MPath.LINETO, _MPath.LINETO, _MPath.LINETO])
ax.add_patch(FancyArrowPatch(path=s2, arrowstyle="-|>", mutation_scale=6,
                             lw=1.0, color=ORG, zorder=3, shrinkA=0, shrinkB=0))

save(fig, "fig_reliability_v4")
