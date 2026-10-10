---
name: paper-method
description: Drafts and revises the method section of an ML paper, including notation, equations, design rationale, algorithm boxes and theory statements, and keeps symbols, terms and mathematical meaning consistent across the manuscript. Use when the user asks to write or rewrite the method, problem formulation or theory, fix notation, remove numbers or citations from the method, explain an equation, check that a formula means what the text says, or make a fragmented method read as one computation. Not for the experimental setup or results (paper-experiments), figure design (paper-visuals) or sentence polish elsewhere (paper-language). 触发词：改方法、写方法部分、公式、符号统一、记号、方法不要数字、定理、问题定义、算法框、方法太碎。
license: CC-BY-NC-SA-4.0
---

# Paper Method

Use this skill to write the method as a computation a peer can trace and reimplement, with notation, equations and theory that agree with that computation.

## Goal

The deliverable is the revised method section in the manuscript files. It must:

- compile, with every equation label and cross-reference resolving
- keep every number, label and citation key that existed before, unless the user approved moving it
- let a reader name the inputs, the operations in order, the outputs and the quantity being optimized, from the method alone
- use one symbol per object and one term per meaning, matching the rest of the paper
- contain no hyperparameter values, no experimental results and no citations beyond the necessary classics

## Reader Standard

Write for a peer who wants to reimplement the method from the paper and its appendix. That reader asks, for every step: what goes in, what comes out, what is optimized, and why this step exists. A sentence that names a component without saying what it computes fails that reader.

Each design choice is introduced by the requirement it answers, then by the operation, then by the reason the operation meets the requirement. A design reason is stated as a reason. Whether the design produced the gain is a question for the experiments section.

## Read the Project First

1. Map the manuscript through `\input` and `\include`. Read the whole method, the problem formulation, the appendix sections it points to, and the experimental setup, which is where hyperparameter values belong.
2. Find the source of truth for what the method does. That may be code, an algorithm note, or the user's description. Prose never adds a step the source does not contain.
3. Fetch the remote copy before editing if the project has one.
4. Read the math macros (`\newcommand`, `\DeclareMathOperator`) and the notation already established, including any terminology file the project keeps. Recorded terminology is binding.
5. Detect the conventions from the manuscript, or from the exemplar if the user names one:
   - the display-equation environment (`equation`, `align`, or a project macro)
   - the equation reference form (`\eqref{}` or `Eq.~\ref{}`)
   - the run-in heading style (`\paragraph`, `\noindent\textbf`, or a project macro)
   - the theorem environments and where proofs go
   - the vector and matrix typeface

Follow detected conventions. A new manuscript with no conventions uses the template's own forms.

## Build the Ledgers

**Symbol ledger.** One row per symbol the method defines or uses.

| Column | Content |
| --- | --- |
| Symbol | as typeset, with its sub and superscripts |
| Object | what it denotes, in plain words |
| Type | scalar, vector, matrix, set, sequence, distribution, function, index, policy, score |
| Domain and indices | the range of each index and what it counts |
| Defined at | the first sentence that defines it |
| Used in | every later location, including figures, captions, appendix and algorithm boxes |

Act on the ledger. Two objects sharing one symbol get separate symbols. One object carrying two symbols gets one. A symbol used before its definition gets its definition moved up or a short gloss at first use.

**Term ledger.** One row per technical term: the term, its meaning, where it is first defined, and every variant spelling or synonym found. Variants are reduced to the recorded term. A new term is introduced only when the object has no name yet.

[references/notation-and-meaning.md](references/notation-and-meaning.md) holds a filled example of both ledgers and the checks for reading a formula. Read it before changing any equation.

## Write the Method

**Overview first.** Open with one paragraph that states the input, the output and the chain of operations between them, in the order the computation runs. Symbols enter only when needed later.

**Order by dependency.** Sections and run-ins follow the order in which one step's output feeds the next. Development history and module names do not decide the order.

**Few headings, full blocks.** A subsection exists only for an independent technical question. Run-in headings are one to four plain words, in the detected style. Each run-in block holds a full paragraph. Adjacent blocks of one sentence or one equation are merged. One user put it as "方法不要那么多paragraph，尽可能避免这么碎".

**Requirement, operation, reason.** For each design element, state the difficulty it removes, the operation, and why the operation removes the difficulty. Say why a quantity is bounded, normalized or held fixed.

**Training and inference apart.** State which parameters training updates, what inference reads, and whether any step uses information the setting does not allow, such as labels or future inputs.

**Algorithm, equation and prose agree.** Pseudocode gives the execution order, equations give the relations, and prose gives the purpose. All three name the same objects with the same symbols.

## Numbers, Symbols and Citations

These rules hold for every method section and are never relaxed by an exemplar.

- **No hyperparameter values.** Name every tunable quantity by a letter, such as $k$ candidates, temperature $\tau$ or threshold $\delta$, and give the value in the experimental setup or appendix. Constants that are part of the mathematics stay, such as the 1 in $1-p$, the exponent of a squared norm, or $\tfrac{1}{2}$ in a definition. One user, finding a value inside a method equation, wrote "竟然在正文公式出现数字？？".
- **Letters as symbols.** A function or quantity is a letter, with descriptive subscripts set upright when needed ($r_{\mathrm{len}}$). Words such as $\mathrm{Score}(x)$ or $\mathit{reward}$ do not serve as symbols. Standard operators stay ($\exp$, $\log$, $\max$, $\arg\max$, $\mathbb{E}$).
- **No experiment talk.** The method names no benchmark, model size or result, and does not point to tables. "We find that this works better" belongs to the experiments.
- **Few citations.** Cite only a classic the method directly builds on, such as the base algorithm being modified. The method does not separate "our addition" from "existing parts" with citations.
- **Numbers that already exist stay verbatim.** When the user asks to remove numbers from the method, move each value to the setup or appendix with its letter, and keep its literal form.

## Equations

Introduce each display with its purpose: what it defines or computes. After the display, a "where" clause defines only the symbols that are new. Follow a key equation with one to three sentences on what it does, for example how its terms trade off, what happens at the extremes, or which step consumes the result.

- An equation is part of a sentence and carries its punctuation.
- Stacked displays without prose between them are split by a sentence that says how each feeds the next.
- A label is added only when the text refers to the equation.
- New displays use the detected environment. Existing legal environments and macros stay.
- Long expressions break at a relation or a top-level operator, never inside a bracket pair.
- A global font-size reduction of equations is a typesetting decision, outside this skill.

**Meaning changes are flagged, never slipped in.** Changing a sum to a mean, adding an epsilon, reversing a KL divergence, swapping an inverse for a pseudoinverse or dropping an assumption can change the method. Make such a change only when the definitions, dimensions or source code determine it uniquely, and report it as a mathematical change with its reason. When two readings are plausible, keep the original and report both.

## Theory

State theory in three layers: the general result, the extra conditions for the useful special case, and what the result implies for the implemented method. Assumptions come before the result. The body keeps the statement and the proof idea. A long proof goes to the appendix with a precise reference.

Align the target quantity, assumptions and probability source before comparing two bounds. A smaller upper bound does not show a smaller measured error, and a stationarity guarantee does not show global optimality. An empirical method with no theoretical claim gets no theorem added for completeness.

## Layout Inside the Method

A wrapped figure (`wrapfigure`) narrows paragraph text but does not narrow display math. A display equation inside the wrap span runs under the figure. When an equation falls inside a wrap span:

1. move the figure earlier or later so the span ends before the equation
2. shorten the span by placing the figure next to a longer paragraph
3. turn the figure into a full-width float
4. as a last resort, make a short equation inline

Check the result on the rendered page.

When the method exceeds its space, apply this order and stop when it fits:

1. cut sentences that restate an earlier sentence
2. merge one-sentence blocks into their neighbors
3. inline short definitions that do not need display
4. move long derivations and full configurations to the appendix with a precise reference

Font shrinking, negative spacing at headings and figure resizing belong to paper-typesetting and paper-visuals.

## Stop and Discuss

Act directly on edits inside the requested span. Stop and discuss before:

- renaming a symbol or term across the manuscript
- a mathematical change that the source does not determine uniquely
- adding or removing a subsection, a theorem or a step of the method
- reordering the method's subsections

Ask at most three questions, each with a recommended answer and the affected text. If an instruction reverses an established rule, such as asking for numbers in the method, confirm it in one sentence first.

## Long Tasks

When the task rewrites the whole method or touches three or more subsections, read with parallel subagents, one per subsection or appendix part. Each returns:

- every symbol defined or used, with type and line
- every term, with variants
- every display equation, its label and what it defines
- every number literal and citation key in the span
- every reference to a table, figure or experiment

The main agent merges these into one symbol ledger and one term ledger, resolves conflicts, and only then edits. The rewritten method must read as one computation.

## Build and Inspect

Compile with the project's build entry. Check the log for undefined references and overfull boxes in the method. Then look at the rendered pages:

- no equation overlaps a wrapped figure or runs into the margin
- brackets, sub and superscripts render as intended
- equation numbers appear only where the text refers to them
- run-in headings render in the detected style

## Final Checklist

- Every symbol in the ledger has one object, one definition, and a definition before or at its first use.
- The method contains no hyperparameter value, no result, no benchmark name and no table reference.
- Every function and quantity is a letter. No word serves as a symbol.
- Citations in the method are limited to necessary classics.
- Every display equation has a purpose sentence before it, and every key equation has an interpretation after it.
- Every mathematical change is reported with its reason. Every number that existed before is present, in the method or where it was moved.
- Prose, equations and the algorithm box name the same steps in the same order.
- The English rules hold: no em dash, no "It is worth noting", "Notably", "Specifically" or "In particular" as openers, "uses" instead of "leverages" or "utilizes".

## Delivery

Discussion and explanations are in Chinese. Manuscript text is in English.

Deliver:

- the changed locations (file and line) with a one-line summary each
- the new text, for short edits
- each mathematical change: original expression, new expression, reason
- each moved number: its letter, its old location, its new location
- a before and after for any paragraph where claim strength changed, a term changed, a sentence grew noticeably longer, or a collaborator's sentence was altered
- the compile result and a note on the rendered equations
- whether the changes were pushed. Push only when the user asks.

A full paragraph-by-paragraph bilingual comparison is produced only when the user asks for it ("对照", "改前改后", "逐段给我看").

Read [references/method-examples.md](references/method-examples.md) for worked before and after examples.
