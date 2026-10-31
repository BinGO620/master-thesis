# MMM2027 全量备份（清理前）

**打包日期**：2026-10-23
**原因**：按"只保留成品"的要求把 `01_small_papers/MMM2027/` 从 188 文件 / 20 MB
        裁剪到 17 文件 / 492 KB，删掉的全部在这里。

## 压缩包里有什么

`MMM2027_full_backup_2026-10-23.zip`（18 MB，188 个文件），包含清理前的完整目录：

| 目录 | 内容 | 为什么删 |
|---|---|---|
| `archive/` | 历史稿（manuscript v0/v1）、12 份审稿意见、写作路线图、禁词表、术语表、图表规划、更早的 mmm-legacy | 写作过程材料，成品不需要 |
| `checks/` | 查重 docx（4.1 MB）、5 个去 AI 痕迹脚本 | 过程工具 |
| `figures/archive/` | 被取代的旧图 14 张 + 两批中间渲染件（8.8 MB） | 旧版本 |
| `figures/*.png, *.svg` | 六张图的 png/svg 版本 | 编译只用 pdf |
| `figures/*.py` | 20 个绘图脚本 | 不能独立复现（依赖 results/ 下的跑批数据） |
| `tables/` | 5 张表的 csv 与 md + PROVENANCE | 表已内联在正文里 |
| `MMM2026_submission/` | 提交快照 PDF（与 `papers/MMM2027_RoGS-SLAM_submission.pdf` 哈希相同） | 重复 |
| `manuscript_v3.md` | 正文 Markdown 源 | 生成脚本已丢，改不动，正文以 body.tex 为准 |
| `supplementary.md` | SI 的 Markdown 源 | 同上 |
| `latex/LLNCS_README.txt` | LNCS 模板原版说明 | 不需要 |
| `latex_si/postprocess_si.py` | SI 后处理脚本 | 一次性转换工具 |
| `latex/main_v2.tex` 等 v2 全套 | MRCS 时期旧稿 | 已单独归档到 `MMM2027_v2_2026-08-29/` |

## 恢复方式

```bash
cd /data/monogs-ours/biyelunwen/01_small_papers
unzip ../../04_archive/MMM2027_full_backup_2026-10-23.zip
```

解出来是 `MMM2027/` 目录，与清理前的结构一致（文件是英文旧名 `main_v3.tex` 那套）。
注意：恢复会覆盖当前的精简版。
