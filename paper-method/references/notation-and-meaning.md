# Notation and Mathematical Meaning

## Contents

- Filled ledgers
- Reading a formula
- Operations that look alike
- Theory in three layers
- Terms that are not interchangeable
- Deciding whether an edit is safe

## Filled ledgers

A synthetic method that samples candidate answers, scores them, and updates a policy.

| Symbol | Object | Type | Domain and indices | Defined at | Used in |
| --- | --- | --- | --- | --- | --- |
| $x$ | input question | element of $\mathcal{X}$ | none | Problem setup, first sentence | Eq. (1), Algorithm 1 |
| $y_i$ | $i$-th sampled answer | sequence | $i = 1,\dots,k$ | Sampling run-in | Eq. (1), Eq. (2) |
| $k$ | answers sampled per input | positive integer | none | Sampling run-in | Algorithm 1, setup (value) |
| $s(x, y)$ | answer score | function to $\mathbb{R}$ | none | Scoring run-in | Eq. (2), Figure 2 |
| $\pi_\theta$ | current policy | distribution over answers | parameters $\theta$ | Problem setup | Eq. (1) to Eq. (3) |
| $\pi_{\mathrm{old}}$ | sampling policy of the current round | distribution | none | Update run-in | Eq. (3) |

| Term | Meaning | First defined | Variants found | Action |
| --- | --- | --- | --- | --- |
| answer score | output of $s$ | Scoring run-in | "reward", "rating" | use "answer score" everywhere |
| round | one sample-score-update cycle | Overview | "iteration", "step" | "step" stays for optimizer steps only |

## Reading a formula

Check these together with the sentence before and after the display.

- **Binding.** Every index is bound or defined. Summation bounds match the text. A returned variable exists.
- **Types and dimensions.** Each operation applies to its operands. Matrix products have the intended shape. A set and an ordered sequence are different objects.
- **Distributions.** Each expectation names its distribution or sampling process. Conditional and marginal are kept apart. Independence comes from the protocol or an assumption, never from the use of different symbols.
- **Optimization.** The direction (minimize or maximize), the variable being differentiated, and what is held fixed are stated. Two expressions with the same forward value can have different gradients, for example under stop-gradient.
- **Approximation.** The target objective, its sample estimate, a surrogate, a truncated version and the implemented update are named separately. An unbiased numerator does not make a normalized ratio unbiased. A finite search is not an exact maximizer.
- **Scope.** Quantifiers, failure probabilities, which variable goes to a limit, and constants hidden in big-O notation are visible.
- **Boundary behavior.** Empty sets, zero denominators and edge time steps behave sensibly within the domain the paper states.

## Operations that look alike

| Pair | What the definitions must settle |
| --- | --- |
| transpose and conjugate transpose | whether the objects are real or complex |
| inverse and pseudoinverse | whether the matrix is invertible, and which solution is meant |
| norm and squared norm | which quantity the claim controls |
| norm of an expectation and expectation of a norm | when the randomness is integrated out |
| $D_{\mathrm{KL}}(p \Vert q)$ and $D_{\mathrm{KL}}(q \Vert p)$ | which distribution supplies the expectation |
| sum and mean | whether the normalization changes the objective, the step size or a regularizer |
| probability and density | which object a change of variables acts on |

A form that differs from the common one is checked against its definition before any change. A complex bilinear form may use a plain transpose on purpose.

## Theory in three layers

| General result | Extra step that needs support before claiming it |
| --- | --- |
| guarantee for an exact continuous process | the learned, discretized, finite-budget version actually run |
| bound on a stationarity measure | a condition that turns stationarity into optimality |
| smaller upper bound | evidence that the actual error is smaller |
| robustness under tested perturbations | a certificate before claiming worst-case robustness |
| inclusion of solution sets | conditions before claiming equivalence |

## Terms that are not interchangeable

- objective, loss, score and reward, unless the method defines them as equal
- generalization gap, excess risk and test loss
- parameter count, trainable fraction, FLOPs, latency and total compute
- percentage-point change and relative change. A drop from 100 ms to 75 ms is a 25% latency reduction and about a 1.33 times speedup.
- observed correlation, mechanism hypothesis and intervention evidence
- training-free, per-input optimization and inference with a pretrained helper

## Deciding whether an edit is safe

| Situation | Action |
| --- | --- |
| a typo fixed uniquely by definitions, dimensions or code | correct it, check every use, report it as a mathematical change |
| two readings both fit the manuscript | keep the original, report both readings and what would decide |
| a value or constant looks wrong | keep the literal value, report the suspected correction and its basis |
| a statement claims more than its proof | narrow the statement to what is proved, inside the edit span |
| a needed proof or derivation does not exist | finish the other edits and report the gap |

After any change to a key symbol, trace it through definition, objective, theorem, proof, algorithm box, figure, caption and appendix. When a part was not checked, say so. A clean compile shows that the typesetting works and says nothing about correctness.
