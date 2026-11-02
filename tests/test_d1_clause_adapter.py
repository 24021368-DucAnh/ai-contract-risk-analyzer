import csv
import hashlib
import unittest
from pathlib import Path

from scripts.build_d1_clause_candidates import build_d1_clause_candidates


ROOT = Path(__file__).resolve().parents[1]


class D1ClauseAdapterTests(unittest.TestCase):
    def test_v06_baseline_excludes_hdld005_and_context_exact_spans(self):
        with (ROOT / "data/processed/clauses_v06.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))

        result = build_d1_clause_candidates(rows)
        items = result["items"]

        self.assertEqual(len(items), 183)
        self.assertEqual({item["contract_id"] for item in items},
                         {"HDLD001", "HDLD002", "HDLD003", "HDLD004"})
        self.assertEqual(result["source"], "data/processed/clauses_v06.csv")
        self.assertEqual(result["taxonomy_version"], "clause_taxonomy_v03")
        self.assertEqual(sum(item["span"] is None for item in items), 9)
        self.assertEqual(sum(item["source_reference_span"] is not None for item in items), 9)
        self.assertTrue(all(len(item["labels"]) == 1 for item in items))
        self.assertTrue(all(item["annotator"] is None for item in items))
        self.assertEqual(result["status"], "CANDIDATE_NOT_SEGMENTATION_GOLD")
        self.assertFalse(result["scope"]["segmentation_gold"])
        self.assertFalse(result["scope"]["adjudicated"])

    def test_pending_row_is_not_promoted_to_label_candidate(self):
        rows = [{
            "clause_id": "HDLD001_C001", "contract_id": "HDLD001",
            "clause_type": "JOB_INFO", "annotation_status": "NEEDS_REVIEW",
            "start_offset": "0", "end_offset": "5", "offset_quality": "EXACT",
        }]
        result = build_d1_clause_candidates(rows)
        self.assertEqual(result["items"], [])

    def test_exact_span_must_match_and_raw_hash_is_recorded(self):
        rows = [{
            "clause_id": "HDLD001_C001", "contract_id": "HDLD001",
            "clause_type": "JOB_INFO", "annotation_status": "REVIEWED",
            "start_offset": "0", "end_offset": "11", "offset_quality": "EXACT",
            "clause_text": "Lương tháng",
        }]
        raw = {"HDLD001": "Lương tháng"}
        result = build_d1_clause_candidates(rows, raw_texts=raw, source_sha256="a" * 64)
        self.assertEqual(result["raw_source_sha256"]["HDLD001"], hashlib.sha256(raw["HDLD001"].encode()).hexdigest())
        rows[0]["clause_text"] = "Lương tuần"
        with self.assertRaisesRegex(ValueError, "EXACT span does not match"):
            build_d1_clause_candidates(rows, raw_texts=raw)

    def test_invalid_span_is_rejected(self):
        rows = [{
            "clause_id": "HDLD001_C001", "contract_id": "HDLD001",
            "clause_type": "JOB_INFO", "annotation_status": "REVIEWED",
            "start_offset": "5", "end_offset": "5", "offset_quality": "CONTEXT",
            "clause_text": "x",
        }]
        with self.assertRaisesRegex(ValueError, "invalid source span"):
            build_d1_clause_candidates(rows)


if __name__ == "__main__":
    unittest.main()
