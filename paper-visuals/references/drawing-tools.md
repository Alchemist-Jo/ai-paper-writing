# Drawing Tools

## Contents

- Choosing the tool
- Inserted width and printed size
- draw.io
- TikZ
- Plotting scripts
- SVG files
- Image models
- Rendering for inspection

## Choosing the tool

Use the tool the project already uses for each figure. For a new figure with no precedent:

| Figure | Tool | Reason |
| --- | --- | --- |
| overview, Figure 1, detail diagram | draw.io | editable, scriptable XML, vector PDF export with embedded fonts |
| schematic dominated by math or tensor shapes | TikZ | the paper's own fonts and exact geometry |
| results plot | a plotting script, such as matplotlib | reproducible from data, one shared style |
| photograph, screenshot, rendered sample | raster at sufficient resolution | the content is raster |

## Inserted width and printed size

Every size decision uses the printed size, which is the size on the compiled page.

```
printed size (pt) = source size × inserted width (pt) / source canvas width
```

The inserted width is the `\includegraphics` width times `\linewidth` at that point. Take `\textwidth` and `\columnwidth` from the template's documentation, or measure the body text block on a rendered page with `pdftotext -bbox`. TeX points are 1/72.27 inch.

The page holding a figure is in the `.aux` file: `\newlabel{fig:name}{{3}{4}...}` places Figure 3 on page 4.

## draw.io

**File structure.** A `.drawio` file is XML: `mxfile` holds one `diagram` per page, each with an `mxGraphModel` whose `root` lists `mxCell` elements. Cells `0` and `1` are the root and the default layer. A vertex has `vertex="1"`, a `value` (its label, HTML when the style has `html=1`), a `style` and an `mxGeometry` with `x`, `y`, `width`, `height`. Children of a container or group use coordinates relative to their parent. An edge has `edge="1"`, `source`, `target` and optional waypoints in `<Array as="points">`. A diagram saved compressed holds base64 of raw-deflated, URL-encoded XML. Save uncompressed so scripts and diffs can read it.

**Style keys used most.**

| Key | Meaning |
| --- | --- |
| `fontFamily`, `fontSize`, `fontColor` | label font, size in canvas units, color |
| `fontStyle` | bitmask: 1 bold, 2 italic, 4 underline |
| `fillColor`, `strokeColor`, `strokeWidth` | box fill, border, border weight |
| `rounded=1;absoluteArcSize=1;arcSize=N` | rounded corners with a fixed size in canvas units, the same at every box size |
| `dashed=1;dashPattern=6 4` | dashed stroke |
| `edgeStyle`, `curved=1`, `endArrow`, `endSize` | connector routing, curvature, arrowhead type and size |
| `whiteSpace=wrap`, `spacing`, `align`, `verticalAlign` | text box behavior |
| `shadow`, `gradientColor`, `glass`, `sketch` | decoration, normally off |

Inline HTML spans in a label can set a different font, size or style for a symbol, for example an italic symbol in the math font inside a text label.

**Build scripts.** For more than a few edits, write a Python script with `xml.etree.ElementTree` that reads the source and writes the new file:

1. Define the brief's values once as constants: fonts, sizes per role, palette, tints, stroke weights, corner size.
2. Define one style function per role: card, group frame, label, main-flow edge, feedback edge, symbol span.
3. Edit cells by id. A polish never adds, removes or renames a cell, so `figure_audit.py diff` can match every cell and compare its label, kind, visibility and, for an arrow, the cells it connects. An arrow drawn with free end points has no recorded source or target, so the script takes the smallest shape near each end. Positions are not compared, and arrow routes are checked on the render.
4. Write to the new version's path, then export and check.

A later style change becomes a change of one constant, applied to every figure by rerunning the scripts.

**Export.** The desktop application exports from the command line. On macOS the binary is `/Applications/draw.io.app/Contents/MacOS/draw.io`; on Linux it is `drawio`, run under `xvfb-run` on a headless machine.

```bash
draw.io -x -f pdf --crop -o fig.pdf fig.drawio      # vector PDF cropped to the content
draw.io -x -f png -s 2 -o fig.png fig.drawio        # preview at twice the canvas size
```

Fonts named in `fontFamily` must be installed on the exporting machine, and are then embedded. Check every export with `pdffonts`. The exporter embeds static TrueType fonts (`.ttf`) as TrueType, while CFF-based OpenType fonts (`.otf`) and variable fonts are embedded as Type 3. Many math fonts fall in the second group, and `figure_audit.py pdf` reports them. When the venue rejects Type 3 fonts, use a static TrueType font that has the needed glyphs, and confirm with `pdffonts` again. LaTeX labels enabled with `math=1` can come out blank in command-line exports, so check the render whenever they are used.

## TikZ

Compile each figure as its own document so it can be checked alone:

```latex
\documentclass[tikz,border=2pt]{standalone}
% load the paper's font and math packages here, so text matches the body
\begin{document}
\begin{tikzpicture}
  % draw at the inserted width, so the figure is included at scale 1
\end{tikzpicture}
\end{document}
```

Draw at the final width and include the PDF at its natural size, so text prints at the size written in the source. Define styles once with `\tikzset` for each role in the brief. Keep the source beside the PDF.

## Plotting scripts

One style module, imported by every plot script, sets the sizes from the inserted width and the caption size:

```python
import matplotlib as mpl

TEXT_WIDTH_PT = 397.0   # from the template; use the column width for a one-column plot
CAPTION_PT = 9.0        # caption font size of the template

def use_paper_style(width_fraction=1.0, aspect=0.4):
    width_in = TEXT_WIDTH_PT * width_fraction / 72.27
    mpl.rcParams.update({
        "figure.figsize": (width_in, width_in * aspect),
        "font.size": CAPTION_PT,
        "axes.labelsize": CAPTION_PT,
        "xtick.labelsize": CAPTION_PT - 1,
        "ytick.labelsize": CAPTION_PT - 1,
        "legend.fontsize": CAPTION_PT - 1,
        "pdf.fonttype": 42,          # TrueType; the default Type 3 is rejected by some venues
        "ps.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })
```

The placeholder values are replaced from the template. The module also holds the brief's palette, markers and line styles per method, and the font family. Include the plot with the same `width_fraction` of `\linewidth`, so it is scaled close to 1. Keep each script next to its data or record which result files it reads.

## SVG files

Edit an SVG as text when the change is small and structural, such as a color or a label. Export to PDF with Inkscape, `inkscape fig.svg --export-type=pdf --export-filename=fig.pdf`, then check fonts with `pdffonts`. Converting text to paths avoids font problems but removes searchable text, so use it only when embedding fails.

## Image models

An image model can produce a concept sketch for a discussion about layout. Its output typically shows the signs of a generated figure, invents labels and ignores the brief. The sketch is labeled as a sketch, it is never inserted in the paper, and the final figure is drawn in an editable tool from the approved concept.

## Rendering for inspection

```bash
pdftoppm -r 150 -f 4 -l 4 -png main.pdf page          # the page holding the figure
pdftoppm -r 40  -f 4 -l 4 -png main.pdf thumb         # thumbnail, for balance and color
pdftoppm -r 150 -f 4 -l 4 -gray -png main.pdf gray    # grayscale, for encodings without color
```

When the paper cannot be built, render the exported figure alone at its printed size. A PDF exported from draw.io is measured in points, so the pixel width for an inserted width W pt at a given dpi is W × dpi / 72:

```bash
pdftoppm -scale-to-x 298 -scale-to-y -1 -png fig.pdf alone               # W = 143 pt at 150 dpi
pdftoppm -scale-to-x 60 -scale-to-y -1 -png fig.pdf alone-thumb          # thumbnail
pdftoppm -scale-to-x 298 -scale-to-y -1 -gray -png fig.pdf alone-gray
```

Render the previous version the same way and view the two side by side, for example with `magick prev.png new.png +append compare.png` when ImageMagick is available, or by opening both images. Look at the renders directly. Text extraction and scripts do not replace looking.
