# WORKFLOW — 四仓确立后的工作方式（2026-11-01 定稿）

## 一句话

**monogs-ours 永远是唯一做实验的地方；四个新仓是"发布快照"——里程碑到点才同步，平时不碰。**

```
日常研究（论文3 等）          里程碑触发                    成果归档
┌─────────────────┐   ┌──────────────────────┐   ┌──────────────────┐
│  monogs-ours     │──▶│ 同步到对应仓（四步）    │──▶│ RoGS-Densify 等   │
│  老规矩：NEXT_   │   │                      │   │ （只增不改的快照）  │
│  SESSION 进门、  │   └──────────────────────┘   └──────────────────┘
│  预注册、账本     │
└─────────────────┘
```

## 平时（论文3 照旧）

在 monogs-ours：`paper3/NEXT_SESSION.md` 进门 → 预注册先行 → feat 分支开发 →
账本登记。重构没动它的任何纪律设施。当前挂起事项：`P3-D2-011` 用户答复 +
G4 核销 → 580 帧 FDose。

## 三类触发时机（才动新仓）

| 时机 | 目标仓 | 动作 |
|---|---|---|
| 论文3 阶段成果（判决落地/投稿） | RoGS-Densify | 四步同步 |
| 论文2 审稿返修 | RoGS-Map | **直接在仓内改**：论文源唯一真身 = `RoGS-Map/papers/paper2/`（不在 biyelunwen）；改后重跑表生成器 + 门禁；若需新实验 → 回 monogs-ours 跑，结果经 manifest 同步 |
| 写大论文某章 | master-thesis | 数字从对应仓 `results/*/evidence/` 取（各章来源见其 README）；里程碑冻 `04_archive/` |

## 四步同步（以 RoGS-Densify 为例）

```bash
# 1. 把新产物登记进 manifest（新 run 判据件、新脚本）
$EDITOR /data/monogs-export/manifests/rogs_densify.yaml
# 2. 照单重灌（覆盖式复制！源头永远是 monogs-ours）
python /data/monogs-export/copy_by_manifest.py \
    --manifest /data/monogs-export/manifests/rogs_densify.yaml --dst /data/RoGS-Densify
# 3. 过闸（三件必跑）：
python /data/monogs-export/config_parity_check.py          # ★ 配置/主干同源机检
pytest tests/ -q                                            # 门禁基线
#    + 一次 40 帧冒烟，数字对上仓内 evidence
# 4. PROVENANCE.md 补同步记录 → commit → push
```

## 三条铁律

1. **新仓里不做实验**——所有实验回 monogs-ours；新仓只收"已判据确认"的成果。
2. **数字零手抄**——大论文引用数字一律出自对应仓 evidence/manifest，注明批次。
3. **每次 manifest 重拷后必跑 parity check**——复制是覆盖式的，会复原手工删除/修改
   （2026-11-01 RoGS-Map 事故教训，见其 PROVENANCE「事故记录」）。

## 复现性现状（详见各仓 PROVENANCE「数字验证矩阵」）

- RoGS-SLAM：Table 1 逐位重算 32/72 命中（maskfree 列 18/18）；余 35 格为外部方法列
  （结构性无工件）+ 5 格 BONN combined 待查 3090 工件。
- RoGS-Map：论文 PDF 8 表 239/239 数字全命中；284 门禁全绿。
- RoGS-Densify：105 门禁全绿 + A/B 等价；580 帧待论文3 阶段门。
- 配置同源：三仓全部 yaml 与 monogs-ours@31b0f0367 逐字节一致（parity 机检）。
