import csv
import unittest
from pathlib import Path

from scripts.build_offsets import normalize_whitespace


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


class ClauseV06Tests(unittest.TestCase):
    def test_snapshot_preserves_v05_and_adds_reviewed_hdld005_with_exact_spans(self):
        with (PROCESSED / "clauses_v05.csv").open(encoding="utf-8-sig", newline="") as handle:
            old = list(csv.DictReader(handle))
        with (PROCESSED / "clauses_v06.csv").open(encoding="utf-8-sig", newline="") as handle:
            new = list(csv.DictReader(handle))

        self.assertEqual(new[:len(old)], old)
        added = new[len(old):]
        self.assertGreaterEqual(len(added), 45)
        self.assertEqual({row["contract_id"] for row in added}, {"HDLD005"})
        self.assertEqual([row["clause_id"] for row in added],
                         [f"HDLD005_C{i:03d}" for i in range(1, len(added) + 1)])
        self.assertEqual({row["annotation_status"] for row in added}, {"REVIEWED"})
        self.assertEqual({row["offset_quality"] for row in added}, {"EXACT"})
        self.assertFalse(any("Nghĩa vụ khác theo thoả thuận8" in row["clause_text"]
                             for row in added))
        raw = (PROCESSED / "raw_text" / "HDLD005.txt").read_text(encoding="utf-8")
        previous_end = 0
        for row in added:
            start, end = int(row["start_offset"]), int(row["end_offset"])
            self.assertLessEqual(previous_end, start, row["clause_id"])
            self.assertLess(start, end, row["clause_id"])
            self.assertEqual(normalize_whitespace(raw[start:end]),
                             normalize_whitespace(row["clause_text"]), row["clause_id"])
            self.assertNotIn("Ghi rõ thời hạn sử dụng dịch vụ", row["clause_text"])
            previous_end = end
        self.assertIn("WORKING_CONDITIONS", {row["clause_type"] for row in added})
        self.assertIn("TRAINING", {row["clause_type"] for row in added})

    def test_metadata_counts_match_current_snapshot(self):
        with (PROCESSED / "clauses_v06.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        with (ROOT / "data" / "contracts_metadata.csv").open(encoding="utf-8-sig", newline="") as handle:
            metadata = list(csv.DictReader(handle))
        for item in metadata:
            if item["dataset_status"] == "ANNOTATED":
                self.assertEqual(item["dataset_version"], "v06")
                self.assertEqual(int(item["clause_count"]),
                                 sum(row["contract_id"] == item["contract_id"] for row in rows))


if __name__ == "__main__":
    unittest.main()
