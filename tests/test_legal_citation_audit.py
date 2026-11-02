"""Ensure legal-source discovery emits locators, never source text or PII."""

import tempfile
import unittest
import csv
from pathlib import Path

from scripts.audit_legal_citations import collect_references


class LegalCitationAuditTests(unittest.TestCase):
    def test_heading_excluded_and_source_content_not_emitted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "data/processed/raw_text"
            source.mkdir(parents=True)
            (source / "HDLD001.txt").write_text(
                "Điều 1: Tiêu đề\nBí mật cá nhân: email@example.com. "
                "Căn cứ Điều 33 pháp luật.\n", encoding="utf-8")
            records = collect_references(source, root / "absent.csv", root)
            self.assertEqual(1, len(records))
            self.assertEqual("33", records[0]["article_number"])
            self.assertEqual(2, records[0]["source_line"])
            self.assertNotIn("email@example.com", str(records))
            self.assertTrue(all("source_text" in r for r in records))
            self.assertEqual("HUMAN_LEGAL_REVIEW_REQUIRED", records[0]["review_status"])

    def test_known_mismatch_is_still_unapproved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "data/processed/raw_text"
            source.mkdir(parents=True)
            lines = ["placeholder"] * 80 + ["Theo Điều 38 Bộ luật Lao động 2019"]
            (source / "HDLD003.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
            row, = collect_references(source, root / "missing.csv", root)
            self.assertEqual("36", row["candidate_correct_article"])
            self.assertEqual("HUMAN_LEGAL_REVIEW_REQUIRED", row["review_status"])

    def test_annotation_notes_are_scanned_without_copying_note_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "data/processed/raw_text"
            source.mkdir(parents=True)
            notes = root / "data/processed/clauses_v06.csv"
            with notes.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=("contract_id", "clause_id", "notes"))
                writer.writeheader()
                writer.writerow({"contract_id": "HDLD002", "clause_id": "HDLD002_C001",
                                 "notes": "Số định danh: 123123123. Theo Điều 11"})
            row, = collect_references(source, notes, root)
            self.assertEqual("ANNOTATION_NOTE_REFERENCE", row["source_kind"])
            self.assertEqual("11", row["article_number"])
            self.assertEqual("HDLD002_C001", row["linked_clause_ids"])
            self.assertNotIn("123123123", str(row))


if __name__ == "__main__":
    unittest.main()
