"""Fig. 1 (v6) - where the four components attach to the MonoGS backbone.

What was wrong with the printed v3, and what changed:

1. SIZE. v3 was drawn 12.2 cm wide but included at 0.73\\textwidth, so its 7 pt
   labels printed at about 5.1 pt. The figure read as crowded because it was
   scaled to 73 %. This version is drawn 12.2 cm wide and included at
   \\textwidth, so every label prints at its drawn size; the extra height is
   bought back by tightening the three vertical bands.
2. ALIGNMENT. Every box is sized from its own label (measured with TextPath),
   R, K and D share one baseline and one height, and each blue arrow rises from
   its component's centre straight into the centre of the backbone box it feeds.
   v3 drew D taller and higher than R and K, with its arrow off-centre.
3. ROUTING. The mask feeds the backbone from above: one dashed trunk in the
   lane between K and D, one dashed bus above the backbone, and three stubs
   dropping onto the tops of its consumers, offset from the blue arrows so no
   line is collinear with another. In v3 the bus ran in the same corridor as the
   three component arrows and the stubs had to dodge them. L's site-2 edge
   leaves the right side of L and runs along the bottom margin, instead of
   squeezing between the reliability box and the component row.

Topology is unchanged (results/evidence/method_attachment_audit.md): R -> pose
solve residual, K -> keyframe gate, D -> candidate confirm/delete; L consumed at
exactly two sites (tracking residual, candidate confirmation); the optional mask
at mapping loss, keyframe insertion and the tracking warm-up.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as _MPath
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

from scripts._figstyle_v3 import C, TEXTWIDTH, apply_style, save

apply_style(font_size=7)
PT2CM = 2.54 / 72
WIDTH_CM = 12.2


def text_w(label, fs):
    """Width in data units (1 unit = 1 cm) of a label's widest line."""
    fp = FontProperties(family="DejaVu Sans", size=fs)
    return max(TextPath((0, 0), ln, prop=fp, usetex=False).get_extents().width
               for ln in label.split("\n")) * PT2CM


BLUE_BG = "#DCE9F5"
BLUE_ED = C["combined"]
ORG = "#B26B2C"
ORG_BG = "#F5E3CE"
GREY_BG = "#EFEFEF"
GREY_ED = "#B9B9B9"
MASK = "#9A9A9A"

# ------------------------------------------------------------------ layout ---
MARGIN = 0.22
SITE2_Y = 0.03          # the one long horizontal, in its own channel
L_Y, L_H = 0.05, 0.95
CT_Y, CT_H, CFS = 1.06, 0.80, 7.2
BB_Y, BB_H, BFS = 2.28, 0.40, 6.9
BUS_Y = 2.86
STUB_DX = 0.34                      # mask stubs drop left of each blue arrow
CGAP = 0.34                         # min horizontal gap between component boxes
H = 3.14

comp_labels = {
    "pose solve":     "robust reweighting (R)\nHuber residual weight",
    "keyframe\ngate": "uniform keyframe\ncoverage (K)",
    "Gaussian map":   "lineage lifecycle (D)\nconfirm / delete\nnew Gaussians",
}
cw = {k: text_w(v, CFS) + 0.24 for k, v in comp_labels.items()}
bb_min = {"frame $t$": 1.00, "pose solve": 1.20, "keyframe\ngate": 1.15,
          "window BA": 1.30, "Gaussian map": 1.55}
bw = {k: max(text_w(k, BFS) + 0.26, m) for k, m in bb_min.items()}

order = ["frame $t$", "pose solve", "keyframe\ngate", "window BA", "Gaussian map"]
kg = "keyframe\ngate"
# R sits under pose solve and K under keyframe gate, so those two centres must
# be at least one component-width apart; the other gaps are free.
g2_min = (cw["pose solve"] + cw[kg]) / 2 + CGAP - (bw["pose solve"] + bw[kg]) / 2
gaps = [0.80, g2_min, 0.80, 0.80]
used = sum(bw.values()) + sum(gaps) + 2 * MARGIN
slack = (WIDTH_CM - used) / len(gaps)
if slack < 0:
    raise SystemExit(f"layout {-slack:.2f} cm too wide")
gaps = [g + slack for g in gaps]

c, x = {}, MARGIN
for k, g in zip(order, gaps + [0]):
    c[k] = x + bw[k] / 2
    x += bw[k] + g

fig = plt.figure(figsize=(TEXTWIDTH, H / 2.54))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH_CM)
ax.set_ylim(0, H)
ax.axis("off")


def box(x, y, w, h, label, face, edge, fs=7.0, lw=0.9, ls="-", z=2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
        facecolor=face, edgecolor=edge, lw=lw, linestyle=ls, zorder=z))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, color=C["ink"], zorder=z + 1, linespacing=1.26)


def arrow(x1, y1, x2, y2, color, lw=1.0, z=3, ls=None, ms=7):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=ms,
        lw=lw, color=color, zorder=z, shrinkA=1.5, shrinkB=1.5, linestyle=ls))


# ============================ backbone row (grey) ===========================
for k in order:
    box(c[k] - bw[k] / 2, BB_Y, bw[k], BB_H, k, GREY_BG, GREY_ED)
for prev, cur in zip(order, order[1:]):
    arrow(c[prev] + bw[prev] / 2, BB_Y + BB_H / 2,
          c[cur] - bw[cur] / 2, BB_Y + BB_H / 2, "#8A8A8A")

# =========================== component row (blue) ===========================
for k, label in comp_labels.items():
    box(c[k] - cw[k] / 2, CT_Y, cw[k], CT_H, label, BLUE_BG, BLUE_ED, fs=CFS)
    arrow(c[k], CT_Y + CT_H, c[k], BB_Y, BLUE_ED, lw=1.1)

# ================ reliability signal L: exactly TWO out-edges ==============
L_LABEL = "reliability signal (L)\n$s=(1-e_{\\mathrm{flow}})(1-vg)$"
L_W = text_w(L_LABEL, 8.8) + 0.50
box(MARGIN, L_Y, L_W, L_H, L_LABEL, ORG_BG, ORG, fs=8.8)

# site 1: straight up into R, on R's own centre line
c_r, c_d = c["pose solve"], c["Gaussian map"]
arrow(c_r, L_Y + L_H, c_r, CT_Y, ORG, lw=1.3)
ax.text(c_r + 0.12, (L_Y + L_H + CT_Y) / 2, "site 1", fontsize=6.8,
        color="#8A4E17", ha="left", va="center", fontweight="bold")

# site 2: out of L's right side, along the bottom margin, up into D from below
s2x = MARGIN + L_W
ax.add_patch(FancyArrowPatch(
    path=_MPath([(s2x, L_Y + L_H / 2), (s2x + 0.20, L_Y + L_H / 2),
                 (s2x + 0.20, SITE2_Y), (c_d, SITE2_Y), (c_d, CT_Y)],
                [_MPath.MOVETO, _MPath.LINETO, _MPath.LINETO, _MPath.LINETO,
                 _MPath.LINETO]),
    arrowstyle="-|>", mutation_scale=7, lw=1.3, color=ORG, zorder=3,
    shrinkA=0, shrinkB=0.5))
ax.text(c_d - 0.12, SITE2_Y + 0.20, "site 2", fontsize=6.8, color="#8A4E17",
        ha="right", va="center", fontweight="bold")

# ==================== optional semantic mask (dashed) =======================
M_LABEL = "optional semantic mask\n(person, combined only)"
M_W = text_w(M_LABEL, 7.0) + 0.44
# trunk rises in the lane between K's box and D's, which carries no other line
TRUNK_X = (c[kg] + cw[kg] / 2 + c["Gaussian map"] - cw["Gaussian map"] / 2) / 2
box(TRUNK_X - M_W / 2, L_Y, M_W, L_H, M_LABEL, "white", MASK, fs=7.0,
    ls="--", lw=0.8)

ax.add_patch(FancyArrowPatch(
    path=_MPath([(TRUNK_X, L_Y + L_H), (TRUNK_X, BUS_Y)],
                [_MPath.MOVETO, _MPath.LINETO]),
    arrowstyle="-", lw=0.9, color=MASK, zorder=2, linestyle=(0, (3.5, 2.2)),
    shrinkA=0, shrinkB=0))
stubs = [c[k] - STUB_DX for k in ("pose solve", kg, "window BA")]
ax.add_patch(FancyArrowPatch(
    path=_MPath([(min(stubs), BUS_Y), (max(stubs + [TRUNK_X]), BUS_Y)],
                [_MPath.MOVETO, _MPath.LINETO]),
    arrowstyle="-", lw=0.9, color=MASK, zorder=2, linestyle=(0, (3.5, 2.2)),
    shrinkA=0, shrinkB=0))
for x_stub in stubs:
    ax.add_patch(FancyArrowPatch(
        (x_stub, BUS_Y), (x_stub, BB_Y + BB_H), arrowstyle="-|>",
        mutation_scale=5, lw=0.9, color=MASK, zorder=2, shrinkA=0, shrinkB=0))

ax.text(MARGIN, H - 0.12, "MonoGS backbone", fontsize=6.9,
        color="#8A8A8A", fontweight="bold", ha="left", va="center")

# ----------------------------------------------------------------- checks ----
print(f"canvas {WIDTH_CM:.2f} x {H:.2f} cm")
for k in order:
    print(f"  {k!r:22} bb {c[k]-bw[k]/2:5.2f}..{c[k]+bw[k]/2:5.2f}"
          + (f"  comp {c[k]-cw[k]/2:5.2f}..{c[k]+cw[k]/2:5.2f}" if k in cw else ""))
print("  bb gaps " + " ".join(f"{c[b]-bw[b]/2-(c[a]+bw[a]/2):+.2f}"
                              for a, b in zip(order, order[1:])))
rk = c[kg] - cw[kg] / 2 - (c["pose solve"] + cw["pose solve"] / 2)
kd = c["Gaussian map"] - cw["Gaussian map"] / 2 - (c[kg] + cw[kg] / 2)
print(f"  comp gaps R->K {rk:+.2f}  K->D {kd:+.2f}")
print(f"  L {MARGIN:.2f}..{MARGIN+L_W:.2f}"
      f" | mask {TRUNK_X-M_W/2:.2f}..{TRUNK_X+M_W/2:.2f} | trunk {TRUNK_X:.2f}"
      f" | right {c['Gaussian map']+bw['Gaussian map']/2:.2f}")
save(fig, "fig1_pipeline_v6")
