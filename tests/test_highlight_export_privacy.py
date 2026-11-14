"""Export must never fall back to an unreviewed raw signed contract."""

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfWriter

from scripts.export_highlight_payload import build_payload


class HighlightExportPrivacyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.processed = self.root / "data/processed"
        (self.processed / "raw_text").mkdir(parents=True)
        (self.processed / "approved").mkdir(parents=True)
        (self.root / "data/intake/restricted").mkdir(parents=True)
        self.unit_id = "SIGNED-U01"
        self.canary = "PRIVATE-CANARY-098761"
        (self.processed / "raw_text" / f"{self.unit_id}.txt").write_text(
            self.canary, encoding="utf-8"
        )
        self.safe_text = "Điều 1. Công việc và tiền lương."
        self.derivative = self.processed / "approved" / "SIGNED-U01.txt"
        self.derivative.write_text(self.safe_text, encoding="utf-8")
        self.source = self.root / "source.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        with self.source.open("wb") as handle:
            writer.write(handle)
        (self.root / "data/intake/restricted/rights.txt").write_text(
            "synthetic approval fixture", encoding="utf-8"
        )
        self.manifest = {
            "candidate_id": "SIGNED", "local_path": "source.pdf",
            "sha256": self.digest(self.source), "bytes": str(self.source.stat().st_size),
            "t1_eligible": "no",
        }
        self.unit = {
            "unit_id": self.unit_id, "candidate_id": "SIGNED", "source_pages": "1-1",
            "signed_check": "VERIFIED", "similarity_group": "FAMILY1",
            "distinct_document_check": "PASS", "template_independence_check": "PENDING",
            "rights_authority_check": "VERIFIED",
            "rights_evidence_path": "data/intake/restricted/rights.txt",
            "rights_store_process": "GRANTED", "rights_share_internal": "GRANTED",
            "rights_eval_derivative": "GRANTED", "visual_redaction": "PASS",
            "text_redaction": "PASS", "metadata_redaction": "PASS",
            "derivative_path": "data/processed/approved/SIGNED-U01.txt",
            "derivative_sha256": self.digest(self.derivative),
            "prepared_by_id": "reviewer_a", "second_reviewer_id": "reviewer_b",
            "second_review_date": "2026-10-28", "second_review_decision": "APPROVED",
            "leakage_check": "PASS", "split": "TRAIN", "decision": "ACCEPTED_ADDITIONAL",
        }
        self.write_csv(self.root / "data/intake/manifest.csv", [self.manifest])
        self.write_csv(self.root / "data/intake/contract_unit_review_queue.csv", [self.unit])
        self.write_csv(self.processed / "clauses_v06.csv", [{
            "contract_id": self.unit_id, "clause_id": "SIGNED-U01_C01",
            "section_title": "Điều 1", "clause_text": self.safe_text,
            "clause_type": "OTHER", "start_offset": "0",
            "end_offset": str(len(self.safe_text)), "offset_quality": "EXACT",
        }])

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def write_csv(path, rows):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def export(self):
        return build_payload(self.unit_id, processed=self.processed, root=self.root)

    def test_approved_export_reads_only_sha_verified_redacted_derivative(self):
        payload = self.export()
        self.assertEqual(payload["raw_text"], self.safe_text)
        self.assertNotIn(self.canary, str(payload))
        self.assertEqual(payload["clauses"][0]["highlight_text"], self.safe_text)

    def test_approved_html_embeds_only_reviewed_text_and_no_private_canary(self):
        from scripts.build_highlight_preview import build_preview

        output = self.root / "data/intake/private/preview.html"
        build_preview(self.unit_id, output, root=self.root)
        html = output.read_text(encoding="utf-8")
        self.assertIn(self.safe_text, html)
        self.assertNotIn(self.canary, html)

    def test_pending_intake_is_rejected_even_if_raw_text_exists(self):
        self.unit["decision"] = "HOLD"
        self.write_csv(self.root / "data/intake/contract_unit_review_queue.csv", [self.unit])
        with self.assertRaisesRegex(ValueError, "not accepted"):
            self.export()

    def test_modified_redacted_derivative_fails_closed(self):
        self.derivative.write_text(self.safe_text + self.canary, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "intake gate"):
            self.export()

    def test_unreviewed_development_fixture_requires_explicit_mode(self):
        with self.assertRaisesRegex(ValueError, "not accepted"):
            build_payload("HDLD003")


if __name__ == "__main__":
    unittest.main()
