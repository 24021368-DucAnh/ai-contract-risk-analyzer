import unittest

from scripts.build_legal_corpus_review_queue import build_review_queue

SOURCE_HASH = "a" * 64


class LegalCorpusReviewQueueTests(unittest.TestCase):
    def setUp(self):
        self.ocr = (
            f"SOURCE_SHA256: {SOURCE_HASH}\n"
            "===== PDF_PAGE 001 | OCR_CANDIDATE =====\n"
            "Điều 13. Hợp đồng lao động\n"
            "1. Hợp đồng lao động là sự thỏa thuận.\n"
            "===== PDF_PAGE 002 | OCR_CANDIDATE =====\n"
            "Điều 14. Hình thức hợp đồng lao động\n"
            "Hợp đồng phải được giao kết bằng văn bản.\n"
        )
        self.provisions = [
            {
                "document_id": "BLLD2019",
                "citation_id": "BLLD2019:art13:cl1",
                "article": "13",
                "content": "1. Hợp đồng lao động là sự thỏa thuận.",
            },
            {
                "document_id": "BLLD2019",
                "citation_id": "BLLD2019:art14:cl1",
                "article": "14",
                "content": "Hợp đồng phải được giao kết bằng văn bản có chứng thực.",
            },
        ]

    def test_builds_pii_free_pending_review_rows_with_source_pages_and_text_match(self):
        rows = build_review_queue(self.provisions, self.ocr)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["ocr_article_pages"], "1")
        self.assertEqual(rows[0]["text_match_status"], "OCR_EXACT_NORMALIZED")
        self.assertEqual(rows[1]["ocr_article_pages"], "2")
        self.assertEqual(rows[1]["text_match_status"], "NO_EXACT_OCR_MATCH")
        self.assertEqual(rows[0]["source_sha256"], SOURCE_HASH)
        self.assertEqual(rows[0]["review_status"], "PENDING_VISUAL_LEGAL_REVIEW")
        self.assertEqual(rows[0]["verbatim_text_verified"], "NO")
        self.assertFalse(any("content" in key for key in rows[0]))
        self.assertFalse(any(self.provisions[0]["content"] in value for value in rows[0].values()))

    def test_rejects_duplicate_citation_ids(self):
        duplicate = self.provisions + [dict(self.provisions[0])]

        with self.assertRaisesRegex(ValueError, "duplicate citation_id"):
            build_review_queue(duplicate, self.ocr)

    def test_requires_source_hash_in_ocr_receipt(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_SHA256"):
            build_review_queue(self.provisions, self.ocr.replace(f"SOURCE_SHA256: {SOURCE_HASH}\n", ""))


if __name__ == "__main__":
    unittest.main()
