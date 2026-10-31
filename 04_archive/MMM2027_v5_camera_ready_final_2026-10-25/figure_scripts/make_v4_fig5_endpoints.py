"""Fig. 5 (v4) - one intervention, three pose-side endpoints, opposite signs.

Redesign away from the v3 noise-floor-normalised single-axis bars (reviewer
feedback: "shift in units of the endpoint's own noise floor" needed the
caption to decode). Three small panels, one per endpoint, each in RAW units:
zero line, grey band = +/-1 re-run noise floor, bar = measured shift. Lower is
better for all three endpoints (per-frame penalty, coherent amplitude, ATE),
so each panel reads left = better, right = worse.

Data (transcription-checked): results/evidence/pose_trackside_ate_gate.md
(shift_ATE = -1.4157, floor_ATE = 0.3519),
pose_trackside_verdict.md (shift_P = +0.0806, floor = 0.0662),
pose_coherent_verdict.md (shift_coherent = -0.0248, floor = 0.0180).
"""
import matplotlib.pyplot as plt

from _figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=7.4)

ENDPOINTS = [
    ("per-frame penalty\n(cm/frame)", +0.0806, 0.0662, "1.22$\\times$ floor"),
    ("coherent amplitude\n(cm)", -0.0248, 0.0180, "1.38$\\times$ floor"),
    ("full-trajectory ATE\n(cm)", -1.4157, 0.3519, "4.0$\\times$ floor"),
]
EXPECT = {0: "+0.0806", 1: "-0.0248", 2: "-1.4157"}
for i, (_, shift, _, _) in enumerate(ENDPOINTS):
    assert f"{shift:+.4f}" == EXPECT[i], f"transcription mismatch at {i}"

fig, axes = plt.subplots(1, 3, figsize=(TEXTWIDTH, 2.35 / 2.54))
fig.subplots_adjust(left=0.035, right=0.995, top=0.795, bottom=0.20, wspace=0.24)

for ax, (title, shift, floor, mult) in zip(axes, ENDPOINTS):
    lim = max(abs(shift), floor) * 1.75
    ax.axvspan(-floor, floor, color=C["panel_bg"], zorder=0)
    ax.axvline(0, color=C["ink"], lw=0.9, zorder=2)
    col = C["bad"] if shift > 0 else C["good"]
    ax.barh(0, shift, height=0.52, color=col, edgecolor="white",
            linewidth=0.4, zorder=3)
    ax.set_xlim(-lim * 1.3, lim * 1.3)
    ax.set_ylim(-0.62, 0.66)
    ax.set_yticks([])
    ax.set_xticks([-lim, 0, lim])
    ax.set_xticklabels(["better", "0", "worse"], fontsize=6.4)
    ax.set_xlabel(title, fontsize=6.6, labelpad=2.5, linespacing=1.3)
    for sp in ("left", "top", "right"):
        ax.spines[sp].set_visible(False)

    vcol = C["bad"] if shift > 0 else C["good"]
    sign = "+" if shift > 0 else "\u2212"
    label = (f"{sign}{abs(shift):.4f}" if abs(shift) < 0.1
             else f"{sign}{abs(shift):.2f}")
    ax.text(0, 0.44, label, ha="center", va="center",
            fontsize=6.8, fontweight="bold", color=vcol, zorder=4)
    ax.text(0, -0.44, mult, ha="center", va="center", fontsize=6.4,
            color="#707070", zorder=4)

save(fig, "fig5_endpoints_v4")
