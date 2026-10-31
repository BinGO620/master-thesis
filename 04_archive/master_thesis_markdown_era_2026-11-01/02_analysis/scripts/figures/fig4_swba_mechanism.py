#!/usr/bin/env python3
"""fig4_swba_mechanism.py — SWBA 机制示意图（论文 Ch4）

示意图（无数据源）：时间轴 KF 序列、free/anchor 区分、稠密窗口边、
修正回灌箭头。
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

fig, ax = plt.subplots(figsize=(9, 4.0))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")

# KF timeline
ax.annotate("", xy=(11.6, 1.2), xytext=(0.6, 1.2),
            arrowprops=dict(arrowstyle="-|>", color="#404040", lw=1.6))
ax.text(0.6, 0.85, "帧流 →", fontsize=8, color="#404040")

# keyframes on the timeline: older anchors (filled), free (open), new KF (star)
KFS = [(1.6, "K-5"), (3.0, "K-4"), (4.4, "K-3"), (5.8, "K-2"), (7.2, "K-1"), (8.8, "K (新)")]
roles = ["anchor", "anchor", "anchor", "anchor", "free", "free"]
for (x, label), role in zip(KFS, roles):
    if role == "anchor":
        ax.add_patch(mpatches.Circle((x, 1.2), 0.22, fc="#4f81bd", ec="#2c3e50", lw=1.2))
    else:
        ax.add_patch(mpatches.Circle((x, 1.2), 0.22, fc="white", ec="#c0504d", lw=1.8))
    ax.text(x, 0.6, label, ha="center", fontsize=8.5)

# zone shading
ax.add_patch(mpatches.Rectangle((1.25, 0.95), 5.0, 0.5, fc="#dce6f1", alpha=0.5, zorder=0))
ax.add_patch(mpatches.Rectangle((6.45, 0.95), 2.75, 0.5, fc="#fde9d9", alpha=0.6, zorder=0))
ax.text(3.75, 1.85, "固定锚 (n_anchors=4)", ha="center", fontsize=8, color="#4f81bd")
ax.text(7.8, 1.85, "自由块 (n_free=2)", ha="center", fontsize=8, color="#c0504d")

# dense window edges from new KF to all others
for (x, label), role in zip(KFS[:-1], roles[:-1]):
    ax.plot([8.8, x], [1.42, 3.4], color="#808080", lw=0.9, ls="-", alpha=0.65)
# free-free consecutive edge
ax.plot([8.8, 7.2], [1.35, 1.35], color="#c0504d", lw=1.4)
ax.text(8.0, 1.05, "free-free 边", fontsize=7.5, color="#c0504d")

# optimizer box
ax.add_patch(mpatches.FancyBboxPatch(
    (3.2, 3.4), 5.6, 1.2, boxstyle="round,pad=0.08",
    fc="#e6e0ec", ec="#404040", lw=1.2))
ax.text(6.0, 4.0, "窗口光度联合优化（GN+线搜索）\n冻结内点集 · 锚定仿射 · 步长护栏",
        ha="center", va="center", fontsize=8.5)

# edges into optimizer
ax.annotate("", xy=(6.0, 4.6), xytext=(6.0, 5.2),
            arrowprops=dict(arrowstyle="-|>", color="#808080", lw=1.0))
ax.text(6.0, 5.45, "稠密窗口边（指数距离 ≤ n_anchors 的全部对）",
        ha="center", fontsize=8)

# write-back arrow (the soul of the figure)
ax.annotate("", xy=(10.6, 2.3), xytext=(8.8, 3.4),
            arrowprops=dict(arrowstyle="-|>", color="#2e8b57", lw=2.4,
                            connectionstyle="arc3,rad=-0.25"))
ax.text(10.9, 2.0, "修正回灌\n(下一帧跟踪\n热启动)", ha="center", fontsize=8.5,
        color="#2e8b57", fontweight="bold")

# segment re-anchor note
ax.add_patch(mpatches.FancyBboxPatch(
    (1.0, 2.6), 2.0, 0.8, boxstyle="round,pad=0.06",
    fc="#ddebd8", ec="#808080", lw=0.9))
ax.text(2.0, 3.0, "KF 间非 KF 帧\n线性插值重锚定", ha="center", fontsize=7.5)

ax.set_title("SWBA：稠密窗口边 + 固定锚 + 修正回灌", fontsize=10, fontweight="bold")
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig4_swba_mechanism.png")
plt.savefig(path, dpi=200, bbox_inches="tight")
print("saved", path)
