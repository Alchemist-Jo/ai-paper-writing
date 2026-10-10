# Method Examples

All examples are synthetic teaching material. They describe no real method.

## 1. Numbers leave the method

**Before.**

```latex
For each question we sample 8 answers at temperature 0.7 and keep those with score above 0.5.
```

**After.**

```latex
For each question $x$, the policy samples $k$ answers at temperature $\tau$, and the answers whose score exceeds a threshold $\delta$ are kept.
```

The values 8, 0.7 and 0.5 move to the experimental setup, each next to its letter, in their original literal form.

## 2. Words stop serving as symbols

**Before.**

```latex
\begin{equation}
\mathrm{Reward}(x, y) = \mathrm{Correct}(y) - \lambda \cdot \mathrm{Length}(y)
\end{equation}
```

**After.**

```latex
\begin{equation}
r(x, y) = c(y) - \lambda\, \ell(y),
\end{equation}
where $c(y) \in \{0, 1\}$ indicates a correct answer and $\ell(y)$ is the answer length in tokens.
```

Each function becomes a letter, and the "where" clause gives each letter its meaning once.

## 3. An equation inside its sentences

**Before.**

```latex
We normalize the scores.
\begin{equation}
w_j = \frac{\exp(s_j)}{\sum_{m \in \mathcal{C}} \exp(s_m)}
\end{equation}
The next step uses them.
```

**After.**

```latex
Candidates are drawn in proportion to their normalized scores,
\begin{equation}
w_j = \frac{\exp(s_j / \tau)}{\sum_{m \in \mathcal{C}} \exp(s_m / \tau)},
\label{eq:weight}
\end{equation}
where $\mathcal{C}$ is the current candidate set. A small $\tau$ concentrates the draw on the top-scoring candidate, while a large $\tau$ approaches uniform sampling over $\mathcal{C}$.
```

The temperature is added here only because the synthetic source defines one. Without that source, the expression stays as it was. The sentence after the display tells the reader how the one tunable quantity changes behavior. The label is kept because a later paragraph refers to this equation.

## 4. A fragmented method becomes continuous

**Before.** Five run-ins, each holding one sentence: "Inputs.", "Encoder.", "Retrieval.", "Decoder.", "Output.".

**After.** Two run-ins. "Retrieval." covers how the encoded input selects records, and why the number of records is bounded. "Generation." covers how the decoder conditions on the input and the selected records. The input and output move into the overview paragraph.

## 5. A component list becomes a computation

**Before.** Our method consists of an encoder, a retrieval module and a decoder, which collaborate to produce the output.

**After.** The encoder maps the input to a representation, which selects records from the store. The decoder then generates the output conditioned on the input and the selected records.

## 6. Exact versus approximate

**Before.** We exactly optimize the objective by evaluating the retrieved candidates.

**After.** The objective is defined over the full candidate set. The implementation evaluates the retrieved subset, so its quality depends on which candidates retrieval keeps.

## 7. Wrapped figure over a display equation

**Problem.** A `wrapfigure` placed before a paragraph spans eighteen lines. The paragraph ends after ten lines, and the next paragraph opens with a display equation, which runs under the figure on the rendered page.

**Fix.** Move the `wrapfigure` after the display equation, beside the longer interpretation paragraph that follows it. The figure's span then ends before the next display. Check the rendered page again, because the move also changes where the page breaks.
