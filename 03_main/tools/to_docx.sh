#!/bin/bash
# 把大论文导成 docx，用于交学校（学校要求 .doc/.docx）。
#
# 思路：LaTeX 负责内容与版本管理，docx 只做交付排版。
# 步骤：flatten.py 展开 \input → pandoc 转 docx → 人工套学校模板。
#
# 用法：
#   ./tools/to_docx.sh
# 产物：
#   build/thesis.docx
#
# ⚠ 已知损失：公式、交叉引用编号、复杂表格在转换里会有偏差。
#    导出的 docx 必须人工过一遍，不要当成定稿直接交。
set -euo pipefail
cd "$(dirname "$0")/.."

PANDOC="${PANDOC:-/data/conda_envs/tex/bin/pandoc}"
OUT="build/thesis.docx"
FLAT="build/flat.tex"

mkdir -p build

# 先确保源文件能编译通过，避免拿一份本身就坏的稿子去转
if [ ! -f build/main.pdf ]; then
    echo "编译一次以验证源文件……"
    ./build.sh >/dev/null || { echo "❌ LaTeX 编译失败，先修源文件" >&2; exit 1; }
fi

# pandoc 不展开 \input，必须先拍平
python3 tools/flatten.py main.tex "$FLAT"

# 注意 reader 必须是 latex，不能加 raw_tex 扩展：
# raw_tex 会把 titlepage 里的排版命令整块当原始 TeX 丢弃，封面会整个消失（实测踩过）。
"$PANDOC" "$FLAT" \
    --from latex \
    --to docx \
    --resource-path=.:figures:refs \
    --output "$OUT"

[ -f "$OUT" ] || { echo "❌ 没有产出 docx" >&2; exit 1; }

# 内容非空检查：转出空文档是这种流程最常见的静默失败
PARAS=$(unzip -p "$OUT" word/document.xml 2>/dev/null | grep -o '<w:t' | wc -l)
if [ "$PARAS" -lt 50 ]; then
    echo "❌ docx 内容过少（$PARAS 个文本节点），转换可能失败" >&2
    exit 1
fi

echo "✅ 导出完成：$OUT（$PARAS 个文本节点）"
echo "⚠ 记得在 Word 里套学校模板、更新目录、核对公式与图表编号。"
ls -lh "$OUT"
