"""Build a provisional, contract-grouped split for a reviewed clause snapshot."""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GROUP_ASSIGNMENTS = {
    "v05": {"train": ("SIM_B",), "dev": ("SIM_A",), "test": ("SIM_C",)},
    "v06": {"train": ("SIM_B", "SIM_D"), "dev": ("SIM_A",), "test": ("SIM_C",)},
}
# Keep the historical v05 split reproducible; v06 uses stricter leakage QC.
NEAR_THRESHOLDS = {"v05": 0.90, "v06": 0.85}
MIN_NEAR_LENGTH = 30
MIN_LENGTH_RATIO = 0.85


def load_current_data(root: Path = ROOT, dataset_version: str = "v06") -> tuple[list[dict], dict[str, dict]]:
    if dataset_version not in GROUP_ASSIGNMENTS:
        raise ValueError(f"unsupported dataset version: {dataset_version}")
    with (root / f"data/processed/clauses_{dataset_version}.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    with (root / "data/contracts_metadata.csv").open(encoding="utf-8-sig", newline="") as handle:
        metadata = {row["contract_id"]: row for row in csv.DictReader(handle)}
    return rows, metadata


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def overlap_reason(left: str, right: str, min_similarity: float) -> tuple[str, float] | None:
    if left == right:
        return "EXACT_CROSS_SPLIT", 1.0
    if min(len(left), len(right)) < MIN_NEAR_LENGTH:
        return None
    if min(len(left), len(right)) / max(len(left), len(right)) < MIN_LENGTH_RATIO:
        return None
    similarity = SequenceMatcher(None, left, right, autojunk=False).ratio()
    if similarity >= min_similarity:
        return "NEAR_CROSS_SPLIT", round(similarity, 3)
    return None


def build_manifest(rows: list[dict], metadata: dict[str, dict], dataset_version: str = "v06") -> dict:
    if dataset_version not in GROUP_ASSIGNMENTS:
        raise ValueError(f"unsupported dataset version: {dataset_version}")
    assignments = GROUP_ASSIGNMENTS[dataset_version]
    near_threshold = NEAR_THRESHOLDS[dataset_version]
    group_to_split = {
        group: split for split, groups in assignments.items() for group in groups
    }
    seen_ids = set()
    grouped_rows = {split: [] for split in assignments}
    for row in rows:
        clause_id = row["clause_id"]
        if clause_id in seen_ids:
            raise ValueError(f"duplicate clause_id: {clause_id}")
        seen_ids.add(clause_id)
        contract_id = row["contract_id"]
        contract = metadata.get(contract_id)
        if contract is None or contract.get("dataset_status") != "ANNOTATED":
            raise ValueError(f"missing annotated contract metadata: {contract_id}")
        if row["annotation_status"] != "REVIEWED":
            raise ValueError(f"unreviewed clause: {clause_id}")
        group = contract["similarity_group"]
        if group not in group_to_split:
            raise ValueError(f"unassigned similarity group: {group}")
        grouped_rows[group_to_split[group]].append(row)

    exclusions = []
    earlier_rows = []
    for split, split_rows in grouped_rows.items():
        if split != "train":
            for row in split_rows:
                current_text = normalized(row["clause_text"])
                matches = []
                for earlier in earlier_rows:
                    match = overlap_reason(
                        current_text, normalized(earlier["clause_text"]), near_threshold
                    )
                    if match:
                        matches.append((earlier["clause_id"], *match))
                if matches:
                    exact = [match for match in matches if match[1] == "EXACT_CROSS_SPLIT"]
                    chosen = exact or matches
                    exclusions.append({
                        "clause_id": row["clause_id"],
                        "split": split,
                        "reason": chosen[0][1],
                        "matched_clause_ids": sorted(match[0] for match in chosen),
                        "max_similarity": max(match[2] for match in chosen),
                    })
        earlier_rows.extend(split_rows)

    excluded_ids = {item["clause_id"] for item in exclusions}
    overall_counts = Counter(row["clause_type"] for row in rows)
    splits = {}
    for split, split_rows in grouped_rows.items():
        active = [row for row in split_rows if row["clause_id"] not in excluded_ids]
        splits[split] = {
            "contracts": sorted({row["contract_id"] for row in split_rows}),
            "similarity_groups": list(assignments[split]),
            "clause_count": len(split_rows),
            "scorable_clause_count": len(active),
            "exact_span_scorable_count": sum(row["offset_quality"] == "EXACT" for row in active),
            "excluded_clause_ids": sorted(row["clause_id"] for row in split_rows if row["clause_id"] in excluded_ids),
            "class_counts": dict(sorted(Counter(row["clause_type"] for row in split_rows).items())),
            "scorable_class_counts": dict(sorted(Counter(row["clause_type"] for row in active).items())),
        }
    return {
        "schema_version": 1,
        "status": "PROVISIONAL",
        "dataset": f"data/processed/clauses_{dataset_version}.csv",
        "method": "whole-contract similarity_group assignment",
        "near_duplicate_rule": {
            "normalized_text": "casefold and collapsed whitespace",
            "min_similarity": near_threshold,
            "min_length": MIN_NEAR_LENGTH,
            "min_length_ratio": MIN_LENGTH_RATIO,
        },
        "splits": splits,
        "exclusions": exclusions,
        "overall_class_counts": dict(sorted(overall_counts.items())),
        "priority_labels_under_10": [
            label for label, count in sorted(overall_counts.items(), key=lambda item: (item[1], item[0]))
            if count < 10
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-version", choices=tuple(GROUP_ASSIGNMENTS), default="v06")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows, metadata = load_current_data(dataset_version=args.dataset_version)
    manifest = build_manifest(rows, metadata, dataset_version=args.dataset_version)
    dataset_bytes = (ROOT / manifest["dataset"]).read_bytes()
    manifest["dataset_sha256"] = hashlib.sha256(dataset_bytes).hexdigest()
    output = args.output or ROOT / f"data/splits/provisional_{args.dataset_version}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
