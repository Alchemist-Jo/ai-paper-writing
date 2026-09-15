---
name: ai-paper-writing
description: "Manually selected AI paper writing with three modes: Grill collaborative writing, Draft manuscript writing, and Style reference imitation. Uses ICLR/ICML corpus statistics and CVPR cases for claims, sections, paragraphs, figures and tables. Run only when the user explicitly selects ai-paper-writing; infer the mode from their request. Excludes standalone blogs/reports, summary-only, training execution and submission."
disable-model-invocation: true
---

# AI Paper Writing

Activate only by explicit selection of this skill. Use the conversation's artifact, evidence, venue and constraints. Read [Evidence contract](references/evidence-contract.md), then choose one mode; do not require a separate confirmation when the request is clear.

| Mode | Use | Execution |
| --- | --- | --- |
| **Grill · 协作写作** | Develop the argument together through focused questions and iterative prose | Read [Grill](references/mode-grill.md); ask one decision at a time, recommend an answer, wait for feedback, and write from resolved decisions |
| **Draft · 论文写作** | Draft, restructure, polish or review a manuscript from available evidence | Read [Draft](references/mode-draft.md); complete the requested artifact and necessary consistency edits |
| **Style · 示例仿写** | Match a reference paper's structure, language, paragraphs, figures or tables | Read [Style](references/mode-style.md); inspect the source, map its features to project evidence, and produce the requested prose or visuals |

Modes may support one another within the requested scope. Grill decisions belong to the user; facts should be retrieved. Draft and Style proceed directly when sufficient information is available. Do not silently turn a drafting request into an interview.

## Shared execution

1. Read [Statistics to decisions](references/statistics-to-decisions.md) for structure, prose or visuals; read the mapped full source sections and relevant CSV rows before using numbers. Preserve cohort, denominator and weighting.
2. Use [Task routes](references/task-routes.md) to load only the necessary full sections. Apply [Architecture and language](references/architecture-and-language.md), [Venue adaptation](references/venue-adaptation.md), and [Figures and tables](references/figures-and-tables.md) as needed.
3. Deliver text or edit the manuscript directly. Follow [Execution and delivery](references/execution-and-delivery.md). Protect facts, reported numbers, names and uncertainty. Unobserved results remain explicit draft placeholders.

Scientific evidence and user constraints govern claims. Current official rules govern submission layout; supplied exemplars govern transferable style; matched corpus statistics supply defaults. Historical fixed counts, stage limits and formatting recipes are optional examples. No acceptance prediction or mandatory reference quota.

[Source map](SOURCE.md) indexes the preserved statistics, readings, visual audits and cases in `sources/`. These are evidence, not additional skill invocations. [Validation](reports/validation.md) and `evals/` state what was checked. Return the requested artifact first, followed only by material changes, missing evidence and verification limits.
