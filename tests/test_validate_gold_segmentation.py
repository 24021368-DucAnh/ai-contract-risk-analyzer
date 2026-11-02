import hashlib
import unittest

from scripts.validate_gold_segmentation import validate_gold_segmentation


def make_gold(text="Điều 1\nNội dung Điều."):
    return {
        "schema_version": "gold_segmentation_v1",
        "doc_id": "SYNTHETIC001",
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "offset_unit": "unicode_code_point",
        "annotation": {
            "annotator_id": "annotator-a",
            "reviewer_id": "reviewer-b",
            "adjudicator_id": "adjudicator-c",
            "adjudicated_at": "2026-11-01T10:00:00+07:00",
            "decision": "ADJUDICATED_ACCEPTED",
        },
        "segments": [
            {"start_char": 0, "end_char": 6, "gold_clause_ref": "SYNTHETIC001_C001"},
            {"start_char": 7, "end_char": len(text), "gold_clause_ref": "SYNTHETIC001_C002"},
        ],
    }


class GoldSegmentationValidationTests(unittest.TestCase):
    def test_valid_adjudicated_partition_uses_unicode_codepoint_offsets(self):
        text = "Điều 1\nNội dung 😀 Điều."
        payload = make_gold(text)
        payload["segments"][1]["end_char"] = len(text)
        result = validate_gold_segmentation(payload, text)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["segment_count"], 2)

    def test_source_hash_must_match_exact_canonical_text(self):
        with self.assertRaisesRegex(ValueError, "source_sha256"):
            validate_gold_segmentation(make_gold(), "Điều 1\nNội dung điều.")

    def test_overlapping_segments_are_rejected(self):
        payload = make_gold()
        payload["segments"][1]["start_char"] = 5
        with self.assertRaisesRegex(ValueError, "overlaps"):
            validate_gold_segmentation(payload, "Điều 1\nNội dung Điều.")

    def test_non_whitespace_gaps_are_rejected(self):
        payload = make_gold()
        payload["segments"][1]["start_char"] = 8
        with self.assertRaisesRegex(ValueError, "uncovered non-whitespace"):
            validate_gold_segmentation(payload, "Điều 1\nNội dung Điều.")

    def test_duplicate_clause_references_are_rejected(self):
        payload = make_gold()
        payload["segments"][1]["gold_clause_ref"] = payload["segments"][0]["gold_clause_ref"]
        with self.assertRaisesRegex(ValueError, "must be unique"):
            validate_gold_segmentation(payload, "Điều 1\nNội dung Điều.")

    def test_annotator_and_reviewer_must_be_distinct(self):
        payload = make_gold()
        payload["annotation"]["reviewer_id"] = "annotator-a"
        with self.assertRaisesRegex(ValueError, "must be distinct"):
            validate_gold_segmentation(payload, "Điều 1\nNội dung Điều.")

    def test_only_adjudicated_accepted_rows_can_be_gold(self):
        payload = make_gold()
        payload["annotation"]["decision"] = "PENDING"
        with self.assertRaisesRegex(ValueError, "ADJUDICATED_ACCEPTED"):
            validate_gold_segmentation(payload, "Điều 1\nNội dung Điều.")

    def test_adjudication_timestamp_requires_timezone(self):
        payload = make_gold()
        payload["annotation"]["adjudicated_at"] = "2026-11-01T10:00:00"
        with self.assertRaisesRegex(ValueError, "must include a timezone"):
            validate_gold_segmentation(payload, "Điều 1\nNội dung Điều.")


if __name__ == "__main__":
    unittest.main()
