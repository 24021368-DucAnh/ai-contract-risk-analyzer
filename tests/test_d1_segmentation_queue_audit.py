import unittest

from scripts.audit_d1_segmentation_queue import audit_queue


class D1SegmentationQueueAuditTests(unittest.TestCase):
    def setUp(self):
        self.clauses = [
            {
                "clause_id": "HDLD001_C001", "contract_id": "HDLD001",
                "annotation_status": "REVIEWED", "offset_quality": "EXACT",
                "clause_text": "Lương tháng",
            },
            {
                "clause_id": "HDLD001_C002", "contract_id": "HDLD001",
                "annotation_status": "REVIEWED", "offset_quality": "CONTEXT",
                "clause_text": "Lương và phụ cấp",
            },
        ]
        self.queue = [
            {
                "clause_id": "HDLD001_C001", "contract_id": "HDLD001",
                "offset_quality": "EXACT", "start_char": "0", "end_char": "11",
                "review_status": "PENDING_MANUAL_SEGMENTATION", "reviewer_id": "", "review_note": "",
            },
            {
                "clause_id": "HDLD001_C002", "contract_id": "HDLD001",
                "offset_quality": "CONTEXT", "start_char": "12", "end_char": "18",
                "review_status": "PENDING_MANUAL_SEGMENTATION", "reviewer_id": "", "review_note": "",
            },
        ]
        self.raw_texts = {"HDLD001": "Lương tháng! Lương"}

    def test_valid_queue_coverage_checks_exact_offsets_and_context_separately(self):
        result = audit_queue(self.clauses, self.queue, self.raw_texts)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["expected_d1_clauses"], 2)
        self.assertEqual(result["valid_codepoint_spans"], 2)
        self.assertEqual(result["contract_counts"]["HDLD001"]["CONTEXT"], 1)
        self.assertEqual(result["reviewer_or_note_filled_rows"], 0)
        self.assertNotIn("Lương", str(result))

    def test_missing_row_fails_coverage(self):
        result = audit_queue(self.clauses, self.queue[:1], self.raw_texts)

        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["missing_queue_rows"], 1)

    def test_context_span_is_not_required_to_match_clause_text(self):
        self.queue[1]["start_char"] = "0"
        self.queue[1]["end_char"] = "6"

        result = audit_queue(self.clauses, self.queue, self.raw_texts)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["valid_codepoint_spans"], 2)

    def test_exact_span_mismatch_fails(self):
        self.queue[0]["end_char"] = "12"

        result = audit_queue(self.clauses, self.queue, self.raw_texts)

        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("EXACT span" in error for error in result["errors"]))

    def test_duplicate_queue_ids_fail(self):
        result = audit_queue(self.clauses, self.queue + [self.queue[0]], self.raw_texts)

        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("duplicate" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
