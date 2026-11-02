import importlib
import importlib.util
import unittest


class LegalArticleReviewQueueTests(unittest.TestCase):
    def queue_module(self):
        self.assertIsNotNone(
            importlib.util.find_spec("scripts.build_legal_article_review_queue"),
            "legal article review queue module is missing",
        )
        return importlib.import_module("scripts.build_legal_article_review_queue")

    def test_builds_complete_queue_and_tracks_duplicate_heading_pages(self):
        queue = self.queue_module()
        rows = queue.build_review_rows(
            ["Điều 1. Một\nĐiều 2. Hai", "Điều 2. Hai lần nữa"],
            article_count=3,
            source_sha256="a" * 64,
        )

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["article_no"], "1")
        self.assertEqual(rows[0]["occurrence_count"], "1")
        self.assertEqual(rows[0]["pages"], "1")
        self.assertEqual(rows[1]["occurrence_count"], "2")
        self.assertEqual(rows[1]["pages"], "1;2")
        self.assertEqual(rows[2]["detection_status"], "NOT_DETECTED_BY_OCR")
        self.assertTrue(all(row["review_status"] == "PENDING_VISUAL_REVIEW" for row in rows))

    def test_parser_requires_ordered_page_markers_and_ocr_only_status(self):
        candidate = (
            "STATUS: OCR_CANDIDATE_UNPROOFREAD\n"
            + "SOURCE_SHA256: " + "b" * 64 + "\n"
            + "PAGE_COUNT: 2\n"
            + "===== PDF_PAGE 001 | OCR_CANDIDATE =====\nĐiều 1. Một\n"
            + "===== PDF_PAGE 002 | OCR_CANDIDATE =====\nĐiều 2. Hai\n"
        )

        queue = self.queue_module()
        source_hash, pages = queue.parse_ocr_candidate(candidate)

        self.assertEqual(source_hash, "b" * 64)
        self.assertEqual(len(pages), 2)
        self.assertIn("Điều 2", pages[1])
        with self.assertRaisesRegex(ValueError, "ordered page markers"):
            queue.parse_ocr_candidate(candidate.replace("PDF_PAGE 002", "PDF_PAGE 003"))
        with self.assertRaisesRegex(ValueError, "unproofread OCR candidate"):
            queue.parse_ocr_candidate(candidate.replace("OCR_CANDIDATE_UNPROOFREAD", "APPROVED"))

    def test_rejects_invalid_article_count_or_hash(self):
        queue = self.queue_module()
        for invalid_count in (0, True, 1.5):
            with self.assertRaisesRegex(ValueError, "article_count"):
                queue.build_review_rows(["Điều 1"], invalid_count, "c" * 64)
        with self.assertRaisesRegex(ValueError, "source SHA-256"):
            queue.build_review_rows(["Điều 1"], 1, "not-a-hash")


if __name__ == "__main__":
    unittest.main()
