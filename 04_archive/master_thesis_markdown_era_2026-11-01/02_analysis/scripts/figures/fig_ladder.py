#!/usr/bin/env python3
"""fig_ladder.py — person_tracking 修复阶梯瀑布图（论文 Ch4）

数据源（单一事实源）：/data/monogs-ours/results/person_tracking_repair/
evidence/verdict.md 的阶梯总账。输出到 03_results/figures/。
"""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "03_results", "figures")
)

# pt1 ladder (arm label, mean ATE cm, accepted?)
# last two bars are the fulltable concurrent-era terminal (seed3 promotion,
# 2026-09-07): era differs from the serial-era R1-R18 bars — hatched.
LADDER = [
    ("基线\nCombined-Prune", 12.28, "base"),
    ("R1 短几何边\n(后处理)", 13.06, "fail"),
    ("R2 硬掩码\n(跟踪内)", 10.39, "win"),
    ("R6 掩码+ICP\n(config 最优)", 9.56, "win"),
    ("R7 光度短边\n(后处理)", 11.72, "fail"),
    ("R8 光度长边\n(后处理)", 12.42, "fail"),
    ("R9 SWBA\n(在线, 路线B)", 7.81, "win"),
    ("R13 深窗口", 8.43, "fail"),
    ("R15 回环v1", 8.19, "fail"),
    ("R16 SWBA+回环v2\n(两层架构)", 7.40, "best"),
    ("R17 回环v3\n(几何通道)", 7.57, "warn"),
    ("R18 回环v4\n(分通道配额)", 7.88, "warn"),
    ("fulltable 基线\n(并发时代)", 13.62, "base"),
    ("gate 终态\n(final+逐帧门)", 7.83, "gate"),
]
COLORS = {"base": "#888888", "fail": "#c0504d", "win": "#4f81bd", "best": "#2e8b57",
          "warn": "#e0a030", "gate": "#2e8b57"}
ERA_HATCH = {"gate": "//", "best": None}  # concurrent-era bars hatched

fig, ax = plt.subplots(figsize=(12.5, 4.6))
x_pos = list(range(len(LADDER)))  # 均匀分布；宽度靠 figsize 保证
bars = ax.bar(x_pos, [v for _, v, _ in LADDER], color=[COLORS[k] for _, _, k in LADDER], width=0.62)
for x, (_, v, k) in zip(x_pos, LADDER):
    if ERA_HATCH.get(k):
        bars[x].set_hatch(ERA_HATCH[k])
        bars[x].set_edgecolor("white")
    ax.text(x, v + 0.15, f"{v:.2f}", ha="center", fontsize=9,
            fontweight="bold" if k in ("best", "gate") else "normal")
ax.axhline(5.0, color="#c00000", ls="--", lw=1.2)
ax.text(len(LADDER) - 0.4, 5.25, "5cm 目标线", color="#c00000", fontsize=9, ha="right")
ax.set_xticks(x_pos)
ax.set_xticklabels([n for n, _, _ in LADDER], fontsize=7.5)
ax.set_ylabel("ATE RMSE (cm)")
ax.set_title("person_tracking 修复阶梯：SWBA −36%，两层架构 7.40，部署终态（gate 门控）7.83\n"
             "（关键臂选示；R1-R18 串行时代 3 seeds/臂 + fulltable 并发时代 3-seed，口径见表 4.x）",
             fontsize=11)
ax.set_ylim(0, 14.5)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig4_ladder_pt1.png")
plt.savefig(path, dpi=200)
print("saved", os.path.abspath(path))
