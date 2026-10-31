# Supplementary — Lifecycle comparison (deferred vs prune) & extended analyses (MMM 2027)

> **3090 正式数已回填**（`p2t_verdict_3090.md`，36-run P2-T 官方重跑）。本补充与主文 §4.5
> 共享同一 36-run P2-T 主表；下表 ATE/G 均来自 3090 正式 run。

---

## S.1 Backbone lifecycle comparison (deferred vs prune) — self-tracked, 3-seed

主文 §4.5 只报承载 terminal compression 的 **prune 臂**对外 ATE。本补充给出双臂同 protocol
完整表，含 compactness（G_def/G_prune）与 ATE 的 Pareto 关系，定位为 **lifecycle 适用域边界
（measurement）**，非 "deferred wins"。

| seq | prune G±sd | deferred G±sd | prune ATE±sd | deferred ATE±sd | G_def/G_prune | deferred ATE % worse |
|---|---|---|---|---|---|---|
| balloon | 35513±5595 | 22378±1850 | **3.06**±0.14 | 3.29±0.17 | 0.630 | +7.5% |
| balloon2 | 45197±9443 | 24808±1741 | **5.28**±0.11 | 5.67±0.38 | 0.549 | +7.4% |
| mv_no_box | 41568±4202 | 30805±3155 | **2.66**±0.12 | 3.19±0.15 | 0.741 | +19.9% |
| mv_no_box2 | 62266±10864 | 54028±9193 | **5.14**±0.28 | 6.18±0.94 | 0.868 | +20.2% |
| pt1 | 53915±5319 | 39739±1855 | **10.04**±0.58 | 14.91±3.29 | 0.737 | +48.5% |
| pt2 | 69718±20027 | 44246±4415 | **10.44**±0.84 | 15.93±4.55 | 0.635 | **+52.6%** |

<!-- data: p2t_verdict_3090.md (3090 official) -->

**Reading (Pareto frontier, not a win/loss):**
- **deferred ATE ≥ prune on 6/6** same-sign → 升级为 "trade" 而非 "indistinguishable"
  （P=0.031 exchangeability，但 sign-test 未预注册 ⇒ exploratory，只述方向）。
- **G_def/G_prune < 1 on all six sequences**（0.549–0.868）：deferred 用更小地图换少量 ATE 代价。
  低覆盖序列（mask 漏 mover，如 balloon 人+气球抓不住气球）compactness<1 同向复现。
- **pt2 破 50% no-harm 带（+52.6%）**。**不删除**（非 catastrophic），诚实报告。
- **H-D（lifecycle 适用域边界）三分支 INDETERMINATE**（`hd_coverage_prereg.md` §4）：
  (a)逐帧 vs (b)±15帧 覆盖率秩在 pt1/pt2 翻转 ⇒ prereg 触发；Spearman ρ=+0.257, p=0.62（只报方向，
  不报显著性；该 ρ 来自 2060 版，3090 版秩同向未重算）。**不构成"验证成立"，只作可证伪 gating
  假设的一条方向观察**。
- **不复活 compactness headline**；本表定位 = 主文 backbone floor 的内部完整性（Pareto-frontier measurement）。

## S.2 FPS/VRAM (2060, NOT comparable to high-end competitors)

主文 limitation 已声明 FPS 是 2060 数不得与竞品并列。基线效率数据（VRAM 可用、6GB 可跑完全部）
作为 2060 局限性记录在 `resources/02-baselines/`，不进正式比较表。

## S.3 删除比例跨序列稳定性（skeleton §4.6 注）

op<0.01 删除比例 8.4–18.4%，序列间稳定（balloon 最高 16.2%、mv_no_box 最低 9.4%）；balloon 高删比例
与其「人+气球」含更多可软抑制 floaters 相关（描述性，非归因）。完整 per-sequence 表见
`results/evidence/p3_artifact_full18.md`。
