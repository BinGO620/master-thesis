#!/usr/bin/env python3
"""check_citations.py — 引用完整性门禁（master_thesis）

检查 04_writing/chapters/*.md 的 [@key] 引用与 01_literature/references.bib
的条目是否一一对应：
  - MISSING：正文引用了 bib 里没有的 key（编译会断链）——必须为 0
  - UNUSED：bib 里有但正文从未引用的条目——提示（可能是待写章节或遗漏）

同时扫描反 AI 化套话（README 15 条原则的可脚本化部分）。

用法: python3 02_analysis/scripts/check_citations.py
退出码：MISSING > 0 时非零（可挂 CI/提交前检查）。
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BIB = os.path.join(ROOT, "01_literature", "references.bib")
CHAP = os.path.join(ROOT, "04_writing", "chapters", "*.md")

# 反 AI 化套话（README 原则 3/4 的可脚本化子集）
BOILERPLATE = [
    "Furthermore", "Moreover", "It is worth noting",
    "plays a crucial role", "has attracted extensive",
    "具有重要意义", "丰富了相关研究", "提供了新的视角", "催生了",
]

# 文档性占位（非真实引用），不参与 MISSING 判定
PLACEHOLDERS = {"key"}


def main():
    keys = set(re.findall(r"@\w+\{([^,]+),", open(BIB).read()))
    cited = {}
    for f in glob.glob(CHAP):
        for m in re.findall(r"\[@([A-Za-z0-9_:\-]+)\]", open(f).read()):
            if m in PLACEHOLDERS:
                continue
            cited.setdefault(m, set()).add(os.path.basename(f))

    missing = sorted(k for k in cited if k not in keys)
    unused = sorted(k for k in keys if k not in cited)

    print(f"bib entries: {len(keys)}  distinct cited: {len(cited)}")
    if missing:
        print(f"MISSING from bib ({len(missing)}):")
        for k in missing:
            print(f"  {k} <- {','.join(sorted(cited[k]))}")
    else:
        print("MISSING: none")

    if unused:
        print(f"UNUSED bib entries ({len(unused)}): {', '.join(unused)}")
    else:
        print("UNUSED: none")

    hits = []
    for f in glob.glob(CHAP):
        for i, line in enumerate(open(f), 1):
            for b in BOILERPLATE:
                if b in line:
                    hits.append((os.path.basename(f), i, b))
    print(f"boilerplate hits: {len(hits)}")
    for f, i, b in hits:
        print(f"  {f}:{i}  {b}")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
