"""Fig. 5 (v6) - two controlled comparisons, side by side.

Layout change relative to the printed v5 (which stacked the two panels): the
stack cost 210 pt of page height for two panels that are each only ~100 pt
tall, because each row repeated its own tick strip and the two were separated
by hspace.  Side by side they share one row, so the figure drops to roughly
110 pt -- the single largest page saving available without touching the text.

Every legibility guarantee of v5 is kept:
  * drawn at exactly \\textwidth, saved without bbox crop, included at
    \\textwidth, so scale is 1.000 and 7 pt text prints at 7 pt;
  * two-line axis categories and shortened legend labels, because each panel
    is now ~4.9 cm wide and the full labels would collide (measured: the old
    "naive p90, same flow" is 2.61 cm, the old legend row 8.14 cm);
  * audit() still checks printed size, label-on-label overlap, canvas bounds,
    and the y-tick clearance on both panels.

Panel (a) is the standard three-arm ablation bar chart: same frozen flow, three
consumers (none / naive p90 threshold / our weighting), ATE bars with per-seed
dots.  Panel (b) keeps the boundary separation scatter: two non-overlapping
groups, one gap.

Data: panel (a) reads results/runs_remote_cache/WPB/WPB-CONFIRM per-seed
tracking_raw.csv (36 runs); panel (b) reuses the transcription-checked 18 + 5
points of make_v3_fig45_combined.py, sourced from
results/evidence/rpe_stratification_rule_test.{json,md} +
rpe_boundary_heldout.{json,md}.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from scripts._pubstyle import (C, TEXTWIDTH, apply_style, save_exact, audit,
                               panel_label, text_w, crop_vertical)

apply_style(font_size=7)

FS_TICK = 7.0
FS_LABEL = 7.2
FS_LEGEND = 7.0
FS_VALUE = 6.8      # value labels: 6.8 pt still clears the 6.0 pt floor and our
                    # 6.6 pt target, and at this size 12 horizontal labels fit

SEQ = ["pt1", "pt2", "mv_no_box2", "balloon2"]
SEQ_TICK = ["pt1", "pt2", "mv_no\nbox2", "balloon\n2"]
ARMS = [("vanilla", "vanilla", C["vanilla"]),
        ("flowmask", "naive p90", C["naive"]),
        ("MRCS", "ours", C["combined"])]

# Per-seed ATE RMSE (cm), transcribed from
# results/runs_remote_cache/WPB/WPB-CONFIRM/{arm}_{seq}_{seed}/tables/tracking_raw.csv
# (last row, column ate_rmse_cm). 36 runs, 3 arms x 4 sequences x 3 seeds.
SEED_ATE = {
    "pt1|vanilla": [76.92, 55.63, 57.10],
    "pt1|flowmask": [62.11, 39.76, 52.36],
    "pt1|MRCS": [41.54, 37.49, 36.51],
    "pt2|vanilla": [45.15, 43.45, 47.50],
    "pt2|flowmask": [61.84, 39.67, 51.69],
    "pt2|MRCS": [9.40, 8.78, 9.09],
    "mv_no_box2|vanilla": [6.88, 5.88, 34.16],
    "mv_no_box2|flowmask": [6.61, 5.74, 6.35],
    "mv_no_box2|MRCS": [4.90, 4.71, 5.29],
    "balloon2|vanilla": [23.39, 24.40, 24.50],
    "balloon2|flowmask": [31.10, 11.37, 27.44],
    "balloon2|MRCS": [14.23, 10.92, 10.54],
}
D = {(s, a): np.array(SEED_ATE[f"{s}|{a}"]) for s in SEQ for a, _, _ in ARMS}

# ---- boundary data (transcription-checked, identical to v3) ----
DEV = [
    ("f2_xyz", 0.222, 0.99, "redundant"), ("f3_office", 0.456, 1.02, "redundant"),
    ("f2_person", 0.498, 0.92, "redundant"), ("f1_desk", 0.847, 1.07, "redundant"),
    ("f3_st_xyz", 0.910, 0.57, "redundant"), ("mv_no_box", 1.210, 1.17, "redundant"),
    ("f3_st_rpy", 1.465, 1.02, "redundant"), ("mv_no_box2", 1.521, 1.09, "redundant"),
    ("pt2", 1.572, 0.89, "redundant"), ("f3_st_hf", 1.041, 1.21, "ambiguous"),
    ("f3_wk_xyz", 1.717, 8.76, "necessary"), ("balloon", 2.028, 3.96, "necessary"),
    ("f3_wk_rpy", 2.264, 3.41, "necessary"), ("f3_wk_hf", 2.327, 5.27, "necessary"),
    ("crowd", 2.643, 15.24, "necessary"), ("balloon2", 2.730, 1.92, "necessary"),
    ("pt1", 2.894, 2.73, "necessary"), ("crowd2", 2.980, 20.95, "necessary"),
]
HELD = [("obox2", 2.068, 1.62, "necessary"), ("synchronous", 2.424, 138.97, "necessary"),
        ("f2_desk_wp", 0.602, 0.94, "redundant"), ("f3_loh", 0.456, 1.09, "redundant"),
        ("obox", 2.117, 1.42, "in-band")]
TAU, BAND = 1.6445, (1.572, 1.717)

H_CM = 5.10
fig = plt.figure(figsize=(TEXTWIDTH, H_CM / 2.54))
# (b)'s width is pinned by its x label ("mask-free arm's own RPE (cm/frame)",
# 4.57 cm at 7.2 pt), so it takes 4.6 of the 11.55 cm usable and (a) -- which
# carries 12 numeric value labels -- gets the remaining ~6.9 cm.
# (b)'s width is pinned by its x label.  The full "mask-free arm's own RPE
# (cm/frame)" is 4.57 cm at 7.2 pt, which starves (a): its 12 value labels are
# 13.6 pt wide on a 10.9 pt bar pitch and collide.  The label is shortened to
# 3.21 cm ("mask-free" already names the arm, and the caption says which arm),
# which lets (a) take 7.0 cm where the pitch is 16.5 pt and nothing collides.
# Width budget (all measured): (a)'s 12 horizontal value labels need the bar
# pitch >= ~14 pt, and (b) needs >= 3.8 cm to keep its 18 + 5 points legible.
# left 0.098 = y label + y ticks; right 0.982 = outer margin.
gs = fig.add_gridspec(1, 2, width_ratios=[5.9, 4.1],
                      left=0.098, right=0.982, top=0.845, bottom=0.285,
                      wspace=0.30)

# ====================== (a) three-arm bar chart =============================
ax = fig.add_subplot(gs[0])
x = np.arange(len(SEQ))
# w is solved, not chosen: in a 6.4 cm panel each data unit is ~45 pt, and a
# horizontal value label is 14 pt, so the bar pitch must be >= 0.34 units for
# adjacent labels to clear.  (v5 was stacked and 12.2 cm wide, hence w=0.27.)
w = 0.37
label_artists = {}          # (i, j) -> Text, resolved after the first draw
for j, (key, label, col) in enumerate(ARMS):
    offs = (j - 1) * w
    means = [float(np.mean(D[(s, key)])) for s in SEQ]
    sds = [float(np.std(D[(s, key)])) for s in SEQ]
    ax.bar(x + offs, means, w * 0.88, color=col, edgecolor="white",
           linewidth=0.4, zorder=2, label=label)
    ax.errorbar(x + offs, means, yerr=sds, fmt="none", ecolor=C["ink"],
                elinewidth=0.6, capsize=1.2, capthick=0.6, zorder=3)
    for i, s in enumerate(SEQ):
        ax.plot(np.full(3, x[i] + offs) + np.linspace(-0.030, 0.030, 3),
                D[(s, key)], "o", ms=1.6, mfc="white", mec=C["ink"], mew=0.45,
                zorder=4)
        label_artists[(i, j)] = ax.text(
            x[i] + offs, (means[i] + sds[i]) * 1.12, f"{means[i]:.1f}",
            ha="center", va="bottom", fontsize=FS_VALUE, color=C["ink"],
            rotation=90, zorder=5)

ax.set_yscale("log")
ax.set_ylim(3, 500)
ax.set_yticks([5, 20, 100])
ax.set_yticklabels(["5", "20", "100"], fontsize=FS_TICK)
ax.set_ylabel("ATE RMSE (cm)", fontsize=FS_LABEL)
ax.set_xticks(x)
ax.set_xticklabels(SEQ_TICK, fontsize=FS_TICK, linespacing=1.15)
ax.set_xlim(-0.62, len(SEQ) - 0.38)
ax.grid(axis="y", zorder=0)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.005), ncol=3,
          handlelength=0.85, columnspacing=1.0, borderaxespad=0.0,
          labelspacing=0.20, fontsize=FS_LEGEND - 0.3, handletextpad=0.35,
          frameon=False)
panel_label(ax, "a", x=-0.175, y=1.045, size=8.6)

# ====================== (b) boundary separation =============================
ax2 = fig.add_subplot(gs[1])
ax2.axvspan(*BAND, color=C["panel_bg"], zorder=0)
ax2.axvline(TAU, color="#909090", lw=0.7, ls="--", zorder=1)

groups = {"redundant": ([], []), "necessary": ([], []), "ambiguous": ([], [])}
for name, rpe, n, g in DEV:
    groups[g][0].append(rpe)
    groups[g][1].append(n)
MARK = {"redundant": ("o", C["redundant"]), "necessary": ("D", C["necessary"]),
        "ambiguous": ("^", "#8C8C8C")}
for g, (mk, col) in MARK.items():
    xs, ys = groups[g]
    edge_col, mew = (C["ink"], 0.9) if g == "ambiguous" else ("white", 0.4)
    ax2.plot(xs, ys, mk, ms=3.4 if mk != "^" else 4.0, mfc=col, mec=edge_col,
             mew=mew, ls="none", zorder=3)
ax2.plot([r for _, r, _, _ in HELD], [n for _, _, n, _ in HELD], "o", ms=4.6,
         mfc="none", mec=C["ink"], mew=0.8, ls="none", zorder=4)
ax2.plot([], [], "o", ms=4.0, mfc="none", mec=C["ink"], mew=0.8, ls="none",
         label="held-out (5)")

for name, rpe, n, g in DEV:
    if name in ("crowd", "f3_st_hf"):
        dy = 1.5 if g != "ambiguous" else 0.62
        ax2.annotate(name, (rpe, n), xytext=(rpe + 0.06, n * dy),
                     fontsize=FS_LEGEND - 0.4, color="#606060", zorder=5)

ax2.set_yscale("log")
ax2.set_ylim(0.45, 400)
ax2.set_xlim(0.0, 3.25)
ax2.set_xticks([0, 1, 2, 3])
for t in ax2.get_xticklabels(minor=True) + ax2.get_xticklabels():
    t.set_clip_on(True)
ax2.set_yticks([0.5, 2, 10, 50, 200])
ax2.set_yticklabels(["0.5", "2", "10", "50", "200"], fontsize=FS_TICK)
ax2.tick_params(axis="x", which="both", labelsize=FS_TICK)
ax2.set_ylabel("mask necessity $N$", fontsize=FS_LABEL)
ax2.set_xlabel("mask-free arm's own\nRPE (cm/frame)", fontsize=FS_LABEL - 0.2,
               labelpad=2.0, linespacing=1.15)
ax2.grid(axis="y", zorder=0)
# No "gap" annotation: the caption already defines the grey band as the
# empirical gap, and inside a 2.8 cm panel the word collided with the
# f3_st_hf marker at every position that stayed inside the band.

handles, _ = ax2.get_legend_handles_labels()
GROUP_LAB = {"redundant": "redundant (9)", "necessary": "necessary (8)",
             "ambiguous": "ambiguous (1)"}
for g, (mk, col) in MARK.items():
    edge_col, mew = (C["ink"], 0.9) if g == "ambiguous" else ("white", 0.4)
    handles.append(Line2D([], [], marker=mk, ms=3.8, mfc=col, mec=edge_col,
                          mew=mew, ls="none", label=GROUP_LAB[g]))
ax2.legend(handles, [h.get_label() for h in handles], loc="upper left",
           ncol=1, handlelength=0.75, columnspacing=0.7, borderaxespad=0.15,
           labelspacing=0.20, fontsize=FS_LEGEND - 0.3, handletextpad=0.30,
           framealpha=0.95, frameon=True, edgecolor="#DDDDDD")
panel_label(ax2, "b", x=-0.145, y=1.005, size=8.6)

# ---------------------------------------------------------------- checks ----
fig.canvas.draw()
r = fig.canvas.get_renderer()


def resolve_labels(ax, artists, max_steps=14):
    """Raise any value label that overlaps a neighbour, then re-check.

    Bars that sit at nearly the same height (pt2: 45.4 / 51.1 / 51.4) put their
    labels on top of each other no matter how wide the bar pitch is, because the
    collision is vertical, not horizontal.  Each label is lifted in small
    multiplicative steps in axis coordinates until its rendered box clears every
    other label box in the same panel.  This runs on the drawn figure, so the
    result is measured, not assumed.
    """
    order = list(artists)
    for _ in range(max_steps):
        boxes = {k: artists[k].get_window_extent(r) for k in order}
        moved = False
        for a in range(len(order)):
            for b in range(a + 1, len(order)):
                ka, kb = order[a], order[b]
                ba, bb = boxes[ka], boxes[kb]
                # require a real clearance, not just non-overlap: a 1-2 pt
                # touch still shows as collision in the placed figure
                pad = 0.8 * fig.dpi / 72.0        # 0.8 pt
                ox = min(ba.x1, bb.x1) - max(ba.x0, bb.x0)
                oy = min(ba.y1, bb.y1) - max(ba.y0, bb.y0)
                if ox <= -pad or oy <= -pad:
                    continue
                # lift the label whose bar is higher (it has room to move up)
                hi, lo = (ka, kb) if ba.y0 > bb.y0 else (kb, ka)
                t = artists[hi]
                xd, yd = t.get_position()
                t.set_position((xd, yd * 1.10))
                moved = True
        if not moved:
            return True
        fig.canvas.draw()
    return False


if not resolve_labels(ax, label_artists):
    raise SystemExit("could not resolve value-label collisions in panel (a)")
print("  value labels resolved: none overlap in panel (a)")

for name, a in (("a", ax), ("b", ax2)):
    bbs = sorted((t.get_window_extent(r) for t in a.get_yticklabels()
                  if t.get_text()), key=lambda b: b.y0)
    gaps = [u.y0 - v.y1 for v, u in zip(bbs, bbs[1:])]
    if gaps:
        tight = min(gaps) * 72 / fig.dpi
        print(f"  panel ({name}) y-tick gap: min {tight:.1f} pt")
        if tight < 4.0:
            raise SystemExit(f"panel ({name}) y ticks only {tight:.1f} pt clear")
# each panel's x tick labels must not collide within the panel
for name, a in (("a", ax), ("b", ax2)):
    bbs = sorted((t.get_window_extent(r) for t in a.get_xticklabels()
                  if t.get_text()), key=lambda b: b.x0)
    gaps = [u.x0 - v.x1 for v, u in zip(bbs, bbs[1:])]
    if gaps:
        tight = min(gaps) * 72 / fig.dpi
        print(f"  panel ({name}) x-tick gap: min {tight:.1f} pt")
        if tight < 1.5:
            raise SystemExit(f"panel ({name}) x tick labels only {tight:.1f} pt apart")
print(f"  panel widths: a {ax.get_window_extent(r).width*2.54/fig.dpi:.2f} cm, "
      f"b {ax2.get_window_extent(r).width*2.54/fig.dpi:.2f} cm")
print(f"  height {H_CM:.2f} cm (v5 stacked was 7.40 cm)")

crop_vertical(fig)
audit(fig, "fig5", scale=1.0)
save_exact(fig, "fig5_controlled_comparison_v6")
