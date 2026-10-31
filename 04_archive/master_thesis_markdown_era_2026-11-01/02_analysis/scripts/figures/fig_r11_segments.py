#!/usr/bin/env python3
"""fig_r11_segments.py — R11 组合臂逐段柱状图（论文 Ch4 图，待画清单 #4）

论点（verdict.md R11 判决）：SWBA+硬掩码组合在**前段确实改善**，但硬掩码
降低逐帧光度损失的观测自由度，SWBA 的窗口边继承同一偏差 → **中段修正
基线被侵蚀**，整体增益归零（7.81→7.76，噪声级）。

数据源（单一事实源）：
  /data/monogs-ours/results/person_tracking_repair/{r9_swba_pt1_seed0,
  r11_swba_mask_pt1_seed0}/**/per_frame_ape.csv（seed0）
分段边界与 verdict.md R11 判决原文一致（0-99/100-199/200-299/300-399）。
"""
import csv
import glob
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

MONOGS = "/data/monogs-ours/results/person_tracking_repair"
OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "03_results", "figures")
)

SEGS = [("0-99", 0, 99), ("100-199", 100, 199),
        ("200-299", 200, 299), ("300-399", 300, 399)]
ARMS = [("R9 SWBA 单独 (7.81)", "r9_swba_pt1_seed0", "#2e8b57"),
        ("R11 SWBA+硬掩码 (7.76)", "r11_swba_mask_pt1_seed0", "#c0504d")]


def load(tag):
    g = glob.glob(f"{MONOGS}/{tag}/**/per_frame_ape.csv", recursive=True)
    if not g:
        raise FileNotFoundError(tag)
    return {int(r["frame_id"]): float(r["ape_cm"])
            for r in csv.DictReader(open(g[0]))}


def seg_mean(d, a, b):
    xs = [v for k, v in d.items() if a <= k <= b]
    return sum(xs) / len(xs) if xs else float("nan")


data = {lbl: load(tag) for lbl, tag, _ in ARMS}
x = np.arange(len(SEGS))
w = 0.36

fig, ax = plt.subplots(figsize=(8.4, 4.0))
for i, (lbl, _, color) in enumerate(ARMS):
    vals = [seg_mean(data[lbl], a, b) for _, a, b in SEGS]
    bars = ax.bar(x + (i - 0.5) * w, vals, w, label=lbl, color=color)
    for bx, v in zip(bars, vals):
        ax.text(bx.get_x() + bx.get_width() / 2, v + 0.08, f"{v:.2f}",
                ha="center", fontsize=8.5)

ax.set_xticks(x)
ax.set_xticklabels([n for n, _, _ in SEGS])
ax.set_xlabel("帧段")
ax.set_ylabel("段内平均逐帧 APE (cm)")
ax.set_title("R11 组合臂逐段：前段改善、中段基线被侵蚀（person_tracking, seed 0）")
ax.legend(fontsize=8.5, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
ax.annotate("前段改善\n(掩码起效)", xy=(0.5, max(seg_mean(data[ARMS[0][0]], 0, 99),
                                              seg_mean(data[ARMS[1][0]], 0, 99)) + 0.5),
            ha="center", fontsize=8, color="#2e8b57")
ax.annotate("中段侵蚀\n(光度自由度被压缩)", xy=(2.0, 8.4),
            ha="center", fontsize=8, color="#c0504d")
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig4_r11_segments.png")
plt.savefig(path, dpi=200)
print("saved", path)
