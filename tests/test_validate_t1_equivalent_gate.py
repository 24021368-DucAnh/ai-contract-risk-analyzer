"""The composite receipt must remain distinct from original BRD intake."""

import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate_t1_equivalent_gate import validate


class EquivalentGateTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        if not (root / "data/intake/restricted/T1_segmentation_gold_v01/manifest.json").is_file():
            self.skipTest("restricted local Gold is unavailable")

    def test_owner_attested_composite_and_original_gate_are_separate(self):
        result = validate()
        self.assertEqual(result["accepted_equivalent"], 10)
        self.assertEqual(result["mode_counts"], {
            "PUBLIC_TEMPLATE_VERIFIED": 5,
            "REAL_EXECUTED_RESTRICTED": 4,
            "SYNTHETIC_CALIBRATION_CONTROL": 1,
        })
        self.assertEqual(result["original_brd_accepted"], 0)
        self.assertEqual(len(result["slice_unique_8"]), 8)
        self.assertEqual(len(result["slice_t1_real_9"]), 9)

    def test_source_tamper_fails_closed(self):
        from scripts import validate_t1_equivalent_gate as gate

        real_digest = gate.digest

        def changed_digest(path):
            if path.name == "HDLD014.txt":
                return "0" * 64
            return real_digest(path)

        with patch.object(gate, "digest", side_effect=changed_digest):
            with self.assertRaisesRegex(ValueError, "source hash mismatch"):
                gate.validate()


if __name__ == "__main__":
    unittest.main()
