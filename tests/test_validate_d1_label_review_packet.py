import unittest

from scripts.validate_d1_label_review_packet import (
    validate_packet,
    validate_reviewed_packet,
)


def row(**updates):
    item = {
        "clause_id": "HDLD001_C001", "contract_id": "HDLD001",
        "candidate_label": "JOB_INFO", "source_span_start": "0",
        "source_span_end": "5", "offset_quality": "EXACT",
        "reviewer_label": "", "reviewer_span_start": "", "reviewer_span_end": "",
        "reviewer_id": "", "review_status": "PENDING_INDEPENDENT_REVIEW",
        "adjudicated_label": "", "adjudicator_id": "", "adjudication_date": "",
        "notes": "",
    }
    item.update(updates)
    return item


class D1ReviewPacketValidationTests(unittest.TestCase):
    def test_accepts_pending_exact_candidate(self):
        result = validate_packet([row()], {"HDLD001_C001"})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["adjudicated_rows"], 0)

    def test_rejects_duplicate_and_missing_ids(self):
        with self.assertRaisesRegex(ValueError, "duplicate clause_id"):
            validate_packet([row(), row()], {"HDLD001_C001"})
        with self.assertRaisesRegex(ValueError, "do not match"):
            validate_packet([row()], {"HDLD001_C002"})

    def test_context_must_not_claim_exact_span(self):
        with self.assertRaisesRegex(ValueError, "CONTEXT cannot"):
            validate_packet([row(offset_quality="CONTEXT")], {"HDLD001_C001"})

    def test_reviewer_fields_must_start_blank(self):
        with self.assertRaisesRegex(ValueError, "must start blank"):
            validate_packet([row(reviewer_id="someone")], {"HDLD001_C001"})

    def test_reviewed_gold_requires_distinct_adjudicator_and_timezone(self):
        completed = row(
            reviewer_label="JOB_INFO", reviewer_span_start="0", reviewer_span_end="5",
            reviewer_id="reviewer-1", review_status="REVIEWED_AGREES",
            adjudicated_label="JOB_INFO", adjudicator_id="adjudicator-1",
            adjudication_date="2026-11-02T10:00:00+07:00",
        )
        result = validate_reviewed_packet([completed], {"HDLD001_C001"})
        self.assertEqual(result["gold_clause_label_rows"], 1)
        completed["adjudication_date"] = "2026-11-02T10:00:00"
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            validate_reviewed_packet([completed], {"HDLD001_C001"})


if __name__ == "__main__":
    unittest.main()
