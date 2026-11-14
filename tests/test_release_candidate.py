"""Check the release receipt and hard-case evidence against the frozen inputs."""

import csv
import gzip
import hashlib
import json
import unittest
from pathlib import Path

from scripts.build_offsets import normalize_whitespace

ROOT = Path(__file__).resolve().parents[1]


class ReleaseCandidateTests(unittest.TestCase):
    def test_release_receipt_matches_every_included_file(self):
        receipt = json.loads((ROOT / 'data/releases/v06-rc1/manifest.json').read_text(encoding='utf-8'))
        frozen_paths = {'scripts/validate_dataset.py'}
        for relative_path, expected_hash in receipt['files'].items():
            if relative_path == 'docs/annotation_guideline.md':
                content = gzip.decompress((ROOT / 'data/releases/v06-rc1/frozen/docs/annotation_guideline.md.gz').read_bytes())
                self.assertEqual(hashlib.sha256(content).hexdigest(), expected_hash, relative_path)
                continue
            path = (ROOT / 'data/releases/v06-rc1/frozen' / relative_path
                    if relative_path in frozen_paths else ROOT / relative_path)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             expected_hash, relative_path)

    def test_current_freeze_receipt_matches_current_files(self):
        receipt = json.loads((ROOT / 'data/releases/current_freeze_2026-11-06/manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(receipt['status'], 'CURRENT_WORKSPACE_FREEZE_RECEIPT')
        for relative_path, expected_hash in receipt['files'].items():
            self.assertEqual(hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest(),
                             expected_hash, relative_path)

    def test_hard_cases_keep_inherited_labels_source_evidence_and_scoring_masks(self):
        with (ROOT / 'data/processed/clauses_v06.csv').open(encoding='utf-8-sig', newline='') as f:
            dataset = {r['clause_id']: r for r in csv.DictReader(f)}
        split = json.loads((ROOT / 'data/splits/provisional_v06.json').read_text(encoding='utf-8'))
        cases = [json.loads(line) for line in (ROOT / 'data/evaluation/hard_test_v06_rc1.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertTrue(cases)
        self.assertEqual(len(cases), len({c['case_id'] for c in cases}))
        for case in cases:
            row = dataset[case['clause_id']]
            self.assertIn(row['contract_id'], split['splits']['test']['contracts'])
            self.assertNotIn(row['clause_id'], split['splits']['test']['excluded_clause_ids'])
            self.assertEqual(case['expected_clause_type'], row['clause_type'])
            self.assertEqual(case['input_text'], row['clause_text'])
            self.assertIsNone(case['legal_risk_ground_truth'])
            self.assertEqual(case['independent_review_status'], 'PENDING')
            path = ROOT / case['source_raw_text']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), case['source_raw_sha256'])
            source = path.read_text(encoding='utf-8')
            span = case['source_reference_span']
            self.assertEqual(source[span['start']:span['end']], span['text'])
            if row['offset_quality'] == 'EXACT':
                self.assertEqual(normalize_whitespace(span['text']), normalize_whitespace(row['clause_text']))
                self.assertEqual(case['gold_exact_clause_span'], {'start': span['start'], 'end': span['end']})
            else:
                self.assertIsNone(case['gold_exact_clause_span'])


if __name__ == '__main__':
    unittest.main()
