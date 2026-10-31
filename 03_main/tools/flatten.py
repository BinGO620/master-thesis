#!/usr/bin/env python3
"""把 main.tex 的 \\input 递归展开成单文件，供 pandoc 转 docx。

pandoc 不展开 \\input，直接转 main.tex 会得到空文档。这个脚本做三件事：
  1. 递归展开 \\input{...}
  2. 整段删掉导言区命令（\\documentclass、\\usepackage、\\hypersetup{...}、
     \\ctexset{...} 这类可能跨多行的带括号命令）
  3. 删掉 docx 里没有对应物的结构命令（\\label、\\addcontentsline、\\maketitle 等）

只删「对 docx 无意义」的东西，不碰正文内容和章节命令。

用法：
    python3 flatten.py main.tex build/flat.tex
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 带参数、需要整段删除的命令 → 要吞掉多少个参数
# （有的命令有几个必选参数，比如 \addcontentsline{toc}{chapter}{标题} 是三个，
#   只删一个会留下 {chapter}{标题} 这种残骸）
DROP_WITH_ARG = {
    "documentclass": 1, "usepackage": 1, "RequirePackage": 1,
    "hypersetup": 1, "ctexset": 1, "captionsetup": 1,
    "DeclareCaptionFont": 2,          # \DeclareCaptionFont{名字}{定义}
    "graphicspath": 1, "bibliographystyle": 1, "bibliography": 1,
    "thesistitle": 1, "setlength": 2, "addcontentsline": 3,
    "renewcommand": 2, "newcommand": 2, "linespread": 1,
    "markboth": 2, "addbibresource": 1, "vspace": 1, "hspace": 1,
    "rule": 2,
}

# 直接删掉整行的命令。
# 注意结尾不能用 \b：{document} 以 "}" 收尾，后面紧跟行尾时不构成单词边界，
# 会导致 \begin{document} 漏删（实测踩过）。
DROP_LINE = re.compile(
    r"^\s*\\(begin\{document\}|end\{document\}|maketitle|tableofcontents|"
    r"frontmatterpagenumbering|mainmatterpagenumbering|phantomsection|"
    r"thispagestyle|pagestyle|clearpage|newpage|frenchspacing|raggedright|"
    r"label|tight)(?![a-zA-Z])"
)

INPUT = re.compile(r"^\s*\\input\{([^}]+)\}")


def strip_command(text: str, cmd: str, nargs: int = 1) -> str:
    """删掉 \\cmd 及其 nargs 个配平的 {...} 参数，支持跨行和可选 [...] 参数。"""
    out = []
    i = 0
    pat = re.compile(r"\\" + re.escape(cmd) + r"\*?\s*")

    def skip_group(s, j, open_ch, close_ch):
        """从 s[j] 起跳过一组配平的括号，返回结束位置。"""
        depth = 0
        while j < len(s):
            if s[j] == open_ch:
                depth += 1
            elif s[j] == close_ch:
                depth -= 1
                if depth == 0:
                    return j + 1
            j += 1
        return j

    while True:
        m = pat.search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:m.start()])
        j = m.end()
        # 可选参数 [..]（\documentclass[UTF8]{...} 这种）
        while j < len(text) and text[j] == "[":
            j = skip_group(text, j, "[", "]")
            while j < len(text) and text[j] in " \t":
                j += 1
        # 必选参数
        k = 0
        while k < nargs and j < len(text) and text[j] == "{":
            j = skip_group(text, j, "{", "}")
            k += 1
            while j < len(text) and text[j] in " \t":
                j += 1
        # 吞掉行尾空白与换行
        if j < len(text) and text[j] == "\n":
            j += 1
        i = j
    return "".join(out)


def expand(path: Path, seen=None):
    if seen is None:
        seen = set()
    if path in seen:
        raise RuntimeError(f"循环 input：{path}")
    seen.add(path)

    if not path.exists():
        alt = path.with_suffix(".tex")
        if alt.exists():
            path = alt
        else:
            print(f"⚠ 找不到 {path}，跳过", file=sys.stderr)
            return ""

    text = path.read_text(encoding="utf-8")
    parts = []
    for line in text.splitlines():
        m = INPUT.match(line)
        if m:
            target = ROOT / m.group(1)
            if not target.suffix:
                target = target.with_suffix(".tex")
            parts.append(expand(target, seen))
            continue
        if DROP_LINE.match(line):
            continue
        parts.append(line + "\n")
    return "".join(parts)


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "main.tex")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else "build/flat.tex")
    if not src.is_absolute():
        src = ROOT / src
    if not dst.is_absolute():
        dst = ROOT / dst
    dst.parent.mkdir(parents=True, exist_ok=True)

    text = expand(src)
    for cmd, nargs in DROP_WITH_ARG.items():
        text = strip_command(text, cmd, nargs)

    # 带尺寸的换行 \\[0.3cm] pandoc 会当语法错，改成普通换行；
    # 不带参数的 \\ 保留（tabular 里它是行分隔符，pandoc 认）
    text = re.sub(r"\\\\\[[^\]]*\]", r"\\\\", text)
    text = re.sub(r"(?m)^\s*%\s*-+.*\n", "", text)   # 分隔线注释

    text = re.sub(r"(?m)^\s*%[^\n]*\n", "", text)  # 注释行（pandoc 会当空行）
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    dst.write_text(text, encoding="utf-8")
    print(f"展开完成：{dst}（{len(text.splitlines())} 行）")


if __name__ == "__main__":
    main()
