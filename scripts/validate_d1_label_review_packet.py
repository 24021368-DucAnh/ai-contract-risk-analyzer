"""Validate the D1 independent label review packet without judging its labels."""

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

EXPECTED_CONTRACTS = {"HDLD001", "HDLD002", "HDLD003", "HDLD004"}
FIELDS = {
    "clause_id", "contract_id", "candidate_label", "source_span_start",
    "source_span_end", "offset_quality", "reviewer_label", "reviewer_span_start",
    "reviewer_span_end", "reviewer_id", "review_status", "adjudicated_label",
    "adjudicator_id", "adjudication_date", "notes",
}
LABELS = {
    "COMPENSATION_BENEFITS", "CONTRACT_TERM", "EMPLOYEE_OBLIGATIONS_DISCIPLINE",
    "EMPLOYER_RIGHTS_OBLIGATIONS", "INSURANCE_SAFETY", "JOB_INFO", "LEAVE",
    "OTHER", "TERMINATION", "TRAINING", "WORKING_CONDITIONS", "WORKING_TIME",
}


def validate_packet(rows: list[dict[str, str]], expected_clause_ids: set[str]) -> dict:
    errors: list[str] = []
    ids = [row.get("clause_id", "") for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate clause_id")
    if set(ids) != expected_clause_ids:
        errors.append("packet clause IDs do not match expected D1 coverage")
    if any(set(row) != FIELDS for row in rows):
        errors.append("packet columns do not match schema")
    for index, row in enumerate(rows):
        owner = f"row {index + 2}"
        if row.get("contract_id") not in EXPECTED_CONTRACTS:
            errors.append(f"{owner}: contract outside D1 scope")
        if row.get("review_status") != "PENDING_INDEPENDENT_REVIEW":
            errors.append(f"{owner}: invalid initial review status")
        if any(row.get(key, "").strip() for key in (
            "reviewer_label", "reviewer_span_start", "reviewer_span_end",
            "reviewer_id", "adjudicated_label", "adjudicator_id", "adjudication_date",
        )):
            errors.append(f"{owner}: reviewer/adjudication fields must start blank")
        if row.get("offset_quality") == "CONTEXT":
            if row.get("source_span_start") or row.get("source_span_end"):
                errors.append(f"{owner}: CONTEXT cannot have an exact source span")
        elif row.get("offset_quality") == "EXACT":
            try:
                start, end = int(row["source_span_start"]), int(row["source_span_end"])
            except (KeyError, ValueError):
                errors.append(f"{owner}: EXACT source span must be integer offsets")
            else:
                if start < 0 or end <= start:
                    errors.append(f"{owner}: invalid EXACT source span")
        else:
            errors.append(f"{owner}: offset_quality must be EXACT or CONTEXT")
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "status": "PASS",
        "rows": len(rows),
        "contract_counts": {
            contract: sum(row["contract_id"] == contract for row in rows)
            for contract in sorted(EXPECTED_CONTRACTS)
        },
        "context_rows": sum(row["offset_quality"] == "CONTEXT" for row in rows),
        "adjudicated_rows": 0,
    }


def validate_reviewed_packet(rows: list[dict[str, str]], expected_clause_ids: set[str]) -> dict:
    """Require independent review and adjudication before labels can be called gold."""
    validate_packet_structure(rows, expected_clause_ids)
    errors = []
    for index, row in enumerate(rows):
        owner = f"row {index + 2}"
        if row["candidate_label"] not in LABELS or row["reviewer_label"] not in LABELS:
            errors.append(f"{owner}: candidate/reviewer label is outside taxonomy")
        if not row["reviewer_id"].strip() or row["reviewer_id"] == "legacy_v06":
            errors.append(f"{owner}: independent reviewer_id is required")
        if row["review_status"] not in {"REVIEWED_AGREES", "REVIEWED_DISAGREES_ADJUDICATED"}:
            errors.append(f"{owner}: review status is not complete")
        if row["offset_quality"] == "EXACT":
            try:
                start, end = int(row["reviewer_span_start"]), int(row["reviewer_span_end"])
                if start < 0 or end <= start:
                    raise ValueError
            except ValueError:
                errors.append(f"{owner}: reviewer exact span is invalid")
        elif row["reviewer_span_start"] or row["reviewer_span_end"]:
            errors.append(f"{owner}: CONTEXT reviewer exact span must remain blank")
        if not row["adjudicated_label"] or row["adjudicated_label"] not in LABELS:
            errors.append(f"{owner}: adjudicated_label is required and must be in taxonomy")
        if not row["adjudicator_id"].strip() or row["adjudicator_id"] == row["reviewer_id"]:
            errors.append(f"{owner}: distinct adjudicator_id is required")
        try:
            timestamp = datetime.fromisoformat(row["adjudication_date"])
            if timestamp.utcoffset() is None:
                raise ValueError
        except ValueError:
            errors.append(f"{owner}: adjudication_date must be timezone-aware ISO-8601")
    if errors:
        raise ValueError("; ".join(errors))
    return {"status": "PASS", "rows": len(rows), "gold_clause_label_rows": len(rows)}


def validate_packet_structure(rows: list[dict[str, str]], expected_clause_ids: set[str]) -> dict:
    """Check identity/scope/span shape while allowing completed reviewer fields."""
    errors = []
    ids = [row.get("clause_id", "") for row in rows]
    if len(ids) != len(set(ids)) or set(ids) != expected_clause_ids:
        errors.append("packet IDs are duplicate or do not match expected D1 coverage")
    for row in rows:
        if set(row) != FIELDS or row.get("contract_id") not in EXPECTED_CONTRACTS:
            errors.append("packet schema or D1 contract scope invalid")
        if row.get("offset_quality") not in {"EXACT", "CONTEXT"}:
            errors.append("invalid offset_quality")
    if errors:
        raise ValueError("; ".join(errors))
    return {"status": "PASS", "rows": len(rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("candidates", type=Path)
    args = parser.parse_args()
    packet = list(csv.DictReader(args.packet.open(encoding="utf-8-sig", newline="")))
    candidates = json.loads(args.candidates.read_text(encoding="utf-8"))
    expected = {item["clause_id"] for item in candidates["items"]}
    print(json.dumps(validate_packet(packet, expected), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
