"""Export reviewed v06 labels for D1 review, without claiming segmentation gold."""

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D1_IDS = frozenset({"HDLD001", "HDLD002", "HDLD003", "HDLD004"})
CLAUSE_TYPES = frozenset({
    "COMPENSATION_BENEFITS", "CONTRACT_TERM", "EMPLOYEE_OBLIGATIONS_DISCIPLINE",
    "EMPLOYER_RIGHTS_OBLIGATIONS", "INSURANCE_SAFETY", "JOB_INFO", "LEAVE",
    "OTHER", "TERMINATION", "TRAINING", "WORKING_CONDITIONS", "WORKING_TIME",
})


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_d1_clause_candidates(
    rows: list[dict[str, str]], raw_texts: dict[str, str] | None = None,
    source_sha256: str | None = None,
) -> dict:
    """Keep legacy labels; CONTEXT has no exact gold span."""
    items = []
    seen_ids: set[str] = set()
    contract_counts = {contract_id: 0 for contract_id in D1_IDS}
    for row in rows:
        clause_id = row.get("clause_id", "")
        if clause_id in seen_ids:
            raise ValueError(f"{clause_id}: duplicate clause_id")
        seen_ids.add(clause_id)
        if row["contract_id"] not in D1_IDS or row["annotation_status"] != "REVIEWED":
            continue
        if row["clause_type"] not in CLAUSE_TYPES:
            raise ValueError(f"{clause_id}: invalid clause_type {row['clause_type']!r}")
        quality = row["offset_quality"]
        if quality not in {"EXACT", "CONTEXT"}:
            raise ValueError(f"{row['clause_id']}: invalid offset_quality {quality!r}")
        source_span = {
            "start_char": int(row["start_offset"]),
            "end_char": int(row["end_offset"]),
            "offset_unit": "python_codepoint",
        }
        if source_span["start_char"] < 0 or source_span["end_char"] <= source_span["start_char"]:
            raise ValueError(f"{row['clause_id']}: invalid source span")
        if quality == "EXACT" and raw_texts is not None:
            raw = raw_texts.get(row["contract_id"])
            if raw is None:
                raise ValueError(f"{row['clause_id']}: missing raw text")
            actual = raw[source_span["start_char"]:source_span["end_char"]]
            if _normalize_whitespace(actual) != _normalize_whitespace(row["clause_text"]):
                raise ValueError(f"{row['clause_id']}: EXACT span does not match clause_text")
        items.append({
            "clause_id": row["clause_id"],
            "contract_id": row["contract_id"],
            "labels": [row["clause_type"]],
            "span": source_span if quality == "EXACT" else None,
            "source_reference_span": source_span if quality == "CONTEXT" else None,
            "offset_quality": quality,
            "annotator": None,
        })
        contract_counts[row["contract_id"]] += 1
    result = {
        "status": "CANDIDATE_NOT_SEGMENTATION_GOLD",
        "source": "data/processed/clauses_v06.csv",
        "taxonomy_version": "clause_taxonomy_v03",
        "scope": {
            "contracts": sorted(D1_IDS),
            "annotation_status_required": "REVIEWED",
            "offset_policy": "EXACT spans only; CONTEXT kept as reference and excluded from exact span gold",
            "segmentation_gold": False,
            "adjudicated": False,
        },
        "items": items,
        "contract_counts": dict(sorted(contract_counts.items())),
    }
    if source_sha256 is not None:
        result["source_sha256"] = source_sha256
    if raw_texts is not None:
        result["raw_source_sha256"] = {
            contract_id: hashlib.sha256(raw.encode("utf-8")).hexdigest()
            for contract_id, raw in sorted(raw_texts.items())
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clauses", type=Path, default=ROOT / "data/processed/clauses_v06.csv")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {args.output}")
    raw_texts = {
        contract_id: (ROOT / f"data/processed/raw_text/{contract_id}.txt").read_text(encoding="utf-8")
        for contract_id in sorted(D1_IDS)
    }
    source_bytes = args.clauses.read_bytes()
    with args.clauses.open(encoding="utf-8-sig", newline="") as handle:
        result = build_d1_clause_candidates(
            list(csv.DictReader(handle)), raw_texts=raw_texts,
            source_sha256=hashlib.sha256(source_bytes).hexdigest(),
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"D1 label candidates: {len(result['items'])}; output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
