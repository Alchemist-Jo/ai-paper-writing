# AI Paper Writing Skills

本仓库包含 8 个用于撰写和修改机器学习论文的 agent skill，面向 LaTeX 项目。每个 skill 负责论文的一个部分，按长程任务的方式工作：

1. 先读项目，识别论文已有的约定。
2. 用台账记录必须保留的内容。
3. 大范围任务拆给并行 subagent。
4. 在渲染后的页面上检查结果。
5. 只在属于作者的决定上停下来询问。

skill 采用 Agent Skills 格式，Claude Code 和 Codex 都能加载。讨论和报告用中文，论文正文用英文。

## Skill 列表

| Skill | 负责范围 | 请求示例 |
| --- | --- | --- |
| `paper-framing` | 核心论点、论证链、贡献表述、章节大纲 | 理一下这篇论文的主线 |
| `paper-opening` | 摘要、引言、相关工作、引用核对 | 重写摘要和引言 |
| `paper-method` | 方法部分、符号、公式、理论陈述 | 方法部分符号统一，去掉数字 |
| `paper-experiments` | 实验设置、结果、消融、统计、benchmark 构建 | 实验分析不要复述表格数字 |
| `paper-visuals` | 按分阶段流程画图、表格、图注 | 方法图不改逻辑，优化呈现 |
| `paper-language` | 最小修改润色、用词、中译英 | 最小改动润色这一节 |
| `paper-typesetting` | 版面、页数预算、声明、参考文献、Overleaf 或 Git 同步 | 压到 9 页，图不要在标题下面 |
| `paper-checklist` | 只读检查与投稿前检查，问题交给上面对应的 skill | 投稿前全文检查 |

`paper-checklist` 不修改论文。它按三个级别输出编号表格：阻碍提交、影响理解、局部表达。每一行注明负责修改的 skill。回复“修 1、3、5”后，由对应 skill 修改这些行，再重跑相关检查。

`paper-visuals` 的画图流程分为以下阶段：

1. 读取项目中已有的图。
2. 写一份所有图共用的设计 brief。
3. 新图或重画先确认构思。
4. 用可复现的 draw.io、TikZ 或绘图脚本源文件作图。
5. 导出矢量 PDF。
6. 用 `figure_audit.py` 检查印刷字号、字体嵌入、Type 3 字体、配色漂移和类似代码的标签。
7. 在页面上与上一版并排比较。

只改呈现时，脚本会核对新旧两版的元素和标签完全一致。

## 适用范围

这些 skill 是通用的。会议模板和征稿说明规定了的部分，例如页数、页边距、字号、必需章节和声明，以模板为准；skill 只处理模板没有规定的部分，两者冲突时按模板执行，并把冲突报告给作者，不静默覆盖。每个 `SKILL.md` 开头都写了这条规则。

两条团队约定对所有论文生效，因为模板不规定它们：全文所有表格和所有行间公式使用导言区设定的同一个字号，表格源码只写单元格、booktabs 横线和图注。

## 约定与范文

每个 skill 修改前先识别论文已有的约定，例如图注格式、行间公式环境和段首小标题宏，并保持这些约定。优先级依次为：

1. 会议规则
2. 用户的明确指示
3. 论文已有的约定
4. skill 给出的默认形式

需要参考另一篇论文的结构或排版时，在请求中给出 arXiv 编号、PDF 或 TeX 源文件。skill 把它缓存在 `~/.cache/paper-exemplars/<id>/`，只作为资料读取。

## 安装

克隆仓库后，把每个 skill 链接到所用 agent 的 skill 目录。

```bash
git clone https://github.com/Alchemist-Jo/ai-paper-writing.git ~/paper-skills

# Claude Code
mkdir -p ~/.claude/skills
for d in ~/paper-skills/paper-*; do ln -sfn "$d" ~/.claude/skills/"$(basename "$d")"; done

# Codex
mkdir -p ~/.agents/skills
for d in ~/paper-skills/paper-*; do ln -sfn "$d" ~/.agents/skills/"$(basename "$d")"; done
```

所有 skill 都允许模型按请求自动选用，也可以按名称调用：Claude Code 中写 `/paper-checklist`，Codex 中写 `$paper-checklist`。更新仓库后，已安装的 skill 通过链接同步更新。

## 依赖

- 带构建入口的 LaTeX 项目，例如 `latexmk`、Makefile 或构建脚本。
- Poppler 的 `pdftoppm`、`pdfinfo`、`pdffonts`，用于页面渲染和 PDF 检查。
- Python 3，用于 `paper-checklist/scripts/scan.py` 和 `paper-visuals/scripts/figure_audit.py`，两者只用标准库。
- draw.io 桌面版，用于在命令行导出示意图。

## 许可

CC BY-NC-SA 4.0，各 skill 的 frontmatter 也作了相同声明。见 [LICENSE](LICENSE)。
