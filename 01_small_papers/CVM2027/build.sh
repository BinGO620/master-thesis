#!/bin/bash
# 编译 CVM 2027 小论文（源码原样保留，编译在 build/ 内进行，不污染源码目录）。
#
# 为什么不在源码目录直接编译：模板文件（cvm.sty / cvm_eso.sty / cvm.bst / cvmbib.bib）
# 放在 template_cvm/ 子目录里，tectonic 不认 TEXINPUTS 的相对/递归写法（实测全部失败）。
# 可靠做法是把模板平铺进 build/，再从 build/ 编译。
#
# 用法：./build.sh
set -euo pipefail
cd "$(dirname "$0")"

TECTONIC="${TECTONIC:-/data/conda_envs/tex/bin/tectonic}"

rm -rf build
mkdir -p build/tables build/figs

# 模板平铺到 build/ 根目录（eso-pic.sty 会 \input{cvm_eso.sty}，必须同层）
cp template_cvm/*.sty template_cvm/*.bst template_cvm/cvmbib.bib build/
cp paper2_cvm.tex build/
cp tables/*.tex build/tables/
cp figs/* build/figs/

cd build
"$TECTONIC" -X compile --keep-logs paper2_cvm.tex

# 失败必须大声失败：绝不能让上一版的旧 PDF 冒充新构建
if [ -f paper2_cvm.log ] && grep -q "^!" paper2_cvm.log; then
    echo "❌ LaTeX 报错："
    grep -A3 "^!" paper2_cvm.log | head -20
    exit 1
fi
[ -f paper2_cvm.pdf ] || { echo "❌ 没有产出 PDF"; exit 1; }

echo "✅ 构建完成"
pdfinfo paper2_cvm.pdf 2>/dev/null | grep -E '^Pages' || true
ls -lh paper2_cvm.pdf
