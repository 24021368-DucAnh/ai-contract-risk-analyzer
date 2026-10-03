import csv
import unittest
from pathlib import Path

from scripts.build_context_offsets import fill_context_offsets
from scripts.build_offsets import normalize_whitespace


ROOT = Path(__file__).resolve().parents[1]


class ContextOffsetTests(unittest.TestCase):
    def test_v05_has_location_for_every_clause_with_quality_flag(self):
        raw_dir = ROOT / "data" / "processed" / "raw_text"
        with (ROOT / "data" / "processed" / "clauses_v05.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        raw = {path.stem: path.read_text(encoding="utf-8") for path in raw_dir.glob("*.txt")}

        self.assertEqual(len(rows), 183)
        self.assertEqual(
            {quality: sum(row["offset_quality"] == quality for row in rows)
             for quality in ("EXACT", "CONTEXT")},
            {"EXACT": 174, "CONTEXT": 9},
        )
        for row in rows:
            start, end = int(row["start_offset"]), int(row["end_offset"])
            self.assertLess(start, end)
            excerpt = raw[row["contract_id"]][start:end]
            self.assertTrue(excerpt.strip(), row["clause_id"])
            if row["offset_quality"] == "EXACT":
                self.assertEqual(
                    normalize_whitespace(excerpt), normalize_whitespace(row["clause_text"])
                )
            else:
                self.assertIn("OFFSET_CONTEXT", row["notes"])

    def test_context_spans_highlight_only_the_relevant_source_phrase(self):
        expected = {
            "HDLD003_C018": "các loại bảo hiểm",
            "HDLD003_C018A": "các khoản thuế",
            "HDLD004_C023": "nghỉ ngơi",
            "HDLD004_C024": "hỗ trợ học nghề, học văn hóa",
            "HDLD004_C025": "bố trí chỗ ăn, ở",
            "HDLD004_C026": "trang bị bảo hộ lao động",
            "HDLD004_C027": "bồi thường thiệt hại",
            "HDLD004_C043": "có hiệu lực từ ngày ......... tháng ........... năm ..........",
        }
        processed = ROOT / "data" / "processed"
        with (processed / "clauses_v05.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["clause_id"]: row for row in csv.DictReader(handle)}
        for clause_id, phrase in expected.items():
            row = rows[clause_id]
            raw = (processed / "raw_text" / f"{row['contract_id']}.txt").read_text(encoding="utf-8")
            self.assertEqual(raw[int(row["start_offset"]):int(row["end_offset"])], phrase, clause_id)

    def test_context_spans_are_reproducible_from_v04(self):
        processed = ROOT / "data" / "processed"
        with (processed / "clauses_v04.csv").open(encoding="utf-8-sig", newline="") as handle:
            original = list(csv.DictReader(handle))
        with (processed / "clauses_v05.csv").open(encoding="utf-8-sig", newline="") as handle:
            current = list(csv.DictReader(handle))
        raw = {
            path.stem: path.read_text(encoding="utf-8")
            for path in (processed / "raw_text").glob("*.txt")
        }
        self.assertEqual(fill_context_offsets(original, raw), current)


if __name__ == "__main__":
    unittest.main()
