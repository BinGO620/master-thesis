# Mechanism: ADC regrow tail at code level (MonoGS densify/split/reset)

> 产出：2026-08-07。目的：把「ADC regrow tail」从探测现象升级为**代码级可证伪**机制。
> 归 04-paper-positioning §2.2 待办 B；对应 `our_method/02-method.md` 工作包「WP-T 机制」。
> 全部基于 `gaussian_splatting/scene/gaussian_model.py` + `utils/slam_backend.py` 的实际代码
> （行号 2026-08-07 ours-v3 快照）。未被改动的核心代码是项目唯一不可动的实体。

---

## 0. 要证明的结论（可证伪的机制主张）—— ⚠ 2026-08-08 重写版（取代下方 REWORK 段；原 ADC 归因已证伪撤回）

> **MonoGS 的标准最终 color-refinement（26000-iter 纯光度优化、opacity 活、无 prune/densify/reset）
> 通过把贡献趋零的 floaters 软抑制到 sigmoid(opacity)<0.01，制造一批可复现的"软选择队列"，这批
> 高斯在终图 `final_after_opt` 里占 9–16%、在 volume rendering 里光学贡献 <1%（theory.md 上界），
> 可被终图一次性删除且 |dPSNR|≤0.0001 dB。**该软选择对 refine 质量有正面作用（不是缺陷）**。**
>
> 反事实（`p3_terminal_refine_freeze_result.md`）：refinement 期间冻结 opacity ⇒ 尾巴 12.8%→3.7%
> （机制验证：尾巴确为 refine 的 opacity DOF 制造）。但冻结后 PSNR −0.53dB、N 涨 35%（关联合参数
> 补偿）⇒ **软选择有正面贡献，"refine-aware 省参"贡献不成立**，不省 compute、不做在线压缩。

> 原 §1–§5 的 ADC-regrow 归因版本已于 2026-08-07 证伪（`p3_terminal_mech_autopsy.md`），
> 不再作为论文机制主张。以下保留代码事实链（它们在机制解释 §3.4 里仍有用），但**删去"ADC 稳态
> 生成模型"作为归因**。

---

## 1. 代码事实链（逐条）

### 1.1 新高斯的默认 opacity = sigmoid(0.4–0.5) 附近，而不是高不透明

初始来自深度图的高斯：`opacities = inverse_sigmoid(0.5 * ones)`（`gaussian_model.py:477`）
⇒ 出生在 sigmoid=0.5。密度/候选插入路径复用同一 `_gaussians_from_points`
（`:410-478`），也是 `inverse_sigmoid(0.5)`。

**含义**：对「新插入即低 op 后代」的链的起点，所有新生的高斯都从 0.5 开始，**不会**一出生
就是高不透明。opacity 只能靠后续优化步（Adam 更新 logit）向上或向下漂移。

### 1.2 clone/split 的 opacity 是 `self._opacity[...].repeat`——直接继承父代，不重置

- `densify_and_clone`（`:1337-1375`）：`new_opacities = self._opacity[selected_pts_mask]`（`:1351`），
  然后 `densification_postfix(...)`。**后代 = 父代的 logit 逐字复制**。
- `densify_and_split`（`:1274-1335`）：`new_opacity = self._opacity[selected_pts_mask].repeat(N,1)`
  （`:1303`），`new_scaling` 会被 `scaling_inverse_activation(scale/(0.8*N))` 缩小（`:1297-1299`），
  但 **opacity 没有任何 rescale**。

**含义（关键）**：如果一个父代是低 opacity（无论为何低），clone 出来的后代继承同一个低
logit。Densify 的判据是梯度 `grad >= densify_grad_threshold`（`:1279` for clone、`:1340` for split）
——**它不是 opacity 判据**。所以一个「低 opacity 但高梯度（正在被优化）」的高斯会不断被
复制成更多低 opacity 后代。

### 1.3 每轮 densify 后唯一的二次删减 = `prune_mask = get_opacity < min_opacity`

`densify_and_prune`（`:1377-1392`）：

```
grads = xyz_gradient_accum / denom
densify_and_clone(grads, max_grad, extent)   # 先 clone
densify_and_split(grads, max_grad, extent)   # 再 split
prune_mask = (self.get_opacity < min_opacity).squeeze()
...
self.prune_points(prune_mask)
```

这里 `min_opacity` = 配置里的 `gaussian_th = 0.7`（TUM base `:293`;对应运行映射的
`Training.gaussian_th`）。所以在**同一轮**内，`op<0.7` 的高斯会被 `prune_points` 删掉。

**但这是「下一轮之前」的删减**。新的低 opacity 后代在下一次 densify 被删掉之前，**已经作为活
高斯参与了这一轮及后续的渲染/梯度**，而且 `prune_mask` 对**当前时刻**的 opacity 求值——
新 clone 的 opacity 在它还没被足够梯度向上推之前,可能低于 0.7 被当轮删。这不矛盾，需要我们
精确说明 tail 的来源，见 §2。

### 1.4 opacity reset 只在极稀疏点触发，且是全局集合

映射主循环 `utils/slam_backend.py:497-510`：

```
update_gaussian = (iteration_count % gaussian_update_every == gaussian_update_offset)
if update_gaussian:
    gaussians.densify_and_prune(densify_grad_threshold, gaussian_th, gaussian_extent, size_threshold)
    gaussian_split = True
## Opacity reset
if (iteration_count % gaussian_reset) == 0 and (not update_gaussian):
    gaussians.reset_opacity_nonvisible(visibility_filter_acm)   # :510
    gaussian_split = True
```

- `gaussian_update_every = 150`, offset 50（`base_config.yaml:291-292`）⇒ 每 150 迭代一次 densify
  （`iteration % 150 == 50` 时触发）。
- `gaussian_reset = 2001`（`:295`），且 `not update_gaussian` 条件确保它与 densify 不在同一迭代。
  2001 % 150 = 51 ≠ 50 ⇒ 不与 densify 重合。实际触发迭代：2001, 4002, 6003, 8004, 10005, 12006, …
  （每 2001 迭代一次，相当于每 ~13.3 个 densify 轮才触发一次 reset）。

  `reset_opacity`（全量置 0.01）只在 init 阶段 `init_gaussian_reset = 500` 或 `opt_params.densify_from_iter = 500`
  时，于首帧初始化早期调用（`slam_backend.py:221-224`）。mapping 阶段的 reset 是 `reset_opacity_nonvisible`
  （`:758-766`）：把**所有非可见**高斯的 sigmoid 置 0.4（`inverse_sigmoid(0.4)`），**可见的保持不变**。

**含义**：opacity 的重置机制只把「这一轮不可见」的高斯压回 0.4，把「可见」的保留。它**不会**
在密集 tail（能碰到的低 op 高斯往往恰好「可见」或不在 reset 时的 visibility 集合里）上产生
全局归一。尾部低 opacity 一旦形成，Reset 机制既不把它拉起来、也不会特意删它。

### 1.5 二次稠密删减在调用链上的频率

主循环里 `densify_and_prune` 每 150 迭代一次。在这个频率上，`prune_mask = op<0.7` 会删掉
「当下 op 仍 <0.7」的高斯。**若一个低 op 后代在被下一轮 prune 前**通过足够梯度被推到 op≥0.7，
就不会被当轮删；反之会被删。T 世代之后，存活的低 op 高斯要么是「刚在一次 prune 后新建还没被
下次 prune 碰到」的周期尾部产物，要么是「梯度把它推到 ≥0.7 之后又优化回 <0.01」的振荡残留。
两类合在一起，构成稳态的 `op<0.01` tail。

---

## 2. （原 ADC 稳态生成模型 —— 已证伪撤回，仅供历史，不作为论文主张）

> ⚠ 2026-08-08 裁决：本节原"稳态 tail"生成模型（随 densify 频率×复制量单调放大）是**在线 ADC
> 归因**，已被 `p3_terminal_mech_autopsy.md` 证伪（tail 不是在线稳态）。对应预测实验（任务 C
> densify 阈值）的 FALSIFIED 结果见 `p3_densify_tail_batch1_stopped_mech.md`。保留此节仅为记录
> 推理路径，**论文机制主张一律以 §0/§5 定稿版（color-refinement 软抑制）为准**。

设每个 densify 轮 $t$ 后插入 $K_t$ 个后代（`clone`+`split` 各产生），它们出生的 opacity logit
$= \mathrm{op}_{\mathrm{init}}$（通常 $\ge 0.5$，但 clone 的父代可能是任意值）。设优化在下一轮
$t{+}\Delta$ 前给每个新后代的 logit 以随机游走。**只要存在**：

1. 一个「父代低 op 且梯度高」的复制源（§1.2），或
2. 一个「新后代在下轮 prune 前优化不足」的窗口（§1.3），

那么每一轮 $t$ 都会**重新生成**一批 `op<0.01` 的高斯。这是因为：
- 生成判据是 `grad >= th`（§1.2），不是 opacity；
- 删除判据是 `op < 0.7`（§1.3），在下一轮才评估；
- opacity reset 不作用于这个窗口（§1.4）。

**预测（可证伪）**：tail 宽度（即 `op<0.01` 占比）应当随「densify 频率 × 每轮复制量」单调放大。
这正是任务 C 的预测性实验要测的：把 `densify_grad_threshold` 降低（更多 clone），tail 应变宽；
升高则变窄。

> 这不是「事后拟合」机制，而是从代码的控制流推出的、**可被 A/B（densify 阈值）实测检验**
> 的因果链。若 A/B 不沿此方向移动，则该机制主张被证伪。

---

## 3. 已有的直接观测（探测证据，吻合代码机构）

`R3-P05-map-compression-step5b-terminal-3seed.md` 的机制探针：

| seq | base frac_op<0.05 | compress-seed0 frac_op<0.05 |
|---|---|---|
| balloon | ~0.25 | 0.175 |
| mv_no_box | ~0.14 | 0.149 |
| pt1 | ~0.13 | 0.122 |

**压缩后终图仍 ~12-17.5% 低 opacity**。这与 §2 的生成模型完全吻合：在线/终端删除唤起的
`_prune_raw` 只删当前存量，但**存量是由 ADC 稳态流持续再生的**；删掉一批，密集轮会再填一批。
这就是「ADC regrow loop」的代码级解释——不是「管不住」，而是「生成频率 > 删除后到终点的
重新累积」。

---

## 4. 一张表把机制与理论、预测串起来

| 层 | 内容 | 输出 |
|---|---|---|
| 理论（`papers/mmm/theory.md`） | volume rendering 公式：op<0.01 ⇒ 权重<1%、遮挡<1%、整批扰动有界 | 「0 代价」= 严格数学上界 |
| 机制（本文） | 代码控制流：densify 生成判据=梯度、删除判据=op<0.7、reset 稀疏且只对不可见 | 为何稳态 tail 存在 |
| 预测（任务 C） | densify 阈值 ↓ ⇒ tail ↑、可删 ∝ ↑；阈值 ↑ ⇒ tail ↓ | 把机制从描述变可测 |

**终态论文主张（重写后，2026-08-08）：**
> 动态 3DGS SLAM 终图的 `op<0.01` tail 是 **color-refinement 的 opacity 软抑制**产物，不是
> ADC 在线稳态（在线 `final` 图 `<0.01`≈0.69%，refinement 后 `final_after_opt` 才到 10.4%）。
> 这批软选择出的近零贡献高斯可被终图一次性删除零代价（12/12 run，|dPSNR|≤0.0001dB），且
> matched-rate 控制证明该队列**专一安全**（同数量随机/高 opacity 删除损失 0.4–3.8dB）。
> 软选择对 refine 质量有正面作用（frozen-opacity −0.53dB）——不省 compute、不做在线压缩，
> 只做**存储/传输层面的 byte 减量**。

---

## 5. 结论（可写进论文）—— 2026-08-08 REWORK 定稿：机制 = color-refinement 软抑制，非 ADC

本文 §1-§4 的"ADC regrow 产生稳态 tail"主张已被 `final`(在线) vs `final_after_opt`(refinement 后)
PLY 直接比对（P2-T 36 run + P3-DENSIFY-TAIL 10 run）**证伪**（`p3_terminal_mech_autopsy.md`）：
- 在线 `final` 图 `<0.01` 均值仅 0.69%，几乎无极端低 opacity 尾巴；
- refinement 后 `final_after_opt` 才到 10.4%（36/36 增长，均 +9.7pp）；
- 归因在 **color-refinement 的 soft-suppression**：26000-iter 纯光度优化、opacity 活、无
  prune/densify/reset（`TriReliability.enabled=false` ⇒ 不冻结）。

**定稿机制主张**（skeleton §3.4 引用）：
1. `final_after_opt` 里确有 9-16% `op<0.01` 高斯，删掉它们 |dPSNR|≤0.0001dB（12/12）——可复现
   零代价压实观测。
2. 该批次是 **color-refinement 压到近零 opacity、集合上光学贡献≈0 的高斯**（软抑制集），
   删掉不损失；且**专一安全**（matched-rate 控制：同数量随机/高 opacity 删损失 0.4–3.8dB）。
3. `theory.md` 上界对「任何 `op<0.01` 高斯在 volume rendering 中贡献<1%」无条件成立
   （不依赖 tail 来源）。
4. **软选择对 refine 质量有正面作用**（frozen-opacity 反事实：尾巴 12.8%→3.7% 但 PSNR −0.53dB、
   N+35%）。
5. **不省 compute**：不做在线压缩、不把 compression 当"修复 refine 缺陷"。终端删除只是把
   软选择结果固化成存储/传输的 byte 减量（6–11%）。

**已不成立（撤回）**：「tail 是 ADC densify 梯度判据+继承 opacity+稀疏 reset 的稳态产物」。
**已验证（frozen-opacity 反事实，1 run）**：尾巴确由 refine 软抑制制造，但软选择有用（分支③
关联合参数补偿，非①defective loop）。

> 代码事实源（在线 densify/reset 路径本身数据未动）：`gaussian_model.py`（get_opacity:151-152、
> _gaussians_from_points:477-478、densify_and_clone:1337-1375、densify_and_split:1274-1335、
> densify_and_prune:1377-1392、reset_opacity*:753-790）；`slam_backend.py` init:213-224，mapping:492-511。
> color-refinement：`slam_backend.py:826-908`（26000 iters，纯光度，无 prune/densify/reset）。
> 配置默认：`configs/rgbd/tum/base_config.yaml`（gaussian_update_every=150、offset=50、gaussian_reset=2001、
> gaussian_th=0.7、densify_grad_threshold=0.0002、color_refinement_iterations=26000、opacity_lr=0.05）。
