# 小论文（01_small_papers）

两篇会议小论文的**完整可编译副本**。原件仍在仓库的 `papers/` 下，这里是小论文工作区，
两边内容一致；若要改稿，先定在哪边改，别两边同时动。

## 索引

### MMM2027（已录用，camera-ready 定稿）

RoGS-SLAM，可靠性引导加权 + 时域覆盖采样，动态场景下的 mask-free 方案。
**14 页（12 正文 + 2 参考文献）**，交付物已就绪，等签版权表与 conftool 上传。

```
MMM2027/
├── paper_rev1_camera_ready/  当前工作副本：main.tex + body.tex + build.sh（改这里）
├── deliverable/              交付物：camera-ready PDF + 源码 zip + evidence/
├── figures/                  六张图的唯一真身（脚本源在 figure_src/）
├── figure_src/               绘图脚本 + 渲染素材
├── paper/                    投稿版原样，只读，可回退
├── supplementary/            补充材料（MMM 无 SI 通道，仅内部留档）
└── source_zip/               源码包平铺目录
```

编译：`cd paper_rev1_camera_ready && TECTONIC=/data/conda_envs/tex/bin/tectonic ./build.sh`（14 页）。
`tectonic` 不在 PATH，必须带这个前缀。

**图只放 `figures/`**。`paper_rev1_camera_ready/` 下不要放图片副本——XeTeX 先查当前目录，
`\graphicspath` 只是后备，放了副本会导致改图不生效。

改稿前先读 `paper_rev1_camera_ready/CHANGES.md`。各版本的完整快照（最早稿、投稿版、
camera-ready）在 `../04_archive/`，索引见 `../04_archive/readme.md`。

### CVM2027（在投）

动态场景高斯地图的解剖、压缩与离线修复。

| 路径 | 内容 |
|---|---|
| `CVM2027/paper2_cvm.tex` | **编译入口**（主文件） |
| `CVM2027/build.sh` | 一键编译，产 `build/paper2_cvm.pdf` |
| `CVM2027/template_cvm/` | CVM 模板：`cvm.sty`、`cvm.bst`、`cvmbib.bib` 等 |
| `CVM2027/figs/` | 论文用的图（pdf + png） |
| `CVM2027/tables/` | 8 张表的 tex 源 |
| `CVM2027/figures/` | 图的**工作区**：每图一目录，含 prompt 与 PROVENANCE |
| `CVM2027/supplement/` | 补充材料 tex |
| `CVM2027/submission/` | 提交快照（final_2026-10-22 / final_2026-10-23） |
| `CVM2027/VERSION_LOCK.md` | 版本锁，记录每个构建的哈希与页数 |
| `CVM2027/R2_sections/` | 各节 Markdown 草稿 |
| `CVM2027/INTERNAL_tex_notes.md` | 内部排版笔记，不入投稿件 |

## 编译验证（2026-10-24）

两篇都能在本机原样复现交付件：

- MMM：`paper_rev1_camera_ready/build/main.pdf` 14 页，`pdftotext` md5 `c37f6a14…`，
  与 `deliverable/` 里的 camera-ready PDF 逐字节相同
- CVM：`build/paper2_cvm.pdf` 14 页，与投稿件逐字一致

编译器用 tectonic（`/data/conda_envs/tex/bin/tectonic`），会自动下载缺失宏包。

## 两篇的关系（写大论文时必须讲清）

CVM 那篇的 baseline 臂，就是 MMM 那篇的完整方法：配置里 `method_from` 指向前者，
只关掉了 SWBA 和回环。所以两篇不是独立工作，存在继承关系。

数字口径的交叉核对表在
`/data/monogs-ours/results/paper2_fulltable/evidence/paper1_paper2_crosscheck_2026-10-05.md`，
其中几条硬规则：MMM 是 4 个 BONN 场景、CVM 是 7 个序列，两表不可合并、不可逐序列对比，
引用绝对数字必须注明批次。
