import importlib
import importlib.util
import unittest


class LegalOcrStructureIndexTests(unittest.TestCase):
    def queue_module(self):
        self.assertIsNotNone(
            importlib.util.find_spec("scripts.build_legal_ocr_structure_index"),
            "legal OCR structure index builder is missing",
        )
        return importlib.import_module("scripts.build_legal_ocr_structure_index")

    def candidate(self, pages):
        content = [
            "STATUS: OCR_CANDIDATE_UNPROOFREAD",
            "SOURCE_SHA256: " + "a" * 64,
            f"PAGE_COUNT: {len(pages)}",
            "",
        ]
        for number, page in enumerate(pages, 1):
            content.extend((f"===== PDF_PAGE {number:03d} | OCR_CANDIDATE =====", page, ""))
        return "\n".join(content)

    def test_builds_document_article_clause_point_hierarchy_with_page_refs(self):
        builder = self.queue_module()
        candidate = self.candidate([
            "Điều 1. Scope\n1. Clause one\na) Point a\nb) Point b",
            "Continuation\n2. Clause two\nĐiều 2. Other\n1. Clause one",
        ])

        rows = builder.build_structure_index(
            candidate,
            document_id="LAW-BLLD-VBHN-18-2026",
            document_number="18/VBHN-VPQH",
            article_count=3,
        )

        by_id = {row["node_id"]: row for row in rows}
        self.assertEqual(len(rows), 9)
        self.assertEqual(by_id["LAW-BLLD-VBHN-18-2026:art:1"]["source_pages"], "1;2")
        self.assertEqual(
            by_id["LAW-BLLD-VBHN-18-2026:art:1:clause:1"]["parent_id"],
            "LAW-BLLD-VBHN-18-2026:art:1",
        )
        self.assertEqual(
            by_id["LAW-BLLD-VBHN-18-2026:art:1:clause:1:point:a"]["parent_id"],
            "LAW-BLLD-VBHN-18-2026:art:1:clause:1",
        )
        self.assertEqual(
            by_id["LAW-BLLD-VBHN-18-2026:art:1:clause:2"]["source_pages"],
            "2",
        )
        self.assertEqual(
            by_id["LAW-BLLD-VBHN-18-2026:art:3"]["structure_evidence"],
            "OCR_ARTICLE_NOT_DETECTED; MANUAL_SEARCH_REQUIRED",
        )
        self.assertTrue(all(row["legal_review_status"] == "PENDING_LEGAL_REVIEW" for row in rows))
        self.assertTrue(all("text" not in row for row in rows))

    def test_duplicate_article_headings_are_reported_and_longest_body_is_parsed(self):
        builder = self.queue_module()
        candidate = self.candidate([
            "Mục lục\nĐiều 1. Scope\nĐiều 2. Other",
            "Điều 1. Scope\n1. Full clause\na) Full point\nĐiều 2. Other",
        ])

        rows = builder.build_structure_index(
            candidate,
            document_id="LAW-X",
            document_number="X/1",
            article_count=2,
        )
        by_id = {row["node_id"]: row for row in rows}

        self.assertEqual(by_id["LAW-X:art:1"]["occurrence_count"], "2")
        self.assertEqual(by_id["LAW-X:art:1"]["source_pages"], "2")
        self.assertIn("LAW-X:art:1:clause:1", by_id)
        self.assertIn("LAW-X:art:1:clause:1:point:a", by_id)

    def test_accepts_utf8_bom_from_real_ocr_candidate_files(self):
        builder = self.queue_module()
        candidate = "\ufeff" + self.candidate(["Điều 1. Scope\n1. Clause"])
        candidate = candidate.replace(
            "SOURCE_SHA256: " + "a" * 64 + "\nPAGE_COUNT:",
            "SOURCE_FILE: fixture.pdf\nSOURCE_SHA256: " + "a" * 64
            + "\nOCR_ENGINE: Tesseract\nPAGE_COUNT:",
        )
        rows = builder.build_structure_index(
            candidate,
            document_id="LAW-X",
            document_number="X/1",
            article_count=1,
        )
        self.assertEqual(len(rows), 3)

    def test_does_not_treat_article_citation_as_a_heading(self):
        builder = self.queue_module()
        candidate = self.candidate([
            "Điều 1. Scope\n1. Clause\nĐiều 2 của Bộ luật này được áp dụng...",
        ])
        rows = builder.build_structure_index(
            candidate,
            document_id="LAW-X",
            document_number="X/1",
            article_count=2,
        )
        by_id = {row["node_id"]: row for row in rows}
        article_two = by_id["LAW-X:art:2"]
        self.assertEqual(article_two["occurrence_count"], "0")
        self.assertEqual(
            article_two["structure_evidence"],
            "OCR_ARTICLE_NOT_DETECTED; MANUAL_SEARCH_REQUIRED",
        )

    def test_accepts_common_ocr_variants_for_vietnamese_d_article_heading(self):
        builder = self.queue_module()
        candidate = self.candidate([
            "Ñ Điều 1. OCR prefix variant\n1. Clause",
            "Điều 2. Heading\n2. Clause",
            "Điều 3 của Bộ luật này is a citation, not a heading",
        ])
        rows = builder.build_structure_index(
            candidate,
            document_id="LAW-X",
            document_number="X/1",
            article_count=3,
        )
        articles = [row for row in rows if row["node_type"] == "article"]
        self.assertEqual([row["occurrence_count"] for row in articles], ["1", "1", "0"])


if __name__ == "__main__":
    unittest.main()
