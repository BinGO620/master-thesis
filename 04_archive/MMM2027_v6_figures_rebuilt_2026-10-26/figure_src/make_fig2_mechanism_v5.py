"""Fig. 2 (v5) - what each configuration bakes into the final map.

One row of five panels instead of two rows. The printed v3 stacked two rows of
4:3 frames; at the panel width needed for five cells the frame height is 2.0 cm,
so the whole figure is 2.9 cm instead of 6.4 cm. The v3 second observation frame
(frame 400, movers gone) is dropped: "the movers are gone by frame 400" belongs
in the caption, and the render is of frame 400 anyway, so the empty room is
already visible in all three maps.

Panels are one equal-width row with one gutter, so the observations and the maps
share a single visual axis. Labels are plain text under each panel in a fixed
strip rather than chips drawn inside the images; only the annotation that
carries meaning sits on a render (the ghost-trail ellipse and its arrow).

Row content: the observed scene at frame 80 (person present), then each arm's
final map rendered at frame 400 from its own estimated pose. The backbone's map
keeps the movers' ghost trails; both RoGS-SLAM configurations reconstruct the
static office, mask-free without any class label. Renders are post-hoc assets
for illustration, not a benchmark metric.
"""
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import Ellipse

from scripts._figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=7)

FIG_ROOT = Path(__file__).resolve().parent.parent / "fig2_renders"
# two-line labels, one slot per line for all four panels, so the row reads
# evenly: what the panel is, then what separates it from its neighbours
PANELS = [
    ("input_f80.png", "frame 80\nmovers present", "#5A5A5A"),
    ("vanilla_f400.png", "vanilla\nunmodified", "#5A5A5A"),
    ("maskfree_f400.png", "RoGS-SLAM mask-free\nATE 12.1 cm", C["maskfree"]),
    ("combined_f400.png", "RoGS-SLAM combined\nATE 3.1 cm", C["combined"]),
]

N = len(PANELS)
M, G = 0.006, 0.014                      # outer margin, gutter (fractions of W)
WP = (1 - 2 * M - (N - 1) * G) / N
IMG_CM = WP * TEXTWIDTH * 2.54 * 0.75     # 4:3 images
LABEL_CM = 0.92                           # text strip under each panel
H_CM = IMG_CM + LABEL_CM

fig = plt.figure(figsize=(TEXTWIDTH, H_CM / 2.54))
HP = IMG_CM / H_CM                        # image height, in figure fractions
Y_IMG = 1.0 - HP - 0.02

BAD, BAD_TX = "#C46A3B", "#8A4E17"
for i, (name, label, col) in enumerate(PANELS):
    x = M + i * (WP + G)
    ax = fig.add_axes([x, Y_IMG, WP, HP])
    ax.imshow(plt.imread(FIG_ROOT / name), aspect="auto")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
        sp.set_color("#B9B9B9" if col == "#5A5A5A" else col)
    ax.set_title(label, fontsize=6.4, color=col, pad=2.5, linespacing=1.25,
                 fontweight="bold" if i > 1 else "normal")

# the backbone's ghost cluster, the only cue drawn on a render
ax = fig.axes[1]
ax.add_patch(Ellipse((0.555, 0.60), 0.34, 0.56, transform=ax.transAxes,
                     facecolor="none", edgecolor=BAD, lw=0.9,
                     linestyle=(0, (3, 2)), zorder=7))
ax.annotate("movers' ghost\ntrails baked in", xy=(0.42, 0.36),
            xytext=(0.22, 0.10), xycoords="axes fraction",
            textcoords="axes fraction", ha="center", va="center",
            fontsize=6.0, fontweight="bold", color=BAD_TX, linespacing=1.05,
            arrowprops=dict(arrowstyle="->", color=BAD, lw=0.8, shrinkA=3,
                            shrinkB=2),
            bbox=dict(boxstyle="round,pad=0.24", facecolor="white",
                      edgecolor=BAD, linewidth=0.8, alpha=0.92), zorder=8)

print(f"figure {TEXTWIDTH*2.54:.2f} x {H_CM:.2f} cm")
print(f"  panel {WP*TEXTWIDTH*2.54:.2f} x {IMG_CM:.2f} cm"
      f"  gutter {G*TEXTWIDTH*2.54:.2f} cm  margin {M*TEXTWIDTH*2.54:.2f} cm")
print(f"  row spans x={M:.3f}..{M+N*WP+(N-1)*G:.3f}")
save(fig, "fig2_reliability_v5")
