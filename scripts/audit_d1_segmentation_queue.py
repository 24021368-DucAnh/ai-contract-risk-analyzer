"""Audit D1 segmentation-queue coverage without printing contract text."""

import argparse
import csv
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D1_IDS = frozenset({"HDLD001", "HDLD002", "HDLD003", "HDLD004"})
QUEUE_FIELDS = {
    "clause_id", "contract_id", "offset_quality", "start_char", "end_char",
    "review_status", "reviewer_id", "review_note",
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path.name}: missing header")
        return list(reader)


def audit_queue(
    clause_rows: Iterable[dict[str, str]],
    queue_rows: Iterable[dict[str, str]],
    raw_texts: dict[str, str],
) -> dict:
    """Return PII-free coverage and integrity counts for the manual D1 queue."""
    source_by_id = {
        row["clause_id"]: row
        for row in clause_rows
        if row.get("contract_id") in D1_IDS and row.get("annotation_status") == "REVIEWED"
    }
    queue = list(queue_rows)
    counts_by_contract: dict[str, Counter] = defaultdict(Counter)
    errors: list[str] = []
    seen: set[str] = set()
    valid_spans = 0

    if queue and set(queue[0]) != QUEUE_FIELDS:
        errors.append("queue column set does not match expected private review schema")

    for row in queue:
        clause_id = row.get("clause_id", "")
        contract_id = row.get("contract_id", "")
        quality = row.get("offset_quality", "")
        counts_by_contract[contract_id]["queue"] += 1
        counts_by_contract[contract_id][quality or "MISSING_QUALITY"] += 1
        if clause_id in seen:
            errors.append("duplicate clause IDs in queue")
        seen.add(clause_id)
        source = source_by_id.get(clause_id)
        if source is None:
            errors.append("queue contains clause IDs outside reviewed D1 v06")
            continue
        if source.get("contract_id") != contract_id or source.get("offset_quality") != quality:
            errors.append("queue metadata differs from v06 source row")
        if row.get("review_status") != "PENDING_MANUAL_SEGMENTATION":
            errors.append("unexpected non-pending queue status; requires explicit review")

        try:
            start, end = int(row["start_char"]), int(row["end_char"])
            text = raw_texts[contract_id]
            if not (0 <= start < end <= len(text)):
                raise ValueError
            if quality == "EXACT":
                clause_text = source["clause_text"]
                span_text = " ".join(text[start:end].split())
                expected_text = " ".join(clause_text.split())
                if span_text != expected_text:
                    errors.append("EXACT span no longer matches normalized clause text")
                    continue
            elif quality != "CONTEXT":
                errors.append("unsupported offset quality")
                continue
            valid_spans += 1
            counts_by_contract[contract_id]["valid_span"] += 1
        except (KeyError, TypeError, ValueError):
            errors.append("invalid or unavailable code-point span")

        if row.get("reviewer_id", "").strip() or row.get("review_note", "").strip():
            counts_by_contract[contract_id]["annotated_metadata"] += 1

    missing = set(source_by_id) - seen
    if missing:
        errors.append("queue does not cover every reviewed D1 clause")

    contracts = {
        contract_id: dict(sorted(counts.items()))
        for contract_id, counts in sorted(counts_by_contract.items())
    }
    return {
        "status": "PASS" if not errors else "FAIL",
        "expected_d1_clauses": len(source_by_id),
        "queue_rows": len(queue),
        "unique_queue_ids": len(seen),
        "missing_queue_rows": len(missing),
        "valid_codepoint_spans": valid_spans,
        "reviewer_or_note_filled_rows": sum(c["annotated_metadata"] for c in counts_by_contract.values()),
        "contract_counts": contracts,
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clauses", type=Path, default=ROOT / "data/processed/clauses_v06.csv")
    parser.add_argument("--queue", type=Path, default=ROOT / "data/intake/private/d1_segmentation_review_queue_v06.csv")
    parser.add_argument("--raw-dir", type=Path, default=ROOT / "data/processed/raw_text")
    args = parser.parse_args()

    clause_rows = _read_csv(args.clauses)
    queue_rows = _read_csv(args.queue)
    raw_texts = {
        contract_id: (args.raw_dir / f"{contract_id}.txt").read_text(encoding="utf-8")
        for contract_id in D1_IDS
    }
    result = audit_queue(clause_rows, queue_rows, raw_texts)
    import json

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
