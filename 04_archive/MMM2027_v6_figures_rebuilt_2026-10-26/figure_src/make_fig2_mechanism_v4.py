"""Fig. 2 (v4) - what each configuration bakes into the final map.

Redesign after the "lines crowded, not aligned" note on the printed v3:

- one grid: the two observation frames sit in the same three-column grid as the
  three maps, sharing one panel width, one gutter and one outer margin, so the
  row-1 pair is centred exactly over the row-2 middle panel instead of being
  centred independently;
- row-1 titles and row-2 labels are plain text in fixed strips of equal height,
  not chips floating inside the images;
- the two "static office reconstructed" overlays are gone. They said the same
  thing twice, covered map content, and the caption already states it. The one
  cue that carries meaning stays: the dashed ellipse and arrow on the
  backbone's ghost trails;
- per-arm ATE moves from an in-image chip into the row-2 label, so nothing is
  drawn on top of a render.

Content unchanged: row 1 is the observed scene at frame 80 (person present) and
frame 400 (both movers gone); row 2 is each arm's final map rendered at frame
400 from its own estimated pose. Renders are post-hoc assets for illustration,
not a benchmark metric.
"""
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import Ellipse

from scripts._figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=7)

FIG_ROOT = Path(__file__).resolve().parent.parent / "fig2_renders"
f80 = plt.imread(FIG_ROOT / "input_f80.png")
f400 = plt.imread(FIG_ROOT / "input_f400.png")
maps = {"vanilla": plt.imread(FIG_ROOT / "vanilla_f400.png"),
        "maskfree": plt.imread(FIG_ROOT / "maskfree_f400.png"),
        "combined": plt.imread(FIG_ROOT / "combined_f400.png")}

import os
H_CM = float(os.environ.get("F3_H", "6.50"))
fig = plt.figure(figsize=(TEXTWIDTH, H_CM / 2.54))

BAD, BAD_TX = "#C46A3B", "#8A4E17"
M, G = 0.009, 0.019                       # outer margin and gutter, in fig width
WP = (1 - 2 * M - 2 * G) / 3              # panel width, shared by both rows
HP = WP * TEXTWIDTH * 0.75 / (H_CM / 2.54)   # 4:3 images
TITLE_H = 0.062                            # fixed text strip per row
COLS = [M + i * (WP + G) for i in range(3)]

Y2 = 0.010                                 # row 2 (maps)
Y1 = Y2 + HP + TITLE_H + 0.026             # row 1 (observations)
assert Y1 + HP <= 0.995, f"row 1 overflows the canvas: {Y1 + HP:.3f}"

labels = {"vanilla": ("vanilla (unmodified)", "#5A5A5A"),
          "maskfree": ("RoGS-SLAM mask-free", C["maskfree"]),
          "combined": ("RoGS-SLAM combined", C["combined"])}
ates = {"maskfree": "ATE 12.1 cm", "combined": "ATE 3.1 cm"}


def panel(x, y, im, title, color, bold=True):
    ax = fig.add_axes([x, y, WP, HP])
    ax.imshow(im, aspect="auto")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
        sp.set_color("#B9B9B9" if color == "#5A5A5A" else color)
    ax.set_title(title, fontsize=6.6, color=color, pad=3.0,
                 fontweight="bold" if bold else "normal")
    return ax


# ---- row 1: the movers, then gone. The pair is centred over the row-2 grid so
# the two rows share one visual axis; a pair flush left would leave a third of
# the row-1 band empty.
X1 = (1 - (2 * WP + G)) / 2
for i, (im, tag) in enumerate(((f80, "frame 80: movers present"),
                               (f400, "frame 400: movers gone"))):
    panel(X1 + i * (WP + G), Y1, im, tag, "#5A5A5A")

# ---- row 2: the three final maps, one column each
for i, (key, im) in enumerate(maps.items()):
    lab, col = labels[key]
    title = f"{lab}  ({ates[key]})" if key in ates else lab
    ax = panel(COLS[i], Y2, im, title, col)

# the one cue worth drawing: the backbone's ghost cluster
ax = fig.axes[2]
ax.add_patch(Ellipse((0.555, 0.60), 0.34, 0.56, transform=ax.transAxes,
                     facecolor="none", edgecolor=BAD, lw=1.0,
                     linestyle=(0, (3, 2)), zorder=7))
ax.annotate("movers' ghost\ntrails baked in", xy=(0.42, 0.38),
            xytext=(0.20, 0.14), xycoords="axes fraction",
            textcoords="axes fraction", ha="center", va="center",
            fontsize=6.4, fontweight="bold", color=BAD_TX, linespacing=1.05,
            arrowprops=dict(arrowstyle="->", color=BAD, lw=0.9, shrinkA=4,
                            shrinkB=2),
            bbox=dict(boxstyle="round,pad=0.28", facecolor="white",
                      edgecolor=BAD, linewidth=0.9, alpha=0.92), zorder=8)

print(f"figure {TEXTWIDTH*2.54:.2f} x {H_CM:.2f} cm")
print(f"  panel w={WP*TEXTWIDTH*2.54:.2f} cm  h={HP*H_CM:.2f} cm"
      f"  gutter={G*TEXTWIDTH*2.54:.2f} cm  margin={M*TEXTWIDTH*2.54:.2f} cm")
print(f"  row1 y={Y1:.3f}..{Y1+HP:.3f}  row2 y={Y2:.3f}..{Y2+HP:.3f}")
print(f"  row1 spans x={X1:.3f}..{X1+2*WP+G:.3f}"
      f"  row2 spans x={COLS[0]:.3f}..{COLS[2]+WP:.3f}"
      f"  row1 centre {(X1+WP+G/2):.3f} row2 centre {(COLS[0]+COLS[2]+WP)/2:.3f}")
save(fig, "fig3_map_comparison_v4")
