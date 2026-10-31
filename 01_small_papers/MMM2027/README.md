# MMM 2027 — RoGS-SLAM

论文 1 的工作区。当前状态：**camera-ready 已定稿，14 页**（12 正文 + 2 参考文献），
交付物在 `deliverable/`，等签版权表与 conftool 上传（硬截止 2026-11-01）。

## 目录

```
MMM2027/
├── paper_rev1_camera_ready/   当前工作副本（改这里）
│   ├── main.tex
│   ├── body.tex               正文唯一源，直接编辑
│   ├── build.sh               编译 → build/main.pdf
│   └── CHANGES.md             逐条改动记录，动前必读
├── deliverable/               交付物
│   ├── RoGS-SLAM_MMM2027_camera_ready.pdf   camera-ready 正文，14 页
│   ├── RoGS-SLAM_MMM2027_source.zip         源码包（24 文件，自包含）
│   └── evidence/                            结论级数字的出处
├── figures/                   六张图的唯一真身
│   ├── fig1_pipeline.pdf              方法与组件挂载总览
│   ├── fig2_reliability.pdf           可靠性信号：光流到权重
│   ├── fig3_map_comparison.pdf        各路配置的地图对比
│   ├── fig4_component_necessity.pdf   组件必要性的场景分层（主贡献）
│   ├── fig5_controlled_comparison.pdf 两个受控对照
│   └── fig6_pose_endpoints.pdf        一个介入三个位姿终点
├── figure_src/                绘图脚本 + 渲染素材（重画图从这里改）
├── paper/                     投稿版原样，只读（= git tag mmm2027-submission）
├── supplementary/             补充材料（MMM 无 SI 通道，内部留档）
├── source_zip/                源码包平铺目录
└── README.md
```

## 编译

```bash
cd paper_rev1_camera_ready && TECTONIC=/data/conda_envs/tex/bin/tectonic ./build.sh
cd paper && ./build.sh           # 投稿版，14 页
cd supplementary && ./build.sh   # 11 页
```

引擎是 tectonic，缺宏包会自动下载，第一次编译需要网络。**`tectonic` 不在 PATH**，
每次都要显式带 `TECTONIC=/data/conda_envs/tex/bin/tectonic` 前缀。

**图只放 `figures/`**。`paper_rev1_camera_ready/` 下不要放图片副本——XeTeX 找图先查
当前目录，`\graphicspath` 只是后备，放了副本就会导致改了 `figures/` 却不生效。

## 验证

camera-ready 的交付 PDF 与 `paper_rev1_camera_ready/` 现场编译产物：`pdftotext` md5
`63e5aa3fe1d5a582674a8330e08f52c6`，全文相同；14 页。
源码 zip 解压到干净目录重编也是 14 页、同一 md5。

### 图（2026-10-26 重做后）

```bash
cd figure_src && ./build_figures.sh        # 重建 + 自检 + 安装到 ../figures/
cd figure_src && ./build_figures.sh --check  # 只重建自检，不安装
```

每个脚本保存前自己审计，不达标直接报错退出：印刷字号 < 6.6 pt、任意两标签重叠、
文字出画布、标签越出所属框、任何边短于 12 pt。六图页宽必须都是 345.827 pt
（= `\textwidth`，排入缩放 1.000），否则字号会被二次缩放。

### 字体（用户特别问过）

**合规，且与论文2的坑不是一回事。**

- `main.tex` 只有 `\usepackage[T1]{fontenc}`，没有任何字体替换
  （无 `times` / `newtxtext` / `setmainfont`）。**不要加** `times`：tectonic 下它
  静默失败，字体回退且加粗斜体全丢——那是论文2踩过的坑。
- 字体由官方 `llncs.cls` v2.24 决定（Latin Modern / Computer Modern）。用未修改的
  cls 编一个空壳样例，产出字体与本文完全相同（`LMRoman10-Regular`、
  `LMRoman9-Bold`…，子集前缀都一样）。
- 正式排版字体由 Springer 在 production 套用；作者只需不覆盖模板设定。
- 查证命令：

```bash
pdffonts deliverable/RoGS-SLAM_MMM2027_camera_ready.pdf          # 应见 LMRoman* 的 Bold/Italic
grep -iE "Font shape|substitut" paper_rev1_camera_ready/build/main.log   # 应为空
```

投稿版（`paper/`）与已投出的 `papers/MMM2027_RoGS-SLAM_submission.pdf` 逐字一致，
源文件与 git tag `mmm2027-submission` 逐字节一致。

## 交源码

上传 conftool 用的是 `deliverable/RoGS-SLAM_MMM2027_source.zip`，解压即编译，
里面含 `figures/` 与 `evidence/`。不要再从活区临时打包——活区随时会变。

**包内 `main.tex` 的 `\graphicspath` 必须是 `{figures/}`**（包内相对路径），
活区的 `paper_rev1_camera_ready/main.tex` 是 `{../figures/}`。两边不同，
互相覆盖会让 zip 编不过或让活区出错图。

## 备注

`body.tex` 以前是由 Markdown 源经脚本生成的，那个脚本和 md 源都已移除。
现在 `body.tex` 就是唯一的正文源，直接编辑它。

补充材料的图也用 `figures/` 下的 pdf，但 MMM 2027 没有 SI 投稿通道，
这部分只是内部留档。

原来的 v2 版（MRCS 时期，23 页）和全部历史文件已归档到
`../../04_archive/MMM2027_full_backup_2026-10-23.zip`。

## 版本链

本目录（`01_small_papers/MMM2027/`）**永远是最新版**。以下快照在 `../../04_archive/`：

| 快照 | 日期 | 是什么 |
|---|---|---|
| `MMM2027_v0_earliest_2026-08-25/` | 2026-08-25 | 最早的可读文本（MRCS 时期），含穷尽式初稿 v0 |
| `MMM2027_v2_2026-08-29/` | 2026-08-29 | MRCS 第二版 tex，23 页 |
| `MMM2027_v3_submission_2026-09-01/` | 2026-09-01 | 投出去的版本（= 本目录 `paper/` 的内容） |
| `MMM2027_v4_camera_ready_2026-10-24/` | 2026-10-24 | camera-ready 整改版 |
| `MMM2027_v5_camera_ready_final_2026-10-25/` | 2026-10-25 | camera-ready 定稿：恢复自洽、数字对表、图内字号 ≥ 6 pt |
| `MMM2027_v6_figures_rebuilt_2026-10-26/` | 2026-10-26 | **当前定稿**：六图全部重做 + 压回 14 页（= 本目录现状） |

索引与约定见 `../../04_archive/readme.md`。以后每改到一个里程碑，就把完整状态
整份冻进 `04_archive`，不要只存增量。
