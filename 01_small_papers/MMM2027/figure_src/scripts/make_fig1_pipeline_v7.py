"""Fig. 1 (v7) - where the four components attach to the MonoGS backbone.

What the printed v6 got wrong, measured on the delivered PDF:

* BOX OVERFLOW. The "lineage lifecycle (D) / confirm / delete / new Gaussians"
  label is 3 lines in a 0.80 cm box; at 7.2 pt with linespacing 1.26 it needs
  27.2 pt and the box offers 22.7 pt, so the text hung out of the border.
  Every box height is now solved from its own label block plus padding.
* STUB ARROWS. The component->backbone arrows were 11.9 pt and the site-1 stub
  1.7 pt; both read as nubs. The vertical bands are now sized so that no edge is
  shorter than MIN_EDGE_PT, and the module asserts this.
* MASK ROUTING. v6 sent the mask up a trunk between K and D to a bus above the
  backbone, leaving 5.1 pt stubs. The mask box now sits at the right end of its
  own band and the bus leaves it horizontally, so the three drops to the
  backbone have a real length and no line crosses another.
* SITE 2. The long bottom run to D is kept (it is the only way to reach D from a
  bottom-left L without crossing the mask lane) but it is now the only line in
  that lane.

Topology is unchanged (results/evidence/method_attachment_audit.md): R -> pose
solve residual, K -> keyframe gate, D -> candidate confirm/delete; L consumed at
exactly two sites (tracking residual, candidate confirmation); the optional mask
at mapping loss, keyframe insertion and the tracking warm-up.
"""
import math

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as _MPath

from scripts._pubstyle import (C, TEXTWIDTH, apply_style, save_exact, audit,
                               text_w, block_h, PT2CM, WIDTH_CM, min_seg,
                               crop_vertical)

apply_style(font_size=7)
plt.rcParams["font.size"] = 7

# ------------------------------------------------------------------ palette ---
BLUE_BG, BLUE_ED = "#DCE9F5", C["combined"]
ORG, ORG_BG = "#B26B2C", "#F5E3CE"
GREY_BG, GREY_ED = "#EFEFEF", "#B9B9B9"
MASK = "#9A9A9A"
INK = C["ink"]

# ------------------------------------------------------------------- sizes ---
FS_BB = 7.0          # backbone boxes
FS_COMP = 7.2        # component boxes
FS_L = 7.6           # reliability-signal box
FS_MASK = 7.0        # semantic-mask box
FS_SITE = 6.9        # the two site tags
LS = 1.26            # linespacing used for every multi-line label

PAD_Y = 0.10         # cm of vertical padding inside a box
PAD_X = 0.14         # cm of horizontal padding inside a box
MARGIN = 0.20        # cm left/right canvas margin
MIN_EDGE_PT = 12.0   # no edge (arrow or stub) shorter than this

BACKBONE = ["frame $t$", "pose solve", "keyframe gate", "window BA",
            "Gaussian map"]
COMPONENTS = {
    "pose solve": "robust reweighting (R)\nHuber residual weight",
    "keyframe gate": "uniform keyframe\ncoverage (K)",
    "Gaussian map": "Gaussian lineage (D)\nconfirm / delete / new",
}
LAB_L = "reliability signal (L)\nstatic confidence $s$"
LAB_M = "optional semantic mask\n(person, combined only)"


def box_h(label, fs):
    return block_h(label, fs, LS) + 2 * PAD_Y


# ------------------------------------------------------- horizontal layout ---
bb_w = {k: text_w(k, FS_BB) + 2 * PAD_X for k in BACKBONE}
cp_w = {k: text_w(v, FS_COMP) + 2 * PAD_X for k, v in COMPONENTS.items()}

GAP_MIN = 0.42
gaps = [GAP_MIN] * 4
used = sum(bb_w.values()) + sum(gaps) + 2 * MARGIN
slack = (WIDTH_CM - used) / len(gaps)
if slack < 0:
    raise SystemExit(f"backbone row {-slack:.2f} cm too wide")
gaps = [g + slack for g in gaps]

cx, x = {}, MARGIN
for k, g in zip(BACKBONE, gaps + [0]):
    cx[k] = x + bb_w[k] / 2
    x += bb_w[k] + g

# Component boxes need not sit exactly under a backbone centre: an arrow only
# has to land *inside* the backbone box it feeds.  Placing them at the centres
# exactly (what v6 did) collides R and K, because those two component boxes are
# together wider than the two backbone boxes they hang from.  Solve instead for
# positions that (a) keep each arrow inside its consumer, and (b) keep the
# component boxes apart.
CP_ORDER = ["pose solve", "keyframe gate", "Gaussian map"]
ARROW_PAD = 0.12          # cm of backbone box kept clear on each side
CP_GAP = 0.34             # cm between adjacent component boxes

lo = {k: cx[k] - bb_w[k] / 2 + ARROW_PAD for k in CP_ORDER}
hi = {k: cx[k] + bb_w[k] / 2 - ARROW_PAD for k in CP_ORDER}

cpc = {}                  # component centre x
# R: as far left as still inside pose-solve
cpc["pose solve"] = lo["pose solve"]
# K: as far right as still inside keyframe-gate, and clear of R
k_min = cpc["pose solve"] + cp_w["pose solve"] / 2 + CP_GAP + cp_w["keyframe gate"] / 2
cpc["keyframe gate"] = max(lo["keyframe gate"], min(hi["keyframe gate"], k_min))
# D: as far right as the canvas allows, and inside Gaussian-map
d_max = min(hi["Gaussian map"], WIDTH_CM - MARGIN - cp_w["Gaussian map"] / 2)
d_min = cpc["keyframe gate"] + cp_w["keyframe gate"] / 2 + CP_GAP + cp_w["Gaussian map"] / 2
cpc["Gaussian map"] = min(d_max, max(lo["Gaussian map"], d_min))

# --------------------------------------------------------- vertical layout ---
H_L = box_h(LAB_L, FS_L)
H_C = max(box_h(v, FS_COMP) for v in COMPONENTS.values())
H_B = box_h("window BA", FS_BB)
H_M = box_h(LAB_M, FS_MASK)

Y_L = 0.06
Y_C = Y_L + H_L + 0.48                      # site-1 stub
Y_B = Y_C + H_C + 0.50                      # component arrows
BUS_Y = Y_B + H_B + 0.44                    # mask bus, clear of the backbone
Y_M = BUS_Y + 0.42                          # mask box sits above its own bus
H = Y_M + H_M + 0.26                        # headroom for the backbone caption

fig = plt.figure(figsize=(TEXTWIDTH, H / 2.54))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH_CM)
ax.set_ylim(0, H)
ax.axis("off")

boxes = []      # (text_artist, patch, pad_pt) for the audit


def box(x, y, w, h, label, face, edge, fs, lw=0.9, ls="-", z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.07",
                       facecolor=face, edgecolor=edge, lw=lw, linestyle=ls,
                       zorder=z)
    ax.add_patch(p)
    t = ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color=INK, zorder=z + 1, linespacing=LS)
    boxes.append((t, p, 1.2))
    return p


def arrow(x1, y1, x2, y2, color, lw=1.0, ms=7.0, ls="-", z=3):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=ms, lw=lw, color=color,
                                 zorder=z, shrinkA=0, shrinkB=1.2,
                                 linestyle=ls))


def poly(pts, color, lw=1.0, ms=7.0, head=True, ls="-", z=3):
    ax.add_patch(FancyArrowPatch(
        path=_MPath(pts, [_MPath.MOVETO] + [_MPath.LINETO] * (len(pts) - 1)),
        arrowstyle="-|>" if head else "-", mutation_scale=ms, lw=lw,
        color=color, zorder=z, shrinkA=0, shrinkB=1.2, linestyle=ls))
    for a, b in zip(pts, pts[1:]):
        min_seg(a, b, f"{color} edge")


# ================================ backbone ==================================
for k in BACKBONE:
    box(cx[k] - bb_w[k] / 2, Y_B, bb_w[k], H_B, k, GREY_BG, GREY_ED, FS_BB)
for prev, nxt in zip(BACKBONE, BACKBONE[1:]):
    arrow(cx[prev] + bb_w[prev] / 2, Y_B + H_B / 2,
          cx[nxt] - bb_w[nxt] / 2, Y_B + H_B / 2, "#8A8A8A")

# =============================== components =================================
for k, label in COMPONENTS.items():
    box(cpc[k] - cp_w[k] / 2, Y_C, cp_w[k], H_C, label, BLUE_BG, BLUE_ED, FS_COMP)
    arrow(cpc[k], Y_C + H_C, cpc[k], Y_B, BLUE_ED, lw=1.15, ms=7.5)

# ==================== reliability signal L: two out-edges ===================
l_w = text_w(LAB_L, FS_L) + 2 * PAD_X
box(MARGIN, Y_L, l_w, H_L, LAB_L, ORG_BG, ORG, FS_L)

# site 1: straight up into R, on R's own centre line
c_r, c_d = cpc["pose solve"], cpc["Gaussian map"]
arrow(c_r, Y_L + H_L, c_r, Y_C, ORG, lw=1.35, ms=7.5)
ax.text(c_r + 0.13, (Y_L + H_L + Y_C) / 2, "site 1", fontsize=FS_SITE,
        color="#8A4E17", ha="left", va="center", fontweight="bold")

# site 2: out of L's right side, along the bottom lane, up into D from below.
# This is the only line in the bottom lane, so it can run the full width.
l_r = MARGIN + l_w
l_cy = Y_L + H_L / 2
poly([(l_r, l_cy), (c_d, l_cy), (c_d, Y_C)], ORG, lw=1.35, ms=7.5)
ax.text(c_d - 0.14, l_cy + 0.16, "site 2", fontsize=FS_SITE,
        color="#8A4E17", ha="right", va="center", fontweight="bold")

# ======================= optional semantic mask =============================
m_w = text_w(LAB_M, FS_MASK) + 2 * PAD_X
m_x = WIDTH_CM - MARGIN - m_w
box(m_x, Y_M, m_w, H_M, LAB_M, "white", MASK, FS_MASK, ls="--", lw=0.85)

# the bus drops from the mask box onto its own lane above the backbone, runs
# left over it, and three dashed stubs drop onto the consumers' top edges.
stub_of = {"pose solve": cpc["pose solve"],
           "keyframe gate": cpc["keyframe gate"],
           "window BA": cx["window BA"]}
STUB_DX = 0.30                   # stubs sit right of each blue arrow, so the
                                 # bus can start clear of the backbone caption
stubs = {k: v + STUB_DX for k, v in stub_of.items()}
# the mask box is wider than the lane, so the trunk enters it from its left
# edge rather than from under its middle
TRUNK_X = m_x + 0.26
poly([(TRUNK_X, Y_M), (TRUNK_X, BUS_Y)], MASK, lw=0.9, head=False,
     ls=(0, (3.5, 2.2)))
poly([(min(stubs.values()), BUS_Y), (TRUNK_X, BUS_Y)], MASK, lw=0.9,
     head=False, ls=(0, (3.5, 2.2)))
for k, xs in stubs.items():
    poly([(xs, BUS_Y), (xs, Y_B + H_B)], MASK, lw=0.9, ms=5.5,
         ls=(0, (3.5, 2.2)))

ax.text(MARGIN, H - 0.10, "MonoGS backbone", fontsize=6.9, color="#8A8A8A",
        fontweight="bold", ha="left", va="top")

# ---------------------------------------------------------------- checks ----
shortest = min([Y_C - (Y_L + H_L), Y_B - (Y_C + H_C), BUS_Y - (Y_B + H_B)])
print(f"canvas {WIDTH_CM:.2f} x {H:.2f} cm (v6 was 12.20 x 3.14)")
print(f"  bands: site1 {Y_C-(Y_L+H_L):.2f}  comp->bb {Y_B-(Y_C+H_C):.2f}  "
      f"mask {BUS_Y-(Y_B+H_B):.2f} cm  (min {shortest/PT2CM:.1f} pt)")
print(f"  boxes: L {H_L:.2f} C {H_C:.2f} B {H_B:.2f} M {H_M:.2f} cm")
print(f"  comp gap R->K "
      f"{cpc['keyframe gate']-cp_w['keyframe gate']/2-(cpc['pose solve']+cp_w['pose solve']/2):.2f} cm")
print(f"  R centre {c_r:.2f} in pose-solve {lo['pose solve']:.2f}..{hi['pose solve']:.2f}")
print(f"  K centre {cpc['keyframe gate']:.2f} in {lo['keyframe gate']:.2f}..{hi['keyframe gate']:.2f}")
print(f"  D centre {c_d:.2f} in {lo['Gaussian map']:.2f}..{hi['Gaussian map']:.2f}")
print(f"  mask box {m_x:.2f}..{WIDTH_CM-MARGIN:.2f}")

crop_vertical(fig)
audit(fig, "fig1", scale=1.0, boxes=boxes)
save_exact(fig, "fig1_pipeline_v7")
