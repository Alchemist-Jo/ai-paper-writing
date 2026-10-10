# Argument Examples

Every example below is synthetic. None of it is a finding of the current project.

## 1. Parallel categories become two control dimensions

**Before.** A storage paper lists two problems as "read-side imbalance" and "write-side imbalance" and proposes one module for each. Readers see two unrelated fixes.

**Diagnosis.** Once the access pattern is fixed, the system still controls two things: where each request lands and when requests overlap. The "read-side" fix spreads keys across shards. The "write-side" fix staggers bursts in time. These are one problem with two dimensions.

**After.** The chain becomes:

1. The access pattern fixes the demand.
2. The placement step balances load across shards, which is the spatial dimension.
3. Balanced placement does not control arrival overlap, so bursts still collide.
4. The scheduling step bounds concurrent arrivals per shard, which is the temporal dimension.
5. The system selects native, spatial-only, temporal-only or joint execution from the observed load.

Terminology follows the chain. "Spatial shaping" and "temporal shaping" name mechanisms. "Burst collision" stays as the name of the phenomenon.

The required figures follow from the chain as well. One figure shows that balanced placement still collides in time. Another maps the four execution modes onto the two dimensions.

## 2. A module list becomes a chain with reasons

**Before.** We first implement a retrieval module. We then add a scoring module. Finally, we implement selection.

**After.** The method retrieves a candidate set within the evaluation budget. A scoring function compares these candidates on the property the task rewards, and the selection rule returns the highest-scoring candidate. Retrieval is bounded by the budget because scoring cost grows with the number of candidates.

The revision states each step's input, output and reason. It does not claim each module as a separate contribution.

## 3. Benefit and price in one place

**Before.** Our method improves accuracy across all settings. (The extra inference cost appears in the appendix.)

**After.** The method improves accuracy in the four tested settings at the cost of one additional forward pass per query. The cost and the settings where the gain disappears are reported with the main results.

## 4. Narrowing a claim to its evidence

Assume the only evidence is a reduced error in two settings under one budget.

**Before.** Our method consistently solves the problem and supports a wide range of applications.

**After.** Under the same evaluation budget, the method reduces error in both tested settings.

The positive result stays. The unsupported generalization is removed rather than hedged.

## 5. Outline format for discussion

A discussion outline is delivered in Chinese and has this shape:

```
1 Introduction
  作用：让外行读者理解为什么访问模式固定后，存储仍会拥塞
  主张 C1：分片负载均衡后，请求仍会在时间上冲突。证据：Figure 2，Table 3
  主张 C2：两个维度的整形可以按负载选择。证据：Section 5.3
2 Related Work
  作用：说明已有方法只控制其中一个维度
3 Method
  3.1 空间整形。作用：在写入前完成分片均衡，并说明为什么只在这一侧做就够了
  3.2 时间整形。作用：限制每个分片的并发到达
4 Experiments
  作用：分别验证 C1 和 C2，并报告额外开销

待定决策
1. 引言先讲“均衡后仍冲突”这一发现，还是先讲系统约束？
   建议先讲发现，因为 Figure 2 可以直接支撑它。
```
