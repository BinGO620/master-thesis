# 摘要

> 状态：中英双语成稿 v1（中文 ~750 字，2026-09-05；英文同版，2026-09-15
> 核对为完整成稿而非骨架——原状态行"英文骨架待扩"已过期）。终稿抛光
> 待研究章收口后统一进行。

## 中文摘要（成稿 v1）

面向动态场景的 3D 高斯泼溅（3DGS）同步定位与建图（SLAM）研究。
动态内容违反刚性世界假设，其代价不是精度下降而是量级崩溃：未经
动态处理的 3DGS-SLAM 基座在动态基准上漂移 39-147cm，而静态场景
仅约 1.5cm。本文从观测、估计、表示三个正交层次组织研究内容：

（1）观测层——免类别先验的可靠性引导动态跟踪（RoGS-SLAM）。主流
方法以外部类别网络检测并移除运动体，继承了闭集标签与硬边界的
缺陷。本文以观测光流与刚性重投影流的分歧构造逐像素静态置信，
以有下界的 Cauchy 降权替代 0/1 移除；配合均匀关键帧覆盖、Huber
IRLS 重加权与 lineage 提交-撤销生命周期构成四组件系统。在 18 条
RGB-D 序列的统一协议下，crowd 场景达到 2.2-2.3cm ATE（显存
4.0GB），并以 120-run 预注册因析测量组件必要性：无任何序列奖励
全部组件，组件必要性依场景类型而定。该工作已投稿国际会议。

（2）估计层——跟踪循环内的在线滑窗光度联合优化（SWBA）。逐帧
光度优化的位姿误差以随机游走累积为全局漂移；本文以边类型×跨度
的四象限消融（各 3 seeds）系统证明漂移的事后不可修复性——短程
边局部一致而不可见，长程边被动态污染而方向错误。据此提出 SWBA：
以稠密窗口光度边在新关键帧入场时联合重估最近关键帧位姿并立即
回灌跟踪，修正发生在错误尚局部之时。person_tracking 序列 ATE
13.62±3.27→7.83±0.51cm（−42%，两层架构叠加逐帧部署门控，
3-seed 确认），为该架构同类方法已知最优；并实证其适用
边界——对事件型漂移有效、对连续累积型无效。

（3）表示层——场景状态转换下的可信度驱动高斯生命周期。预注册
四臂 pilot（含安慰剂门禁）验证退出机制后，三序列 × 三臂 × 3 seeds
的正式研究将贡献主张修正为地图维护端：残影清理在 2/3 序列成立
（填充保守化臂静态区残差改善最强，3/3 配对），跟踪端增益未随样本
量复现而撤回；与（1）的提交端生命周期合成完整闭环。

本文全部实验遵循预注册判决、激活核实与负结果如实呈现的方法论
纪律，证据链完整可复核。

关键词：动态 SLAM；3D 高斯泼溅；鲁棒估计；光流一致性；滑窗
联合优化；生命周期管理

## Abstract（成稿 v1）

This thesis studies simultaneous localization and mapping (SLAM) with
3D Gaussian Splatting (3DGS) in dynamic environments. Dynamic content
violates the rigid-world assumption at a catastrophic rather than
incremental cost: an unmodified 3DGS-SLAM backbone drifts 39-147cm on
dynamic benchmarks against roughly 1.5cm on static scenes. The thesis
organizes its contributions across three orthogonal layers:

(1) Observation layer - reliability-guided tracking without class priors
(RoGS-SLAM). Instead of detecting and removing movers with an external,
class-conditioned network, we derive a per-pixel static confidence from
the disagreement between observed optical flow and rigid reprojection
flow, and down-weight rather than remove, with the weight bounded away
from zero. Together with uniform keyframe coverage, Huber IRLS
reweighting, and a lineage commit-retract lifecycle, the four-component
system tracks the crowd scenes at 2.2-2.3cm ATE (4.0GB) under one
18-sequence protocol; a pre-registered 120-run factorial finds that no
sequence rewards all components - component necessity is regime-dependent.

(2) Estimation layer - sliding-window photometric BA inside the tracking
loop (SWBA). Per-frame photometric optimization accumulates pose error
as a random walk; a 2x2 factorial over edge type and span (3 seeds each)
systematically demonstrates that the drift is not recoverable post hoc -
short edges are locally consistent and blind to it, long edges are
dynamically contaminated and push the wrong way. SWBA therefore optimizes
the recent keyframe poses with dense window photometric edges at every
keyframe insertion and writes corrections back into tracking
immediately, so the fix happens while the error is still local. On
person_tracking, ATE improves 13.62±3.27 -> 7.83±0.51cm (−42%, the
two-layer architecture with per-frame deployment gating, confirmed over
three seeds), with the scope boundary honestly characterized: effective
for event-type drift, ineffective for continuous accumulation.

(3) Representation layer - credibility-driven Gaussian lifecycle under
scene-state transitions. A pre-registered four-arm pilot with a placebo
gate validated the exit mechanism; the formal study (3 sequences x 3 arms
x 3 seeds) then corrected the contribution claim to the map-maintenance
side: ghost cleanup holds on 2 of 3 sequences (the conservatized-fill arm
improves static-region residuals most, 3/3 paired), while the tracking
gain did not reproduce at the larger sample size and was retracted,
completing the lifecycle loop begun by (1)'s commit side.

All experiments follow pre-registered verdicts, mandatory activation
verification, and honest reporting of negative results; the evidence
chain is fully reproducible.

**Keywords**: Dynamic SLAM; 3D Gaussian Splatting; robust estimation;
optical-flow consistency; sliding-window optimization; lifecycle management
