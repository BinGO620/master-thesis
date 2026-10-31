# Auto Review Log — Narrow Main Line (terminal compression + backbone ATE)

> 目标：审「窄主线能否写成能过 CCF-C 的 MMM 稿 + 死清单是否漏方向」。
> 审稿人：codex MCP。REVIEWER_MODEL=gpt-5.6-sol。Round1 thread `019fdd53`，Round2 thread `019fdd9a`。
> 立场：brutal，默认认为作品某处坏了。

---

## Round 1 (2026-08-07)

### Verdict
- **A = BORDERLINE, probably reject** as a mechanism paper; viable only as *tightly-scoped empirical/system-characterization* paper.
- 最该防的拒稿理由：intervention 就是"删低于阈值的 Gaussian" → reviewer 会判为 obvious post-processing heuristic；competitive ATE ≠ novelty。

### Recommended claim (reviewer-approved)
> Standard color refinement in dynamic 3DGS SLAM induces a reproducible opacity-soft-selected cohort of roughly 9–16% near-zero-contribution Gaussians that can be removed from final maps without measurable rendering loss, while our 6GB self-tracked backbone achieves competitive Bonn accuracy.

**Forbidden words**：ADC regrowth / compute savings / online compaction / general dynamic-SLAM improvement。

### Highest-ROI experiments (offline, no new GPU campaign)
1. **Matched-rate deletion controls** on ALL existing PLYs：random / high-opacity / low-opacity deletion at the same removal fraction. Only if the low-opacity cohort uniquely preserves PSNR/SSIM/LPIPS is the result non-trivial.
2. **Artifact-level savings**：serialized bytes, load time, rendering time before/after, with confidence intervals — framed explicitly as storage/transfer reduction, NOT refinement or runtime acceleration.

### Allocation decision：Ship the paper if goal = credible narrow empirical MMM. Spend time on controls, resource measurements, comparisons, writing. Do NOT spend 3 weeks finding another mechanism or running large GPU sweeps.

---

## Round 2 (2026-08-08) — 复核重写后 skeleton（matched-rate + artifact 控件落地）

### Verdict: **BORDERLINE，明显上升，当前还不到 accept — 补两个洞即 accept-as-narrow-empirical**

一句话：matched-rate 已证明非 random 无害，artifact bytes 补上效用；但**定理量词错**（单高斯<1% 上界被误写成整批删除无条件保证）+ **backbone lifecycle 衔接未对齐**。

### 两个 ship-gate 洞（补上即 accept）

**洞1（最危险，Reviewer-2 可打穿）**：#0 支柱的"整批删除零代价由严格数学上界保证，不依赖数据集"——量词错。`op<0.01` 只保证**单个** Gaussian 在任一像素单项贡献<1%，不保证**同一条射线上 m 个**低-op 高斯的**累计**透明度质量 <1%（m=100 时累计 opacity ≈63%）。正确表述：
- 数学只证**单高斯最大影响**；整批安全 = **empirical rendering validation**；零代价 = 实测结论，非 dataset-independent theorem。
- **补（便宜且值钱）**：直接统计每像素被删 cohort 的累计 compositing weight `W_removed(p)=Σ_{k∈R} T_k(p)α_k(p)`，报 mean / 99th / maximum —— 这才是真正 "near-zero contribution cohort" 的 cohort-level 证据。

**洞2（衔接问题）**：terminal compression 跑在 **prune 臂**上，但 §4.5 却大篇幅比较 deferred/prune，而 deferred 6/6 ATE 都不优。答复：
- 主文**只报承载 terminal compression 的 prune backbone** 对外 baseline ATE；deferred/prune 内部比较移 supplementary 或删；
- N/bytes/quality 必须与 ATE 表**同一 prune lifecycle、同一 checkpoint 定义**；
- 不用 deferred 的更低 G 数为 terminal methoder 增色。

### Q3 matched-rate 够不够
足以支撑窄表述 "on the 3 evaluated maps, opacity ranking identifies a substantially safer deletion cohort than random/high-op at matched rate"；**不够**支撑 "low-opacity deletion is specifically safe in general"。四个漏洞：
1. random 可能只单次抽样（方差大，尤其 balloon2 −0.438dB）→ 需 random 重复 ≥10（最好 20）+ 置信区间；
2. 只测 3 个 map，主表却有 12 runs → 证据层级不一致；
3. 只测 ~10% 一个 operating point → 需 5/10/15% 多 rate 曲线；
4. dPSNR 不足够：对 GT 的差值可掩盖空间正负抵消 → 须同时报 compressed-vs-original-render 的 PSNR/SSIM/LPIPS + 最大/高分位像素误差。

**最便宜补实验**：对已有 12 个 final_after_opt maps 全部做 matched-rate low/high/random；random 10-20 次报 mean/std/CI + low-op 相对分布位置；报 GT-dPSNR 与 before-vs-after render；覆盖 5/10/15% 多 rate。不重训练，删除+bytes CPU 分钟级；interval-5 离线渲染 ~12 maps × 12 policies ≈ 1-4 GPU-h（三轮 rate ≈ 5-12 GPU-h）。**截稿前值得付**。

### Q4 其他死叙事 / 数字
1. **"competitive backbone"有挑结果嫌疑**：突出 balloon/mv_no_box 但 pt1/pt2 是 10cm+。必须给**全部六序列同一协议**；可写"competitive on balloon and mv_no_box"，不能拿两序列替代整个 Bonn verdict。
2. **数字自相矛盾**：标题 claim 写 9-16% 但表有 18.4%（两处）→ 实际范围 **8.4–18.4%**；artifact 表 6.4–11.3% 与存在性表 8.4–18.4% 来源/seed 不同需解释，否则读者以为不一致。
3. **"Standard color refinement"范围过大** → 改 "the terminal color-refinement stage in our MonoGS-based backbone"。
4. **标题略过强**："Zero-Cost Terminal Compression" 暗示压缩算法+完全无成本；实际有离线 prune/serialization/validation cost、只减 6–11% 固定格式 bytes、非编码压缩。倾向标题 C 或 "Opacity-Selected Terminal Pruning in Dynamic 3DGS SLAM Maps"。**"floater"慎用**（低-op ≠ floater，除非有空间位置证据）。

### Q5 篇幅
能撑，8–10 页核心即够；硬填 12 页暴露薄。分配建议：砍 deferred/prune 双臂故事（省 0.5–1页）；数学降级为单项界 + cohort cumulative-weight certificate；扩 matched-rate robustness + random uncertainty + 多 rate 曲线（+0.75页）；加 qualitative error maps（random/high-op 局部破坏，+0.5页）；Related Work 别用"从不问""此前没人表征"这类不可守的绝对句；limitations 七条压成一段。
**最终闭环**：`refinement 产生 tail → cohort-level contribution 测量 → controlled deletion specificity → artifact reduction → same-lifecycle SLAM validity`。当前 skeleton 已有主体。

---

## 合并动作清单（Round1+2，按优先级）

### 必做（ship-gate）
- [ ] **修正 batch theorem**：数学只证单高斯单项界；整批零代价 = 实测结论，措辞从"无条件保证"降为"实测 + 单高斯上界"。
- [ ] **cohort-level 累计权重证书**：统计每像素 `W_removed(p)=Σ T_k α_k`，报 mean/99th/max——把 "near-zero contribution" 从单高斯推到整个队列。
- [ ] **matched-rate 扩到现有 12 maps**：low/high/random × 12 PLYs，random ≥10 次（最好 20）报分布 + CI，多 rate（5/10/15%），报 GT-dPSNR + before-vs-after render distortion + 高分位像素误差。
- [ ] **lifecycle 衔接对齐**：主文只报 prune backbone 对外 ATE；deferred/prune 比较移 supplementary。

### 写作措辞修正（便宜，直接改）
- [ ] 数字范围改 8.4–18.4%，artifact 与存在性表来源差异显式说明（不同 maps/seeds/设置）。
- [ ] “Standard color refinement” → "the terminal color-refinement stage in our MonoGS-based backbone"。
- [ ] 标题倾向 C 或 "Opacity-Selected Terminal Pruning in Dynamic 3DGS SLAM Maps"；慎用"floater"。
- [ ] competitive 措辞限定 "on balloon and mv_no_box"，主表给 6 序列同一协议。
- [ ] Related Work 删不可守的绝对句。
- [ ] limitations 七条压成一段。

### 补实验预算权衡
- matched-rate 扩到 12 maps × 多策略 ≈ **1–4 GPU-h**（5–12 GPU-h if 三 rate + 20 random）——**截稿前值得付**，因为这是把 BORDERLINE 抬到 accept 的核心证据。
- 优先 CPU/offline 全部能做的（composite-weight 证书、多 rate、random 重复、before-vs-after render 度量）;GPU 只用于 render 本身。

### 状态
- Round verdict：**BORDERLINE（明显上升）→ 补两个洞可 accept-as-narrow-empirical**。
- 下一步：按两份清单改 skeleton/mechanism.md 措辞 + 跑 cohort 累计权重 + 扩 matched-rate。

---

## Round 3 (2026-08-08) — 复核 ship-gate 补实验 + 重写 skeleton/manuscript

### Verdict: **ACCEPT-AS-NARROW-EMPIRICAL for MMM**

一句话理由（codex）：两个核心 ship gate 已关闭——累计权重证书证明 cohort 整体确实近零贡献，
18-map matched-rate 实验又以重复随机对照 + 空间失真指标证明 opacity 排序的专一性，证据链已达
MMM 窄实证论文可接受标准。

### Q2 最弱支柱（提交前不必堵，但要按此定位）
**artifact savings** 最弱：删除 ~12% 固定长度 PLY records → 9–16% bytes 节省近乎线性必然，
只能作为实际效用，**不能**包装成新压缩算法或与编码压缩方法竞争。论文真正贡献 = soft-selection
characterization + 安全删除证据。

### Q3 不再需要补 blocker 级实验
若有余量，最高价值 = 把 cohort weight certificate 扩到 pt1/pt2 或全部 18 maps（增强外部一致性，
**非 ship gate**，不必须）。其余时间全部给写作。

### 提交前必修（已修，commit `af86625`）
1. `p3_cohort_weight_cert.md` 标题称 4 maps、表里只有 3 maps → 统一 **3 maps**；
2. manuscript conclusion bytes `6–11%` → **9–16%**（对齐全 18 图）。

### 保持的 claim 边界
- 严格限定 "our MonoGS-based prune backbone 的 terminal refinement"；
- 不复普适动态 SLAM / runtime acceleration / 编码压缩叙事；
- 禁词表持续有效（ADC regrowth / compute savings / online compaction / general dynamic-SLAM improvement）。
