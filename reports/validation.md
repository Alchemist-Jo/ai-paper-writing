# Validation record

Date: 2026-09-15. Scope: personal skill refactor and public distribution.

## Completed

- Three operative modes: Grill collaborative writing, Draft manuscript writing, Style reference imitation.
- Current Markdown references resolve. One discoverable SKILL.md remains.
- Claude manual-invocation and Codex allow_implicit_invocation metadata are preserved; both agent metadata files agree.
- Source cohort index contains 150 ICLR and 100 ICML papers; all corresponding Markdown/JSON readings and visual records are present.
- All 68 CSV tables retain their rows and fields. 825,721 numeric cells were compared directly with the supplied corpus and remain unchanged. Full statistical and visual reports are preserved byte for byte.
- Four query-tool checks passed: exact row/value lookup, visible truncation with total match count, unknown-field reporting, and example-paper title lookup.
- The yao-meta-skill trigger evaluator passed 18 handcrafted rule/concept cases covering explicit selection, the three modes and nearby exclusions. The case and concept files are in evals/.
- Public text was checked for inherited private project references, machine-specific user paths and credential-shaped strings. Source path references were normalized; private project applications were excluded. Original attribution and scientific names are preserved.
- The package was copied to both local agent installations and compared directly before retiring the old standalone skill directories.

## Limits

The trigger evaluator is a lexical/concept smoke check, not a model activation benchmark. The behavioral cases in evals/output-cases.md are fixtures for future runs; no independent agent execution or blind writing-quality evaluation was performed. This release does not claim measured style similarity, acceptance probability or verified improvement in paper quality.

The inherited corpus was not independently re-read in full. Archived source links may refer to original PDFs or third-party assets that are not bundled. Current workflow links and source availability were checked; all external links were not exhaustively revalidated.

## Reproduce the package check

```bash
python3 scripts/validate_package.py
```

The query examples in README use only the Python standard library. Original corpus-generation scripts are retained as source material; their full dependency environments were not installed or executed during this refactor.
