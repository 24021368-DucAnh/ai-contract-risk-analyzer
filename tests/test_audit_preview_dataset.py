import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.audit_preview_dataset import audit_preview_dataset, summarize_blockers

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/processed/clauses_v06.csv"
METADATA = ROOT / "data/contracts_metadata.csv"
RAW_TEXT = ROOT / "data/processed/raw_text"


def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def write_rows(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class PreviewAuditTests(unittest.TestCase):
    def test_blocker_summary_aggregates_unknown_contract_rows(self):
        summary = summarize_blockers([
            "clauses:2: unknown contract_id HDLD010",
            "clauses:3: unknown contract_id HDLD010",
            "pending annotation review: 2 rows",
        ])

        self.assertEqual(summary, [
            "HDLD010: 2 rows lack a metadata record",
            "pending annotation review: 2 rows",
        ])

    def test_unreviewed_new_contract_is_blocked_without_hiding_structural_result(self):
        fields, rows = read_rows(BASE)
        new_row = dict(rows[0], clause_id="HDLD999_C001", contract_id="HDLD999",
                       annotation_status="NEEDS_REVIEW")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw_dir = root / "data/processed/raw_text"
            raw_dir.mkdir(parents=True)
            source_dir = root / "data/raw/contracts"
            source_dir.mkdir(parents=True)
            for source in (ROOT / "data/raw/contracts").glob("HDLD00[1-6].*"):
                shutil.copyfile(source, source_dir / source.name)
            for source in RAW_TEXT.glob("HDLD00[1-5].txt"):
                shutil.copyfile(source, raw_dir / source.name)
            (raw_dir / "HDLD999.txt").write_bytes((RAW_TEXT / "HDLD001.txt").read_bytes())
            preview = root / "clauses_v07.csv"
            write_rows(preview, fields, rows + [new_row])
            audit = audit_preview_dataset(BASE, preview, METADATA, raw_dir)

        self.assertEqual(audit.structural_errors, [])
        self.assertEqual(audit.new_rows, 1)
        self.assertEqual(audit.pending_rows, 1)
        self.assertTrue(any("pending annotation review" in item for item in audit.release_blockers))
        self.assertTrue(any("unknown contract_id HDLD999" in item for item in audit.release_blockers))
        self.assertEqual(sum("dataset_version mismatch" in item for item in audit.release_blockers), 5)
        self.assertEqual(audit.span_errors, 0)
        self.assertEqual(audit.valid_spans, len(rows))
        self.assertEqual(audit.row_counts_by_contract["HDLD999"]["metadata_missing"], 1)
        self.assertEqual(audit.row_counts_by_contract["HDLD999"]["NEEDS_REVIEW"], 1)

    def test_changed_base_row_is_structural_error(self):
        fields, rows = read_rows(BASE)
        changed = [dict(row) for row in rows]
        changed[0]["clause_type"] = "OTHER"
        with tempfile.TemporaryDirectory() as directory:
            preview = Path(directory) / "clauses_v07.csv"
            write_rows(preview, fields, changed)
            audit = audit_preview_dataset(BASE, preview, METADATA, RAW_TEXT)

        self.assertTrue(any("changed from base" in item for item in audit.structural_errors))

    def test_new_reviewed_row_is_not_silently_accepted(self):
        fields, rows = read_rows(BASE)
        new_row = dict(rows[0], clause_id="HDLD001_C999")
        with tempfile.TemporaryDirectory() as directory:
            preview = Path(directory) / "clauses_v07.csv"
            write_rows(preview, fields, rows + [new_row])
            audit = audit_preview_dataset(BASE, preview, METADATA, RAW_TEXT)

        self.assertTrue(any("new row is not NEEDS_REVIEW" in item for item in audit.structural_errors))

    def test_missing_preview_column_is_reported_without_crashing(self):
        fields, rows = read_rows(BASE)
        fields.remove("clause_id")
        with tempfile.TemporaryDirectory() as directory:
            preview = Path(directory) / "clauses_v07.csv"
            write_rows(preview, fields, [{key: value for key, value in row.items() if key in fields} for row in rows])
            audit = audit_preview_dataset(BASE, preview, METADATA, RAW_TEXT)

        self.assertIn("preview columns differ from base", audit.structural_errors)

    def test_new_rows_without_source_metadata_are_explicitly_blocked(self):
        fields, rows = read_rows(BASE)
        new_row = dict(rows[0], clause_id="HDLD999_C001", contract_id="HDLD999",
                       annotation_status="NEEDS_REVIEW")
        with tempfile.TemporaryDirectory() as directory:
            preview = Path(directory) / "clauses_v07.csv"
            write_rows(preview, fields, rows + [new_row])
            audit = audit_preview_dataset(BASE, preview, METADATA, RAW_TEXT)

        self.assertTrue(any("incomplete source metadata" in item for item in audit.release_blockers))
        self.assertEqual(audit.span_errors, 0)
        self.assertEqual(audit.row_counts_by_contract["HDLD999"]["metadata_missing"], 1)


if __name__ == "__main__":
    unittest.main()
