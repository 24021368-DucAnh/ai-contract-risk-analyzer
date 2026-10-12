import csv
import unittest
from pathlib import Path

from scripts.build_provisional_split import build_manifest, load_current_data


ROOT = Path(__file__).resolve().parents[1]


class ProvisionalSplitTests(unittest.TestCase):
    def test_v06_covers_new_group_without_split_leakage(self):
        rows, metadata = load_current_data(ROOT, dataset_version="v06")
        manifest = build_manifest(rows, metadata, dataset_version="v06")
        self.assertEqual(manifest["dataset"], "data/processed/clauses_v06.csv")
        self.assertEqual(manifest["splits"]["train"]["contracts"], ["HDLD003", "HDLD005"])
        self.assertEqual(manifest["splits"]["dev"]["contracts"], ["HDLD001", "HDLD002"])
        self.assertEqual(manifest["splits"]["test"]["contracts"], ["HDLD004"])
        self.assertEqual(sum(part["clause_count"] for part in manifest["splits"].values()), 234)
        self.assertEqual(manifest["overall_class_counts"]["WORKING_CONDITIONS"], 7)

    def test_v06_excludes_close_template_paraphrases_from_scoring(self):
        rows, metadata = load_current_data(ROOT, dataset_version="v06")
        manifest = build_manifest(rows, metadata, dataset_version="v06")
        excluded = {item["clause_id"] for item in manifest["exclusions"]}

        self.assertTrue({
            "HDLD001_C005", "HDLD001_C015", "HDLD001_C016",
            "HDLD002_C005", "HDLD002_C016", "HDLD002_C017",
            "HDLD004_C011", "HDLD004_C016",
        }.issubset(excluded))

    def test_keeps_template_groups_together_and_covers_all_reviewed_rows(self):
        rows, metadata = load_current_data(ROOT, dataset_version="v05")
        manifest = build_manifest(rows, metadata, dataset_version="v05")

        self.assertEqual(manifest["status"], "PROVISIONAL")
        self.assertEqual(manifest["splits"]["train"]["contracts"], ["HDLD003"])
        self.assertEqual(manifest["splits"]["dev"]["contracts"], ["HDLD001", "HDLD002"])
        self.assertEqual(manifest["splits"]["test"]["contracts"], ["HDLD004"])
        self.assertEqual(sum(part["clause_count"] for part in manifest["splits"].values()), 183)
        self.assertEqual(manifest["splits"]["dev"]["scorable_clause_count"], 55)
        self.assertEqual(manifest["splits"]["test"]["scorable_clause_count"], 43)
        self.assertEqual(manifest["overall_class_counts"]["WORKING_CONDITIONS"], 6)
        self.assertEqual(manifest["priority_labels_under_10"], [
            "WORKING_CONDITIONS", "CONTRACT_TERM", "WORKING_TIME"
        ])

    def test_excludes_exact_and_near_train_overlap_from_dev_scoring(self):
        rows = [
            self.row("B1", "HDLD003", "Điều khoản về thời gian làm việc và nghỉ ngơi rõ ràng."),
            self.row("A1", "HDLD001", "Điều khoản về thời gian làm việc và nghỉ ngơi rõ ràng."),
            self.row("A2", "HDLD002", "Điều khoản về thời gian làm việc và nghỉ ngơi rất rõ ràng."),
            self.row("C1", "HDLD004", "Người lao động được nhận công cụ phục vụ công việc."),
        ]
        metadata = {
            "HDLD001": self.meta("HDLD001", "SIM_A"),
            "HDLD002": self.meta("HDLD002", "SIM_A"),
            "HDLD003": self.meta("HDLD003", "SIM_B"),
            "HDLD004": self.meta("HDLD004", "SIM_C"),
        }

        manifest = build_manifest(rows, metadata, dataset_version="v05")
        exclusions = {item["clause_id"]: item for item in manifest["exclusions"]}

        self.assertEqual(set(exclusions), {"A1", "A2"})
        self.assertEqual(exclusions["A1"]["reason"], "EXACT_CROSS_SPLIT")
        self.assertEqual(exclusions["A2"]["reason"], "NEAR_CROSS_SPLIT")
        self.assertEqual(manifest["splits"]["dev"]["scorable_clause_count"], 0)
        self.assertEqual(manifest["splits"]["test"]["scorable_clause_count"], 1)

    def test_rejects_unknown_or_mixed_group_assignments(self):
        rows = [self.row("X1", "HDLD001", "Nội dung hợp đồng.")]
        metadata = {"HDLD001": self.meta("HDLD001", "SIM_UNKNOWN")}

        with self.assertRaisesRegex(ValueError, "unassigned similarity group"):
            build_manifest(rows, metadata, dataset_version="v05")

    @staticmethod
    def row(clause_id, contract_id, text):
        return {
            "clause_id": clause_id,
            "contract_id": contract_id,
            "clause_text": text,
            "clause_type": "WORKING_TIME",
            "annotation_status": "REVIEWED",
            "offset_quality": "EXACT",
        }

    @staticmethod
    def meta(contract_id, similarity_group):
        return {
            "contract_id": contract_id,
            "similarity_group": similarity_group,
            "dataset_status": "ANNOTATED",
        }


if __name__ == "__main__":
    unittest.main()
