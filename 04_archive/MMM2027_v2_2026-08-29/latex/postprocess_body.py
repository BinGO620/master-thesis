#!/usr/bin/env python3
"""Post-process the generated LNCS body without changing body font size.

Table 1 is the only table kept in the main paper. The remaining full efficiency
summary is supplied separately in the supplementary material. No font-size or
page-height hacks are applied here.
"""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "body_v3.tex"
content = open(path).read()
# Keep the main table at its normal top-float position. Remove stale placement
# mutations from older builds if a regenerated body still contains them.
content = content.replace("\\begin{table}[!b]", "\\begin{table}[t]")
content = content.replace("\\begin{table}[!t]", "\\begin{table}[t]")
# Keep the pose-side subsection heading with enough of its opening paragraph.
content = content.replace(
    "\\subsection{The pose-side mechanism, and why the endpoint must be named}",
    "\\needspace{7\\baselineskip}\n\\subsection{The pose-side mechanism, and why the endpoint must be named}",
)
# Remove stale page-height enlargements from older builds.
for n in ("8", "4", "2"):
    content = content.replace(f"\\enlargethispage{{{n}\\baselineskip}}\n", "")
content = content.replace("\\enlargethispage{\\baselineskip}\n", "")
# The compact main-paper layout leaves the final section at the end of page 12.
# No font-size changes are applied.
open(path, "w").write(content)
print(f"postprocessed {path}")
