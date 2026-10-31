#!/usr/bin/env python3
"""fig2_3_taxonomy.py — anti/face-dynamic 分类树（论文 Ch2 图）

示意图：两条路线的代表方法树，本文 RoGS-SLAM 高亮在几何/运动一致性档。
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

fig, ax = plt.subplots(figsize=(9, 4.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")


def node(x, y, w, h, text, fc, fs=7.5, bold=False, ec="#606060"):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec=ec, lw=1.0))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, fontweight="bold" if bold else "normal")


def link(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color="#909090", lw=0.9)


# root
node(4.5, 6.0, 3.0, 0.8, "动态场景 3DGS-SLAM\n动态处理路线", "#f2f2f2", 9, True)

# two branches
node(0.8, 4.6, 4.4, 0.8, "anti-dynamic（移除/降权）", "#fde9d9", 8.5, True)
node(6.8, 4.6, 4.4, 0.8, "face-dynamic（显式建模）", "#dce6f1", 8.5, True)
link(6.0, 6.0, 3.0, 5.4)
link(6.0, 6.0, 9.0, 5.4)

# anti sub-branches
node(0.3, 2.9, 2.7, 1.3, "语义先验档\nWildGS-SLAM\nRoSe-SLAM", "#fff5ec", 7.5)
node(3.3, 2.9, 2.7, 1.3, "几何/运动一致性档\nDy3DGS-SLAM  GGD-SLAM\nMoPe  DL-SLAM", "#fff5ec", 7.5)
link(3.0, 4.6, 1.6, 4.2)
link(3.0, 4.6, 4.6, 4.2)

# highlight RoGS
node(0.55, 1.0, 2.2, 1.2, "RoGS-SLAM\n（本文 Ch.3）\n光流一致性+降权", "#2e8b57", 7.5, True, "#1e5c3a")
ax.text(1.65, 0.6, "← 免类别先验", ha="center", fontsize=7, color="#2e8b57")
link(1.6, 2.9, 1.65, 2.2)

# face sub-branches
node(6.3, 2.9, 2.3, 1.3, "4D/变形场\nD4DGS-SLAM\nFlow4DGS-SLAM", "#eef3fa", 7.5)
node(8.8, 2.9, 2.3, 1.3, "实时动态\nDynaGSLAM\nRiGS", "#eef3fa", 7.5)
link(9.0, 4.6, 7.4, 4.2)
link(9.0, 4.6, 9.9, 4.2)

# note: single-arrow gap
ax.text(6.0, 1.2, "face 路线在单目设置下\n仍处早期（实时性/深度尺度）",
        ha="center", fontsize=7.5, color="#606060", style="italic")

ax.set_title("动态处理两路线与本文定位（Ch.2.3）", fontsize=10, fontweight="bold")
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig2_3_taxonomy.png")
plt.savefig(path, dpi=200, bbox_inches="tight")
print("saved", path)
