---
name: paper-experiments
description: Drafts and revises the experiments of an ML paper, covering the setup, main results, ablations, analysis, statistics and benchmark-construction sections, and keeps every reported number and row name traceable to a result source. Use when the user asks to write or rewrite results or ablations, turn tables into analysis, cut restated numbers, decide what to compare, frame results positively without hiding failures, check statistics or error bars, or describe a benchmark or dataset contribution. Not for designing or typesetting tables and figures (paper-visuals) or for the method section (paper-method). 触发词：改实验、写实验部分、结果分析、消融、不要复述数字、实验设置、对比哪些基线、统计口径、误差条、benchmark 构建。
license: CC-BY-NC-SA-4.0
---

# Paper Experiments

Use this skill to turn results into evidence for the paper's claims, with tables carrying the numbers and prose carrying the analysis.

**Scope.** A venue template and its call for papers decide the parts they specify, such as the page limit, margins, fonts, required sections and statements. This skill covers what they leave open, and the template wins where the two disagree.

## Goal

The deliverable is the revised experiments section in the manuscript files. It must:

- compile, with every table and figure reference resolving
- keep every number, label and citation key that existed before, in its literal form
- answer one stated question per results paragraph, and link each answer to a claim from the introduction
- trace every number in the prose, every table row and every ablation variant name to a result source
- keep the setup no longer than it was before the edit
- keep any failed primary comparison visible

## Reader Standard

Write for a reviewer who reads a results paragraph next to its table. After each paragraph, that reader should know the question being answered, which comparison to look at, what the comparison shows, and what it means for the paper's claim. The table already gives the values. Prose that lists them again gives the reader nothing new. One user put the rule as "实验部分避免过多列数字而是分析".

Analysis still needs substance. A section cut down to one-line verdicts reads as thin evidence. Each paragraph keeps its interpretation and its scope.

## Read the Project First

1. Map the manuscript through `\input` and `\include`. Read the contribution list and the method first, because they define what the experiments must support. Then read every table, figure and paragraph of the experiments and the related appendix.
2. Find the result sources: run outputs, logs, extraction scripts, result files, or tables the user supplied. The project notes often record where they live. Ask only when the files do not reveal them.
3. Fetch the remote copy before editing if the project has one.
4. Detect the conventions from the manuscript, or from the exemplar if the user names one:
   - how the section is grouped (setup, main results, ablations, analysis)
   - the run-in style for ablation and analysis blocks, and whether variant names are set in italics
   - how prose points to tables and figures
   - where full configurations live

## Build the Result Ledger

One row per number, row name or variant name that the prose or a table states.

| Column | Content |
| --- | --- |
| Item | the number or name as written |
| Location | file and line, or table label and cell |
| Source | the run output, log, script or user-supplied table that produces it |
| Status | matches, mismatch, or no source |

A mismatch is reported with both values and is never resolved by picking the better one. An item with no source is reported. Table rows and ablation names come only from sources. Generated drafts tend to invent plausible variants such as "w/o Replay" or "Uniform allocation". A name absent from the sources is removed or reported, never kept because it reads well.

Keep a second, short ledger of questions: each experiment, the question it answers, and the introduction claim it supports. An experiment that supports no claim is a candidate for the appendix.

## Write the Setup

The setup holds only what changes the meaning of a comparison: data and splits, models, baselines named in full with citations, metrics and their direction, and the budget that the comparison holds equal. Full hyperparameters and per-task configurations go to the appendix with a precise reference.

**The setup never grows during a revision.** A new detail replaces a less important one or goes to the appendix.

**No process or status text.** The manuscript never states pending runs, dates, archived or historical results, internal run names, which machine ran which job, or how the work was scheduled. The number of repetitions appears only where it defines an uncertainty estimate.

**No benchmark targeting.** Training data, environments and design choices are never described as built for a downstream benchmark. Transfer to a benchmark is reported as transfer.

## Write the Results

Organize results by question, not by run order or benchmark list. Each results paragraph moves through four functions, merged or expanded as the content needs:

1. the question and the comparison the reader should look at, with the table or figure reference
2. the observation, stated as a pattern, with at most one key number when the number itself carries the point
3. the interpretation: what the observation means for the claim
4. the scope: where the observation holds, stated once

**Lead with supported positive evidence.** Open with the result that most directly supports the claim. Give exceptions their own sentence after it, without hedging every sentence. A failed primary comparison stays in the main text. Ordering may change, and visibility may not.

**State causes only with evidence.** When the cause of an observation is unknown, write "The cause has not been established." and add no speculation after it.

**Hold the claim fixed while framing.** Moving the strongest evidence earlier, or recasting a difference as what the method achieves, is allowed when the comparator and conditions stay the same. An unchanged number with a stronger interpretation is a changed claim. Revert any edit that alters the claim, the comparison, the uncertainty or a stated limitation.

## Write Ablations and Analysis

Group ablations by module or role, one run-in block per module, in the detected run-in style. Inside a block, name each variant as the sources name it, in italics when the manuscript does. Each variant states what was removed or replaced and what changed as a result.

Keep the evidence types apart:

- removing a component shows its contribution in this system under these conditions
- replacing a component tests whether a simpler or alternative design suffices
- a hyperparameter sweep shows sensitivity and a working range
- only an intervention on the hypothesized object supports a mechanism claim

Analysis subsections each answer one question, usually with one figure. Detailed statistics, per-item breakdowns and long case listings go to the appendix.

## Statistics and Comparisons

[references/statistics-and-benchmarks.md](references/statistics-and-benchmarks.md) covers denominators, failure handling, uncertainty, fair comparison and benchmark papers. Read it whenever the edit touches an aggregate, an error bar, a significance claim or a benchmark contribution. The rules that apply to every edit:

- Error bars, intervals and "±" values come from computed statistics, with their meaning stated. None are invented.
- "Significant" is used only for a test that was run. "Robust" names the perturbation it survives.
- Percentage points and relative percentages are named correctly.
- Reported values copied from other papers are marked apart from values this project reproduced.
- Pending results use the project's pending marker in a draft and never carry an imagined number.

## Decide What to Compare

When the user asks what to compare, recommend baselines that test the claim: the closest methods, a simple method that could explain the gain, and the same model without the proposed change. Compare at a matched budget, or show the budget difference. A table that spans several benchmarks on one metric reads more easily with an average column whose weighting is stated. More baselines never substitute for a fair comparison.

## Fit the Section to Its Space

When the experiments exceed their space, apply this order and stop when it fits:

1. cut prose that restates table values
2. merge paragraphs that answer the same question
3. move secondary tables and per-benchmark breakdowns to the appendix, with a pointer
4. hand table compaction to paper-visuals and page placement to paper-typesetting

Never cut a setup item that defines a comparison, a failed primary comparison, or the interpretation sentence of a result.

## Stop and Discuss

Act directly on edits inside the requested span. Stop and discuss before:

- adding or removing an experiment, a baseline, a table row or an ablation variant
- changing the primary metric or the aggregation
- moving a main result to the appendix or an appendix result to the main text
- claiming a mechanism from the results
- a new figure concept, which also involves paper-visuals

Ask at most three questions, each with a recommended answer and the evidence behind it.

## Long Tasks

When the task rewrites the whole experiments section or touches three or more subsections, use parallel subagents, one per subsection or main table. Each returns:

- the question its part answers and the claim it supports
- every number stated in prose, with the table cell and source that holds it
- every row and variant name, with its source
- every mismatch or item without a source
- process or status text found

The main agent merges the returns into one result ledger and one question ledger before editing. The rewritten section must read as one argument for the paper's claims, not as table summaries in a row.

## Build and Inspect

Compile with the project's build entry. Check the log for undefined references. On the rendered pages, check that each results paragraph sits near the table it discusses, and that the setup has not pushed a main table to a later page.

## Final Checklist

- Every number in the prose matches its source and its table cell. No paragraph restates a row of table values.
- Every table row and ablation variant name has a source.
- The setup is no longer than before, and contains no process or status text.
- Every results paragraph names its question, its comparison and its interpretation.
- A failed primary comparison is visible in the main text.
- No causal claim lacks supporting evidence, and unknown causes use the fixed sentence.
- No phrasing presents the method or its training data as designed for a benchmark.
- No error bar, significance claim or "first" lacks a basis.
- The English rules hold: no em dash, no "It is worth noting", "Notably", "Specifically" or "In particular" as openers, "uses" instead of "leverages" or "utilizes", and no "not X but Y" unless the contrast is the claim.

## Delivery

Discussion and explanations are in Chinese. Manuscript text is in English.

Deliver:

- the changed locations (file and line) with a one-line summary each
- the new text, for short edits
- result-ledger rows with status mismatch or no source
- a before and after for any paragraph where claim strength changed, a term changed, a sentence grew noticeably longer, or a collaborator's sentence was altered
- the compile result
- whether the changes were pushed. Push only when the user asks.

A full paragraph-by-paragraph bilingual comparison is produced only when the user asks for it ("对照", "改前改后", "逐段给我看").

Read [references/result-examples.md](references/result-examples.md) for worked before and after examples.
