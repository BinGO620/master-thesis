# MMM2027 v0 最早稿快照

**冻结日期**：2026-10-24（内容冻结点为 2026-08-25，从既有备份中抽出，未改动字节）
**来源**：`04_archive/MMM2027_full_backup_2026-10-23.zip`
**对应 git tag**：`mmm2027-submission` 的 `papers/maskfree_bundle/archive/` 子树

## 这是什么

论文 1 最早的可读文本形态，比投稿版早一周。当时方法名还叫 MRCS
（Mask-Free Reliability & Coverage Sampling），不是现在的 RoGS-SLAM。

这个快照不是"某一版 tex"，而是写作起点阶段的三层材料，按时间从旧到新：

| 路径 | 日期 | 内容 |
|---|---|---|
| `mmm-legacy/` | 2026-08 上旬 | 更早的 terminal compression 专稿（头条是终端剪枝，后降级为脚注），含 idea/RESEARCH_BRIEF、骨架、机制、理论、12 份过程文档 |
| `skeleton_exp21.md` | 2026-08-25 前 | exp21 时期的投稿骨架，头条已换成 mask-free |
| `manuscript_v0.md` | 2026-08-25 | **穷尽式初稿，10057 词**，七节全通。刻意保留的资产，不是废弃物 |
| `manuscript_v1.md` | 2026-08-25 | 从 v0 压缩出的精选稿，8714 词，向 v2 推进 |

## 注意

- `manuscript_v0.md` 在自己文件头写明是 **FROZEN RECORD**，压缩工作发生在后来的稿里。
  它存在的理由是不同的页数限制/扩展版/毕业论文章节可以直接从这里取材，
  而不是回头去证据文件里重新挖。
- `mmm-legacy/` 下的 `references.bib` 是 partial 的，别当完整文献表用。
- 这一期的数字口径与投稿版不同（例如当时的倍数主张后来被审计推翻），
  **引用这里的任何数字前先核口径**，不要与 v3 之后的读数混用。

## 恢复方式

纯 Markdown 与图片，直接读即可，无需编译。若要重排成 tex，需自建骨架——
当时的 md→tex 生成脚本已丢失，正文以 v3 的 `body.tex` 为准。
