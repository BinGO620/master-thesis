# camera-ready 修改记录（进行中）

基线：`../paper/`（投稿版，与 git tag `mmm2027-submission` 逐字节一致）
工作副本：本目录
状态：**内容修改基本完成，尚未做页数压缩到 12 页正文**

## 已改（对应审稿意见）

### A 组 · 方法定义（R1-2、R4-1）

- **修正 L1/L2 事实错误**（3.3）。原文说"replaces the L2 tracking residual"，
  实际代码是 L1 光度 + 几何残差（`slam_backend.py` 用 `l1_loss`，`l2_loss` 全仓库无调用）。
  改为"保留 L1 目标、在其上叠加 IRLS 权重"。
- **补权重作用层级**（3.3）。明确权重乘在逐像素残差上、再按权重和归一化，
  给出完整式子 $L=\alpha\frac{\sum w_{rgb}v|I-\hat I|}{\sum w_{rgb}}+(1-\alpha)\frac{\sum w_d|D-\hat D|}{\sum w_d}$，
  并说明等权时退化为原损失。审稿人 R1 明确问的就是这一层。
- **补 e_flow 完整归一化式**（3.4）。$a=\|f_{obs}-f_{static}\|_2$，
  $e_{flow}=1-\exp(-\tilde a/(\sigma+\varepsilon))$，$\sigma=\max(1.4826 MAD, 2.0\text{px})$，
  并说明 2.0 px 是在静态序列上标定的 $a$ 的噪声底，非有限流动的像素被排除而不是记 0。
- **补几何线索 g 的定义**（3.4）。同一归一化器作用于轴向深度残差 $r_d=|D-\hat D|$。
- **补生命周期证据规则**（3.5）。一个视角如何产生 support / contradiction / occluded：
  $\tau_d=\max(0.03,0.02\hat z)$、$\delta=z-\hat z$、颜色差阈值 0.15、
  $C^+=\sum s h$ 与 $C^-=\sum s$、$h=\mathrm{clip}(1-|\delta|/\tau_d,0,1)$、promote/reject/expire 判据。
- **补 warm-up 与刚性流位姿来源**（3.4）。用的是 tracker 自己在 warm-up 后的位姿估计，
  不是参考位姿也不是真值。
- **补 3.6 变更清单漏项**（R4-2）。"simpler → combined" 是四个开关不是三个，
  补上 warm-up 期间的硬跟踪掩码。

### B 组 · 证据包（R1-1、R4-3）

- **正文加指路句**（Protocol 末）。说明预注册记录、各臂配置、8 格 factorial 的逐 seed ATE
  与完成状态、cue 拆分 factorial、RPE held-out 逐 run、完整 18 序列表随源码包在 `evidence/` 下。
- 材料本身都在仓库里，尚未整理成 `evidence/` 目录（待办）。

### C 组 · 对照归因（R1-3、R4-2）

- **补三臂等价设置**（5.4）。keyframe 规则、robust kernel 与 δ、生命周期、优化预算
  三臂相同，差异只在流如何进入残差。
- **明确没做更强的对照**（5.4）。保留同样归一化分数、只变硬/软的那条对照没跑，
  如实写出并把归因留在开放状态。

### D 组 · 成本与失败案例（R2-4、R3-1、R3-2、R3-3）

- **RAFT 端到端成本**（5.7）。加回 54 ms/帧后端到端接近 0.6 FPS，
  并声明没测过换轻量光流估计器，0.75 FPS 是在线阶段速率不是部署速率。
- **静态退化根因**（Limitations 3）。不是"噪声"，是机制自身的闭环：
  刚性流用正在被优化的位姿预测，其位姿误差就是流残差，$\delta t$ 在 0.8 m 处诱发
  $f_x\delta t/z$ 像素，5 mm 就 3.3 px，超过 2.0 px 底。数据上体现为
  $e_{flow}$ 与深度的相关性从 GT 位姿下 $+0.11$ 翻到扰动下 $-0.58$，
  即近景被系统性判成动态，形成跨帧正反馈。在环 oracle（只把 GT 相对位姿喂给刚性流预测、
  跟踪照常优化）把 `f3_st_hf` 从 35.3 恢复到 2.85 cm，坐实因果并给出任何修法的上界。
- **4/18 失败序列特征**（Limitations 1）。四条都是 sitting 或近静态、无持续移动体；
  `f3_st_hf` 的区别是近景平移，放大 $1/z$ 项；不是遮挡或纹理模式的问题。

### E 组 · 定位（R2-1、R3-4）

- **说清与既有一致性方法的区别**（2.3）。本方法的决定是连续的：
  有界权重、最多衰减 10 倍、从不移除，且同一信号还加权生命周期。
- **跨骨架可移植性**（Limitations 5）。机制只依赖渲染深度与不透明度、观测深度、位姿、
  以及位姿求解里能施加逐像素权重的位置，任何稠密 RGB-D 高斯 SLAM 都具备；
  不能直接搬的是标定（MAD 与噪声底依赖具体骨架的残差统计）。

### 自包含性（用户要求）

- 删掉正文里唯一的 `SI S9` 指针，论文不再引用任何补充材料。
  MMM 两轮通知都没提补充材料通道，正文必须自洽。

## 压缩与收口（2026-10-23，压完 14 页）

压缩执行（15 → 14 页 = 12 正文 + 2 参考文献）：

- **删 5.4 尾部自陈句**（"we have not run it, and leave that attribution open"）。
  按用户「不自爆」裁定处理：对照本身没跑，正文如实边界句保留（"rules out the
  information alone and not every flow-consuming treatment"），删的只是主动认领句。
  未伪造任何对照结果。
- **删摘要与引言两处 "claim no state-of-the-art accuracy"**（DISCIPLINE「禁自爆式
  言论」）。
- **删题注与正文的重复**（小论文三原则③）：图 4/5/6 题注的"Numbers are in the text
  below / Readings are in Secs / Values in Sec"指路句；图 1 题注里 "(combined only,
  never routed through L)" 与 3.1 正文重复。
- **删与图题/节内重复的复述**：5.1 "and the readings are these"、5.3 "These cells are
  attribution-campaign anchors"、5.2 "Two further results belong beside these marginals"、
  引言 P2 "Two kinds of evidence are missing" 三句式、结论首段与前文重复的收束句。
- **正文句式收紧不丢数字**：Limitations 1/4/5、5.2 判据段、5.3 drift 括号、5.7 FPS
  段、3.4 MAD 释义、3.5 生命周期尾、引言 P1 链式小句合并。
- **冒号削 29 → 17 处**（soft target <40/10k，现 39.1/10k）。
- **图 4/5/6 宽度各收 4-7%** 省垂直空间。
- 全部 30 个关键数字（ATE、比例、阈值、相关性、run 数）逐个 grep 验证存活；
  6 图 1 表齐全；`style_tells.py` AI 短语为空、em dash 6.9/10k、句长 CV 0.796。

同时完成：

- 去掉 `runningheads`（`\documentclass[a4paper]{llncs}`），官方不加页眉页码。
- 实名三作者 Bin Chen / Jie Su / Jing Zhang，两单位 + 三个邮箱，
  `authorrunning = Bin Chen et al.`（`02_resources/论文作者以及其他信息.md` 为准）。
  **ORCID 未填**（用户没给，绝不编造），如需自行补 `\orcidlink{...}`。
- 摘要 `39--147` 与正文 `39.3/147.5` 口径统一为约数。
- `build.sh` 加 `--keep-intermediates`，`build/main.bbl` 已生成（源码包要求）。

## 待办

1. ✅ 压到 12 页正文 + 2 页参考文献（14 页，2026-10-23 完成）。
2. ✅ 去掉 `runningheads`。
3. ✅ 换实名与单位（ORCID 待用户给）。
4. 补致谢与基金信息（官方要求，需用户提供基金号）。
5. ✅ `build.sh` 保留 `.bbl`。
6. 把证据材料整理成 `evidence/` 目录随 zip 提交。
7. hard-vs-soft 对照实验：**用户裁定不跑**（服务器故障 + 截止紧张），正文已如实收口。

## 图 1/2/3 重排（2026-10-24）

用户反馈「图一和图二线条很拥挤还没有对齐」。定位到根因后重做了三张图，
数据与拓扑一个没动，只改布局。

**根因**：旧图都按 12.2 cm 画，正文却按 `0.73/0.76/0.68\textwidth` 缩放排入，
7 pt 的标签实际印成 5.1/5.3/4.8 pt。拥挤的主因就是这层缩放。

- **图 1（pipeline）** `make_fig1_pipeline_v6.py`：改按 1:1 排满版心
  （`width=\textwidth`，画布 12.2×3.14 cm）。每个框宽度由自身标签用 TextPath
  实测决定；R/K/D 三条组件框同基线同高，蓝箭头从框心垂直升入对应骨干框中心
  （旧图 D 框更高更靠上、箭头偏离中心）；可选掩码改从**上方**接入——一条虚线
  主干走在 K 与 D 之间，上方一条虚线总线，三条短 stub 落到消费者顶边并偏开蓝
  箭头，不再与组件箭头共走廊；L 的 site 2 从 L 右侧出、沿底边走到 D 下方上升。
- **图 2（reliability 流程）** `make_v5_fig2_reliability.py`：几何线索 g 从前
  版那条横贯全图的虚线改为 s 上方的一个独立输入框，只留一段竖直短箭头；所有
  边改为正交，消除了三处斜箭头的交叉；两个消费点并排在 s 下方，各走一段自己
  的短竖直箭头。
- **图 3（地图对比）** `make_fig3_map_comparison_v5.py`：从 3 列两行改成单行
  五格。满宽下双行网格要 6.5 cm 高，会把正文顶到 15 页；单行只要 2.57 cm，
  每格 2.27 cm，与旧版缩放后的 2.6 cm 相当。两行变一行后，面板、间距、标签条
  天然在同一基线上。题注的 "Top/Bottom" 相应改为 "The first two panels / The
  last three"。
- 图 4/6 放到满宽、图 5 放到 0.72（0.76 会跳 15 页）；`\enlargethispage`
  从 4 行减到 3 行。最后仍是 **14 页**（12 正文 + 2 参考文献）。

**过程中的两个失误，已修正**：
1. 误把图 2 认成 fig3 那组渲染对比图，一度覆盖了正式 fig2。从
   `deliverable/` 完整恢复（md5 已核对，与 `source_zip/` 一致）。
2. `paper_rev1_camera_ready/` 下残留了一份旧 fig2 副本，而 xeCJK/XeTeX 先在
   当前目录找图，`\graphicspath` 只作后备，导致改图后编出来的仍是旧图。已删除
   该目录下的图片副本，图片唯一真身是 `../figures/`。

**验证**：源码包解压到干净目录重编，14 页，`pdftotext` md5
`c37f6a14b576262459d4fe22d63531bf`，与工作区编译逐字节一致；30 个关键数字
全部 grep 存活。

## 自洽性修复 + 字号达标（2026-10-25）

### 1. 删掉正文指向源码包的句子（用户指出的重大错误）

4.1 节末尾原有一句，把预注册记录、各臂配置、factorial 逐 seed 结果等六样东西
指到源码包的 `evidence/` 目录，并说「so each number in Secs. 4--5 can be traced
to a run」。

**这是设计错误**：主论文必须自洽，不能依赖发表后读者拿不到的外部文件。审稿流程
结束后没人有源码包。整句删除，连同前面半句 "each reported cell maps to exactly
one run directory" 一并去掉。

同类的三处一并清理：

- 3.1 "Constants are resolved from the run configuration" → "Every constant is
  given where it is introduced"
- 3.6 "All sixteen constants ... are resolved from the run configuration" →
  "... are stated in Secs. 3.3--3.6"
- 3.3 "the two other kernels the codebase implements" → "... we implemented"
- 5.3 "drift discipline" → "batch-to-batch drift we budget"；"same-campaign cells"
  → "same-batch cells"；"the 18-sequence campaign is canonical" → "... is the one
  we report throughout"

核验：正文扫 `evidence/`、`source archive`、`supplementary`、`run directory`，
命中 0。

### 2. 三处数字按证据表改正

随源码包发的 `table1_18seq_ate.csv` 与正文对不上，审稿人一比对就能看出来。

| 位置 | 原 | 改 |
|---|---|---|
| 5.3 mv_no_box 分母 | 2.65±0.12 | 2.66±0.12 |
| Lim.1 pt1 mask-free sd | 32.41±8.52 | 32.41±8.51 |
| Lim.2 pt2 combined | 10.45 | 10.44 |

### 3. 图内文字全部 ≥ 6 pt

Springer camera-ready 说明要求图内字母不小于 6 pt。v4 实测不达标：图 5 最小
4.3 pt，图 2 4.6，图 1 4.9，图 6 5.5，图 3 5.7。

根因两层：

- 图 3 的 ghost 标注直接写了 `fontsize=5.8`
- 图 5/6 按 12.2 cm 画布作画，正文按 0.72 / 0.95 倍排入，缩放把字号一起压小

修法：**按最终印刷宽度作画**。图 5 画布改为 `TEXTWIDTH * 0.72`，图内字号按这个
尺度重定；图 3/4/6 直接提字号。图 1/2 的公式下标也要达标，把 L 框提到 8.8 pt、
图 2 各框提到 8.6 pt，并相应加高框体避免文字撑破框线。

修字号时暴露的三个排版缺陷，一并修掉：

- 图 5 (b) 图例在收窄画布后被裁切 → 恢复原画布宽度，字号反向放大 1/0.739
- 图 1 的 L 框两行文字纵向撑破框线 → 框高 0.60 → 0.95 cm
- 图 2 的 disagreement 框撑破、e_flow 框被压 → 计算行框高 0.72 → 0.86 cm

核验：六张图逐张用 PyMuPDF 量实际印出的字号，低于 6 pt 的 span 数 = **0**；
页数仍为 14。

### 4. 顺带修的可复现性问题

图 4/5/6 的生成脚本原先只存在于归档 zip 里，`figure_src/scripts/` 下没有。
已取回放入 `figure_src/scripts/`（`make_v4_fig3_ablation.py`、
`make_v4_fig4_controlled.py`、`make_v4_fig5_endpoints.py`）。

图 5 的数据源目录 `results/runs_remote_cache/` 已从工作树删除，脚本会直接崩。
把 36 个 run 的逐 seed ATE 转录进脚本并加注释说明来源；数值经与 2026-09-01 的
results 归档包逐条核对，与已发表图一致。

### 验证

- `pdftotext` md5 `740b66eb9d66d02ef0bcb70b70ea1984`
- 源码 zip 解压干净目录重编：14 页，同一 md5
- 风格检查：破折号 7.0/10k、句长 CV 0.799、AI 高频短语 0
