---
name: paper-language
description: Polishes the English of an existing ML paper with minimal edits that keep the author's voice, terms, numbers and claim strength, removes LLM-overused wording, process text and abrupt transitions, and translates Chinese drafts into paper English. Use when the user asks to polish, proofread, smooth transitions, remove AI tone, make minimal edits, shorten without losing meaning, fix grammar, translate a Chinese paragraph, or show a paragraph-by-paragraph before and after. Not for restructuring the argument (paper-framing) or rewriting a section's content (paper-opening, paper-method, paper-experiments). 触发词：润色、改语法、最小修改、去 AI 味、衔接、过渡突兀、中译英、精简、对照、改前改后、逐段给我看。
license: CC-BY-NC-SA-4.0
---

# Paper Language

Use this skill to make existing paper text correct, clear and continuous while it still reads as the author wrote it.

**Scope.** A venue template and its call for papers decide the parts they specify, such as the page limit, margins, fonts, required sections and statements. This skill covers what they leave open, and the template wins where the two disagree.

## Goal

The deliverable is the polished text in the manuscript files. It must:

- keep every number, symbol, label, citation key and technical term exactly as it was
- keep the claim strength of every sentence
- keep each paragraph no longer than it was, unless the user asked for expansion
- read in the author's voice, so that a coauthor sees their own text with errors removed
- contain no banned wording, process text or unsupported transition

## Reader Standard

Two readers judge the result. A reviewer should find the text precise and easy to follow. The author should recognize every paragraph as their own. The most frequent complaint about polishing is a change of voice. One author put it as "我不满意的就是修改版语言风格大变". An edit that improves a sentence but changes the voice is a failed edit.

## Read the Project First

1. Read the target span and one paragraph on each side of it. Transitions are judged against the neighbors.
2. Read the project's terminology record if one exists. Otherwise, collect the terms the span uses and check how the rest of the paper writes them.
3. Fetch the remote copy before editing if the project has one, so collaborators' latest text is the text being polished.
4. Identify text written by collaborators: comment macros, attributed edits, or sections the user names. Comments stay in place.
5. Profile the author's voice from untouched paragraphs: typical sentence length, preferred connectives, use of "we", tense in method and results, spelling variety (American or British), and hyphenation habits.

## Build the Edit Ledger

One row per sentence changed.

| Column | Content |
| --- | --- |
| Location | file and line |
| Original | the sentence before |
| Revised | the sentence after |
| Reason | grammar, banned wording, transition, contradiction, redundancy, process text, translation |
| Length | word count before and after |

The ledger enforces the length rule and feeds the delivery. A row without a reason is reverted.

## Edit in This Order

1. **Meaning.** Find sentences that contradict a neighbor, the paper's numbers or its terms. Fix only the contradiction.
2. **Logic and transitions.** Check that each paragraph's first sentence follows from the previous paragraph's last. A connective must name a relation that exists. "Therefore" needs a cause, and "However" needs a contrast. When inserted content reads as abrupt, integrate it into the surrounding sentences instead of adding a bridging sentence.
3. **Grammar.** Agreement, articles, countability, tense, prepositions, dangling modifiers, and the referent of "this", "it" and "which".
4. **Wording.** Remove banned and overused wording, using the list in [references/wording-rules.md](references/wording-rules.md). Read it before every polishing task.
5. **Redundancy.** Cut repeated background, repeated definitions, empty evaluation and sentence-final participle phrases that add nothing. Assumptions, units, denominators, comparison conditions, failures and costs are never cut.

## Minimal Edit Rules

- **Fewest words changed.** Correct sentences stay as they are. A grammatical error is fixed inside its sentence, without restructuring the sentence.
- **Sentences do not grow.** A revised sentence is no longer than the original unless a missing condition must be restored. A paragraph never grows. When a transition needs words, pay for them by cutting redundancy in the same paragraph. As one author put it: "总结最小更改，要求句子长度不能变长".
- **Terms never change.** A technical term is never replaced with a synonym, even a better one. Renaming is a decision for the user.
- **Collaborator text.** Near-synonyms and mild simplifications written by a collaborator stay. Fix only grammar and real contradictions.
- **Numbers, symbols, labels and citations stay verbatim.**
- **Claim strength stays.** A language edit never strengthens or weakens a claim. When a claim looks stronger than its evidence, report it and leave it.

## Patterns to Remove

- **Process and status text.** Sentences about pending work, dates, archived or historical results, internal names, or how the work was done. Sentences addressed to the author, such as "This paragraph now explains". These are deleted and listed in the delivery.
- **Stacked hedges.** "may potentially", "could possibly". One qualifier at the evidence's strength remains. Scope is stated once, where it applies.
- **"Not X but Y."** Rewrite as a direct statement unless the contrast is itself the claim.
- **Rows of short sentences.** Join sentences that share a subject or a causal link. Short sentences stay for turning points.
- **Repeated openings.** Vary sentences that all start with "We" or "The" by restructuring, never by inserting an empty opener.
- **Term-dense sentences.** A sentence that introduces several new terms at once is split so each term arrives with its meaning.
- **Lists in prose.** Bulleted or enumerated prose outside the contribution list is rewritten as a paragraph, with the user's approval when it changes the layout.
- **Rhetorical questions and slogans.** Replaced with the statement they imply.

## Stance at Evidence Strength

Write a supported claim plainly. Remove hedges that the evidence does not call for, and replace vague verbs with the accurate verb: "show" for a proof or a controlled comparison, "observe" for a measurement, "suggest" for indirect evidence. This sharpens the wording without changing the claim, which is the only stance edit this skill makes.

## Translate Chinese Drafts

Identify the claim of each Chinese sentence, then write it with English syntax. Do not keep the Chinese topic-first order, long pre-nominal modifiers or chains of nominalizations. Keep every condition and the original degree of certainty. Use the paper's existing English terms. When a term has no established English form in the paper, propose one and list it for the user.

## Parallel-Text Mode

When the user asks for "对照", "改前改后", "逐段给我看" or "完整对照", produce a paragraph-by-paragraph comparison. Each entry holds:

- the location
- the original English
- the revised English
- a Chinese rendering of the revised text
- one line per change, with its reason

For a large task, write the comparison to a Markdown file outside the manuscript tree, which is never compiled or pushed, and give the user its path. For a few paragraphs, show it in the reply.

## Stop and Discuss

Act directly on edits inside the requested span. Stop and discuss before:

- editing outside the requested span
- renaming a term
- merging, splitting, reordering or deleting a paragraph
- deleting a sentence that carries content
- changing a claim's strength

Ask at most three questions, each with the original text and a recommended answer. When the user asks to discuss first ("先和我讨论", "你先说一下思路"), describe the planned edits and wait.

## Long Tasks

When the task covers three or more sections or the whole paper, use parallel subagents, one per section. Give each subagent the term record, the voice profile and the wording rules. Each subagent edits only its assigned files, or returns proposed edits when sections share a file, and returns its edit-ledger rows and any terms or claims it flagged.

The main agent then checks across sections: the same term written the same way, the same fix applied to the same error, and transitions at section boundaries. The polished paper must read as one author's voice.

## Build and Inspect

Compile with the project's build entry when an edit could move the layout: a paragraph changed length near a float or a page boundary, or the main body is near its page limit. Then check on the rendered pages that the body still ends within its limit and that no float moved away from its reference. Pure word substitutions that keep line counts need no build.

## Final Checklist

- Every number, symbol, label, citation key and term matches the original.
- No paragraph is longer than before. Every row in the edit ledger has a reason.
- Collaborator text changed only for grammar or contradiction, and every comment is still in place.
- No banned opener, banned word, em dash or `$>$`/`$<$` in prose remains in the edited span.
- No process or status text remains in the edited span.
- Every connective names a real relation, and every paragraph opening follows from the previous paragraph.

## Delivery

Discussion and explanations are in Chinese. Manuscript text is in English.

Deliver:

- the changed locations (file and line) with a one-line summary each
- the new text, for short edits
- a before and after for any paragraph where claim strength would have changed, a term changed, a sentence grew noticeably longer, or a collaborator's sentence was altered
- deleted process text and flagged claims, listed separately
- the compile result, when a build ran
- whether the changes were pushed. Push only when the user asks.

The full bilingual comparison is produced only in parallel-text mode.

Read [references/edit-examples.md](references/edit-examples.md) for worked minimal edits.
