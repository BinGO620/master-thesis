#!/usr/bin/env python3
"""fig_drift_curves.py — pt1 逐帧漂移曲线对比（论文 Ch4 图 4.3）

数据源：monogs-ours/results/person_tracking_repair/*/datasets_bonn/**/per_frame_ape.csv
（seed0）。对比：基线族（r2 前 196 帧即基线行为）、R6 组合、R9 SWBA。
"""
import csv
import glob
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

MONOGS = "/data/monogs-ours/results/person_tracking_repair"
OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "03_results", "figures")
)

RUNS = [
    ("R2 硬掩码 (config 最优族, 10.39)", "r2_hardtrack_seed0", "#4f81bd"),
    ("R6 掩码+ICP 组合 (9.56)", "r6_combo_seed0", "#8064a2"),
    ("R9 SWBA 在线 (7.81)", "r9_swba_pt1_seed0", "#2e8b57"),
]


def load(tag):
    g = glob.glob(f"{MONOGS}/{tag}/**/per_frame_ape.csv", recursive=True)
    if not g:
        raise FileNotFoundError(tag)
    rows = list(csv.DictReader(open(g[0])))
    return [int(r["frame_id"]) for r in rows], [float(r["ape_cm"]) for r in rows]


fig, ax = plt.subplots(figsize=(8, 3.8))
for label, tag, color in RUNS:
    fr, ape = load(tag)
    ax.plot(fr, ape, lw=1.4, color=color, label=label)

ax.axvspan(221, 246, color="#c0504d", alpha=0.12)
ax.text(233, ax.get_ylim()[1] * 0.95, "事件窗口\n(221-246)", ha="center",
        fontsize=8, color="#c0504d")
ax.set_xlabel("帧号")
ax.set_ylabel("逐帧 APE (cm)")
ax.set_title("person_tracking 逐帧漂移：SWBA 压平尾部发散（seed 0）")
ax.legend(fontsize=8, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig4_drift_curves.png")
plt.savefig(path, dpi=200)
print("saved", path)
