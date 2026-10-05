import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HighlightPreviewTests(unittest.TestCase):
    def test_generates_self_contained_preview_from_the_exported_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "HDLD003.html"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_highlight_preview.py"),
                    "HDLD003",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            match = re.search(
                r'<script id="contract-payload" type="application/json">(.*?)</script>',
                html,
                re.DOTALL,
            )
            self.assertIsNotNone(match)
            payload = json.loads(match.group(1))
            self.assertEqual(payload["contract_id"], "HDLD003")
            self.assertEqual(len(payload["clauses"]), 61)
            clauses = {row["clause_id"]: row for row in payload["clauses"]}
            self.assertEqual(clauses["HDLD003_C018"]["highlight_text"], "các loại bảo hiểm")
            self.assertEqual(clauses["HDLD003_C018A"]["highlight_text"], "các khoản thuế")


if __name__ == "__main__":
    unittest.main()
