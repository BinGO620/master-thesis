# 02_analysis/ — 论文图表生成（分析过程，非论文产物）

职责：读取 monogs-ours/results 的实验输出，生成论文用图表的**脚本与配置**。
论文最终引用的图表在 ../03_results/（产物，进 git）；本目录是生成过程。

## 布局

- `scripts/figures/` — 一个图一个脚本（可复现；数据源用绝对路径或
  环境变量 `MONOGS_RESULTS` 指向 monogs-ours/results，**不复制数据**）
- `configs/` — 路径、实验筛选、图表样式配置
- `intermediate/` — 可再生的中间汇总 CSV/JSON（默认不提交，已 gitignore）

## 依赖

- python3 + matplotlib（实验仓库 conda env: /data/conda_envs/monogs-ours）
- 数据源路径默认 /data/monogs-ours/results

## 复现

```bash
# 图（输出到 03_results/figures/）
cd 02_analysis/scripts/figures
python3 fig_ladder.py            # 图 4.1 修复阶梯
python3 fig_drift_curves.py      # 图 4.3 漂移曲线
python3 fig4_swba_mechanism.py   # 图 4.2 机制示意
python3 fig1_architecture.py     # 图 1.1 总架构
python3 fig2_1_paradigm_timeline.py
python3 fig2_3_taxonomy.py
python3 fig5_ablation_bars.py

# 表格数字核实（58 项，改动任何表后必跑）
python3 02_analysis/scripts/verify_tables.py
```
