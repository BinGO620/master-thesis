# 硕士毕业论文工作区

## 一、总任务

完成硕士毕业论文。

## 二、本人身份

陈彬，导师苏洁，专业计算机科学与技术，研究方向视觉 SLAM，具体领域基于 3DGS 的动态 SLAM。
小论文两篇：MMM2027（已录用）、CVM2027（在投）。

## 三、限制条件

1. **学术型硕士**：大论文要求三个研究内容。**系统不作为研究内容**。
2. **AI 率**：禁止写作 AI 化。完整规则见 `03_main/WRITING_RULES.md`，那是写作时的
   最高约束，动笔前必读。摘要要点：少冒号、少破折号、少括号解释、句长要有变化、
   不要习惯性分点、不要八股式重复。
3. **重复**：禁止在开头、中间、结尾反复重申同一个论述。详略得当，不为「严谨」做
   公式化重复。

## 四、目录安排

```
biyelunwen
├── 01_small_papers   两篇会议小论文的完整可编译副本
├── 02_resources      可复用资源：学校模板、通用参考文献
├── 03_main           大论文主工作区
├── 04_archive        版本快照归档
└── readme.md         总则（本文件）
```

各子目录下另有 readme 作索引，**新增文件或目录时同步更新对应的索引**。

## 五、当前状态（2026-10-23）

框架已搭好，可以开始写。

- 两篇小论文已完整复制并验证可原样编译（MMM 14 页、CVM 14 页，文本与原投稿件一致）
- 大论文骨架可编译，15 页，全是占位内容
- 文献库已合并（50 条）
- 写作规范与自检脚本已就位

**卡点**：三个研究内容怎么切分还没定。详见 `03_main/OUTLINE.md` 的「待决问题」，
其中 Q1 是第三项研究内容从哪来，这是接下来最该先解决的事。

## 六、常用命令

```bash
./03_main/build.sh                          # 编译大论文 → build/main.pdf
./03_main/tools/to_docx.sh                  # 导出 docx（交学校用）
python3 03_main/tools/check_style.py 03_main/chapters/   # 写作风格自检

./01_small_papers/CVM2027/build.sh          # 编译 CVM 小论文
cd 01_small_papers/MMM2027/paper_rev1_camera_ready && \
  TECTONIC=/data/conda_envs/tex/bin/tectonic ./build.sh   # 编译 MMM 小论文
```

`tectonic` 不在 PATH，MMM 那条必须带 `TECTONIC=` 前缀。

## 七、提交约定

**本目录已纳入 git 跟踪**（2026-10-24 起）。此前整个 `biyelunwen/` 是未跟踪的，
一次误删或 `git clean` 就没了；毕业论文要靠它，所以收进版本控制。

提交粒度沿用仓库 `DISCIPLINE.md` 的「最小单元原则」——一个小节写完、一张图定稿、
一个阶段收口，就是一个 commit，不攒批。具体到本目录：

| 做完什么 | 提交什么 |
|---|---|
| 大论文写完一节 | `03_main/chapters/` + 同步改过的 `OUTLINE.md` / `refs` |
| 小论文改到一个里程碑 | `01_small_papers/<篇名>/` 下改动的源、图、交付物 |
| 版本收口 | 先在 `04_archive/` 冻一份完整快照，再提交活区 |
| 新增参考文献 | `02_resources/` 与其 `readme.md` 登记 |
| 写作规范调整 | `03_main/WRITING_RULES.md`，若构成项目级规则再上移到仓库 `DISCIPLINE.md` |

提交信息写清楚改了什么、为什么。用 `git add <显式路径>`，不用 `git add -A`——
本仓库有大量未跟踪的实验产物，`-A` 会把它们卷进来。

### 什么不进 git

只排 `build.sh` 一条命令就能重建的中间件，规则写在 `biyelunwen/.gitignore`：

- LaTeX 的 `aux` / `log` / `blg` / `out` / `toc` / `synctex.gz`，以及 `build/` 目录
- Python 的 `__pycache__`、`*.pyc`
- `figure_src/` 下 matplotlib 顺带导出的 `png` / `svg` 预览件（论文只用 pdf）

**例外**：`main.bbl` 要入库，期刊要求源码包带它；`figure_src/fig2_renders/`
的原始渲染图也要入库，脚本跑不出来，得重跑实验才能再生。

判据就一句：删了之后，能不能只用本目录的文件加 `build.sh` 复原。能复原的不入库。

### 归档

`04_archive/` 存论文的版本快照，一次里程碑一份完整拷贝，配 `MANIFEST.md` 说明来历与
恢复方式。活区永远只放最新版。索引见 `04_archive/readme.md`。

## 八、环境

- LaTeX 编译器：tectonic 0.17.0，路径 `/data/conda_envs/tex/bin/tectonic`
  （xelatex 系，中文可用，缺宏包会自动下载）
- pandoc 3.8，同上目录，用于导出 docx
- 字体：本机没有 SimSun / SimHei / Times New Roman，样式自动回退到
  Noto Serif/Sans CJK SC 与 Latin Modern。**这些是预览字体，定稿排版必须用真字体
  在 Windows 上再排一次**，否则行宽和页数都会变。
