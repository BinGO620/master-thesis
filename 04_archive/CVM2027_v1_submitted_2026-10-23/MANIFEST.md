# MANIFEST — CVM2027 论文 2 投稿快照

**日期**：2026-10-27（论文 1/2 收口日、论文 3 立项起点；快照内容对应 2026-10-23 投稿态）
**来源**：`biyelunwen/01_small_papers/CVM2027/` 活区工作副本的完整拷贝（去 build/ 编译中间件）
**内容**：论文 2（CVM 2027，动态场景高斯地图的解剖、压缩与离线修复）完整工作区——
  `paper2_cvm.tex` 编译入口、`template_cvm/` 模板、`figs/`+`figures/` 图件、`tables/` 表源、
  `R2_sections/` 各节草稿、`supplement/` 补充材料、`submission/` 提交包
  （final_2026-10-22 + final_2026-10-23，main.pdf + prior_work + supplementary.pdf）、
  `REVIEW_STATUS.md`（审稿前状态）、`VERSION_LOCK.md`、`R2_NARRATIVE.md`。
**对应 git**：`2da89592a`（论文 2 v8.18c 提交包 final_2026-10-23 入库 commit）。
**性质**：在投稿件，等审稿结果（录用通知预计 2026-12-15）。审稿意见回来后按意见在活区改稿，
  改到里程碑再冻下一版快照。
**与论文 1 的关系**：CVM 的 baseline 臂 = MMM 的完整方法（`method_from` 指向前者，
  只关 SWBA 和回环），存在继承关系；数字交叉核对规则见
  `results/paper2_fulltable/evidence/paper1_paper2_crosscheck_2026-10-05.md`
  （场景面板不同：MMM 4 场景 / CVM 7 序列，禁混排，引用须注明批次）。
**恢复方式**：`cp -r CVM2027_v1_submitted_2026-10-23/ ../01_small_papers/CVM2027/`，
  活区永远只放最新版。
