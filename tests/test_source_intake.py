import csv
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SourceIntakeTests(unittest.TestCase):
    def test_local_hdld007_is_an_unannotated_template_without_filled_cccd(self):
        source = ROOT / "data" / "raw" / "contracts" / "HDLD007.docx"
        raw_path = ROOT / "data" / "processed" / "raw_text" / "HDLD007.txt"
        if not source.exists() and not raw_path.exists():
            self.skipTest("HDLD007 content stays local pending redistribution permission")
        self.assertTrue(zipfile.is_zipfile(source))
        text = raw_path.read_text(encoding="utf-8")
        self.assertNotIn("\r", text)
        self.assertFalse(text.endswith("\n"))
        self.assertGreater(len(text), 4500)
        for number in range(1, 10):
            self.assertRegex(text, rf"ĐIỀU {number}:|Điều {number}:")
        self.assertNotRegex(text, r"\b\d{12}\b")  # no filled CCCD

    def test_hdld007_provenance_is_registered_without_entering_the_dataset(self):
        with (ROOT / "data" / "contracts_metadata.csv").open(encoding="utf-8-sig", newline="") as handle:
            metadata = {row["contract_id"]: row for row in csv.DictReader(handle)}
        row = metadata["HDLD007"]
        self.assertEqual(row["dataset_status"], "TO_ANNOTATE")
        self.assertEqual(row["similarity_group"], "SIM_E")
        self.assertEqual(row["clause_count"], "")
        self.assertEqual(row["dataset_version"], "")
        self.assertIn("HDLD007", (ROOT / "docs" / "data_sources.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
