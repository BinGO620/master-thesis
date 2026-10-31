#!/usr/bin/env python3
"""fig2_2_pipeline.py — 3DGS-SLAM 系统流水线图（论文 Ch2.2 图）

示意图：MonoGS 式 3DGS-SLAM 的跟踪/建图/致密化三模块闭环，标注本文
各章贡献的挂接点（Ch.3 观测端四组件 / Ch.4 跟踪循环内 SWBA 窗口 /
Ch.5 地图生命周期），以及动态内容注入残差的路径。

数据源：无（结构示意图，依据 02_related_work_2_2_3dgs_slam.md 与
Ch.3 §3.2 的挂接点表）。
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

fig, ax = plt.subplots(figsize=(10.5, 4.8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 6.6)
ax.axis("off")


def node(x, y, w, h, text, fc, fs=8, bold=False, ec="#606060", lw=1.0):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.06", fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, fontweight="bold" if bold else "normal")


def arrow(x1, y1, x2, y2, color="#909090", lw=1.1, style="-|>", ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, ls=ls))


# ---- 三模块主链 ----
y, h, w = 3.6, 1.15, 2.6
xs = [0.4, 4.2, 8.0]
labels = [
    "跟踪 (Tracking)\n逐帧 Adam 光度优化\n位姿 T_t",
    "建图 (Mapping)\n窗口联合优化\n高斯参数",
    "致密化 (Densify)\nclone / split / prune\n地图增长",
]
fcs = ["#dce6f1", "#eaf3ea", "#fdf3d9"]
for x, t, fc in zip(xs, labels, fcs):
    node(x, y, w, h, t, fc, 8, bold=True)
for i in range(2):
    arrow(xs[i] + w, y + h / 2, xs[i + 1], y + h / 2, lw=1.3)

# 渲染反馈闭环：致密化 → 跟踪（渲染图像）
arrow(xs[2] + w / 2, y, xs[0] + w / 2, y, color="#4f81bd", lw=1.2, ls="--")
ax.text((xs[0] + xs[2] + w) / 2, y - 0.42, "可微光栅化渲染（式 2.4）——闭环反馈",
        ha="center", fontsize=7.5, color="#4f81bd")

# ---- 动态内容注入（从上方分别指向跟踪与建图，避开下方挂接箭头） ----
node(5.4, 5.4, 3.2, 0.8, "动态内容\n运动体注入光度/几何残差", "#fde9d9", 7.5)
arrow(6.2, 5.4, 1.7, y + h, color="#c0504d", lw=1.2, style="-|>")
arrow(8.0, 5.4, 9.3, y + h, color="#c0504d", lw=1.2, style="-|>")

# ---- 本文各章挂接点 ----
node(0.4, 1.4, 4.0, 1.5,
     "Ch.3 观测端（四组件）\nK 关键帧覆盖 · R Huber IRLS\nL 可靠性信号 · D lineage 提交",
     "#e8e0f0", 7.5)
arrow(2.0, 2.9, 1.7, y, color="#8064a2", lw=1.1)

node(4.9, 1.4, 4.0, 1.5,
     "Ch.4 跟踪循环内\nSWBA 窗口光度联合优化\n（事件型漂移）",
     "#e0f0e0", 7.5)
arrow(6.9, 2.9, 6.9, y, color="#2e8b57", lw=1.1)

node(9.6, 1.4, 4.0, 1.5,
     "Ch.5 地图生命周期\n退出/恢复/残影清除\n（状态转换端）",
     "#fce4e4", 7.5)
arrow(11.6, 2.9, 11.6, y, color="#c0504d", lw=1.1)

ax.text(7.0, 0.6, "本文三章分别作用于观测定价、跟踪循环与地图演化三个层次",
        ha="center", fontsize=8, color="#404040")

plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig2_2_pipeline.png")
plt.savefig(path, dpi=200)
print("saved", path)
