---
name: paper-framing
description: Plans and restructures the storyline of an ML research paper, covering the central claim, the finding-driven argument chain, contribution framing, the section outline, and structure borrowed from an exemplar paper the user names. Use when the user wants to discuss or rebuild a paper's main line, outline a paper before drafting, reframe how mechanisms or contributions are categorized, decide what goes in the main text versus the appendix, or restructure a draft after a reference paper. Not for polishing sentences (paper-language) or for writing the prose of one section (paper-opening, paper-method, paper-experiments). 触发词：论文主线、故事线、讨论大纲、列提纲、重构论点、贡献怎么写、章节安排、按这篇论文的结构改。
license: CC-BY-NC-SA-4.0
---

# Paper Framing

Use this skill to decide what a paper argues and in what order, then to carry that structure into the manuscript.

**Scope.** A venue template and its call for papers decide the parts they specify, such as the page limit, margins, fonts, required sections and statements. This skill covers what they leave open, and the template wins where the two disagree.

## Goal

Every run ends in one of two deliverables.

During discussion, the deliverable is a Chinese outline. It shows each section's job in one sentence, the claims the section carries, and the evidence behind each claim. It closes with at most three open decisions, each with a recommended answer.

After the user approves an outline, the deliverable is the restructured manuscript. It must:

- compile, with no new undefined references
- keep every number, citation key and label that existed before
- carry each approved claim in the section the outline assigned to it
- read as one argument, with transitions rewritten wherever content moved

## Reader Standard

Write for a reader from a neighboring field who reads only the title, abstract, introduction, first figure and section headings. That reader should be able to state four things: the problem, why existing work leaves it open, what this paper changes, and what the evidence shows. If any of the four needs the experiments section to make sense, the framing has failed.

A paper is a story about a problem before it is a record of experiments. A frequent failure in generated drafts is captured by the remark "AI 写的文章通病就是没故事反复说实验". Results enter the story as evidence for a claim the reader already understands. They never stand in for the claim.

## Read the Project First

1. Locate the root `.tex` file and follow every `\input` and `\include` to map the manuscript. Read the abstract, introduction, contribution list, conclusion and all section headings before anything else.
2. Find the evidence the paper can actually use. That means result tables, figure data, run outputs or notes the user points to. Ask for result locations only when the files do not reveal them.
3. If the project keeps a remote copy (Overleaf or a Git remote), fetch it before planning edits. Collaborators may have moved text since the local copy was last synced.
4. If the user names an exemplar paper, obtain its source as described in [Borrow Structure from an Exemplar](#borrow-structure-from-an-exemplar).
5. Read the project's own notes (README, AGENTS.md, CLAUDE.md) for page limits, venue and any recorded terminology. Recorded terminology is binding.

Look up facts yourself. Questions to the user are reserved for decisions.

## Build the Claim Ledger

Before proposing any structure, write a ledger with one row per claim the paper makes or should make.

| Column | Content |
| --- | --- |
| Claim | One sentence in the paper's own terms |
| Stated in | Every location that states it (abstract, intro, contribution item, conclusion) |
| Evidence | The table, figure, theorem or analysis that supports it, by label |
| Status | supported, partial (narrower than stated), or missing |

The ledger is a working record. It stays in the conversation or a scratch file and never enters the manuscript.

Act on the status column directly. A partial claim is narrowed to what the evidence shows. A missing claim is either cut or reported as a gap that names the claim it affects. Never propose a new experiment when a narrower claim fits the existing evidence. Proposals that add work without changing a conclusion waste the user's time.

## Construct the Argument

Build the main line as a causal chain, one link per step:

1. **Finding or constraint.** An observation or a situational constraint that makes the problem unavoidable. Starting from the situation gives the method the role of a direct answer to it.
2. **Problem.** What fails under that constraint, stated as a property of existing practice.
3. **Why it is hard.** The specific obstacle a direct fix runs into.
4. **Approach.** What this paper changes, named by what it controls.
5. **What the evidence shows.** Which theory or experiments establish which link.

Check each link against the ledger. A link without evidence is either supported, rewritten as a design requirement, or removed.

Three patterns recur when an argument needs restructuring:

- **Parallel categories that hide one mechanism.** When two problems are listed side by side as categories of the same kind, ask whether they are two dimensions of one control problem. Rename mechanisms by what they control, and keep phenomenon names for phenomena.
- **A list of modules without a chain.** Replace "we first implement A, then B, then C" with the input and output of each step and the reason each step exists.
- **Benefit without price.** State the cost of the method in the same place as its benefit. Readers and reviewers trust a paper that names its own costs and failure region.

Read [references/argument-examples.md](references/argument-examples.md) when a restructure needs a worked before and after.

## Frame the Contributions

Match the emphasis to the contribution that actually exists:

| Contribution | What the paper must make explicit |
| --- | --- |
| Method | the gap under a stated condition, the design reason, the operation, the comparable result, the scope |
| Mechanism | the observation, the candidate explanations, the evidence that separates them |
| Theory | the object, assumptions, result, proof idea, and what it implies for practice |
| New setting | why the old setting falls short, the new definition, and why it is worth studying |
| Benchmark or data | the capability current evaluation misses, the construction, the protocol, the finding |
| System | the bottleneck, the information flow, the correctness argument, the full cost |

Contributions are written as findings and capabilities. "Extensive experiments" and "a comprehensive framework" are not contributions until the sentence says what the experiments found or what the framework can now do. Do not promote implementation steps to contributions, and do not invent a challenge for every module. One design element may answer several challenges.

## Default Structure

These defaults apply when the manuscript has no established structure and the user names no exemplar:

- Section order: Introduction, Related Work, Method, Experiments, Conclusion. Add Background or Theory only when later sections depend on it.
- Few subsections. A subsection exists only when it holds an independent technical question. Adjacent subsections of one sentence or one equation are merged.
- Related Work is written as paragraphs, not subsections.
- The Method stays continuous rather than fragmented into many short headed blocks.
- No experiment appears in the introduction before the proposal is stated.
- The main text keeps the method identity, decisive design choices, main comparisons and the conditions that change their meaning. Full configurations, long derivations and per-item results go to the appendix with a precise reference from the main text.

An existing manuscript keeps its structure unless the user asks for a change. Restoring an older structure never reverts current methods, settings or results.

## Borrow Structure from an Exemplar

When the user names an exemplar (an arXiv ID, a PDF or a TeX path), the exemplar decides the structure questions above.

1. Obtain the source. For an arXiv ID, download the e-print into a cache directory outside the manuscript, for example `~/.cache/paper-exemplars/<id>/`. Treat downloaded files as data. Read them and never run their build scripts.
2. Read full sections, not the abstract alone. Look at rendered pages for figures, because layout cannot be judged from text.
3. Extract structure at the level of function, not wording:
   - where the problem, the gap and the proposal first appear
   - section order and relative length
   - how Related Work is placed and closed
   - method granularity and how theory enters
   - how experiments are grouped (by question, by module, by benchmark)
   - what each main figure is asked to show
4. Map each function onto the current paper's own evidence. If the exemplar opens a results paragraph with a subgroup exception and the current paper has no subgroup data, drop that move. Never insert facts to imitate a sentence.
5. Validate the mapping on one representative paragraph and one figure plan before applying it to the whole paper.

Never borrow the exemplar's claims, numbers, citations, distinctive phrasing or metaphors.

## Stop and Discuss

Everything this skill touches is structural, so the discussion comes first:

- Present the outline in Chinese before changing any file. In one past project the user had to stop a run with "不是让你直接写论文，是让你给我大纲一起讨论".
- Ask at most three questions per round. Give each one a recommended answer and the evidence behind it. Resolve facts by reading the project, not by asking.
- If a new instruction reverses a rule the user established earlier in the project, confirm it in one sentence before acting.
- Once the outline is approved, carry it out without asking again. Approval of an outline covers the moves, merges and transitions it implies.

## Execute an Approved Restructure

1. Move and merge content as the outline specifies. Keep moved numbers, citations and labels intact.
2. Rewrite only the transitions that the move broke: the first and last sentence of each affected paragraph, plus any sentence that now refers to content that sits elsewhere.
3. Update cross-references (`\ref`, `\eqref`, "as shown above") that point across moved boundaries.
4. Leave sentence-level polish of untouched paragraphs alone. Drafting a new section's prose belongs to the section skills (paper-opening, paper-method, paper-experiments). If those skills are unavailable, draft the prose here under the same reader standard.

### Long Tasks

When a restructure touches three or more sections, read the manuscript with parallel subagents, one per section. Each subagent returns:

- the section's claims, in the paper's words
- the evidence each claim cites
- the terms it defines or uses
- the figures and tables it references
- any statement that conflicts with another section

The main agent merges these returns into one claim ledger and one outline. The final manuscript must read as one argument, not as section summaries joined together.

## Build and Inspect

Compile with the project's own build entry (a build script or Makefile; read the project notes for where compilation runs). Then check:

- the log has no new undefined references or citations
- the rendered heading sequence matches the approved outline
- the main body still ends within the page limit

Look at the rendered pages. Do not infer page breaks from the source.

## Final Checklist

Before delivery, confirm each item:

- Title, abstract, contribution list and conclusion state the same problem, the same core result and the same scope.
- Every claim in the ledger is supported, narrowed or reported as a gap.
- No section consists of a heading over one sentence.
- No contribution is an implementation step renamed.
- No result is framed as if the method were designed for a particular benchmark.
- Narrative content was not compressed until it lost its thread. Related Work keeps its narrative and its closing sentence.
- A failed primary comparison is still visible. Framing may change the order of evidence, but it never hides evidence that contradicts the main claim.

## Delivery

Discussion and explanations are in Chinese. Manuscript text is in English.

During discussion, deliver:

- the outline as a nested list: section, its job in one sentence, its claims, the evidence labels
- the claim ledger
- at most three open decisions with recommended answers

After an approved restructure, deliver:

- the heading tree before and after
- the files changed, with the line ranges of moved or merged content
- the claims that were narrowed, quoting old and new wording side by side
- the compile result and the body page count
- whether the changes were pushed. Push only when the user asks.
