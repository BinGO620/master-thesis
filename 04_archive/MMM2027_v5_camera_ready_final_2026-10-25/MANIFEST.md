# MMM2027 v5 camera-ready 定稿快照

**冻结日期**：2026-10-25
**来源**：`01_small_papers/MMM2027/`（`paper_rev1_camera_ready/`、`deliverable/`、`figure_src/scripts/`）
**状态**：camera-ready 定稿，14 页（12 正文 + 2 参考文献）

## 与 v4 的差别

v4 是审稿意见整改完成、但图与正文还有三处硬问题的版本。v5 修掉的就是这三处。

### 1. 正文删掉了指向源码包的句子

v4 在 4.1 节末尾有一句，说预注册记录、各臂配置、factorial 逐 seed 结果等六样东西
「ship with the source archive under `evidence/`」。这句话让主论文依赖一个发表后
读者拿不到的外部文件，自洽性被破坏。**已整句删除。**

同类的两处也一并改掉：

- 3.1 节末尾 "Constants are resolved from the run configuration" → "Every constant is
  given where it is introduced"（常数本来就全写在正文里）
- 3.6 节末尾 "resolved from the run configuration" → "stated in Secs. 3.3--3.6"
- 3.3 节 "the two other kernels the codebase implements" → "the two other kernels we implemented"

5.3 节的 "drift discipline"、"same-campaign cells" 也改成读者能懂的
"batch-to-batch drift we budget"、"same-batch cells"。

### 2. 三处数字按证据表改正

随源码包发出的 `table1_18seq_ate.csv` 与正文对不上，审稿人能查出来。

| 位置 | v4 | v5（= 证据表） |
|---|---|---|
| 5.3 mv_no_box 分母 | 2.65±0.12 | **2.66±0.12** |
| Lim.1 pt1 mask-free | 32.41±**8.52** | 32.41±**8.51** |
| Lim.2 pt2 combined | **10.45** | **10.44** |

### 3. 所有图内文字 ≥ 6 pt

Springer camera-ready 说明明确要求图内字母不得小于 6 pt。v4 实测：

| 图 | v4 最小字号 | v5 |
|---|---|---|
| 图 1 | 4.9 pt | 6.0 |
| 图 2 | 4.6 pt | 6.0 |
| 图 3 | 5.7 pt | 6.0 |
| 图 5 | **4.3 pt** | 6.0 |
| 图 6 | 5.5 pt | 6.0 |

根因有两层。图 3 的标注直接写了 `fontsize=5.8`。图 5/6 更隐蔽：脚本按 12.2 cm
画布、7 pt 画图，正文却按 0.72 / 0.95 倍宽度排入，缩放系数 0.739 / 0.985 把字号
一起压小了。修法是**按最终印刷宽度作画**——图 5 的画布改成 `TEXTWIDTH * 0.72`，
图内部的字号按这个尺度重新定，印出来就是画出来的大小。

修字号时暴露并修掉的排版缺陷：

- 图 5 (b) 图例在收窄画布后被裁掉 → 恢复原画布宽度、字号反向放大 1/0.739
- 图 1 的 L 框字号提到 8.8 pt 后，两行文字纵向撑破框线 → L 框高度 0.60→0.95 cm
- 图 2 的 disagreement 框同样撑破 → 计算行框高 0.72→0.86 cm
- 图 2 的 e_flow 框上边被 s 框压住 → 同步调整

## 目录

| 路径 | 内容 |
|---|---|
| `source/` | `paper_rev1_camera_ready/` 原样，含 `CHANGES.md` |
| `deliverable/` | 交付 PDF（295135 B，14 页）+ 源码 zip（231957 B，24 文件）+ 六图 + `evidence/` |
| `figure_scripts/` | 六张图的生成脚本，含本次修好的字号参数 |

## 验证

- `pdftotext` md5 `740b66eb9d66d02ef0bcb70b70ea1984`，与工作区编译一致
- 源码 zip 解压到干净目录重编，14 页，同一 md5
- 六张图逐张用 PyMuPDF 量了实际印出的字号，低于 6 pt 的 span 数为 **0**
- 正文扫过 `evidence/`、`source archive`、`supplementary`，命中 0
- 风格检查：破折号 7.0/10k、句长 CV 0.799、AI 高频短语 0

## 恢复方式

```bash
cd source && TECTONIC=/data/conda_envs/tex/bin/tectonic ./build.sh   # 14 页
```

图不在 `source/` 里，用 `deliverable/RoGS-SLAM_MMM2027_source.zip`（内含 `figures/`）
或把 `deliverable/*.pdf` 放回 `source/../figures/`。
