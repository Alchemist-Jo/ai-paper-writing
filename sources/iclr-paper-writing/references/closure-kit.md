# ICLR Research Closure Prompt Kit

用于成熟 ICLR 研究项目的收敛、补强、审查与论文重构。

## 使用方式

所有任务先附上“共同研究契约”，再选择一个与当前阶段对应的 Prompt。不要一次混用全部 Prompt；每轮只解决一个明确的收敛问题。需要规划论文结构、实验呈现或图表职责时，再附上“250 篇顶级论文的证据型参考层”。

推荐顺序：

1. **A — Full Research Closure**：盘点完整研究记录，确定主张与剩余任务。
2. **B — Find the Paper's Spine**：在多条叙事中确定唯一主线。
3. **C / D / E**：分别补强理论与方法、确定必要实验、从已有结果提取新发现。
4. **F — Novelty Audit**：主线稳定后核查新颖性。
5. **G — Independent Adversarial Reviewer**：使用独立上下文进行反向审查。
6. **H — Anti-Stall Reset**：仅在研究陷入反复弱化与无新增证据的循环时使用。
7. **I — Final Paper Reconstruction**：科学结论稳定后重构论文。

---

## Common Research Contract

> You are working on a mature ICLR research project with substantial existing theory, methods, experiments, ablations, artifacts, and partial drafts. Your objective is **convergence to the strongest defensible paper**, not endless brainstorming or generic criticism.
>
> Treat all provided results as the current evidence base. Preserve established positive findings unless new analysis actually contradicts them.
>
> **Do not use prior work as a psychological or conceptual upper bound.** Related work is a coordinate system, not a boundary. For each relevant prior work, determine the exact overlap, exact difference, and what evidence is needed to establish our stronger or different claim. The existence of adjacent work is not itself an argument for weakening the paper.
>
> **Do not repeat uncertainty without new evidence.** Every concern must name a concrete failure mode and terminate in one of four actions:
>
> `derive / test / revise / dismiss`.
>
> Do not generate endless “possible limitations.” Once an issue has been checked and resolved, close it unless new evidence reopens it.
>
> Maintain ambitious hypotheses when they remain compatible with the evidence. Distinguish rigor from timidity.
>
> Prefer a few decisive analyses or experiments over indiscriminate benchmark accumulation.
>
> Whenever several interpretations are possible, maintain independent hypotheses long enough to discriminate them empirically or theoretically rather than prematurely collapsing to the most conservative story.

---

## 250 篇顶级论文的证据型参考层

### 来源、统计口径与使用边界

本节整理自 [Elite ML Paper Anatomy 2026](https://github.com/ZenAlexa/elite-ml-paper-anatomy-2026)。仓库统一深读了 250 篇 ICLR/ICML 2026 Outstanding、Oral 与 Spotlight 论文：ICLR 150 篇，ICML 100 篇。分析先计算论文内相对量，再汇总会议内分布，并对 ICLR 与 ICML 等权。统计总体属于高等级论文样本，适合用作结构先验、缺项检查和版面起稿参考；具体论文仍应由科学主张、证据类型与会议当年规则决定。

主要来源：

- [250 篇统计报告](https://github.com/ZenAlexa/elite-ml-paper-anatomy-2026/blob/main/reports/statistical_analysis_250.md)
- [250 篇顶会论文写作手册](https://github.com/ZenAlexa/elite-ml-paper-anatomy-2026/blob/main/docs/writing-playbook.md)
- [ICLR 全文写作蓝图](https://github.com/ZenAlexa/elite-ml-paper-anatomy-2026/blob/main/docs/iclr-full-paper-blueprint.md)
- [250 篇图表解剖](https://github.com/ZenAlexa/elite-ml-paper-anatomy-2026/blob/main/reports/visual_design_analysis_250.md)
- [统计分析方案](https://github.com/ZenAlexa/elite-ml-paper-anatomy-2026/blob/main/docs/statistical-analysis-plan.md)

### 一、最重要的统计结论

#### 1. 正文资源集中于方法、结果和引言

| 模块 | 正文占比的会议等权均值 | 常见职责 |
| --- | ---: | --- |
| 方法 | 23.83% | 组件、对象、目标、变换与执行接口 |
| 结果 | 17.01% | 主张对应结果、异质性、成本与失败条件 |
| 引言 | 14.84% | 对象、缺口、核心洞见、贡献与结果预告 |
| 理论 | 10.15% | 假设、形式对象、保证、复杂度与可观测推论 |
| 实验设计 | 9.83% | 数据、任务、基线、指标、控制、分母与预算 |
| 相关工作 | 8.43% | 分类轴、最近邻差异、继承关系与方法缺口 |
| 消融 | 5.38% | 组件职责、机制、替代解释与敏感性 |
| 结论 | 2.87% | 按贡献顺序回收证据与影响 |

方法、结果和引言合计占正文 55.68%。起稿时可先保证这三部分形成连续证据链，再依据论文类型分配理论、系统、鲁棒性和分析空间。经验型论文的参考区间为：引言 12%–17%，相关工作 6%–11%，方法 18%–29%，理论 0%–16%，实验设计 7%–12%，结果 12%–22%，消融 0%–9%，结论 2%–3.5%，Limitations 0%–3%。这些区间分别来自样本分布，不能简单相加为固定模板。

#### 2. 摘要依靠功能顺序形成稳定结构

摘要平均 188 词、7.97 句，中位数为 181 词、8 句。功能覆盖率包括：对象与范围 100.0%，问题或缺口 94.8%，核心洞见 97.2%，方法 98.0%，定性结果 91.6%，定量结果 55.6%，影响主张 94.4%。98.0% 的摘要至少给出一种结果。

高频功能链：

`对象与范围 → 问题与缺口 → 核心洞见 → 方法 → 实验设置或理论 → 结果 → 影响`

完整句序共有大量变体。写作时固定功能覆盖与推进关系，句数和压缩方式根据内容确定。代表性数字应同时写明比较对象、决策量和适用范围。

#### 3. 完整的机制闭环仍然稀缺

250 篇论文共编码 1,972 条主张，其中 29.0% 完全闭合，61.1% 部分闭合，4.7% 保持开放，5.2% 在该论文范围内不可检验。91.6% 的论文至少有一条完全闭合的主张。覆盖全部十个节点的论文占 30.8%。

关键连接的论文覆盖率为：

| 连接 | 覆盖率 |
| --- | ---: |
| 对象 → 缺口 | 94.8% |
| 缺口 → 核心洞见 | 94.0% |
| 核心洞见 → 方法组件 | 70.8% |
| 组件 → 公式或理论对象 | 68.8% |
| 公式 → 可观测预测 | 42.8% |
| 预测 → 实验 | 44.4% |
| 实验 → 结果 | 98.4% |
| 结果 → 消融 | 84.4% |
| 消融 → 结论 | 81.6% |

最值得补强的连接通常位于“形式化对象 → 可观测预测 → 判别实验”。这一缺口直接对应 Prompt C、D 和 E 的任务范围。

#### 4. 实验报告以描述性聚合为主，不确定性信息相对少

80.4% 的论文使用 mean、average、median 或其他聚合量；72.4% 给出点估计且未呈现不确定性；42.8% 报告 seed、run 或重复试验；23.2% 报告 SD、SE 或方差；9.6% 使用区间、误差条或不确定性带；5.2% 使用假设检验或 p 值。

这些频率描述样本实践。具体项目应按主张所需的估计对象与变异来源确定统计方法。每项决定性结果至少明确：

- 聚合单位、分母和权重；
- seed、任务、数据集、模型或参与者的层级；
- `±`、阴影、区间和误差条的定义；
- 主决策量及其实质差值；
- 机制证据、实质差异与统计不确定性的关系；
- 使用 bootstrap、检验或回归时的重采样或配对单位。

#### 5. 实验设计需要形成可核查协议

单篇论文的 15 类实验设计字段中位覆盖 8 类，四分位区间为 6–9。覆盖率较高的字段包括指标与评价量 81.6%、数据集与来源 79.2%、基线与比较器 74.0%、模型或架构 70.8%、训练或推理预算 70.4%、控制或干预 63.6%。Seed 或重复运行覆盖 37.6%，显式 RQ、假设或预测覆盖 36.8%，失败、停止或接受标准覆盖 19.2%。

建议用一张实验协议表集中记录：研究问题、预测、失败判定、数据及分母、任务协议、模型版本、基线与资源匹配、指标方向与聚合、重复单位、预算、超参数选择、运行环境、控制变量、泄漏或污染控制，以及人类评测协议。

#### 6. 附录承担核查材料，正文保留改变判断的信息

附录/正文页数比中位数为 1.40，词数比中位数为 0.84。论文平均从正文调用附录 10.48 次。附录内容覆盖率较高的类别包括追加结果 81.6%、实现细节 74.4%、扩展方法 68.0%、数据细节 45.2%、鲁棒性 45.2%、证明 44.4%。92.0% 的证明对象位于附录。

正文应保留：中心主张、核心方法对象、关键公式或算法接口、定理的假设与结论、决定性实验配置与分母、主结果、一个机制消融，以及会改变适用判断的失败或成本。附录承载完整证明、配置、全结果矩阵、追加消融、鲁棒性、失败全集和复现材料。正文中的每个附录指针应说明调用对象及其用途。

#### 7. 图表承担不同的证据职责

仓库对 3,071 个 Figure 和 2,329 个 Table 进行了对象级审计。每篇论文的正文 Figure 中位数为 5，正文 Table 中位数为 3；附录 Figure 和 Table 的中位数分别为 5 和 4。会议等权均值向上取整得到的起稿上包络为正文 6 图/4 表、附录 8 图/7 表。图表数量应服从证据需求，并允许一个对象承担多项相容职责。

高覆盖率的视觉职责包括：主比较 97.7%、headline 证据 95.7%、鲁棒性 94.3%、方法接口 91.0%、机制诊断 88.3%、消融 86.7%、理论或机制 85.7%、实验设计 83.0%、质性证据 80.7%、效率或成本 74.3%。机制—消融证据链覆盖 73.5%，趋势图与精确数值表配对覆盖 64.2%。

建议分工：

- Figure 1：对象、缺口、核心接口与 headline 结果；
- 方法图：输入、组件、状态、数据流与输出；
- 主结果表：精确比较值、分母、成本和失败；
- 趋势图：规模、预算、时间、数据量或分布变化；
- 机制与消融图：诊断量、组件干预与替代解释；
- 边界图或表：鲁棒性、异质性、效率、失败条件与适用范围。

视觉统计的中心规格包括：正文 Figure 面板中位数 2，主要系列中位数 4，图中文字中位数 8 pt，数据线宽中位数 1 pt；正文 Table 的行列中位数为 6×6，小数精度中位数 2 位。最终图应在投稿版面的单栏或通栏尺寸下检查可读性。颜色、marker 与线型应提供冗余编码；caption 需定义对象、比较、编码、主要发现、分母和不确定性。

### 二、可直接执行的研究与写作规则

#### Claim map

为每项贡献建立一行：

`主张 → 方法对象 → 公式或保证 → 可观测预测 → 判别实验 → 结果 → 消融 → 结论 → 附录证据`

每行必须能够回答：主张是否可判定；哪项结果支持它；最强替代解释是什么；哪个实验区分两种解释；正文在哪里完成结论；附录在哪里提供核查材料。

#### 章节推进

- 引言：`context → problem → prior failure → missing insight → core idea → method preview → result preview → contribution list`。
- 相关工作：`分类轴 → 最近邻 → objective / assumption / scope / data access / cost / evaluation target 的明确差异 → 方法缺口`。
- 方法组件：`定义组件 → 对象与公式 → 机制解释 → 可观测预测 → 对应实验`。
- 理论：`假设 → 形式对象 → 定理或命题 → proof idea → 可观测预测 → 实验接口 → 结果解释`。
- 结果：按主张或预测组织，先写判断，再给数值和图表，随后说明机制、异质性、失败与代价。
- 消融：围绕组件职责、最近邻机制替换、理论关键条件、任务异质性和替代解释组织。
- 结论：按贡献顺序回收证据，不首次引入主张或数字。

#### 写作顺序

1. 建立 claim map。
2. 建立实验协议表。
3. 设计主结果、机制消融、失败面和成本证据对象。
4. 写方法对象、公式、算法与预测。
5. 写实验、结果与消融。
6. 组织证明、完整配置、全结果和复现附录。
7. 根据已经闭合的证据回写相关工作与引言。
8. 最后写摘要与结论。
9. 检查术语、符号、图表顺序、统计定义和附录调用。

---

## Prompt A — Full Research Closure / Research Director

**适用场景：** 项目总体接近完成，但最终论文的中心主张尚未确定。

> Act as the research director responsible for closing this ICLR project.
>
> Read all supplied theory, methods, experimental results, ablations, drafts, notes, figures, and related work as one research record.
>
> Reconstruct the **strongest coherent scientific thesis** supported by the evidence.
>
> Determine:
>
> 1. the central claim of the paper;
> 2. the genuinely new idea or mechanism;
> 3. the minimum set of contributions required to support that claim;
> 4. the exact evidence chain from hypothesis → method/theory → experiments → conclusion;
> 5. which existing results are central, supporting, redundant, or distracting;
> 6. the remaining gaps that could materially change acceptance probability.
>
> Do not produce an open-ended wishlist.
>
> Classify every proposed remaining task as:
>
> **DECISIVE** — could change the paper's main conclusion;
> **DIAGNOSTIC** — explains mechanism or failure mode;
> **COSMETIC** — adds volume but little information.
>
> Recommend only the highest-value decisive and diagnostic tasks.
>
> Then give a concrete closure plan and explicit stopping criteria: what must be finished before the paper should be frozen and written.

---

## Prompt B — Find the Paper's Spine

**适用场景：** 现有想法和结果过多，论文缺少单一、明确的主线。

> Ignore the current section structure and reconstruct the paper from first principles.
>
> Find the **single strongest intellectual spine** connecting the problem, insight, method, theory, and empirical evidence.
>
> Start from:
>
> **What previously unexplained or poorly solved phenomenon does this work make intelligible or controllable?**
>
> Then identify:
>
> - one primary thesis;
> - at most 2–4 supporting contributions;
> - the conceptual mechanism connecting them;
> - the strongest result that makes the thesis difficult to dismiss.
>
> Competing narratives should be compared explicitly. Do not merge incompatible stories merely to preserve all existing work.
>
> Prefer the narrative with the greatest combination of:
>
> **novelty × explanatory power × empirical support × technical depth × generality**.
>
> Demote results that do not strengthen this spine to appendices, secondary analysis, or removal.
>
> Output the final logical chain:
>
> `Problem → Missing insight → Core idea → Method/theory → Predictions → Evidence → Consequence`
>
> and explain exactly why this is stronger than the alternative framings.

---

## Prompt C — Push the Theory and Method One Level Further

**适用场景：** 实证结果已经较强，需要判断方法或理论能否形成更原创、更可检验的表述。

> Treat the current method and theory as a strong intermediate solution, not necessarily the endpoint.
>
> Search for a deeper formulation that explains **why the method works**, when it should work, and what new prediction follows from it.
>
> Explore several genuinely different possibilities before converging:
>
> - a stronger or more general objective;
> - an invariant, decomposition, or conserved quantity;
> - a mechanistic interpretation;
> - a tighter mathematical model;
> - a weaker assumption yielding the same result;
> - a stronger conclusion under existing assumptions;
> - an alternative derivation revealing a hidden connection;
> - a principled algorithmic modification implied by the theory.
>
> Do not manufacture novelty through unnecessary machinery.
>
> For every candidate extension, ask:
>
> **What new observable consequence would distinguish this theory from the current explanation?**
>
> Kill candidates that produce no new prediction, simplification, guarantee, or experimentally testable distinction.
>
> Return the strongest 1–3 extensions, their derivation skeletons, the exact assumptions, and the minimum experiment or proof needed to validate each.

---

## Prompt D — Decide What Experiments Are Actually Missing

**适用场景：** 在投入更多计算资源前，确定能够区分解释的最小实验集合。

> Audit the paper claim-by-claim against the existing experiments.
>
> Construct an internal matrix:
>
> `Claim × Evidence × Alternative explanation × Missing discriminator`.
>
> Search specifically for experiments that can distinguish competing explanations rather than merely increase the number of datasets or baselines.
>
> For every proposed new experiment specify:
>
> **Hypothesis**  
> **Controlled variable**  
> **Comparison**  
> **Metric**  
> **Predicted outcome under our explanation**  
> **Predicted outcome under the strongest alternative**  
> **What conclusion becomes possible after observing the result**
>
> Prioritize:
>
> 1. experiments that eliminate a serious alternative explanation;
> 2. experiments exposing the mechanism;
> 3. regime/scaling tests that establish generality;
> 4. ablations isolating genuinely causal components;
> 5. failure cases that sharpen the theory.
>
> Reject experiments that merely make a table larger.
>
> Produce the **smallest experiment set that maximally increases information and reviewer confidence**.

---

## Prompt E — Extract New Science From Existing Results

**适用场景：** 已有大量表格、曲线、日志、运行记录、checkpoint、消融或历史实验，需要从中提取尚未表述的科学发现。

> Treat the existing experimental record as a dataset to be scientifically mined, not merely summarized.
>
> Search for structure that the current paper has not yet articulated:
>
> - regime changes;
> - scaling behavior;
> - interactions between variables;
> - threshold effects;
> - surprising inversions;
> - systematic failure modes;
> - quantities that collapse across settings;
> - results inconsistent with the naive explanation;
> - hidden correlations suggesting a new mechanism.
>
> Compare experiments chronologically when useful: identify which historical modification caused each qualitative change and what that reveals about the system.
>
> Try multiple explanatory hypotheses and actively look for evidence that separates them.
>
> Do not force every observation into the current story.
>
> The goal is to discover **new claims from already-paid-for experiments**.
>
> Return the strongest newly extractable findings, the evidence supporting each, the figures/tables that should expose them, and any minimal follow-up needed to turn a pattern into a defensible scientific claim.

---

## Prompt F — Novelty Audit Without Defensive Collapse

**适用场景：** 已经形成候选主线，需要精确核查与相关工作的重叠及区别。

> Perform an aggressive novelty audit of the proposed paper, but do not automatically weaken it because neighboring work exists.
>
> For each relevant prior work, identify precisely:
>
> `their claim / their mechanism / their assumptions / their evidence / their scope`
>
> versus:
>
> `our claim / our mechanism / our assumptions / our evidence / our scope`.
>
> An objection of the form “something similar has been studied” is invalid unless you can identify the exact overlapping proposition, method, or empirical finding.
>
> Classify every novelty concern as:
>
> **FATAL OVERLAP** — the main contribution is already established;
> **POSITIONING ISSUE** — novelty remains but must be stated differently;
> **EVIDENCE GAP** — distinction exists but needs one discriminating result;
> **NON-ISSUE** — superficial similarity only.
>
> Search for opportunities where prior work actually makes our result **more interesting**, because we contradict, generalize, mechanistically explain, unify, or expose a limitation of an established view.
>
> End with the strongest accurate novelty statement, not the safest one.

---

## Prompt G — Independent Adversarial Reviewer

**适用场景：** 主线及证据链已形成，需要在独立上下文中尝试证伪中心主张。

**上下文要求：** Use a fresh context. Do **not** give this agent the generator's internal debate unless necessary.

> Act as an independent ICLR reviewer trying to falsify this paper's central claim.
>
> Do not brainstorm generic weaknesses.
>
> Attack only concrete propositions:
>
> - Is the claimed mechanism uniquely supported?
> - Is there a hidden confound?
> - Does an ablation fail to isolate the intended variable?
> - Does the theory actually imply the empirical claim?
> - Is a theorem assumption violated in the experiment?
> - Is a comparison unfair?
> - Is the novelty statement contradicted by a specific prior result?
> - Is a statistical or scaling conclusion unsupported?
>
> For every criticism provide the exact evidence or missing test that would decide it.
>
> Classify each issue:
>
> **fatal / major but repairable / minor / not valid**.
>
> Do not lower the score because the work is ambitious. Ambitious claims should receive stronger tests, not automatic skepticism.
>
> Conclude with the smallest set of repairs that would make the strongest version of the paper survive your own audit.

---

## Prompt H — Anti-Stall Reset

**适用场景：** 模型反复讨论“可能不新颖”“审稿人可能不喜欢”并持续弱化主张，且没有新增证据。

> Reset the research state.
>
> You are currently over-penalizing uncertainty and treating hypothetical reviewer objections as evidence. Stop doing that.
>
> Re-open the strongest live hypotheses.
>
> From now on:
>
> - Do not repeat a concern unless new evidence has appeared.
> - Do not weaken a claim merely because related work exists.
> - Do not replace a concrete research question with vague caution.
> - Do not call a route blocked unless you can name the exact unresolved technical or empirical obstacle.
> - Every objection must produce a derivation, experiment, counterexample, literature match, or actionable revision.
> - Resolved concerns are closed.
>
> Re-evaluate the project from the actual evidence.
>
> Identify the strongest plausible paper, the strongest unresolved alternative explanation, and the **few decisive actions** that separate them.
>
> Continue from there.

---

## Prompt I — Final Paper Reconstruction

**适用场景：** 科学主线已经稳定，研究阶段即将结束，需要围绕中心主张重构论文。

> The research phase is closing. Reconstruct the paper around the agreed scientific thesis rather than preserving the historical order in which the work was done.
>
> Design:
>
> **Title → Abstract → Introduction → Contributions → Method → Theory → Experiments → Analysis → Limitations/Discussion**
>
> so that each section advances the same central argument.
>
> The Introduction should establish:
>
> 1. the real problem;
> 2. why existing approaches leave a specific gap;
> 3. the new insight;
> 4. what becomes possible because of it;
> 5. the strongest evidence.
>
> Do not make related work the protagonist.
>
> Do not use prophylactic self-deprecation such as “we only,” “merely,” or “despite limitations” unless scientifically necessary.
>
> Calibrate claims to evidence, but state supported contributions at full strength.
>
> Identify which existing figures/tables belong in the main paper, which belong in the appendix, and what one figure should communicate the entire paper at a glance.
>
> Produce the final section-level argument and contribution wording before writing prose.
