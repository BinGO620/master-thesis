"""Fig. 4 (v5) - component necessity is regime-dependent, conventional ablation bars.

What the printed v4 got wrong, measured on the delivered PDF:

* FLOOR. The tick labels were set at 6.0 pt and the legend at 6.2 pt.  Included
  at width=\\textwidth (scale 1.007) those print at 6.04 and 6.24 pt, i.e. on
  or under the venue floor.  Everything now draws at >= 7.0 pt so sub-6 pt
  cannot happen even after rounding.
* The plot area was 0.685 x 0.20..0.885 of a 4.55 cm canvas, leaving 8.5 pt of
  bottom margin for a two-line tick label.  The canvas is now solved from the
  measured label block instead.

Redesign away from the v3 diverging heatmap (reviewer feedback: the heatmap +
support-rule strip read as an analysis artefact, not as a SLAM ablation). The
conventional form is a grouped ATE bar chart: for each sequence, the full
mask-free configuration next to the three single-component removals. Removing
a component that matters lifts its bar; the regime split (which bar lifts
where) is directly visible.

Data (transcription-checked): results/evidence/archive_pre_exp32/
wpa_factorial_readout.md, L2 conditional ATE (mean +/- sd over co-completed
seeds, k=3 everywhere) for the four cells {K1R1L1, K0R1L1, K1R0L1, K1R1L0}.
The removal-effect Delta (mean log-ratio, sd over seeds) is carried only to
mark directional cells under the frozen support rule |mean| >= 1 sd (SI S9).
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from scripts._pubstyle import (C, TEXTWIDTH, apply_style, save_exact, audit,
                               crop_vertical)

apply_style(font_size=7)

FS_TICK = 7.0
FS_LEGEND = 7.0
FS_LABEL = 7.4

SEQS = ["mv_no_box", "mv_no_box2", "pt2", "balloon", "pt1"]
SEQ_TAGS = ["object-only", "object-only", "person", "mixed-mover", "person, hard"]

ARMS = ["full", "w/o K", "w/o R", "w/o L"]
# conditional ATE RMSE (cm), mean, sd over the 3 seeds
ATE_MEAN = np.array([
    [3.28, 4.21, 3.38, 3.93],    # mv_no_box
    [5.12, 9.33, 5.07, 5.85],    # mv_no_box2
    [8.76, 18.65, 8.69, 10.37],  # pt2
    [13.45, 11.21, 29.42, 18.36],  # balloon
    [36.59, 30.15, 55.22, 41.38],  # pt1
])
ATE_SD = np.array([
    [0.40, 0.50, 0.41, 1.17],
    [0.36, 2.11, 0.64, 0.59],
    [0.41, 6.60, 0.90, 0.18],
    [1.43, 1.17, 4.05, 5.12],
    [3.36, 5.20, 2.81, 9.34],
])
# removal-effect mean log-ATE shift and seed sd, from the same readout;
# a removal is directional when |mean| < 1 sd (not marked = supported)
DELTA_MEAN = np.array([
    [0.250, 0.586, 0.719, -0.182, -0.201],   # K
    [0.030, -0.013, -0.011, 0.780, 0.413],   # R
    [0.157, 0.131, 0.170, 0.291, 0.108],     # L
])
DELTA_SD = np.array([
    [0.162, 0.250, 0.309, 0.131, 0.183],
    [0.187, 0.178, 0.147, 0.037, 0.140],
    [0.417, 0.158, 0.048, 0.202, 0.199],
])
for (r, c), v in {(0, 0): "+0.250", (0, 3): "-0.182", (1, 3): "+0.780",
                  (1, 4): "+0.413", (2, 2): "+0.170", (2, 3): "+0.291"}.items():
    assert f"{DELTA_MEAN[r, c]:+.3f}" == v, f"transcription mismatch at {(r, c)}"
# column j of ATE_* is arm j; removal arms 1..3 map to rows 0..2 of DELTA_*
DIRECTIONAL = np.zeros_like(ATE_MEAN, dtype=bool)
for j in range(1, 4):
    for i in range(len(SEQS)):
        DIRECTIONAL[i, j] = abs(DELTA_MEAN[j - 1, i]) < DELTA_SD[j - 1, i]
assert DIRECTIONAL.sum() == 6  # R on 3 easy seqs, L on mv/mv2/pt1

COLORS = ["#1F5C99", "#E69F00", "#4DA198", "#A0529A"]  # full, -K, -R, -L

fig = plt.figure(figsize=(TEXTWIDTH, 5.20 / 2.54))
ax = fig.add_axes([0.115, 0.185, 0.875, 0.700])

x = np.arange(len(SEQS))
w = 0.19
for j, (arm, col) in enumerate(zip(ARMS, COLORS)):
    offs = (j - 1.5) * w
    ax.bar(x + offs, ATE_MEAN[:, j], w * 0.92, color=col,
           edgecolor="white", linewidth=0.4, zorder=2,
           label="full (K·R·L)" if j == 0 else arm)
    ax.errorbar(x + offs, ATE_MEAN[:, j], yerr=ATE_SD[:, j],
                fmt="none", ecolor=C["ink"], elinewidth=0.6, capsize=1.4,
                capthick=0.6, zorder=3)
    for i in range(len(SEQS)):
        if DIRECTIONAL[i, j]:
            ax.plot(x[i] + offs, ATE_MEAN[i, j] + ATE_SD[i, j] * 1.55, "o",
                    ms=2.6, mfc="none", mec=C["ink"], mew=0.6, zorder=4)

ax.set_yscale("log")
ax.set_ylim(2.2, 120)
ax.set_yticks([3, 5, 10, 20, 50, 100])
ax.set_yticklabels(["3", "5", "10", "20", "50", "100"])
ax.set_ylabel("ATE RMSE (cm, log scale)", fontsize=FS_LABEL)
ax.set_xticks(x)
ax.set_xticklabels([f"{s}\n{t}" for s, t in zip(SEQS, SEQ_TAGS)])
ax.tick_params(axis="x", pad=2.5, labelsize=FS_TICK)
ax.tick_params(axis="y", labelsize=FS_TICK)
for lbl in ax.get_xticklabels():
    lbl.set_fontsize(FS_TICK)
    lbl.set_linespacing(1.35)
ax.set_xlim(-0.55, len(SEQS) - 0.45)
ax.grid(axis="y", zorder=0)

proxy = Line2D([], [], marker="o", mfc="none", mec=C["ink"], ls="none",
               ms=3.0, mew=0.6,
               label="removal effect within 1 sd (directional)")
handles, labels = ax.get_legend_handles_labels()
handles.append(proxy)
labels.append(proxy.get_label())
ax.legend(handles, labels, loc="upper left", ncol=1, handlelength=1.1,
          borderaxespad=0.2, labelspacing=0.32, fontsize=FS_LEGEND)

crop_vertical(fig)
audit(fig, "fig4", scale=1.0)
save_exact(fig, "fig4_component_necessity_v5")
