"""Structural admission checks for source-authorized signed contract units."""

import hashlib
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfWriter

from scripts.validate_intake_gate import evaluate_units, load_csv


class IntakeGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.add_blank_page(width=612, height=792)
        with (self.root / "original.pdf").open("wb") as handle:
            writer.write(handle)
        (self.root / "safe.pdf").write_bytes(b"redacted-derivative")
        (self.root / "data/intake/restricted").mkdir(parents=True)
        (self.root / "data/intake/restricted/authorization.txt").write_text(
            "permission", encoding="utf-8")
        self.manifest = [{
            "candidate_id": "CAND1", "local_path": "original.pdf",
            "sha256": self.hash_file("original.pdf"),
            "bytes": str((self.root / "original.pdf").stat().st_size),
            "t1_eligible": "yes",
        }]
        self.unit = {
            "unit_id": "CAND1_U01", "candidate_id": "CAND1", "source_pages": "1-2",
            "signed_check": "VERIFIED", "similarity_group": "GROUP1",
            "distinct_document_check": "PASS", "template_independence_check": "PASS",
            "rights_authority_check": "VERIFIED",
            "rights_evidence_path": "data/intake/restricted/authorization.txt",
            "rights_store_process": "GRANTED", "rights_share_internal": "GRANTED",
            "rights_eval_derivative": "GRANTED", "visual_redaction": "PASS",
            "text_redaction": "PASS", "metadata_redaction": "PASS",
            "derivative_path": "safe.pdf", "derivative_sha256": self.hash_file("safe.pdf"),
            "prepared_by_id": "researcher1", "second_reviewer_id": "reviewer2",
            "second_review_date": "2026-10-28", "second_review_decision": "APPROVED",
            "leakage_check": "PASS", "split": "T1", "decision": "ACCEPTED_T1",
        }

    def hash_file(self, name):
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def test_admits_evidenced_signed_unit_only(self):
        errors, summary = evaluate_units(self.manifest, [self.unit], self.root)
        self.assertEqual([], errors)
        self.assertEqual(1, summary["accepted_t1"])

    def test_denies_unsupported_permission_and_self_review(self):
        claimed = dict(self.unit, rights_share_internal="PENDING",
                       second_reviewer_id="researcher1")
        errors, summary = evaluate_units(self.manifest, [claimed], self.root)
        self.assertTrue(any("rights_share_internal" in x for x in errors))
        self.assertTrue(any("independent reviewer" in x for x in errors))
        self.assertEqual(0, summary["accepted_t1"])

    def test_denies_broken_source_and_derivative_provenance(self):
        claimed = dict(self.unit, derivative_sha256="0" * 64)
        self.manifest[0]["sha256"] = "f" * 64
        errors, summary = evaluate_units(self.manifest, [claimed], self.root)
        self.assertTrue(any("source hash" in x for x in errors))
        self.assertTrue(any("derivative hash" in x for x in errors))
        self.assertEqual(0, summary["accepted_t1"])

    def test_denies_shared_family_in_different_splits(self):
        other = dict(self.unit, unit_id="CAND1_U02", decision="ACCEPTED_ADDITIONAL",
                     split="TRAIN")
        errors, summary = evaluate_units(self.manifest, [self.unit, other], self.root)
        self.assertTrue(any("crosses dataset splits" in x for x in errors))
        self.assertEqual(0, summary["accepted_t1"])

    def test_denies_claimed_unit_outside_source_pdf(self):
        claimed = dict(self.unit, source_pages="2-3")
        errors, summary = evaluate_units(self.manifest, [claimed], self.root)
        self.assertTrue(any("source_pages exceed" in x for x in errors), errors)
        self.assertEqual(0, summary["accepted_t1"])

    def test_denies_overlapping_source_spans_even_if_one_is_on_hold(self):
        pending = dict(self.unit, unit_id="CAND1_U02", source_pages="2-2",
                       decision="HOLD")
        errors, summary = evaluate_units(self.manifest, [self.unit, pending], self.root)
        self.assertTrue(any("overlapping source_pages" in x for x in errors), errors)
        self.assertEqual(0, summary["accepted_t1"])

    def test_denies_unredacted_original_reused_as_derivative(self):
        claimed = dict(self.unit, derivative_path="original.pdf",
                       derivative_sha256=self.hash_file("original.pdf"))
        errors, summary = evaluate_units(self.manifest, [claimed], self.root)
        self.assertTrue(any("distinct from source" in x for x in errors), errors)
        self.assertEqual(0, summary["accepted_t1"])

    def test_denies_rights_evidence_outside_restricted_area(self):
        claimed = dict(self.unit, rights_evidence_path="authorization_public.txt")
        (self.root / "authorization_public.txt").write_text("permission", encoding="utf-8")
        errors, summary = evaluate_units(self.manifest, [claimed], self.root)
        self.assertTrue(any("restricted location" in x for x in errors), errors)
        self.assertEqual(0, summary["accepted_t1"])

    def test_reconciles_actual_pending_queue_without_accepting_any(self):
        root = Path(__file__).resolve().parents[1]
        manifest = load_csv(root / "data/intake/manifest.csv")
        units = load_csv(root / "data/intake/contract_unit_review_queue.csv")
        errors, summary = evaluate_units(manifest, units, root)
        self.assertEqual([], errors)
        self.assertEqual(10, summary["screened_units"])
        self.assertEqual(0, summary["accepted_t1"])
        self.assertEqual(0, summary["accepted_additional"])


if __name__ == "__main__":
    unittest.main()
