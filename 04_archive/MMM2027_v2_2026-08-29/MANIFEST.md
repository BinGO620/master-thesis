# MMM2027 v2 归档

**归档日期**：2026-10-23
**归档原因**：被 v3（投稿定稿版）取代，从 `01_small_papers/MMM2027/latex/` 移出
**状态**：历史稿，不用于投稿，不再维护

## 这是什么

MRCS 时期的第二版构建：
- 标题还是 `MRCS: Reliability-Guided Coverage Sampling...`，不是投稿用的 RoGS-SLAM
- 正文 23 页，超出 MMM 的 12+2 页限制
- 参考文献 22 条，投稿版是 29 条
- 正文仍带 S1-S12 的 SI 指针（投稿版已内联展开）
- `body_v2.tex` 由 `manuscript.md` 生成，那条链已废弃

## 文件

| 文件 | 说明 |
|---|---|
| `latex/main_v2.tex` | v2 主文件 |
| `latex/body_v2.tex` | v2 正文，68 KB（v3 是 34 KB） |
| `latex/main_v2.pdf` | v2 构建产物，23 页 |
| `latex/compile_v2.sh` | v2 的编译脚本，已失效（路径指向旧的 bundle 位置） |
| `latex/postprocess_body.py` | v2 的正文后处理脚本 |

## 取代者

`01_small_papers/MMM2027/`（v3，对应 git tag `mmm2027-submission`）
