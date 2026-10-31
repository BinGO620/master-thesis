# master-thesis

硕士学位论文写作区 + 论文史档案。对应三个研究内容，分别由三个代码仓库承载：

```
                 ┌────────────────────────────────────────────┐
                 │              master-thesis（本仓）           │
                 │   03_main/  大论文（第3/4/5章 = 三个研究内容）  │
                 └──────┬──────────────┬──────────────┬────────┘
                        │              │              │
        第3章 可靠观测    │   第4章 地图表示与维护        │  第5章 地图生长
                        ▼              ▼              ▼
                 RoGS-SLAM        RoGS-Map        RoGS-Densify
                (MMM 2027 录用)  (CVM 2027 在投)    (论文3 进行中)
```

继承关系：**可靠观测 → 地图表示与维护 → 地图生长**（RoGS-Map 的 baseline 臂 =
RoGS-SLAM 完整方法；RoGS-Densify 的实验臂继承同一方法平台）。

## 目录（真身 vs 副本）

| 路径 | 身份 | 说明 |
|---|---|---|
| `03_main/` | **唯一真身** | 大论文：`main.tex` + `chapters/`（第3/4/5章）、`OUTLINE.md`（章节规划与写作纪律）、`WRITING_RULES.md`、`TERMS.md` |
| `01_small_papers/MMM2027/` | **唯一真身** | 论文1 camera-ready 工作区（编译/图/交付物/evidence）；代码复现见 RoGS-SLAM |
| `01_small_papers/CVM2027/` | **冻结副本** | 论文2 源已迁至 **RoGS-Map `papers/paper2/`**（唯一真身），本目录只读，勿改 |
| `02_resources/` | 参考资料 | 审稿分析、模板、CFP |
| `04_archive/` | 历史快照 | 两篇小论文的 v0–v6 版本链（只增不改） |

## 各章 ↔ 证据链

每章的数字与判据件在对应代码仓库内（`results/` + `evidence/`），大论文引用时按
`OUTLINE.md` 的口径纪律注明批次与来源仓，不把数字搬进本仓。

- 第3章 ↔ RoGS-SLAM：Table 1（18 序列）由 `results/evidence/verify_table1.py` 重算核对。
- 第4章 ↔ RoGS-Map：R33 主表 / R-D / 修复 L3 的单一事实源为其 `results/*/evidence/`。
- 第5章 ↔ RoGS-Densify：Phase 0 / FDose 预注册与判决在 `paper3/`（预注册即判据先锁）。

## 已知过期引用（如实登记）

`03_main/OUTLINE.md` 等文件里指向 monogs-ours 内部路径的引用（如 `../../paper3/PROBLEM.md`）
在新仓结构下已过期——对应内容已分别迁往 RoGS-Densify（`paper3/`）与本仓。修订章节时顺手更新。

## 编译

```bash
cd 03_main && ./build.sh          # 大论文
cd 01_small_papers/MMM2027/paper_rev1_camera_ready && TECTONIC=/data/conda_envs/tex/bin/tectonic ./build.sh
```

## 纪律

- 两篇小论文的会议源与大论文章节的关系见 `03_main/OUTLINE.md` §六（会议论文不直接搬入）。
- `04_archive/` 只增不改：每到一个里程碑整份冻结快照。
- MMM2027 camera-ready 硬截止 2026-11-01，交付前不动 `deliverable/`。
