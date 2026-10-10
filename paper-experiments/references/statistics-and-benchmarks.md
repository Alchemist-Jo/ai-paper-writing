# Statistics, Comparisons and Benchmark Papers

## Contents

- What a reported value measures
- Denominators, filters and failures
- Fair comparison
- Uncertainty
- Significance and practical size
- New calculations
- Benchmark and dataset papers

## What a reported value measures

Identify three units before writing about any aggregate: the unit that is scored (a question, an image, a trajectory), the unit that is averaged, and the unit that is repeated independently (a training seed, an annotator, a sampled answer). Their counts are different sample sizes and are never swapped.

A task-averaged score, $K^{-1}\sum_{k=1}^{K} s_k$, weights every task equally. A score pooled over all items weights each task by its size. Both answer valid questions. Report the one the protocol fixed, and state the weighting. Averaging different metrics needs a stated normalization and direction.

## Denominators, filters and failures

State which items enter the evaluation and which enter the metric. A score on a filtered subset is reported with the filter and its coverage.

Timeouts, invalid outputs, out-of-memory errors, backend failures, missing records and genuine zero scores are different events. Follow the protocol's rule for counting them and state the rule. A latency computed over successful requests is reported with the success count.

For pairwise preference, state how ties, abstentions and invalid judgments enter the denominator.

## Fair comparison

The claim decides which conditions must match: data split, available information, base model, prompt, post-processing, tuning opportunity, evaluator and compute budget. A shared model name does not show that the other conditions match.

When budget or access cannot be matched, show the difference and say what each comparison supports. Tokens, calls, FLOPs, wall-clock time and memory measure different resources. An oracle or a method with extra information is labeled as a reference point.

## Uncertainty

Before writing "mean ± value" or drawing a band, confirm what the value is: a standard deviation over a stated unit, a standard error, or a confidence interval with its level and method. Report the number of repetitions and their level.

One training run supports no claim about stability across training runs. Item-level variation inside one run supports only item-level statements. Never reconstruct an interval from a plot or a single mean.

Comparisons on the same items keep their pairing. Repeated responses, frames from one video or several judgments of one item are dependent, so they are never counted as independent cases.

## Significance and practical size

"Statistically significant" requires a named test and its assumptions. Without a test, report the difference and the known uncertainty. A small difference that passes a test is not automatically useful in practice, and a large observed difference does not establish a mechanism. A difference that fails a test does not establish equivalence.

Results chosen after many slices, models or settings are marked as exploratory. A grouping chosen after seeing the results is reported as such and never rewritten as a prior hypothesis.

## New calculations

Keep source values at their precision. A new difference, ratio or aggregate is reported with its inputs, formula, denominator and missing-value rule, separately from the source values.

Subtracting two percentages gives a percentage-point difference. Dividing that difference by the baseline gives a relative change, which is undefined for a zero baseline. A drop from 100 ms to 75 ms is a 25% latency reduction and about a 1.33 times speedup.

## Benchmark and dataset papers

When the contribution is a dataset, a task suite or an evaluation protocol, the experiments section carries the argument for it.

1. **Target.** The capability or condition current evaluation misses, compared against the closest existing resources.
2. **Construction.** Sources, candidate collection, filtering, annotation and splits, each with what it changes and why. Report filter counts that exist, and never back-fill counts that were not recorded.
3. **Protocol.** Inputs, allowed information and tools, output parsing, scoring and the handling of invalid outputs.
4. **Coverage.** How items distribute over the dimensions that matter, and which regions have no items.
5. **Findings.** What the evaluation reveals about current methods, with the evaluated matrix as actually run. Missing combinations are shown, never filled by multiplying counts.

Human annotation states the instructions, the unit, the aggregation and the quality checks actually run. Agreement scores appear only when they were measured. Contamination or overlap that was not checked is never described as excluded.
