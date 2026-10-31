#!/bin/bash
# Build the main paper (MMM 2027, Springer LNCS).
#
#   ./build.sh          -> build/main.pdf
#   ./build.sh --clean  -> remove build/
#
# Output goes to build/ so the source tree stays clean for source submission.
#
# Engine: tectonic (auto-downloads missing packages, first run needs network).
# The Springer class (llncs.cls) and style (splncs04.bst) are bundled locally.
set -euo pipefail
cd "$(dirname "$0")"

TECTONIC="${TECTONIC:-tectonic}"

if [ "${1:-}" = "--clean" ]; then
    rm -rf build
    echo "cleaned build/"
    exit 0
fi

mkdir -p build
"$TECTONIC" -X compile --keep-logs --keep-intermediates --outdir build main.tex

# Fail loudly: never let a stale PDF from a previous run pass as fresh.
if [ -f build/main.log ] && grep -q "^!" build/main.log; then
    echo "ERROR: LaTeX failed:"
    grep -A3 "^!" build/main.log | head -20
    exit 1
fi
[ -f build/main.pdf ] || { echo "ERROR: no PDF produced"; exit 1; }

# Page guard: MMM allows 12 body pages + at most 2 reference pages = 14.
PAGES=$(pdfinfo build/main.pdf 2>/dev/null | awk '/^Pages/{print $2}')
if [ "$PAGES" != "14" ]; then
    echo "WARNING: $PAGES pages; the limit is 14 (12 body + 2 references)"
fi

echo "OK: build/main.pdf ($PAGES pages)"
