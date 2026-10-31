#!/usr/bin/env python3
"""中文论文写作风格自检。

针对的是 AI 写作的几个可量化痕迹：冒号/破折号/括号密度、分点罗列、
句长均一、段首词重复、套话高频词。

用法：
    python3 check_style.py chapters/          # 检查目录下所有 .tex/.md
    python3 check_style.py chapters/ch1.tex   # 检查单个文件

只报可疑处，不做自动修改。规则出处见 WRITING_RULES.md。
"""
import re
import sys
from pathlib import Path

# 阈值：每千字的允许上限（见 WRITING_RULES.md 第一节）
LIMITS = {
    "colon": 3.0,      # ：
    "dash": 2.0,       # ——
    "paren": 4.0,      # （）()
}

# 套话。命中即列出，由作者判断是否保留。
CLICHES = [
    "随着.*?的快速发展", "近年来", "众所周知", "值得注意的是", "需要指出的是",
    "综上所述", "总而言之", "总的来说", "由此可见", "不言而喻", "毋庸置疑",
    "显著提升", "大幅改善", "极大地", "完全解决", "有效证明了", "充分说明",
    "一定程度上", "某种意义上", "某种程度上", "相对来说", "首次提出",
    "填补了空白", "全新的",
]

# 分点标记
BULLET_PATTERNS = [
    r"^\s*[（(]\d+[）)]",           # （1）
    r"^\s*\d+[、.]\s",              # 1、 1.
    r"^\s*[一二三四五六七八九十]+[、是]",  # 一、
    r"\\begin\{itemize\}", r"\\begin\{enumerate\}",
    r"^\s*[-*]\s+",                 # markdown 列表
]

CJK = re.compile(r"[\u4e00-\u9fff]")


def strip_tex(text: str) -> str:
    """去掉 LaTeX 命令、公式、注释，只留要检查的自然语言。"""
    text = re.sub(r"(?<!\\)%.*", "", text)                  # 注释
    text = re.sub(r"\\begin\{(equation|align|array|tabular)\*?\}.*?"
                  r"\\end\{\1\*?\}", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " ", text)                   # 行内公式
    text = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", text)  # 命令
    text = re.sub(r"[{}]", " ", text)
    return text


def split_paragraphs(text: str):
    lines = []
    buf = []
    for line in text.splitlines():
        if line.strip():
            buf.append(line.strip())
        elif buf:
            lines.append(" ".join(buf))
            buf = []
    if buf:
        lines.append(" ".join(buf))
    return [p for p in lines if len(CJK.findall(p)) >= 15]


def split_sentences(par: str):
    parts = re.split(r"(?<=[。！？；])", par)
    return [s for s in parts if len(CJK.findall(s)) >= 3]


def head_word(par: str, n=2) -> str:
    """取段首 n 个汉字，用来查段首重复。"""
    m = re.match(r"[\u4e00-\u9fff]{%d}" % n, par)
    return m.group(0) if m else ""


def analyse(path: Path, text: str):
    raw = text
    if path.suffix == ".tex":
        text = strip_tex(text)

    cjk_count = len(CJK.findall(text))
    if cjk_count < 100:
        return None

    per_k = 1000.0 / cjk_count
    stats = {
        "file": str(path),
        "chars": cjk_count,
        "colon": text.count("：") + text.count(":") * 0,  # 半角冒号多为语法，不计
        "dash": text.count("——"),
        "paren": text.count("（") + text.count("("),
        "bullets": sum(len(re.findall(p, raw, re.M)) for p in BULLET_PATTERNS),
        "cliche_hits": [],
        "short_sent_ratio": 0.0,
        "repeated_heads": [],
    }

    for pat in CLICHES:
        for m in re.finditer(pat, text):
            ctx = text[max(0, m.start() - 10):m.end() + 10].replace("\n", " ")
            stats["cliche_hits"].append((m.group(0), ctx))

    paras = split_paragraphs(text)
    sents = [s for p in paras for s in split_sentences(p)]
    if sents:
        lens = [len(CJK.findall(s)) for s in sents]
        short = sum(1 for L in lens if L <= 15)
        stats["short_sent_ratio"] = short / len(sents)
        stats["sent_len_mean"] = sum(lens) / len(lens)
        stats["sent_len_sd"] = (sum((L - stats["sent_len_mean"]) ** 2 for L in lens) / len(lens)) ** 0.5

    heads = {}
    for p in paras:
        h = head_word(p)
        if h:
            heads[h] = heads.get(h, 0) + 1
    stats["repeated_heads"] = [(h, c) for h, c in heads.items() if c >= 3]

    stats["per_k"] = {k: stats[k] * per_k for k in ("colon", "dash", "paren")}
    return stats


def report(stats):
    f = stats["file"]
    print(f"\n=== {f} ===")
    print(f"  正文汉字 {stats['chars']}，句数均长 {stats.get('sent_len_mean', 0):.1f} 字"
          f"（标准差 {stats.get('sent_len_sd', 0):.1f}）")

    issues = 0
    for key, label in (("colon", "冒号"), ("dash", "破折号"), ("paren", "括号")):
        val = stats["per_k"][key]
        limit = LIMITS[key]
        flag = "⚠" if val > limit else " "
        if val > limit:
            issues += 1
        print(f"  {flag} {label} {stats[key]} 处，密度 {val:.1f}/千字（上限 {limit}）")

    b = stats["bullets"]
    flag = "⚠" if b > 6 else " "
    if b > 6:
        issues += 1
    print(f"  {flag} 分点标记 {b} 处")

    if stats.get("short_sent_ratio", 1) < 0.15:
        issues += 1
        print(f"  ⚠ 短句（≤15字）占比仅 {stats['short_sent_ratio']:.0%}，句长偏均一")

    if stats["repeated_heads"]:
        issues += 1
        print("  ⚠ 段首重复：")
        for h, c in stats["repeated_heads"]:
            print(f"      「{h}」出现 {c} 次")

    if stats["cliche_hits"]:
        issues += 1
        print(f"  ⚠ 套话 {len(stats['cliche_hits'])} 处：")
        for word, ctx in stats["cliche_hits"][:8]:
            print(f"      「{word}」… {ctx}")

    if issues == 0:
        print("  ✅ 未发现量化问题")
    return issues


def main():
    targets = sys.argv[1:] or ["."]
    files = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            files += sorted(list(p.rglob("*.tex")) + list(p.rglob("*.md")))
        elif p.is_file():
            files.append(p)

    files = [f for f in files if "archive" not in f.parts]
    if not files:
        print("没有找到 .tex / .md 文件")
        return 1

    total = 0
    for f in files:
        try:
            st = analyse(f, f.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
        if st:
            total += report(st)

    print(f"\n共 {len(files)} 个文件，{total} 类问题待人工确认。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
