import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HighlightPayloadTests(unittest.TestCase):
    def test_exports_newly_annotated_hdld005(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "export_highlight_payload.py"), "HDLD005"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertGreaterEqual(len(payload["clauses"]), 45)
        self.assertEqual({row["offset_quality"] for row in payload["clauses"]}, {"EXACT"})

    def test_exports_original_text_and_distinct_clause_highlights(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "export_highlight_payload.py"), "HDLD003"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["contract_id"], "HDLD003")
        self.assertEqual(
            payload["raw_text"],
            (ROOT / "data" / "processed" / "raw_text" / "HDLD003.txt").read_text(encoding="utf-8"),
        )
        self.assertEqual(len(payload["clauses"]), 61)
        clauses = {row["clause_id"]: row for row in payload["clauses"]}
        self.assertEqual(clauses["HDLD003_C018"]["highlight_text"], "các loại bảo hiểm")
        self.assertEqual(clauses["HDLD003_C018A"]["highlight_text"], "các khoản thuế")
        for row in payload["clauses"]:
            self.assertEqual(
                payload["raw_text"][row["start_offset"]:row["end_offset"]],
                row["highlight_text"],
            )


if __name__ == "__main__":
    unittest.main()
