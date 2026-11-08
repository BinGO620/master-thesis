# 术语表

同一概念全文只用一种译法。新术语先加到这里再用，避免同一篇论文里
「动态物体」「运动目标」「移动对象」混着写。

## 核心术语

| 英文 | 中文 | 说明 |
|---|---|---|
| SLAM | 同时定位与地图构建 | 首次出现给全称，之后用 SLAM |
| 3D Gaussian Splatting (3DGS) | 三维高斯泼溅 | 首次给全称 |
| Gaussian map | 高斯地图 | 指 SLAM 运行时或运行后存下来的那个高斯表示 |
| Dynamic scene | 动态场景 | 不写「动态环境」，全文统一 |
| Rigid scene flow | 刚性场景流 | 与「观测光流」相对 |
| Optical flow | 光流 | |
| Reliability weight | 可靠性权重 | 不写「可信度权重」 |
| Keyframe | 关键帧 | |
| Tracking | 跟踪 | 与 localization 区分：localization 译「定位」 |
| Mapping | 建图 | 不写「地图构建」（首次全称里已用） |
| Densification | 致密化 | |
| Pruning | 剪枝 | |
| Primitive | 基元 | 高斯地图中的单个高斯；章内不写「点」「高斯」（可数单个体时） |
| Densification dose | 剂量 | 梯度阈值决定的单轮致密化新增量，2026-11-08 ch5 用 |
| Churn (turnover ratio) | 周转率 | 剪枝删除量与致密化新增量之比，2026-11-08 ch5 用 |
| Clone / split | 克隆 / 分裂 | 致密化算子，章内用中文 |
| Lifecycle | 生命周期 | 指高斯的产生与删除过程 |
| Pose | 位姿 | |
| Trajectory | 轨迹 | |
| ATE (Absolute Trajectory Error) | 绝对轨迹误差 | |
| RPE (Relative Pose Error) | 相对位姿误差 | |
| Ablation | 消融 | |
| Baseline | 基线 | 不写「基准」，基准指 benchmark |
| Benchmark | 基准 / 评测集 | 看语境 |
| Protocol | 协议 | 指实验协议 |
| Seed | 随机种子 | |
| Run | 跑批 / 一次运行 | |
| Regime | 场景类型 / 情形 | ⚠ 这个词的中文不好定，见下 |

## 需要留意的几个

**Regime。** 小论文里指「场景的难易类型」，如纯物体、混合移动体、人群。
直接译「机制」是错的（那是 mechanism）。译「场景类型」或「情形」都可，
但全文只能选一个。暂定「场景类型」。

**Mask-free。** 小论文的核心卖点之一，「不使用语义分割掩码」。
译「无掩码」或「不依赖语义掩码」。暂定「无掩码」，首次出现时加一句解释。

**Bundle / Combined configuration。** 指把几个组件组合在一起的配置。
译「组合配置」。

## 机构与数据集

| 英文 | 写法 |
|---|---|
| BONN RGB-D Dynamic | BONN 动态数据集 |
| TUM RGB-D | TUM RGB-D 数据集 |
| Replica | Replica 数据集 |
| MonoGS | 保留英文，指 Matsuki 等的方法与本仓库基座 |
| RoGS-SLAM | 保留英文，指本人第一篇小论文的方法 |
| RGD-SLAM / SplaTAM / Co-SLAM 等 | 保留英文原名 |
