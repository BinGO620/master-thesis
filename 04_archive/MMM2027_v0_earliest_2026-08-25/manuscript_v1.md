# MRCS — Manuscript draft, **v1 (selected)**

> **Target**: CCF-C, initially MMM (Springer **LNCS**, `llncs.cls`; 12 pages body + 2 pages
> references). This is the live draft; it advances toward v2.
>
> **Version state** (`WRITING_ROADMAP.md` §八): **v0 → v1 done 2026-08-25 (exp46).**
> v0 is frozen verbatim in `manuscript_v0.md` (16.84 pages of text) and is an **asset, not a
> discard** — anything cut below is recoverable there without returning to `results/`.
> What v1 removed, and where each piece went, is itemised in `WRITING_ROADMAP.md` §八-A.
> Material moved out of the body lives in `supplementary.md` §S2–S7, which was written to
> receive it (not merely promised).
>
> **Discipline for this file** (project rule, non-negotiable, unchanged by compression):
> 1. Every factual statement about a competitor is traceable to that paper's own text — see
>    `results/evidence/competitor_protocol_table.md` for the quote and line number of each.
>    **Paraphrase from memory is not evidence.**
> 2. Every number about our own system is traceable to a run artifact under `results/`.
> 3. The forbidden-phrase list in `WRITING_ROADMAP.md` §六 applies to every line here.
> 4. **A claim's scope statement travels with the claim.** Compression may move a *table* to the
>    supplement; it may never separate a claim from its caveat.

## Status of sections

| § | Section | Status | Blocked on |
|---|---|---|---|
| 1 | **Introduction** | ✅ **drafted (this file, exp46)** | — (contribution bullets are F1/F2/F3) |
| 2 | **Related Work** | ✅ **drafted (this file)** | — |
| 3 | **Method** | ✅ **drafted (this file, 2026-08-25)** | — (constants **and attachment points** verified against resolved config + source; audit `results/evidence/method_attachment_audit.md` corrected 3 errors and disclosed a 4th component) |
| 4 | **Experimental Protocol** | ✅ **drafted (this file)** | — |
| 5 | **Results / ablations** | ✅ **drafted (this file, exp46)** | — (ratios tiered by vanilla CV per `headline_ratio_recompute.md`; §5.5 boundary rebuilt on `rpe_stratification_rule_test.md` after the ~2.5 cm/frame threshold was falsified) |
| 6 | **Limitations** | ✅ **drafted (this file, exp46)** | — (14 items: the roadmap's 8 + Δ_L compound scope + fitted boundary + no cue selector + TRC negative + rendering + map-side) |
| 7 | **Conclusion** | ✅ **drafted (this file, exp46)** | — |

---

# 1. Introduction

Dynamic content breaks monocular and RGB-D SLAM in a specific way: a moving object supplies
photometric and geometric residuals that the estimator, which assumes a rigid world, resolves by
moving the camera. On the standard dynamic benchmarks this is not a marginal degradation. Our
3DGS-SLAM backbone, run unmodified on 3 seeds, drifts to 39.32±1.01 cm on a sequence with a person
and a balloon, 43.85±8.55 cm on a person-tracking sequence, and 147.5±39.0 cm on a crowded one —
against roughly 1.5 cm on the static sequences from the same datasets.

The dominant response is to detect the movers and remove them. An external, pretrained,
class-conditioned network labels which pixels belong to things that could move, and the estimator
discards them; this structure runs from keypoint-era systems through neural-implicit SLAM and into
essentially every recent 3DGS-based dynamic system (Sec. 2.1). It works, and we do not argue
otherwise. But it makes the dynamic decision a per-frame classification by a second model, with that
model's runtime cost and failure modes, and it is closed-set: the category list has no label for many
of the movers these benchmarks actually contain — balloons, carried boxes, objects placed and
removed. A recent line replaces the *class* prior with a learned uncertainty (Sec. 2.2), and a third
keeps a segmentation network but moves the dynamic decision out of it (Sec. 2.3).

Our own configuration sits in that third line, and we want to be exact about what is and is not new
in it. It decides which pixels to trust from *consistency* — the disagreement between observed
optical flow and the flow a rigid scene would produce — rather than from categories, and it
down-weights rather than removes. **Operating without semantic segmentation is not itself a
contribution we claim**; prior work has done that (Sec. 2.3). What has not been supplied, for this
family of designs, is evidence answering two questions that decide whether such a system is
understood at all. *Which* of its parts are actually necessary, and on which sequences do they stop
being necessary — a system reported as an assembled bundle leaves this unmeasured. And is a reported
gain attributable to the proposed mechanism, or merely to the extra information the mechanism was
handed — which can only be separated by a counterpart consuming *the same information* through a
deliberately naive mechanism.

We therefore present a mask-free kernel for dynamic 3DGS-SLAM together with the measurements that
bound it, and our contributions are the measurements:

1. **Component necessity is regime-dependent, and we measured it rather than asserting it.** A
   pre-registered three-factor factorial (8 cells × 5 sequences × 3 seeds = 120 runs) finds that
   uniform keyframe coverage is strongly positive on object-only sequences but **negative** on the
   mixed-mover sequence; that robust reweighting is indistinguishable from zero on 3 of 5 sequences
   yet is the single largest effect in the matrix on the hardest one; and that the reliability signal
   is the only component never negative anywhere. **No sequence has all three positive — 0 of 5 — so
   no globally necessary subset exists** in this design (Sec. 5.2). This is a statement about
   mechanism, not engineering: the necessary subset is a function of the regime.

2. **The gain is not attributable to the information alone.** Under an equal, byte-identical, strictly
   causal flow budget, a naive per-pixel threshold on the *same* frozen flow improves on the baseline
   on only 2 of 4 held-out sequences and is **worse than the baseline on one** (0.90×), while our
   mechanism improves on 4 of 4 (1.63–4.99×) and beats the naive counterpart on 4 of 4 (Sec. 5.4).
   This closes the "it just had more information" reading.

3. **The pose-side mechanism is a variance–bias trade, confirmed by measuring the intermediate
   quantity.** One single-variable intervention moves per-frame tracking error *worse* (+0.0806,
   1.22× its noise floor) and full-trajectory error *better* (−1.42 cm, 4.0×), and the coherent,
   drift-contributing component of the error explains why by falling (−0.0248, 1.38×) (Sec. 5.6).
   The consequence generalises beyond our system: **a claim that pose estimation improved is not
   well formed until the endpoint is named**, because a per-frame-magnitude endpoint does not
   predict trajectory quality.

We also report where our mask-free configuration is *not* sufficient, since the same evidence that
supports the above delimits it. Semantic segmentation turns out to be redundant on both pure-object
sequences and on one of two person sequences, but dominant on mixed-mover sequences and on a second
person sequence where our mask-free configuration fails outright (32.41±8.51 cm, recovered to
11.89±2.36 cm with the mask). Across all 18 sequences the mask-free arm's own per-frame drift
separates those two groups without overlap (Sec. 5.5) — a diagnostic we report with its limits
rather than as a selector. We do not claim state-of-the-art accuracy: our absolute error trails the
best reported dynamic systems by 1.4–2.5× on the TUM walking and person sequences, and we give the
full 18-sequence table without selective highlighting.

---

# 2. Related Work

## 2.1 Dynamic SLAM built on explicit dynamic priors

Handling moving objects in SLAM has long followed a *detect-then-exclude* structure: an external
model labels which pixels belong to potentially moving things, and the estimator discards them. In
the keypoint era DynaSLAM computes "a pixel-wise semantic segmentation of the images" with Mask
R-CNN, and NGD-SLAM keeps the structure with a YOLO detector; neural-implicit SLAM inherited it, with
RoDyn-SLAM forming its motion mask by "incrementally fusing the optical flow mask" with "the semantic
segmentation mask" to reject sampled rays.

The pattern is widespread in 3DGS-based dynamic SLAM. RGD-SLAM segments with "the pre-trained version
of OneFormer on the COCO dataset" and refines the motion mask with an EKF; DG-SLAM uses OneFormer "to
generate prior semantic segmentation" and initialises poses from DROID-VO; BDGS-SLAM turns YOLOv5
detections into a per-Gaussian Bayesian dynamic prior; DAGS-SLAM "fuses lightweight YOLO instance
priors" with a per-Gaussian motion probability; and DynaGSLAM combines "coarse motion blobs computed
from the RAFT optical flow image with real-time online SAM2", adopting poses from DynoSAM "without
modification". Every quotation here is anchored to its source line in the evidence appendix.

Whatever the representation, the dynamic decision here is delegated to an external, pretrained,
class-conditioned model. That inherits a second model's runtime cost and failure modes; it makes the
decision a *per-frame classification*, so a missed or spurious detection propagates into the map;
and it is *closed-set*, with no label for many movers these benchmarks actually contain — balloons,
carried boxes, objects placed and removed.

## 2.2 Replacing the class prior with a learned uncertainty

A recent alternative drops the category prior while keeping a learned one. WildGS-SLAM predicts
per-pixel uncertainty from "a pre-trained DINOv2 feature extractor" — the finetuned version "which
injects 3D awareness" — decoded by a shallow MLP and supervised with metric depth "as estimated by
Metric3D v2". Its own baseline overview defines *Prior Free* as "not using class priors, where 'O'
represents object detection and 'S' denotes semantic segmentation", which places the contribution
precisely: the *semantic class* prior is removed, while a learned appearance prior remains, supplied
by two external pretrained networks.

This distinction matters for how we position our own system, and we hold ourselves to it: our
mask-free configuration removes semantic segmentation, **not** the dependence on a pretrained
network — it still consumes frozen optical flow. We therefore describe it as *mask-free*, never as
*prior-free*.

## 2.3 Dynamic decisions from consistency rather than from categories

A third line keeps a segmentation or depth network but moves the *dynamic decision* out of
it, or removes the semantic network entirely. Gassidy separates objects from background
through "the instance masks Si generated by YOLO segmentation", then decides which of those
objects are dynamic by iteratively analysing rendering-loss flows from a photometric-geometric
loss, so the category label never decides motion. DGS-SLAM runs an online Track-Anything
segmentation in its frontend and adds a robust mask enforcing photometric consistency across
keyframes, explicitly "reducing noise from inaccurate segmentation and artifacts such as
shadows". Dy3DGS-SLAM drops the semantic network in a monocular setting, fusing an optical-flow
mask with a depth mask from "the DepthanythingV2 estimation network". GARAD-SLAM goes furthest:
it states that "we do not perform semantic segmentation on the feature points in the tracking
phase", and instead builds a conditional random field over Gaussians in the backend, maps the
segmentation back to frontend feature points, and validates labels with sparse optical flow.

Our own configuration belongs to this line, next to GARAD-SLAM. **We therefore do not claim that
operating without semantic segmentation is by itself new.** What this line does show is that
"mask-free" has to be checked per system rather than read off a label: of these four, two still
consume a segmentation network and a third a monocular depth network.

## 2.4 Robust estimation and temporal sampling in SLAM

The ingredients we combine are individually classical. Robust M-estimation with Huber or
Cauchy kernels is standard practice for suppressing gross outliers in photometric and
geometric residuals; residual-based reweighting has ample precedent in dense and neural
SLAM; and keyframe management is a core component of every modern system. Our backbone,
MonoGS, "maintain[s] a small window W_k" of keyframes over which Gaussians and camera
poses are optimised, states that for camera localisation it "does not use any pretrained
monocular depth predictor or other existing tracking modules", and reports its accuracy as
"comparable to systems which perform explicit loop closure" - i.e. it performs none itself.

What is missing is therefore neither another robust kernel nor the removal of the semantic prior,
but the two measurements Sec. 1 named: which components are individually necessary, and whether a
gain is attributable to the mechanism or to the information it was handed. Sec. 5 supplies both.

## 2.5 Reading absolute numbers across these systems

The systems above are not evaluated under a common protocol. They differ in input modality
(WildGS-SLAM is monocular RGB, the rest RGB-D), in which pretrained networks they consume, in how
far back later frames are allowed to rewrite the reported trajectory — several run a global or dense
bundle adjustment after tracking completes, whereas MonoGS and our system optimise only within a
bounded keyframe window — and in reported hardware, which one system does not state. We list these
axes per method, with the supporting sentence and line number for each cell, in S6, and our own
configurations appear there under the same columns. We do this to make the comparison legible, not
to argue that any of these methods is unfair or that our numbers should be discounted; **no
conclusion in this paper rests on that table.**

---

# 3. Method

Our system adds four components to a 3DGS-SLAM backbone. None of the four is a new
primitive, and we do not present them as such (Sec. 2.4); this section states precisely **what each
one changes in the estimator**, so that the ablations in Sec. 5 can be read as interventions on
named quantities rather than on a monolithic "our method". Every constant quoted below is the
resolved value actually used in the reported runs, not a nominal default (Sec. 3.7).

## 3.1 Backbone and where the components attach

The backbone is MonoGS in its RGB-D configuration: the frontend estimates each frame's pose by
minimising a photometric and geometric residual against a fixed Gaussian map, and the backend
periodically re-optimises Gaussian parameters and the poses of a bounded keyframe window. We change
neither the Gaussian representation nor the rasteriser. We **do** change the density lifecycle, and
we say so rather than describing our configuration as the stock backbone.

Four components attach at four distinct places, named separately because Sec. 5.2 shows their
contributions are not interchangeable (Fig. 1): **coverage** decides *which frames become keyframes*
(§3.2); **robust reweighting** decides *how much each pixel's residual counts in the pose solve*
(§3.3); **reliability weighting** decides *which pixels are trusted to be static* (§3.4); and the
**lineage-tagged density lifecycle** decides *which newly created Gaussians survive* (§3.5). The
third is the only one consumed at more than one site — one in the frontend, one in the lifecycle —
and §3.4 names both, because the ablation of Sec. 5.2 removes them together.

A fifth, **optional** component supplies a semantic person mask (§3.6). Our *mask-free* configuration
disables it entirely, our *combined* configuration enables it; we keep the two distinct throughout
and never use a number obtained with the mask to support a statement about the mask-free system.

> **Figure 1** (`figures/fig1_pipeline.pdf`).
> *Where the components attach.* Grey is the backbone; each teal box sits beneath the one stage it
> modifies. The reliability signal is the only component with **two** out-edges — it weights the
> tracking residual (1) and the candidate confirmation that decides which Gaussian lineages survive
> (2) — which is why the ablation in Sec. 5.2 measures their *joint* effect. The olive box is the
> optional person mask of the *combined* configuration, dashed because *mask-free* removes it; its
> three sites belong to it, not to the reliability signal. Constants: S2. No edge asserts an effect
> we did not measure.

## 3.2 Coverage: uniform temporal keyframe sampling

MonoGS selects keyframes adaptively, primarily by co-visibility, so keyframe density is a property of
the scene: across our five ablation sequences the backbone's native density spans **0.045 to 0.075
keyframes per frame**, a factor of 1.7, with easier scenes sampled more sparsely. `DynamicKeyframe`
adds one rule on top: if the current frame is more than `gap_cap = 5` frames from the last keyframe,
insert one regardless of what the co-visibility test concluded. The native criterion is not removed,
only floored.

The measurable effect is a change of *regime* rather than of degree. With the rule enabled density
becomes near-constant across sequences at **0.198 to 0.204 keyframes per frame** — a 3% spread, the
reciprocal of `gap_cap` — so temporal sampling moves from *scene-adaptive* to *uniform*, at a cost of
2.7–4.5× more keyframes and roughly double the final map size. This is the sense in which "coverage"
is meant, measured at the granularity of the **keyframe budget**; we do not claim a measurement of
per-point observation counts. Sec. 5.2 reports that this trade is favourable on both object-only
sequences and on `pt2`, but **negative on `balloon`**, so uniform coverage is not asserted to be
universally better.

## 3.3 Robust reweighting: Huber IRLS inside the pose solve

`RobustTracking` replaces the L2 photometric and geometric tracking residual with an
iteratively-reweighted least-squares step. At each tracking iteration, for residual $r$ the weight
is the standard Huber IRLS weight

$$w_{\text{rob}}(r) = \min\!\left(\frac{\delta}{|r|},\, 1\right),$$

applied separately to the RGB and depth residual channels with
$\delta_{\text{rgb}} = \delta_{\text{depth}} = 0.1$ in the units of the respective channel. Two
implementation properties matter for how Sec. 5 should be read. The weight is computed from a
**detached** residual, so it is a per-iteration reweighting and not an extra path through the
gradient. And it is **recomputed at every tracking iteration**, so the weights co-adapt with the
pose as the solve proceeds — which distinguishes it from the fixed per-frame map of Sec. 3.4.

## 3.4 Reliability: a per-frame, per-pixel static-confidence map

This is the component that consumes optical flow. Its purpose is to answer, without any category
label, *which pixels can be trusted as evidence about camera motion*.

**Two flows, one disagreement.** For frame $t$ we take a precomputed backward optical flow
$f_{\text{obs}} = f_{t \to t-1}$ from a frozen RAFT network, and the flow the same pixel *would*
have if the scene were rigid, $f_{\text{static}}$, obtained by reprojecting through the current
depth and ego-motion estimate. Their disagreement is the raw cue: a mover is precisely what makes
observed flow depart from the rigid prediction, so no category label is required.

**Threshold-free normalisation.** The disagreement magnitude becomes a cue
$e_{\text{flow}} \in [0,1]$ through a per-frame robust normaliser `scale = max(1.4826·MAD, floor)`:
0 at or below the frame median, approaching 1 for robust outliers, with no hand-set cutoff. The floor
is a noise-floor prior in physical units (2.0 px) guarding one failure mode — on a near-static frame
MAD collapses and any nonzero deviation would otherwise saturate to 1.

**Combining the cues.** A geometric cue $g$ measures depth-residual anomaly, gated by map opacity
$v$ so unmapped regions cannot vote. The two combine multiplicatively into a static confidence

$$s = (1 - e_{\text{flow}})\,(1 - v\,g) \;\in\; [0, 1],$$

so a pixel is trusted only if *both* cues find it unremarkable, and $s \to 1$ recovers the
unmodified estimator — a no-harm property we rely on for the static sequences. With $d = 1 - s$ the
tracking weight is a frame-adaptive Cauchy down-weight

$$w_{\text{rel}} = \frac{1}{1 + (d/\tau)^2}, \qquad
\tau = \operatorname{median}(d) + 1.4826\,\operatorname{MAD}(d) + \varepsilon ,$$

with $\tau$ estimated from the frame's own $d$ distribution rather than fixed as a temperature.

**The weight is bounded away from zero.** What multiplies the residual is
$\max(w_{\text{rel}}, 0.10)$ in every reported run. This is substantive, not an implementation
detail: the mechanism attenuates a pixel by at most 10× and **never removes one**. It is the
sharpest statement of how our mechanism differs from a mask, and Sec. 5.4 leans on it — the
controlled counterpart there thresholds the *same* flow field into a hard decision, so the
comparison is bounded attenuation versus hard removal, not a better-tuned cutoff.

**When it is computed, and where it is consumed.** The map is computed **once per frame** after
`warmup_iters = 10` tracking iterations, then frozen for that frame's remaining solve: the warm-up
prevents a still-converging pose from suppressing the contradictions that should inform it, and
freezing prevents the weight from adapting to the pose it constrains. Absent frozen flow,
$w_{\text{rel}} \equiv 1$ and the estimator is unchanged. The frozen map is then consumed at
**two** sites: (1) the **tracking residual**, where $\max(w_{\text{rel}}, 0.10)$ multiplies the
Huber weight of Sec. 3.3 in both the RGB and the depth channel; and (2) **candidate confirmation**
in the lifecycle of Sec. 3.5, where $s$ weights the support/contradiction evidence deciding whether
a new Gaussian lineage is confirmed, contradicted, or left to expire — reverting to unweighted
integer counts when the component is off. We enumerate both because this fixes the scope of what
Sec. 5.2 measures: the component is a *pair* of interventions sharing one signal, the ablation
removes the pair, and we therefore do not attribute the measured effect to the tracking site alone.

**A limitation the estimator creates.** $\tau$ is a *majority* statistic, so a mover occupying a
large share of the frame joins the population setting its own knee and cannot be down-weighted
relative to itself. This is a property of the estimator, not a tuning oversight, and it is one reason
the mask stays dominant on mixed-mover sequences (Sec. 5.1).

> **Figure 2** (`figures/fig2_mechanism.png`).
> *The reliability signal, one frame of `balloon`, mask-free.* Left to right: the RGB frame; the
> flow cue $e_{\text{flow}}$; the opacity-gated geometry cue $v\,g$; their multiplicative fusion
> $1-s$; and the resulting Cauchy down-weight $1-w$ applied to the tracking residual. Red is
> evidence of motion. The green contour is a frozen ground-truth-pose dynamic mask, drawn for
> reference only — it is never consumed by the mask-free configuration. The panel beneath
> recomputes mean $s$ and mean $w$ over the whole sequence, with the displayed frame marked. The
> frame is chosen by a stated rule — the one whose separability is closest to the sequence
> median, i.e. a *typical* frame rather than the most favourable one — and that separability is
> modest (AUC 0.734 for this frame, 0.733 over 82 frames), which is the honest reading of what a
> class-agnostic cue buys: it is informative, not a segmentation.

## 3.5 The density lifecycle: lineage-tagged insert-then-remove

The backbone creates new Gaussians at every keyframe from pixels the current map does not yet
explain. Stock MonoGS commits them immediately and thereafter governs them only by its own
opacity-based density control. Our reported configuration replaces that commit rule, and because the
replacement is load-bearing we describe it as a component rather than as part of the backbone.

Each Gaussian created at a keyframe carries a **lineage** identifier. Over following keyframes the
lineage accumulates support and contradiction evidence from the views that observe it; a lineage
gathering `confirming_views = 2` worth of support is retained, while one gathering
`reject_contradictions = 2` worth of contradiction, or reaching `ttl_keyframes = 5` unconfirmed, is
**deleted in full** — every Gaussian carrying that tag. As Sec. 3.4 states, the reliability signal
weights this evidence when enabled; without it the evidence is unweighted integer counts. This is
not a marginal cleanup: across the main campaign's runs the deleted fraction of created lineages has
median **0.55** (range 0.27–0.81). A reader comparing our configuration against stock MonoGS is
therefore comparing against a different density rule, and we would rather say so than let "we use
MonoGS" imply otherwise. Per-run counters, and a negative result on a third lifecycle variant we
implemented and did **not** adopt, are in S2.1.

## 3.6 The optional semantic mask, and why it is reported separately

In the *combined* configuration a Mask R-CNN person mask (dilated by 7 px) is applied at the
mapping loss and the keyframe-insertion gate, and — for the first `warmup_iters` tracking
iterations only — as a hard mask on the tracking residual, after which the soft weight of Sec. 3.4
takes over. We audited which code paths this switch actually opens rather than assuming: the mapping
loss and the keyframe-insertion gate belong to *this* component and not to the reliability signal of
Sec. 3.4, an attribution an earlier draft of ours got wrong in both directions.

We therefore report *mask-free* and *combined* as two configurations of one system, and Sec. 5.1
quantifies where the mask is redundant and where it is dominant, instead of claiming the mask is
unnecessary.

## 3.7 Provenance of the constants in this section

Every constant above was read back from the **resolved** configuration of a reported run and from
the source, not from a nominal default and not from prose. S2 tabulates all sixteen with their
sources, together with the two sites at which the reliability signal is consumed, one configured
field that is **inert** and which we report as such rather than deleting, and one
configuration-hygiene wart we state rather than tidy away. We are explicit about this provenance
because an audit of an earlier draft of this section corrected three factual errors in it and
disclosed a component it had omitted.

---

# 4. Experimental Protocol

Every decision below was in force before the campaigns of Sec. 5 were run. The full protocol,
including per-sequence frame counts, is in S1; this section states only what a reader needs in order
to interpret the tables.

**Sequences.** 18 RGB-D sequences, 8 from BONN RGB-D Dynamic and 10 from TUM RGB-D, covering static,
low-motion, high-motion and *object-only* dynamic scenes. The denominator is fixed at these 18 and no
campaign may select a subset after seeing results. The object-only group is deliberate: those movers
carry no person label, so they separate "handles dynamics" from "detects people".

**Trajectory accuracy.** Full-trajectory ATE RMSE (cm) via `evo` after an **SE(3) Umeyama alignment
without scale correction** — a Sim(3) alignment would absorb a global scale an RGB-D system is not
entitled to, so it is never used. ATE covers **all** frames; the keyframe-only RMSE printed to
console is a different quantity and is never quoted as a headline. We also report RPE (translation)
under the same alignment.

**Seeds and completion.** Every configuration runs with **3 seeds**, reported as mean ± sd (ddof = 1)
with per-cell spread; cells whose spread reaches 2× are flagged and their mean is not quotable alone.
A run counts as completed only if its trajectory contains ≥ **95%** of the sequence's frames, and a
pair with fewer than two co-completed seeds is reported as *unresolved* in its own row rather than
dropped — the denominator stays at 18, and a configuration that cannot finish is reported as a
failure to finish, not as missing data. Seed averaging does not capture all dispersion; S5 quantifies
what it misses.

**Rendering, efficiency, hardware.** Rendering metrics are computed offline from the final Gaussian
map re-rendered over all frames; the end-of-run refinement optimises Gaussian parameters only and
performs no pose step, so it does not modify the reported trajectory. Arms run for tracking only show
"—", meaning *not run*, never *failed*. Efficiency is reported from the online phase and **only ever
compared between our own configurations on identical hardware**. Optical flow is precomputed by a
frozen RAFT network, so **RAFT inference is not in the online rate** (Sec. 5.7). All Sec. 5 campaigns
ran on **RTX 3090**.

**Provenance.** Each reported cell corresponds to exactly one run directory; where a seed was
executed more than once the **latest** run supplies every metric of that cell, so a cell's trajectory
error and its rendering metrics always come from the same run, and duplicates are listed rather than
averaged away. Frozen flow is precomputed per sequence, making the flow input byte-identical across
every arm that consumes it.

---

# 5. Results

Ratios are quoted **only** where the baseline they divide by is itself stable, by the rule stated
first.

## 5.1 Trajectory error across 18 sequences

**How ratios may be read.** Our backbone's own dispersion is not uniform across sequences, and this
governs which improvement ratios are quotable at all. Over the 3-seed vanilla rerun set, **8 of the
18 sequences have a baseline coefficient of variation above 20%**, two of them above 60%. On such a
sequence the improvement ratio is a function of which basin the baseline fell into rather than a
property of our method — extremal pairing puts `mv_no_box` anywhere in 1.30–8.45×. **We therefore
quote a single ratio only where the baseline CV is ≤ 20%, and report mean ± sd otherwise.** Every
baseline cell in the full table (S3) carries its sd and CV so the reader can apply this rule
independently; per-sequence pairing ranges are in S3.2.

**Gains over the unmodified backbone.** On the qualifying sequences the mask-free configuration
improves by **2.2–4.7×** — `pt2` 43.85±8.55 → 9.30±0.64 (4.71×), `balloon` 39.32±1.01 → 12.11±1.90
(3.25×), `balloon2` 22.05±1.55 → 10.14±0.62 (2.17×) — and the combined configuration by
**4.2–17.1×**: `f3_wk_rpy` 17.13×, `balloon` 12.85×, `f3_wk_xyz` 9.20×, `balloon2` 4.18×, `pt2`
4.20×. `balloon` is worth singling out not for being the largest but for being the
**best-conditioned**: 12.85× against a baseline whose CV is 3%, still 11.97× under the most
conservative pairing. Larger ratios exist — `crowd2` 60.93×, `crowd` 37.11× — but their baselines
vary by 26% and 21% and we report them only with that dispersion attached. On
`mv_no_box`/`mv_no_box2` the mean ratios are 4.95×/3.00× but the baseline CV (62%/101%) forbids
quoting them, so those two sequences carry a different claim below rather than a gain.

**Where the mask matters, measured between our own two arms.** The comparison mask-free ÷ combined
never passes through the vanilla denominator, and both arms are low-dispersion (6/6 cells 3-seed,
5/6 with sd ≤ 0.84), so it is the cleanest statement we can make about the mask:

| Sequence | mask-free | combined | ratio | reading |
|---|---:|---:|---:|---|
| `mv_no_box2` | 5.62±0.30 | 5.14±0.28 | 1.09× | mask redundant |
| `mv_no_box` | 3.10±0.46 | 2.65±0.12 | 1.17× | mask redundant |
| `pt2` | 9.30±0.64 | 10.45±0.84 | 0.89× | mask redundant (mask-free marginally better) |
| `balloon2` | 10.14±0.62 | 5.27±0.11 | 1.92× | mask dominant |
| `pt1` | 32.41±8.51 | 11.89±2.36 | 2.73× | mask dominant |
| `balloon` | 12.11±1.90 | 3.06±0.11 | 3.96× | mask dominant |

Semantic segmentation is thus **redundant on both pure-object sequences and on one of the two person
sequences, and dominant on the mixed-mover sequences and on `pt1`**. We do not claim the mask is
unnecessary; we claim its necessity is sequence-dependent, and Sec. 5.5 gives the observable that
tracks it.

**What we do not claim.** We do not claim state-of-the-art accuracy. In absolute terms our combined
configuration trails the best reported dynamic method on the TUM walking and person sequences by
1.4–2.5× (`f3_wk_xyz` 3.06 vs 2.01 for RGD-SLAM and 1.22 for WildGS-SLAM; `pt1` 11.89 vs 7.21), and
`pt1` remains a failure region for every configuration we ran. The full 18-sequence table is given
without selective highlighting for exactly this reason.

## 5.2 Component necessity is regime-dependent (Fig. 3)

We ran a pre-registered three-factor factorial over the components of §3.2–3.4 — coverage `K`,
robust reweighting `R`, reliability `L` — as 8 cells × 5 sequences × 3 seeds = 120 runs, mask-free
throughout, with the lifecycle of §3.5 pinned identically in all 8 cells so it cannot confound the
contrast. Each factor's pairwise marginal on log-ATE is signed so that **positive means removing the
component hurts**. The five sequences are ordered by tracking difficulty: two pure-object
scenes (`mv_no_box`, `mv_no_box2`), one person scene (`pt2`), one mixed-mover scene
(`balloon`), and one harder person scene (`pt1`).

| | `mv_no_box` | `mv_no_box2` | `pt2` | `balloon` | `pt1` |
|---|---:|---:|---:|---:|---:|
| Δ_K coverage | +0.250±0.162 | +0.586±0.250 | +0.719±0.309 | **−0.182±0.131** | −0.201±0.183 |
| Δ_R robust | +0.030±0.187 | −0.013±0.178 | −0.011±0.147 | **+0.780±0.037** | +0.413±0.140 |
| Δ_L reliability | +0.157±0.417 | +0.131±0.158 | +0.170±0.048 | +0.291±0.202 | +0.108±0.199 |

> **Figure 3** (`figures/fig3_regime_split.pdf`).
> *Component necessity is regime-dependent.* The same marginals as the table above, as a diverging
> map with zero pinned to the neutral colour: rows are the three components, columns the five
> sequences ordered by tracking difficulty. Each cell gives mean $\pm$ sd over 3 seeds and the
> verdict. The figure exists for the **sign pattern** rather than the magnitudes — no column is
> positive throughout, which is the claim the table makes the reader assemble by hand.

Three readings, in decreasing order of how firmly the data support them.

**No sequence has all three components positive — 0 of 5.** This is the paper's central measurement.
Coverage is strongly positive on the object-only sequences and on `pt2` but **negative on `balloon`**,
the one mixed-mover sequence: uniform temporal sampling actively hurts there. Robust reweighting is
indistinguishable from zero on the three easier sequences yet is the largest single effect anywhere
in the table on `balloon` (+0.780±0.037, the tightest cell in the matrix). The necessary subset is
therefore a function of the sequence, and **no globally necessary subset exists** in this design. A
system reported only as an assembled bundle leaves this unmeasured, which is why we consider the
measurement, not the mechanism, to be the contribution.

**Reliability is the only component never negative** — 5/5 non-negative, significant on `pt2` and
`balloon`, directionally consistent but within one sd elsewhere. Removing it costs 1.13–1.37× in ATE
(`balloon` 13.45±1.43 → 18.36±5.12; `pt2` 8.76±0.41 → 10.37±0.18), and it never appears in the worst
cell of the 8-cell table.

**The scope of that last claim, stated precisely.** As Sec. 3.4 sets out, `L` is consumed at two
sites, and the factorial pins reliability-weighted candidate confirmation on in all 8 cells.
Switching `L` off therefore removes the tracking down-weight **and** degrades the confirmation
evidence to unweighted integer counts, so Δ_L is the **joint** effect of the two sites; we did not
isolate them and do not apportion the effect between them. An apparatus check before dispatch
confirmed the axis is a real mechanism removal rather than a null-vs-null comparison. Finally, 3
seeds per cell gives weak per-sequence intervals: every statement here is descriptive, and cells
whose sign sits inside one sd are reported as directional only.

## 5.3 A two-by-two corroboration

A 2×2 over the mask and coverage (3 seeds per cell; full table in S4) corroborates both readings. On
`balloon` the mask axis moves ATE roughly fourfold (3.06±0.14 with it, 12.11±1.90 without) while the
coverage axis moves it essentially not at all (3.06 vs 3.03) — matching the negative Δ_K above. On
`mv_no_box` all four cells land within 2.66–3.90 cm against a vanilla mean of 15.33 cm: neither
switch accounts for the improvement alone, the remaining components hold the result without them, and
only removing all of them returns the system to baseline.

## 5.4 The gain is not attributable to the flow information alone

The obvious objection to Sec. 5.1 is that our system consumes a precomputed flow field the baseline
does not, so the comparison could be measuring the extra information rather than our mechanism. We
built the counterpart that isolates this: an arm consuming **the same frozen backward flow,
byte-for-byte**, through a deliberately naive per-pixel threshold at the 90th percentile (frozen on
pilot sequences before any confirmation run), used as a hard mask in place of our weighting. Three
arms × 4 held-out sequences × 3 seeds = 36 runs, all completing ≥ 95% of frames; held-out sequences
and the decision rule were fixed before the first run.

| Sequence | vanilla | naive flow threshold | MRCS |
|---|---:|---:|---:|
| `pt1` | 63.22±10.65 | 51.41±11.17 | **38.51±2.51** |
| `pt2` | 45.37±2.02 | 51.07±11.09 | **9.09±0.31** |
| `mv_no_box2` | 15.64±14.14 | 6.23±0.43 | **4.97±0.29** |
| `balloon2` | 24.10±0.56 | 23.30±9.87 | **11.90±1.85** |

(Dispersion here is mean ± half-range, the pre-registered convention for this campaign, and these
are the campaign's own in-arm vanilla and MRCS runs rather than rows borrowed from Sec. 5.1.)

The naive counterpart improves on vanilla on only 2 of 4 sequences and is **worse than vanilla on
`pt2`** (0.90×). MRCS improves on vanilla on 4/4 with all 3 seeds agreeing in sign (1.63–4.99×) and
beats the naive counterpart on 4/4 (paired log-ratio means +0.274/+1.710/+0.226/+0.593, i.e.
1.25–5.53×, 3/3 seeds same sign each). Under an equal and causal flow budget, then, "any
flow-consuming anti-dynamics treatment" does not reproduce the result.

**Honest boundaries on this campaign.** The effect on `pt1` is not uniform — its three seeds give
+0.402/+0.059/+0.361, the middle one far below the pre-registered margin — so we do not claim the gap
is robust there. `mv_no_box2` clears the margin only barely (+0.226 against δ = 0.20). All three arms
sit between 38 and 63 cm on `pt1`, a regime in which every method we ran fails and ours is merely
least bad. And the fairness statement that must travel with this table: both arms consume the *same*
strictly causal backward flow $f_{t\to t-1}$, precomputed offline for byte-reproducibility, so the
comparison is about how the flow is used — while the caveat that our online frame rate excludes RAFT
inference (Sec. 5.7) stands untouched.

## 5.5 Where the mask-free configuration stops being sufficient

Sec. 5.1 showed the mask is redundant on 3 of 6 sequences and dominant on the other 3. We asked
whether any quantity our mask-free configuration can itself observe tracks that split, and tested one
across all 18: the mask-free arm's own **RPE** (translation, per frame). Necessity is read as
$N$, the ratio of mask-free to combined ATE,, with $N \ge 1.5$ counted as the mask being
necessary, $N \le 1.2$ as redundant, and the band between reported separately rather than forced to
a side.

The two groups **do not overlap**:

| group | mask-free RPE (cm/frame) | sequences |
|---|---|---|
| mask redundant | **0.222 – 1.572** | `f2_xyz`, `f3_office`, `f2_person`, `f1_desk`, `f3_st_xyz`, `mv_no_box`, `f3_st_rpy`, `mv_no_box2`, `pt2` |
| mask necessary | **1.717 – 2.980** | `f3_wk_xyz`, `balloon`, `f3_wk_rpy`, `f3_wk_hf`, `crowd`, `balloon2`, `pt1`, `crowd2` |

Every threshold in (1.572, 1.717) separates all 17 decided sequences. The one sequence in the
ambiguous band, `f3_st_hf` ($N = 1.21$, RPE 1.041), would fall on the predicted side if it were
counted, so its exclusion makes the statement weaker rather than stronger.

**This is not a restatement of "mask-free did badly".** `f3_st_hf` and `crowd` have nearly identical
mask-free ATE (35.59 and 34.89 cm) but $N$ differing 12.6-fold (1.21 vs 15.24), and it is RPE that
separates them (1.041 vs 2.643). Per-frame drift predicts whether the mask will help; accumulated
trajectory error does not — the same endpoint-dependence we report in Sec. 5.6.

**What this is and is not.** The separating interval is read off the same 18 sequences that define
it, with no held-out set, so it describes our benchmark rather than validating a criterion; and
computing it requires *running* the mask-free arm, so it diagnoses a configuration after the fact
rather than selecting one in advance. We state it because it is the first candidate we have found
that is a genuinely mask-free observable — the obvious alternative, sequence-level semantic area, we
tested and measured to be non-separating, and it would in any case require running the very semantic
detector a mask-free mode exists to avoid. Pre-registering this interval and testing it on unseen
sequences is the concrete next step, not a claim of this paper.

## 5.6 The pose-side mechanism, and why the endpoint must be named

A single-variable intervention — widening the share of pixels the tracking weight suppresses — moves
three pose-side endpoints in a pattern only one mechanism explains. Each shift is reported against
its own re-run noise floor, measured by repeating an identical configuration.

| endpoint | shift | floor | margin | direction |
|---|---:|---:|---:|---|
| per-frame dynamic penalty | **+0.0806** | 0.0662 | 1.22× | **worse** |
| coherent amplitude on high-dynamic frames | **−0.0248** | 0.0180 | 1.38× | **lower** |
| full-trajectory ATE | **−1.4157** cm | 0.3519 | 4.0× | **better** |

Per-frame tracking gets *worse* while the full trajectory gets *better*, and the middle quantity says
why: the coherent — drift-contributing — component of the error falls. Suppressing more pixels leaves
each frame noisier but less systematically pulled; noise averages out along a trajectory whereas bias
accumulates. This is a variance–bias trade, reported as *confirmed by measuring the intermediate
quantity* rather than inferred from the two endpoints. The consequence is the part we would carry
further: the same intervention moves two legitimate pose-side endpoints in **opposite directions**, so
a claim that tracking "got better" is not well formed without naming the endpoint, and a
per-frame-magnitude endpoint does not predict trajectory quality.

**Domain.** Only `balloon` supports this decomposition, because only it carries the per-frame dynamic
annotation the stratification needs. A cross-sequence check on `f3_wk_xyz` moved ATE in the same
direction on 3/3 seeds (26.74 → 25.72 cm) but by less than that sequence's own noise floor (1.17
against 1.26 cm), so there the ATE effect is **indistinguishable** and we claim nothing from it. The
1.38× margin on the intermediate quantity is the weakest link and would benefit from more repeats.
Confirming variance–bias as *a* mechanism also does not establish it as the only one; a map-side
contribution is not excluded.

## 5.7 Rendering, cost, and two things they do not show

Three facts belong here rather than in the supplement because they bound how the above should be
read; S5 gives each in full. **Rendering metrics do not order the arms the way trajectory error
does**: full-frame PSNR consistently rewards the arm with the *worse* trajectory, restricting it to a
static band does not rescue it, and of the four rendering metrics only **depth-L1 against
ground-truth depth** is co-ordered with ATE — so it is the only one we read as corroborating a
trajectory claim. **One cost sits outside our online figures and we name it**: optical flow is
precomputed by a frozen RAFT network at 54 ms per frame pair, bounding that branch near 18.6 fps, and
our reported online rate does not include it; efficiency is compared only between our own
configurations on identical hardware. **And seed averaging hides two dispersion facts**: an identical
configuration with an identical seed does not reproduce bit-for-bit (one pair, both completing all
873 frames, gave 15.72 vs 21.42 cm), so our cross-seed sd understates total dispersion; and on the
fully static Replica sequences the combined configuration is both worse and less stable than vanilla
(`office0` 3.82±4.58 against 0.368±0.012, one seed at 9.10 cm), so we recommend it only for sequences
already known to contain dynamic content.

---

# 6. Limitations

These are the limits on what we **claim**; the limits on how our numbers should be reproduced or read
— statistical scope, run-to-run nondeterminism, the rendering-metric caveat, the bounded map-side
interpretation, and a negative result on temporal aggregation — are in S7, and every one of them
applies to the claims below.

**1. A boundary where the mask-free configuration fails.** On `pt1` our mask-free configuration
reaches 32.41±8.51 cm and the mask recovers it to 11.89±2.36 cm, while `pt2` — same dataset, same
kind of scene, a person being tracked — needs no mask at all (0.89×). So "the mask is redundant on
person sequences" is false as stated: true of `pt2`, false of `pt1`.

**2. We do not claim state-of-the-art accuracy.** On TUM walking and person sequences our combined
configuration trails the best reported dynamic method by 1.4–2.5× (`f3_wk_xyz` 3.06 vs 2.01 and
1.22; `pt1` 11.89 vs 7.21). `pt1` is a failure region for every configuration and every counterpart
we ran, ours included. Our tables are reported in full rather than filtered to the favourable rows.

**3. The combined configuration degrades on fully static scenes.** On Replica it is both worse and
less stable than the unmodified backbone (`office0` 3.82±4.58 against 0.368±0.012, one seed at
9.10 cm; `room0` bistable too), so we recommend it only for sequences already known to contain
dynamic content. The baseline is itself bimodal on `room0`, so bistability there is partly a property
of the regime rather than only of our method.

**4. Baseline dispersion forbids some ratios entirely, and one cost sits outside our rate.** 8 of 18
sequences have vanilla CV > 20%, two above 60%; on those an improvement ratio is a function of which
basin the baseline fell into, so we quote single ratios only for CV ≤ 20% sequences — which is why
our headline bands are 2.2–4.7× and 4.2–17.1× rather than the wider numbers raw means would allow.
Separately, RAFT inference (54 ms per frame pair, bounding that branch near 18.6 fps) is precomputed
and **not** in our reported online rate; we state this as an operating condition, and an end-to-end
deployment must pay it.

**5. Generality across frameworks is untested.** All evidence here comes from a single MonoGS-based
implementation. We therefore say our system *does not require semantic segmentation within this
implementation*, and make no framework-generality claim.

**6. The reliability ablation is a joint effect of two sites.** The factorial pins
reliability-weighted candidate confirmation on in all 8 cells, so switching the component off removes
both the tracking down-weight and the weighting of the map-admission evidence. Δ_L is their joint
effect; we did not isolate the two sites and do not apportion the effect between them.

**7. The boundary diagnostic of Sec. 5.5 is fitted, not validated, and is not a selector.** Its
separating interval is read off the same 18 sequences that define it, with no held-out set, and
computing it requires running the mask-free arm, so it characterises a configuration after the fact
rather than choosing one in advance. It replaced an earlier threshold of our own that a
cross-sequence check falsified: that value was interpolated from two sequences and misclassified four
others, three of them badly. Pre-registering the interval and testing it on unseen sequences is
future work.

**8. We do not have a cue selector.** A separate campaign established that the reliability signal's
two cues are not equally good everywhere — a geometry-only setting wins on 3 of 4 sequences while the
combined setting still wins on the fourth — so a regime-dependent choice is warranted. But the
simplest candidate, sequence-level semantic area, we tested and *measured* to be non-separating: the
sequence preferring the combined setting (4.54%) sits between two preferring geometry-only (3.30% and
8.24%), so no threshold exists. It would in any case require running the semantic detector a
mask-free mode exists to avoid. We report that a selector is needed and that we do not have one.

---

# 7. Conclusion

We presented a mask-free kernel for dynamic 3DGS-SLAM and, more to the point, the measurements that
bound it: 2.2–4.7× over an unmodified backbone on the sequences whose baseline is stable enough for a
ratio to be well defined, and 4.2–17.1× with the optional mask enabled — the best-conditioned being
12.85× against a baseline whose coefficient of variation is 3%.

The findings we would keep are not the ratios. A pre-registered 120-run factorial shows that **which
components are necessary is a function of the regime**, with no sequence requiring all three and one
component actively harmful on a mixed-mover scene. A controlled counterpart consuming byte-identical
flow through a naive threshold shows the **gain does not follow from the information alone**. And
three pose-side endpoints, including a directly measured intermediate quantity, show a
**variance–bias trade** in which per-frame tracking worsens while the trajectory improves — from
which follows a discipline that outlives this system: name the endpoint.

We are equally clear about the boundary. Segmentation is redundant on some sequences and dominant on
others; our mask-free configuration fails outright on one person sequence; the combined configuration
is worse than the unmodified backbone on fully static scenes. Across all 18 sequences the mask-free
arm's own per-frame drift separates the mask-redundant from the mask-necessary group without overlap,
the most concrete handle we have on *when* to enable the mask — but it is fitted to these sequences
and requires running the mask-free arm first, so we report it as a diagnostic rather than a selector.
Pre-registering it and testing it on unseen sequences, and finding a cue selector built from
mask-free observables, are the two pieces of future work this evidence most directly sets up.

---

# Evidence appendix (not part of the submitted paper)

Anchors for every competitor statement in §2. Line numbers are from
`pdftotext resources/01-references/<X>.pdf`; full quotes in
`results/evidence/competitor_protocol_table.md` §3.

| Claim in §2 | Source |
|---|---|
| DynaSLAM uses Mask R-CNN for pixel-wise semantic segmentation | DynaSLAM L199, L208–209 |
| NGD-SLAM uses YOLO detection | NGD-SLAM L72 |
| RoDyn-SLAM fuses optical-flow mask with semantic segmentation mask | RoDyn-SLAM L92–93 |
| RGD-SLAM uses COCO-pretrained OneFormer | RGD-SLAM L568, L363 |
| DG-SLAM uses OneFormer + DROID-VO + DROID-VO keyframe selection | DG-SLAM L804, L83, L805–806 |
| DG-SLAM runs dense BA upon completion of tracking | DG-SLAM L91–92 |
| BDGS-SLAM uses YOLOv5 + Bayesian per-Gaussian prior | BDGS-SLAM L49 |
| DAGS-SLAM fuses YOLO instance priors, on-demand scheduler | DAGS-SLAM L14, L607 |
| DynaGSLAM uses RAFT blobs + SAM2, poses from DynoSAM unmodified | DynaGSLAM L261–268 |
| WildGS-SLAM uses finetuned 3D-aware DINOv2 + Metric3D v2 | WildGS-SLAM L291–293, L306 |
| WildGS-SLAM "Prior Free" definition (class priors only) | WildGS-SLAM Table 7 caption |
| WildGS-SLAM is monocular; final global BA after all frames | WildGS-SLAM L24; "Final Global BA" |
| Co-SLAM global BA over all past keyframes | Co-SLAM L106, L43 |
| MonoGS keyframe window $W_k$ / no pretrained predictor / no loop closure | MonoGS L393, L103, L521+L526 |

Anchors for §3 (our own method). Every constant and every attachment point was read back from the
resolved configuration of a reported run and from the source, **not** from prose; the full audit,
including three errors it corrected in an earlier draft of this section, is
`results/evidence/method_attachment_audit.md`.

| Claim in §3 | Source |
|---|---|
| `gap_cap = 5`, keyframe density 0.045–0.075 → 0.198–0.204 kf/frame | `scripts/measure_keyframe_coverage.py`; resolved `DynamicKeyframe` |
| Huber IRLS, $\delta_{\text{rgb}}=\delta_{\text{depth}}=0.1$, detached, per-iteration | `utils/slam_utils.py:439-453` `_robust_irls_weight`; resolved `RobustTracking` |
| $s=(1-e_{\text{flow}})(1-vg)$, MAD normaliser, `flow_scale_floor = 2.0` | `utils/reliability_signal.py`; resolved `ReliabilitySignal` |
| computed once per frame at `warmup_iters = 10`, then frozen | `utils/slam_frontend.py:1136-1141` |
| **site 1** — tracking RGB *and* depth residual, weight floored at 0.10 | `utils/slam_frontend.py:1213,1294-1310` → `utils/slam_utils.py:541-594` (`static_conf = clamp(w, 0.10, 1)`) |
| **site 2** — reliability-weighted candidate confirmation $C^\pm$ | `utils/slam_frontend.py:1284-1290` (stash) → `utils/deferred_commit.py:141-144,427-456` |
| reliability off ⇒ confirmation reverts to integer counts | `utils/deferred_commit.py:17-29`; E0 gate table in `wpa_reliability_contribution.md` §1 |
| mapping loss + insertion gate belong to `SemanticMask`, not to reliability | `utils/slam_backend.py:429,484` → `utils/semantic_mask.py:88`; `utils/slam_frontend.py:863-870` |
| hard mask active only before `warmup_iters` | dispatch in `utils/slam_utils.py:132-154` (`hard_tracking_mask` unset ⇒ soft branch bypasses it) |
| lineage lifecycle: 3 arms, `immediate` = stock MonoGS | `utils/deferred_commit.py:35-56` `lifecycle_mode` docstring |
| deleted-lineage fraction median 0.55, range 0.27–0.81; contradiction median 6%, max 15% | 45 × `results/runs/P6/**/deferred_commit_summary.json` |
| withheld-candidate variant worse on 4/6 sequences (not adopted) | `our_method/03-results.md` R2-P01-E2 / E2 full-length row |
| `occ_tighten_thresh = 2.0` inert (twice over) | `utils/slam_frontend.py:1647,1657-1661`; `dyn_cov` ∈ [0,1] at `:863-870` |

Anchors for §4 (our own protocol):

| Claim in §4 | Source |
|---|---|
| SE(3) Umeyama, no scale for RGB-D | `utils/eval_utils.py:95` `align_trajectory(..., correct_scale=monocular)`, monocular=False |
| ATE = full-trajectory `ate_rmse_cm` | `tracking_raw.csv` schema; console KF-RMSE is a different quantity |
| 95% completion gate | `results/evidence/wpa_factorial_prereg.md`, `wpm_maskonly_prereg.md` |
| run-to-run 15.72 vs 21.42 cm, 873/873 both | `results/evidence/main_table_provenance_audit.md` |
| latest-run provenance rule + duplicate footer | `scripts/build_18seq_main_table.py:read_ate` + table footer |
| online-phase efficiency definition | `efficiency_raw.csv` notes field; `efficiency_stability_tables.md` |
| keyframe coverage measurement | `scripts/measure_keyframe_coverage.py` |
| refinement does not optimise poses | `utils/slam_backend.py: color_refinement()` (steps `gaussians.optimizer` only) |
| frame counts per sequence | loader `num_frames`, cross-checked constant across all runs of each sequence |

---

**Draft status: v1, exp46 (2026-08-25). All seven sections selected down from v0.
MEASURED BY REAL COMPILE with all three figures in place: `latex/main_v1.tex` builds to
**18 pages** under `llncs.cls` (真 abstract 203 词, 三图齐全, 无参考文献; LNCS 把引用放在 12 页正文之外).
Against that limit **v2 owes ~6 pages** — more than the 4.35 the old estimate implied, because
that estimate used 520 words/page (real: ~477) and allowed 0.50 page for the title block and
abstract (real: 1.48). The build also caught a silent fault worth knowing about: XeTeX was
dropping every Unicode minus sign, which would have printed §5.2's load-bearing
Δ_K(balloon) = −0.182 as "0.182"; the converter now refuses to emit non-ASCII at all.
Calibration and the full defect list: `results/evidence/latex_page_rate_calibration.md`.
Regenerate with `scripts/md2latex_manuscript.py --figdir papers/maskfree_bundle/figures`.
v0 record: `manuscript_v0.md`.**
