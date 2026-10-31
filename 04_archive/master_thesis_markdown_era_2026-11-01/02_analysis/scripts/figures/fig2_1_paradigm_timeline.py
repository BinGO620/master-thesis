#!/usr/bin/env python3
"""fig2_1_paradigm_timeline.py — SLAM 范式时间线（论文 Ch2 图）

示意图（无数据源）：滤波式→图优化→学习式→3DGS 四阶段时间线，
每阶段标注代表方法与本文关系。
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "03_results", "figures")
)

fig, ax = plt.subplots(figsize=(9, 3.2))
ax.set_xlim(2000, 2027)
ax.set_ylim(0, 4)
ax.axis("off")

# main timeline
ax.annotate("", xy=(2027, 0.8), xytext=(2000, 0.8),
            arrowprops=dict(arrowstyle="-|>", color="#404040", lw=2))
for y in [2000, 2005, 2010, 2015, 2020, 2025]:
    ax.plot([y, y], [0.72, 0.88], color="#404040", lw=1)
    ax.text(y, 0.5, str(y), ha="center", fontsize=8, color="#404040")

PHASES = [
    (2000, 2007, "滤波式\nEKF/FastSLAM", "#f2dcdb"),
    (2007, 2020, "图优化\nORB-SLAM 系列", "#dce6f1"),
    (2020, 2023, "学习式\nDROID-SLAM", "#e6e0ec"),
    (2023, 2027, "3DGS-SLAM\nMonoGS 及动态扩展", "#ddebd8"),
]
for x0, x1, label, color in PHASES:
    ax.add_patch(mpatches.FancyBboxPatch(
        (x0, 1.6), x1 - x0 - 0.3, 1.1, boxstyle="round,pad=0.1",
        fc=color, ec="#808080", lw=1))
    ax.text((x0 + x1) / 2, 2.15, label, ha="center", va="center", fontsize=8.5)

# annotations
ax.annotate("本文架构立场：\n优化式（非学习式）", xy=(2025, 2.7), xytext=(2020.5, 3.6),
            fontsize=8, ha="center", color="#2e8b57",
            arrowprops=dict(arrowstyle="->", color="#2e8b57", lw=1))
ax.annotate("本文基座", xy=(2024, 1.6), xytext=(2024, 0.15), fontsize=8,
            ha="center", color="#2e8b57",
            arrowprops=dict(arrowstyle="->", color="#2e8b57", lw=1))

ax.set_title("SLAM 范式演进与本文定位", fontsize=10, fontweight="bold")
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig2_1_paradigm_timeline.png")
plt.savefig(path, dpi=200, bbox_inches="tight")
print("saved", path)
