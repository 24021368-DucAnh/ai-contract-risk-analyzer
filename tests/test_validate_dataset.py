import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_dataset import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
CLAUSES = ROOT / "data" / "processed" / "clauses_v05.csv"
METADATA = ROOT / "data" / "contracts_metadata.csv"
RAW_TEXT = ROOT / "data" / "processed" / "raw_text"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class DatasetValidationTests(unittest.TestCase):
    def test_current_snapshot_passes_and_reports_context_for_review(self):
        report = validate_dataset(CLAUSES, METADATA, RAW_TEXT)

        self.assertEqual(report.errors, [])
        self.assertEqual(report.contract_count, 4)
        self.assertEqual(report.clause_count, 183)
        self.assertEqual(report.offset_quality_counts, {"EXACT": 174, "CONTEXT": 9})
        self.assertEqual(report.annotation_status_counts, {"REVIEWED": 183})
        self.assertEqual(len(report.context_clause_ids), 9)
        self.assertEqual(report.class_counts["WORKING_CONDITIONS"], 6)

    def test_bad_clause_fields_and_offsets_are_reported_together(self):
        fields, rows = read_csv(CLAUSES)
        rows[0]["clause_type"] = "MADE_UP"
        rows[1]["clause_id"] = rows[0]["clause_id"]
        rows[2]["contract_id"] = "HDLD999"
        rows[3]["clause_text"] = " "
        rows[4]["end_offset"] = "999999"
        rows[5]["start_offset"] = "nope"
        rows[6]["annotation_status"] = "NOT_REVIEWED"
        with tempfile.TemporaryDirectory() as directory:
            clauses = Path(directory) / "clauses_v05.csv"
            write_csv(clauses, fields, rows)
            report = validate_dataset(clauses, METADATA, RAW_TEXT)

        errors = "\n".join(report.errors)
        for expected in (
            "invalid clause_type", "duplicate clause_id", "unknown contract_id",
            "empty clause_text", "offset out of bounds", "invalid start_offset",
            "invalid annotation_status",
        ):
            self.assertIn(expected, errors)

    def test_exact_text_mismatch_and_context_marker_are_reported(self):
        fields, rows = read_csv(CLAUSES)
        exact = next(row for row in rows if row["offset_quality"] == "EXACT")
        context = next(row for row in rows if row["offset_quality"] == "CONTEXT")
        exact["clause_text"] = "This differs from the source"
        context["notes"] = ""
        with tempfile.TemporaryDirectory() as directory:
            clauses = Path(directory) / "clauses_v05.csv"
            write_csv(clauses, fields, rows)
            report = validate_dataset(clauses, METADATA, RAW_TEXT)

        self.assertIn("EXACT span mismatch", "\n".join(report.errors))
        self.assertIn("CONTEXT requires OFFSET_CONTEXT note", "\n".join(report.errors))

    def test_metadata_count_mismatch_is_reported(self):
        fields, rows = read_csv(METADATA)
        rows[0]["clause_count"] = "38"
        with tempfile.TemporaryDirectory() as directory:
            metadata = Path(directory) / "metadata.csv"
            write_csv(metadata, fields, rows)
            report = validate_dataset(CLAUSES, metadata, RAW_TEXT)

        self.assertIn("clause_count mismatch", "\n".join(report.errors))

    def test_empty_clause_file_is_not_accepted_as_clean(self):
        fields, _ = read_csv(CLAUSES)
        with tempfile.TemporaryDirectory() as directory:
            clauses = Path(directory) / "clauses_v05.csv"
            write_csv(clauses, fields, [])
            report = validate_dataset(clauses, METADATA, RAW_TEXT)

        self.assertIn("no clause rows", "\n".join(report.errors))

    def test_context_span_must_highlight_nonblank_source(self):
        fields, rows = read_csv(CLAUSES)
        context = next(row for row in rows if row["offset_quality"] == "CONTEXT")
        raw = (RAW_TEXT / f"{context['contract_id']}.txt").read_text(encoding="utf-8")
        blank_position = raw.index(" ")
        context["start_offset"] = str(blank_position)
        context["end_offset"] = str(blank_position + 1)
        with tempfile.TemporaryDirectory() as directory:
            clauses = Path(directory) / "clauses_v05.csv"
            write_csv(clauses, fields, rows)
            report = validate_dataset(clauses, METADATA, RAW_TEXT)

        self.assertIn("CONTEXT span is blank", "\n".join(report.errors))


if __name__ == "__main__":
    unittest.main()
