"""Fig. 2 (v5) - the reliability signal's computation, left to right.

Rebuilt after the "lines crowded, not aligned" note on the printed v4:

- the geometric cue g gets its own input box above s, and joins it with one
  short vertical drop. v4 drew g as a dashed line running the width of the
  figure underneath two other boxes to reach s; that was its longest line and
  the source of the collinearity;
- every edge is horizontal or vertical. v4 had three diagonal edges into the
  compute row and two of them crossed;
- one grid: boxes on each row share a baseline and are sized from their own
  labels (measured with TextPath), so no label touches its border;
- the two consumption sites sit side by side under the box that feeds them,
  each on its own short drop, instead of one long polyline across the bottom.

The computation is unchanged (Sec. 3.4): observed minus rigid flow gives the
disagreement a, a per-frame robust MAD normaliser turns it into e_flow, the
depth-residual cue g fuses with it into s = (1 - e_flow)(1 - vg), and s becomes
a floored Cauchy weight consumed at the tracking residual (site 1) and at
lifecycle confirmation (site 2).
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


ORG, ORG_BG = "#B26B2C", "#F5E3CE"
GREY_BG, GREY_ED = "#EFEFEF", "#B9B9B9"
PAD = 0.20

H = 3.10
IN_Y, IN_H, FS = 2.14, 0.64, 8.6
CP_Y, CP_H = 0.98, 0.86
SITE_Y, SITE_H = 0.14, 0.48
BUS_IN = IN_Y + IN_H + 0.15
BUS_S = 0.80

fig = plt.figure(figsize=(TEXTWIDTH, H / 2.54))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, WIDTH_CM)
ax.set_ylim(0, H)
ax.axis("off")


def box(x, y, w, h, label, face, edge, fs=FS, lw=0.9, ls="-", z=2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
        facecolor=face, edgecolor=edge, lw=lw, linestyle=ls, zorder=z))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, color=C["ink"], zorder=z + 1, linespacing=1.26)


def path(pts, color, lw=1.0, ls=None, ms=7, head=True, z=3):
    ax.add_patch(FancyArrowPatch(
        path=_MPath(pts, [_MPath.MOVETO] + [_MPath.LINETO] * (len(pts) - 1)),
        arrowstyle="-|>" if head else "-", mutation_scale=ms, lw=lw,
        color=color, zorder=z, shrinkA=0, shrinkB=0.6, linestyle=ls))


# ------------------------------------------------------ row 1: the inputs ----
LAB_FRAME = "frame $t$\ndepth, pose"
LAB_OBS = "observed flow\n$f_{\\mathrm{obs}}$, RAFT"
LAB_RIG = "rigid flow\n$f_{\\mathrm{static}}$, reproj."
LAB_G = "geometric cue $g$\ndepth residual"
w_frame, w_obs, w_rig = (text_w(l, FS) + PAD for l in (LAB_FRAME, LAB_OBS, LAB_RIG))
w_g = text_w(LAB_G, FS) + PAD

x_frame = 0.20
x_obs = x_frame + w_frame + 0.22
x_rig = x_obs + w_obs + 0.22
mid_flows = (x_obs + (x_rig + w_rig)) / 2          # centre between the two flows

# ----------------------------------------------------- row 2: the compute ----
LAB_DIS = "disagreement $a$\nrobust MAD norm."
LAB_EFL = "cue $e_{\\mathrm{flow}}$\n$1-e^{-\\tilde a/\\sigma}$"
LAB_S = ("static confidence $s$\n$s=(1-e_{\\mathrm{flow}})(1-vg)$\n"
         "Cauchy w., floor 0.10")
w_dis, w_efl, w_s = (text_w(l, FS) + PAD for l in (LAB_DIS, LAB_EFL, LAB_S))

x_dis = mid_flows - w_dis / 2
x_efl = x_dis + w_dis + 0.22
x_s = WIDTH_CM - 0.20 - w_s
print(f"DIAG w_dis={w_dis:.2f} w_efl={w_efl:.2f} w_s={w_s:.2f} x_dis={x_dis:.2f} x_efl={x_efl:.2f} x_s={x_s:.2f} slack={x_s-(x_efl+w_efl):.2f}")
if x_s - (x_efl + w_efl) < 0.10:
    raise SystemExit("compute row too tight")

# g sits over s, so its drop is one short vertical
x_g = x_s + w_s / 2 - w_g / 2
if x_g < x_rig + w_rig + 0.22:
    raise SystemExit("g box collides with the rigid-flow box")

for x, w, lab in ((x_frame, w_frame, LAB_FRAME), (x_obs, w_obs, LAB_OBS),
                  (x_rig, w_rig, LAB_RIG), (x_g, w_g, LAB_G)):
    box(x, IN_Y, w, IN_H, lab, GREY_BG, GREY_ED)
for x, w, lab in ((x_dis, w_dis, LAB_DIS), (x_efl, w_efl, LAB_EFL),
                  (x_s, w_s, LAB_S)):
    box(x, CP_Y, w, CP_H, lab, ORG_BG, ORG)

# ------------------------------------------------------------- edges: flows --
c_frame, c_obs, c_rig, c_g = (x + w / 2 for x, w in
                              ((x_frame, w_frame), (x_obs, w_obs),
                               (x_rig, w_rig), (x_g, w_g)))

# frame t -> observed (horizontal) and -> rigid (over the top, T-junction into
# observed on the way past, so one trunk feeds both without a second crossing)
path([(x_frame + w_frame, IN_Y + IN_H / 2), (x_obs, IN_Y + IN_H / 2)], "#8A8A8A")
path([(c_frame, IN_Y + IN_H), (c_frame, BUS_IN), (c_rig, BUS_IN),
      (c_rig, IN_Y + IN_H)], "#8A8A8A", lw=0.9, ms=6)

# the two flows -> disagreement, on two different horizontal levels so the
# routes never meet
LOW_A, LOW_B = CP_Y + CP_H + 0.28, CP_Y + CP_H + 0.14
path([(c_obs, IN_Y), (c_obs, LOW_A), (x_dis + w_dis * 0.32, LOW_A),
      (x_dis + w_dis * 0.32, CP_Y + CP_H)], ORG)
path([(c_rig, IN_Y), (c_rig, LOW_B), (x_dis + w_dis * 0.68, LOW_B),
      (x_dis + w_dis * 0.68, CP_Y + CP_H)], ORG)
path([(x_dis + w_dis, CP_Y + CP_H / 2), (x_efl, CP_Y + CP_H / 2)], ORG, lw=1.1)
path([(x_efl + w_efl, CP_Y + CP_H / 2), (x_s, CP_Y + CP_H / 2)], ORG, lw=1.1)

# g -> s, straight down
path([(c_g, IN_Y), (c_g, CP_Y + CP_H)], ORG, lw=0.9, ls=(0, (3.5, 2.2)), ms=6)

# ------------------------------------------------------------- edges: sites --
LAB_1, LAB_2 = "site 1: tracking residual", "site 2: lifecycle confirmation"
w_1, w_2 = (text_w(l, 7.4) + 0.34 for l in (LAB_1, LAB_2))
pad = 0.30
tot = w_1 + pad + w_2
# the pair is right-aligned to the same margin as the top row, so the bottom
# row ends where every other row ends; the bus from s reaches it from above
x_2 = WIDTH_CM - 0.20 - w_2
x_1 = x_2 - pad - w_1
if x_1 < 0.20:
    raise SystemExit(f"site row overflows: starts at {x_1:.2f}")
box(x_1, SITE_Y, w_1, SITE_H, LAB_1, "white", ORG, fs=7.4, ls=(0, (3, 2)))
box(x_2, SITE_Y, w_2, SITE_H, LAB_2, "white", ORG, fs=7.4, ls=(0, (3, 2)))
c_1, c_2 = x_1 + w_1 / 2, x_2 + w_2 / 2
c_s = x_s + w_s / 2
path([(c_s, CP_Y), (c_s, BUS_S), (c_1, BUS_S)], ORG, head=False)
path([(c_s, BUS_S), (c_2, BUS_S)], ORG, head=False)
path([(c_1, BUS_S), (c_1, SITE_Y + SITE_H)], ORG)
path([(c_2, BUS_S), (c_2, SITE_Y + SITE_H)], ORG)

# --------------------------------------------------------------- checks -----
print(f"canvas {WIDTH_CM:.2f} x {H:.2f} cm")
print(f"  row1  frame {x_frame:.2f}  obs {x_obs:.2f}..{x_obs+w_obs:.2f}"
      f"  rig {x_rig:.2f}..{x_rig+w_rig:.2f}  g {x_g:.2f}..{x_g+w_g:.2f}")
print(f"  row2  dis {x_dis:.2f}..{x_dis+w_dis:.2f}"
      f"  efl {x_efl:.2f}..{x_efl+w_efl:.2f}  s {x_s:.2f}..{x_s+w_s:.2f}")
print(f"  sites {x_1:.2f}..{x_2+w_2:.2f}  (s centre {x_s+w_s/2:.2f})")
print(f"  lanes LOW_A {LOW_A:.2f} LOW_B {LOW_B:.2f} (dis top {CP_Y+CP_H:.2f},"
      f" flow bottom {IN_Y:.2f})")
save(fig, "fig2_reliability_v5")
