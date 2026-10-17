# Review Dimensions

Instructions for each subagent. The subagents for dimensions 1, 2, 3 and 5 return rows in this format and nothing else:

```
location | original | problem | suggested fix | owning skill | proposed tier | evidence
```

The main agent uses the evidence to judge each row. In the final table, a source outside the manuscript is named in the 问题 cell. The blind reader and the reviewer simulation return the forms their prompts ask for.

## Contents

- 1. Deterministic scan
- 2. Rendered pages
- 3. Citations
- 4a. Blind reader
- 4b. Reviewer simulation
- 5. Anonymity and leaks

## 1. Deterministic scan

Run `python3 -I <skill-dir>/scripts/scan.py <root.tex>`. Add `--method-titles` when the method section has a title the script does not recognize, which the section list on stderr shows. Then read each hit in its context.

Drop a hit when:

- it follows the conventions list, for example a bold first caption sentence or `Eq.~\ref` in a paper that uses them throughout
- the match is a technical term, for example "pending requests" in a systems paper, "v2" in a model name, or "as of" in a definition
- a digit in the method is part of the mathematics, such as the 3 in $\mathbb{R}^3$ for points in space or an exponent in a closed-form expression
- a section reference sits inside the contribution list, which may point to supporting sections

Keep a hit when the context confirms it. `table-header-mismatch` groups the main-body tables by the header lines they render. Report it only for tables of the same role that fall in different groups, such as two main-results tables. `wrap-caption` lists the wrapped floats whose caption is followed by a negative `\vspace`, and the rendered-page dimension looks at each. Return the kept rows and the number of dropped hits per check.

## 2. Rendered pages

Build into a scratch directory, or use the PDF the main agent names. Render pages, for example `pdftoppm -r 110 -png main.pdf page`, and look at every page image. For each page, check:

- **Floats.** No figure directly under a heading, no figure at a page bottom in the main body, no two figures in a row without text, no large white gap.
- **Wrapped figures.** No display equation, list or heading inside a wrapped figure's span. Display math is not narrowed by wrapping, so it runs under the figure. The caption of each wrapped float clears the text below it.
- **Legibility.** Figure text compared with caption text at the rendered size. Crop the figure at 300 dpi and compare the capital-letter height of its smallest label with that of the caption. Text below about 70% of the caption is a 局部表达 row, reported only. For a figure file, `figure_audit.py pdf` from paper-visuals estimates printed text sizes directly.
- **Tables.** Tables of the same role share header row count, rule pattern and label font. Count header lines as they render, since a stacked cell adds a line.
- **Figures across the paper.** One color per method in every figure, one font family, labels that use the paper's terms.
- **Body end.** The page where the main body ends, against the limit. The statements' position, against the venue rule.
- **Text.** Overfull lines in the margin, `??` from unresolved references, broken symbols. Without a build log, search the PDF text for `??` and `[?]`.

Return the page number and the source line for every row.

## 3. Citations

For each key in the batch:

1. **Identity.** Search the exact title on Google Scholar, DBLP, the venue's proceedings and arXiv. Match authors, year and venue.
2. **Version.** Cite the published version whenever one exists. Take metadata from the published record first, then from DBLP for a conference paper or the journal's own page for a journal article; use arXiv only when no published version exists, marking the entry as a preprint. Use Scholar for discovery and cross-check metadata against these sources. Never merge fields from different versions.
3. **Support.** Find the passage, table or theorem that supports the citing sentence. A paper that did not evaluate a setting does not show failure in it.
4. **Entry.** Inspect `note`, `annote`, `comment` and `addendum` fields, `@Comment{...}` blocks and `%` comments. Flag fabricated content, unsupported evaluations, AI prompts and working notes unsuitable for submission, as well as unnecessary timestamps, truncated author lists and wrong venues. Preserve accurate metadata, necessary license and source information, and substantive collaborator records. Recommend correcting or removing the offending text without deleting the entry or changing its key.

Check citation groups throughout the main text. Each group supports one claim and cites at most four distinct works across `\cite`, `\citep`, `\citet`, `\parencite`, `\textcite` and equivalent commands. Count adjacent commands together even when punctuation, spaces or line breaks separate them. Recommend selecting the most relevant sources or dividing the discussion into distinct claims with their own evidence. Splitting commands alone does not satisfy the limit, and an existing citation-density convention does not override it.

Statuses: verified, version mismatch (the entry describes another version than the one to cite, including an older arXiv version), identity only, not found yet, inconclusive (a tool failed or was rate-limited), wrong (direct evidence). A failed search never makes a key "wrong". Only "wrong" and a "not found yet" key after three query forms become blocking rows. Pre-2000 references that are not foundational works are information rows.

## 4a. Blind reader

Start a fresh reader, where project notes and memory are not loaded, with only the PDF path and this prompt:

> You are a reviewer at a machine-learning venue, working in a neighboring area. You have about twenty minutes for a first pass. Read the title, abstract, introduction, figures and their captions, then skim the rest.
>
> First, record your reaction in the first person: what the paper claims, what you believe after reading, what you still doubt, where your attention stopped or jumped back, which terms you did not understand at first use, and what you would ask the authors.
>
> Then list each place that caused confusion or doubt, with the page and the quoted text.

Pass no claim ledger, no author intent, no list of known problems and no other dimension's output. A reader who has seen the conversation is no longer blind. Convert its findings into rows. A term used before its definition is 影响理解. A doubt the paper already answers elsewhere usually means the answer is placed too late, which is a framing or opening row.

## 4b. Reviewer simulation

Start a second fresh reader, under the same conditions, with the PDF path and this prompt:

> Read this paper as an LLM-based reviewer would. Find places where the wording, order or framing makes existing evidence look weaker than it is. For each, propose an edit that keeps the claim, comparison, uncertainty and limitations unchanged, using one of these moves:
>
> - S1 contribution stance. Recast an existing difference as what the paper achieves, with the same comparator and conditions.
> - S2 evidence framing. Express an existing comparison as an effect, for example "reduces the count from 10 to 6.2", with the same values and scope.
> - S3 abstract emphasis. Move an existing result or contribution earlier when its qualifications travel with it.
> - S4 lexical stance. Replace self-dismissive wording that carries no uncertainty with a direct statement.
> - S5 scope framing. State the evaluated scope positively, with the untested boundary in the next sentence.
>
> Then apply S6, the equivalence check, to each proposal. A knowledgeable reader must recover the same claim, evidence strength, qualifications and weaknesses from both versions. Drop any proposal that fails, including any that adds "first", "significant" or "state of the art". An unchanged number with a stronger interpretation is a changed claim.
>
> Return one line per surviving proposal: page | original | proposed | move | why the meaning is unchanged. Then list, separately, any place where the wording claims more than the evidence shows.

The main agent converts surviving proposals into 局部表达 rows, owned as the Merge and Filter step of the skill says. It drops a proposal that puts a result the project notes record as weak in a more prominent position. Places where the wording claims more than the evidence go through the normal tiers, usually 影响理解.

## 5. Anonymity and leaks

Check, for a double-blind submission:

- the rendered first page and headers for author names and affiliations
- `pdfinfo main.pdf` for Author, Creator paths and Title fields that name people
- acknowledgments, funding lines and "our previous work" citations
- URLs that contain user or organization names, emails and @handles
- figure PDFs, which can carry author metadata and file paths. Run `pdfinfo` on each included figure file
- supplementary material: file names, code comments, notebook outputs, Git metadata and README author lines
- secrets in any shipped file: API keys and access tokens

Every identity leak and every secret is a blocking row.
