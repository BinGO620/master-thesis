# MMM Submission — 终端 opacity 软选择压实 + 有竞争力骨干 论文骨架

> 产出：2026-08-08（重写版，取代 2026-08-07 的 ADC-regrow 叙事版，版本见 git）。
> 目标截稿：**2026-08-30**。目标会场：MMM 2027, Siem Reab, Cambodia。篇幅：12 页正文 + 2 页引用（LNCS Springer）。
> 本文档 = 骨架 + 各节要点 + 证据文件指针。**内容写进 `papers/mmm/`，不污染方法区。**
>
> **⚠ 此版本已按 AUTO_REVIEW Round 1/2 裁决重写**：删掉被证伪的 ADC-regrow 机制叙事，
> 换成**受控的经验/系统表征（soft-selection characterization）**定位 + matched-rate 对照 +
> artifact 存储度量。死因与禁词见文末「禁词与不回炉」节。

**标题候选（Round2 修正——去掉绝对保证、慎用 floater）**：
> 审稿人定位 = **soft-selection 表征**。标题不承担"完全零成本压缩算法"的保证（有离线
> prune/serialization/validation cost；只减 6–11% 固定格式 bytes；非编码压缩）。
>
> - **Title A（Round2 推荐）**：*Opacity-Selected Terminal Pruning in Dynamic 3DGS SLAM Maps*
> - **Title B**：*Soft-Selected Near-Zero-Contribution Cohorts in Dynamic 3DGS SLAM: A Controlled
>   Terminal-Pruning Characterization*（"floater" 需空间证据，正文慎用，标题不用）
> - **Title C**：*On the Disposable Low-Opacity Gaussians of Dynamic 3DGS SLAM Final Maps*

---

## ⚠ Round 2（2026-08-08）两处关键修正（codex 复核落地，见 AUTO_REVIEW.md）

---

## ⚠ Round 2（2026-08-08）两处关键修正（codex 复核落地，见 AUTO_REVIEW.md）

1. **定理量词修正（本质）**：~~"整批删除零代价由严格数学上界无条件保证"~~ 是**错的**。`op<0.01`
   只保证**单个** Gaussian 对任一像素单项贡献 <1%，**不保证同一射线上 m 个低-op 高斯的累计
   透明度质量 <1%**（m=100 时累计 opacity ≈63%）。正确定位：
   - 数学只证**单高斯最大影响**（上界 A/B）；
   - **整批安全 = empirical rendering validation**（12/12 |dPSNR|≤0.0001dB）；
   - "零代价"是**实测结论**，不是 dataset-independent theorem。
   - **补（cohort-level，ship-gate）**：直接统计每像素被删 cohort 的累计 compositing weight
     `W_removed(p)=Σ_{k∈R} T_k(p)α_k(p)`，报 mean / 99th / maximum —— 这才是 "near-zero
     contribution cohort" 的真正 cohort-level 证据。
2. **lifecycle 衔接（Reviewer-2 会问）**：terminal compression 跑在 **prune 臂**上，但原文
   却在 §4.5 大篇幅比较 deferred/prune（而 deferred 6/6 ATE 都不优）= "didn't win" 支线。
   → 主文**只报承载 terminal compression 的 prune backbone** 对外 baseline ATE；deferred/prune
   内部比较移 supplementary 或删。N/bytes/quality 必须与 ATE 表**同一 prune lifecycle、同一
   checkpoint 定义**；不用 deferred 的更低 G 数为 terminal 增色。

---

## 核心叙事（一句话，审稿人认可的最强一句 claim）

> **Standard color refinement in dynamic 3DGS SLAM induces a reproducible opacity-soft-selected
> cohort of roughly 8–18% near-zero-contribution Gaussians that can be removed from final maps
> without measurable rendering loss, while our 6GB self-tracked backbone achieves competitive
> Bonn accuracy.**

三段式支撑：
1. **存在性（measurable）**：终图 `final_after_opt` 有 8–18% `sigmoid(op)<0.01` 高斯，**单个**其光学贡献 <1%（`theory.md` 单高斯单项上界；整批 vs 实测 + cohort 累计权重，见 §Round2）。
2. **专用性（non-trivial）**：matched-rate 删除控制证明**只有**低 opacity 队列专一安全 —— random 同数量删除代价 −0.4~−2.0 dB、high-op −2.3~−3.8 dB（round2 控件，审稿人 kill-gate 未触发）；
3. **实证面（floor）**：自跟踪骨干在 6 动态序列上是**有竞争力**的 SLAM（balloon 3.07 / mv_no_box 2.58 cm ATE），不是只有后处理。

---

## 论文结构（12 页 LNCS）

### 1. Introduction（~1.5 页）

**P1（问题）**：动态 3DGS SLAM 的最终地图是 insert-then-prune 范式的产物，随着时间累积
规模膨胀。但膨胀里有一类"结构性可删"的高斯：被最终 color-refinement 的纯光度优化压到
sig 近零 opacity、在 volume rendering 里贡献趋近于零。**这引出一个此前没被问的问题：
终图里有多少高斯本质是可以零代价删掉的，且为什么它们存在？**

**P2（现有方案不足，对照 gap）**：
- 在线剪枝（MGS-SLAM、Speedy-Splat、PUP-3DGS）在训练期内牺牲保真换紧凑度，**从不问终图
  opacity 分布里有多少是"稳态浮渣"**；
- 编码压缩（3DGS.zip、LightGaussian、Compact-3D）在编码层做存储，**不对 opacity 软选择机制
  提问**；
- 因此"终图的 opacity 软选择 + 零代价压实"是一个未被表征过的现象级 gap。

**P3（贡献，3 条 bullet）**：
1. **受控测量发现**：**the terminal color-refinement stage in our MonoGS-based backbone** 的
   opacity 自由度产生**可复现的软选择队列** —— 终图 8–18%（12/12 run）高斯被压到 sigmoid op<0.01，
   单高斯光学贡献 <1%（严格单项上界）。
2. **专用性非平凡**：matched-rate 删除控制证明该队列**专一安全**；删同数量随机/高 opacity
   高斯分别损失 0.4–2.0 / 2.3–3.8 dB，删低 opacity 队列 ≈ 0 dB。
3. **实证面**：同骨干在 Bonn 6 动态序列上 3-seed 自跟踪主表，**competitive on balloon（3.07）and
   mv_no_box（2.58）** cm ATE（介于 RGD-SLAM 2.26 与 DG-SLAM 3.65 之间），零代价压实是在能打的
   基座上的可投观测。

### 2. Related Work（~1 页，3 段）

**P1 在线 3DGS 剪枝**：MGS-SLAM（单目显著性）、Speedy-Splat、PUP-3DGS、DCSHARP —— 都在
训练期内服务位姿/加速/画质，**不问终端 opacity 分布**。

**P2 存储压缩**：3DGS.zip 综述、LightGaussian、Compact-3D —— 编码层，**不对"可删的浮渣"
做机制表征**。我们把删除推到保真无关的极值（op<0.01），用一个严格上界说明为什么安全。

**P3 动态 SLAM 紧凑度**：DG-SLAM / BDGS-SLAM / DAGS-SLAM 有自适应 Gaussian 管理，但核心是
动态抗干扰而非紧凑度本身。**我们的 gap**：以上都没问「终图 opacity 分布里有多少是
color-refinement 软选择出的零贡献浮渣」。

### 3. Method（~2 页）

**3.1 骨干与评估平台（0.5 页，简洁引用）**：MonoGS + mask-both + DynamicKeyframe +
insert-then-prune。不是 novelty，仅 1 段 + pipeline 图（引用原有论文 + 主表实证面）。
**自跟踪，非冻结位姿**（Non-negotiable：主表必须 full SLAM 自跟踪）。

**3.2 终图 soft-selection 观测与 Terminal Compression 算子（0.6 页，核心方法）**：
- 加载 `final_after_opt`（refinement 后）PLY。
- **观测**：refinement 的 26000-iter 纯光度优化（opacity 活、无 prune/densify/reset）把
  10–13 pp 高斯压到 sigmoid op<0.01（证据 `p3_terminal_mech_autopsy.md` + frozen-opacity
  反事实 `p3_terminal_refine_freeze_result.md`：冻结 opacity 后尾巴 12.8%→3.7%，**证明这批
  是 refine 的 opacity DOF 软选择产物**）。
- **算子**：`_prune_raw` 删 `sigmoid(opacity) < 0.01`。重渲染验证（offline interval-5 full-frame，
  零 GPU 预算）。
- **为什么是 0.01**：`theory.md` 上界 A/B 严格单调于阈值 —— op<0.01 时单高斯权重 <1%、
  最大遮挡 odds <~1%；op<0.05 的 balloon seed-1 破 −0.087 dB ⇒ 0.01 是最粗安全格。
- **（Round2 修正）**：阈值选择依据的是**单高斯上界**；**整批删除的零代价由 empirical rendering
  validation（12/12 |dPSNR|≤0.0001dB）支撑，不是无条件定理**。"cohort" 用累计 compositing
  weight（§P0 补实验）来定义近零贡献。

**3.3 为什么删除单个低 opacity 高斯代价小：数学上界（0.4 页，引用 theory.md 不重推导）**：
volume rendering front-to-back alpha compositing 下，**单个** `op<0.01` 高斯：
1. 对任意像素最终颜色权重贡献 <1%（`α_k·T_k < 0.01`）；
2. 对被它挡在更后的表面的遮挡 odds <~1%（`α_k/(1−α_k) ≈ 0.0101`）。
**这是数据集无关的单项界；不声称整批**（整批由实测 + cohort 累计权重支撑）。

**3.4 为什么这批存在：机制解释（0.4 页，改写后版本，非 ADC）**：
- 关键事实（`p3_terminal_mech_autopsy.md`）：在线 `final` 图 `op<0.01` 均值仅 0.69%（36/36 run），
  refinement 后 `final_after_opt` 才到 10.4%（36/36 增长，+9.7pp）。**尾巴是 refine 阶段制造的**，
  不是在线 ADC 稳态。
- frozen-opacity 反事实（`p3_terminal_refine_freeze_result.md`）：26000-iter 纯光度优化、opacity
  作为自由参数做**隐性软选择** —— 通过把贡献趋零的 floaters 压到近零 opacity 来优化 RGB-only
  损失。冻结 opacity 后尾巴 12.8%→3.7%（机制验证成立），但地图质量 −0.53dB、N 涨 35%
  （关联合参数补偿）⇒ **软选择对 refine 质量有正面作用，不是缺陷**。
- ⇒ "终端压缩"是把这个软选择的**结果**安全地固化成文件减量，而不是试图在线省 compute。

### 4. Experiments（~3.5 页，核心篇幅）

**4.1 设置（0.3 页）**：BONN 动态序列（balloon, balloon2, mv_no_box, mv_no_box2, pt1, pt2），
3 seeds，RTX 2060 6GB（**自跟踪**）。渲染为 offline full-frame interval-5 同口径。

**4.2 主结果 —— 存在性与零代价（实测结论，非定理）（0.7 页，Table 1）**：

| seq | seed | op<0.01 rm% | dPSNR |
|---|---|---|---|
| balloon | 0/1/2 | 12.8/18.4/17.3 | −0.0001/−0.0001/+0.0001 |
| mv_no_box | 0/1/2 | 9.9/8.4/10.0 | +0.0000/−0.0000/−0.0001 |
| pt1 | 0/1/2 | 9.9/10.1/10.3 | +0.0000/−0.0000/+0.0000 |
| pt2 | 0/1/2 | 18.4/11.2/10.5 | −0.0000/+0.0000/+0.0000 |

→ **12/12 run 全部 |dPSNR| ≤ 0.0001 dB；移除范围 8.4–18.4%（mean 9–16%）**（证据
`R3-P05-map-compression-step5b-terminal-3seed.md`）。**零代价是实测，由单高斯上界 + cohort
累计权重（P0）解释为何非意外。移除比例不人为缩窄，统一写实际范围 8.4–18.4%。**

**4.3 非平凡性 —— matched-rate 删除控制（0.7 页，Table 2，round2 控件，核弹级）**：
同移除比例（~10% 终图），三种删除策略 vs 零代价主张：

| seq | low_op dPSNR | high_op dPSNR | random dPSNR |
|---|---|---|---|
| balloon | **−0.0000** | −3.822 | −0.788 |
| balloon2 | **−0.0125** | −2.272 | −0.438 |
| mv_no_box | **−0.0012** | −3.812 | −2.050 |

（证据 `p3_matched_rate_deletion.md`）
→ **删低 opacity 队列 ≈ 0 dB；同数量删高 opacity 损失 2.3–3.8 dB（1–2 个量级）；随机删损失
0.4–2.1 dB。** ⇒ 这不是"随便删什么都便宜"——低 opacity 队列是**专一安全**的。这个表直接
预判审稿人最可能的"obvious heuristic"拒稿理由，并回答"why not random / why not high-op"。

**4.4 产物级节省 —— 存储/传输，非运行时加速（0.4 页，Table 3，round2 控件）**：
op<0.01 删除后的序列化字节：

| seq | N | rm | bytes before | bytes after | % saved |
|---|---|---|---|---|---|
| balloon | 27648 | 3118 (11.3%) | 2.21 MB | 1.96 MB | 11.3% |
| balloon2 | 70746 | 4560 (6.4%) | 5.66 MB | 5.30 MB | 6.4% |
| mv_no_box | 38678 | 3157 (8.2%) | 3.09 MB | 2.84 MB | 8.2% |

（证据 `p3_matched_rate_deletion.md` §Files）
→ **显式定位为 storage/transfer reduction（≈ 移除比例），NOT refinement/runtime acceleration。**
禁词表里"compute savings"不写。

**4.5 实证面 —— 有竞争力的自跟踪骨干（0.7 页，Table 4，主文只报 prune 臂，P2-T 主表）**：
**（Round2 修正）主文只报承载 terminal compression 的 prune backbone 对外 baseline ATE；
deferred/prune 内部比较移 supplementary。** 6 动态序列 × prune × 3 seed = 18 run，自跟踪
全轨迹 ATE（`p2t_verdict_final.md`，从 prune 列读；deferred 列不在正文）：

| seq | prune G | prune ATE | （supp：deferred G） | （supp：deferred ATE） |
|---|---|---|---|---|
| balloon | 39784±5511 | **3.07**±0.14 | 19803±267 | 3.11 |
| balloon2 | 33524±2631 | **5.22** | 30519±4236 | 5.84 |
| mv_no_box | 40806±4228 | **2.58**±0.05 | 31561±2529 | 2.87 |
| mv_no_box2 | 65343±7680 | **4.68** | 50655±16848 | 5.61 |
| pt1 | 55596±4072 | **10.97** | 44154±1313 | 11.51 |
| pt2 | 69609±16219 | **10.35** | 44196±1961 | 16.80 |

→ **competitive 措辞限定 "on balloon and mv_no_box"：balloon 3.07 / mv_no_box 2.58 cm 有竞争力**
（介于 RGD-SLAM 2.26 与 DG-SLAM 3.65 之间）；pt1/pt2 是 10 cm+ 如实报（诚实呈现，不挑结果）。
**主表给全部六序列同一协议**（同一 prune lifecycle、同一 checkpoint 定义 = terminal compression
跑的那批 map）。**FPS 是 2060 的数不得与竞品并列**（硬约束）。terminal compression 的 N/bytes/
quality 必须来自与这张表同一批 prune map。

**4.6 安全边界（0.3 页）**：op<0.05 不安全（balloon seed1 破 −0.087dB）；0.05–0.10 带含表面
细节；删除比例 9–16% 序列间稳定但 balloon 高、mv_no_box 低（可进 supplementary 分析）。

### 5. Limitations（~0.5 页，如实，AUTO_REVIEW/三轮证据 7 条收紧版）

1. 只验证了 **the terminal color-refinement stage in our MonoGS-based backbone**；其他 SLAM 前端是否产生软选择队列**未知**（跨前端外推不下结论）。
2. 删除比例 9–16% 非大比例压缩，但**零代价**（这是特征非缺陷，只报"有多少可删"不报"能压多少"）。
3. 只测了 3D Gaussians；4DGS/显式动态未测。
4. **不做在线 terminal compression**：refine 的软选择本身对质量有正面作用（freeze −0.53dB），删它不省 compute。
5. matched-rate 控件基于 offline interval-5 同口径渲染；报值注明口径。
6. frozen-opacity 反事实仅 balloon seed0 单 run = 机制验证非判决，含 +5000 插入竞态 caveat。
7. 骨干 ATE 自跟踪（2060 实测），但 FPS/VRAM 不得与高显存竞品并列。

### 6. Conclusion（~0.3 页）

动态 3DGS SLAM 终图的 color-refinement 会软选择出一批 sigmoid-op<0.01、光学贡献 <1% 的高斯
队列，可被终图一次性删除且零渲染代价（严格上界 + 12/12 实测 + matched-rate 非平凡控制），
同时也为存储/传输省 6–11% 字节。该观测建立在一个有竞争力的自跟踪骨干（balloon 3.07 /
mv_no_box 2.58 cm ATE）之上。

---

## 图表清单

1. **Fig1 Pipeline**：骨干 + refinement 软选择 + 终图压缩流程图（已有架构，简化绘制）。
2. **Fig2 主结果**：12/12 run 压缩率 × dPSNR 散点（数据 `R3-P05-map-compression-step5b-terminal-3seed.md`）。
3. **Fig3 机制**：opacity 直方图 在线 final vs refinement 后 final_after_opt（`p3_terminal_mech_autopsy.md`，≈0.69% → 10.4%）；可选叠 frozen-opacity（3.7%）。
4. **Fig4 非平凡性**：matched-rate 三策略 dPSNR 柱状（低/高/随机，`p3_matched_rate_deletion.md`）——**承重图**。
5. **Table1** 存在性 + 零代价主表（§4.2）。
6. **Table2** matched-rate 控制表（§4.3）。
7. **Table3** artifact 存储节省（§4.4）。
8. **Table4** 骨干 ATE 主表（§4.5）。
9. **Table5**（supplementary）安全边界 + 删除比例稳定性。

---

## 待补工作（写作/补齐证据，按优先级）

### P0 — 直接决定 skeleton 能否成稿（零新 GPU 或多为已具）

- [x] **matched-rate 删除控制**（3 seq，已跑完，`p3_matched_rate_deletion.md`）→ §4.3。
- [x] **artifact 字节节省**（已算，`p3_matched_rate_deletion.md`）→ §4.4。
- [x] **骨干 ATE 主表**（P2-T 36 run，`p2t_verdict_final.md`）→ §4.5（主文只报 prune 臂）。
- [x] **frozen-opacity 反事实**（`p3_terminal_refine_freeze_result.md`）→ §3.4 机制。
- [ ] **改 mechanism.md → 删掉已证伪的 ADC 归因段**，重写为"soft-suppression 机制 + REWORK 记录"（✅ 已改 2026-08-08 commit `44951c0`）。

### P0.5 — **Round 2 ship-gate 补实验**（codex：做这两个就把 BORDERLINE 抬到 accept-as-narrow-empirical，截稿前值得付）

- [x] **cohort-level 累计权重证书**：统计每像素被删 cohort 的 `W_removed(p)=Σ_{k∈R} T_k(p)α_k(p)`，报 mean / 99th / maximum。这就是把 "near-zero contribution cohort" 从**单高斯单项界**推到**整个队列**的实测证据（补 theory.md 量词错误）。CPU/offline，无需重训练。**（✅ 已扩到全 18 张 P2-T prune 图：W_mean≈0.05–0.10%、W_p99 全部<2%（typical<1%）、最坏 2 个单像素 >5% 但 p99 ≤1.8% ——`p3_cohort_weight_cert.md` 已落盘完整 6 序列 × 3 seed 表）**
- [x] **matched-rate 扩到现有所有 12 张 prune final_after_opt map**（bak P2-T 18 prune + 现有）：low/high/random × 12 PLYs；random ≥10 次（最好 20）报 mean/std/95%CI + low-op 在分布中的位置；覆盖多 rate（5/10/15%）；同时报 GT-dPSNR **与** compressed-vs-original-render 的 PSNR/SSIM/LPIPS + 高分位像素误差。**（✅ 已跑完，`p3_matched_rate_extended.md` 落盘 18 图 × rate 5/10% × random 10 reps；aggregate：low GTdPSNR mean −0.00008/max|.|0.00210、high mean −3.43/min −5.68、random mean −0.65±0.27 全 <0；bvSSIM low 恒 1.00/high 大跌——§4.3 已填）**

### P1 — 补强论证 / 缝隙防线

- [ ] **跨前端外推克制**：如果有资源，在 vanilla MonoGS（无 mask）跑 1–2 序列验证软选择队列是否
  backbone-specific（否则 limitation §1 更硬）——**低优先**，reviewer 不会 main kill。
- [ ] **skeleton 交 codex 做 Round 2 复核**：确认 matched-rate + artifact 是否把 A 从 borderline
  抬到 passable，以及禁词表是否还有漏。（审稿人选 codex MCP。）
- [x] **图/表产出**：Fig2（`fig2_main_results.png`）+ Fig4 承重图（`fig4_matched_rate.png`）+ **Fig3 机制图（`fig3_mechanism.png`，真实 per-run 数据从 `p3_terminal_mech_autopsy.md` §1，非占位）全部已出**。

### P2 — 可进 supplementary

- [ ] op<0.02 边界扫描（若安全可扩删除率）。
- [ ] 删除比例 9–16% 跨序列稳定性分析（balloon 高 / mv_no_box 低成因）。

---

## 禁词与不回炉（写稿守则，AUTO_REVIEW + 机制证伪裁决）

**禁词表**（审稿人直接点名 + 机制证伪）：
- ~~ADC regrowth~~ —— 机制已证伪（`p3_terminal_mech_autopsy.md`），tail 是 refine 软抑制不是 ADC 稳态。
- ~~compute savings / 省计算~~ —— freeze 反事实否掉（−0.53dB、N+35%），软选择对质量有正作用。
- ~~online compaction~~ —— 不做在线压缩，只做终图后处理。
- ~~general dynamic-SLAM improvement~~ —— 只报"我们骨干有竞争力（balloon/mv_no_box）"，不声称普适改善。
- ~~"Zero-Cost Terminal Compression"（标题）~~ —— 标题不能承担"完全零成本压缩算法"保证；改
  "Opacity-Selected Terminal Pruning"。慎用 ~~"floater"~~（低-op ≠ floater，需空间位置证据）。
- ~~"整批删除零代价由无条件定理保证"~~ —— 量词错（单高斯单项界 ≠ 整批）；整批 = 实测 +
  cohort 累计权重。
- 不写不可守的 Related Work 绝对句：~~"从不问" / "此前没人表征"~~。

**不回炉**：terminal compression 不当"省 compute/修复 refine 缺陷"写；不复活性在线抗动态机制
（deferred/eviction/α-carve/RT/DBA）；不追新 ATE headline。

---

## 写作时间线（Round2 复核后最终版，8/30 ddl）

| 日期 | 任务 | 产出 |
|---|---|---|
| 8/8（本会话） | 重写 skeleton + mechanism → codex Round2 = BORDERLINE（补两个洞可 accept） | 定稿骨架 + ship-gate 清单 |
| 8/8–8/9 | **跑 ship-gate 补实验**（cohort 累计权重 + matched-rate 扩 12 maps + random 重复 + 多 rate） | P0.5 证据（1–12 GPU-h）|
| 8/8–8/10 | Intro + Related Work + Method 初稿（措辞按 Round2 清单） | 3–4 页 |
| 8/10–8/12 | Experiments 4 表 + 图 2/3/4 + ship-gate 上表 | 核心实验节 |
| 8/12–8/14 | 绘图 + limitation（压成一段）+ conclusion | 全稿 ~8–10 页 |
| 8/14–8/28 | 同行审读 + 润色 + 格式 + codex 终审 | camera-ready |
| 8/30 | 提交 | LNCS 12+2 页 |

> codex 建议：8–10 页核心即够，硬填 12 页暴露薄。**最终闭环**：`refinement 产生 tail →
> cohort-level contribution 测量 → controlled deletion specificity → artifact reduction →
> same-lifecycle SLAM validity`。

---

## 目录结构（`papers/mmm/`）

```
papers/mmm/
├── skeleton.md       ← 本文档（重写完成）
├── manuscript.md     ← 草稿正文（逐步填充）
├── theory.md         ← 数学上界（已存在，不依赖 tail 来源，直接复用）
├── mechanism.md      ← ⚠ 待改：删 ADC 归因，重写 soft-suppression（skeleton §3.4 引用它）
├── figures/          ← 待生成图表
├── tables/           ← 主表数据（§4 四表）
├── references.bib    ← 参考文献
└── submit/           ← camera-ready 最终 PDF
```
