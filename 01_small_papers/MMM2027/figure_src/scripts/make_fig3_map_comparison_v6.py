"""Fig. 3 (v6) - what each configuration bakes into the final map.

What the printed v5 got wrong, measured on the delivered PDF:

* TITLE COLLISION. The last two titles were "RoGS-SLAM mask-free" (2.71 cm) and
  "RoGS-SLAM combined" (2.68 cm) over panels only 2.27 cm wide, so each title
  ran into its neighbour's (the audit now measures 18.0 x 8.2 pt of overlap on
  the delivered file).  The arm names now live in the caption's own colour key
  -- the panel titles carry only the arm tag, which fits.
* Every title is now asserted to stay inside its own panel column, and the
  audit checks the titles against each other.

One filmstrip of five panels across the text width, one baseline, one gutter,
one label strip.  Order is the argument: the observed scene at frame 80, the
same room at frame 400 with both movers gone, then each arm's final map
rendered at frame 400 from its own estimated pose.  The backbone's map keeps
the movers' ghost trails; both RoGS-SLAM arms reconstruct the static office,
mask-free without any class label.  Renders are post-hoc assets for
illustration, not a benchmark metric.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from scripts._pubstyle import (C, TEXTWIDTH, apply_style, save_exact, audit,
                               text_w, WIDTH_CM, crop_vertical)

apply_style(font_size=7)

FIG_ROOT = Path(__file__).resolve().parent.parent / "fig2_renders"
BAD, BAD_TX = "#C46A3B", "#8A4E17"

FS_TITLE = 7.0
# (file, line1, line2, colour, bold)  -- the arm name is in line 1 and must fit
# inside one panel column; the caption decodes the colours.
PANELS = [
    ("input_f80.png", "frame 80", "movers present", "#5A5A5A", False),
    ("input_f400.png", "frame 400", "movers gone", "#5A5A5A", False),
    ("vanilla_f400.png", "vanilla", "unmodified", "#5A5A5A", False),
    ("maskfree_f400.png", "mask-free", "ATE 12.1 cm", C["maskfree"], True),
    ("combined_f400.png", "combined", "ATE 3.1 cm", C["combined"], True),
]

N = len(PANELS)
M, G = 0.012, 0.016                     # figure fractions
WP = (1 - 2 * M - (N - 1) * G) / N
IMG_CM = WP * WIDTH_CM * 0.75            # 4:3 renders
TITLE_CM = 2 * FS_TITLE * 1.28 / 72 * 2.54 + 0.10   # two lines + pad
LABEL_CM = TITLE_CM + 0.10
H_CM = IMG_CM + LABEL_CM

# every title must fit its own column
for _, l1, l2, _, _ in PANELS:
    widest = max(text_w(l1, FS_TITLE), text_w(l2, FS_TITLE))
    if widest > WP * WIDTH_CM - 0.04:
        raise SystemExit(f"title {l1!r}/{l2!r} is {widest:.2f} cm, "
                         f"panel is {WP * WIDTH_CM:.2f} cm")

fig = plt.figure(figsize=(TEXTWIDTH, H_CM / 2.54))
HP = IMG_CM / H_CM
# the image strip occupies the bottom IMG_CM; the title strip is the space above
Y_IMG = 0.0

titles = []
for i, (name, l1, l2, col, bold) in enumerate(PANELS):
    ax = fig.add_axes([M + i * (WP + G), Y_IMG, WP, HP])
    ax.imshow(plt.imread(FIG_ROOT / name), aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
        sp.set_color("#B9B9B9" if col == "#5A5A5A" else col)
    t = ax.set_title(f"{l1}\n{l2}", fontsize=FS_TITLE, color=col, pad=2.5,
                     linespacing=1.28,
                     fontweight="bold" if bold else "normal")
    titles.append((t, ax))

# the one cue drawn on a render: the backbone's ghost cluster
ax = fig.axes[2]
ax.add_patch(Ellipse((0.555, 0.60), 0.34, 0.56, transform=ax.transAxes,
                     facecolor="none", edgecolor=BAD, lw=0.9,
                     linestyle=(0, (3, 2)), zorder=7))
ax.annotate("movers' ghost\ntrails baked in", xy=(0.52, 0.42),
            xytext=(0.53, 0.14), xycoords="axes fraction",
            textcoords="axes fraction", ha="center", va="center",
            fontsize=6.6, fontweight="bold", color=BAD_TX, linespacing=1.10,
            arrowprops=dict(arrowstyle="->", color=BAD, lw=0.8, shrinkA=3,
                            shrinkB=2),
            bbox=dict(boxstyle="round,pad=0.24", facecolor="white",
                      edgecolor=BAD, linewidth=0.8, alpha=0.95), zorder=8)

print(f"figure {WIDTH_CM:.2f} x {H_CM:.2f} cm   (v5: 12.20 x 2.41)")
print(f"  panel {WP * WIDTH_CM:.2f} x {IMG_CM:.2f} cm  gutter {G * WIDTH_CM:.2f} cm")
for (_, l1, l2, _, _), (t, _ax) in zip(PANELS, titles):
    print(f"  title {max(text_w(l1, FS_TITLE), text_w(l2, FS_TITLE)):.2f} cm "
          f"in {WP * WIDTH_CM:.2f} cm: {l1!r}")

# check each title against its own panel column, and all titles against others
fig.canvas.draw()
r = fig.canvas.get_renderer()
canvas_w = fig.get_size_inches()[0] * fig.dpi
for i, (t, ax) in enumerate(titles):
    bb = t.get_window_extent(r)
    col_l = (M + i * (WP + G)) * canvas_w
    col_r = (M + i * (WP + G) + WP) * canvas_w
    if bb.x0 < col_l - 0.4 or bb.x1 > col_r + 0.4:
        raise SystemExit(
            f"title {t.get_text().splitlines()[0]!r} spans "
            f"{bb.x0:.1f}..{bb.x1:.1f} px, column is {col_l:.1f}..{col_r:.1f}")

# the ghost annotation must stay inside its own panel, not spill into the
# neighbour: the annotation box is wider than a panel is at this size
for t in fig.axes[2].texts:
    bb = t.get_window_extent(r)
    ab = fig.axes[2].get_window_extent(r)
    if bb.x0 < ab.x0 - 0.4 or bb.x1 > ab.x1 + 0.4:
        raise SystemExit(
            f"annotation {t.get_text().splitlines()[0]!r} spans "
            f"{bb.x0:.1f}..{bb.x1:.1f} px, its panel is "
            f"{ab.x0:.1f}..{ab.x1:.1f}")

crop_vertical(fig)
audit(fig, "fig3", scale=1.0)
save_exact(fig, "fig3_map_comparison_v6")
