# 大论文主工作区（03_main）

## 索引

| 路径 | 做什么 |
|---|---|
| `WRITING_RULES.md` | **动笔前必读**。降 AI 率的硬规则，最高写作约束 |
| `OUTLINE.md` | 论文大纲与研究内容规划。三个研究内容尚未定稿，见其中「待决问题」 |
| `main.tex` | 主文件，串起所有章节 |
| `ujnthsis.sty` | 版式定义，参数抄自学校硕士模板 |
| `build.sh` | 编译，产物在 `build/` |
| `chapters/` | 正文章节，一章一文件 |
| `frontmatter/` | 封面、声明、摘要、参考文献、致谢、附录 |
| `refs/` | 文献库 `references.bib`（50 条，两篇小论文合并）+ 国标样式 |
| `figures/` | 图 |
| `tools/` | 辅助脚本 |

## 当前状态

骨架可编译，15 页，全是占位内容。三个研究内容没定，章节标题都是临时的。

## 常用命令

```bash
./build.sh                      # 编译，产物 build/main.pdf
./build.sh clean                # 清理

python3 tools/check_style.py chapters/     # 写作风格自检（标点/套话/句长）
```

## 写作流程（建议）

1. 先读 `WRITING_RULES.md` 和 `OUTLINE.md`
2. 一节一节推进，每节写之前先用一句话说清这节要说什么
3. 写完跑一次 `check_style.py`
4. 每章完成后 commit 一次

## 环境

- 编译器：`/data/conda_envs/tex/bin/tectonic`（0.17.0，xelatex 系，中文可用）
- 字体：本机没有 SimSun/SimHei/Times New Roman，样式会自动回退到
  Noto Serif/Sans CJK SC 与 Latin Modern。**版面预览用，定稿排版要用真字体再排一次。**
- 导出 docx：见 `tools/to_docx.sh`（待建）
