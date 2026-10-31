#!/usr/bin/env python3
"""fig2_4_map_lifecycle.py — 在线地图管理决策树（论文 Ch2.4 图）

示意图：一个高斯基元从插入到退出/恢复的五状态决策链，标注每步的
判据与本文对应的研究内容（Ch.3 lineage 提交端 / Ch.5 退出恢复端）。
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

fig, ax = plt.subplots(figsize=(10, 4.4))
ax.set_xlim(0, 13)
ax.set_ylim(0, 6)
ax.axis("off")


def node(x, y, w, h, text, fc, fs=7.5, bold=False, ec="#606060", lw=1.0):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, fontweight="bold" if bold else "normal")


def arrow(x1, y1, x2, y2, color="#909090", lw=1.0, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))


# ---- 五状态主链（横向） ----
y = 3.4
h = 0.95
w = 1.9
xs = [0.3, 2.6, 4.9, 7.2, 9.5]
labels = [
    "① 插入\n新基元进入地图",
    "② 致密化\nclone / split 增多",
    "③ 持久化\n保留并参与渲染",
    "④ 退出\n剪枝 / 删除",
    "⑤ 恢复\n背景补全 / 重插入",
]
fcs = ["#eaf3ea", "#eaf3ea", "#eaf3ea", "#fde9d9", "#dce6f1"]
for x, t, fc in zip(xs, labels, fcs):
    node(x, y, w, h, t, fc, 7.5, bold=True)
# 主链箭头
for i in range(4):
    arrow(xs[i] + w, y + h / 2, xs[i + 1], y + h / 2, lw=1.2)

# 回环箭头：退出→恢复→持久化（可回滚）
arrow(xs[3] + w / 2, y, xs[4] + w / 2, y, color="#c0504d", lw=1.1)
arrow(xs[4] + w / 2, y + h, xs[2] + w / 2, y + h, color="#c0504d", lw=1.1)
ax.text(9.9, y + h + 0.12, "可回滚（Ch.5）", ha="center", fontsize=6.8,
        color="#c0504d", style="italic")

# ---- 每步判据（上方小字） ----
crit = [
    "观察-确认\n(多帧证据)",
    "梯度/生命周期\n(时间感知)",
    "静态性确认\n(可信度)",
    "状态转换检测\n(残影/遮挡)",
    "可信度驱动\n(背景补全)",
]
for x, c in zip(xs, crit):
    ax.text(x + w / 2, y + h + 0.35, c, ha="center", va="bottom",
            fontsize=6.6, color="#404040")

# ---- 本文对应（下方标注） ----
ax.text(0.3 + 2 * w, y - 0.45, "本文 Ch.3：lineage 生命周期（提交端）",
        ha="center", fontsize=7.5, color="#2e8b57", fontweight="bold")
ax.text(9.5 + w / 2, y - 0.45, "本文 Ch.5：退出/恢复（状态转换端）",
        ha="center", fontsize=7.5, color="#1f4e79", fontweight="bold")

# 分隔虚线：进 / 出
ax.plot([7.05, 7.05], [1.6, 5.6], ls="--", color="#b0b0b0", lw=0.9)
ax.text(7.05, 5.75, "进（提交端）", ha="center", fontsize=7, color="#606060")
ax.text(11.2, 5.75, "出（状态转换端）", ha="center", fontsize=7, color="#606060")

# ---- 底部：空缺说明 ----
ax.text(6.5, 0.75,
        "空缺 G3：在线、增量、可回滚的状态转换感知生命周期不完整——\n"
        "多数工作止于「进」与「删」，已提交基元在场景状态改变时的命运缺乏系统形式化",
        ha="center", fontsize=7.5, color="#404040",
        bbox=dict(boxstyle="round,pad=0.4", fc="#f7f7f7", ec="#c0c0c0", lw=0.8))

ax.set_title("在线地图管理的五状态决策链与本文定位（Ch.2.4）",
             fontsize=10, fontweight="bold")
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig2_4_map_lifecycle.png")
plt.savefig(path, dpi=200, bbox_inches="tight")
print("saved", path)
