#!/usr/bin/env python3
"""fig5_ablation_bars.py — 致密化消融柱状图（论文 Ch5 动机，Ch3 复用）

数据源：results/densification_ablation/（Phase 0，7 臂×3 seed，
moving_obstructing_box 非标准序列——图中注明不可横向比较）。
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

MONOGS = "/data/monogs-ours/results/densification_ablation"
OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "03_results", "figures")
)

ARMS = [
    ("A0\n默认", "A0_default_seed{}", "#888888"),
    ("A1\n延迟", "A1_late_densify_seed{}", "#4f81bd"),
    ("A2\n高阈值", "A2_high_threshold_seed{}", "#c0504d"),
    ("A3\n高频", "A3_frequent_update_seed{}", "#c0504d"),
    ("A4\n激进clone", "A4_aggressive_clone_seed{}", "#2e8b57"),
    ("A5\n保守split", "A5_conservative_split_seed{}", "#c0504d"),
    ("A6\n禁用", "A6_no_densification_seed{}", "#c0504d"),
]

means, stds = [], []
for _, pat, _ in ARMS:
    vals = []
    for s in range(3):
        f = f"{MONOGS}/{pat.format(s)}/tables/tracking_raw.csv"
        rows = list(csv.DictReader(open(f)))
        vals.append(float(rows[-1]["ate_rmse_cm"]))
    m = sum(vals) / 3
    sd = (sum((v - m) ** 2 for v in vals) / 3) ** 0.5
    means.append(m)
    stds.append(sd)

fig, ax = plt.subplots(figsize=(8, 4.0))
xs = range(len(ARMS))
ax.bar(xs, means, yerr=stds, capsize=3,
       color=[c for _, _, c in ARMS], width=0.62)
for x, m in zip(xs, means):
    ax.text(x, m + 1.2, f"{m:.1f}", ha="center", fontsize=9)
ax.axhline(means[0], color="#888888", ls=":", lw=1.2)
ax.text(6.4, means[0] + 1.0, "A0 对照", fontsize=8, color="#888888", ha="right")
ax.set_xticks(list(xs))
ax.set_xticklabels([n for n, _, _ in ARMS], fontsize=8.5)
ax.set_ylabel("ATE RMSE (cm)")
ax.set_title("致密化消融（Phase 0，moving_obstructing_box 诊断序列×3 seed：\n抑制致密化全错，激进 clone −29% —— 诊断性相对信号，不可与标准子集横向比较）",
             fontsize=9)
ax.set_ylim(0, 70)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig5_densification_ablation.png")
plt.savefig(path, dpi=200)
print("saved", path)
