"""Fig. 2 (v3) - what each configuration bakes into the final map.

2026-08-30 redesign v3 (comprehension-first): the reader must SEE the movers
before seeing what the maps keep of them.

- row 1: the observed scene at two times — frame 80 (the person mid-sequence;
  a balloon she plays with stays near the ceiling, mostly out of frame) and
  frame 400 (both movers gone). Same room, ~5 minutes apart.
- row 2: each arm's FINAL map rendered at frame 400 from its own estimated
  pose. The backbone's map is shredded by the movers' ghost trails; both
  RoGS-SLAM configurations reconstruct the static office — mask-free without
  any class label. The two arms' maps are similar here; they differ in
  tracking stability (ATE 12.1 vs 3.1 cm), which the caption states.

Renders: RTX 3090 posthoc pipeline (P11-REMEDIAL vanilla/mask-free, P2-T
combined); illustration asset, not a benchmark metric.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from scripts._figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=7)

fig_root = Path("/tmp/figsrc") / "fig2_renders"
f80 = plt.imread(fig_root / "input_f80.png")
f400 = plt.imread(fig_root / "input_f400.png")
maps = {"vanilla": plt.imread(fig_root / "vanilla_f400.png"),
        "maskfree": plt.imread(fig_root / "maskfree_f400.png"),
        "combined": plt.imread(fig_root / "combined_f400.png")}

FIG_H = 6.2 / 2.54
FIG_W = TEXTWIDTH
fig = plt.figure(figsize=(FIG_W, FIG_H))

# ---- row 1: the movers, then gone. Neutral grey time chips: the style guide
# reserves blue/orange for good/bad cues — no green, no red anywhere.
# W1 is sized so row 1 (H1 = W1*aspect) clears row 2's top (Y2+H2 = 0.459):
# H1 <= 1 - 0.012 - 0.459 - 0.02 gap  =>  W1 <= 0.367 at this figure aspect.
W1 = 0.36                       # two observed cells side by side
H1 = W1 * FIG_W * 0.75 / FIG_H  # 4:3 frames
Y1 = 1.0 - 0.012 - H1
X0 = (1 - (2 * W1 + 0.024)) / 2   # centre the pair
for i, (im, tag) in enumerate((
        (f80,  "frame 80 — movers present"),
        (f400, "frame 400 — movers gone"))):
    ax = fig.add_axes([X0 + i * (W1 + 0.024), Y1, W1, H1])
    ax.imshow(im, aspect="auto")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.7); sp.set_color("#B9B9B9")
    ax.set_title(tag, fontsize=6.6, fontweight="bold", color="#5A5A5A",
                 pad=2.0,
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#EFEFEF",
                           edgecolor="none"))

# ---- row 2: the three final maps. Orange = the failure (ghost trails),
# deep blue = the recovered static office; per-arm ATE annotated in-panel so
# the equal-looking maps don't hide the tracking gap the caption states.
from matplotlib.patches import Ellipse
BAD, BAD_TX = "#C46A3B", "#8A4E17"          # orange = failure being shown
W2 = (1 - 2 * 0.012 - 2 * 0.024) / 3
H2 = W2 * FIG_W * 0.75 / FIG_H
Y2 = 0.030
labels = {"vanilla": ("vanilla (unmodified)", "#5A5A5A"),
          "maskfree": ("RoGS-SLAM mask-free", C["maskfree"]),
          "combined": ("RoGS-SLAM combined", C["combined"])}
ates = {"maskfree": "ATE 12.1 cm", "combined": "ATE 3.1 cm"}
for i, (key, im) in enumerate(maps.items()):
    ax = fig.add_axes([0.012 + i * (W2 + 0.024), Y2, W2, H2])
    ax.imshow(im, aspect="auto")
    ax.set_xticks([]); ax.set_yticks([])
    lab, col = labels[key]
    for sp in ax.spines.values():
        sp.set_linewidth(1.5 if key != "vanilla" else 1.1)
        sp.set_color(col)
    ax.set_xlabel(lab, fontsize=6.4, fontweight="bold", color=col,
                  labelpad=1.5)
    if key == "vanilla":
        # circle the ghost cluster (desk/chair streaks) and point the label at it
        ax.add_patch(Ellipse((0.555, 0.60), 0.34, 0.56, transform=ax.transAxes,
                             facecolor="none", edgecolor=BAD, lw=1.0,
                             linestyle=(0, (3, 2)), zorder=7))
        ax.annotate("movers' ghost\ntrails baked in",
                    xy=(0.42, 0.38), xytext=(0.24, 0.17),
                    xycoords="axes fraction", textcoords="axes fraction",
                    ha="center", va="center",
                    fontsize=6.4, fontweight="bold", color=BAD_TX,
                    linespacing=1.0,
                    arrowprops=dict(arrowstyle="->", color=BAD, lw=0.9,
                                    shrinkA=4, shrinkB=2),
                    bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                              edgecolor=BAD, linewidth=0.9, alpha=0.92),
                    zorder=8)
    else:
        ax.text(0.5, 0.42, "static office\nreconstructed",
                transform=ax.transAxes, ha="center", va="center",
                fontsize=6.4, fontweight="bold", color=C["combined"],
                linespacing=1.0,
                bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                          edgecolor=C["combined"], linewidth=0.9, alpha=0.88),
                zorder=8)
        ax.text(0.05, 0.94, ates[key], transform=ax.transAxes,
                ha="left", va="top", fontsize=6.0, fontweight="bold",
                color=C["combined"],
                bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                          edgecolor=C["combined"], linewidth=0.7, alpha=0.88),
                zorder=8)

save(fig, "fig2_mechanism_v3")
