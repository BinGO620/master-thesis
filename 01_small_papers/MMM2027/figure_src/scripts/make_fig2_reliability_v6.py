"""Fig. 2 (v6) - the reliability signal, from flows to weights.

What the printed v5 got wrong, measured on the delivered PDF:

* BOX OVERFLOW. The input boxes are 2-line labels in a 0.64 cm box: at 8.6 pt
  they need 21.7 pt and the box offers 18.1 pt, so text hung outside the border.
  The "static confidence" box was worse: 3 lines needing 32.5 pt in 24.4 pt of
  box.  Every box height is now solved from its own label block.
* FLOOR. v5 drew subscripts at 0.7 x 8.6 = 6.02 pt, right on the venue floor.
  The box text is now 9.0 pt, so subscripts print at 6.3 pt, and save_exact()
  re-checks the emitted Tf sizes rather than trusting the artist setting.
* LANES. The two flow->disagreement elbows ran 0.14 cm (4.0 pt) apart and read
  as one thick line.  Lanes are now 0.32 cm apart and each edge is asserted to
  be at least MIN_EDGE_PT long.
* ROUTING. Every edge is horizontal or vertical; the geometric cue g drops
  straight onto s from above, in its own column, as in v5.

The computation is unchanged (Sec. 3.4): observed minus rigid flow gives a, a
per-frame robust MAD normaliser turns it into e_flow, the depth-residual cue g
fuses with it into s = (1 - e_flow)(1 - vg), and s becomes a floored Cauchy
weight consumed at the tracking residual (site 1) and at lifecycle confirmation
(site 2).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as _MPath

from scripts._pubstyle import (C, TEXTWIDTH, apply_style, save_exact, audit,
                               text_w, block_h, PT2CM, WIDTH_CM, min_seg,
                               crop_vertical)

apply_style(font_size=7)

ORG, ORG_BG = "#B26B2C", "#F5E3CE"
GREY_BG, GREY_ED = "#EFEFEF", "#B9B9B9"
INK = C["ink"]

FS = 9.0            # box text (subscripts print at 6.3 pt)
FS_SITE = 8.2       # the two consumption-site boxes
LS = 1.28
PAD_X, PAD_Y = 0.15, 0.11
MARGIN = 0.20

MIN_EDGE_PT = 12.0

LAB_FRAME = "frame $t$\ndepth, pose"
LAB_OBS = "observed flow\n$f_{\\mathrm{obs}}$, RAFT"
LAB_RIG = "rigid flow\n$f_{\\mathrm{static}}$, reproj."
LAB_G = "geometric cue $g$\ndepth residual"
LAB_DIS = "disagreement $a$\nrobust MAD norm."
LAB_EFL = "cue $e_{\\mathrm{flow}}$\n$1-e^{-\\tilde a/\\sigma}$"
LAB_S = ("static confidence $s$\n$s=(1-e_{\\mathrm{flow}})(1-vg)$\n"
         "Cauchy w., floor 0.10")
LAB_1 = "site 1: tracking residual"
LAB_2 = "site 2: lifecycle confirmation"


def bw(label):
    return text_w(label, FS) + 2 * PAD_X


def bh(label, fs=FS):
    return block_h(label, fs, LS) + 2 * PAD_Y


# --------------------------------------------------- row 1: the four inputs ---
IN = [LAB_FRAME, LAB_OBS, LAB_RIG]
w_in = [bw(t) for t in IN]
GAP = 0.46
x_frame = MARGIN
x_obs = x_frame + w_in[0] + GAP
x_rig = x_obs + w_in[1] + GAP
w_g = bw(LAB_G)

# --------------------------------------------------- row 2: the computation ---
CP = [LAB_DIS, LAB_EFL, LAB_S]
w_cp = [bw(t) for t in CP]

x_dis = x_obs + w_in[1] / 2 - w_cp[0] / 2        # under observed flow
x_efl = x_dis + w_cp[0] + 0.52
x_s = WIDTH_CM - MARGIN - w_cp[2]
x_g = x_s + w_cp[2] / 2 - w_g / 2

if x_g < x_rig + w_in[2] + 0.30:
    raise SystemExit(f"g box collides with rigid flow ({x_g:.2f} < "
                     f"{x_rig + w_in[2] + 0.30:.2f})")
if x_s - (x_efl + w_cp[1]) < 0.40:
    raise SystemExit("compute row too tight")

# --------------------------------------------------------- vertical levels ---
H_IN = max(bh(t) for t in IN)
H_CP = max(bh(t) for t in CP)
H_G = bh(LAB_G)
H_SITE = max(bh(t, FS_SITE) for t in (LAB_1, LAB_2))

Y_SITE = 0.06
BUS_S = Y_SITE + H_SITE + 0.40
Y_CP = BUS_S + 0.42
LANE_A = Y_CP + H_CP + 0.74          # observed flow  -> disagreement
LANE_B = Y_CP + H_CP + 0.46          # rigid flow     -> disagreement
Y_IN = LANE_A + 0.50
BUS_IN = Y_IN + H_IN + 0.30          # frame t -> rigid flow, over the top
H = BUS_IN + 0.10

fig = plt.figure(figsize=(TEXTWIDTH, H / 2.54))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH_CM)
ax.set_ylim(0, H)
ax.axis("off")

boxes = []


def box(x, y, w, h, label, face, edge, fs=FS, lw=0.9, ls="-", z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.07",
                       facecolor=face, edgecolor=edge, lw=lw, linestyle=ls,
                       zorder=z)
    ax.add_patch(p)
    t = ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, color=INK, zorder=z + 1, linespacing=LS)
    boxes.append((t, p, 1.2))
    return p


def path(pts, color, lw=1.05, ms=7.5, head=True, ls="-", z=3):
    ax.add_patch(FancyArrowPatch(
        path=_MPath(pts, [_MPath.MOVETO] + [_MPath.LINETO] * (len(pts) - 1)),
        arrowstyle="-|>" if head else "-", mutation_scale=ms, lw=lw,
        color=color, zorder=z, shrinkA=0, shrinkB=1.2, linestyle=ls))
    for a, b in zip(pts, pts[1:]):
        min_seg(a, b, f"edge {color}")


# ------------------------------------------------------------------ boxes ---
for x, w, lab in ((x_frame, w_in[0], LAB_FRAME), (x_obs, w_in[1], LAB_OBS),
                  (x_rig, w_in[2], LAB_RIG)):
    box(x, Y_IN, w, H_IN, lab, GREY_BG, GREY_ED)
box(x_g, Y_IN, w_g, H_G, LAB_G, GREY_BG, GREY_ED)
for x, w, lab in ((x_dis, w_cp[0], LAB_DIS), (x_efl, w_cp[1], LAB_EFL),
                  (x_s, w_cp[2], LAB_S)):
    box(x, Y_CP, w, H_CP, lab, ORG_BG, ORG)
w_1, w_2 = bw(LAB_1) * FS_SITE / FS + 0.10, bw(LAB_2) * FS_SITE / FS + 0.10
x_2 = WIDTH_CM - MARGIN - w_2
x_1 = x_2 - 0.34 - w_1
box(x_1, Y_SITE, w_1, H_SITE, LAB_1, "white", ORG, fs=FS_SITE, ls=(0, (3, 2)))
box(x_2, Y_SITE, w_2, H_SITE, LAB_2, "white", ORG, fs=FS_SITE, ls=(0, (3, 2)))

c_frame = x_frame + w_in[0] / 2
c_obs = x_obs + w_in[1] / 2
c_rig = x_rig + w_in[2] / 2
c_g = x_g + w_g / 2
c_dis = x_dis + w_cp[0] / 2
c_s = x_s + w_cp[2] / 2
c_1, c_2 = x_1 + w_1 / 2, x_2 + w_2 / 2

# ------------------------------------------------------------------ edges ---
# frame t -> observed flow (straight across)
path([(x_frame + w_in[0], Y_IN + H_IN / 2), (x_obs, Y_IN + H_IN / 2)],
     "#8A8A8A")
# frame t -> rigid flow, over the top, T-junction into observed on the way
path([(c_frame, Y_IN + H_IN), (c_frame, BUS_IN), (c_rig, BUS_IN),
      (c_rig, Y_IN + H_IN)], "#8A8A8A", ms=6.5)

# the two flows -> disagreement, on two clearly separated lanes
path([(c_obs, Y_IN), (c_obs, LANE_A), (x_dis + w_cp[0] * 0.30, LANE_A),
      (x_dis + w_cp[0] * 0.30, Y_CP + H_CP)], ORG)
path([(c_rig, Y_IN), (c_rig, LANE_B), (x_dis + w_cp[0] * 0.70, LANE_B),
      (x_dis + w_cp[0] * 0.70, Y_CP + H_CP)], ORG)

# compute chain, straight across
path([(x_dis + w_cp[0], Y_CP + H_CP / 2), (x_efl, Y_CP + H_CP / 2)], ORG,
     lw=1.15)
path([(x_efl + w_cp[1], Y_CP + H_CP / 2), (x_s, Y_CP + H_CP / 2)], ORG,
     lw=1.15)

# geometric cue g -> s, straight down in its own column
path([(c_g, Y_IN), (c_g, Y_CP + H_CP)], ORG, lw=0.95, ms=6.5,
     ls=(0, (3.5, 2.2)))

# s -> the two consumption sites, one bus below the compute row
path([(c_s, Y_CP), (c_s, BUS_S), (c_1, BUS_S)], ORG, head=False, lw=1.15)
path([(c_s, BUS_S), (c_2, BUS_S)], ORG, head=False, lw=1.15)
path([(c_1, BUS_S), (c_1, Y_SITE + H_SITE)], ORG)
path([(c_2, BUS_S), (c_2, Y_SITE + H_SITE)], ORG)

# ---------------------------------------------------------------- checks ----
print(f"canvas {WIDTH_CM:.2f} x {H:.2f} cm (v5 was 12.20 x 3.10)")
print(f"  rows: in {H_IN:.2f}  compute {H_CP:.2f}  g {H_G:.2f}  site {H_SITE:.2f}")
print(f"  lanes LOW_A {LANE_A:.2f} LOW_B {LANE_B:.2f} "
      f"(sep {(LANE_A-LANE_B)/PT2CM:.1f} pt, compute top {Y_CP+H_CP:.2f})")
print(f"  row1 x: frame {x_frame:.2f} obs {x_obs:.2f}..{x_obs+w_in[1]:.2f} "
      f"rig {x_rig:.2f}..{x_rig+w_in[2]:.2f} g {x_g:.2f}..{x_g+w_g:.2f}")
print(f"  row2 x: dis {x_dis:.2f}..{x_dis+w_cp[0]:.2f} "
      f"efl {x_efl:.2f}..{x_efl+w_cp[1]:.2f} s {x_s:.2f}..{x_s+w_cp[2]:.2f}")
print(f"  sites {x_1:.2f}..{x_2+w_2:.2f}")

crop_vertical(fig)
audit(fig, "fig2", scale=1.0, boxes=boxes)
save_exact(fig, "fig2_reliability_v6")
