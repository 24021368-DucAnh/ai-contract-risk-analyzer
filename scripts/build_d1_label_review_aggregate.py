"""Create a PII-free count-only guide for independent D1 label review."""

import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D1_IDS = frozenset({"HDLD001", "HDLD002", "HDLD003", "HDLD004"})


def build_aggregate(rows: list[dict[str, str]], source_sha256: str) -> dict:
    by_contract: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    by_label: collections.Counter = collections.Counter()
    offsets: collections.Counter = collections.Counter()
    seen: set[str] = set()
    total = 0
    for row in rows:
        if row.get("contract_id") not in D1_IDS or row.get("annotation_status") != "REVIEWED":
            continue
        cid = row.get("clause_id", "")
        if not cid or cid in seen:
            raise ValueError("D1 source has missing or duplicate clause IDs")
        seen.add(cid)
        label, quality = row.get("clause_type", ""), row.get("offset_quality", "")
        if not label or quality not in {"EXACT", "CONTEXT"}:
            raise ValueError("D1 source contains invalid label or offset quality")
        by_contract[row["contract_id"]][label] += 1
        by_label[label] += 1
        offsets[quality] += 1
        total += 1
    return {
        "status": "AGGREGATE_REVIEW_GUIDE_NOT_GOLD",
        "source_sha256": source_sha256,
        "taxonomy_version": "clause_taxonomy_v03",
        "scope": "D1 HDLD001-004; counts only; no text or inferred correctness",
        "total_reviewed_rows": total,
        "by_contract": {key: dict(sorted(value.items())) for key, value in sorted(by_contract.items())},
        "by_label": dict(sorted(by_label.items())),
        "offset_quality": dict(sorted(offsets.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clauses", type=Path, default=ROOT / "data/processed/clauses_v06.csv")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {args.output}")
    raw = args.clauses.read_bytes()
    with args.clauses.open(encoding="utf-8-sig", newline="") as handle:
        result = build_aggregate(list(csv.DictReader(handle)), hashlib.sha256(raw).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Aggregate review guide: {result['total_reviewed_rows']} rows; {len(result['by_label'])} labels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
