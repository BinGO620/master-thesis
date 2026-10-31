# Research Brief — Dynamic 3DGS SLAM，CCF-C 冲刺

## Problem Statement
在 MonoGS（动态 3DGS SLAM）上加一个方法贡献，使其 3 周末内达到可投 CCF-C（MMM 8/30 主攻，CVM 10/26 接力）。**需要一个能站着过审稿、且现有 GPU（2060 6GB）3 周内能跑完证据的贡献**。

## Context
- 基座：MonoGS + 自研 combined backbone（mask-both + RobustTracking + DynamicKeyframe + ReliabilitySignal + insert-then-prune lifecycle），在 Bonn 动态序列上自跟踪。
- 骨干 ATE 有竞争力：balloon 3.07 / mv_no_box 2.58 cm（prune 3-seed），介于 RGD-SLAM 2.26 与 DG-SLAM 3.65 之间。6 序列 36 run 主表已齐（P2-T）。
- `papers/mmm/` 已有 theory.md（op<0.01 贡献<1% 的数学上界）与 mechanism.md（已证伪重写中）。

## Constraints
- **Compute**：RTX 2060 6GB（VRAM 上限硬约束）。全实验 ~15-28h/campaign 的量级可行；**FPS 是 2060 的数不得与竞品并列**；大型 render 可离线（3090 或离线重渲）。
- **Data**：Bonn dynamic（balloon/balloon2/mv_no_box/mv_no_box2/pt1/pt2）、TUM、Replica 在 `/data/Datasets`。mask 已冻结（GTMC/MaskRCNN）。
- **Timeline**：MMM 8/30（~3 周）；CVM 10/26 接力。CVM 是 MMM 成长版（同方法两篇）。
- **Target venue**：CCF-C，MMM 非必投、投期随实验状态。**缺一个 pass 贡献/机制贡献级的主打**，不是从零（骨干 ATE 已能当 floor）。

## What We Already Tried（死人清单 — 不回炉）
- **在线抗动态机制全判死**：deferred ATE 6/6 差、eviction 复核 NO-GO、α-carve 闸门不可达、ReliabilityTracking +1.2% flat、DBA-photo NO-GO、CoarsePoseInit 证伪、FullFramePose/全帧 PnP negative、masked_icp 负结果。
- **compactness 四次独立复现**（−55/−54/−47/−51%）但 headline 死（S6 只 2/6 dominate、等预算需退化成全插再全删）。
- **terminal compression（本项目的唯一直观「幸存正向」）**：删终图 op<0.01 高斯 12/12 run 删 9-16%、|dPSNR|≤0.0001dB。**但机制被证伪**——op<0.01 tail 不是在线 ADC 稳态，是 26000-iter color-refinement 的 opacity 软抑制产物；frozen-opacity 反事实证实（tail 12.8%→3.7%），但锁 opacity 非免费修复（−0.53dB，N+35%），「refine-aware 省参」贡献不成立。
- 结论：**任何建立在「在线删东西改善地图/跟踪」或「终端压实是系统级省参」上的 idea 都不站。**

## Surviving Assets（可当实证面 / 平台的）
1. **动态 3DGS SLAM 骨干 ATE**（balloon 3.07 / mv_no_box 2.58 cm，6 序列 36 run 主表）——实证 floor。
2. **frozen-pose de-confounding 装置**（P2-SF，self-frozen，ATE 注入 gate 逐位复现到 4dp）——现成的受控评估基础设施。
3. **theory.md 的 op<0.01 贡献上界**（数学上仍成立，不依赖 tail 来源）。
4. **零代价终图压实的观测**（12/12 删 9-16% |dPSNR|≤0.0001dB）——可复现，但弱（被判定非系统级贡献）。
5. **完整的预注册/合同/复跑纪律**（同 campaign 重跑锚 + gate）——评估可信度高的平台。

## Non-Goals（不回炉、不追）
- 回到 deferred/eviction/α-carve/RT/DBA 在线抗动态。
- 把 terminal compression 当「省 compute / 修复 refine 缺陷」写（已被反事实否）。
- 追新 ATE headline 或位姿改进（RNN 跟踪侧是深坑，多轮无 gain）。

## Open Direction（本 pipeline 要探索的发散区）
我们在「能站的贡献」上缺一块。候选未探/浅探方向（开放发散，不预设）：
- 终图 **opacity 软选择 → map 压缩/量化/存储**（3DGS 存储效率，K-12 时代新热点）。
- **refine 阶段本身**的机制利用（而非移除）——opacity DOF 的软选择能做什么。
- 动态场景**特定**、而非通用抗动态的东西（mask 覆盖率自适应、时序一致性、多源融合）。
- 用 P2-SF 装置做一个**干净、可辩护**的机制 isometry（而非 victory）。
- 3DGS map 的 **memory/latency/efficiency** 相比竞品（6GB 跑完是卖点）。

## 产出要求
- 输出到 `idea-stage/IDEA_REPORT.md`（含 ranked ideas + novelty + reviewer 反馈 + 3 周内可达的实验计划）。
- 每个 idea 必须对照上表死人清单 + 幸存资产：能站 ≠ 好看，必须有 3 周内 2060 能验证的证据设计。
