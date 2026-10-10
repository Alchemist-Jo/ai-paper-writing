# Tables and Captions

## Contents

- Cell meaning
- Structure and rules
- Consistency across tables
- Fitting a table
- Captions
- Examples

## Cell meaning

Before editing, establish for each cell its method, dataset, setting, metric, unit and aggregation. Values from other papers, values reproduced under a different budget, and values measured under a different protocol are separated by a group, a marker or a note.

Headers state units and the better direction (↑ or ↓) when the direction is not obvious. Abbreviations, denominators and failure symbols are explained in the caption or a table note.

After moving rows or columns, check that every value still sits under its method and condition. Existing LaTeX values keep their literal form. A new table uses the precision of its source, the same within each column.

## Structure and rules

- Text columns are left aligned. Numeric columns are right aligned or aligned at the decimal point.
- Rules come from booktabs: `\toprule`, `\midrule`, `\bottomrule`, and `\cmidrule(lr){i-j}` under a grouped header. No `\hline` and no vertical rules.
- Best and second-best markings apply within comparable groups only, with their meaning in the caption.
- Missing, failed, out-of-memory and not-run cells use distinct, explained symbols. None of them enters an average as zero.

## Consistency across tables

Tables that play the same role, such as two main-results tables over different benchmark families, share:

- the number of header rows
- the rule pattern, including where `\cmidrule` appears
- the label font for row and column names
- the method order and naming
- the header form, either symbols or words throughout
- the marking scheme for best values and deltas
- the font size

Check this on the rendered pages. A table with a one-row header next to a table with a three-level header reads as inconsistent even when each is correct alone.

## Fitting a table

1. Shorten headers to the paper's defined short terms, and explain abbreviations in the caption.
2. Regroup columns under a shared header.
3. Split the table where it holds two comparisons.
4. Move per-item detail to the appendix, keeping the results that change a conclusion in the main text.
5. As a last step, apply a local font size or `\resizebox`, then check legibility on the rendered page.

A table that fits but cannot be read still needs a layout change.

## Captions

A caption has two parts.

1. **What it shows.** One sentence. For a results figure or table, state the observation the evidence supports. For a method figure, state what the figure depicts. Format this sentence as the manuscript's convention does, which may be bold.
2. **How to read it.** Encodings, the condition, the metric direction, and what any error bar or band shows. Only what the reader needs to read this figure.

Panel labels in the caption match the figure, in the same case and order. Figure captions sit below figures and table captions above tables unless the template does otherwise.

Remove promotional words ("revolutionary", "remarkable"), "significant" without a test, and sentences that repeat the section text.

## Examples

These examples are synthetic.

**Table, before.**

```latex
\begin{tabular}{|c|c|c|}
\hline
Method & Result & Time \\
\hline
A & 0.84 & 12.5 \\
B & 0.82 & 11.0 \\
\hline
\end{tabular}
```

**Table, after.** Assume the sources confirm that the result is accuracy and the time is latency in milliseconds.

```latex
\begin{tabular}{lrr}
\toprule
Method & Accuracy $\uparrow$ & Latency (ms) $\downarrow$ \\
\midrule
A & 0.84 & 12.5 \\
B & 0.82 & 11.0 \\
\bottomrule
\end{tabular}
```

The values are identical. Without that confirmation, the header keeps "Result" and "Time" and the missing definitions are reported.

**Two tables unified.** Table 1 has a three-level header (benchmark family, benchmark, metric). Table 2 stacks two header lines inside one cell with `\shortstack`. Both list the same methods over different benchmarks. After the edit, both use two header rows, a family row with `\cmidrule` and a benchmark row, with the metric stated once in the caption.

**Caption, before.** Our revolutionary method is significantly better. (A) Main result.

**Caption, after.** Accuracy rises with the sampling budget for all methods, and the gap to the baseline widens beyond the smallest budget. (a) Points show independent runs, and lines connect the mean at each budget.
