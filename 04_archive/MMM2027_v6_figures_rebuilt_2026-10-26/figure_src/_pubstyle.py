"""Final rint geometry helpers: draw at true print size, then *verify* the geometry.

Why this module exists
----------------------
The v3-v6 figures were drawn at 12.2 cm and saved with ``bbox_inches="tight"``.
Tight cropping changes the page box (e.g. 349.27 pt instead of 345.83 pt), so
``\\includegraphics[width=\\textwidth]`` silently rescales the whole figure, and
every label then prints at a size nobody measured.  Fig. 5 was additionally
included at 0.72\\textwidth and printed its 8.4 pt labels at 6.1 pt.

Two rules here:

1. ``save_exact()`` writes the PDF with **no** bounding-box crop, so the page box
   is exactly ``WIDTH_CM`` wide.  Included at ``width=\\textwidth`` the scale is
   1.000 and a drawn 7 pt label prints at 7 pt.
2. ``audit()`` measures, on the drawn canvas, every text extent (rotation-aware,
   through the renderer) and **raises** on: a glyph below the venue floor, two
   labels overlapping, a label crossing the canvas edge, or a label spilling out
   of the box that owns it.  Geometry that cannot pass cannot be shipped.

The MMM/Springer floor is 6 pt.  We hold ourselves to ``TARGET_PT`` so that any
future rounding still clears it.
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

try:                                                      # run as scripts.x
    from scripts._figstyle_v3 import (C, TEXTWIDTH, apply_style, panel_label)
except ImportError:                                       # run from scripts/
    from _figstyle_v3 import C, TEXTWIDTH, apply_style, panel_label  # noqa: F401

PT2CM = 2.54 / 72
WIDTH_CM = TEXTWIDTH / (1 / 2.54) if False else 12.2   # 12.2 cm = \textwidth
MIN_PT = 6.0        # venue floor: MMM/Springer, figures included
TARGET_PT = 6.6     # our own floor, with margin


# ------------------------------------------------------------------ metrics ---
def text_w_pt(label, fs):
    """Width in points of a label's widest line, at font size ``fs``."""
    fp = FontProperties(family="DejaVu Sans", size=fs)
    return max(TextPath((0, 0), ln, prop=fp, usetex=False).get_extents().width
               for ln in label.split("\n"))


def text_w(label, fs):
    """Width in cm (1 data unit = 1 cm in every figure here)."""
    return text_w_pt(label, fs) * PT2CM


def nlines(label):
    return label.count("\n") + 1


def block_h(label, fs, linespacing=1.26):
    """Height in cm of a multi-line label block."""
    return nlines(label) * fs * linespacing * PT2CM


# ------------------------------------------------------------------- saving ---
def save_exact(fig, stem, dpi=600, scale=1.0, min_pt=None):
    """Write PDF/SVG/PNG with the page box exactly the drawn figure size.

    Refuses to write a PDF whose *emitted* glyph sizes are below the floor:
    matplotlib's mathtext renders sub/superscripts smaller than the Text
    artist's fontsize, so auditing the artist alone is not enough.  The check
    reads the Tf operators out of the produced PDF, i.e. what will print.
    """
    _check(fig, stem)
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.svg")
    fig.savefig(f"{stem}.png", dpi=dpi)
    w, h = (v * 2.54 for v in fig.get_size_inches())
    print(f"wrote {stem}.{{pdf,svg,png}}  ({w:.2f} x {h:.2f} cm)")
    printed = pdf_font_sizes(f"{stem}.pdf")
    lo = min(printed) * scale
    floor = MIN_PT if min_pt is None else min_pt
    print(f"  printed glyph sizes: min {lo:.2f} pt "
          f"(floor {floor} pt){'' if lo >= floor else '  <-- BELOW FLOOR'}")
    if lo < floor - 1e-9:
        raise SystemExit(f"{stem}: smallest printed glyph {lo:.2f} pt "
                         f"< {floor} pt")
    return f"{stem}.pdf"


def pdf_font_sizes(path):
    """Every distinct font size (pt) actually used to paint glyphs."""
    import re, zlib
    data = open(path, "rb").read()
    tf = re.compile(rb"/(\w+)\s+([\d.]+)\s+Tf")
    show = re.compile(rb"T[jJ]\b")
    sizes = set()
    for m in re.finditer(rb"stream\r?\n", data):
        s = m.end()
        e = data.find(b"endstream", s)
        if e < 0:
            continue
        try:
            body = zlib.decompress(data[s:e])
        except zlib.error:
            body = data[s:e]
        cur = None
        for ln in body.split(b"\n"):
            mt = tf.search(ln)
            if mt:
                cur = float(mt.group(2))
            elif show.search(ln) and cur is not None:
                sizes.add(round(cur, 2))
    return sorted(sizes) or [0.0]


def _check(fig, stem):
    """Hook kept for symmetry: geometry is audited by audit() before saving."""
    return


def crop_vertical(fig, pad_cm=0.015):
    """Shrink the canvas vertically to the drawn ink, keeping width untouched.

    Every script draws at exactly \\textwidth and must stay 12.2 cm wide, so a
    general tight-bbox crop is not allowed (it would change the width and the
    inclusion scale).  What *is* free is vertical whitespace: mpl leaves 10-25
    pt of blank above and below the content, and that blank prints as dead
    space between the figure and its caption.  This shifts and rescales every
    axes so the ink sits pad_cm from the top and bottom edges, then sets the
    figure height to match.  Width and scale are unchanged, so a 7 pt label
    still prints at 7 pt.
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    # Ink bbox from the drawn artists, not fig.get_tightbbox(): the schematic
    # figures use one full-canvas axes, whose tightbbox is the whole figure and
    # would hide the empty band above and below the drawing.
    ys = []
    for ax in fig.axes:
        for t in ax.texts:
            if t.get_text().strip():
                b = t.get_window_extent(r)
                ys += [b.y0, b.y1]
        for ln in ax.lines:
            try:
                b = ln.get_window_extent(r)
            except Exception:
                continue
            ys += [b.y0, b.y1]
        # Patches and collections are skipped: on a log axes a bar or a fill
        # reports a window extent that runs to the transformed zero (-1e5 px),
        # which would pin the bbox to the canvas edge and hide the blank band.
        if ax.axison:
            # the axes frame itself is ink
            ab = ax.get_window_extent(r)
            ys += [ab.y0, ab.y1]
            for t in (ax.xaxis.label, ax.yaxis.label, ax.title):
                if t.get_text().strip():
                    b = t.get_window_extent(r)
                    ys += [b.y0, b.y1]
            for t in ax.get_xticklabels() + ax.get_yticklabels():
                if t.get_text().strip():
                    b = t.get_window_extent(r)
                    ys += [b.y0, b.y1]
            leg = ax.get_legend()
            if leg is not None:
                b = leg.get_window_extent(r)
                ys += [b.y0, b.y1]
    for t in fig.texts:
        if t.get_text().strip():
            b = t.get_window_extent(r)
            ys += [b.y0, b.y1]
    if not ys:
        return False
    W, H = fig.get_size_inches()
    dpi = fig.dpi
    lo_px, hi_px = min(ys), max(ys)
    pad_in = pad_cm / 2.54
    y0 = max(lo_px / dpi - pad_in, 0.0)
    y1 = min(hi_px / dpi + pad_in, H)
    if y1 - y0 >= H - 1e-6:
        return False                           # already tight
    new_H = y1 - y0

    # every axes: keep its inches offset relative to the new bottom edge
    rects = []
    for ax in fig.axes:
        p = ax.get_position()
        rects.append((ax, p))
    texts = [(t, t.get_position()) for t in fig.texts]

    fig.set_size_inches(W, new_H, forward=True)
    for ax, p in rects:
        nb = (p.y0 * H - y0) / new_H
        nh = p.height * H / new_H
        ax.set_position([p.x0, nb, p.width, nh])
    for t, (tx, ty) in texts:
        t.set_position((tx, (ty * H - y0) / new_H))
    print(f"  cropped vertically: {H * 2.54:.2f} -> {new_H * 2.54:.2f} cm "
          f"(saved {(H - new_H) * 72:.0f} pt)")
    return True


# -------------------------------------------------------------------- audit ---
def _texts(fig):
    """Every *visible* Text artist with its owner axes (None = figure text)."""
    out = []

    def visible(t):
        if not t.get_visible() or not t.get_text().strip():
            return False
        return True

    for ax in fig.axes:
        for t in ax.texts:
            out.append((t, ax))
        if not ax.axison:          # axis turned off: no ticks/labels are drawn
            continue
        out.append((ax.xaxis.label, ax))
        out.append((ax.yaxis.label, ax))
        for t in ax.get_xticklabels() + ax.get_yticklabels():
            out.append((t, ax))
        for t in (ax.title,):
            out.append((t, ax))
        leg = ax.get_legend()
        if leg is not None:
            for t in leg.get_texts():
                out.append((t, ax))
    for t in fig.texts:
        out.append((t, None))
    return [(t, ax) for t, ax in out if visible(t)]


def audit(fig, name, scale=1.0, min_pt=TARGET_PT, overlap_tol=0.5,
          boxes=None, quiet=False):
    """Verify printed legibility and layout.  Raises on any violation.

    scale : inclusion scale (1.0 when saved with save_exact and included at
            width=\\textwidth).  Printed size = drawn size x scale.
    boxes : optional {text_artist: patch_artist} pairs; each label must stay
            inside its own box with ``pad`` pt of clearance.
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.get_size_inches() * fig.dpi          # canvas in px
    items = []
    for t, ax in _texts(fig):
        bb = t.get_window_extent(r)
        items.append((t, ax, bb))

    errors = []

    # 1 -- printed glyph size
    for t, ax, bb in items:
        printed = t.get_fontsize() * scale
        if printed < min_pt - 1e-9:
            errors.append(f"font {printed:.2f} pt < {min_pt} pt: {t.get_text()!r}")

    # 2 -- nothing may cross the canvas edge (this is what clipped fig. 5)
    for t, ax, bb in items:
        if bb.x0 < -0.2 or bb.y0 < -0.2 or bb.x1 > W + 0.2 or bb.y1 > H + 0.2:
            errors.append(
                f"text outside canvas: {t.get_text()!r} bbox=({bb.x0:.1f},"
                f"{bb.y0:.1f})..({bb.x1:.1f},{bb.y1:.1f}) canvas=({W:.0f}x{H:.0f})")

    # 3 -- no two labels may overlap
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][2], items[j][2]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0)
            oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > overlap_tol and oy > overlap_tol:
                errors.append(
                    f"labels overlap by {ox:.1f}x{oy:.1f} pt: "
                    f"{items[i][0].get_text()!r} <-> {items[j][0].get_text()!r}")

    # 4 -- every boxed label stays inside its own box
    if boxes:
        for t, patch, pad_pt in boxes:
            tb = t.get_window_extent(r)
            pb = patch.get_window_extent(r)
            pad = pad_pt * fig.dpi / 72.0
            if (tb.x0 < pb.x0 + pad - 0.2 or tb.x1 > pb.x1 - pad + 0.2 or
                    tb.y0 < pb.y0 + pad - 0.2 or tb.y1 > pb.y1 - pad + 0.2):
                errors.append(
                    f"label overflows its box: {t.get_text()!r} "
                    f"text({tb.x0:.1f},{tb.y0:.1f})..({tb.x1:.1f},{tb.y1:.1f}) "
                    f"box({pb.x0:.1f},{pb.y0:.1f})..({pb.x1:.1f},{pb.y1:.1f})")

    if not quiet:
        print(f"[audit] {name}: {len(items)} labels, "
              f"min printed {min(t.get_fontsize() * scale for t, _, _ in items):.2f} pt"
              f" -> {'FAIL' if errors else 'PASS'}")
    if errors:
        for e in errors:
            print("   ! " + e)
        raise SystemExit(f"audit failed for {name}: {len(errors)} violation(s)")
    return True


def min_seg(p0, p1, label=""):
    """Assert an edge is long enough to read as an edge, not a nub."""
    import math
    L = math.dist(p0, p1) / PT2CM            # cm -> pt
    if L < 8.0:
        raise SystemExit(f"segment too short ({L:.1f} pt): {label} {p0}->{p1}")
    return L
