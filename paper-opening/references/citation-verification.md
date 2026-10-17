# Citation Verification

Verification answers three questions for each key: whether the work exists as cited, whether the entry describes the right version, and whether the work supports the sentence that cites it. A syntactically valid BibTeX entry answers none of them.

## Procedure for each key

1. **Identity.** Search Google Scholar, DBLP, the venue's proceedings page and arXiv using the title. Match title, authors, year and venue against the entry. Use Scholar for discovery and cross-check metadata against the sources specified below.
2. **Version.** Cite the published version whenever one exists. Take metadata from the published record first, then from DBLP for a conference paper or the journal's own page for a journal article. Use arXiv only when no published version exists, and mark the entry as a preprint. Never combine fields from different versions into an entry that never existed.
3. **Support.** Find the passage, equation, table or theorem that supports the citing sentence. A title or abstract supports only what it states. A paper that did not evaluate a setting does not show failure in that setting.
4. **Entry hygiene.** Correct author names and venue. Inspect `note`, `annote`, `comment` and `addendum` fields, `@Comment{...}` blocks and `%` comments. Remove fabricated content, unsupported evaluations, AI prompts and working notes unsuitable for submission. Remove scraping timestamps and access dates unless the template requires them. Keep accurate bibliographic metadata, necessary license and source information, and substantive collaborator records. Correct or remove the offending text without deleting the entry or changing its key.

## Statuses

| Status | Meaning | Action |
| --- | --- | --- |
| verified | identity, version and support confirmed | keep |
| version fixed | the work exists but the entry described another version | correct the entry and state what changed |
| identity only | the work exists, the cited content is not yet confirmed | keep the key, narrow the sentence to what is confirmed |
| not found yet | three query forms found nothing | report it, and do not delete it in bulk |
| inconclusive | a search tool failed or was rate-limited | report as inconclusive, never as not found |
| wrong | direct evidence shows the identity or content is wrong | fix the key or the sentence, and give the evidence |

A failed request does not show that a reference is fabricated, and neither does a year that differs between versions. A new reference enters the manuscript only with status verified.

## Signs of a fabricated reference

- A plausible title whose exact string returns nothing on Scholar, DBLP and arXiv.
- Real authors attached to a title they never wrote.
- A venue and year combination where the venue did not run that year, or the paper is absent from the proceedings.
- An arXiv ID whose abstract page shows a different paper.

## Old references

A reference before 2000 stays when it is a well-known foundation of the field. Other pre-2000 references are flagged for the user, not deleted.

## Fresh-context check

New references written in the same context that cites them are checked again by a subagent that receives only the keys and the citing sentences. Fabricated references are most often caught by an independent second pass.
