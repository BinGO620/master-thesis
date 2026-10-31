# Idea Discovery Report — Dynamic 3DGS SLAM，CCF-C 冲刺

**Direction**: 用这个 skill 发散 idea，找出 3 周末内 2060 可验证、且能过审稿的 standalone 贡献
**Date**: 2026-08-07
**Pipeline**: research-brief → landscape (codex) → ideation (codex) → feasibility (asset check) → 审稿 → idea 排名 → 实验计划
**NOTE**: 子 skill（research-lit/idea-creator/novelty-check/research-review/research-refine-pipeline）本地不存在，
本报告用 codex MCP + 本地 02-related-work-gaps.md + 项目资产检查等效替代，产出 canonical IDEA_REPORT + 实验计划。

---

## Executive Summary

**结论先行：没有一个 "能站" 的新 idea 能在 3 周内 2060 上验证到让审稿人 pass 的程度。**

核心原因（这不是悲观，是死清单 + 反事实 + 资产盘点共同给出的事实）：
1. 我们已死掉所有**在线/跟踪侧**机制（deferred/eviction/α-carve/RT/DBA/位姿）——在线贡献没有活着的主线。
2. 唯一"幸存正向" terminal compression 的**机制被证伪**（tail 是 refine 软抑制，不是 ADC 稳态），且
   frozen-opacity 反事实否掉了"refine-aware 省参"这条系统贡献（−0.53dB、N+35%）。
3. 发散去试探，最显眼的 three candidate 也各自撞墙：
   - **方向5（dynamic-static lifecycle compaction）**——需要 per-Gaussian motion-ownership，但实测
     `static_prob`/`static_obs_count`/`unmapped_score` 列在 prune 臂 final 图里**全是占位默认值
     （0.70/0/0），从未被填充**。要填充需 gaussian-level motion 追踪，3 周从零实现超范围。
   - **方向1（refine-aware progressive compaction 省 compute）**——freeze 反事实已给出负面下界
     （锁 opacity 地图更大），在 2060 上移除 <1% 贡献的高斯对前向时间/VRAM 影响 <1%，"省 compute"
     几乎不可证显著。
   - **方向2（贡献度 beyond opacity）**——零/1 GPU 但几乎必然负（opacity-only 删 <0.01 已 12/12 零代价，
     引入 complex score 很难在 matched 压缩比下更好）。

**推荐的诚实后撤**：与其强行造一个新的"机制贡献"，不如把已证实的窄主线写成**诚实可投的工程/实证篇**。
下面 ranked 部分给出"最不坏"的那条 + 它为什么只能当 backup，不做主打。

---

## Landscape（Phase 1，codex + 02-related-work-gaps.md）

```
Dynamic 3DGS SLAM efficiency and map control
|-- A. Gaussian lifecycle management (在线 birth/maturity/prune/terminal compaction)
|-- B. Post-SLAM refinement (参数可训性 / opacity 软抑制 / refine-aware pruning / 质量-成本权衡)
|-- C. Dynamic-scene decomposition (静态vs动态所有权 / 瞬态退役 / motion-confidence / 重出现持久性)
|-- D. Resource-aware representation (固定/空间自适应 budget / memory 正则 / deployment 压缩)
`-- E. Mechanism & diagnostics (opacity-scale-visibility 轨迹 / prune/schedule 效应 / lineage / image-space 贡献)
```

我们的资产对照：
- 我们唯一讲清的部分在 B∩A 的**交点**（B. 软选择 → A. 终图压实）——但这一点已证明**不是系统级贡献**。
- C（动态专属）是最大的缺口，也是 MGS-SLAM/LEGO-SLAM/GaussianFlow 已占的领域，且我们缺 gaussian-level
  motion ledger（实测未填充）。
- D（resource-aware/6GB 卖点）在 3 周内最有希望变成"实证面"（metrics 已齐），但作为**贡献**它顶多是 secondary。

---

## Ranked Ideas（Phase 2，codex 排名 × 我按 2060/3周 可行性再排）

> 括号 = 初始代码又排名（1 最高）。我的重排把 **2060 可证显著性** 作为硬门槛。

### ⭐ Idea A（=codex#1/3 合并）："post-SLAM refinement 是隐式软选择，但留下可物理压实的结果" —— 诚实窄主线
- **是什么**：承认 terminal compression 机制是 refine 软选择，把它写成"动态 SLAM 终图为何有可零代价删的
  低贡献高斯 + 一个零渲染代价的压实"（不吹省 compute，不吹修复 refine）。
- **零/低 GPU**：P2-T 36-run 已全部要求 |dPSNR|≤0.0001dB 的删除证据 + theory.md 上界 + frozen-opacity
  机制解释。**补 0-1 GPU** 广义化到多 seq 的 contribution vs opacity 对照（可选，且可能负）。
- **防守性**：中。诚实、可辩护（审稿人无法扣"机制错"因为我们自己标了），但**"窄"**——单后处理观测，
  可能被读成"实现清洁"而非科学。**对上 3 周**：现成数据，几乎零新 GPU。
- **风险**：被质疑"这是 bug 不是贡献"（freeze 反事实已证明 opacity 抑制有用，所以不是 purely 垃圾）。
  codex#3 的机制价值在于解释"soft selection useful, not defective"——这个本身是一句话的洞见，撑不起一篇。

### ⭐⭐ Idea B（=codex#5）：dynamic-static lifecycle compaction —— 最独立、但需 motion ledger
- **是什么**：用"静态 vs 动态所有权 + 瞬态对象退役"做比 opacity 更准的压缩。
- **为何搁置**：**实测 `static_prob`/`static_obs_count`/`unmapped_score` 三列在 prune 臂 final 图全是默认值
  （0.70/0/0），无 gaussian-level motion-ownership 可用**。要重建=新实现 motion 追踪，3 周超范围。
  **除非**——补一个 0.5 GPU-hr 探针：检查 **MGS-SLAM 式的 image-space contribution 是否已隐含 motion 信息**
  （若被删的高斯天然是"近期 m 移动过"的，可能用 recency/timespan 信号够用，不需完整 motion 追踪）。

### ⭐ Idea C（=codex#2）：image-space contribution score beyond opacity
- 零/1 GPU-hr；证伪概率高（opacity-only 已足够好）。**作为 ablation** 可接受，作为主打不行。

### ❌ Eliminated
- codex#1（refine-aware delete 省 compute）：freeze 反事实负面下界，2060 上"省 compute"不可证显著。
- codex#4（maturity-aware patience deletion）：需要 recovery-probability 量表，3 周难，且地基是#
- codex#6（budgeted densification）：拥挤方向，18-27 run，需 novel dynamic-aware budget 信号（我们没有）。
- codex#7（refine param scheduling）：用于 ablation，非独立主打。
- codex#8（terminal prune as standalone primitive）：本身弱；可作为 Idea A 的广义化佐证。

---

## Novelty 校验（Phase 3，重点）

为避免撞车，Idea A 必须显式区分（来自 02-related-work-gaps.md §3 已铺开）：
- **MGS-SLAM（在线 significance pruning）**：τ_α=0.7/τ_r=0.85，删"大部分高斯"以保 pose；我们是
  **终端 op<0.01 删除浮渣尾巴**，目标内存/传输，零渲染代价。两个数量级不同的域。
- **在线训练期剪枝**（Speedy-Splat / DCSHARP-GS / ShorterSplatting / PUP-3DGS）：在训练管线里为加速；
  我们是终图压实。
- **存储压缩**（3DGS.zip / LightGaussian / Compact3D）：通用重建 + 属性量化/蒸馏；我们针对**动态 SLAM
  insert-then-prune 的 refaine 软抑制产物**，来源特定。
- 新增（本轮）：**freeze-opacity 机制解释**——"这种尾巴是 refine 的 opacity DOF 软选择造成的"，这是
  领域里没人系统讲的一环，可作为 Idea A 的 novelty 支点。

**Eliminate 检查**：Idea B 若用 recency/motion 信号，须先确认不撞 MGS-SLAM（它用 significance 不是 motion）与
GaussianFlow SLAM（normalized-error prune）。**Idea B 前置探针**必须查这个。

---

## Reviewer 反馈（Phase 4，codex 充当 senior reviewer，已内嵌）

codex 已给的关键评审点（direct quote-condensed）：
> "The best paper-shaped claim is NOT 'terminal opacity pruning removes a tail'. It is:
> **Post-SLAM refinement performs implicit soft model selection, but leaves the selected representation
> physically uncompacted. A contribution- and maturity-aware lifecycle policy converts this implicit
> selection into hard compaction during optimization, reducing refinement and deployment cost without
> sacrificing reconstruction quality.** That claim has mechanism, intervention, and consequence. It also
> survives the discovery that ADC did not create the tail."

**审稿人致命一击（我方自噬）**：上面那条 "claim" 里"reducing refinement and deployment cost"——冻结 opacity
反事实实测**不省**（地图反大 35%，PSNR −0.53dB）。所以连 codex 自己的 best claim 在我们的 2060 上也站不住
"省成本"。**审稿人若要求"要么省 compute 要么更好质量要么更小 map"，Idea A 一条都拿不出新东西**——它
只是在解释已经被证实零代价的删除为什么能删（来源=refine 软选择），这在 strict CCF-C 会被当"mechanism
note"而非贡献。

---

## 诚实结论 + 推荐行动（Phase 4.5）

**三周现实下，没有一个待发散的新 idea 能把项目从"窄观测"抬成"机制贡献"。**

三个互斥的诚实去路（按 ROI 排）：

1. **【守】把窄主线写成可投稿**（Idea A，几乎零新 GPU）：用 P2-T 36-run 主表（骨干 ATE 有竞争力）
   + terminal 零代价压实 + freeze 机制解释 + theory 上界，拼一篇**实证/工程向** CCF-C。标题避开
   "significance-guided pruning"（撞 MGS-SLAM），突出 "low-opacity floater cleanup / zero-render-cost /
   refine soft-selection"。诚实且不烧 GPU，但注定是**平庸但真实**的一篇。
2. **【探】0.5 GPU-hr 探针救 Idea B**：检查被删的低贡献高斯是否天然集中在"近期受过扰动的区域"
   （recency / visibility 信号），若是，dynamic-aware recency 压缩可作独立贡献且不撞 MGS；若不是，
   关 Idea B。**这是唯一还能长出"动态专属"贡献的口子，成本一颗烟。**
3. **【弃】接受的现实**：3 周不是"想出新机制"的时候，是"把已证实的东西写成 pass"的时候。若审稿标准苛刻
   to CCF-C 需要机制贡献，那么**诚实结论可能是这轮拼不出**，不如把子集投 CVM（10/26，成长版有更多时间）。

**推荐动作**：先跑 Idea B 的 0.5-GPU-hr 探针（决定能不能救出唯一独立贡献）；同时启动 Idea A 的 MMM 稿
（数据已齐，不冲突）。若 B 探针负 → 落 Idea A 保底；若 B 探针正 → B 作主打、A 作实证面。

---

## 实验计划（refine-logs/EXPERIMENT_PLAN.md 摘要，详情见该文件）

| # | 实验 | GPU | 判定 | 状态 |
|---|---|---|---|---|
| E1 | **Idea B 探针**：低贡献高斯是否含 recency/motion/visibility 信号（在线日志已有），若是 → 独立贡献；否 → 关 B | ~0.5h | 是否有 >opacity 的可压缩信号 | 待跑（0.5-GPU-hr） |
| E2 | **Idea A 广义化**：P2-T 36 run 已齐，补 1-2 seq 的 contribution-vs-opacity 对照（可选）| ~1h | 证明 opacity-only 已足够 / 或 complex score 更强 | 已有数据为主 |

> 除非 E1 探针为正，否则**不启动任何新的大规模 campaign**。3 周预算留给 MMM 稿写作（Idea A）+ 可能的
> E2 小对照。

---

## Next Steps
- [ ] 跑 E1 探针（0.5 GPU-hr）——决定 Idea B 生死
- [ ] 按 E1 结果定稿 IntendedA/B：B 正→B 主打；B 负→A 保底
- [ ] 启动 MMM 稿（`papers/mmm/`，数据已 P2-T 齐）
- [ ] CVM 10/26 作成长版接力（有 2 个月，可重探 gaussian-level motion ledger）
