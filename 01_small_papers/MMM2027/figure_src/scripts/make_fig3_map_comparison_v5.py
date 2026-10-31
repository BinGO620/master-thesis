"""Fig. 3 (v5) - what each configuration bakes into the final map.

One filmstrip of five panels across the text width, instead of a 3-column grid
of two rows. At full width the old grid is 6.5 cm tall, which pushes the body
over its page budget; a single row is 2.4 cm and each panel still comes out at
2.3 cm wide, the same as the printed 3-column version (2.6 cm) once that was
scaled to 0.68\\textwidth.

The alignment problem disappears with the second row: one baseline for all five
panels, one gutter, one label strip, so every label sits at the same height and
every panel edge lines up. Titles are two-line in a fixed slot (what the panel
is, then how it reads) so the strip is even.

Order is the argument: the observed scene at frame 80, the same room at frame
400 with both movers gone, then each arm's final map rendered at frame 400 from
its own estimated pose. The backbone's map keeps the movers' ghost trails; both
RoGS-SLAM arms reconstruct the static office, mask-free without any class label.
Renders are post-hoc assets for illustration, not a benchmark metric.
"""
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import Ellipse

from scripts._figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=7)

FIG_ROOT = Path(__file__).resolve().parent.parent / "fig2_renders"
BAD, BAD_TX = "#C46A3B", "#8A4E17"
PANELS = [
    ("input_f80.png", "frame 80\nmovers present", "#5A5A5A"),
    ("input_f400.png", "frame 400\nmovers gone", "#5A5A5A"),
    ("vanilla_f400.png", "vanilla\nunmodified", "#5A5A5A"),
    ("maskfree_f400.png", "RoGS-SLAM mask-free\nATE 12.1 cm", C["maskfree"]),
    ("combined_f400.png", "RoGS-SLAM combined\nATE 3.1 cm", C["combined"]),
]

N = len(PANELS)
M, G = 0.006, 0.014
WP = (1 - 2 * M - (N - 1) * G) / N
IMG_CM = WP * TEXTWIDTH * 2.54 * 0.75      # 4:3 renders
LABEL_CM = 0.86
H_CM = IMG_CM + LABEL_CM

fig = plt.figure(figsize=(TEXTWIDTH, H_CM / 2.54))
HP = IMG_CM / H_CM
Y_IMG = 1.0 - HP - 0.015

for i, (name, label, col) in enumerate(PANELS):
    ax = fig.add_axes([M + i * (WP + G), Y_IMG, WP, HP])
    ax.imshow(plt.imread(FIG_ROOT / name), aspect="auto")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
        sp.set_color("#B9B9B9" if col == "#5A5A5A" else col)
    ax.set_title(label, fontsize=7.0, color=col, pad=2.5, linespacing=1.25,
                 fontweight="bold" if i > 1 else "normal")

# the one cue drawn on a render: the backbone's ghost cluster
ax = fig.axes[2]
ax.add_patch(Ellipse((0.555, 0.60), 0.34, 0.56, transform=ax.transAxes,
                     facecolor="none", edgecolor=BAD, lw=0.9,
                     linestyle=(0, (3, 2)), zorder=7))
ax.annotate("movers' ghost\ntrails baked in", xy=(0.44, 0.38),
            xytext=(0.24, 0.09), xycoords="axes fraction",
            textcoords="axes fraction", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color=BAD_TX, linespacing=1.05,
            arrowprops=dict(arrowstyle="->", color=BAD, lw=0.8, shrinkA=3,
                            shrinkB=2),
            bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                      edgecolor=BAD, linewidth=0.8, alpha=0.93), zorder=8)

print(f"figure {TEXTWIDTH*2.54:.2f} x {H_CM:.2f} cm  (old 3-column grid: 6.50 cm)")
print(f"  panel {WP*TEXTWIDTH*2.54:.2f} x {IMG_CM:.2f} cm"
      f"  gutter {G*TEXTWIDTH*2.54:.2f} cm")
save(fig, "fig3_map_comparison_v5")
