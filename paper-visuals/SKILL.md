---
name: paper-visuals
description: Designs, draws, polishes and audits the figures of an ML paper through a staged workflow (project reading, a shared figure brief, concept approval, a reproducible draw.io, TikZ or plotting source, vector export, scripted checks and rendered-page comparison with the previous version), and also unifies tables and writes captions. Use when the user asks to draw or redraw a method, overview or Figure 1, polish a figure without changing its logic, fix a figure that looks generated, rigid or inconsistent, fix figure fonts, colors or text size, plot results from data, restructure or unify tables, fix table headers, or rewrite captions. Not for deciding which experiments to run or writing result analysis (paper-experiments), or for page placement and float spacing (paper-typesetting). 触发词：画图、改图、方法图、主图、Figure 1、优化图的呈现、不改逻辑、图太丑、太死板、AI 味、配色、字体不统一、字太小、drawio、数据图、表格、表头、统一表格、caption、图注。
license: CC-BY-NC-SA-4.0
---

# Paper Visuals

Use this skill to make each figure and table carry one point clearly, in the paper's own terms, and to make all of them look like one designed set. Figures get a full production workflow, because they fail more often than any other part of a paper and every failure is visible at a glance.

**Scope.** A venue template and its call for papers decide the parts they specify, such as the page limit, margins, fonts, required sections and statements. This skill covers what they leave open, and the template wins where the two disagree.

## Goal

The deliverables are figure sources, exported figures, table LaTeX and captions, inserted in the manuscript. Each must:

- support one stated point, which the caption's first sentence names
- use the paper's terms verbatim for every word that appears in it
- keep every element of the original unless the user approved removing it
- trace every plotted value and table cell to a result source
- be vector where the content allows, with every font embedded, sized for its inserted width
- follow the figure brief, so fonts, colors, strokes and spacing match across figures
- read better than the previous version on the rendered page, at full size and as a thumbnail

## Reader Standard

A reviewer looks at the figures before reading the text around them. Within a few seconds that reader should know what a figure shows, which element is the paper's method, how information flows, and which direction is better. The figure should look designed by the authors for this paper. Default tool colors, mixed fonts, rows of identical boxes and labels lifted from code tell the reviewer it was not.

## Modes

The user's words decide the mode. The named target decides the scope. When the user names one figure file, only that file and its export change, and the manuscript changes only to insert the new export. One user put it as "别动我的论文，我让你改这个svg".

| Mode | Typical request | May change | Approval before building |
| --- | --- | --- | --- |
| new figure | 画一张方法图、新的 Figure 1 | everything | the concept plan |
| redesign | 重画、逻辑不对、太死板 | structure and elements | the concept plan and the list of added or removed elements |
| style polish | 优化呈现、美化、不改逻辑 | fonts, colors, strokes, spacing, alignment, geometry | none, once the brief exists |
| results plot | 画结果图、重画数据图 | encoding, layout, style | a change in what the plot compares |
| table and caption | 统一表格、改图注 | structure, rules, wording | adding or removing rows or columns |
| audit | 检查图 | nothing | none |

Style polish keeps the figure's logic: every element, label, symbol and panel, and the cells each arrow connects. Positions, sizes, the direction of flow on the page, alignment and line breaks are geometry, and a polish may change them. One user stated the mode as "不更改原本图像逻辑，但是优化画图呈现". A change that removes, rewords, reconnects or hides an element is a redesign step and needs approval.

A request can carry a constraint and complaints together, such as "不改逻辑" with "太死板" and "流程要优化". The constraint decides the mode, and the complaints become goals of the polish.

## Read the Project First

1. Locate each target figure's source and how it is produced: a `.drawio` file, a build script that writes it, TikZ code, a plotting script with its data, or an SVG. A raster file without a source limits the edit to what can be done on the image, and the delivery says so.
2. Find earlier versions and any figure brief or audit notes the project keeps. Make sure the current version can be recovered before editing, through Git or a copy in a sibling version folder.
3. Find the tools on this machine: the draw.io desktop application and its command-line export, a TeX installation for TikZ, the plotting library, and the fonts the figures use.
4. Find each figure's inserted width: the `\includegraphics` width times the text or column width of the template. Find the caption font size from the template.
5. Render the pages that hold the targets and look at them. Read the text that references each figure, and the method and experiment terms it must match.
6. Detect conventions from the manuscript, or from an exemplar the user names: caption style, subfigure labels, the color of each method or role, the figure font, how symbols are typeset, and table rules and macros.

## Write the Figure Brief

The brief is the style ledger for every figure in the paper. Write it once, before the first figure is built, and save it beside the figure sources so later edits reuse it. When the project already has one, it is the convention. When existing figures share a style, the brief records that style rather than inventing a new one. The one exception is text that prints below the size threshold in Export and Verify. For that role the brief sets the threshold size and lists the figures that differ until they are rebuilt. Run `figure_audit.py style` on the existing sources to see the values each role uses in each figure, with counts. Recording the existing style needs no approval. Any other change to a shared value is discussed first.

The brief fixes, by role:

- typography: the label font, the symbol font that matches the paper's math, sentence case, bold only for titles and group tags, and a size per role given in printed points at the inserted width
- shapes and strokes: one corner size and one stroke weight per role (group frames, cards, chips, main flow, feedback, pictograms)
- color: one hue per method or role with its meaning, fixed tint levels for frames and cards, the neutrals for text, borders and arrows; a detail figure uses at most two accents plus grey, and an overview uses one hue per module
- geometry: the canvas width for each placement class (full width, column, wrapped) and the conversion from canvas units to printed points
- export commands, and the checks every figure must pass

[references/figure-brief.md](references/figure-brief.md) holds the brief template, the per-figure audit template and the subagent return format.

## Build the Ledgers

**Element ledger**, one per figure. One row per element: box, arrow, label, icon, formula or panel, the paper term it shows, where the paper defines that term, and whether the wording matches. An element whose wording has no match is renamed to the paper's term or reported.

**Number-source ledger**, one per table or data plot. One row per cell or series: the value as written, the source that produces it, and the status (matches, mismatch, no source). Rows and series names come only from sources.

## Design the Figure

New figures and redesigns pass through a concept before anything is drawn.

1. **State the point.** One sentence for what the figure must show and which claim it supports. Two unrelated points make two figures or two panels.
2. **Choose the type.** A Figure 1 shows the problem and why current methods fall short, often through one running example. An overview shows the whole method as modules. A detail figure, often wrapped beside text, shows one mechanism. A results plot shows one comparison.
3. **Choose the content.** Keep the key process and the key formulas, and convey everything else through grouping, position, arrows, icons and small concrete examples. One user stated it as "图像只留关键流程和关键公式其他用视觉元素表示".
4. **Compose around modules.** Each module becomes a region, framed lightly. Loops return as arrows, and phases such as training and inference are separated by position or a frame. A row of equal boxes joined by arrows reads as a list, and one user rejected it as "不应该出现这种多个块线性流程并排".
5. **Present the concept** to the user as a short Chinese plan: the point, the regions, the flow, the formulas kept and where the figure goes. Add a rough layout sketch when the layout is the question. An image model may produce that sketch, and it never becomes the figure.

[references/figure-design.md](references/figure-design.md) covers figure types, composition, layout rules, typography, color, results plots and the signs that a figure looks generated. Read it before designing or redrawing.

## Build the Source

- Draw in an editable, reproducible source: the tool the project already uses, otherwise draw.io for diagrams, TikZ for math-heavy schematics and a plotting script for data. [references/drawing-tools.md](references/drawing-tools.md) gives the procedure for each tool, including draw.io file structure, build scripts, export commands and plotting defaults.
- Take every font, size, color, stroke and radius from the brief. A value that is not in the brief is added to the brief first.
- Prefer a build script that edits the source by cell id over manual edits, so a style change applies to every figure at once and a polish can be shown to keep every cell.
- Words in a figure are the paper's terms. Code identifiers, file names, keyword arguments, comments and flags such as `t/f` never appear. One user rejected a figure with "图表里的文字必须正规…t/n/f这种代码comment绝对不能出现在图表". Symbols are typeset as in the paper.
- Method figures carry no hyperparameter values. A value belongs in the setup.
- Results plots are generated from data by a script. Plotted points are never edited by hand.

## Export and Verify

Each figure goes through this loop until every check passes.

1. **Export** a vector PDF, cropped, with fonts embedded, and a PNG preview.
2. **Run the scripted checks** with `python3 -I <skill-dir>/scripts/figure_audit.py`:
   - `drawio` on the source, with `--insert-width-pt` and `--caption-pt`, for printed text sizes, fonts, colors, decoration, raster images and code-like labels
   - `diff` between the previous and new source for a style polish. It compares cell ids, labels, element kinds, the cells each arrow connects and visibility, and lists line-break changes separately. Every removed, added, reworded, reconnected or hidden element must be one the user approved. Positions are not compared, so arrow routes and arrows that touch no cell are checked on the render
   - `pdf` on the export, for fonts that are not embedded, Type 3 fonts, raster resolution and text sizes
   - `style` across all figure sources, for the values each role uses, to compare with the brief
3. **Look at the figure on the compiled page**, three ways: at full size for overlaps, clipping, alignment and arrow routes; as a thumbnail for balance, density and color; in grayscale for whether encodings survive without color. When the paper cannot be built, render the exported figure alone at its inserted width, as [references/drawing-tools.md](references/drawing-tools.md) shows, and say so in the delivery.
4. **Compare with the previous version** side by side at the same size. The new version must read better at thumbnail size and lose nothing at full size. When it does not, stop and show both versions to the user. One user asked for exactly this: "先停止，看一下和历史版本比".
5. **Fix and repeat.** A script pass without looking at the page is not a check.

Text below about 70% of the caption size is reported with its location, and is enlarged only when the layout allows. The usual fix raises that role's size in the brief for every figure of the same placement class, and makes room by shortening labels or tightening spacing. Changing one figure's canvas width instead would give it a different printed size from its siblings.

## Build a Table

- Use booktabs rules (`\toprule`, `\midrule`, `\bottomrule`, `\cmidrule`). No `\hline` and no vertical rules.
- Tables of the same role share the number of header rows, the rule pattern, the label font, the method order, and the choice between symbols and words in headers. A stacked header cell counts as the lines it renders.
- Every value comes from its source, at the source's precision, consistent within each column.
- Mark the best value only within comparable groups, by the metric's direction, and state the marking in the caption.
- Keep the project's macros for deltas, best values and highlighted rows.
- The table source carries cells, booktabs rules and its caption, and nothing that sets size or spacing: no `\small`, `\footnotesize`, `\tabcolsep`, `\arraystretch` or `\vspace`. The paper sets one size for all tables and all equations in the preamble. A table wider than its slot is wrapped in `\resizebox{\linewidth}{!}{...}` and in nothing else. A global font size does not enter the body text.

[references/tables-and-captions.md](references/tables-and-captions.md) holds table and caption examples and the consistency checks. Read it before unifying tables.

## Write the Caption

- The first sentence states what the figure or table shows. For a results figure, it states the observation the evidence supports. Format it as the detected convention does.
- The rest says how to read it: encodings, conditions, the better direction, and what error bars mean when there are any.
- Terms, case and panel labels match the figure exactly. The caption does not restate the body, and the body never copies the caption.
- After a color change, every color word in the caption still names the same elements.

## When a Figure or Table Is Crowded

Apply this order and stop when it reads clearly:

1. remove text inside the figure that repeats the caption
2. replace text labels with visual elements where the meaning survives
3. shorten labels to the paper's shortest defined terms
4. split the figure into panels, or into two figures
5. move a secondary panel or table to the appendix, with a precise reference

For a table: shorten headers, regroup columns, split the table, move detail to the appendix. Tables print at the single `\small` size `paper-typesetting` sets in the preamble, so a table never carries its own font size. A table that still overflows is wrapped once in `\resizebox{\linewidth}{!}{...}`, and that is the only resize.

## Stop and Discuss

Act directly within the mode's limits. Stop and discuss before:

- building a new concept or redesign that the user has not approved
- adding or removing a panel, element, table row or column
- changing the palette, font or brief for all figures
- changing what a table or plot compares or how it aggregates
- delivering a version that does not read better than the previous one

Ask at most three questions, each with a recommended answer and the rendered images that show the question.

## Long Tasks

With three or more figures or tables, use parallel subagents, one per target. Before starting them, the main agent writes or loads the brief, and every subagent receives it. Each subagent writes only its own source, export and audit file. Each returns:

- the element ledger or number-source ledger of its target
- the scripted check results and the printed size of its smallest text
- for a polish, the `diff` result
- the paths of its full-size and thumbnail renders, and the previous version's render
- every mismatch with the paper's terms, the sources or the brief, and every unresolved defect

The main agent opens every render and every audit before accepting a figure. A subagent's report of success is not acceptance.

## Build and Inspect

Compile with the project's build entry. Render every page that holds a changed figure or table and look at it. Check the figure at its real inserted size, next to its caption and body text, because a figure that reads well alone can be too small or too dense on the page.

## Final Checklist

- Every word in every figure matches the paper's terms. No code identifier, flag or undefined abbreviation appears.
- Every figure follows the brief: one label font, one symbol font, one color per method or role, one stroke weight per role.
- A style polish shows no removed, added, reworded, reconnected or hidden element unless the user approved it.
- Every color word in a caption still matches the figure.
- Every figure PDF embeds its fonts and is vector where the content allows. Type 3 fonts are reported when the venue rejects them.
- Text below about 70% of the caption size is reported with its location.
- Each changed figure was compared with its previous version on the rendered page, and reads better.
- Every plotted value and table cell matches its source. No row or series name lacks a source.
- Tables of the same role share header row count, rule style and label font. No `\hline` remains.
- Every caption's first sentence states what the figure shows, in the detected format.

## Delivery

Discussion and explanations are in Chinese. Manuscript text is in English.

Deliver:

- the changed sources, exports and table or caption locations
- before and after renders of each changed figure on its page
- the scripted check results that remain open: small text, Type 3 fonts, drift from the brief
- for a polish, the `diff` result
- ledger rows with status mismatch or no source
- the compile result, and whether the changes were pushed. Push only when the user asks.
