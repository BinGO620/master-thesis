"""Shared v3 publication style for the MRCS manuscript figures.

Differences from v2 (_figstyle.py), per VISUAL_AUDIT.md + FIGURE_PLAN_v3.md:
- no red/green pairs anywhere: directional cues use blue (good) / orange (bad);
- the diverging map is a continuous RdBu ramp with the neutral middle at grey;
- one writable PALETTE dict of roles, reused by every panel;
- default font 7 pt at LNCS text width (12.2 cm), everything vector PDF+SVG.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt

CM = 1 / 2.54
TEXTWIDTH = 12.2 * CM

# ---------------------------------------------------------------- palette ----
# Role -> colour. Fixed across every panel of the paper.
C = {
    # backbone / unmodified baseline: quiet neutral grey
    "vanilla":    "#8C8C8C",
    "vanilla_lt": "#D9D9D9",
    # our two configurations: one hue, two values
    "maskfree":   "#5B92C8",   # lighter blue
    "combined":   "#1F5C99",   # deep blue
    # the controlled counterpart consuming the same flow (warm = "not ours")
    "naive":      "#D9822B",
    # prior-work reference
    "prior":      "#8E6BA6",
    # directional semantics (colour-blind safe pair, NO red/green opposition)
    "good":       "#1F5C99",   # blue  = better / positive
    "bad":        "#C46A3B",   # orange = worse / negative
    # structural greys
    "ink":        "#262626",
    "rule":       "#BFBFBF",
    "panel_bg":   "#F7F7F7",
    # scatter groups for the boundary figure (blue/orange safe pair)
    "redundant":  "#5B92C8",
    "necessary":  "#D9822B",
}

# diverging ramp for the regime matrix: RdBu, zero pinned to near-white grey
DIV_RAMP = ["#B2182B", "#D6604D", "#F4A582", "#EDEAE8", "#92C5DE", "#4393C3", "#2166AC"]


def apply_style(font_size=7):
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"]
    plt.rcParams["svg.fonttype"] = "none"
    mpl.rcParams.update({
        "pdf.fonttype": 42,
        "font.size": font_size,
        "axes.labelsize": font_size,
        "axes.titlesize": font_size,
        "xtick.labelsize": font_size - 0.5,
        "ytick.labelsize": font_size - 0.5,
        "legend.fontsize": font_size - 0.5,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": 0.6,
        "axes.edgecolor": C["ink"],
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.2,
        "ytick.major.size": 2.2,
        "legend.frameon": False,
        "grid.color": C["rule"],
        "grid.linewidth": 0.4,
        "lines.linewidth": 1.0,
        "patch.linewidth": 0.5,
    })


def panel_label(ax, label, x=-0.055, y=1.04, size=8):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=size,
            fontweight="bold", color=C["ink"], ha="left", va="bottom")


def save(fig, stem, dpi=600):
    fig.savefig(f"{stem}.pdf", bbox_inches="tight", pad_inches=0.01)
    fig.savefig(f"{stem}.svg", bbox_inches="tight", pad_inches=0.01)
    fig.savefig(f"{stem}.png", dpi=dpi, bbox_inches="tight", pad_inches=0.01)
    print(f"wrote {stem}.{{pdf,svg,png}}")
