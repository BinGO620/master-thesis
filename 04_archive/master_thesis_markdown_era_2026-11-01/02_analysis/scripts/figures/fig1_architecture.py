#!/usr/bin/env python3
"""fig1_architecture.py — 论文第一图：三研究内容在动态 3DGS-SLAM 流水线中的三层定位

纯示意图（无数据源），用 matplotlib 画框图。输出 03_results/figures/。
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
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.axis("off")

C_OBS, C_EST, C_REP = "#dce6f1", "#e6e0ec", "#ddebd8"
EDGE = "#404040"


def box(x, y, w, h, label, fc, fs=9, lw=1.2):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.06",
        fc=fc, ec=EDGE, lw=lw))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs)


def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1.2))


# 主体流水线（中层）
box(0.3, 2.4, 1.5, 0.9, "RGB-D 输入", "#f2f2f2")
box(2.3, 2.4, 1.7, 0.9, "跟踪\n(逐帧位姿优化)", "#f2f2f2")
box(4.5, 2.4, 1.7, 0.9, "建图\n(高斯优化)", "#f2f2f2")
box(6.7, 2.4, 1.7, 0.9, "致密化\n与生命周期", "#f2f2f2")
box(8.8, 2.4, 1.1, 0.9, "地图", "#f2f2f2")
arrow(1.8, 2.85, 2.3, 2.85)
arrow(4.0, 2.85, 4.5, 2.85)
arrow(6.2, 2.85, 6.7, 2.85)
arrow(8.4, 2.85, 8.8, 2.85)
ax.annotate("", xy=(2.6, 2.1), xytext=(5.3, 2.1),
            arrowprops=dict(arrowstyle="-|>", color="#7f7f7f", lw=1.0, ls="--"))
ax.text(3.95, 1.92, "渲染反馈", ha="center", fontsize=7.5, color="#7f7f7f")

# 三层标注
# 观测层
box(1.0, 4.3, 3.0, 0.9, "研究内容一（观测层）\n可靠性引导降权 [Ch.3]", C_OBS, fs=8.5)
arrow(2.5, 4.3, 3.1, 3.35)
# 估计层
box(4.3, 4.3, 2.6, 0.9, "研究内容二（估计层）\nSWBA 滑窗联合优化 [Ch.4]", C_EST, fs=8.5)
arrow(5.6, 4.3, 5.3, 3.35)
# 表示层
box(7.3, 4.3, 2.4, 0.9, "研究内容三（表示层）\n状态转换生命周期 [Ch.5]", C_REP, fs=8.5)
arrow(8.5, 4.3, 7.5, 3.35)

# 动态干扰标注
box(0.6, 0.6, 3.4, 0.8, "动态干扰：行人 / 搬运 / 物体出现与移除", "#fde9d9", fs=8)
arrow(2.3, 1.4, 2.9, 2.4)
arrow(4.0, 1.4, 5.2, 2.4)

ax.text(0.3, 5.35, "图 1.1  三研究内容的系统定位：观测 / 估计 / 表示三层次",
        fontsize=10, fontweight="bold")

plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig1_architecture.png")
plt.savefig(path, dpi=200, bbox_inches="tight")
print("saved", path)
