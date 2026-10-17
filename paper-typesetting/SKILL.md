---
name: paper-typesetting
description: Lays out and compiles an ML paper in LaTeX, covering preamble conventions, float placement, wrapped figures, the main-body page budget, required statements, appendix numbering, bibliography hygiene, anonymity settings and synchronization with the Overleaf or Git remote, and checks every change on rendered pages. Use when the user asks to fix layout or white space, fit the page limit, move figures, fix compile errors or undefined references, clean the bib file, adopt another paper's template or layout, place ethics or reproducibility statements, or pull and push the manuscript. Not for drawing figures or restructuring tables (paper-visuals) or for wording (paper-language). 触发词：排版、编译、超页、压到 9 页、留白、图的位置、wrapfigure、vspace、bib、参考文献格式、模板、照搬排版、拉取、推送、Overleaf。
license: CC-BY-NC-SA-4.0
---

# Paper Typesetting

Use this skill to make the compiled paper fit its venue and read cleanly page by page, without changing its content.

**Scope.** A venue template and its call for papers decide the parts they specify, such as the page limit, margins, fonts, required sections and statements. This skill covers what they leave open, and the template wins where the two disagree.

## Goal

The deliverable is the compiled PDF and the changed LaTeX sources. The PDF must:

- compile through the project's own build entry with no undefined references or citations
- end the main body within the venue's page limit, with required statements where the venue puts them
- keep every number, label, citation key and sentence that existed before, unless the user approved a cut
- keep the preamble conventions the manuscript already uses
- show no layout defect on the rendered pages: no figure directly under a heading or at a page bottom, no overlap, no large white gap, no isolated caption
- match the remote copy, with collaborators' edits preserved

## Reader Standard

A reviewer flips through the PDF before reading it. Figures should sit near the text that discusses them, pages should look evenly filled, and fonts and spacing should be uniform. Good layout goes unnoticed. Every defect the reviewer notices costs attention that should go to the content.

## Read the Project First

1. Find the build entry: a build script, a Makefile or the project notes. Find where compilation runs, since some projects compile on a remote machine, and where the PDF lands. Run any check scripts the project provides.
2. Fetch the remote copy before editing, following [Synchronize with the Remote](#synchronize-with-the-remote).
3. Read the venue rules from the template and the call for papers: the main-body page limit, what counts toward it, the required statements and their position, the anonymity option, and font or file requirements.
4. Read the preamble and detect its conventions:
   - caption settings, including a bold first sentence and caption font size
   - float spacing settings and placement defaults
   - the display-equation environment and any size setting attached to it
   - the equation reference form and the run-in heading macro
   - appendix numbering and table font sizes
   - link colors and custom environments, such as a contribution list
5. Render the current pages to images and look at them before planning changes.

When a collaborator's latest version changed the preamble, for example restoring the official template, the latest version is the convention. Restoring the earlier preamble is a decision for the user.

When the user names an exemplar layout ("照搬这篇的排版"), detect the same conventions from the exemplar and apply them through the preamble and macros. Content, numbers and wording stay.

## Build the Page Ledger

One row per page of the main body, plus one for the appendix start.

| Column | Content |
| --- | --- |
| Page | page number |
| Starts | sections or run-ins that start on the page |
| Floats | figures and tables on the page, with position (top, bottom, wrapped) |
| Defects | white gap, figure under heading, figure at page bottom, overlap, overfull line, float far from its reference |

The ledger records where the main body ends, compared against the limit. Every fix is tested against the ledger after a rebuild.

## Layout Rules

These rules hold unless the venue requires otherwise.

- **Spacing commands only inside floats.** `\vspace` appears only inside figure and table environments. Headings and paragraphs never receive manual spacing. One user stated it as "vspace 确定是只有图像和表格，没有section".
- **Body text keeps the template's size.** The body, headings and captions keep the sizes the template sets. No margin change, no line-spread change, and no `\small` around body text.
- **One base size for every table and every equation, set once.** Set `\small` in the preamble for every table and numbered display environment the project uses, including `tabular`, `tabular*`, `tabularx`, `equation`, `align`, `gather` and `multline` where present, or through the project's shared macros. Do not add unnumbered displays to set their size. Overflow-table scaling below is the sole exception to the shared base size.
- **A table carries no formatting of its own.** No font size, no `\tabcolsep`, no `\arraystretch`, no `\vspace` and no per-table rule macro, since those values live in the preamble once. `\centering` inside the float stays. This is the "表格默认什么都不要带" rule: a table's source holds its cells, its booktabs rules and its caption, nothing else.
- **Overflow is `\resizebox`, and only that.** A table too wide for the column or page is wrapped once in `\resizebox{\linewidth}{!}{...}`. Do not reach for `\small`, `\footnotesize`, a narrower `\tabcolsep` or `adjustbox` to make it fit. Check the printed text size on the rendered page after the resize.
- **Rules come from booktabs.** `\toprule`, `\midrule` and `\bottomrule`, with `\cmidrule` under a grouped header. Never `\hline`, never `\cline`, never a vertical rule.
- **Figures and headings.** A figure never sits directly under a section heading. As the same user put it: "图像不能出现在标题下面".
- **Figures and page bottoms.** A figure does not sit at the bottom of a page in the main body, unless the venue's template places it there.
- **No consecutive figures without text.** Two figures in a row become one figure with panels, a side-by-side pair, or a wrapped figure beside text.
- **Wrapped figures.** A `wrapfigure` starts before a paragraph long enough to cover its height. It never precedes a display equation, a list, a heading or a page break within its span. Wrapped text does not narrow display math, so an equation inside the span runs under the figure.
- **Labels after captions.** `\label` follows `\caption` in floats, and sits inside the environment that produces the number for equations.
- **Placement through the template.** Use the template's float mechanism. `[H]` everywhere, or forced placement on every float, is avoided.

[references/layout-fixes.md](references/layout-fixes.md) holds the fix for each defect type. Read it before fixing a defect.

## Fit the Page Budget

When the main body exceeds its limit, apply this order. Rebuild after each step, and stop when it fits:

1. remove white space by moving floats, merging adjacent small figures, or wrapping a narrow figure beside text
2. pull up paragraphs whose last line holds one or two words, by a minimal wording change through the rules of paper-language
3. cut sentences that restate earlier sentences, through the rules of paper-language
4. shrink figures within legibility, through the rules of paper-visuals
5. move detail to the appendix, such as full configurations, secondary tables and long derivations, with a precise reference

Never shrink body text, add spacing at headings, change margins or delete content the user did not approve. Tables and equations keep the single size set in the preamble, so fitting a table means shortening it, regrouping columns, splitting it or moving detail to the appendix before any `\resizebox`. Steps 3 and 5 change content, so present the list of cuts or moves to the user before applying them.

## Statements, Appendix and Bibliography

**Statements.** Ethics, reproducibility and LLM-usage statements go where the venue specifies, often right after the main body and outside the page count. Some venues require the statements to begin on the page after the limit. Check the position on the rendered page.

**Appendix.** Numbering follows the template and the manuscript's existing form. Every appendix reference in the body resolves to the right section. Where the paper has proofs, the first appendix is `Proofs`, ordered as `paper-method` prescribes: subsections follow the order of the body, each proof follows its restated statement, and a result the body never states is stated and proved where the appendix first uses it. Where the paper has no proof, the first letter goes to the first real appendix content.

**Bibliography.** The bib file is part of the paper:

- remove fabricated claims, unsupported judgments, AI instructions and working notes unsuitable for submission from `note`, `annote`, `comment` and `addendum` fields, `@Comment{...}` blocks and `%` comments; remove scraping timestamps and access dates the style does not require
- preserve accurate publication metadata, required notices, source and license information, and collaborator review comments unless their removal is authorized; cleaning a comment does not delete its bibliography entry or citation key
- correct author names and venues against the published version
- keep keys stable, because other sections cite them
- flag references from before 2000 that are not foundational works, and never delete references in bulk
- report suspected fabricated entries to paper-opening's verification procedure

Use [citation verification](../paper-opening/references/citation-verification.md) for the source order and comment cleanup. Each citation group at one location in the body cites at most four works, counting adjacent citation commands together even across source lines. Keep the most relevant sources or divide the prose into distinct supported claims; splitting commands alone does not reduce the group.

**Anonymity.** For a double-blind submission, use the template's anonymous option, hide acknowledgments, and clear author names from PDF metadata.

## Synchronize with the Remote

1. Fetch the remote before editing. Collaborators may have changed text or left comments.
2. Merge without overwriting collaborators' edits or comments. When both sides changed the same lines, show both versions to the user and wait.
3. Never force-push, and never discard remote commits.
4. Push only when the user asks. A standing instruction such as "改完直接推" holds for the rest of the session.
5. After pushing, confirm that the remote holds the new commit.

## Stop and Discuss

Act directly on fixes that move floats, fix compile errors or clean bib fields. Stop and discuss before:

- changing the preamble in a way that affects the whole paper, such as caption style, float spacing or fonts
- cutting sentences or moving content to the appendix to fit the budget
- restoring a template or preamble that a collaborator changed
- changing the order of sections or statements

Ask at most three questions, each with a recommended answer and the rendered pages that show the problem.

## Long Tasks

A full layout pass inspects every page. Use parallel subagents to inspect rendered page images in batches, for example pages 1 to 3, 4 to 6, 7 to the body end, and the appendix. Each returns the page-ledger rows for its pages, with the source line of each defect.

Fixes are applied by the main agent, one at a time, from the first defective page forward, with a rebuild after each fix. Each fix moves everything after it, so a defect on a later page may disappear or change.

## Build and Inspect

Compile with the project's build entry. Then:

- read the log for undefined references and citations, missing files, font substitutions and overfull lines wider than a few points
- render every changed page and its neighbors to images and look at them, for example with `pdftoppm -r 100`
- locate the last page of the main body and compare it with the limit. A label at the end of the body, if the project defines one, gives the page number directly
- run the project's own check scripts if it has any

Report what was inspected. A clean log without looking at the pages is not an inspection.

## Final Checklist

- The build finishes with no undefined references or citations.
- The main body ends within the limit, and the statements sit where the venue requires.
- No `\vspace` outside floats, no margin change, no change to body font size.
- Tables and equations use the single base size set in the preamble. No table carries its own font-size or spacing setting; one `\resizebox{\linewidth}{!}{...}` is allowed only for an overflowing table, with rendered legibility checked.
- No figure directly under a heading, at a page bottom, or overlapping text or equations.
- No two figures in a row without text between them, unless they form one figure.
- Every number, label, citation key and approved sentence is still present.
- The bib file has no fabricated or unsuitable comments or unneeded timestamps; accurate required metadata and source/license notices remain, and no reference was deleted in bulk.
- Every citation group in the body contains at most four works, including adjacent commands and line breaks.
- The remote holds the final version, or the delivery says it was not pushed.

## Delivery

Discussion and explanations are in Chinese.

Deliver:

- the changed files with a one-line summary per change
- rendered images of each changed page, before and after
- the main-body end page against the limit
- the remaining log warnings that affect the output
- the content cuts or moves applied, if the user approved any
- whether the changes were pushed. Push only when the user asks.
