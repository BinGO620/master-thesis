"""Fig. 6 (v5) - one intervention, three pose-side endpoints, opposite signs.

What the printed v4 got wrong, measured on the delivered PDF:

* SCALE. Drawn 333.4 pt wide, included at 0.95\\textwidth, so its 6.4 pt tick
  words ("better", "worse", "0") printed at 6.31 pt -- over the floor but with
  no margin, and visibly the smallest text in the paper.  It is now drawn at
  exactly \\textwidth and included at \\textwidth (scale 1.000), with every
  label at >= 7.0 pt.
* The three panel captions were 6.6 pt and are now 7.4 pt; the value labels
  6.8 -> 7.6 pt.  The panels are given the height those sizes need.

Three small panels, one per endpoint, each in RAW units: zero line, grey band
= +/-1 re-run noise floor, bar = measured shift.  Lower is better for all three
endpoints (per-frame penalty, coherent amplitude, ATE), so each panel reads
left = better, right = worse.

Data (transcription-checked): results/evidence/pose_trackside_ate_gate.md
(shift_ATE = -1.4157, floor_ATE = 0.3519),
pose_trackside_verdict.md (shift_P = +0.0806, floor = 0.0662),
pose_coherent_verdict.md (shift_coherent = -0.0248, floor = 0.0180).
"""
import matplotlib.pyplot as plt

from scripts._pubstyle import (C, TEXTWIDTH, apply_style, save_exact, audit,
                               crop_vertical)

apply_style(font_size=7)

FS_TICK = 7.0
FS_CAP = 7.4
FS_VALUE = 7.6
FS_MULT = 7.0

ENDPOINTS = [
    ("per-frame penalty\n(cm/frame)", +0.0806, 0.0662, "1.22$\\times$ floor"),
    ("coherent amplitude\n(cm)", -0.0248, 0.0180, "1.38$\\times$ floor"),
    ("full-trajectory ATE\n(cm)", -1.4157, 0.3519, "4.0$\\times$ floor"),
]
EXPECT = {0: "+0.0806", 1: "-0.0248", 2: "-1.4157"}
for i, (_, shift, _, _) in enumerate(ENDPOINTS):
    assert f"{shift:+.4f}" == EXPECT[i], f"transcription mismatch at {i}"

PT2CM = 2.54 / 72
# canvas height = plot band + tick row + caption block + breathing room, all
# solved from the sizes above (v4 hard-coded 2.35 cm and clipped the captions).
# Below the axes sit the tick labels and then the caption, so the axes bottom
# is set from their sum, not from the caption alone.
PLOT_CM = 1.55
TICK_CM = FS_TICK * 1.30 * PT2CM + 0.18
CAP_CM = 2 * FS_CAP * 1.30 * PT2CM + 0.26
BELOW_CM = TICK_CM + CAP_CM
H_CM = PLOT_CM + BELOW_CM + 0.06

fig, axes = plt.subplots(1, 3, figsize=(TEXTWIDTH, H_CM / 2.54))
fig.subplots_adjust(left=0.030, right=0.996,
                    top=1.0 - 0.03 / H_CM, bottom=BELOW_CM / H_CM,
                    wspace=0.26)

for ax, (title, shift, floor, mult) in zip(axes, ENDPOINTS):
    lim = max(abs(shift), floor) * 1.75
    ax.axvspan(-floor, floor, color=C["panel_bg"], zorder=0)
    ax.axvline(0, color=C["ink"], lw=0.9, zorder=2)
    col = C["bad"] if shift > 0 else C["good"]
    ax.barh(0, shift, height=0.46, color=col, edgecolor="white",
            linewidth=0.4, zorder=3)
    ax.set_xlim(-lim * 1.30, lim * 1.30)
    ax.set_ylim(-0.68, 0.72)
    ax.set_yticks([])
    ax.set_xticks([-lim, 0, lim])
    ax.set_xticklabels(["better", "0", "worse"], fontsize=FS_TICK)
    ax.set_xlabel(title, fontsize=FS_CAP, labelpad=2.6, linespacing=1.30)
    for sp in ("left", "top", "right"):
        ax.spines[sp].set_visible(False)

    sign = "+" if shift > 0 else "−"
    label = (f"{sign}{abs(shift):.4f}" if abs(shift) < 0.1
             else f"{sign}{abs(shift):.2f}")
    ax.text(0, 0.52, label, ha="center", va="center",
            fontsize=FS_VALUE, fontweight="bold", color=col, zorder=4)
    ax.text(0, -0.52, mult, ha="center", va="center", fontsize=FS_MULT,
            color="#707070", zorder=4)

crop_vertical(fig)
audit(fig, "fig6", scale=1.0)
save_exact(fig, "fig6_pose_endpoints_v5")
