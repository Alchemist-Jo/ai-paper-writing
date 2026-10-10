# Figure Design

## Contents

- Figure types
- Composition
- Layout rules
- Typography
- Color
- Results plots
- Signs that a figure looks generated
- Examples

## Figure types

Each type answers one question. Decide the type before choosing a layout.

| Type | Question it answers | Common forms |
| --- | --- | --- |
| Figure 1 | what problem the paper addresses and why current methods fall short | one running example with the failure and the paper's outcome; existing approach beside the paper's approach; a compact result teaser when the gain is the headline |
| overview | what the method computes, in what order, with what feedback | modules as regions with flow between them; a loop between interacting components; layers for phases such as offline and online |
| detail | how one mechanism works | one module enlarged, often wrapped beside the text that describes it |
| results | what the evidence shows for one comparison | lines, points, bars, scatter or heatmap chosen from the question |
| qualitative | what outputs look like | the same inputs across methods, with comparable crops and settings |

A Figure 1 uses the same running example that the introduction and method use. A result teaser fits only when the gain is large and the comparison is fair. When the paper's value is qualitative, the example form works better.

## Composition

- **Modules as regions.** Each module the method names becomes a region on a pale frame or separated by space, with a small tag that uses the method's term. Elements inside a region belong to that module.
- **Flow with meaning.** An arrow carries an object. Label it with the object's term or symbol when the regions do not already make the object clear. The main flow reads in one dominant direction.
- **Loops and phases.** Feedback returns as a curved arrow, often dashed and in the color of the module that drives it. Phases are separated by position or a frame, never by a legend alone.
- **Key formulas only.** Keep the one or two formulas that define the method's core quantities, typeset as in the paper. Every other step is shown through icons, a small example or the shape of the data.
- **Concrete over abstract.** A small instance, such as one input with its candidate outputs, says more than a box labeled "Candidate Generation". Thumbnails stacked with a slight offset read as many items.
- **Hierarchy.** Primary components are larger and carry a pale tint of their module color. Secondary components are smaller or grey. Frames are paler than cards, and cards are paler than their content.
- **Density.** Size each card to its content. A large empty card, or a figure whose regions hold one word each, reads as low information. Fill freed space by enlarging thumbnails and glyphs, never by adding words.

A single row of equal boxes says only "these steps happen in order". When the method really is a chain, show what changes between steps: the data, its size, or who acts on it.

## Layout rules

These rules hold for every diagram.

1. Align card edges to a shared grid. Repeated elements have equal size and equal spacing.
2. Use one gutter between unrelated elements and a smaller one inside a group. Text keeps a margin inside its card.
3. Treat every box, label, icon and arrow label as a bounding box. Only declared composites may overlap: an icon inside its card, a stack of thumbnails, a connector ending on its target's border.
4. Draw connectors behind boxes and text. No connector crosses text or another connector where a route around exists. Two connectors do not run in parallel for a long stretch.
5. Arrow labels sit beside their arrow, not on another element.
6. When content does not fit, shorten or remove secondary text, then widen the canvas or move a whole region. Never shrink one label below its role's size, close a gutter, or cover another element.

## Typography

- One label font for all figures, and one symbol font that matches the paper's math. Symbols keep the paper's italics, sub- and superscripts.
- Sizes are set per role (labels, card titles, group tags, symbols) in printed points at the inserted width. Convert with: printed size equals source size times inserted width divided by source canvas width.
- Text at inserted size stays near the caption size. Text below about 70% of the caption size is reported to the user with its location.
- Sentence case. Bold only for card titles, group tags and panel letters.
- Wrapped figures need a width at which their smallest labels stay legible. A narrow wrap that forces tiny text belongs at full width instead.

## Color

- One hue per method or role, with the same meaning in every figure, including plots. The paper's own method keeps its accent even where it does not win.
- A standard colorblind-safe qualitative palette, such as Okabe-Ito or Paul Tol's bright scheme, is the default when the project has none. Keep the project's palette when it has one, and do not change it without the user.
- Tints are fixed mixes with white, one level for frames and one for cards, so every figure has the same lightness steps.
- A detail figure uses at most two accents plus grey. An overview uses one hue per module the method names. Entity colors inside thumbnails or examples are separate from both.
- Pair every color distinction with a second cue: shape, line style, a pattern or a direct label. Check the grayscale render.
- No shadows, gradients, glow, 3D effects or decorative icons.

## Results plots

- Choose the encoding from the question: lines for trends over a variable, points or bars for discrete comparisons, scatter for cost against quality, heatmaps for matrices, distribution plots for spread.
- Axis titles name the quantity and unit. Mark the better direction when it is not obvious.
- Bars that encode absolute quantities start at zero. Lines and points may use a local range, labeled clearly. A log scale is labeled.
- Panels that compare one quantity share the axis range, or the caption states that they differ.
- Error bars and bands appear only when computed, and the caption names the statistic and the number of runs.
- Failed, missing and zero values are drawn differently and never joined into a trend.
- Methods keep their color, marker, line style and legend order across all plots.
- Each plot is produced by a script from data, at its inserted width, with the shared plotting style.

## Signs that a figure looks generated

Reviewers notice these within seconds. One user summarized them as "配色和size都不太对，一股ai味道".

- saturated or arbitrary colors, gradients, shadows, glow and 3D effects
- several font families, or text sizes that vary without a role
- tool-default styling, such as default blue boxes and default arrowheads
- decorative icons that carry no meaning, and icons from mixed styles
- long sentences inside boxes
- internal names, code identifiers or terms the paper never uses
- uneven spacing, misaligned edges, arrows that cross text
- a row of identical boxes for a method that has modules and loops
- a palette or stroke weight that changes from one figure to the next

## Examples

These examples are synthetic.

**A row of boxes regrouped.** Before: six equal boxes in one row, "Input", "Encoder", "Retriever", "Scorer", "Selector", "Output". After: two framed regions, retrieval and generation, tagged with the method's terms. A record store sits beside the retrieval region, and the selected records flow into generation. A dashed return arrow in the retrieval color shows the generation state refining the next query. The scoring formula sits inside the retrieval region.

**Code text removed.** Before: a box labeled `cand_gen(x, n=8)  # t/f`. After: three small candidate thumbnails under the paper's term "candidate answers". The number of candidates is a letter in the method and a value in the setup, so it does not appear.

**Style-only polish.** Before: mixed fonts, default bright colors, three corner radii, arrows of four weights. After: the same cells, labels and arrows in the brief's fonts, colors, radius and stroke weights, aligned to a grid. The `diff` check reports content equal, and the side-by-side render shows the new version reads faster.

**Density raised.** Before: a wrapped detail figure with five large cards holding one short label each and small icons. After: cards sized to their labels, icons doubled in size into the freed space, and one small example added from content the figure already named. No new term appears.

**A plot sized for its slot.** Before: a plot drawn on a large default canvas and scaled to a column, so its tick labels print at about half the caption size. After: the script sets the figure width to the column width and the font sizes in points, so the printed sizes are the sizes in the script.
