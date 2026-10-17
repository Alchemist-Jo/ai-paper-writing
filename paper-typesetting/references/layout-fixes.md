# Layout Fixes

## Contents

- Figure directly under a heading
- Figure at the bottom of a page
- White gap after a float
- Consecutive figures
- Wrapped figure problems
- Overfull lines
- Statements after the main body
- Locating the end of the main body
- Bibliography entry cleanup
- Labels and references
- Submission file checks

## Figure directly under a heading

Cause: the float's source sits right after `\section` or `\subsection`, or LaTeX moved it to the top of a page that starts with a heading.

Fix, in order:

1. Move the float's source one or two paragraphs after the heading.
2. Move it to the end of the previous section so it lands at the top of the earlier page.
3. Change the placement specifier for this float only.

## Figure at the bottom of a page

Cause: a `[b]` or `[h]` specifier, or a float defined late in a page.

Fix: move the float's source earlier, so LaTeX places it at the top of the page, or define it near the end of the previous page's text. Use `[t]` for this float if the template allows it.

## White gap after a float

Cause: a tall float that did not fit pushed text to the next page, or `\vspace` settings inside the float add too much space.

Fix:

1. Move the float so it starts a page, letting text fill the gap.
2. Reduce the space inside the float, which is the only place where spacing commands belong.
3. Make a short figure wider and lower, for example a first figure that spans the text width with a small height.

## Consecutive figures

Fix: merge the two figures into one figure with panels, place them side by side with `minipage` or subfigures and top alignment, or wrap the narrower one beside the paragraph that discusses it.

## Wrapped figure problems

| Problem | Fix |
| --- | --- |
| a display equation inside the wrap span runs under the figure | move the `wrapfigure` after the equation, beside a longer paragraph, or turn it into a full-width float |
| the paragraph is shorter than the figure, so the next heading or list wraps badly | place the figure before a longer paragraph, or reduce its height |
| the wrap span crosses a page break and the figure lands on the wrong page | move the figure earlier, so the span ends on the same page |
| the wrapped text column is too narrow to read | reduce the figure width while keeping its labels legible, or use a full-width float |
| figure labels become unreadable at the wrap width | use a full-width float, or redraw the figure through paper-visuals |

`wrapfig` needs the `wrapfigure` to start at a paragraph boundary. Check every wrapped figure on the rendered page after any edit above it, because text changes move the span.

## Overfull lines

- In prose, a long unbreakable token such as a URL or a long code name causes most overfull lines. Allow a break, or rephrase the sentence through paper-language.
- In tables, shorten headers or regroup columns through paper-visuals.
- In equations, break at a relation or a top-level operator through paper-method's rules.

## Statements after the main body

```latex
% end of the main body
\label{mainbodyend}
\clearpage  % only when the venue requires statements to start on a new page
\section*{Ethics Statement}
...
\section*{Reproducibility Statement}
...
\bibliography{refs}
\appendix
```

Follow the venue's order for statements, references and appendix. Some templates provide their own commands for these sections. Use them when they exist.

## Locating the end of the main body

Place a label at the end of the body, such as `\label{mainbodyend}` above, and read its page from the `.aux` file after a build, or render `\pageref{mainbodyend}` in a draft. Without a label, find the last body page on the rendered PDF.

## Bibliography entry cleanup

Read `note`, `annote`, `comment` and `addendum` fields, `@Comment{...}` blocks and `%` comments. Remove fabricated claims, unsupported judgments, AI instructions and working notes unsuitable for submission, together with timestamps and access dates the style does not require. Preserve accurate publication metadata, necessary source and license notices, and collaborator review comments unless their removal is authorized. Delete the offending comment or field, keeping the entry and its citation key. Follow [citation verification](../../paper-opening/references/citation-verification.md) to correct metadata against the published source.

**Before.**

```bibtex
@article{lee2023scaling,
  title  = {Scaling Laws for Reward Models},
  author = {Lee, J. and others},
  journal= {arXiv preprint},
  year   = {2023},
  note   = {Very important paper, accessed 2024-05-01},
  urldate= {2024-05-01}
}
```

**After.** Assume verification found the published ICML 2024 version and the full author list.

```bibtex
@inproceedings{lee2023scaling,
  title     = {Scaling Laws for Reward Models},
  author    = {Lee, Jane and Park, Min and Chen, Wei},
  booktitle = {International Conference on Machine Learning},
  year      = {2024}
}
```

The key stays the same, the informal note and access date are gone, and the venue and authors follow the published version. The example entry is synthetic.

## Labels and references

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figures/overview.pdf}
  \caption{...}
  \label{fig:overview}
\end{figure}
```

Write `Figure~\ref{fig:overview}` with a non-breaking space, or the project's reference macro. Use the equation reference form the manuscript already uses.

## Submission file checks

- `pdffonts main.pdf` lists every font as embedded.
- `pdfinfo main.pdf` shows no author name in an anonymous submission.
- The page count matches the venue rule for body, references and appendix.
