# figures/ — 图片资产登记表

> 论文所有图片（架构图/曲线图/对比图/定性结果）产出后在此登记一行。
> 图片文件放本目录（PNG/PDF），生成脚本放 02_analysis/scripts/figures/
> （可复现：一个图一个脚本，数据源用绝对路径引用 monogs-ours/results）。
> 正文（chapters/*.md）用相对路径 `../../03_results/figures/xxx.png` 引用。

## 登记表

| 文件 | 章节 | 类型 | 说明/数据源 | 生成脚本 | 登记日期 |
|---|---|---|---|---|---|
| fig5_1_pilot_arms.png | Ch5 | 分组柱状 | pilot 四臂×三序列全网格（判决+对照） | 02_analysis/scripts/figures/fig5_1_pilot_arms.py | 2026-09-05 |
| fig5_1_formal_ghost_cost.png | Ch5(图5.2) | 双面板柱状 | 正式研究主指标+代价：(a)残差代理 3seq×3arm×3seed (b)高斯数膨胀%；数据源 lifecycle_formal/{mapping,efficiency}_raw.csv | 02_analysis/scripts/figures/fig5_1_formal.py | 2026-09-09 |
| fig5_densification_ablation.png | Ch5(动机) | 柱状 | Phase 0 消融 7 臂（含 std 误差棒、非标准序列警示） | 02_analysis/scripts/figures/fig5_ablation_bars.py | 2026-09-05 |
| fig2_3_taxonomy.png | Ch2.3(图2.3) | 分类树 | anti/face 两路线代表方法+本文高亮 | 02_analysis/scripts/figures/fig2_3_taxonomy.py | 2026-09-05 |
| fig4_swba_mechanism.png | Ch4 | 机制示意 | SWBA 稠密窗口边+固定锚+回灌（回灌箭头=本图灵魂） | 02_analysis/scripts/figures/fig4_swba_mechanism.py | 2026-09-05 |
| fig2_1_paradigm_timeline.png | Ch2 | 时间线 | SLAM 四范式演进+本文定位 | 02_analysis/scripts/figures/fig2_1_paradigm_timeline.py | 2026-09-05 |
| fig1_architecture.png | Ch1 | 架构示意 | 论文第一图：三研究内容（观测/估计/表示）在系统流水线中的定位 | 02_analysis/scripts/figures/fig1_architecture.py | 2026-09-05 |
| fig4_drift_curves.png | Ch4 | 曲线 | pt1 逐帧 APE 对比（R2/R6/R9，事件窗口 221-246 标注）；数据源 per_frame_ape.csv seed0 | 02_analysis/scripts/figures/fig_drift_curves.py | 2026-09-05 |
| fig4_ladder_pt1.png | Ch4 | 柱状阶梯 | person_tracking 修复阶梯关键臂选示（R1-R18 串行时代 + fulltable 并发时代终态两臂斜线纹理区分，含 5cm 目标线；绿=两层架构 7.40 与部署终态 gate 7.83，琥珀=回环收口探索）；数据源 person_tracking_ladder.md（两代口径注记） | 02_analysis/scripts/figures/fig_ladder.py | 2026-09-08 |
| fig2_4_map_lifecycle.png | Ch2.4 | 决策链示意 | 在线地图管理五状态（插入/致密化/持久化/退出/恢复）+ 每步判据 + 本文 Ch.3 提交端 / Ch.5 状态转换端定位 + 空缺 G3 说明 | 02_analysis/scripts/figures/fig2_4_map_lifecycle.py | 2026-09-14 |
| fig4_r11_segments.png | Ch4.5.2 | 分组柱状 | R11 组合臂逐段（0-99/100-199/200-299/300-399）对比 R9：前段改善（8.09→7.55、9.33→8.75）但中段基线被侵蚀（6.82→7.38、7.24→7.81），整体增益归零；数据源 person_tracking_repair/{r9_swba_pt1,r11_swba_mask_pt1}_seed0/**/per_frame_ape.csv | 02_analysis/scripts/figures/fig_r11_segments.py | 2026-09-15 |
| fig2_2_pipeline.png | Ch2.2 | 系统流水线示意 | 3DGS-SLAM 三模块（跟踪/建图/致密化）闭环 + 动态内容注入残差路径 + 本文三章挂接点（Ch3 观测端/Ch4 跟踪循环内/Ch5 地图生命周期） | 02_analysis/scripts/figures/fig2_2_pipeline.py | 2026-09-15 |

## 待画图清单（按优先级，导师意见：一图顶千言）

1. ~~总架构图~~（已完成 v1，答辩版可再美化）
2. ~~修复阶梯瀑布图~~（已完成，见登记行）
3. ~~逐帧漂移曲线~~（已完成）
4. ~~R11 组合臂逐段柱状图~~（已完成，见登记行）
5. **anti/face-dynamic 分类图**（Ch.2.3）——两条路线的代表方法树
6. **SWBA 机制图**（Ch.4）——稠密窗口边 + 固定锚 + 回灌示意
7. **致密化消融柱状图**（Ch.5）——7 臂 ATE + 高斯数双轴
