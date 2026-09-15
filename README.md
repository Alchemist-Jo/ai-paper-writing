<p align="center"><img src="assets/banner.svg" alt="AI Paper Writing — Grill, Draft, Style" width="100%"></p>

<p align="center"><strong>A manually invoked skill for turning research evidence into clear AI papers.</strong><br>ICLR / ICML corpus statistics · CVPR case studies · paragraph and figure imitation</p>

<p align="center"><a href="#three-modes">Three modes</a> · <a href="#quick-start">Quick start</a> · <a href="#evidence-library">Evidence library</a> · <a href="README.zh-CN.md">中文说明</a></p>

## Three modes

| Mode | Start here when… | What you get |
| --- | --- | --- |
| **Grill** | You want to reason through the paper together | One focused question at a time, a recommended answer, and prose built from your decisions |
| **Draft** | You have evidence and want the manuscript written or improved | A draft, a reorganized paper, a revised section, an experiment plan or an evidence-based review |
| **Style** | You have a paper whose writing or figures you want to learn from | A source-to-target mapping and original prose or editable visuals using your own evidence |

The modes share the same scientific constraints. Reported values, comparison conditions and uncertainty stay intact. Unknown results remain visible placeholders. A clear drafting request proceeds directly; Grill waits for your answers on unresolved decisions.

## Quick start

Install into the skill directory for your agent. These commands create a new directory and do not replace an existing installation.

**Codex**

```bash
git clone https://github.com/Alchemist-Jo/ai-paper-writing.git ~/.codex/skills/ai-paper-writing
```

**Claude Code**

```bash
git clone https://github.com/Alchemist-Jo/ai-paper-writing.git ~/.claude/skills/ai-paper-writing
```

Select `ai-paper-writing` explicitly in your agent. The package preserves `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.

### Grill: develop the argument together

```text
Use $ai-paper-writing in Grill mode.
Here are my draft and experiment results. Help me decide the central claim,
then write the introduction with me. Ask one question at a time and give
your recommended answer with its evidence.
```

### Draft: finish the requested manuscript work

```text
Use $ai-paper-writing in Draft mode.
Restructure this paper around the supported findings. Use the ICLR corpus
statistics to guide section allocation and evidence placement. Edit the LaTeX
directly, preserve reported numbers, and mark missing results explicitly.
```

### Style: learn from a specific paper

```text
Use $ai-paper-writing in Style mode.
Use the attached paper as the reference for my method section and result figure.
Inspect its paragraph functions, sentence rhythm, panel order and caption.
Write with my method and data, and deliver editable figure source plus a render.
```

## How the evidence changes the writing

| Source observation | Practical use |
| --- | --- |
| Method, results and introduction account for a conference-equal 55.68% of the source corpus's normalized main text | Reserve enough room to connect the method to its evidence; adapt the allocation to the paper type |
| The source corpus contains 242 distinct complete abstract sequences | Preserve functional progression while allowing the sentence count to follow the content |
| Figure and table captions have different length distributions and information roles | Fit the setting, encoding and statistical meaning to each object instead of enforcing fixed word counts |
| CVPR cases separate task coverage, controlled interventions, visual outcomes and cost | Make each experiment answer a stated question and preserve the scope of each metric |

The source corpus contains **250 ICLR/ICML papers**. The CVPR material is a **small purposive case collection**. These have different evidentiary scopes. Frequencies describe the source sample; they are not submission rules, quality scores or acceptance predictions.

## Reference imitation, in practice

```text
Actual paper / rendered figure
        ↓
Section roles · paragraph moves · language · visual organization
        ↓
Source feature → your claim / method / data → target paragraph / panel
        ↓
Original prose or editable visuals
        ↓
Check facts, statistical meaning and final-size readability
```

Style mode inspects the real source when available. A reading note helps locate the relevant passage; a text-only source cannot establish colors or layout. Missing evidence is stated explicitly. Reference-paper results and error bars never become your project's results.

## Evidence library

| Material | Location |
| --- | --- |
| Full statistical report | [250-paper analysis](sources/anatomy/reports/statistical_analysis_250.md) |
| Full figure/table analysis | [Visual analysis](sources/anatomy/reports/visual_design_analysis_250.md) |
| 68 CSV tables | [Statistics and inventories](sources/anatomy/reports/tables/) |
| 250 paper readings | [Reading index](sources/anatomy/reports/tables/reading_index.csv) |
| 250 visual audit records | [Visual audit index](sources/anatomy/reports/visual_audit_index.md) |
| CVPR cases and experimental numbers | [Venue adaptation](references/venue-adaptation.md) |
| Paragraph / figure mapping template | [Style profile](references/style-profile-template.md) |

The statistics, readings and visual records are inherited source material. This release checks preservation and routing; it does not claim a fresh re-review of all 250 papers or measured improvement in paper quality. See [provenance](SOURCE.md) and [validation](reports/validation.md).

A small, dependency-free query tool makes the tables usable without loading an entire inventory:

```bash
python3 scripts/query_evidence.py   --table checkpoint_250_module_summary   --where module=method   --columns module,conference_equal_normalized_word_share,normalized_word_share_q1,normalized_word_share_q3
```

## Package structure

```text
SKILL.md           Three-mode entry point
agents/            Manual-invocation metadata
references/        Current writing, statistical and visual workflows
sources/           Preserved source reports, data and paper analyses
scripts/           Focused evidence queries and package validation
evals/             Routing examples and behavioral cases
reports/           What has actually been checked
```

Current behavior is defined by `SKILL.md` and `references/`. Historical source recipes remain available for context: fixed page counts, fixed figure counts and manuscript-specific restrictions do not override the current workflow.

## Scope and license

The skill supports research argumentation and paper artifacts. Training execution, standalone blog/report writing and submission remain outside its invocation boundary. It does not silently invoke neighboring skills.

The new workflow is released under [MIT](LICENSE). Inherited materials retain their [source notices](THIRD_PARTY_NOTICES.md). Scientific papers, figures and linked external assets retain their original rights.
