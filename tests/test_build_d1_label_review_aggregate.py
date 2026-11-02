import unittest

from scripts.build_d1_label_review_aggregate import build_aggregate


class D1LabelReviewAggregateTests(unittest.TestCase):
    def test_aggregates_counts_without_text(self):
        rows = [
            {"clause_id": "HDLD001_C001", "contract_id": "HDLD001", "annotation_status": "REVIEWED", "clause_type": "JOB_INFO", "offset_quality": "EXACT", "clause_text": "secret text"},
            {"clause_id": "HDLD001_C002", "contract_id": "HDLD001", "annotation_status": "REVIEWED", "clause_type": "JOB_INFO", "offset_quality": "CONTEXT", "clause_text": "other secret"},
            {"clause_id": "HDLD005_C001", "contract_id": "HDLD005", "annotation_status": "REVIEWED", "clause_type": "OTHER", "offset_quality": "EXACT", "clause_text": "excluded"},
        ]
        result = build_aggregate(rows, "a" * 64)
        self.assertEqual(result["total_reviewed_rows"], 2)
        self.assertEqual(result["by_contract"]["HDLD001"]["JOB_INFO"], 2)
        self.assertEqual(result["offset_quality"], {"CONTEXT": 1, "EXACT": 1})
        self.assertNotIn("secret", str(result))

    def test_rejects_duplicate_d1_clause_id(self):
        row = {"clause_id": "HDLD001_C001", "contract_id": "HDLD001", "annotation_status": "REVIEWED", "clause_type": "JOB_INFO", "offset_quality": "EXACT"}
        with self.assertRaisesRegex(ValueError, "duplicate clause IDs"):
            build_aggregate([row, row], "b" * 64)


if __name__ == "__main__":
    unittest.main()
