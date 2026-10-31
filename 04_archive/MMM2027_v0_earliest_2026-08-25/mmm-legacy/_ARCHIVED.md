# papers/mmm/ — 归档说明

> **2026-08-15（exp21）归档**：本目录下的 terminal compression 专稿（`skeleton.md`、
> `manuscript.md`、`mechanism.md`、`theory.md` 等）已移至
> `archive_old_era/terminal_compression/`。
>
> **原因**：方法方向已在 2026-08-09（最高准则落地，exp-v3-10）后完成演进——
> terminal compression 降级为支撑段（map footprint footnote），
> 不再作为独立头条投稿。

## 当前主线稿

**→ `papers/maskfree_bundle/skeleton.md`**

方法名：**MRCS（Mask-Free Reliability & Coverage Sampling）**
标题：*MRCS: Mask-Free Dynamic 3DGS SLAM via Reliability and Coverage Sampling*

核心主张：mask-free 内核（DynamicKeyframe + RobustTracking + ReliabilitySignal）
把动态序列 ATE 从 vanilla 压低 3.6–4.4×，不依赖语义分割，跨 mover 类型鲁棒。

## 归档文件索引

| 文件 | 内容 | 归档原因 |
|---|---|---|
| `archive_old_era/terminal_compression/skeleton.md` | MMM 投稿骨架（terminal pruning 头条，2026-08-08 codex R2 版）| 头条已换，旧叙事保留备查 |
| `archive_old_era/terminal_compression/manuscript.md` | 正文英文稿（8-10 页）| 同上 |
| `archive_old_era/terminal_compression/mechanism.md` | 机制分析（soft-suppression，ADC 已证伪）| 机制结论仍有效，但已并入 maskfree_bundle |
| `archive_old_era/terminal_compression/theory.md` | 单高斯上界数学 | 可复用，如后续补 footprint 段落 |
| `archive_old_era/terminal_compression/supplementary.md` | 补充材料框架 | 未完成 |
| `archive_old_era/terminal_compression/references.bib` | 参考文献（partial）| 待与新稿合并 |

## 可复用的 terminal compression 证据

即使不单独成稿，以下实验结果可作为 MRCS 稿的"地图占用"脚注：
- 终图 8–18% 高斯 sigmoid op<0.01（12/12 run），删除后 |dPSNR| ≤ 0.0003 dB
- cohort 级累计权重 W_p99 < 2%（`results/evidence/p3_cohort_weight_cert.md`）
- matched-rate 对照证明专一安全（`results/evidence/p3_matched_rate_extended.md`）
- 9–16% 序列化字节节省（storage/transfer，非运行时压缩）

证据代码：`scripts/p3_*.py`；数据：`results/runs/P3/`。
