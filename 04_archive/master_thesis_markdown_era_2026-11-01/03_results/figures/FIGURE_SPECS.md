# 图设计稿（文字版，供重绘用）

> 我（当前会话模型）无视觉功能，图片渲染后的质量无法自检。此文件
> 把每张图的设计意图、数据、验收标准写清楚，等有视觉能力的会话
> （或用户）按此重绘/验收。已渲染的图：v1 已出（见 REGISTER.md），
> 本文件同时作为其验收清单。
>
> **状态同步（2026-09-15）**：REGISTER 的 7 张排队图已全部渲染完成
> （fig1_architecture / fig2_1_paradigm_timeline / fig2_2_pipeline /
> fig2_3_taxonomy / fig2_4_map_lifecycle / fig4_ladder_pt1 /
> fig4_drift_curves / fig4_swba_mechanism / fig4_r11_segments /
> fig5_1_pilot_arms / fig5_1_formal_ghost_cost / fig5_densification_ablation）。
> 本文件下方"待画"标注为**历史状态**，保留其设计意图作为验收依据；
> 答辩版重绘时按此清单逐条核对。

## fig1_architecture.png（论文第一图）【已渲染 v1】

- 内容：动态 3DGS-SLAM 流水线（输入→跟踪→建图→致密化→地图，
  渲染反馈虚线）+ 三个研究内容框（观测/估计/表示）各自箭头指向
  流水线对应模块 + 底部动态干扰标注
- 验收：①五个流水线框横排等距 ②三内容框颜色可区分（蓝/紫/绿）
  ③箭头无交叉混乱 ④中文无方框（Noto 字体）⑤图题"图 1.1"
- 已知风险：v1 用 matplotlib 画的框图美观度一般，答辩版建议
  用 draw.io/PPT 重绘

## fig4_ladder_pt1.png【已渲染 v1】

- 内容：pt1 修复阶梯 12 臂柱状图（基线灰/失败红/通过蓝/最优绿）
  + 5cm 目标红线 + 柱顶数值标签
- 验收：①12 根柱子顺序=时间序（R1→R12）②颜色语义一致 ③目标线
  与图例不重叠 ④数值可读
- 数据源：ladder_per_seed.csv.md（mean 列）

## fig4_drift_curves.png【已渲染 v1】

- 内容：R2/R6/R9 三条逐帧 APE 曲线 + 事件窗口（221-246）红色底纹
- 验收：①三条曲线颜色与图例对应 ②事件窗口标注可读 ③y 轴范围
  不裁剪曲线峰值 ④seed0 口径标注在标题
- 数据源：r2_hardtrack_seed0 / r6_combo_seed0 / r9_swba_pt1_seed0
  的 per_frame_ape.csv

## fig4_swba_mechanism（待画）

- 内容：SWBA 机制示意——时间轴上 KF 序列，最近 2 个 free（空心）
  + 4 个 anchor（实心锁），稠密窗口边（free-自由连 + anchor 连），
  修正回灌箭头指向下一帧 tracking
- 关键视觉点：①锚与自由的区别（锁图标/颜色）②回灌箭头是本图
  灵魂（区别于后处理的点）③与 R4（无回灌）的对照小图可选

## fig3_2_signal_pipeline（待画，重绘自论文 Fig.2）

- 内容：f_obs 与 f_static 两条流 → 分歧 → MAD 归一化 → e_flow
  → 与 g 合成 s → Cauchy 权重 w_rel → 两个消费点（跟踪残差/
  生命周期确认）
- 关键视觉点：权重下界 max(w,0.10) 必须显式标出（论文核心主张）

## fig2_1_taxonomy（待画）

- 内容：anti/face-dynamic 分类树，两支各列代表方法（2.3 节的
  10+ 篇），本文 RoGS-SLAM 高亮在几何/运动一致性档
