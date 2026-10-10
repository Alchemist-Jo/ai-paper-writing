# Opening Examples

All examples are synthetic teaching material. Their facts and numbers belong to no real paper.

## 1. Abstract: from number pile to argument

**Before.**
We propose ASR, a method for adaptive sample reweighting. ASR achieves 71.3 on A, 64.2 on B, 58.9 on C and 80.1 on D, outperforming ERM by 2.1, 3.4, 1.7 and 0.9 points. ASR uses Eq. (3) with temperature 0.5 and is the largest study of reweighting to date.

**After.**
Training data for instruction tuning mixes examples that the model already handles with examples that it cannot yet learn from, so uniform sampling spends most updates on neither. Existing reweighting schemes fix the weights before training and cannot follow how the model's competence changes. We propose Adaptive Sample Reweighting (ASR), which re-estimates each example's learning value from the model's current loss and shifts sampling toward examples at the edge of its competence. Across four instruction-following benchmarks, ASR outperforms standard empirical risk minimization at the same training budget, with the largest gain on the benchmark with the most heterogeneous data. Because ASR only changes the sampling distribution, it adds no parameters and applies to any loss-based training pipeline.

The revision names the problem before the method and spells out the method and the baseline in full. Four results and four deltas become one evidence sentence, and the equation reference, the hyperparameter and the unverified superlative are gone.

## 2. Introduction: background before phenomenon

**Before.**
As Table 2 shows, accuracy drops by 11.4 points when the context exceeds 8k tokens (Section 5.2). We attribute this to positional drift (Theorem 1).

**After.**
Long-context models are trained on short sequences and deployed on long ones, so their behavior beyond the training length is extrapolation. When we evaluate several such models past their training length, accuracy falls well before the context limit is reached. As Figure 1 shows, (a) the drop begins at the same relative position across model sizes, while (b) it disappears when positions are re-indexed. Based on this observation, we trace the failure to how positional signals change with distance.

The revision introduces the setting first. Numbers, section references and the theorem reference move to the body, and the figure is described by what its panels show.

## 3. Introduction: the link from gap to proposal

**Before.**
To address these limitations, we propose a new framework.

**After.**
Based on this, we let the scheduler observe each job's measured workload instead of its declared size.

The revision states which observation the proposal builds on and what changes.

## 4. Related work: concede, then draw the boundary

**Before.**
Many methods study retrieval [1-9]. They suffer from poor flexibility. Our method is more advanced.

**After.**
Retrieval-augmented generation conditions a model on documents selected before decoding \citep{a,b,c}. Selection has moved from lexical matching to dense retrievers trained jointly with the generator \citep{d,e}, which raises recall on knowledge-intensive tasks. These methods fix the retrieved set for the whole output. On multi-hop questions, \citet{f} report that most errors occur after the first hop, when the needed document was not in the initial set. Our method updates the retrieved set after each reasoning step, so later hops can retrieve what earlier hops reveal.

Each citation group stays at four keys or fewer and supports one point. A cited work reports the shortfall, and the boundary sentence states a concrete operational difference without an evaluative adjective.

## 5. Untested is not failed

**Before.** Previous methods cannot transfer across models.

**After.** The reported evaluations consider a single model, which leaves cross-model transfer untested.
