---
name: paper-typesetting
description: Lays out and compiles an ML paper in LaTeX, covering preamble conventions, float placement, wrapped figures, the main-body page budget, required statements, appendix numbering, bibliography hygiene, anonymity settings and synchronization with the Overleaf or Git remote, and checks every change on rendered pages. Use when the user asks to fix layout or white space, fit the page limit, move figures, fix compile errors or undefined references, clean the bib file, adopt another paper's template or layout, place ethics or reproducibility statements, or pull and push the manuscript. Not for drawing figures or restructuring tables (paper-visuals) or for wording (paper-language). 触发词：排版、编译、超页、压到 9 页、留白、图的位置、wrapfigure、vspace、bib、参考文献格式、模板、照搬排版、拉取、推送、Overleaf。
license: CC-BY-NC-SA-4.0
---

# Paper Typesetting

Use this skill to make the compiled paper fit its venue and read cleanly page by page, without changing its content.

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
- **No global shrinking.** No global `\small`, no change to margins, line spread or the template's font sizes. A local font size for one table is allowed as the last step of fitting that table.
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

Never use global `\small`, spacing at headings, margin changes or deletion of content the user did not approve. Steps 3 and 5 change content, so present the list of cuts or moves to the user before applying them.

## Statements, Appendix and Bibliography

**Statements.** Ethics, reproducibility and LLM-usage statements go where the venue specifies, often right after the main body and outside the page count. Some venues require the statements to begin on the page after the limit. Check the position on the rendered page.

**Appendix.** Numbering follows the template and the manuscript's existing form. Every appendix reference in the body resolves to the right section.

**Bibliography.** The bib file is part of the paper:

- remove `note` fields that make informal or unsupported remarks, and scraping timestamps or access dates that the style does not require
- correct author names and venues against the published version
- keep keys stable, because other sections cite them
- flag references from before 2000 that are not foundational works, and never delete references in bulk
- report suspected fabricated entries to paper-opening's verification procedure

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
- No `\vspace` outside floats, no global font shrinking, no margin change.
- No figure directly under a heading, at a page bottom, or overlapping text or equations.
- No two figures in a row without text between them, unless they form one figure.
- Every number, label, citation key and approved sentence is still present.
- The bib file has no informal notes or timestamps, and no reference was deleted in bulk.
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
