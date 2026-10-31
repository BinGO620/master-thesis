#!/bin/bash
# Compile v2 LaTeX document with bibliography support
cd /data/monogs-ours/papers/maskfree_bundle/latex

# Remove old auxiliary files
rm -f main_v2.aux main_v2.bbl main_v2.blg main_v2.log main_v2.xdv

# Run tectonic with BibTeX support
conda run -n tex tectonic --keep-logs main_v2.tex

# Check for output PDF
if [ -f main_v2.pdf ]; then
    echo "✅ PDF generated successfully"
    ls -lh main_v2.pdf
else
    echo "❌ PDF generation failed"
    exit 1
fi
