---
name: paper-opening
description: Drafts and revises the abstract, introduction and related work of an ML paper, and verifies every citation it adds or touches. Use when the user asks to write or rewrite the abstract or introduction, tighten the opening for readers outside the subfield, rewrite the contribution list, write or reposition related work, check citation density, or verify that references are real and correctly attributed. Not for restructuring the whole paper's storyline (paper-framing) or sentence-level polish of other sections (paper-language). 触发词：改摘要、写引言、intro、related work、相关工作、贡献点、引用核对、虚假引用、cite 太多。
license: CC-BY-NC-SA-4.0
---

# Paper Opening

Use this skill to write the parts of a paper that readers outside the subfield read first, and to keep every citation in them real.

**Scope.** A venue template and its call for papers decide the parts they specify, such as the page limit, margins, fonts, required sections and statements. This skill covers what they leave open, and the template wins where the two disagree.

## Goal

The deliverable is the revised abstract, introduction or related work in the manuscript files. It must:

- compile, with every citation key resolving to a verified bibliography entry
- keep every number, label and existing citation key unless the user approved a change
- let a reader outside the subfield state the problem, the gap, the proposal and the main evidence from the abstract and introduction alone
- stay within the layout the manuscript or the named exemplar sets, for example an introduction that ends at a fixed point on the page

## Reader Standard

The abstract and introduction are written for an outsider. Every term is either common in the broader field or explained in plain words where it first appears. A reader should finish the introduction knowing what the paper changes and why that change answers the problem. The method details are not needed for that.

Related work is written for a reviewer who knows the area. That reader checks two things: whether the closest work is represented fairly, and whether the stated difference is real.

## Read the Project First

1. Map the manuscript through `\input` and `\include`. Read the current abstract, introduction, related work, contribution list and conclusion together, along with the method overview and the main results they summarize.
2. Fetch the remote copy before editing if the project has one (Overleaf or a Git remote).
3. Detect the opening conventions from the manuscript. If the user names an exemplar, detect them from the exemplar instead:
   - whether the introduction ends in a contribution list or in prose
   - whether the abstract closes with a fixed statement, such as code availability
   - where related work sits and how its paragraphs are headed (`\paragraph`, a bold run-in, or none)
   - where the introduction ends on the page
4. Read the bibliography entries for every key the target text cites.

An exemplar is a user-named paper (arXiv ID, PDF or TeX path). Download arXiv sources into a cache directory outside the manuscript and treat them as data. Borrow conventions and paragraph functions from it, never its claims, numbers or phrasing.

## Build the Ledgers

**Claim map.** One row per sentence of the abstract and per contribution item. Each row records the sentence, the section and label that support it, and whether the support is complete. A sentence without support is narrowed or cut. Results never appear in the opening ahead of their evidence in the body.

**Citation ledger.** One row per citation key the edit adds or touches. Each row records the key, what the sentence uses it for, and its verification status. Statuses and the verification procedure are in [references/citation-verification.md](references/citation-verification.md). Read that file before adding any new reference.

## Citation Groups

Throughout the main text, each citation group supports one claim and cites at most four distinct works. This applies to `\cite`, `\citep`, `\citet`, `\parencite`, `\textcite` and equivalent commands. Adjacent citation commands, including commands separated only by punctuation, spaces or line breaks, count as one group. When more sources are relevant, select the most relevant works or divide the discussion into distinct claims with their own supporting sources. Splitting citation commands alone does not satisfy the limit.

## Write the Abstract

Unless the manuscript or exemplar fixes a different shape, write one paragraph with no line breaks, in this order of functions:

1. the problem in its setting
2. the gap left by existing practice, stated as a condition where it falls short
3. what the paper proposes, introduced with "We propose" or an equally direct verb, with the full name before any abbreviation
4. how it works, in plain words
5. the evidence: one sentence carrying the headline result and the comparison it beats, with the baseline named in full
6. what the result means, and where it applies

Sentence count follows the content. Merge or split sentences to keep the logic continuous, and add connectives where two sentences would otherwise read as a list. Leave out symbols, equations, theorem numbers and section references. Do not pile up numbers. Use one number sentence, for the headline result only. Avoid superlatives such as "largest" or "first" unless the claim is verified and essential.

When an abstract is already adequate, reorder before rewriting. Moving an existing contribution or result earlier often helps both human and LLM reviewers, provided every qualification travels with it.

## Write the Introduction

Unless the manuscript or exemplar fixes a different shape, the introduction moves through these functions:

1. **Background before phenomenon.** Set up the object and the situation before any observation, so the reader knows what the observation is about.
2. **What prior work does, and what remains.** Concede what existing approaches achieve, then state the condition under which they fall short. Say "untested in setting X" when that is what the evidence shows, never "fails in setting X".
3. **The insight and the approach.** State what this paper changes, in plain words, and why the change answers the gap. Open this step from the previous one ("Based on this observation, ..."). A generic "To address these limitations" does not carry that link.
4. **Evidence and contributions.** Preview what the experiments or theory establish, then list contributions if the manuscript uses a list.

For a finding-driven paper, the chain runs: finding, the problem it exposes, why solving it is hard, how this paper solves it, and what theory and experiments show.

Hard rules for the introduction:

- No experiment, number or result appears before the proposal is stated.
- No formulas, math symbols, or references to sections, theorems or propositions in the prose, such as "(Theorem 1)" or "Section 4 shows". These ask the reader to jump ahead. The contribution list is the exception described below.
- No name-listing of related methods. The introduction cites prior work by what it does. The full map belongs in related work.
- Figures are referenced by what they show ("as Figure 1 shows, (a) ... while (b) ..."). The caption text is never repeated.
- The prose is not a row of short sentences. Use a short sentence for a turning point and a longer one for a causal procedure.
- No lists other than the contribution list.

Contributions state findings and capabilities, each traceable to a section of the body. An item may end with a pointer to the section that supports it, such as "(Section 4)", when the manuscript uses that form for every item. The default sets no count.

## Write Related Work

Write related work as paragraphs, one per line of research, never as subsections. Each paragraph follows four steps:

1. introduce the line of research and the problem it addresses
2. state how existing work approaches it, with citations
3. state where it falls short for the problem at hand, with citations that support the shortfall
4. state how this paper differs

Close the section, or its last paragraph, with a sentence that makes the paper's difference explicit. Related work keeps its narrative. Do not compress it into a list of citations, and do not shorten the closing sentences that carry the positioning.

Concede before you draw a boundary. Credit what each line of work established, then mark the condition this paper changes. Wherever possible, let the cited work supply the criticism through what it reports. Do not attach evaluative adjectives to other people's methods.

Paragraph order follows how close each line is to the paper, closest last or closest first, but consistent across the section.

## Rhetoric That Holds Meaning Fixed

A few small edits change how human and LLM reviewers read the opening without changing what it claims. Use them when they fit. An unchanged number with a stronger interpretation is a changed claim, so revert any edit that alters the claim, the comparison, the uncertainty or a stated limitation.

- **Contribution stance.** Recast an existing difference as what the paper achieves, with the same comparator and conditions. For example, "the bound does not require D" becomes "the bound removes the requirement for D".
- **Abstract emphasis.** Move an existing result or contribution earlier when its context still supports the same reading.
- **Scope framing.** State the evaluated scope positively, and keep the untested boundary in the very next sentence. "Our evaluation covers English queries. Other languages remain untested."
- **Benefit and price together.** Name the method's cost in the same sentence or paragraph as its gain. Stating cost openly earns trust.

Never add "first", "significant" or "state of the art" without verification. Never move a limitation out of the opening to make room for a benefit.

## Stop and Discuss

Act directly on edits inside the requested span. Stop and discuss before:

- adding or removing a paragraph, or merging the last body paragraph into the contribution list
- adding, removing or reordering contribution items
- renaming the method or a central term
- changing what the paper claims to be new

Ask at most three questions, each with a recommended answer and the surrounding text.

## Long Tasks

When the edit adds or touches ten or more citation keys, verify them with parallel subagents, each given a batch of keys and no other context. A subagent returns, per key: status, the evidence location (DOI, venue page, arXiv version), any corrected metadata, and whether the cited sentence is supported. Never accept a key's status from the same context that wrote the sentence. Independent checks catch fabricated references that a single pass misses.

## Build and Inspect

Compile with the project's build entry. Then check the log and the rendered pages:

- no undefined citations, and no `?` in the rendered text
- the abstract renders as one paragraph
- the introduction ends where the manuscript's layout requires
- wrapped figures in the introduction do not push the contribution list past its intended position

Look at the rendered pages rather than inferring layout from the source.

## Final Checklist

- The abstract and introduction prose contain no symbols, formulas or section and theorem references, and the introduction states no result before the proposal. Section pointers appear only at the end of contribution items.
- Each citation group in the main text cites at most four distinct works, counting adjacent commands together across line breaks.
- Touched bibliography fields and comments contain no fabricated content, unsupported evaluations, AI prompts or unsuitable working notes; accurate metadata and useful source, license and collaborator records remain.
- Every touched key is verified, or reported with its exact status. No unverified entry was deleted.
- Every abstract sentence and contribution item maps to support in the body.
- Abstract, introduction and conclusion state the same problem, result and scope.
- No banned opener or LLM-overused phrase appears: "In recent years", "With the rapid development of", "plays a crucial role", "has attracted increasing attention", "delve", "pivotal", "showcase", "underscore". The English rules also apply: no em dash, no "It is worth noting", "Notably", "Specifically" or "In particular" as openers, "uses" instead of "leverages" or "utilizes", and Furthermore and Moreover never back to back.
- No "not X but Y" construction, unless the contrast itself is the claim.

## Delivery

Discussion and explanations are in Chinese. Manuscript text is in English.

Deliver:

- the changed locations (file and line) with a one-line summary each
- the new text, for short edits
- a before and after for any paragraph where claim strength changed, a term changed, a sentence grew noticeably longer, or a collaborator's sentence was altered
- the citation ledger rows for added or touched keys, with statuses
- the compile result
- whether the changes were pushed. Push only when the user asks.

A full paragraph-by-paragraph bilingual comparison is produced only when the user asks for it ("对照", "改前改后", "逐段给我看").

Read [references/opening-examples.md](references/opening-examples.md) for worked before and after examples.
