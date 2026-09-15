# Provenance and scope

This skill was reorganized from the author's local `iclr-paper-writing`, `cvpr-paper-writing` and selected `technical-report-style` materials using the `yao-meta-skill` authoring workflow. The three-mode design adds Grill collaborative writing, Draft manuscript writing and Style reference imitation. The single-question/recommended-answer pattern was adapted from the author's local grilling instructions.

## Source groups

### ICLR / ICML corpus

`sources/anatomy/` preserves the locally supplied Elite ML Paper Anatomy 2026 dataset and analysis package, including its MIT license credited to ZenAlexa. The source reports describe 250 papers: 150 ICLR and 100 ICML, selected from Outstanding, Oral and Spotlight categories. The source material records https://github.com/ZenAlexa/elite-ml-paper-anatomy-2026 as its upstream; this release could not confirm that URL as publicly accessible. The bundled materials provide the working evidence source.

- [Statistical report](sources/anatomy/reports/statistical_analysis_250.md)
- [Visual analysis](sources/anatomy/reports/visual_design_analysis_250.md)
- [CSV tables](sources/anatomy/reports/tables/)
- [Paper index](sources/anatomy/reports/tables/reading_index.csv)
- [Visual index](sources/anatomy/reports/visual_audit_index.md)

The release does not claim to have independently re-read or revalidated every paper. Source-level inconsistencies and weighting distinctions are described in [statistics-to-decisions](references/statistics-to-decisions.md). A source reading is not a replacement for inspecting the actual paper when imitating language or figures.

### CVPR cases

`sources/cvpr-paper-writing/references/` retains public-paper case facts, experimental numbers and primary-source links from the supplied local analyses. Private project applications and project-specific constraints were removed. The preserved quantitative material covers RandAR, VGGT, D4RT, Motion Prompting, Go-with-the-Flow, Navigation World Models, VISPROG, Visual Program Distillation and Molmo/PixMo. ViperGPT is labeled ICCV; VideoCoCo is retained as an adjacent preprint, not a CVPR oral sample.

This is a small purposive case collection. It supports experiment organization and scope comparisons, not CVPR population frequencies or acceptance predictions. Consult each linked paper version before citing its numbers in a new manuscript.

### Writing workflows

`sources/iclr-paper-writing/references/` retains the historical blueprint, playbook, full statistics, visual handbook and closure prompts. Manuscript-specific execution instructions were consolidated into current references, rather than distributed as private project history. Fixed counts and old prompt restrictions are historical examples, not operative requirements.

`sources/technical-report-style/` retains terminology, section organization and fact-preserving language guidance with its original license. Blog-only rules were excluded. The current workflow specifies the academic use of these rules.

## Public-distribution edits

Machine-specific paths were converted to corpus-relative provenance where possible, otherwise marked as omitted. The underlying numeric fields were preserved. Original local source backups remain outside the public repository. Old skill entry points and platform metadata were excluded from the source archive so only the new skill is discoverable.

Public documentation uses user-neutral language. The new operative instructions are in `SKILL.md` and `references/`; archived scripts and source prompts do not authorize actions. Some inherited paths refer to original PDFs or third-party source assets that are not bundled. Use the recorded public paper URLs or a user-supplied copy for actual-paper inspection.

## Validation boundary

[Validation](reports/validation.md) separates package checks, metadata checks, source preservation, rule-based trigger examples and unexecuted behavioral evaluations. No independent writing-quality or acceptance benchmark is claimed.
