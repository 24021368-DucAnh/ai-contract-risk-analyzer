import csv
import unittest
from pathlib import Path

from scripts.build_offsets import align_rows, normalize_whitespace


ROOT = Path(__file__).resolve().parents[1]


class OffsetAlignmentTests(unittest.TestCase):
    def test_offsets_point_to_original_text_across_line_breaks(self):
        source = "Heading\nLương căn bản:\u00a0………………..\nNext"
        row = {"contract_id": "HDLD001", "clause_id": "C001", "clause_text": "Lương căn bản: ………………..", "notes": ""}

        aligned = align_rows([row], {"HDLD001": source})[0]

        self.assertEqual((int(aligned["start_offset"]), int(aligned["end_offset"])), (8, 31))
        self.assertEqual(
            normalize_whitespace(source[int(aligned["start_offset"]):int(aligned["end_offset"])]),
            row["clause_text"],
        )

    def test_repeated_text_uses_next_occurrence_in_contract_order(self):
        rows = [
            {"contract_id": "HDLD001", "clause_id": "C001", "clause_text": "same", "notes": ""},
            {"contract_id": "HDLD001", "clause_id": "C002", "clause_text": "same", "notes": ""},
        ]

        aligned = align_rows(rows, {"HDLD001": "same\nother\nsame"})

        self.assertEqual([int(row["start_offset"]) for row in aligned], [0, 11])

    def test_synthetic_clause_is_left_unaligned_and_flagged(self):
        row = {"contract_id": "HDLD001", "clause_id": "C001", "clause_text": "Đóng bảo hiểm đầy đủ.", "notes": "Split annotation."}

        aligned = align_rows([row], {"HDLD001": "Đóng bảo hiểm và các khoản thuế đầy đủ."})[0]

        self.assertEqual((aligned["start_offset"], aligned["end_offset"]), ("", ""))
        self.assertIn("OFFSET_UNVERIFIED", aligned["notes"])

    def test_current_snapshot_has_only_verified_spans(self):
        raw_dir = ROOT / "data" / "processed" / "raw_text"
        with (ROOT / "data" / "processed" / "clauses_v04.csv").open(encoding="utf-8-sig", newline="") as source_file:
            rows = list(csv.DictReader(source_file))
        source = {path.stem: path.read_text(encoding="utf-8") for path in raw_dir.glob("*.txt")}

        self.assertEqual(len(rows), 183)
        self.assertEqual(set(source), {f"HDLD{i:03d}" for i in range(1, 7)})
        self.assertEqual(sum(bool(row["start_offset"]) for row in rows), 174)
        for row in rows:
            start, end = row["start_offset"], row["end_offset"]
            if not start:
                self.assertEqual(end, "")
                self.assertIn("OFFSET_UNVERIFIED", row["notes"])
                continue
            start, end = int(start), int(end)
            self.assertLess(start, end)
            self.assertEqual(
                normalize_whitespace(source[row["contract_id"]][start:end]),
                normalize_whitespace(row["clause_text"]),
                row["clause_id"],
            )

    def test_annotated_contracts_point_to_current_snapshot(self):
        with (ROOT / "data" / "contracts_metadata.csv").open(encoding="utf-8-sig", newline="") as source_file:
            metadata = list(csv.DictReader(source_file))

        self.assertEqual(
            {row["contract_id"]: row["dataset_version"] for row in metadata if row["dataset_status"] == "ANNOTATED"},
            {f"HDLD{i:03d}": "v04" for i in range(1, 5)},
        )

    def test_raw_text_has_stable_clean_line_endings(self):
        for path in (ROOT / "data" / "processed" / "raw_text").glob("*.txt"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("\r", text, path.name)
            self.assertFalse(text.endswith("\n"), path.name)
            for line in text.split("\n"):
                self.assertEqual(line, line.rstrip(), path.name)


if __name__ == "__main__":
    unittest.main()
