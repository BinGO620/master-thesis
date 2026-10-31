#!/bin/bash
# Build the supplementary material.
#
#   ./build.sh          -> build/main.pdf
#   ./build.sh --clean  -> remove build/
set -euo pipefail
cd "$(dirname "$0")"

TECTONIC="${TECTONIC:-/data/conda_envs/tex/bin/tectonic}"

if [ "${1:-}" = "--clean" ]; then
    rm -rf build
    echo "cleaned build/"
    exit 0
fi

mkdir -p build
"$TECTONIC" -X compile --keep-logs --outdir build main.tex

if [ -f build/main.log ] && grep -q "^!" build/main.log; then
    echo "ERROR: LaTeX failed:"
    grep -A3 "^!" build/main.log | head -20
    exit 1
fi
[ -f build/main.pdf ] || { echo "ERROR: no PDF produced"; exit 1; }

echo "OK: build/main.pdf ($(pdfinfo build/main.pdf | awk '/^Pages/{print $2}') pages)"
