---
name: paper-checklist
description: Audits an ML paper read-only, before submission or after a revision, and reports located problems in a tiered Chinese table that names the skill owning each fix. Runs a deterministic source scan, rendered-page inspection, citation verification, a blind fresh-context reader with an LLM-reviewer simulation, and anonymity and leak checks, plus submission requirements such as the page limit, statements, embedded fonts and PDF metadata. Use when the user asks to check, review or audit the paper, run a pre-submission check, find remaining problems, check consistency across sections, check anonymity, or simulate a reviewer. Not for making fixes, which the owning skill applies after the user says to fix. 触发词：检查论文、全文检查、投稿前检查、pre-submission、模拟审稿、审稿视角、一致性检查、匿名检查、查问题、还有什么问题。
license: CC-BY-NC-SA-4.0
---

# Paper Checklist

Use this skill to find what still blocks, confuses or weakens a paper, and to hand each problem to the skill that fixes it. The check never edits the manuscript.

**Scope.** A venue template and its call for papers decide the parts they specify, such as the page limit, margins, fonts, required sections and statements. This skill covers what they leave open, and the template wins where the two disagree.

## Goal

The deliverable is a Chinese issue report with one table per tier, in this order: 阻碍提交, 影响理解, 局部表达. Each row has five columns:

| 位置 | 原文 | 问题 | 修改建议 | 负责 skill |
| --- | --- | --- | --- | --- |

Rows are numbered continuously across tiers, so the user can answer "修 1-5", and each number starts its 位置 cell. A row that rests on something outside the manuscript, such as a project record or a measurement, names that source in its 问题 cell and says whether it was confirmed. Passed checks do not appear. A tier with no rows keeps its heading and says "未发现问题". One closing line names anything that could not be checked and why.

## Reader Standard

The report is read by an author deciding what to fix before a deadline. Every row must be locatable, quote the original, state one problem in one sentence, and give a fix concrete enough to apply. A row that reports a pattern the manuscript uses on purpose costs that author time and trust. Findings are never manufactured to make the report look thorough. A clean dimension contributes no rows.

## Modes

| Mode | When | Scope |
| --- | --- | --- |
| full | the user asks to check the paper, or before submission | all five dimensions, the consistency check, and the submission requirements |
| scoped | after a revision, or when the user names sections | the scan on changed files, rendered pages that changed, keys added or touched, and consistency for the changed claims |

The user's words decide whether the check is for a draft or for submission. Pending markers ("TODO", a project's pending macro) are listed as a count for a draft and as blocking rows for submission. "投稿前" and "pre-submission" mean submission.

## Read the Project First

1. Find the root `.tex` file, the build entry, any check scripts the project ships, and the project notes. Project notes are the README and docs in the project, agent instruction files such as `CLAUDE.md` or `AGENTS.md`, and the agent's memory for this project. A file that a note points to but that does not exist goes into the line on what was not checked.
2. Find the venue rules: the template, the call for papers and the page limit, what counts toward the limit, the required statements and their position, the anonymity policy, and font or file requirements.
3. When the project syncs with a remote through Git, fetch it. If the local copy is behind, tell the user before checking, because findings on an old copy are wasted. When there is no remote to fetch, such as an Overleaf project copied by hand, skip this step and say so in the coverage line.
4. Detect the manuscript's conventions and write them down as a list. That list includes caption style (a bold first sentence or not), the equation reference form, the run-in heading macro, the display-equation environment, the contribution-list environment, and table macros for deltas and best values. Only a pattern used the same way throughout enters the list. A pattern used two ways is a candidate row. Decisions recorded in the project notes, such as a fixed color meaning, also enter the list. Every dimension except the blind reader and the reviewer simulation receives the list, and a pattern that follows it is never reported.
5. Read the terminology record if the project keeps one.
6. Note the problems the project notes record as known and decided. Such a problem is not reported again, unless the manuscript text contradicts the record. That row quotes the text, names the record, and proposes a fix within the author's decision, such as disclosing the difference.

## Run the Dimensions

Run the five dimensions as parallel subagents. Each receives the root path, the conventions list, the mode, and its own instructions from [references/review-dimensions.md](references/review-dimensions.md). Each returns rows with: location, original, problem, suggested fix, owning skill, proposed tier, and the evidence for the finding.

1. **Deterministic scan.** Run `python3 -I <skill-dir>/scripts/scan.py <root.tex>`, where `<skill-dir>` is this skill's directory. Its hits are candidates. Confirm each in context, drop those that follow the conventions list or are false matches, and keep the rest.
2. **Rendered pages.** Build into a scratch directory, so the check writes nothing into the project. When the build entry runs remotely or writes into the project, use the existing PDF if it is newer than every source file, and name the PDF in the coverage line. Render every page to an image and inspect each page. Check layout defects, figure legibility, consistency of tables that play the same role, color consistency across figures, the end of the main body against the limit, and the statements' position. Three defects are easy to miss. A display equation inside a wrapped figure's span runs under the figure, because wrapped text does not narrow display math. A wrapped float that ends with a negative `\vspace` can let its caption run into the text below. Two tables of the same role can differ in header row count.
3. **Citations.** Verify every cited key in full mode, or the added and touched keys in scoped mode, with the procedure in the review-dimensions reference. Check bibliography comments and the limit of four distinct works per citation group throughout the main text, counting adjacent commands together across line breaks. Existing citation-density conventions do not override this limit. Batch the keys across subagents, each with no other context.
4. **Blind reader and reviewer simulation.** Two separate fresh-context readers. The blind reader receives only the PDF and a role prompt, and reports how the paper lands before any analysis. The reviewer simulation reads the PDF as an LLM reviewer would, and proposes meaning-preserving edits where wording undersells existing evidence. Neither sees this conversation, the author's intent, the project notes or the other's output. Start each where project notes and memory are not loaded, such as a headless run (`claude -p` or `codex exec`) from an empty directory that holds only the PDF. When only in-session subagents are available, use them and say in the coverage line that the readers may have seen project notes.
5. **Anonymity and leaks.** Check the source, the PDF, its metadata, figure files and supplementary material for names, affiliations, emails, user-named URLs, acknowledgments, self-identifying citations, file paths and secrets.

## Check Consistency

While the subagents run, the main agent checks that the paper says one thing:

- each claim in the abstract, contribution list and conclusion has its evidence in the body, at the same strength
- each number stated in prose matches its table or figure
- each term and symbol keeps one form and one meaning across sections, captions and appendix
- each baseline and method name is the same in every table and figure
- the scope stated in the opening matches the scope evaluated

A conflict between two locations becomes one row that quotes both.

## Submission Requirements

In full mode for submission, also check the items in [references/presubmission.md](references/presubmission.md): page limit, required statements and their position, anonymous mode, PDF metadata, embedded fonts, file size, supplementary material, and resolved references. Each failed item is a blocking row.

## Assign Tiers

| Tier | Meaning | Typical rows |
| --- | --- | --- |
| 阻碍提交 | violates a venue rule or the paper's integrity | body over the page limit, missing required statement, identity leak, undefined reference, fabricated or wrong citation, number contradicting its source, table row without a source, pending marker at submission |
| 影响理解 | a reader would misread or stop | claim stronger than its evidence, term used in two meanings, figure overlapping an equation, unreadable figure text, abrupt section transition, process text in the manuscript, numbers in the method |
| 局部表达 | correct but below the paper's standard | banned wording, em dash, a `\hline`, a main-text citation group over four distinct works across adjacent commands, unsuitable bibliography comments, inconsistent table headers, figure text below the size threshold |

The typical rows are examples. The tier follows the effect on the reader or the submission, not the dimension that found it. Figure text that cannot be read on the page at full size is 影响理解, and text that is readable but below the size threshold is 局部表达. A term used in two meanings is 影响理解 when a reader cannot tell which one is meant, and 局部表达 when a qualifier settles it.

## Merge and Filter

1. Merge rows with one cause into one row that lists every location. Twelve em dashes are one row. When the locations belong to different owning skills, write one row per owner.
2. Drop rows that follow the conventions list, rows about style choices the paper makes consistently, and rows a subagent could not support with evidence.
3. Order rows by tier, then by position in the paper.
4. Give each row exactly one owning skill: paper-framing, paper-opening, paper-method, paper-experiments, paper-visuals, paper-language or paper-typesetting. Bibliography entry format and versions belong to paper-typesetting. Whether a citation supports its sentence belongs to paper-opening. A reviewer-simulation proposal belongs to the skill that owns its location: the abstract, introduction and related work to paper-opening, the experiments to paper-experiments, and other wording to paper-language.

## After the Report

Wait for the user. When the user says "修", or names rows ("修 1、3、5"), apply the fixes through the owning skills, under each skill's own rules and stops. Then rerun only the checks that cover the fixed rows, and report which rows are resolved. Fixing never happens during the check itself.

## Stop and Discuss

The check is read-only, so it rarely needs to stop. Ask only when a venue rule cannot be found, for example an unknown page limit. Give the recommended value from the call for papers or the template. Ask at most three questions. When two official documents of the venue disagree, check against the stricter value without asking, and name both values in the coverage line.

## Long Tasks

The five dimensions are the subagent split. Citation verification splits further into batches of about ten keys. Rendered-page inspection splits into ranges of ten to twelve pages when the PDF is longer than that. Subagents for the scan, rendered pages, citations and anonymity return rows in the fixed format, and the scan subagent adds the number of dropped hits per check. The blind reader and the reviewer simulation return the forms their prompts ask for, and the main agent converts them into rows. The main agent merges, filters, assigns tiers and writes the report.

## Final Checklist

- No manuscript file changed during the check.
- Every row has location, original, problem, fix and owner.
- No row reports a pattern from the conventions list.
- Rows with one cause are merged.
- The blind reader received only the PDF and its role prompt, or the coverage line says it may have seen project notes.
- Passed checks are absent, and an empty tier says "未发现问题".
- The closing line names what was not checked, such as a failed build or an unreachable citation source.

## Delivery

The report is in Chinese. Quote manuscript text in English as written.

Deliver:

- the three tier tables, with continuous row numbers
- one line on coverage: dimensions run, the PDF inspected and its pages, keys verified, and whether the submission requirements were checked and passed
- one line on what was not checked, if anything

A row looks like this:

| 位置 | 原文 | 问题 | 修改建议 | 负责 skill |
| --- | --- | --- | --- | --- |
| 1. sections/method.tex:88，第 4 页 | `\begin{equation}` 位于 Figure 3 环绕区间内 | 行间公式与 wrapfigure 重叠 | 把 wrapfigure 移到公式之后的长段落旁 | paper-typesetting |
