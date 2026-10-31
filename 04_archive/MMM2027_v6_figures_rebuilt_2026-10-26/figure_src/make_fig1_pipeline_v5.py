"""Fig. 1 (v5) - where the four components attach to the MonoGS backbone.

Clean-column redesign of v3: all three component boxes sit on one baseline and
one height, each vertical arrow is centred under its backbone consumer, the
reliability signal L routes site 2 along the bottom edge into D, and the
optional semantic mask is a single dashed box that lists its three consumers
(no crowded three-stub bus crossing the component arrows).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as _MPath

from scripts._figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=7)

fig = plt.figure(figsize=(TEXTWIDTH, 4.2 / 2.54))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12.2)
ax.set_ylim(0, 4.2)
ax.axis("off")

BLUE_BG = "#DCE9F5"
BLUE_ED = C["combined"]
ORG = "#B26B2C"
ORG_BG = "#F5E3CE"
GREY_BG = "#EFEFEF"
GREY_ED = "#B9B9B9"
MASK = "#9A9A9A"


def box(x, y, w, h, label, face, edge, fs=7.0, lw=0.9, ls="-", z=2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
        facecolor=face, edgecolor=edge, lw=lw, linestyle=ls, zorder=z))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, color=C["ink"], zorder=z + 1, linespacing=1.15)


def arrow(x1, y1, x2, y2, color, lw=1.0, z=3, ls=None):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7,
        lw=lw, color=color, zorder=z, shrinkA=1.5, shrinkB=1.5,
        linestyle=ls))


# ============================ backbone row (grey) ===========================
BB_Y, BB_H = 3.30, 0.55
for x, w, label in [
    (0.30, 1.20, "frame $t$"),
    (1.70, 1.20, "pose solve"),
    (3.50, 1.10, "keyframe\ngate"),
    (5.20, 1.20, "window BA"),
    (7.90, 1.80, "Gaussian map"),
]:
    box(x, BB_Y, w, BB_H, label, GREY_BG, GREY_ED)
for x1, x2 in [(1.50, 1.70), (2.90, 3.50), (4.60, 5.20), (6.40, 7.90)]:
    arrow(x1, BB_Y + BB_H / 2, x2, BB_Y + BB_H / 2, "#8A8A8A")
ax.text(0.05, 3.97, "MonoGS backbone", fontsize=7.5, color="#8A8A8A",
        fontweight="bold", ha="left")

# =========================== component row (blue) ===========================
CT_Y, CT_H = 1.95, 0.80
box(1.15, CT_Y, 2.30, CT_H,
    "robust reweighting (R)\nHuber residual weight", BLUE_BG, BLUE_ED)
box(2.95, CT_Y, 2.20, CT_H, "uniform keyframe\ncoverage (K)",
    BLUE_BG, BLUE_ED)
box(7.50, CT_Y, 2.60, CT_H,
    "lineage lifecycle (D)\nconfirm / delete\nnew Gaussians", BLUE_BG, BLUE_ED)
arrow(2.30, CT_Y + CT_H, 2.30, BB_Y, BLUE_ED, lw=1.1)   # R -> pose solve
arrow(4.05, CT_Y + CT_H, 4.05, BB_Y, BLUE_ED, lw=1.1)   # K -> keyframe gate
arrow(8.80, CT_Y + CT_H, 8.80, BB_Y, BLUE_ED, lw=1.1)   # D -> map

# ================ reliability signal L: exactly TWO out-edges ==============
box(0.20, 0.15, 3.20, 0.90,
    "reliability signal (L)\n$s=(1-e_{\\mathrm{flow}})(1-vg)$",
    ORG_BG, ORG, fs=7.2)

# site 1: L feeds the tracking residual, joining R at the pose solve
arrow(2.30, 1.05, 2.30, CT_Y, ORG, lw=1.3)
ax.text(2.48, 1.50, "site 1", fontsize=7.0, color="#8A4E17",
        ha="left", va="center", fontweight="bold")

# site 2: exits L's right side, runs along the bottom edge, rises into D
site2 = _MPath([(3.40, 0.60), (3.40, 0.05), (8.80, 0.05), (8.80, CT_Y)],
               [_MPath.MOVETO, _MPath.LINETO, _MPath.LINETO, _MPath.LINETO])
ax.add_patch(FancyArrowPatch(path=site2, arrowstyle="-|>",
                             mutation_scale=7, lw=1.3, color=ORG, zorder=3,
                             shrinkA=0, shrinkB=0.5))
ax.text(8.95, 1.45, "site 2", fontsize=7.0, color="#8A4E17",
        ha="left", va="center", fontweight="bold")

# ==================== optional semantic mask (dashed) =======================
box(4.30, 0.15, 2.60, 0.90,
    "optional semantic mask\n(person, combined only)\n"
    "mapping \\textperiodcentered\\ insertion\n\\textperiodcentered\\ tracking warm-up",
    "white", MASK, fs=6.4, ls="--", lw=0.8)
arrow(5.80, 1.05, 5.80, BB_Y, MASK, lw=0.9, ls=(0, (3, 2)))

save(fig, "fig1_pipeline_v5")
