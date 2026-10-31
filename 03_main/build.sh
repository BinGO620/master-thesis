#!/bin/bash
# 编译大论文。产物在 build/，源码目录保持干净。
#
# 用法：
#   ./build.sh          编译
#   ./build.sh clean    清掉 build/
#
# 中文需要 xelatex 系引擎，这里用 tectonic（会自动下载缺失的宏包与字体）。
# 若要出 docx 交给学校，见 ./tools/to_docx.sh。
set -euo pipefail
cd "$(dirname "$0")"

TECTONIC="${TECTONIC:-/data/conda_envs/tex/bin/tectonic}"

if [ "${1:-}" = "clean" ]; then
    rm -rf build
    echo "已清理 build/"
    exit 0
fi

mkdir -p build
# tectonic 的 --outdir 只放产物，源文件仍在当前目录，相对路径不会乱
"$TECTONIC" -X compile --keep-logs --outdir build main.tex

if [ -f build/main.log ] && grep -q "^!" build/main.log; then
    echo "❌ LaTeX 报错："
    grep -A4 "^!" build/main.log | head -30
    exit 1
fi
[ -f build/main.pdf ] || { echo "❌ 没有产出 PDF"; exit 1; }

# 未定义引用、缺图是常见且致命的，单独查一遍
if grep -qE "Reference .* undefined|File .* not found" build/main.log; then
    echo "⚠ 存在未定义引用或缺文件："
    grep -E "Reference .* undefined|File .* not found" build/main.log | sort -u | head -20
fi

echo "✅ 构建完成"
pdfinfo build/main.pdf 2>/dev/null | awk '/^Pages/{print "  页数：" $2}'
ls -lh build/main.pdf
