#!/usr/bin/env python3
"""fig5_1_pilot_arms.py — Ch5 pilot 四臂分组柱状图

数据源：results/lifecycle_pilot/（2026-09-05，24 run 预注册四臂）。
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

MONOGS = "/data/monogs-ours/results/lifecycle_pilot"
OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "03_results", "figures")
)

SEQS = ["crowd3", "balloon2", "crowd"]
ARMS = ["off", "observe", "exit", "exit_fill"]
ARM_LABELS = ["off（基线）", "observe（安慰剂）", "exit（退出）", "exit_fill（+补全）"]
COLORS = ["#888888", "#4f81bd", "#2e8b57", "#8064a2"]


def ate(seq, arm, seed):
    f = f"{MONOGS}/{seq}_{arm}_seed{seed}/tables/tracking_raw.csv"
    if not os.path.exists(f):
        return None
    rows = list(csv.DictReader(open(f)))
    return float(rows[-1]["ate_rmse_cm"]) if rows else None


fig, ax = plt.subplots(figsize=(9, 4.0))
width = 0.19
xs = np.arange(len(SEQS))
for i, (arm, label, color) in enumerate(zip(ARMS, ARM_LABELS, COLORS)):
    means, stds = [], []
    for seq in SEQS:
        vals = [v for v in (ate(seq, arm, s) for s in range(2)) if v is not None]
        means.append(sum(vals) / len(vals) if vals else 0)
        stds.append((sum((v - means[-1]) ** 2 for v in vals) / max(len(vals), 1)) ** 0.5 if len(vals) > 1 else 0)
    pos = xs + (i - 1.5) * width
    bars = ax.bar(pos, means, width * 0.92, yerr=stds, capsize=2.5, color=color, label=label)
    for p, m in zip(pos, means):
        if m > 0:
            ax.text(p, m + 0.12, f"{m:.2f}", ha="center", fontsize=7.5)

ax.set_xticks(xs)
ax.set_xticklabels(["crowd3（对照）\n四臂不可区分=无害", "balloon2（判决）\nexit −5.7% ✅", "crowd（对照）"])
ax.set_ylabel("ATE RMSE (cm)")
ax.set_title("生命周期 pilot：四臂 × 三序列（每臂 2 seeds，误差棒=std）")
ax.legend(fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig5_1_pilot_arms.png")
plt.savefig(path, dpi=200)
print("saved", path)
