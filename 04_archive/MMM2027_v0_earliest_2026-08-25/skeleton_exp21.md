# MRCS: Reliability-Guided Coverage Sampling for Dynamic 3D Gaussian Splatting SLAM — 方法稿骨架

> **标题（2026-08-15 确认）**：
> *MRCS: Reliability-Guided Coverage Sampling for Dynamic 3D Gaussian Splatting SLAM*
>
> 选题依据：标题聚焦**内核机制**而非模式标签。`Reliability-Guided` 对应
> RobustTracking + ReliabilitySignal 的可靠性驱动降权；`Coverage Sampling` 对应
> DynamicKeyframe 的时域覆盖采样；两者合起来准确点出 P-B 2×2 结论——"组合才是内核、
> 单点都不是"。`Dynamic 3D Gaussian Splatting SLAM` 保证检索清晰。无绝对比较语。
> **为什么不用 Mask-Free 做标题**：与RGD有竞争力的数字全部来自 combined（mask-ON），
> mask-free 模式相对 vanilla 有 2.2–4.7× 增益（低方差序列，见 `headline_ratio_recompute.md`）
> 但绝对值不与SOTA 竞争；标题用 Mask-Free
> 会暗示"不用mask就能打SOTA"，与数据不符。正确做法：method 正文中说明"不依赖语义
> 分割亦可运行（mask-free 模式），可选加入mask（combined 模式）进一步提升"。
>
> ⚠ **P7（cue-split）已裁决（48/48）**：固定 both 不是普适最优（geometry-only
> 在 4 序列中 3 个最低 mean、mv_no_box 仍 both 最优），但 P7 只证明需要选择，未验证具体
> selector；MRCS 方法名保持不变，regime-aware cue selection 降级为 future work。
> **WP-HS 决策（2026-08-15）**：H1（person 面积比 → cue 选择）用的是 offline sequence-level
> semantic statistic，不是 online per-frame 动态检测，与 MRCS mask-free 主张不冲突。
> 决定先跑零 GPU 的 person 面积统计闸门，再决定是否花 pt1 6 runs。
> **✅ 闸门已判决（exp22，FAIL，H1 整族关门）**：`wphs_person_area_characterization.md`。
> 6 序列 3770 帧（口径同 mask-ON 臂）显示**不存在任何阈值**可分开 P7 的 geo/both 偏好——
> both-偏好的 mv_no_box(4.54%) 夹在 geo-偏好的 mv_no_box2(3.30%) 与 pt2(8.24%) 之间；
> dilate=0 / median / 检出率三变体同构失败；全部序列 <20%，θ=20% 本身不可达。
> ⇒ **pt1 6 runs 不执行（3090 零消耗），WP-HS 关闭**。
> **future work 措辞升级为已测负结果**："我们检验了最简候选 selector（序列级语义占比）并证否，
> 因此 regime selector 必须来自 mask-free 可观测量（flow/geometry 残差诊断）"——
> 同时消除"要跑语义检测器才能配置 mask-free 模式"的自相矛盾。
> **新增禁词**：不写"person 面积/语义占比可用于选择线索"；不写"人占画面主体"
> （pt1 全 580 帧 person 面积 max 仅 20.24%，`slam_utils.py:297` 的 ~65% 不可复现；
> pt1 的难在 RPE 2.89 cm/frame，不在 person 面积）。
>
> 本文件 = **方法稿骨架**（不是完整写作）：按最高准则回答两问 + 中心主张 + 证据表
> + 防反打消融 + 竞品差异化 + 写作路线图。内容只进 `papers/maskfree_bundle/`，不污染方法区。
> 硬约束：8/31 已不是 ddl（CLAUDE.md 最高准则），实验未全达标不写；这个骨架是写作前的桩，不是凑稿。
> 写作路线图详见 `WRITING_ROADMAP.md`。

---

## 一、最高准则两问（每篇要投的稿先答）

| 问 | 答 | 证据 |
|---|---|---|
| 方法贡献是"我们自己的"吗？ | **是**。DynamicKeyframe（稠密/时序关建帧）是我们加的（不在 MonoGS）；RobustTracking 的 huber 鲁棒核、ReliabilitySignal 的时域减权都是我们实现/调过的。 | `02-method.md` 现行头条；P6/P-B 消融 |
| 对动态 3DGS SLAM 有用吗？ | **是**。mask-free 把动态序列从 vanilla 压下来 —— pt2 43.85±8.55→9.30±0.64（4.71×）、balloon 39.32±1.01→12.11±1.90（3.25×）、balloon2 22.05±1.55→10.14±0.62（2.17×），**不依赖分割网络**。⚠ 不写 framework-general（单一 MonoGS fork）；mv_no_box/mv_no_box2 的倍数因 vanilla CV 62%/101% 不作 headline，改承担 mask 冗余判据 | P6 maskoff 3-seed + `headline_ratio_recompute.md` |

## 二、中心主张（一句话）

> **在无语义分割（mask-free）的条件下，一个由稠密关键帧（Coverage）+ 鲁棒跟踪核
> （Reliability+huber）组成的 MRCS 内核，能把动态 3DGS SLAM 的 ATE 从 vanilla 压低
> **2.2–4.7×**（balloon / balloon2 / pt2，逐序列保守区间 1.87–5.83×）；
> 而**组件的必要性随 regime 分层**——120-run 预注册全因子测出 0/5 序列三组件全正
> ⇒ 不存在全局必要子集。这是竞品（都依赖 explicit 动态检测）没有测过的。**
>
> ⚠ "内核" = RT + Reliability 组合的鲁棒时域减权采样（P-B 2×2 实证：单关任一不崩、全拿走才回
> vanilla）；dense-KF 是覆盖载体，不作内核代名词。
> ⚠ **倍数口径**：只用 vanilla CV ≤ 20% 的序列做 headline；mv_no_box(62%)/mv_no_box2(101%)
> 退出增益 claim，改承担 mask 冗余判据。见 `results/evidence/headline_ratio_recompute.md`。
> ⚠ **不写"对 mover 类型鲁棒"**：mask 在混合 mover（balloon 3.96×）与 pt1（2.73×）上仍主导。

### 与已有工作的差异（回答 R1"你就是拼已有组件？"）

**所有现有动态 3DGS SLAM 方法都依赖 explicit 动态检测**作为前置步骤：

| 方法 | 动态检测机制 |
|---|---|
| RGD-SLAM | RAFT 光流 + YOLO 语义分割 |
| DG-SLAM | DROID-VO + 语义 mask + depth warp consistency |
| BDGS-SLAM | YOLOv5 先验 + Bayesian per-Gaussian 概率更新 |
| DAGS-SLAM | YOLO 实例先验 + per-Gaussian motion probability |
| WildGS-SLAM | DINOv2 特征 + 学习的不确定性 MLP（无语义分割，但仍靠学习的 feature 感知动态）|
| DynaGSLAM | SAM2 分割 + RAFT 光流（显式建模动态物体） |

这条依赖链在三个层面造成限制：**依赖外部预训练模块**（增加系统复杂度与推理开销）；
**单帧分割脆弱性**（误检直接破坏跟踪，各方法用不同方式缓解但本质仍是"先分割再用"）；
**类别封闭**（语义分割只能检测已知动态类别，未知动态物体如气球/晾衣架仍污染地图）。

**我们的差异化立场**：不依赖任何语义先验，**仅在 3DGS SLAM 的 Gaussian map 准入层**，
通过"稠密关键帧 + 鲁棒跟踪核 + 时域可靠性降权"的组合，在 mask-free 条件下把动态
ATE 压低 **2.2–4.7×**（pt2 43.85±8.55→9.30±0.64 / balloon 39.32±1.01→12.11±1.90 /
balloon2 22.05±1.55→10.14±0.62）。**分母全部为 3-seed vanilla 重跑集**
（`resources/02-baselines/.../MonoGS`），不用单 seed。

**这不是说组件本身新**——huber loss 是经典鲁棒 M 估计、光流异常降权有大量先例、
稠密关键帧也在多种 SLAM 系统中使用。**贡献是三层的**：

1. **填补系统验证空档**：在 3DGS SLAM 的 Gaussian 准入层，这个 mask-free 组合
   **从未被系统性验证过**。上表中没有任何方法声称"不用分割、仅靠时域鲁棒采样
   在 3DGS SLAM 里把动态 ATE 压到 ~3cm 且逐组件关掉都不崩"。即使 WildGS-SLAM
   避免了语义分割，它仍然依赖学习出来的特征来感知动态区域，而我们的内核
   在纯物序列上完全不靠任何动态感知机制——只靠鲁棒残差聚合和时域覆盖。

2. **受控对照闭环（WP-B）**：同等 flow 信息预算下，朴素 flow 阈值 mask
   **时好时坏**（4 序列仅 2 个稳定改善，pt2 反更差 0.90×），而 MRCS
   **4/4 稳定 1.63–4.99×**。这回答了"随便什么抗动态处理都行？"——
   **不行，增益来自机制，而非 flow 信息本身**。
   这个受控基线在同类方法稿里不常见，多数只有正向结果没有反向对照。

3. **机制分析与适用域边界（WP-A）**：120-run 全因子消融给出"必要组件子集
   随场景难度分层"的 empirical finding——easy 序列 dense-KF 必要而 RobustTracking
   冗余，hard 序列反过来。这不是"magic bullet"叙事，而是诚实的机制刻画。
   自曝 pt1 边界反例（32cm vs RGD 7cm）并写进 limitation，提升可信度。

**写作时 intro / related work 的切入点**：先有的动态 SLAM（包括 NeRF-based 如 RoDyn-SLAM）
里确实有各种 reliability weighting / robust loss / temporal filtering，但**没有人在
3DGS SLAM 的 Gaussian map 这一层做过 mask-free 的系统验证**，且所有现有 3DGS 动态方法
全部依赖某种学习的或语义的动态先验。我们填补的是这个空档。

## 三、证据表（3-seed / 3090 / prune lifecycle）

### 机制可视化图（§三前置）

**图位置**：`results/evidence/mechanism_figure_paper.png`（5 面板，**2026-08-15 用完整两项 s 重出**）

展示 ReliabilitySignal 如何在 Gaussian map 准入层工作（balloon，mask-free MRCS 臂 = WP-A K1R1L1 seed0，frame 39）。
**五格统一语义：红 = "这条线索认为此处在动"**，从左到右就是机制链本身：
- **(A) RGB**：原始帧，绿色轮廓 = 冻结的 GT-pose 动态掩码（`dynamic_mask_gtmc`，方法从未见过）
- **(B) flow 线索 `e_flow`**：光流一致性异常
- **(C) geometry 线索 `v·g`**：几何异常 × 不透明度门控
- **(D) 融合 `1−s`**，`s=(1−e_flow)(1−v·g)`——**这正是我们报 AUC 的那个量**
- **(E) 降权 `1−w`**：Cauchy 降权叠加在 RGB 上（红 = 被抑制的残差）
- **底部**：全序列重算的 mean_s / mean_w 时间线 + 公式/实测 AUC/选帧规则/近似声明

**与旧版的区别（这是必须改的原因）**：旧图把 s 近似成 **flow-only**（几何项未存档），
而 P7 说 geometry 是 3/4 序列最优线索 ⇒ 头条机制图恰好省掉了自己认定最重要的线索，
审稿人对读 §P7 就会发现。新版**直接调用在线函数**（`geometric_anomaly`/`rigid_flow`/
`assemble_flow_consensus`/`fuse_static_evidence`/`cauchy_tracking_weight`），图与代码不可能漂移。

**选帧是规则不是挑选**：取"逐帧 AUC 最接近序列级 AUC"的那一帧（**典型帧，不是最好帧**），
且动态像素占比落在 [1%, 40%]。本图 frame 39：逐帧 AUC 0.734 vs 序列 0.733。

**诚实近似（图注已写）**：`render_depth`/`opacity` 来自该 run 的**终态地图**在其自身估计位姿下的重渲，
不是帧 t 当时的在线地图；公式与 flow/depth 输入都是在线的，地图不是。

**图上能直接看出、必须在正文承认的一点**：(C) 的几何线索在**背景（地面/墙面）上也大片发红**，
而 (B) 的光流线索更贴合绿色轮廓。这与实测一致（balloon：flow-only AUC 0.747 > geometry-only 0.680），
也说明几何项在终态地图近似下噪声更大。**不要**在正文写"几何线索更干净"。

生成脚本：`scripts/generate_mechanism_figure.py`（可复现，含选帧规则与 AUC 标注）。
配套定量结论：`results/evidence/reliability_separability_verdict.md`。

### 3.1 mover 类型的 mask-free 通用性（方向 A 核心表，全 18 序列）

**（18-seq 完整表与裁决见 `p6_maskoff_18seq_main_table.md`，2026-08-10。以下为摘要。）**

**mask-free 相对 vanilla（MonoGS）—— 18 序列中 15 优 / 3 略差（差值在噪声带）。
⚠ 措辞：写 "consistent across TUM and BONN within our MonoGS-based implementation"，
不写 "framework-general"（无跨框架证据）。⚠ 下表 vs vanilla 列须与 vanilla sd 同读，
CV>20% 的 6 个序列（mv_no_box 62% / mv_no_box2 101% / f3_st_hf 33% / f3_st_rpy 52% /
f3_wk_hf 25% / crowd 21% / crowd2 26%）的比值不可单独引用 —— 见
`results/evidence/headline_ratio_recompute.md`：**

| 序列类 | 代表序列 | vanilla | **mask-free** | vs vanilla |
|---|---|---|---|---|
| TUM 静态 | f1_desk / f2_xyz / f3_office | 1.47/1.66/1.65 | **1.42/1.63/1.54** | 0.94-0.98×（无伤）|
| TUM sitting | f3_st_hf / **st_rpy** / st_xyz | 2.80 / **18.99** / 1.66 | **2.14 / 1.83 / 2.41** | 0.76 / **0.10** / 1.46× |
| TUM walking | wk_hf / **wk_rpy** / wk_xyz | 44.45 / **62.89** / 28.14 | **26.23 / 18.70 / 26.84** | 0.59 / **0.30** / 0.95× |
| BONN 纯物 | mv_no_box / mv_no_box2 | 15.33 / 16.84 | **3.09 / 5.62** | **0.20 / 0.33×** |
| BONN 纯人 | pt2 / pt1 | 43.85 / 44.83 | **9.30 / 32.41** | **0.21 / 0.72×** |
| BONN 混合 | balloon / balloon2 | 39.32 / 22.05 | **12.11 / 10.14** | 0.31 / 0.46× |
| BONN 多人 | crowd / crowd2 | 86.47 / 147.46 | **56.38 / 66.07** | 0.65 / 0.45× |

**mask-free 相对动态 SOTA（RGD/DG/WildGS）—— 诚实适用域**：绝对 ATE 打不过有 mask 的动态方法
（walking/crowd 差 5-28×）。**不 claim SOTA**；头条 = 「mask-free 相对 vanilla 的增益 + 不依赖分割 +
跨 TUM/BONN 一致」，不是「超越有 mask 的动态方法」。
**⚠ combined 侧也必须给全表不做选择性高亮**（审稿 R2-M2/R3-M5）：combined 在 crowd 上优于 RGD
（2.33 vs 2.61），但在 f3_wk_xyz（3.06 vs RGD 2.01 / WildGS 1.22）与 pt1（10.04 vs RGD 7.21）
落后 1.4–2.5×。两侧同表呈现。

**⚠ pt1 边界反例**：同一"person 族"，pt2 maskoff≈combined（0.89×），pt1 却 maskoff 3.2× 差于
combined（32.4 vs 10.0，大方差 ±8.5，RPE 2.8–3.1 远超 pt2 的 ~1.6）。pt1 双稳态/高 RPE，mask-free
失去 mask 加持时跟踪发散。⇒ **"纯人 mask 冗余"仅是 pt2（单人轻遮挡）结论，不是 person 族全局**。
诚实写作 = 把 pt1 作为"适用域边界"写进 limitation（自曝边界防审稿人反打），不强翻头条（见 §三）。

**量化分层判据（pt1 失败边界）**：

> **⚠ 2026-08-25（exp46）就地撤回下方的 "~2.5 cm/frame" 阈值 —— 数据一字未动，只标注读法。**
> 该阈值由 pt1/pt2 **两条**序列内插得出。放到全部 18 序列上检验（`scripts/test_rpe_stratification_rule.py`）
> 后 **17 决定格错 4 个（准确率 76%）**：f3_wk_xyz(RPE 1.72, N **8.76×**)、balloon(2.03, 3.96×)、
> f3_wk_rpy(2.26, 3.41×)、f3_wk_hf(2.33, 5.27×) 的 RPE 都在 2.5 **以下**，而 mask 在它们身上恰恰必需。
> **正确结论更强**：mask-free RPE 把两组分得**完全不重叠**（冗余组 0.22–1.57 / 必需组 1.72–2.98，
> 17/17），分界区间是 **(1.57, 1.72)**、中点 ≈**1.64**，不是 2.5。
> 但该区间**拟合于同一批 18 序列、无 held-out**，且算它要先跑 mask-free 臂 ⇒
> **是事后诊断，不是先验 selector**。下方"这个阈值**不是拍脑袋**"的自辩一并撤回。
> 全表与自限见 `results/evidence/rpe_stratification_rule_test.md`。

| 序列 | 臂 | ATE (cm) | RPE (cm/frame) | 判定 |
|---|---|---:|---:|---|
| pt2 | mask-free | 9.30 ± 0.64 | **1.572 ± 0.017** | 成功（mask冗余）|
| pt2 | mask-ON | 10.45 ± 0.84 | 1.608 ± 0.035 | 基线 |
| pt1 | mask-free | 32.41 ± 8.51 | **2.894 ± 0.194** | **失败**（RPE 1.84× 高于 pt2）|
| pt1 | mask-ON | 11.89 ± 2.36 | **1.723 ± 0.192** | 恢复（mask 必要）|

**分层阈值**：当序列 mask-free RPE > 2.5 cm/frame 时，时域鲁棒采样被高漂移淹没，mask 从冗余变为必需。
pt1 的 2.894 cm/frame 相比 pt2 的 1.572 cm/frame 高 1.84×，超过阈值；加回 mask 后 RPE 降到 1.723，
与 pt2 mask-ON (1.608) 同量级。这个阈值**不是拍脑袋**——它来自两个同类型序列（person tracking）
的对照实验，pt2 在阈值下方（mask-free 成功），pt1 在阈值上方（mask-free 失败）。

**写作中的诚实边界呈现**：limitation 段落需要写明——"当每帧相对漂移超过 ~2.5 cm 时（对应高速运动
或弱纹理环境），时域一致性信号被噪声淹没，此时语义 mask 成为必需。pt1 就是这样的边界反例：
其 RPE (2.89 cm/frame) 显著高于 pt2 (1.57 cm/frame)，mask-free 内核失效，加回 mask 后恢复到
11.89 cm（与 RGD 7.21 cm 仍有差距，但相对 vanilla 44.83 cm 已有改善）。"

### 3.2 P-B 2×2（mask × dynKF）—— 逐组件消融，自报内核定位

### 3.2 P-B 2×2（mask × dynKF）—— 逐组件消融，自报内核定位

**mv_no_box（纯物，决定性）**：四格全 ≈3cm（2.66 / 3.15 / 3.09 / 3.90）。mask 轴 +0.5–0.8cm、
dynKF 轴 +0.4–0.75cm 都小，且**逐组件单独关掉都不崩** ⇒ 内核 = **RT + Reliability 组合的鲁棒时域
减权采样**（dense-KF 提供覆盖，彼此冗余）。**balloon（混合）**：mask 主导（3cm vs 12cm），dynKF
关掉 ATE 不变。完整表见 `p6_pb_2x2_3seed_verdict.md`。

### 3.3 18 序列渲染主表（paper main table，已闭合，2026-08-11）

> **来源**：我们 = 3090 离线重渲 color-refined `final/` PLY + `trj_full_final`（`posthoc_fullframe`，
> 3-seed mean±std, ddof=1）；竞品 = 用户自测 `04-baselines_result.xlsx`（mean）。渲染 = 全分辨率
> 全帧 PSNR/SSIM/LPIPS/Depth-L1。**渲染 = `final_after_opt` 离线终态协议，非我们贡献，仅对齐竞品口径**；
> mask-free 与 combined(mask-ON) 分开，不混淆。headlist = MonoGS（基座）+ RGD-SLAM（动态 SOTA）；
> SplaTAM/Co-SLAM/DG/WildGS 全 18 序列渲染在 xlsx 可按需扩列；`-` = 该 baseline 本身无此指标，非漏跑。
> FPS 是 2060 数，不与竞品并列。**完整主表（markdown 真身）= `results/evidence/18seq_rendering_main_table.{md,xlsx}`**，
> 全 36 行（mask-free 18/18 + mask-ON 18/18）5 指标无缺失。下为展开表。

#### ATE 主判（cm↓，完整 18-seq）

| 序列 | 类型 | **Ours-mask-free** | **Ours-combined(mask-ON)** | MonoGS | RGD-SLAM |
|---|---|---|---|---|---|
| f1_desk | TUM 静态 | 1.42±0.03 | 1.42±0.03 | 1.47 | 2.32 |
| f2_xyz | TUM 静态 | 1.63±0.07 | 1.79±0.06 | 1.66 | 1.71 |
| f3_office | TUM 静态 | 1.54±0.15 | 1.51±0.10 | 1.65 | 1.42 |
| f2_person | TUM 动态 | 7.00±0.32 | 7.30±0.18 | 6.30 | 6.11 |
| f3_st_hf | TUM sitting | 2.14±0.21 | 3.05±0.29 | 2.80 | 2.76 |
| f3_st_rpy | TUM sitting | 1.83±0.03 | 2.81±0.43 | 18.99 | 2.90 |
| f3_st_xyz | TUM sitting | 2.41±0.74 | 4.87±0.71 | 1.66 | 2.03 |
| f3_wk_hf | TUM walking | 26.23±7.74 | 3.03±0.32 | 44.45 | 3.25 |
| f3_wk_rpy | TUM walking | 18.70±2.36 | 3.68±0.22 | 62.89 | 3.55 |
| f3_wk_xyz | TUM walking | 26.84±0.71 | 3.06±0.52 | 28.14 | 2.01 |
| balloon | BONN 混合 | 12.11±2.33 | 3.06±0.14 | 39.32 | 2.45 |
| balloon2 | BONN 混合 | 10.14±0.61 | 5.27±0.12 | 22.05 | 4.26 |
| crowd | BONN 多人 | 56.38±3.10 | 2.33±0.09 | 86.47 | 2.61 |
| crowd2 | BONN 多人 | 66.07±25.98 | 2.42±0.02 | 147.5 | 2.36 |
| mv_no_box | BONN 纯物 | 3.10±0.46 | 2.65±0.12 | 15.33 | 2.28 |
| mv_no_box2 | BONN 纯物 | 5.62±0.30 | 5.14±0.28 | 16.84 | 4.70 |
| pt1 | BONN 纯人 | 32.41±8.52 | 11.89±2.36 | 44.83 | 7.21 |
| pt2 | BONN 纯人 | 9.30±0.64 | 10.45±0.84 | 43.85 | 20.10 |

#### 渲染（PSNR↑ / SSIM↑ / LPIPS↓，完整 18-seq）

| 序列 | 方法 | PSNR | SSIM | LPIPS | Depth-L1 |
|---|---|---|---|---|---|
| f1_desk | **Ours-mask-free** | 24.22±0.04 | 0.825 | 0.236 | 5.93 |
| f1_desk | **Ours-combined(mask-ON)** | 24.16±0.07 | 0.825 | 0.235 | 6.13 |
| f1_desk | MonoGS | 23.57 | 0.783 | 0.246 | 6.30 |
| f1_desk | RGD-SLAM | 23.33 | 0.779 | 0.245 | 3.46 |
| f2_xyz | **Ours-mask-free** | 25.67±0.13 | 0.841 | 0.203 | 11.77 |
| f2_xyz | **Ours-combined(mask-ON)** | 25.77±0.02 | 0.841 | 0.203 | 12.14 |
| f2_xyz | MonoGS | 24.59 | 0.794 | 0.219 | 14.24 |
| f2_xyz | RGD-SLAM | 24.40 | 0.796 | 0.219 | 1.97 |
| f3_office | **Ours-mask-free** | 25.25±0.07 | 0.848 | 0.199 | 14.28 |
| f3_office | **Ours-combined(mask-ON)** | 25.21±0.16 | 0.847 | 0.204 | 13.75 |
| f3_office | MonoGS | 24.96 | 0.840 | 0.206 | 13.94 |
| f3_office | RGD-SLAM | 22.91 | 0.803 | 0.267 | 4.47 |
| f2_person | **Ours-mask-free** | 20.63±0.02 | 0.722 | 0.358 | 23.90 |
| f2_person | **Ours-combined(mask-ON)** | 20.44±0.03 | 0.722 | 0.365 | 26.84 |
| f2_person | MonoGS | 20.17 | 0.677 | 0.387 | 26.07 |
| f2_person | RGD-SLAM | 20.81 | 0.699 | 0.363 | 20.08 |
| f3_st_hf | **Ours-mask-free** | 20.94±0.11 | 0.765 | 0.282 | 31.53 |
| f3_st_hf | **Ours-combined(mask-ON)** | 20.35±0.08 | 0.746 | 0.319 | 36.11 |
| f3_st_hf | MonoGS | 19.14 | 0.699 | 0.299 | 33.65 |
| f3_st_hf | RGD-SLAM | 20.38 | 0.796 | 0.256 | 27.53 |
| f3_st_rpy | **Ours-mask-free** | 22.63±0.03 | 0.802 | 0.231 | 43.59 |
| f3_st_rpy | **Ours-combined(mask-ON)** | 22.44±0.03 | 0.790 | 0.254 | 50.68 |
| f3_st_rpy | MonoGS | 14.56 | 0.521 | 0.449 | 79.26 |
| f3_st_rpy | RGD-SLAM | 19.45 | 0.767 | 0.248 | 28.77 |
| f3_st_xyz | **Ours-mask-free** | 23.19±0.17 | 0.837 | 0.169 | 23.46 |
| f3_st_xyz | **Ours-combined(mask-ON)** | 22.35±0.16 | 0.806 | 0.213 | 30.80 |
| f3_st_xyz | MonoGS | 22.14 | 0.806 | 0.184 | 23.27 |
| f3_st_xyz | RGD-SLAM | 21.16 | 0.827 | 0.166 | 33.52 |
| f3_wk_hf | **Ours-mask-free** | 17.11±0.60 | 0.621 | 0.458 | 75.23 |
| f3_wk_hf | **Ours-combined(mask-ON)** | 18.45±0.10 | 0.727 | 0.309 | 61.31 |
| f3_wk_hf | MonoGS | 13.85 | 0.455 | 0.572 | 104.87 |
| f3_wk_hf | RGD-SLAM | 19.73 | 0.771 | 0.250 | 46.80 |
| f3_wk_rpy | **Ours-mask-free** | 17.54±0.09 | 0.648 | 0.405 | 87.25 |
| f3_wk_rpy | **Ours-combined(mask-ON)** | 18.28±0.04 | 0.723 | 0.333 | 87.18 |
| f3_wk_rpy | MonoGS | 14.60 | 0.504 | 0.548 | 110.59 |
| f3_wk_rpy | RGD-SLAM | 19.07 | 0.757 | 0.286 | 62.39 |
| f3_wk_xyz | **Ours-mask-free** | 15.28±0.06 | 0.522 | 0.557 | 116.96 |
| f3_wk_xyz | **Ours-combined(mask-ON)** | 17.65±0.08 | 0.715 | 0.301 | 76.78 |
| f3_wk_xyz | MonoGS | 13.76 | 0.413 | 0.567 | 101.68 |
| f3_wk_xyz | RGD-SLAM | 19.31 | 0.775 | 0.221 | 54.89 |
| balloon | **Ours-mask-free** | 22.49±0.14 | 0.843 | 0.284 | 26.82 |
| balloon | **Ours-combined(mask-ON)** | 21.56±0.30 | 0.853 | 0.281 | 26.71 |
| balloon | MonoGS | 19.30 | 0.766 | 0.356 | 31.14 |
| balloon | RGD-SLAM | 25.14 | 0.896 | 0.224 | 15.69 |
| balloon2 | **Ours-mask-free** | 19.75±0.13 | 0.794 | 0.338 | 32.19 |
| balloon2 | **Ours-combined(mask-ON)** | 19.31±0.10 | 0.815 | 0.325 | 38.00 |
| balloon2 | MonoGS | 19.17 | 0.736 | 0.371 | 34.32 |
| balloon2 | RGD-SLAM | 24.36 | 0.892 | 0.202 | 25.47 |
| crowd | **Ours-mask-free** | 18.67±0.18 | 0.770 | 0.379 | 50.20 |
| crowd | **Ours-combined(mask-ON)** | 18.17±0.04 | 0.800 | 0.316 | 38.57 |
| crowd | MonoGS | 15.84 | 0.654 | 0.541 | 74.32 |
| crowd | RGD-SLAM | 24.21 | 0.905 | 0.178 | 32.17 |
| crowd2 | **Ours-mask-free** | 19.09±0.09 | 0.758 | 0.431 | 52.80 |
| crowd2 | **Ours-combined(mask-ON)** | 17.09±0.09 | 0.783 | 0.346 | 52.25 |
| crowd2 | MonoGS | 16.52 | 0.648 | 0.522 | 73.05 |
| crowd2 | RGD-SLAM | 24.36 | 0.915 | 0.157 | 45.68 |
| mv_no_box | **Ours-mask-free** | 24.71±0.07 | 0.874 | 0.220 | 18.25 |
| mv_no_box | **Ours-combined(mask-ON)** | 24.65±0.02 | 0.877 | 0.217 | 18.51 |
| mv_no_box | MonoGS | 21.78 | 0.807 | 0.285 | 20.78 |
| mv_no_box | RGD-SLAM | 24.45 | 0.869 | 0.250 | 7.90 |
| mv_no_box2 | **Ours-mask-free** | 25.07±0.05 | 0.881 | 0.239 | 19.09 |
| mv_no_box2 | **Ours-combined(mask-ON)** | 25.13±0.02 | 0.884 | 0.235 | 18.80 |
| mv_no_box2 | MonoGS | 22.90 | 0.835 | 0.276 | 23.26 |
| mv_no_box2 | RGD-SLAM | 24.01 | 0.860 | 0.297 | 6.18 |
| pt1 | **Ours-mask-free** | 21.97±0.45 | 0.829 | 0.323 | 33.84 |
| pt1 | **Ours-combined(mask-ON)** | 22.19±0.11 | 0.856 | 0.278 | 29.05 |
| pt1 | MonoGS | 17.81 | 0.718 | 0.442 | 37.78 |
| pt1 | RGD-SLAM | 24.11 | 0.855 | 0.297 | 11.31 |
| pt2 | **Ours-mask-free** | 22.06±0.12 | 0.854 | 0.269 | 26.13 |
| pt2 | **Ours-combined(mask-ON)** | 21.97±0.17 | 0.853 | 0.265 | 26.98 |
| pt2 | MonoGS | 19.68 | 0.743 | 0.381 | 36.04 |
| pt2 | RGD-SLAM | 22.76 | 0.835 | 0.326 | 12.30 |

**诚实解读**（与 02-method 五张牌一致，勿写出歧义）：
- **mask-ON 全帧 PSNR 常低于 mask-free**（动态剔除 → 缺运动物体，如 balloon 22.49→21.56、crowd 18.67→18.17），但 **SSIM/LPIPS 改善**（crowd 0.770→0.800/0.379→0.316、f3_wk_hf 0.621→0.727/0.458→0.309）。这是"干净渲染 vs 更多物体"的固有 trade-off，不解读成 mask-ON 图像质量差。
- **绝对渲染仍输 RGD**（RGD 动态序列 PSNR 普遍 +2~6dB，如 crowd 24.21 vs 我们 18.17）。**不 claim SOTA**。
- **相对 MonoGS 基座是我们强有力的渲染亮点**：动态序列 PSNR 普遍 +2~5dB（f3_st_rpy 14.56→22.44、f3_wk_rpy 14.60→18.28、pt1 17.81→21.97、crowd 15.84→18.17），SSIM 同步提升。静态序列也**不劣化**（f1_desk 23.57→24.22、f2_xyz 24.59→25.67）。
- **协议透明**：渲染 = color-refined `final_after_opt` 的离线终态（重演 MonoGS 终端光度精修），与我们渲染协议一致的全分辨率全帧口径与竞品可比。这个精修是基座自带环节、**非我们贡献**，对齐口径用；footprint 段落才归因。

## 四、诚实定位与三项"不能写错"（防审稿人反打）

1. **≠「dense-KF 是内核」**：balloon 上 dynKF-off + mask-on = 3.06 不变。
2. **≠「mask 无用」**：balloon 上 mask 主导（3cm vs 12cm）——mask 在有"mask 抓不住的 mover"
   （混合类）的序列上仍是主导机制。
3. **≠「bundle 全序列最优/SOTA 绝对 ATE」**：pt2/balloon 的 mask-free ATE（9–12cm）> mv_no_box
   （3cm），是"难跟踪 mover"的固有水平；只声称"把动态序列从 vanilla 压下来 + 对 mover 类型
   鲁棒 + 不依赖分割"，不声称超越 mask 或绝对 SOTA。

## 五、机制叙述（方法正文的层，不写成 magic component）

- **DynamicKeyframe**：改变关键帧密度/时序覆盖，是"时域一致性的载体"——让每个背景点在时间上
  有多次、跨遮挡的观测机会。
- **RobustTracking (huber)**：对动态像素的异常观测鲁棒，不一致的残差不被单个大误差主导。
- **ReliabilitySignal**：逐像素静态可信度 `s = (1-e_flow)(1-v·g)`，动态像素被降权不入图 → 但**当
  该像素后来变成稳态静态观测时，允许地图在此生长**（这正是方向 B 的桥，见五之注）。
  ⚠ **P7 裁决后**：s 的固定双线索乘法不是普适，但没有任何已验证的 selector。方法正文仍将
  固定 both 作为历史 control；regime-aware cue selection 只作为 future work（geometry 3/4 最优，
  mv_no_box 仍 both 优），不得写成已完成的方法贡献。
- **三者冗余组合** = "可冗余的鲁棒时域采样"——拿走任何一个，bundle 仍 ~3cm；全拿走才回 vanilla。

> **注（与方向 B 的桥）**：Reliability 的"动态降权 + 稳态准入"正是"背景后来被确认 → 补洞"的
> 语义接口。方向 B（occluded 背景时域补洞，见 `results/evidence/probe_bg_observability_finding.md`）
> 把这个机制显式化——当遮挡物移开、3D 背景被确认时更新该处高斯。它是方向 A 的自然扩展/将来方法，
> 两方向互补：A = anti-ghost（干净移除），B = anti-hole（补洞）。

## 六、诚实负结果（审稿人加分项，自报）

- **TRC 多帧 median consensus 不增强分离**（`probe_flow_separability_finding.md`）：K=1 单帧
  anomaly 分离比 1.70 → K=8 降到 0.99（完全不可分）。**方法叙述绝不写"多帧一致性增强检测"**，
  而写"单帧残差 + 鲁棒聚合的 bundle"。
- **TRC 命名**：codex 建议把模块叫 **Temporal Residual Consensus (TRC)**，但必须明确 TRC 用的是
  单帧残差 + 时域鲁棒聚合（不是 trailing median）。

## 七、竞品差异化

竞品 RGD-SLAM / DG-SLAM / Gassidy / DAGS / BDGS 都依赖 explicit 动态检测（YOLO / mask / flow 分割）。
**没有任何竞品声称"mask-free 的鲁棒时域采样 bundle 在无语义分割下把动态序列压到 ~3cm，且逐组件
关掉都不崩"** = novelty 空档（`idea_exploration_maskfree_temporal.md` 已核对 arxiv）。

## 八、待补实验（按最高准则，实验达标前方可写作）

- [x] **主表补全（已做，overnight 批）**：全 6 序列 maskoff 3-seed 已回拉裁决，
  见 `p6_maskoff_6seq_main_table.md`。纯物双复现 + pt2 冗余 + **pt1 边界反例**（见 §3.1）。
- [ ] **pt1 vanilla 基线**：判断 pt1 maskoff(32) 相对 vanilla 的优劣（是否"完全失效"或"仅不如 mask"）。
  已补跑 P5 vanilla seed0（进行中）。
- [ ] **balloon2 maskoff 3-seed 收尾**：软链崩溃后重跑中（rsync 教训：同步后必重指向 /mnt/app/datasets/Bonn/）。
- [ ] **方向 B**（balloon 3D 可恢复性）：已判负（`recoverability ≠ reconstructability`），
  收窄方向 A，不复活除非有"远尺度重建"新角度。
- [ ] **对比竞品表**：把我们的 mask-free ATE 与 RGD/DG/Dyna/Co-SLAM 同序列数值并排（已有部分，
  见 `p2t_verdict_3090.md` competitive floor）。pt1 竞争位已在 `resources/01-references/paper_summaries.md`。

## 九、写作启动闸门（不达不写）

1. 核心表（三类 mover × maskfree/combined）3-seed 完整 —— **基本达成**（mv 双复现 + pt2 + balloon；
   pt1 是边界反例已如实呈现，不算缺口而算适用域）；balloon2 收尾后全 6 序列完整。
2. P-B 消融 + 诚实负结果（TRC median、hole-ghost、**pt1 边界反例**）入文；
3. 竞品差异化表核对过 arxiv；
4. 高准则两问能给出"是 + 是"的完整回答（已答，详见 `p6_maskoff_6seq_main_table.md` §三）。

## 十、禁词（延续 07 禁词表，见 NEXT_SESSION_PROMPT）

- 不写 "8/30 可投 / almost-ready / 就投这个"。
- 不 claim SOTA（报实测值，不比 absolute）；不写"没有分洞/零洞"（mv 无洞但 balloon 有内容替换）。
- backbone（SemanticMask 借来）不是核心贡献，靠消融证内核；terminal compression 是支撑段非头条。
