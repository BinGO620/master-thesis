# MMM2027 v3 投稿版快照

**冻结日期**：2026-10-24（内容为 2026-09-01 投出的版本，原样搬运，未改动任何字节）
**来源**：`01_small_papers/MMM2027_submission.zip`（md5 `98987ab32ae52ef98690abe59b700580`）
+ `/data/monogs-ours/papers/MMM2027_RoGS-SLAM_submission.pdf`（md5 `12b2ff1131469d80ecc3b6d188e517a3`）
**对应 git tag**：`mmm2027-submission`

## 这是什么

投给 MMM 2027 的原始投稿包。审稿人看到的正文、图、参考文献就是这一套。
`paper/` 与 `supplementary/` 与现行的 `01_small_papers/MMM2027/paper`、
`.../supplementary` 逐文件相同——活区那两份就是从这里长出来的。

## 目录

| 路径 | 内容 |
|---|---|
| `MMM2027/paper/` | 投稿时的主论文源（body.tex md5 `6034bbe8…`） |
| `MMM2027/figures/` | 投稿时的六张图（fig1/2/3 后来在 camera-ready 重画，这里是旧版） |
| `MMM2027/supplementary/` | 补充材料源。MMM 无 SI 通道，从未投出，仅内部留档 |
| `MMM2027/README.md` | 当时的目录说明 |
| `MMM2027_RoGS-SLAM_submission.pdf` | 投出去的 PDF 本体，14 页，369080 B |
| `MMM2027_submission.zip` | 原始 zip，保留原样以便与活区对拍 |

## 为什么归档

投稿版已经定稿，不会被再改。活区 `MMM2027/paper` 继续跟着 camera-ready 走，
两边日后必然分叉；把投稿那一刻的状态单独冻在这里，日后要引用"审稿人看到的版本"
不用去翻 git tag（tag 里是整仓，取单篇不方便）。

## 恢复方式

直接把 `MMM2027/` 整个目录拷出去即可编译，与投稿时一致：

```bash
cd MMM2027/paper && TECTONIC=/data/conda_envs/tex/bin/tectonic ./build.sh   # 14 页
```

与投稿 PDF 的比对口径：`pdftotext` 全文逐字一致。
