"""Fig. 4 (v4) - two controlled comparisons, conventional forms.

Redesign away from the v3 strip-plot + annotated scatter (reviewer feedback:
both panels needed the caption to decode). Panel (a) is now the standard
three-arm ablation bar chart: same frozen flow, three consumers (none / naive
p90 threshold / our weighting), ATE bars with per-seed dots. The verdict cell
(pt2: naive worse than vanilla, ours 5x better) is visible without any
annotation beyond value labels. Panel (b) keeps the boundary separation
scatter but strips it to its message: two non-overlapping groups, one gap.

Data: panel (a) reads results/runs_remote_cache/WPB/WPB-CONFIRM per-seed
tracking_raw.csv (36 runs, as v3 did); panel (b) reuses the transcription-
checked 18 + 5 points of make_v3_fig45_combined.py, sourced from
results/evidence/rpe_stratification_rule_test.{json,md} +
rpe_boundary_heldout.{json,md}.
"""
import csv, glob

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from _figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=9.0)

SEQ = ["pt1", "pt2", "mv_no_box2", "balloon2"]
ARMS = [("vanilla", "vanilla (no flow)", C["vanilla"]),
        ("flowmask", "naive p90, same flow", C["naive"]),
        ("MRCS", "ours, same flow", C["combined"])]

# Per-seed ATE RMSE (cm), transcribed from
# results/runs_remote_cache/WPB/WPB-CONFIRM/{arm}_{seq}_{seed}/tables/tracking_raw.csv
# (last row, column ate_rmse_cm). 36 runs, 3 arms x 4 sequences x 3 seeds.
# Inlined because the run cache was pruned from the working tree; the values are
# the ones that produced the published figure (verified unchanged on 2026-10-25
# against the 2026-09-01 results archive).
SEED_ATE = {
    "pt1|vanilla": [76.92, 55.63, 57.10],
    "pt1|flowmask": [62.11, 39.76, 52.36],
    "pt1|MRCS": [41.54, 37.49, 36.51],
    "pt2|vanilla": [45.15, 43.45, 47.50],
    "pt2|flowmask": [61.84, 39.67, 51.69],
    "pt2|MRCS": [9.40, 8.78, 9.09],
    "mv_no_box2|vanilla": [6.88, 5.88, 34.16],
    "mv_no_box2|flowmask": [6.61, 5.74, 6.35],
    "mv_no_box2|MRCS": [4.90, 4.71, 5.29],
    "balloon2|vanilla": [23.39, 24.40, 24.50],
    "balloon2|flowmask": [31.10, 11.37, 27.44],
    "balloon2|MRCS": [14.23, 10.92, 10.54],
}


def seed_ates(seq, arm):
    return np.array(SEED_ATE[f"{seq}|{arm}"])


D = {(s, a): seed_ates(s, a) for s, _ in [(x, None) for x in SEQ] for a, _, _ in ARMS}

# ---- boundary data (transcription-checked, identical to v3) ----
DEV = [
    ("f2_xyz", 0.222, 0.99, "redundant"), ("f3_office", 0.456, 1.02, "redundant"),
    ("f2_person", 0.498, 0.92, "redundant"), ("f1_desk", 0.847, 1.07, "redundant"),
    ("f3_st_xyz", 0.910, 0.57, "redundant"), ("mv_no_box", 1.210, 1.17, "redundant"),
    ("f3_st_rpy", 1.465, 1.02, "redundant"), ("mv_no_box2", 1.521, 1.09, "redundant"),
    ("pt2", 1.572, 0.89, "redundant"), ("f3_st_hf", 1.041, 1.21, "ambiguous"),
    ("f3_wk_xyz", 1.717, 8.76, "necessary"), ("balloon", 2.028, 3.96, "necessary"),
    ("f3_wk_rpy", 2.264, 3.41, "necessary"), ("f3_wk_hf", 2.327, 5.27, "necessary"),
    ("crowd", 2.643, 15.24, "necessary"), ("balloon2", 2.730, 1.92, "necessary"),
    ("pt1", 2.894, 2.73, "necessary"), ("crowd2", 2.980, 20.95, "necessary"),
]
HELD = [("obox2", 2.068, 1.62, "necessary"), ("synchronous", 2.424, 138.97, "necessary"),
        ("f2_desk_wp", 0.602, 0.94, "redundant"), ("f3_loh", 0.456, 1.09, "redundant"),
        ("obox", 2.117, 1.42, "in-band")]
TAU, BAND = 1.6445, (1.572, 1.717)

fig = plt.figure(figsize=(TEXTWIDTH, 4.55 / 2.54))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.06],
                      left=0.105, right=0.988, top=0.935, bottom=0.135,
                      hspace=0.52)

# ====================== (a) three-arm bar chart =============================
ax = fig.add_subplot(gs[0])
x = np.arange(len(SEQ))
w = 0.26
for j, (key, label, col) in enumerate(ARMS):
    offs = (j - 1) * w
    means = [np.mean(D[(s, key)]) for s in SEQ]
    sds = [np.std(D[(s, key)]) for s in SEQ]
    ax.bar(x + offs, means, w * 0.9, color=col, edgecolor="white",
           linewidth=0.4, zorder=2, label=label)
    ax.errorbar(x + offs, means, yerr=sds, fmt="none", ecolor=C["ink"],
                elinewidth=0.6, capsize=1.4, capthick=0.6, zorder=3)
    for i, s in enumerate(SEQ):
        seeds = D[(s, key)]
        ax.plot(np.full(3, x[i] + offs) + np.linspace(-0.035, 0.035, 3),
                seeds, "o", ms=1.9, mfc="white", mec=C["ink"], mew=0.5, zorder=4)
        ax.text(x[i] + offs, (means[i] + sds[i]) * 1.22, f"{means[i]:.1f}",
                ha="center", va="bottom", fontsize=8.4, color=C["ink"], zorder=5)

ax.set_yscale("log")
ax.set_ylim(3, 500)
ax.set_yticks([5, 10, 20, 50, 100, 200])
ax.set_yticklabels(["5", "10", "20", "50", "100", "200"])
ax.set_ylabel("ATE RMSE (cm)")
ax.set_xticks(x)
ax.set_xticklabels(SEQ)
ax.set_xlim(-0.55, len(SEQ) - 0.45)
ax.grid(axis="y", zorder=0)
ax.legend(loc="upper center", ncol=3, handlelength=1.0, columnspacing=1.1,
          borderaxespad=0.15, labelspacing=0.3, fontsize=8.4)
from _figstyle_v3 import panel_label
panel_label(ax, "a", x=-0.055, size=9.0)

# ====================== (b) boundary separation =============================
ax2 = fig.add_subplot(gs[1])
ax2.axvspan(*BAND, color=C["panel_bg"], zorder=0)
ax2.axvline(TAU, color="#909090", lw=0.7, ls="--", zorder=1)

groups = {"redundant": ([], [], []), "necessary": ([], [], []),
          "ambiguous": ([], [], [])}
for name, rpe, n, g in DEV:
    groups[g][0].append(rpe)
    groups[g][1].append(n)
    groups[g][2].append(name)
MARK = {"redundant": ("o", C["redundant"]), "necessary": ("D", C["necessary"]),
        "ambiguous": ("^", "#8C8C8C")}
for g, (mk, col) in MARK.items():
    xs, ys, _ = groups[g]
    edge_col, mew = (C["ink"], 0.9) if g == "ambiguous" else ("white", 0.4)
    ax2.plot(xs, ys, mk, ms=4.0 if mk != "^" else 4.6, mfc=col, mec=edge_col,
             mew=mew, ls="none", zorder=3)
xs_held = [r for _, r, n, g in HELD]
ys_held = [n for _, r, n, g in HELD]
ax2.plot(xs_held, ys_held, "o", ms=5.2, mfc="none", mec=C["ink"], mew=0.8,
         ls="none", zorder=4)
ax2.plot([], [], "o", ms=4.2, mfc="none", mec=C["ink"], mew=0.8, ls="none",
         label="held-out check (5)")

for name, rpe, n, g in DEV:
    if name in ("crowd", "f3_st_hf"):
        dy = 1.5 if g != "ambiguous" else 0.62
        ax2.annotate(name, (rpe, n), xytext=(rpe + 0.07, n * dy),
                     fontsize=8.4, color="#606060", zorder=5)

ax2.set_yscale("log")
ax2.set_ylim(0.45, 400)
ax2.set_xlim(0.0, 3.25)
ax2.set_yticks([0.5, 1, 2, 5, 10, 20, 50, 100])
ax2.set_yticklabels(["0.5", "1", "2", "5", "10", "20", "50", "100"])
ax2.set_ylabel("mask necessity $N$")
ax2.set_xlabel("mask-free arm's own RPE (cm/frame)")
ax2.grid(axis="y", zorder=0)
ax2.text(BAND[1] * 1.06, 0.52, "gap", fontsize=8.4, color="#909090",
         ha="left", va="bottom")

handles, _ = ax2.get_legend_handles_labels()   # the held-out proxy line
GROUP_LAB = {"redundant": "mask redundant (9)", "necessary": "mask necessary (8)",
             "ambiguous": "ambiguous, excluded (1)"}
N_G = {"redundant": 9, "necessary": 8, "ambiguous": 1}
for g, (mk, col) in MARK.items():
    edge_col, mew = (C["ink"], 0.9) if g == "ambiguous" else ("white", 0.4)
    handles.append(Line2D([], [], marker=mk, ms=4.4, mfc=col, mec=edge_col,
                          mew=mew, ls="none", label=GROUP_LAB[g]))
ax2.legend(handles, [h.get_label() for h in handles], loc="upper left",
           ncol=2, handlelength=0.9, columnspacing=0.8, borderaxespad=0.2,
           labelspacing=0.3, fontsize=8.4, handletextpad=0.4)
panel_label(ax2, "b", x=-0.055, size=9.0)

save(fig, "fig4_controlled_v4")
