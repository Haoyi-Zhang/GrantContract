#!/usr/bin/env python3
"""Compare reproducible values, excluding non-deterministic resource measurements."""
import argparse
import csv
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
STABLE=('graphs.csv','observations.csv','summary.json','witnesses.json',
    'bridge-plants.json','bridge-guards.json','bridge-cases.json','bridge-observations.json','bridge-summary.json',
    'parametric-summary.json','metaoracle-summary.json')


def verify_reference_audit() -> None:
    with (ROOT/'reference_audit.csv').open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    keys = [row['key'] for row in rows]
    if not 30 <= len(rows) <= 45 or len(keys) != len(set(keys)):
        raise ValueError('reference audit must contain 30--45 unique records')
    if any(row.get('status') != 'PASS' for row in rows):
        raise ValueError('reference audit contains a non-PASS record')
    tc_rows = [row for row in rows
               if row.get('venue', '').startswith('IEEE Transactions on Computers')]
    if len(tc_rows) != 12:
        raise ValueError('reference audit does not contain twelve TC calibration papers')
    expected = {
        'heterogen': ('HPCA 2022', '756-771', '10.1109/HPCA53966.2022.00061'),
        'disco': ('IEEE Transactions on Computers 72(4)', '1163-1177',
                  '10.1109/TC.2022.3193624'),
        'tardis': ('PACT 2015', '227-240', '10.1109/PACT.2015.12'),
    }
    by_key = {row['key']: row for row in rows}
    for key, (venue, pages, identifier) in expected.items():
        row = by_key.get(key, {})
        if (row.get('venue'), row.get('pages_or_article'), row.get('doi_or_identifier')) != (venue, pages, identifier):
            raise ValueError(f'corrected reference metadata regressed: {key}')
    if by_key.get('rc11corrigendum', {}).get('venue') != 'Author-issued corrigendum':
        raise ValueError('RC11 corrigendum record missing or misclassified')
    synapse = by_key.get('synapse', {})
    if (synapse.get('venue'), synapse.get('pages_or_article')) != ('MICRO 2026 (accepted)', 'to appear'):
        raise ValueError('newest accepted-work metadata missing or overstated')
    dois = [row['doi_or_identifier'].lower() for row in rows
            if row.get('doi_or_identifier', '').startswith('10.')]
    if len(dois) != len(set(dois)):
        raise ValueError('duplicate DOI in reference audit')


def verify_public_protocol_audit() -> None:
    with (ROOT/'public_protocol_audit.csv').open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 5 or len({row['fact_id'] for row in rows}) != 5:
        raise ValueError('public-protocol audit must contain five unique facts')
    commit = '0c5c6d8e06ecf1a1d6fed3e6097e496850306dc0'
    if any(row.get('commit') != commit for row in rows):
        raise ValueError('public-protocol audit is not pinned to the declared commit')
    if any('not a lift' not in row.get('scope_limit', '').lower() for row in rows):
        raise ValueError('public-protocol audit contains an unbounded lifting claim')
    joined = ' '.join(row.get('concrete_fact', '') for row in rows)
    for token in ('ACK', 'ALL_ACKS', 'NumIntPendingAcks', 'zero'):
        if token not in joined:
            raise ValueError('public-protocol audit missing required anchor: '+token)


def load(p):
    if p.suffix=='.json': return json.loads(p.read_text())
    with p.open(newline='') as f: return list(csv.DictReader(f))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    verify_reference_audit()
    verify_public_protocol_audit()
    for name in STABLE:
        if load(a.output/name)!=load(ROOT/'results'/name):
            raise ValueError('scientific result mismatch: '+name)
    parametric=load(a.output/'parametric-summary.json')
    metaoracle=load(a.output/'metaoracle-summary.json')
    if parametric.get('contract_exactness_mismatches') != 0:
        raise ValueError('contract exactness mismatch reported')
    if any(not row.get('contract_exact') for row in parametric.get('contracts', [])):
        raise ValueError('a generated contract failed the explicit safety/maximality audit')
    if any(row.get('unsafe_grant_history_count') or row.get('missed_safe_history_count')
           or row.get('ineligible_grant_history_count')
           for row in parametric.get('contracts', [])):
        raise ValueError('nonzero contract-audit defect count')
    for key in ('kernel_mismatches','observer_mismatches','greatest_contract_mismatches','nonblocking_mismatches'):
        if metaoracle.get(key) != 0:
            raise ValueError('meta-oracle mismatch reported: '+key)
    if metaoracle.get('plants_checked') != 486 or metaoracle.get('receipt_partitions_checked') != 75:
        raise ValueError('meta-oracle universe size regressed')
    if not metaoracle.get('existential_mutant_counterexamples') or not metaoracle.get('eligibility_mutant_counterexamples'):
        raise ValueError('meta-oracle failed to kill required mutants')
    r=json.loads((a.output/'resources.json').read_text())
    if not (r['workers']==1 and r['cpu_seconds']<120 and r['peak_rss_kib']<2.5*1024*1024):
        raise ValueError('resource limit failed')
    print(f'PASS: eleven stable scientific outputs match; contract, meta-oracle, public-source, and {len(list(csv.DictReader((ROOT / "reference_audit.csv").open(newline="", encoding="utf-8"))))}-record reference audits pass; finite values only, not a general proof.')

if __name__=='__main__':
    try: main()
    except (OSError,ValueError,KeyError) as e:
        print('verification failed: '+str(e),file=sys.stderr);sys.exit(2)
