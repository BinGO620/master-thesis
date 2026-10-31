# MMM 2027 — RoGS-SLAM（投稿版）

这是论文 1 的定稿包，17 个文件，1.1 MB。全部内容自包含，不依赖仓库任何其他文件。

## 目录

```
MMM2027/
├── paper/                 主论文
│   ├── main.tex           主文件，\documentclass{llncs}
│   ├── body.tex           正文（第一章到第六章）
│   ├── references.bib     29 条参考文献
│   ├── llncs.cls          Springer LNCS 文档类
│   ├── splncs04.bst       文献样式
│   └── build.sh           编译 → build/main.pdf
├── supplementary/         补充材料（MMM 无 SI 通道，内部留档）
│   ├── main.tex
│   ├── body.tex
│   └── build.sh
├── figures/               正文六张图，按正文出现顺序命名
│   ├── fig1_pipeline.pdf              方法与组件挂载总览
│   ├── fig2_reliability.pdf           可靠性信号：光流到权重
│   ├── fig3_map_comparison.pdf        各路配置的地图对比
│   ├── fig4_component_necessity.pdf   组件必要性的场景分层（主贡献）
│   ├── fig5_controlled_comparison.pdf 两个受控对照
│   └── fig6_pose_endpoints.pdf        一个介入三个位姿终点
└── README.md
```

## 编译

```bash
cd paper && ./build.sh           # 14 页（12 正文 + 2 文献）
cd supplementary && ./build.sh   # 11 页
```

引擎是 tectonic，缺宏包会自动下载，第一次编译需要网络。

## 验证

正文编译产物与已投出的 `papers/MMM2027_RoGS-SLAM_submission.pdf` 逐字一致
（`pdftotext` 全文比对）。源文件与 git tag `mmm2027-submission` 逐字节一致。
把 `paper/` 和 `figures/` 单独拷到空目录也能编出同样的结果。

## 交源码

整个 `MMM2027/` 目录直接打包即可。如果对方只要最小集，去掉 `supplementary/`
和 `README.md`，剩下的 `paper/` 加 `figures/` 也完整。

## 备注

`body.tex` 以前是由 Markdown 源经脚本生成的，那个脚本和 md 源都已移除。
现在 `body.tex` 就是唯一的正文源，直接编辑它。

补充材料的图也用 `figures/` 下的 pdf，但 MMM 2027 没有 SI 投稿通道，
这部分只是内部留档。

原来的 v2 版（MRCS 时期，23 页）和全部历史文件已归档到
`../../04_archive/MMM2027_full_backup_2026-10-23.zip`。
