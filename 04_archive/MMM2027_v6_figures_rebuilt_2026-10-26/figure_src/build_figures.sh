#!/bin/bash
# Rebuild all six paper figures and install them into ../figures/.
#
# Every script draws at exactly \textwidth (12.2 cm) and saves WITHOUT a tight
# bounding box, so \includegraphics[width=\textwidth] scales by 1.000 and a
# drawn 7 pt label prints at 7 pt.  Each script audits itself and refuses to
# write a figure that has: a printed glyph below 6.6 pt, two overlapping
# labels, a label off the canvas, a label outside its own box, or an edge
# shorter than 12 pt.
#
#   ./build_figures.sh          rebuild + install
#   ./build_figures.sh --check  rebuild only, do not install
set -euo pipefail
cd "$(dirname "$0")"

PY=/data/conda_envs/monogs-ours/bin/python
export PYTHONPATH="$PWD:$PWD/.."

SCRIPTS=(
  make_fig1_pipeline_v7.py:fig1_pipeline_v7.pdf:fig1_pipeline.pdf
  make_fig2_reliability_v6.py:fig2_reliability_v6.pdf:fig2_reliability.pdf
  make_fig3_map_comparison_v6.py:fig3_map_comparison_v6.pdf:fig3_map_comparison.pdf
  make_fig4_component_necessity_v5.py:fig4_component_necessity_v5.pdf:fig4_component_necessity.pdf
  make_fig5_controlled_comparison_v6.py:fig5_controlled_comparison_v6.pdf:fig5_controlled_comparison.pdf
  make_fig6_pose_endpoints_v5.py:fig6_pose_endpoints_v5.pdf:fig6_pose_endpoints.pdf
)

for entry in "${SCRIPTS[@]}"; do
    IFS=: read -r script built target <<< "$entry"
    echo "=== $script"
    "$PY" "scripts/$script"
    if [ ! -f "$built" ]; then
        echo "ERROR: $script did not produce $built"; exit 1
    fi
    if [ "${1:-}" != "--check" ]; then
        cp "$built" "../figures/$target"
        echo "    installed ../figures/$target"
    fi
done

if [ "${1:-}" != "--check" ]; then
    echo
    echo "=== installed figure sizes (must all be 12.20 cm wide)"
    for entry in "${SCRIPTS[@]}"; do
        IFS=: read -r script built target <<< "$entry"
        w=$(pdfinfo "../figures/$target" | awk '/Page size/{print $3}')
        h=$(pdfinfo "../figures/$target" | awk '/Page size/{print $5}')
        printf "  %-34s %8s x %8s pt\n" "$target" "$w" "$h"
    done
fi
