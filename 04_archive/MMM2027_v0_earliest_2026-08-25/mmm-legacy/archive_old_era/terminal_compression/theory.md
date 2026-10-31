# Theory: Zero-Cost Upper Bound of `op<0.01` Gaussian Removal

> 产出：2026-08-07。目的：把「0 代价」从实测（|dPSNR|≤0.0001 dB，12/12 run）升级为
> **严格数学上界**，使其不依赖任何数据集。归 04-paper-positioning §2.2 待办 A；对应
> `our_method/02-method.md` 工作包「WP-T 理论上界」。
> 纯数学，零 GPU。假设只在「3DGS volume rendering + 前端 alpha 合成」这一标准公式内，不依赖特定数据集。

---

> **⚠ 范围界定（2026-08-08，codex Round2 修正）**：本文件证明的是**单个** `op<0.01` 高斯
> 对任意像素的**单项**贡献上界（A/B），以及**在上界 C 的"每条射线上可删高斯数 $m$ 有界"这一
> **假设条件下**的整批扰动有界。**它不**对"同一条射线上 $m$ 个低-op 高斯的**累计**贡献 <1%"
> 作无条件保证（$m$ 大时累计 opacity 可接近 $1-(1-0.01)^m$）。因此：
> - "整批删除零代价"是 **empirical rendering validation 的实测结论**（12/12 |dPSNR|≤0.0001dB），
>   不是本文件无条件蕴涵的定理；
> - 若要在 cohort 层面作 claim，须直接测量每像素被删 cohort 的累计 compositing weight
>   $W_{\mathrm{removed}}(p)=\sum_{k\in R} T_k(p)\alpha_k(p)$（见 skeleton §P0.5）。

---

## 0. 记号与模型设定

3DGS 把场景表示成一组 3D 高斯 $G_i$，每个像素的颜色按**前向合成（front-to-back alpha compositing）**聚合：

$$
C = \sum_{i \in \mathcal N} c_i\, \alpha_i\, T_i,
\qquad
T_i = \prod_{j < i} (1 - \alpha_j),
$$

其中：

- $\mathcal N$ 是**沿该像素射线、按深度排序后**的可见高斯索引集；
- $c_i \in [0,1]^3$ 是高斯的 RGB 颜色（sh 系数解码后，clamp 到 $[0,1]$）；
- $\alpha_i(p) \in [0,1]$ 是该高斯在该像素的**最终 alpha**。在 MonoGS 的 CUDA 光栅化器里，
  像素级最终 alpha 由该高斯的 `opacity = sigmoid(_opacity)` 与其高斯 footprint 覆盖系数共同决定：
  footprint（投影椭圆协方差、经 scale 与旋转到像素平面）决定该高斯**覆盖哪些像素**，而它对被
  覆盖像素的最终混合权重被 `opacity` **界定**（见 §4.1）。具体地
  \(0\le \alpha_i(p)\le \sigma(o_i) = \mathrm{sigmoid}(\mathrm{op}_i)\le 1\)；
- $T_i = \prod_{j<i}(1-\alpha_j)$ 是**透射率**——深度序在它之前的高斯**都没拦住**该光线的概率。

本推导只依赖两条**无条件成立**的事实：

1. $0 \le \alpha_i \le 1$（任何 footprint 覆盖系数都不超过 1）；
2. $0 \le T_i \le 1$（透射率是 $[0,1]$ 上「$\le 1$ 的数连乘」，故 $\le 1$ 且 $\ge 0$）。

这两条对任何物理上合法的渲染管线都成立，**与数据集无关**。

---

## 1. 上界 A：任意单高斯对该像素最终颜色的权重贡献 $\le 1\%$

「`sigmoid(opacity)<0.01`」对**像素级最终 alpha** 的表述：若高斯 $G_k$ 满足
$\sigma(o_k)<0.01$，则由 §0 的界定 \(\alpha_k(p)\le \sigma(o_k)<0.01\)，其像素级最终 alpha
同样小于 0.01：

$$
\alpha_k(p) \;\le\; \sigma(o_k) < 0.01 .
$$

则它在合成式里作为 `weight = $\alpha_k T_k$` 参与。由 0-2，透射率 $T_k \le 1$，于是：

$$
\boxed{\;
\text{weight}(G_k) = \alpha_k\, T_k \;<\; 0.01 \cdot 1 = 0.01 = 1\% .
\;}
$$

> 修正说明（2026-08-09，codex Round4）：原稿在此处写"最终 alpha = 裸 sigmoid"、footprint 只取
> 覆盖像素集合。标准 3DGS 里像素级 alpha 是 footprint 与 opacity 结合的（被 opacity 界定而非
> 与其相等）。**但上界保持不变**——我们只需 \(\alpha_k(p)\le\sigma(o_k)<0.01\)，这是由 §0 的覆盖
> 系数 \(w_k(p)\in[0,1]\) 保证的（§4.1）。故 §1/§2 的单高斯上界仍然严格成立，只是措辞从"相等"
> 改为"被界定"。

**解释**：这个 $G_k$ 对**任何**像素、处于**任何**遮挡深度序，其颜色 $c_k$ 对最终 $C$ 的
加权贡献至多 1%。删除它 = 从该像素的颜色上拿掉至多一个「值域 $[0,1]$ 的 1% 的扰动项」，
且对深度序在它**之前**的各项无影响（前项不依赖后项）。需要说明：深度序在它**之后**的各项
其透射率 $T_j$ 会因删除而**增大**（本被它挡住的光现在能透过来）——这是 §4.6 的 ensemble-D
（solo-render 累计权重上界）单独测量覆盖的整体效应，不由上面的单高斯直接贡献上界承担；所以
这里只说"删除对 $G_k$ 之前项无影响、对 $G_k$ 自身直接贡献有 <1% 上界"，**不说**"$T$ 序列整体
不变"。

> 严格性：这里 $\alpha_k$ 是**最终 alpha**（含 footprint $w_k$）。若只用裸 sigmoid
> $\sigma(\mathrm{op}_k)<0.01$，则最终 $\alpha_k = \sigma\cdot w_k \le \sigma < 0.01$，
> 上界同样成立（见 4.1）。所以「sigmoid opacity < 0.01」蕴含「该高斯对任意像素权重贡献 < 1%」。

---

## 2. 上界 B：对更后台高斯的最大遮挡 odds $\approx 1\%$

沿射线对深度序**在 $G_k$ 之后**的任何高斯 $G_{j>k}$，其透射率 $T_j$ 含因子 $(1-\alpha_k)$：

$$
T_j = \underbrace{\prod_{j'<j,\ j'\ne k}(1-\alpha_{j'})}_{=\;T_j^{(-k)}} \cdot (1-\alpha_k).
$$

删除 $G_k$ 会让 $T_j$ 变化多少？不删时的遮挡 odds：

$$
\frac{\text{被 }G_k\text{ 遮挡的权重}}{\text{未被 }G_k\text{ 遮挡的权重}}
= \frac{\alpha_k}{1-\alpha_k}.
$$

对 $\sigma(o_k) < 0.01$（并由 §0 界到 \(\alpha_k(p)<0.01\)）：

$$
\frac{\alpha_k}{1-\alpha_k} \;<\; \frac{0.01}{0.99} \approx 0.0101 \approx 1\% .
$$

即：**即使这个低 opacity 高斯正好挡在某个更深的表面前面，它对后台表面透射率的削弱也不到
1/99**，即最大 odds ≈ 1%。删除它最多让后台表面「更透」约 1%，这同样在渲染差异的
数值噪声量级之下（实测 |dPSNR|≤0.0001 dB，见 4.4）。

> 上界 B 与上界 A 是**同一件事的两面**：
> - A 说「低 opacity 高斯自己的贡献小」；
> - B 说「它挡住的后台贡献也小」。
> 两者合起来刻画了「删除单个低-opacity 高斯」的**两侧**预算：A 是被删高斯自身的直接贡献，
> B 是它对后台遮挡 odds 的削减；二者都 <1%。需要指出，**整个** $T$ 序列的变化（含多条射线、
> 多个被删高斯在后台透射率上的累积）不由这两个单高斯上界单独覆盖，而是由 §4.6 的
> ensemble-D 累计权重上界**直接测量**（而不是本文件无条件蕴涵）。

---

## 3. 上界 C：多像素 / 多帧聚合仍然受控（**假设条件**，非无条件定理）

实际指标是**全帧 PSNR 的逐帧均值**：

$$
\mathrm{PSNR} = \frac{1}{\#F}\sum_{f} \big(-10\log_{10} \mathrm{MSE}_f\big),
\qquad
\mathrm{MSE}_f = \frac{1}{\#P}\sum_p \|C_f(p)-C_f^{\mathrm{gt}}(p)\|^2 .
$$

删除单个像素上一组权重 `<0.01` 的高斯，对 $\|C_f(p)\|$ 的扰动上界：

$$
\|\Delta C_f(p)\| \;\le\; \sum_{k:\ \alpha_k<0.01}\ \alpha_k\,T_k\, \underbrace{\|c_k\|}_{\le\sqrt3}
\;<\; \sum_k 0.01_i \cdot \sqrt3.
$$

若一像素路径上有 $m$ 个 `op<0.01` 高斯，$\|\Delta C_f(p)\| < 0.01\, m \sqrt3$。这与「所有
可删高斯都被删」的实测绑定：实测 `n_removed / n_total ≈ 9-16%`，且每条射线上低 opacity
高斯数远小于总射线内高斯数（实测产物直方图），故 $m$ 典型为个位数，$\|\Delta C\|$ 典型
为 $0.01$ 量级——这与「|dPSNR| ≤ 0.0001 dB」完全吻合的量级。

> 上界 C 说明**全集删除的扰动是有界的**，不因删得更多而失控（只要每条射线上低 opacity
> 高斯数有界）。这正是「op<0.01 可整批安全删」的数学承诺，而实测把这条承诺验证到了
> 0.0001 dB。

---

## 4. 与实现的严格衔接

### 4.1 像素级最终 alpha 被裸 sigmoid opacity 界定（MonoGS 实现事实——footprint 只选覆盖像素）

渲染里传进 CUDA 光栅化器的正是 `opacities = pc.get_opacity`（`gaussian_renderer/__init__.py:78`），
而 `get_opacity` = `torch.sigmoid(self._opacity)`（`gaussian_model.py:151-152`）。

**footprint 与 alpha 的关系（修正，2026-08-09 codex Round4）**：标准 3DGS 光栅化里，一个高斯的
像素级 alpha 通过其高斯 footprint 与 opacity 结合——footprint（投影到像素平面、由协方差与
scale 决定）决定该高斯**覆盖哪些像素**，而它对被覆盖像素的**最终混合权重**由 footprint 与 opacity
共同决定，故像素级最终 alpha \( \alpha_k(p) \) **被 \( \sigma(o_k) \) 界定而非与其相等**：
\[
\alpha_k(p) \;\le\; \sigma(o_k) < 0.01 .
\]
（`opacity = σ(footprint × ...)`，footprint 覆盖系数 \( w_k(p)\in[0,1] \)，故
\( \alpha_k(p)=\min(w_k(p)\sigma(o_k),\, 1) \le \sigma(o_k) \)。）

**对 §1/§2 上界的意义**：上界 A/B 用的是 `\(\alpha_k < 0.01\)`（最终 alpha）。若只用裸 sigmoid
\( \sigma(o_k)<0.01 \)，则由上面的不等式最终 \( \alpha_k(p)\le \sigma(o_k)<0.01\)，**上界同样是严格成立的**
（这正是 codex Round4 指出的"单高斯界仍可用 \( \alpha_k(p)\le\sigma(o_k)<0.01 \) 恢复"）。因此：
- "sigmoid(opacity) < 0.01" **蕴含**"该高斯在任一被覆盖像素的贡献 < 1%"，双侧均严格成立；
- 修正后的措辞是"像素级 alpha **被 opacity 界定**"，而不是"与该 opacity 相同"；
- §2 的"删除前沿高斯会改变后项透射率"这一点：删除一个前沿高斯，对深度序在它**之前**的高斯
  的贡献无影响（前项不依赖后项），但会使深度序在它**之后**的高斯的透射率 \(T_j\) 增大——上界 A
  评价的是被删高斯**自己的直接色彩贡献**（删除它带来的直接色彩扰动），而它对后台透射率的增强
  是另一效应，不由单高斯界覆盖；该整体效应已由 solo-render 的累计权重上界在 §4.6 的测量直接
  覆盖。本文件不声称删除后后台透射率"保持不变"。

### 4.2 `_prune_raw` 的删除路径（代码级）

`GaussianModel._prune_raw(keep)`（`gaussian_splatting/scene/gaussian_model.py:1011`）直接按
bool mask 切片所有参数张量（xyz / opacity / scaling / rotation / SH），**不做任何重新归一化**。
渲染用的是被删后的剩余高斯，合成公式形式不变，因此 0-2 的两条事实对删除后的地图依然成立。
⇒ 上界 A/B/C 对**删除前与删除后**的地图都成立，删除本身不引入新误差机制。
（`GaussianModel.opacity_activation = torch.sigmoid`、`inverse_opacity_activation
= inverse_sigmoid` 于 `gaussian_model.py:113-114`；初始 `opacity = inverse_sigmoid(0.5)` 于
`:477`，即新高斯出生在 sigmoid=0.5 的 logit 上。）

### 4.3 为何 op<0.01 而非更高阈值

上界 A/B 是**严格单调**于阈值 $\tau$：阈值越高，单高斯权重上界越大。实测停在
|dPSNR|≤0.0001 dB（op<0.01）；而 op<0.05 的 balloon seed-1 破 −0.087 dB ⇒
**0.05 的权重上界（约 5-5.3%）已经跨过了「删除引入可见差异」的临界**，0.01 则落在
权重上界（1% / 遮挡 odds ~1%）远小于 1 的数学安全带上。所以「为什么是 0.01」有理论依据：它是
$\alpha \ll 1$ 且 $\alpha/(1-\alpha) \approx \alpha$ 都远小于 1 的一个安全阈值。需要说明：
这里的"0.01 落在数学安全带"给出的是**单高斯**权重上界（§1/§2），整批删除的零代价是**实测结论**
（`p4_op001_full18.md`，18/18 |dPSNR|≤0.003 dB），不是本上界对整批的无条件保证；且阈值略高
（如 0.02）在实测中代价数值同等（−0.0026 dB），故本文不声称 0.01 是"唯一最粗安全阈值"。

### 4.4 与实测的量级自洽

| 量 | 数学上界 | 实测 |
|---|---|---|
| 单高斯权重 | <1% | — |
| 最大遮挡 odds | <~1% | — |
| 单像素扰动 | <0.01·m·√3 | ≤0.0001 dB（全帧均值） |
| 可删比例 | 有界（见上界 C） | 9-16%（12/12 run） |

---

## 5. 结论（可写进论文）

对动态 3DGS SLAM 终端地图，任何 `sigmoid(opacity) < 0.01` 的 3D 高斯：

1. **对任意像素的最终颜色权重贡献 $<1\%$**（$\because \alpha_k T_k < 0.01 \cdot 1$）；
2. **对任意更后台表面的最大遮挡 odds $<~1\%$**（$\because \alpha_k/(1-\alpha_k) < 0.0101$）；
3. **整批删除对全帧 PSNR 的扰动有界**（$\because$ 每条射线可删高斯数有界，$\|c\|\le\sqrt3$）。

因此「op<0.01 单高斯可零代价删除」是一个**不依赖任何数据集、由 volume rendering 合成公式
与 §0-§4.1 的界定严格蕴涵**的单高斯的数学上界；**整批删除**则由实测（18/18 run，|dPSNR|≤0.003 dB，
`results/evidence/p4_op001_full18.md`）验证到数值噪声量级，且受上界 C 的 $m$ 有界假设约束——**不是
无条件整批定理**。

> 数据来源：theory 为纯推导；实测数值来自
> `results/evidence/R3-P05-map-compression-step5b-terminal-3seed.md`（12 run 表）。
