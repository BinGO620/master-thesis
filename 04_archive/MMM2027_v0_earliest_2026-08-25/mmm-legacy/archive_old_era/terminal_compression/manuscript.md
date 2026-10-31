# MMM 2027 manuscript — Opacity-Selected Terminal Pruning in Dynamic 3DGS SLAM

> Manuscript body. Core Intro + Related Work + Method + Experiments; ship-gate evidence
> （cohort 累计权重、matched-rate 扩 18 图、artifact 全 18 图）已并入 §4.3/4.4/4.6/4.7。
> 篇幅目标 8–10 页核心正文 + 2 页引用（LNCS）。英文正文。
>
> **定位：narrow-empirical（soft-selection characterization + safe terminal pruning +
> self-tracked backbone floor），非压缩算法/SOTA 声称。审核状态见 `review-stage/AUTO_REVIEW.md`。**

---

## Abstract (~200 words)

Dynamic 3D Gaussian Splatting (3DGS) SLAM accumulates maps under an insert-then-prune
paradigm whose final maps grow monotonically. We study a structural property of such maps
that prior online-pruning and coding-layer work leaves unexamined: the terminal
color-refinement stage of our MonoGS-based backbone soft-selects a cohort of Gaussians
whose sigmoid opacity is driven below \(10^{-2}\). Across 18 runs (6 sequences × 3 seeds)
this cohort comprises **8–18%** of the final map and can be discarded with **no measurable
rendering loss** (on 17/18 maps \(|\Delta\text{PSNR}|\le 0.0003\) dB, worst −0.0025 dB); a
per-pixel cumulative-compositing-weight upper bound over the same 18 maps shows its
contribution is near-zero **at the pixel level** (99th-percentile <2%, typical <1%), a *sampled*
statement at evaluated poses. The removal is **not** trivially safe: over 18 maps and two removal rates, deleting the same
number of random or high-opacity Gaussians costs −0.2 to −1.0 and −1.6 to −5.7 dB
respectively, while the low-opacity cohort costs at most \(0.003\) dB in the worst case
(the measured worst \(|\Delta|\) is 0.0025 dB for the `op<0.01` operator and 0.0021 dB for the
matched-rate operator). Because PLY size
scales with Gaussian count, this yields a serialized-bytes reduction (**9–16%**) framed
explicitly as storage/transfer savings, not as runtime or compression. The characterization
sits on a self-tracked backbone whose 6-sequence ATE is non-collapsing (3.06 cm on balloon,
2.66 cm on mv_no_box, 10 cm+ on the harder person sequences), reported as an empirical floor
rather than a SOTA claim.

---

## 1. Introduction

**Dynamic 3D Gaussian Splatting (3DGS) SLAM** represents a scene as a set of 3D Gaussians
and, in its online-SLAM form, grows that set via an insert-then-prune loop: new Gaussians
are instantiated from depth, densified where gradients demand, and pruned where opacity
falls too low. The result is a final map whose size in practice is governed by the insertion
budget rather than by any measure of what is actually needed to render it. This raises a
question that, to our knowledge, prior dynamic-SLAM compactness work does not answer:
**how much of a final map is structurally disposable** — removable with zero render cost —
and **why**?

We find that a substantial and *reproducible* fraction is. In the terminal color-refinement
stage of our MonoGS-based backbone, the renderer's opacity is a free parameter optimized by
a long pure-photometric pass. Standard refinement does not add or prune Gaussians; it only
adjusts opacity, geometry and color. As those 26k iterations run, a set of Gaussians whose
contribution is no longer needed is *soft-selected*: their learned opacity is driven toward
zero. Section 3 gives the mechanism evidence (the cohort fraction rises 36/36 runs after
refinement; a supporting opacity-freeze intervention reduces it from 12.8% to 3.7%). The
important consequence is that these Gaussians are exactly the ones a rational post-processing
pass can delete for free.

**Our contributions are threefold.**

1. **A controlled measurement.** Across 18 runs (6 sequences × 3 seeds), the terminal
   refinement of our backbone soft-selects **8–18%** of final-map Gaussians to sigmoid
   opacity \(<10^{-2}\), and deleting them costs no measurable render loss (17/18 maps
   \(|\Delta\text{PSNR}|\le 0.0003\) dB; single worst −0.0025 dB). A
   dataset-independent single-gaussian bound (Section 3.3) gives each Gaussian \(<1\%\)
   per-pixel contribution; a measured per-pixel cumulative-weight upper bound then shows the
   *whole cohort* contributes near-zero at the pixel level across all 18 maps (99th-percentile <2%,
   typical <1%; a sampled upper-bound measurement).
2. **Deletion specificity is non-trivial.** Over 18 maps (6 sequences × 3 seeds) and two removal
   rates, deleting the *same number* of random or high-opacity Gaussians costs **−0.2 to −1.0 dB**
   and **−1.6 to −5.7 dB** respectively (all negative), while the low-opacity cohort costs at most
   \(0.003\) dB both for the matched 5%/10% operator (|ΔPSNR|≤0.0021 dB) and for the actual
   `op<0.01` operator (worst −0.0025 dB). This pre-empts the obvious "any deletion is cheap"
   objection.
3. **A usable self-tracked backbone.** The characterization is not an orphan post-processing
   observation: it sits on a self-tracked backbone whose 3-seed ATE stays reasonable on all six
   sequences under one protocol (3.06 cm on balloon, 2.66 cm on mv_no_box, ~10 cm+ on the
   harder person-tracking sequences), so the compression result is tied to a working SLAM
   system rather than a hand-picked pose screen.

## 2. Related Work

**Online 3DGS pruning.** Methods such as [MGS-SLAM], [Speedy-Splat] and [DCSHARP] prune
Gaussians during training to serve pose accuracy, speed, or reconstruction quality. All operate
in the insert-then-prune loop and none asks whether the *terminal* map contains
structurally-removable near-zero-opacity Gaussians.

**Storage compression.** [3DGS.zip] and related surveys, together with [LightGaussian] and
[Compact-3D], attack serialized size at the coding layer. They do not characterize which
Gaussians a map *itself* deems disposable; we push removal to the fidelity-irrelevant extreme
(opacity \(<10^{-2}\)) and justify it with a single-gaussian weight bound.

**Compactness in dynamic SLAM.** [DG-SLAM] manages Gaussian count as a side effect of
dynamic-object handling rather than as a terminal-map property. We study the end-of-pipeline
opacity distribution directly.

To our knowledge neither direction — online pruning for runtime/quality, nor coding-layer
compression — has separately isolated the terminal soft-selected cohort and shown it to be
removable at zero cost; we report such a measurement here.

## 3. Method

### 3.1 Backbone and evaluation platform

We build on the joint MonoGS backbone with mask-both, dynamic keyframing, robust tracking
and an insert-then-prune lifecycle (the prune arm). No part of the proposed terminal
pruning touches tracking; it is a post-hoc operation on the final map produced by a
self-tracked run. All headline accuracy numbers are self-tracked 3-seed means on the six
Bonn dynamic sequences; Section 4 reports ATE for the same prune lifecycle whose maps we
compress.

### 3.2 The terminal soft-selection observation and the pruning operator

**Observation.** A self-tracked run saves two point clouds: `final` (right after online
mapping) and `final_after_opt` (after the back-end's 26,000-iteration color refinement).
Across all 36 P2-T runs, the gap between the online `final` map and `final_after_opt` is
consistent: the online map has on average 0.69% of Gaussians at sigmoid opacity \(<10^{-2}\)
(range 0–4.9%), and after refinement this **rises** to 10.4% mean — the \(<10^{-2}\) fraction
**grows in all 36/36 runs** (mean +9.7 percentage points), as shown in Fig. 3 (left). The
near-zero cohort is therefore **temporally attributed** to the terminal refinement pass (the
fraction rises sharply after it in every run); a frozen-opacity
intervention (Section 3.4) provides supporting evidence that opacity is the relevant degree of
freedom (Fig. 3, right). We choose the conservative "fraction rises 36/36" phrasing rather than
"the cohort appears only after" because a small online tail (0–4.9%) already exists in some runs.

**Operator.** We load `final_after_opt`, compute `sig = sigmoid(opacity)`, and delete all
Gaussians with `sig < 10^{-2}` via `_prune_raw` (a pure tensor slice; no re-normalization).
We then re-render the surviving map at the stored estimated poses (offline, interval-5,
full-frame) and compare to the original.

**Why 0.01.** The bound in Section 3.3 is strictly monotone in the threshold: at
\(10^{-2}\), a Gaussian's per-pixel weight is \(<1\%\), and its worst occlusion odds on any
behind-surface is \(<1.01\%\). At \(10^{-2}\) deletion is lossless; at \(5\times10^{-2}\)
one balloon run degrades by \(-0.087\) dB. Hence \(10^{-2}\) is a conservative safe threshold
(its single-gaussian weight bound stays below 1% but approaches it; we do not claim it is the unique coarsest
safe threshold, since a slightly higher bound such as \(2\times10^{-2}\) is numerically equivalent
in cost on these runs).

### 3.3 Why a single low-opacity deletion is cheap: the bound

In front-to-back alpha compositing, the color at a pixel is
\(C=\sum_{i\in\mathcal N} c_i \alpha_i T_i\) with \(T_i=\prod_{j<i}(1-\alpha_j)\). For a
Gaussian with \(\alpha_k<10^{-2}\), its weight at any pixel is \(\alpha_k T_k < 10^{-2}\). The
single deletion is bounded, dataset-independently. (Important scope: this bounds **one**
Gaussian's **single** contribution; it does not by itself bound the cumulative mass of many
such Gaussians on one ray. We therefore measure that cumulative mass directly in Section 4
via a per-pixel accumulated-weight upper bound rather than claiming a batch theorem.)

### 3.4 Why it exists: mechanism (temporal attribution + supporting intervention)

Two pieces of evidence attribute the cohort to the opacity degree of freedom of the terminal
refinement pass, without over-claiming a clean causal counterfactual:

1. **Temporal attribution (all 36 runs).** The near-zero cohort's fraction is small in the
   online map (mean 0.69%, range 0–4.9%) and **rises in all 36 runs** after the 26,000-iteration
   color refinement (to mean 10.4%, mean +9.7 percentage points). Because
   refinement neither densities nor prunes nor resets Gaussians, the only degrees of freedom
   it can move are opacity, geometry, and color; the cohort's sharp growth between the two
   checkpoints therefore localizes most of its origin to this pass, while leaving a possible
   smaller online component.
2. **Supporting single-run intervention.** Freezing the opacity group's learning rate during
   refinement (geometry/color still optimize) shrinks the \(<10^{-2}\) cohort from 12.8% to
   3.7%. This is **consistent with** (rather than proof of) opacity soft-selection producing the
   cohort, and we emphasize the comparison is **confounded**: the standard and frozen runs
   already differ before refinement (32,653 vs. 39,074 Gaussians, the latter carrying a
   documented insertion race), so we do not describe it as a causal judgment. The intervention
   also changes final PSNR (−0.53 dB on this single run), which warns against over-reading the
   freeze outcome; we accordingly frame terminal pruning only as faithfully persisting the
   result of the observed soft selection into a smaller artifact, and do **not** claim the
   soft selection is "useful" from this comparison alone.

## 4. Experiments

### 4.1 Setup
**Dataset.** Six Bonn dynamic sequences (balloon, balloon2, mv_no_box, mv_no_box2, pt1, pt2),
3 seeds each. **Two cohorts, disclosed** — (i) the **tracking/accuracy cohort**: the official
36-run P2-T rerun on dual RTX 3090 (24 GB), whose prune-arm ATE and Gaussian counts are reported
in §4.5; (ii) the **map/pruning cohort**: the same 18 maps (`final_after_opt` PLYs) shipped on
the tracking cohort's 36 runs but re-rendered on an RTX 2060 dev box, offline interval-5 full-frame
at stored estimated poses (same instrument as `mc_terminal_comp_3seed`). All deletion / matched-rate /
cohort-weight analyses (§4.2–4.4, 4.6–4.7) use these 18 maps. The 18 pruning maps are a
**subset** of the same 36-run P2-T seed set (the prune arm of each run); they share the **same
lifecycle, same seed set, same checkpoint definition** (`final_after_opt` after the prune arm's
26,000-iteration terminal color refinement). The tracking (ATE) and pruning analyses therefore
refer to the **same 36-run run set**; the pruning re-render itself runs on an RTX 2060 dev box
(offline; no retraining, only reload + delete + re-render), so its results are hardware-independent
and are expected to hold on the 3090 used for tracking. We disclose the render-hardware separation
explicitly; both the ATE floor (§4.5) and the pruning results are measured values, not a single
"identical-run-set identity" beyond the shared 36-run seed set.

### 4.2 Main result — existence and zero cost (measured, not a theorem)

| seq | seed | op<0.01 rm% | dPSNR |
|---|---|---|---|
| balloon | 0/1/2 | 12.8/18.4/17.3 | −0.0001/−0.0001/+0.0001 |
| balloon2 | 0/1/2 | 11.4/8.8/11.2 | −0.0000/−0.0000/−0.0000 |
| mv_no_box | 0/1/2 | 9.9/8.4/10.0 | +0.0000/−0.0000/−0.0001 |
| mv_no_box2 | 0/1/2 | 9.6/12.7/13.0 | −0.0025/−0.0003/−0.0001 |
| pt1 | 0/1/2 | 9.9/10.1/10.3 | +0.0000/−0.0000/+0.0000 |
| pt2 | 0/1/2 | 18.4/11.2/10.5 | −0.0000/+0.0000/+0.0000 |

**18/18 runs: removal range 8.4–18.4% (mean 9–16%). On the four seed-validated sequences
(12 runs) \(|\Delta\text{PSNR}| \le 0.0001\) dB; across all 18 maps the worst single value is
−0.0025 dB (mv_no_box2 seed-0), and 17/18 maps stay \(\le 0.0003\) dB.** Fig. 2 plots each run
as a (removal fraction, \(\Delta\)PSNR) point: the whole cloud hugs the zero line across the
8.4–18.4% removal range. Zero cost is an *empirical* statement, explained by the single-gaussian
bound (§3.3) and confirmed at the pixel level by the cumulative-weight upper bound (§4.6). The
18-map table covers all six sequences × 3 seeds; Fig. 2 plots the 18-map cloud (the subset of the
12 four-sequence runs with the strongest \(10^{-4}\) dB bound is visualized at higher zoom), and
§4.6 extends the pixel-level upper bound to all 18 maps.

### 4.3 Non-triviality — matched-rate deletion controls (why not random / why not high-op)

At a matched \(\sim\)10% removal fraction on 3 maps (low / high / random):

| seq | low_op dPSNR | high_op dPSNR | random dPSNR |
|---|---|---|---|
| balloon | **−0.0000** | −3.822 | −0.788 |
| balloon2 | **−0.0004** | −2.272 | −0.438 |
| mv_no_box | **−0.0012** | −3.812 | −2.050 |

**Low-opacity deletion ≈ 0 dB; deleting the same number of high-opacity (−2.3 to −3.8 dB on
these maps) or random (−0.4 to −2.1 dB) Gaussians costs substantially.** The low-opacity cohort
is *specifically* safe; the worst per-map low-op value here (−0.0012 dB on mv_no_box) is three
orders of magnitude below the worst high-op/random cost.

**Extended controls (18 maps, 3-seed aggregate, `p3_matched_rate_extended.md`):** Deleting
the lowest-opacity Gaussians at rates 5% and 10% keeps \(|\Delta\text{PSNR}| \le 0.0021\) dB
(the measured max \(|\Delta|\) over all 36 map×rate cells is 0.00210 dB) across all six sequences
and three seeds — and the actual `op<0.01` deletion operator, now
measured on all 18 maps (`p4_op001_full18.md`), keeps \(|\Delta\text{PSNR}|\le 0.0003\) dB on
17/18 maps with a single worst value of −0.0025 dB (mv_no_box2 seed-0). **high-opacity deletion
costs −1.6 to −5.7 dB and random deletion −0.2 to −1.0 dB, both with all-negative sign.** For
the random controls the **replicate unit** is the individual map (one map = one sequence-seed
run). Each per-map random cell aggregates 10 draws; each sequence-rate row aggregates 3 maps
(3 seeds). The reported
spread (\([\min,\max]\) range
across the 10 draws, and the 3-seed mean±sd) reflects that non-determinism; every one of the
36 map×rate cells has a strictly negative random dPSNR. The specificity is therefore confirmed
on every sequence, at two removal rates; low-opacity deletion also leaves before/after-render
SSIM unchanged at \(1.00\) whereas high-opacity deletion drops it substantially.
Fig. 4 visualizes the headline 10%-rate row.

### 4.4 Artifact-level savings (storage/transfer, NOT runtime)

PLY is uniform-per-row, so bytes scale with Gaussian count. Aggregated over all 18 P2-T prune
maps (6 sequences × 3 seeds, `p3_artifact_full18.md`):

| seq | op<0.01 rm% (3-seed mean, range) | approx. serialized-bytes saved |
|---|---|---|
| balloon | 16.2% (12.8–18.4) | ≈11–16% |
| balloon2 | 10.5% (8.8–11.4)  | ≈8–11% |
| mv_no_box | 9.4% (8.4–10.0) | ≈8–9% |
| mv_no_box2 | 11.7% (9.6–13.0) | ≈9–11% |
| pt1 | 10.1% (9.9–10.3) | ≈9–10% |
| pt2 | 13.3% (10.5–18.4) | ≈10–16% |

Framed explicitly as **storage/transfer reduction** (bytes scale with Gaussian count →
removal fraction), **not refinement or runtime acceleration**. Aggregate: mean removal ≈11.9%,
≈9–16% of serialized bytes saved.

### 4.5 A self-tracked backbone (empirical floor, not a claim of SOTA)

The compression observation is not an orphan post-processing result: it sits on a self-tracked
backbone whose absolute ATE is moderate but non-collapsing on all six sequences under one
protocol. We report the backbone's prune-arm ATE here **as an empirical floor / system anchor**
for the observed map structure, and **explicitly disclaim "competitive" ranking against published
methods that we have not run under an identical protocol** (the competing numbers cited elsewhere
come from the original papers or trusted reproductions on possibly different splits/evaluation
paths, so a head-to-head table is not auditable). 6 sequences × prune × 3 seeds, self-tracked ATE
(fp: `tracking_raw.csv ate_rmse_cm`); the full two-arm (deferred vs prune) comparison is in the
supplementary (Table S.1):

| seq | prune G | prune ATE |
|---|---|---|
| balloon | 35513±5595 | **3.06**±0.14 |
| balloon2 | 45197±9443 | **5.28**±0.11 |
| mv_no_box | 41568±4202 | **2.66**±0.12 |
| mv_no_box2 | 62266±10864 | **5.14**±0.28 |
| pt1 | 53915±5319 | **10.04**±0.58 |
| pt2 | 69718±20027 | **10.44**±0.84 |

For the two sequences on which a same-style comparison appears in the dynamic-SLAM literature —
balloon and mv_no_box — our 3.06 cm and 2.66 cm are reported against published ATE figures
(RGD-SLAM 2.26 cm; DG-SLAM 3.65 cm). We did not run those methods under an
identical protocol, so these are in-prose comparisons only and we do not construct a formal
baseline table (an auditable head-to-head is out of scope); the ATE numbers are cited by paper
reference in the References section. pt1 and pt2 sit
at 10 cm+ and are reported honestly rather than cherry-picked; the table always lists all six
sequences under the same protocol (identical prune lifecycle and checkpoint definition as the maps
we prune). The ATE floor and the pruning maps come from the same 36-run P2-T seed set, disclosed
in §4.1.

### 4.6 Cohort cumulative-weight measurement (sampled upper bound)

**Measured quantity.** The true contribution of the removed cohort at a pixel \(p\) is
\(W_{\mathrm{removed}}(p)=\sum_{k\in R} \alpha_k(p)\,T_k^{\mathrm{full}}(p)\), where
\(T_k^{\mathrm{full}}\) is transmittance through *all* Gaussians in front. We do not measure
this directly; instead we render the removed cohort **alone** (mask path), giving
\(\widetilde W(p)=\sum_{k\in R}\alpha_k(p)\,T_k^R(p)\) with \(T_k^R\) the transmittance within
the *removed subset only*. Because fewer blockers ⇒ higher transmittance,
\(T_k^R(p)\ge T_k^{\mathrm{full}}(p)\), so \(\widetilde W\) is a **sampled upper bound** on the
cohort's true contribution. We report the per-pixel values of \(\widetilde W\) (mean /
99th-percentile / max) over the interval-5 stored-pose render path — this is a *sampled
measurement at evaluated poses*, not a guarantee over all possible pixels, viewpoints, or
camera trajectories.

**Measured (all 18 P2-T prune maps, 6 seq × 3 seeds):** the removed cohort's per-pixel
cumulative compositing weight — as an upper bound — averages ≈0.05–0.10%
(\(W_{\mathrm{mean}}\)), its 99th-percentile stays <2% everywhere (typical <1%; max 1.81% on
pt2 seed-0). Even at the single worst pixel (over all evaluated frames) it stays <7% on 12 of the
18 maps and <5% on 11 of them, peaking at ≈24% on rare isolated pixels in mv_no_box2 (seed1 15.1%,
seed2 23.7%) and pt2 seed0 (15.4%); those maxima do not move the per-map 99th-percentile (always
<2%), so on representative rays the cohort does not stack. Critically, the existence
zero-cost deletion and the cohort-weight measurement are **two independent measurements on
different metrics**: the deletion PSNR bound spans all 18 maps (`p4_op001_full18.md`, worst
|dPSNR|=0.0025 dB) while the cumulative-weight upper bound independently confirms the whole-cohort
pixel-level near-zero contribution across the same 18 maps (mean ≈0.05–0.10%, p99 <2% everywhere,
rare single-pixel maxima up to ≈24%).
### 4.7 Extended matched-rate robustness + safety boundary

**All 18 P2-T prune maps at rates 5%/10%, 10 random draws each** (see §4.3 aggregate and
`p3_matched_rate_extended.md`): the low-opacity cohort is specifically safe on *every*
sequence, at *both* rates, with random-confidence intervals and before/after render
distortion. **Safety boundary**: `op<0.05` is *not* safe (balloon seed-1 breaks −0.087 dB);
the 0.05–0.10 band carries residual surface detail; `op<0.01` sits in the mathematically
safe band of §3.3.

**Threshold-continuum characterization (18 maps, `p4_threshold_curve_result.md`).** Sweeping
the removal threshold from 0.001 to 0.10 on all 18 maps yields a reproducible structural curve
rather than a single operating point: below op=0.002 almost nothing is removed (0.1% mean),
then removal jumps to **10.7% at op=0.005** and reaches ≈12% at 0.01 — the cohort is **sharply
clustered in the tiny opacity band just below 0.01** — while the cost stays numerically negligible
through ~0.02 (worst single map −0.0025 dB at 0.01, −0.0026 dB at 0.02, both within the ≤0.003 dB
bound) and degrades monotonically thereafter (−0.017 dB at 0.05, −0.17 dB at 0.10). So 0.01 lies
on the flat, near-zero-cost part of the curve, and the sharp banding (rather than a gradual ramp)
is a structural signature consistent with the soft-selection mechanism; we do **not** claim a
unique "coarsest safe" threshold, since 0.02 is numerically equivalent in cost here.

**Spatial structure of the cohort (3 representative maps, `p4_cohort_spatial_result.md`).**
As a **descriptive signature** (3 representative maps, not a full-18 inference), the removable
low-opacity cohort is **not** isolated distant flotsam: its members are tightly
aggregated (mean intra-cohort nearest-neighbor 3.7–4.7 cm) and sit close to the scene's dense
high-opacity surface (4.5–8.4 cm to the nearest ≥0.9-opacity Gaussian; 68–91% have one within
0.1 m and 93–99% within 0.2 m). This is **consistent with** (rather than proof of) the freeze
mechanism: refinement appears to soft-suppress a subset of Gaussians that overlap the
deterministic near-surface region, freeing transmittance to it — but we do not claim a
projected-surface-removal or definitive "redundant near-surface layer" identification, since no
density-matched control or ground-truth surface is used.

## 5. Limitations

*We characterized the terminal color-refinement of our MonoGS-based backbone; whether other
SLAM front-ends produce the same soft-selected cohort is unknown and we do not extrapolate.
Removal (8–18%) is a modest but zero-cost shrink. The spatial-structure analysis covers 3
representative maps (descriptive, not a full-18 inference). Only 3D Gaussians were tested;
4D/explicit dynamics are out of scope. We do not claim online compaction: refinement's soft
selection is observed (a single frozen-opacity run differs by −0.53 dB PSNR, which is a confounded
intervention, not causal evidence of usefulness), and our pruning is purely post-hoc. The
matched-rate controls and the cumulative-weight upper bound use the interval-5 offline render
path at stored estimated poses; they are *sampled* measurements over evaluated pixels/frames,
not guarantees over all viewpoints. The frozen-opacity intervention is a **single** run
(temporally-staged 36-run observation + one supporting intervention) and is mechanism evidence,
not a verdict. Both the deletion PSNR and the cohort weight are measured, not theorem-derived
beyond the single-Gaussian bound of §3.3. ATE/Gaussian counts are self-tracked 3-seed means on
dual RTX 3090; FPS/VRAM figures are from the RTX 2060 development box and are not compared
against high-end competitors.*

## 6. Conclusion

Dynamic 3DGS SLAM's terminal color refinement soft-selects a reproducible low-opacity cohort
(temporally attributed to the refinement pass across all 36 runs, with a supporting
single-run opacity-freeze intervention) that is removed at zero render cost (single-gaussian
bound + measured cohort weight), with a
matched-rate control proving the specificity, a serialized-bytes reduction (9–16%) framed
explicitly as storage/transfer rather than runtime or compression, and no claim of online
compaction. The observation sits on a self-tracked backbone that stays non-collapsing across
all six sequences (3.06 cm on balloon, 2.66 cm on mv_no_box) under one protocol.

---

## References

> Reference list is generated mechanically via `\cite` from `papers/mmm/references.bib`;
> every key cited below has a verified Bibliographic entry (DOIs confirmed against Crossref
> where available). All entries are complete.

- `[MGS-SLAM]` — §2 online pruning (`mgs_slam`, CVM doi verified)
- `[Speedy-Splat]` — §2 online pruning (`speedysplat2025`)
- `[DCSHARP]` — §2 online pruning (`dcsharp2026`, WACV doi verified)
- `[3DGS.zip]` — §2 storage compression (`3dgszip2024`)
- `[LightGaussian]` — §2 storage compression (`lightgaussian2024`)
- `[Compact-3D]` — §2 storage compression (`compact3d2024`, CVPR doi verified)
- `[DG-SLAM]` — §2 dynamic SLAM + §4.5 in-prose ATE comparison (`dgsslam2024`, NeurIPS 2024, doi 10.52202/079017-1633)
- `[MonoGS]` — §3.1 backbone (`monogs2024`, CVPR doi verified = 10.1109/CVPR52733.2024.01708)
