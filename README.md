# AI Paper Writing Skills

Eight agent skills for writing and revising machine-learning papers in LaTeX. Each skill owns one part of the paper and works as a long-horizon guide: it reads the project first, keeps ledgers of what it must preserve, splits large passes across subagents, inspects rendered pages, and stops to ask only at decisions that belong to the author.

The skills follow the Agent Skills format, so both Claude Code and Codex can load them. Discussion and reports are in Chinese, and manuscript text is in English.

## Skills

| Skill | Owns | Example request |
| --- | --- | --- |
| `paper-framing` | central claim, argument chain, contribution framing, section outline | 理一下这篇论文的主线 |
| `paper-opening` | abstract, introduction, related work, citation verification | 重写摘要和引言 |
| `paper-method` | method section, notation, equations, theory statements | 方法部分符号统一，去掉数字 |
| `paper-experiments` | setup, results, ablations, statistics, benchmark construction | 实验分析不要复述表格数字 |
| `paper-visuals` | figures through a staged drawing workflow, tables, captions | 方法图不改逻辑，优化呈现 |
| `paper-language` | minimal-edit polish, wording, Chinese-to-English translation | 最小改动润色这一节 |
| `paper-typesetting` | layout, page budget, statements, bibliography, Overleaf or Git sync | 压到 9 页，图不要在标题下面 |
| `paper-checklist` | read-only audit and pre-submission check, routed to the owners above | 投稿前全文检查 |

`paper-checklist` never edits the manuscript. It returns one numbered table per tier (阻碍提交, 影响理解, 局部表达), and each row names the skill that owns the fix. Replying "修 1、3、5" applies those rows through their owning skills and reruns the affected checks.

## Scope

The skills are general. A venue template and its call for papers govern what they specify: the page limit, margins, fonts, required sections and statements. The skills cover what the template leaves open, and where the two disagree the template wins. Each `SKILL.md` opens with this rule, and a conflict between a skill and the template is reported rather than applied silently.

Subject to the venue rules above, shared defaults set one base size for tables and displayed equations in the preamble. A table's source carries its cells, booktabs rules and caption; one `\resizebox` is allowed only for overflow. Each citation group in the body contains at most four works, counting adjacent citation commands together even across source lines. Bibliography cleanup removes fabricated or unsuitable comments from fields and standalone comments while preserving accurate metadata, necessary source/license notices and citation keys.

## Conventions and Exemplars

Each skill detects the manuscript's own conventions before editing, such as caption style, the display-equation environment and the run-in heading macro, and keeps them. The order of precedence is:

1. the venue's rules
2. the user's explicit instruction
3. the conventions the manuscript already uses
4. the forms suggested in the skill

To borrow structure or layout from another paper, name it in the request with an arXiv id, a PDF or a TeX source. The skill caches it under `~/.cache/paper-exemplars/<id>/` and reads it as data.

## Install

Clone the repository, then link each skill into the skill directories of the agents you use.

```bash
git clone https://github.com/Alchemist-Jo/ai-paper-writing.git ~/paper-skills

# Claude Code
mkdir -p ~/.claude/skills
for d in ~/paper-skills/paper-*; do ln -sfn "$d" ~/.claude/skills/"$(basename "$d")"; done

# Codex
mkdir -p ~/.agents/skills
for d in ~/paper-skills/paper-*; do ln -sfn "$d" ~/.agents/skills/"$(basename "$d")"; done
```

Every skill is model-invocable. The agent selects it from the request, and it can also be called by name, as `/paper-checklist` in Claude Code or `$paper-checklist` in Codex. Pulling the repository updates the installed skills through the links.

## Requirements

- A LaTeX project with a build entry, such as `latexmk`, a Makefile or a build script.
- `pdftoppm`, `pdfinfo` and `pdffonts` from Poppler, for rendered-page inspection and PDF checks.
- Python 3 for `paper-checklist/scripts/scan.py` and `paper-visuals/scripts/figure_audit.py`, which use the standard library only.
- The draw.io desktop application, for exporting diagrams from the command line.

## Layout

```
paper-<name>/
  SKILL.md            instructions loaded when the skill triggers
  agents/openai.yaml  Codex display name, prompt and invocation policy
  references/         detail read on demand, such as worked examples
  scripts/            deterministic checks (paper-checklist, paper-visuals)
```

## License

CC BY-NC-SA 4.0, declared in each skill's frontmatter. See [LICENSE](LICENSE).
