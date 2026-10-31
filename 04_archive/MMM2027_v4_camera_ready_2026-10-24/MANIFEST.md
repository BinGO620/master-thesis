# MMM2027 v4 camera-ready 快照

**冻结日期**：2026-10-24
**来源**：`01_small_papers/MMM2027/paper_rev1_camera_ready/` 与 `.../deliverable/`
**状态**：camera-ready 内容定稿，14 页（12 正文 + 2 参考文献）

## 这是什么

论文 1 收到四份审稿意见后的整改版。与投稿版（`MMM2027_v3_submission_2026-09-01/`）
的差别集中在内容修正与图重排，逐条记录见 `source/CHANGES.md`。

内容侧的要点：

- 修正 3.3 节的事实错误。原文写 "replaces the L2 tracking residual"，
  实际代码是 L1 光度 + 几何残差，改为"保留 L1 目标、在其上叠加 IRLS 权重"。
- 补齐方法定义，包括权重作用层级与归一化式、e_flow 的完整归一化、
  几何线索 g 的定义、生命周期证据规则、warm-up 期间位姿来源、变更清单漏项。
- 静态退化的归因改写。真实根因是位姿误差闭环而非 RAFT 噪声，
  证据在 `results/evidence/archive_pre_exp32/eflow_pose_error_defect.md`。

图侧重排：

| 图 | 本版 | 投稿版 |
|---|---|---|
| fig1 | 满宽 1:1，框宽按标签实测，全部正交路由 | 0.73 宽旧版 |
| fig2 | 可靠性流程图，几何线索 g 独立成框 | 旧版 |
| fig3 | 单行五格，题注 first two / last three | 3 列 2 行，题注 Top/Bottom |
| fig4 / fig6 | 满宽 | 0.64 / 0.78 |
| fig5 | 0.72 | 0.64 |

## 目录

| 路径 | 内容 |
|---|---|
| `source/` | camera-ready 工作副本，`body.tex` md5 `0a525fc0…`，附 `CHANGES.md` |
| `deliverable/` | 交付物：`RoGS-SLAM_MMM2027_camera_ready.pdf`（295646 B，14 页）+ 源码 zip（232325 B，24 文件）+ 平铺的源与图 + `evidence/` |

`source/` 里剔掉了 `build/` 与 `build_deliverable/`（编译中间件，可再生成）。

## 验证口径

- 交付 PDF 与 `source/` 现场编译产物：`pdftotext` md5 `c37f6a14b576262459d4fe22d63531bf`，
  逐字节相同；60 dpi 逐页渲图，14 页成对相同。
- 源码 zip 解压到干净目录重编，14 页，`pdftotext` md5 同上。
- 关键词四个词条与投稿版逐字相同，未改。

## 恢复方式

```bash
cd source && TECTONIC=/data/conda_envs/tex/bin/tectonic ./build.sh   # 14 页
```

图在 `source` 同级不存在，需从 `deliverable/` 平铺件补齐，或直接用
`deliverable/RoGS-SLAM_MMM2027_source.zip`（内含 `figures/`）。
