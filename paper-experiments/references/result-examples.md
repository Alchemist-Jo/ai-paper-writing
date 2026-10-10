# Result Examples

All examples are synthetic teaching material. Their facts and numbers belong to no real paper.

## 1. From restated numbers to analysis

Assume Table 2 reports four benchmarks, and the method is best on all four at the same training budget, with the largest margin on the multi-step benchmark.

**Before.**
As shown in Table 2, our method achieves 71.3 on A, 64.2 on B, 58.9 on C and 80.1 on D, compared with 69.2, 60.8, 57.2 and 79.2 for the baseline.

**After.**
Table 2 compares both methods at the same training budget. The method improves on every benchmark, and the margin is largest on C, the only benchmark that requires several dependent steps. This pattern matches the method's design, which assigns credit to intermediate steps instead of the final answer alone.

The values stay in the table. The prose names the comparison, the pattern and its interpretation. The last sentence relates the pattern to a design reason, without claiming a verified mechanism.

## 2. Positive framing that keeps the failure visible

Assume the method improves three of four benchmarks and is lower on D.

**Before.**
Our method generalizes across all benchmarks.

**After.**
The method improves on A, B and C, which together cover the reasoning tasks in the evaluation. On D, a retrieval-heavy benchmark, it is below the baseline. The cause has not been established.

The positive result opens the paragraph. The exception has its own sentence, and no explanation is invented for it.

## 3. Ablations grouped by module

**Before.**
Table 4 shows the results of w/o A, w/o B, w/o C, Uniform weighting and Fixed schedule. All variants perform worse than the full method.

**After.**

```latex
\noindent\textbf{Sampler.} Replacing the adaptive sampler with \textit{uniform sampling} lowers accuracy on every benchmark, and the drop is largest where the data are most heterogeneous. ...

\noindent\textbf{Scheduler.} With a \textit{fixed schedule}, training reaches the same final accuracy but needs more updates. ...
```

Each block covers one module. Variant names come from the result sources and are set in italics as the manuscript does. The run-in macro follows the detected convention, and `\noindent\textbf` is only one example of it.

## 4. A setup that does not grow

**Request.** Add the evaluation temperature to the setup.

**Before.**
We evaluate on four benchmarks with the same prompt for all models, and report accuracy averaged over benchmarks. Training runs on eight GPUs for two days.

**After.**
We evaluate on four benchmarks with the same prompt and sampling temperature 0.6 for all models, and report accuracy averaged over benchmarks.

The temperature joins an existing sentence, and its value appears here because the setup is where values belong. The hardware sentence describes how the work ran and changes no comparison, so it moves to the appendix. The setup ends shorter than it started.

## 5. Process text removed

**Before.**
Results marked with † use archived data from an earlier version. Finding 2 is pending and will be updated.

**After.** Both sentences are removed from the manuscript. The delivery notes tell the user which cells carry archived data and which finding is pending.

## 6. Transfer without benchmark targeting

**Before.**
Our environments are designed to improve performance on MATH and GSM8K.

**After.**
Training on the generated environments transfers to two held-out benchmarks, MATH and GSM8K.

## 7. Statistics stated with their meaning

Assume four training seeds, a mean of 81.2%, a standard deviation of 0.6 points across seeds, and no significance test.

**Before.**
The method obtains 81.2 ± 0.6 and is statistically superior.

**After.**
Across four training seeds, accuracy averages 81.2% with a standard deviation of 0.6 percentage points.
