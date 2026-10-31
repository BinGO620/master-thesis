#!/usr/bin/env python3
"""fig5_1_formal.py — Ch5 正式研究双面板图：残影清理 + 高斯数代价

数据源：results/lifecycle_formal/（2026-09-06，27 run：3 序列 × 3 臂
× 3 seeds）。
  面板 a：静态区残差代理 static_ghost_excess_depth_l1_cm（cm，越负
          = 退场后残影越少）；Ch5 §5.4 表的数据源
  面板 b：高斯数相对 off 均值的膨胀率（%，exit_fill_cons 的回收效果）

与 fig5_1_pilot_arms.png（pilot 四臂）互补：pilot 图讲立项依据（ATE
门禁），本图讲正式判决后的主张修正（残影主指标 + 代价）。
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

MONOGS = "/data/monogs-ours/results/lifecycle_formal"
OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "03_results", "figures")
)

SEQS = ["mvnobox", "balloon2", "mvnobox2"]
SEQ_LABELS = [
    "mvnobox\n（残影改善最强）",
    "balloon2\n（pilot 判决序列）",
    "mvnobox2\n（适用边界：机制激活但残差不动）",
]
ARMS = ["off", "exit", "exit_fill_cons"]
ARM_LABELS = ["off（基线）", "exit（退出）", "exit_fill_cons（fill 保守化）"]
COLORS = ["#888888", "#2e8b57", "#8064a2"]


def _col(seq, arm, seed, table, key):
    f = f"{MONOGS}/{seq}_{arm}_seed{seed}/tables/{table}.csv"
    if not os.path.exists(f):
        return None
    rows = list(csv.DictReader(open(f)))
    if not rows:
        return None
    v = rows[-1].get(key, "")
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def stats(seq, arm, table, key):
    vals = [v for v in (_col(seq, arm, s, table, key) for s in range(3)) if v is not None]
    if not vals:
        return None, None, 0
    m = sum(vals) / len(vals)
    # 样本 std (ddof=1)：与 Ch5 §5.4 表的 ±0.67 约定一致
    sd = (sum((v - m) ** 2 for v in vals) / max(len(vals) - 1, 1)) ** 0.5
    return m, sd, len(vals)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.2))
width = 0.26
xs = np.arange(len(SEQS))

# 面板 a：残差代理
for i, (arm, label, color) in enumerate(zip(ARMS, ARM_LABELS, COLORS)):
    means, stds, ns = [], [], []
    for seq in SEQS:
        m, sd, n = stats(seq, arm, "mapping_raw", "static_ghost_excess_depth_l1_cm")
        means.append(m if m is not None else 0)
        stds.append(sd if sd is not None else 0)
        ns.append(n)
    pos = xs + (i - 1) * width
    bars = ax1.bar(pos, means, width * 0.92, yerr=stds, capsize=2.5, color=color, label=label)
    for p, m, n in zip(pos, means, ns):
        ax1.text(p, m + (0.32 if m >= 0 else -0.75), f"{m:.2f}", ha="center", fontsize=7.5)
ax1.axhline(0, color="k", linewidth=0.8)
ax1.set_xticks(xs)
ax1.set_xticklabels(SEQ_LABELS, fontsize=8)
ax1.set_ylabel("静态区残差代理 (cm)")
ax1.set_title("(a) 残影清理：越负 = 退场残留越少", fontsize=10)
ax1.legend(fontsize=8)
ax1.spines[["top", "right"]].set_visible(False)

# 面板 b：高斯数膨胀率（相对 off 均值）
off_means = {}
for seq in SEQS:
    m, _, _ = stats(seq, "off", "efficiency_raw", "num_gaussians")
    off_means[seq] = m
for i, (arm, label, color) in enumerate(zip(ARMS[1:], ARM_LABELS[1:], COLORS[1:])):
    means, stds = [], []
    for seq in SEQS:
        m, sd, _ = stats(seq, arm, "efficiency_raw", "num_gaussians")
        if m is None or off_means[seq] in (None, 0):
            means.append(0)
            stds.append(0)
            continue
        # 相对 off 均值的膨胀率（与 Ch5 §5.4 "回收至 +51%" 同口径：
        # 分母 = off 的 3-seed 均值，误差棒 = 逐 seed 值的样本 std）
        vals = [
            100.0 * (_col(seq, arm, s, "efficiency_raw", "num_gaussians") - off_means[seq])
            / off_means[seq]
            for s in range(3)
            if _col(seq, arm, s, "efficiency_raw", "num_gaussians") is not None
        ]
        mu = sum(vals) / len(vals)
        sd = (sum((v - mu) ** 2 for v in vals) / max(len(vals), 1)) ** 0.5
        means.append(mu)
        stds.append(sd)
    pos = xs + (i - 0.5) * width
    ax2.bar(pos, means, width * 0.92, yerr=stds, capsize=2.5, color=color, label=label)
    for p, m in zip(pos, means):
        ax2.text(p, m + 1.5, f"{m:+.0f}%", ha="center", fontsize=7.5)
ax2.axhline(0, color="k", linewidth=0.8)
ax2.set_xticks(xs)
ax2.set_xticklabels([s.split("\n")[0] for s in SEQ_LABELS], fontsize=8)
ax2.set_ylabel("高斯数相对 off (%)")
ax2.set_title("(b) 代价：高斯数膨胀（fill 保守化回收）", fontsize=10)
ax2.legend(fontsize=8)
ax2.spines[["top", "right"]].set_visible(False)

fig.suptitle("生命周期正式研究：主张修正后的主指标与代价（3 seeds，误差棒=std）", fontsize=11)
plt.tight_layout(rect=(0, 0, 1, 0.94))
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "fig5_1_formal_ghost_cost.png")
plt.savefig(path, dpi=200)
print("saved:", path)

# 数据自检：与 Ch5 §5.4 表核对（mvnobox off 均值 +1.29）
m, sd, n = stats("mvnobox", "off", "mapping_raw", "static_ghost_excess_depth_l1_cm")
assert abs(m - 1.29) < 0.02, f"mvnobox off 均值 {m:.3f} 与 §5.4 (+1.29) 不符"
print(f"check ok: mvnobox off ghost_excess {m:.2f}±{sd:.2f} (n={n})")
