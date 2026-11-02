import sys
import unittest

import scripts.ocr_legal_candidate as ocr
from scripts.ocr_legal_candidate import (
    format_candidate,
)


class LegalOcrCandidateTests(unittest.TestCase):
    def test_candidate_labels_every_page_and_unproofread_status(self):
        result = format_candidate("law.pdf", "a" * 64, ["page one", "page two"])

        self.assertIn("STATUS: OCR_CANDIDATE_UNPROOFREAD", result)
        self.assertIn("SOURCE_SHA256: " + "a" * 64, result)
        self.assertIn("===== PDF_PAGE 001 | OCR_CANDIDATE =====", result)
        self.assertIn("===== PDF_PAGE 002 | OCR_CANDIDATE =====", result)
        self.assertIn("Every page and character requires visual comparison", result)

    def test_empty_page_is_still_explicitly_numbered(self):
        result = format_candidate("law.pdf", "b" * 64, [""])

        self.assertIn("===== PDF_PAGE 001 | OCR_CANDIDATE =====", result)
        self.assertIn("PAGE_COUNT: 1", result)

    def test_external_utf8_output_preserves_vietnamese_characters(self):
        result = ocr._run([
            sys.executable,
            "-c",
            "import sys; sys.stdout.buffer.write('Tiếng Việt'.encode('utf-8'))",
        ])

        self.assertEqual(result, "Tiếng Việt")

    def test_checkpoint_resumes_only_when_source_and_ocr_settings_match(self):
        self.assertTrue(
            hasattr(ocr, "make_checkpoint") and hasattr(ocr, "checkpoint_pages"),
            "resumable checkpoint helpers are missing",
        )
        metadata = {
            "source_sha256": "a" * 64,
            "tessdata_sha256": "b" * 64,
            "page_count": 3,
            "scale_to": 2200,
            "engine": "tesseract-5.4.0/vie/psm3",
        }
        checkpoint = ocr.make_checkpoint(metadata, {"1": "synthetic page"})

        self.assertEqual(ocr.checkpoint_pages(checkpoint, metadata), {1: "synthetic page"})

        changed_source = dict(metadata, source_sha256="c" * 64)
        with self.assertRaisesRegex(ValueError, "metadata mismatch"):
            ocr.checkpoint_pages(checkpoint, changed_source)

    def test_checkpoint_rejects_out_of_range_or_non_text_pages(self):
        self.assertTrue(
            hasattr(ocr, "make_checkpoint") and hasattr(ocr, "checkpoint_pages"),
            "resumable checkpoint helpers are missing",
        )
        metadata = {
            "source_sha256": "a" * 64,
            "tessdata_sha256": "b" * 64,
            "page_count": 2,
            "scale_to": 2200,
            "engine": "tesseract-5.4.0/vie/psm3",
        }
        with self.assertRaisesRegex(ValueError, "invalid page entries"):
            ocr.checkpoint_pages(ocr.make_checkpoint(metadata, {"3": "outside"}), metadata)
        with self.assertRaisesRegex(ValueError, "invalid page entries"):
            ocr.checkpoint_pages(ocr.make_checkpoint(metadata, {"1": 1}), metadata)


if __name__ == "__main__":
    unittest.main()
