# Figure Brief and Audit

## Contents

- Brief template
- Filling the brief
- Audit template
- Subagent return format

## Brief template

Save the brief beside the figure sources, for example as `figures/BRIEF.md`. Every value is filled from the project's existing figures, an exemplar the user named, or the user's decision. Angle-bracket fields are placeholders.

```markdown
# Figure brief

## Scope
Figures covered: <names and the sections that hold them>
Mode for this round: <new figure | redesign | style polish | results plot>
Content rule: <for a polish: every cell, label, symbol and panel stays, and every arrow connects the same cells>

## Typography
Label font: <family>, installed as <static TrueType or other>
Symbol font: <family matching the paper's math>, italic as in the paper
Case and weight: sentence case; bold only for card titles, group tags, panel letters
Printed sizes at inserted width (pt): labels <a>, card titles <b>, group tags <c>, symbols <d>
Caption size (pt): <e>

## Shapes and strokes
Units: canvas units at the placement class's canvas width
Corner sizes per role: group frames <r1>, cards <r2>, chips <r3>, thumbnails <r4>
Stroke weights per role: cards <w1>, group frames <w2> dashed, main flow <w3>, feedback <w4> dashed and curved
Pictograms and thumbnails: <border weight>, <line weights>, <entity colors>
Arrowheads: <type and size>

## Color
Roles and hues: <role → hex>, one line per method or module
Tints: group frames <p1>% of the hue, cards <p2>%, card borders <p3>%
Neutrals: text <hex>, secondary text <hex>, borders <hex>, arrows <hex>
Per figure: at most two accents plus grey
Plots: the same hues per method, with <markers and line styles>

## Geometry
Placement classes: full width <canvas units> at <inserted pt>; column <...>; wrapped <...>
Conversion: printed pt = units × inserted pt / canvas units
Height limits: <per figure, when the page budget fixes them>
Grid and gutters: <units between unrelated elements>, <units inside a group>

## Export
<export commands for PDF and preview>
Checks: figure_audit.py drawio, diff (polish), pdf, style; rendered page at full size, thumbnail and grayscale; side by side with the previous version
```

## Filling the brief

- Run `figure_audit.py style` over the existing sources. Values most figures share become the brief. Values used in one figure only are drift unless they carry a meaning, such as an entity color inside a thumbnail.
- Run `figure_audit.py drawio` with the inserted width on each figure to read its printed sizes. Set each role's size so its smallest member stays near the caption size, within the page budget.
- Take the hue assignment from the existing figures. When the user asks for a standard palette, map each existing role to the nearest hue of that palette and keep the assignment.
- Printed text below the threshold is the one exception to copying existing values. That role gets the threshold size, and the brief lists the figures that still differ.
- A brief value changes only with the user's agreement, and the change applies to every figure in the next round.

## Audit template

Each figure gets one audit file beside its source, for example `fig-overview.audit.md`.

```markdown
# <figure name> audit

Source: <path>, built by <script or tool>; previous version: <path>
Inserted width: <pt>; canvas width: <units>; scale <pt per unit>

## Changes
| Area | Before | After |
| --- | --- | --- |

## Element ledger
| Element | Paper term | Defined at | Wording matches |
| --- | --- | --- | --- |

## Content check (polish)
figure_audit.py diff: <content equal, or each removed, added or changed cell with the user's approval>

## Scripted checks
Smallest printed text: <pt> (<percent> of caption), at <cells>
Fonts: <embedded fonts>; Type 3: <none, or which>
Raster images: <none, or count and resolution at inserted size>
Code-like labels: <none, or which>
Drift from the brief: <none, or which values>

## Visual checks
Full size: <overlaps, clipping, alignment, arrow routes>
Thumbnail: <balance, density, color>
Grayscale: <whether every encoding survives>
Against the previous version: <what reads better, what was lost>

## Open issues
<each unresolved defect, or "none">
```

## Subagent return format

A subagent that builds or audits one figure returns, and nothing else:

```
figure | mode | source path | export path | audit path
smallest text (pt, % of caption) | Type 3 fonts | raster images | code-like labels
diff result (polish) | drift from the brief
renders: full size, thumbnail, grayscale, previous version
open issues, one per line
```

The main agent opens every render and every audit before accepting the figure.
