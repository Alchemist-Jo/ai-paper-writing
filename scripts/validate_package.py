#!/usr/bin/env python3
"""Check current references, mode metadata and bundled evidence availability."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate():
    errors = []
    skill = (ROOT / 'SKILL.md').read_text()
    if 'disable-model-invocation: true' not in skill:
        errors.append('Missing Claude manual-invocation metadata')
    for name in ['interface.yaml', 'openai.yaml']:
        text = (ROOT / 'agents' / name).read_text()
        if 'allow_implicit_invocation: false' not in text:
            errors.append(f'Missing Codex manual-invocation metadata: {name}')
    for mode in ['Grill', 'Draft', 'Style']:
        if mode not in skill:
            errors.append(f'Missing mode: {mode}')
    if len(list(ROOT.rglob('SKILL.md'))) != 1:
        errors.append('Archived SKILL.md files can create unintended entry points')
    current_docs = [ROOT / name for name in ['SKILL.md', 'README.md', 'README.zh-CN.md', 'SOURCE.md', 'THIRD_PARTY_NOTICES.md']]
    current_docs += list((ROOT / 'references').glob('*.md'))
    for document in current_docs:
        for link in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if link.startswith(('https:', 'http:', '#')):
                continue
            if not (document.parent / link.split('#')[0]).exists():
                errors.append(f'Missing reference: {document.name} -> {link}')
    corpus = ROOT / 'sources/anatomy'
    with (corpus / 'reports/tables/reading_index.csv').open() as stream:
        cohort = [row for row in csv.DictReader(stream) if row['checkpoint_250'] == 'yes']
    counts = {venue: sum(row['conference'] == venue for row in cohort) for venue in ['ICLR', 'ICML']}
    if counts != {'ICLR': 150, 'ICML': 100}:
        errors.append(f'Unexpected source cohort: {counts}')
    for row in cohort:
        for key in ['reading_markdown', 'reading_json']:
            if not (corpus / row[key]).exists():
                errors.append('Missing reading: ' + row[key])
        for extension in ['md', 'json']:
            if not (corpus / 'visual_audits' / (row['paper_id'] + '.' + extension)).exists():
                errors.append('Missing visual record: ' + row['paper_id'])
    return {'errors': errors, 'cohort': counts, 'csv_tables': len(list((corpus / 'reports/tables').glob('*.csv'))),
            'skill_entrypoints': len(list(ROOT.rglob('SKILL.md')))}


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['errors']))
