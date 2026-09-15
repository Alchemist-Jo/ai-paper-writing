#!/usr/bin/env python3
"""Read source CSV rows without changing their values or statistical meaning."""
import argparse
import csv
import json
from pathlib import Path

TABLES = Path(__file__).resolve().parents[1] / 'sources/anatomy/reports/tables'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List bundled table names')
    parser.add_argument('--table', help='Table stem, or its CSV filename')
    parser.add_argument('--where', action='append', default=[], metavar='FIELD=VALUE')
    parser.add_argument('--contains', action='append', default=[], metavar='FIELD=TEXT')
    parser.add_argument('--columns', help='Comma-separated source fields')
    parser.add_argument('--limit', type=int, default=20, help='Maximum rows to display')
    args = parser.parse_args()
    if args.list:
        print('\n'.join(p.stem for p in sorted(TABLES.glob('*.csv'))))
        return
    if not args.table:
        parser.error('--table is required unless --list is used')
    available = {p.stem: p for p in TABLES.glob('*.csv')}
    stem = args.table.removesuffix('.csv')
    if stem not in available:
        parser.error('Unknown table; use --list to see available names')
    if args.limit < 1:
        parser.error('--limit must be positive')
    with available[stem].open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        columns = args.columns.split(',') if args.columns else fields
        filters = []
        for kind, items in [('exact', args.where), ('contains', args.contains)]:
            for item in items:
                if '=' not in item:
                    parser.error('Filters must use FIELD=VALUE')
                field, value = item.split('=', 1)
                if field not in fields:
                    parser.error(f'Unknown field: {field}; fields: {", ".join(fields)}')
                filters.append((kind, field, value))
        for field in columns:
            if field not in fields:
                parser.error(f'Unknown field: {field}; fields: {", ".join(fields)}')
        matches = []
        total = 0
        for row in reader:
            if all(row[field] == value if kind == 'exact' else value.casefold() in row[field].casefold()
                   for kind, field, value in filters):
                total += 1
                if len(matches) < args.limit:
                    matches.append({field: row[field] for field in columns})
    print(json.dumps({'table': available[stem].name, 'matched_rows': total,
                      'displayed_rows': len(matches), 'values': 'original CSV strings',
                      'rows': matches}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
