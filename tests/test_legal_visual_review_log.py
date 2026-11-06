import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class LegalVisualReviewLogTests(unittest.TestCase):
    def test_visual_log_rows_match_receipted_pdf_hash_and_page_bounds(self):
        receipts = read_csv(ROOT / "data/intake/legal_ocr_candidate_receipts_2026-11-02.csv")
        sources = {row["source_id"]: row for row in receipts}
        log = read_csv(ROOT / "data/intake/legal_ocr_visual_review_log_2026-11-02.csv")

        seen: set[tuple[str, int]] = set()
        for row in log:
            source_id = row["source_id"]
            self.assertIn(source_id, sources)
            source = sources[source_id]
            self.assertEqual(row["source_sha256"], source["source_sha256"], source_id)

            page = int(row["pdf_page"])
            key = (source_id, page)
            self.assertNotIn(key, seen)
            seen.add(key)
            self.assertGreaterEqual(page, 1)
            self.assertLessEqual(page, int(source["source_pages"]))


if __name__ == "__main__":
    unittest.main()
