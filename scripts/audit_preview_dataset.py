"""Audit an unreleased clause preview without treating release blockers as clean data.

Exit 0: structurally valid and release metadata complete.
Exit 1: structural or source-span error.
Exit 2: structurally valid preview with release blockers.
"""

import argparse
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from scripts.validate_dataset import ROOT, validate_dataset


@dataclass
class PreviewAudit:
    structural_errors: list[str] = field(default_factory=list)
    release_blockers: list[str] = field(default_factory=list)
    new_rows: int = 0
    pending_rows: int = 0
    row_counts_by_contract: dict[str, dict[str, int]] = field(default_factory=dict)
    valid_spans: int = 0
    span_errors: int = 0


def _rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def audit_preview_dataset(
    base_path: Path, preview_path: Path, metadata_path: Path, raw_text_dir: Path
) -> PreviewAudit:
    """Check copied release rows, new review rows, and strict validator errors."""
    result = PreviewAudit()
    try:
        base_fields, base_rows = _rows(base_path)
        preview_fields, preview_rows = _rows(preview_path)
    except (OSError, UnicodeError, csv.Error) as error:
        result.structural_errors.append(f"cannot read dataset: {error}")
        return result

    if base_fields != preview_fields:
        result.structural_errors.append("preview columns differ from base")
        return result
    base_by_id = {row["clause_id"]: row for row in base_rows}
    preview_by_id = {row["clause_id"]: row for row in preview_rows}
    if len(base_by_id) != len(base_rows):
        result.structural_errors.append("base dataset contains duplicate clause IDs")
    if len(preview_by_id) != len(preview_rows):
        result.structural_errors.append("preview contains duplicate clause IDs")
    for clause_id, base_row in base_by_id.items():
        current = preview_by_id.get(clause_id)
        if current is None:
            result.structural_errors.append(f"{clause_id}: missing from preview")
        elif current != base_row:
            result.structural_errors.append(f"{clause_id}: changed from base")

    for row in preview_rows:
        if row["clause_id"] not in base_by_id:
            result.new_rows += 1
            if row["annotation_status"] != "NEEDS_REVIEW":
                result.structural_errors.append(
                    f"{row['clause_id']}: new row is not NEEDS_REVIEW"
                )
    result.pending_rows = sum(row["annotation_status"] == "NEEDS_REVIEW" for row in preview_rows)
    if result.pending_rows:
        result.release_blockers.append(f"pending annotation review: {result.pending_rows} rows")

    with metadata_path.open(encoding="utf-8-sig", newline="") as handle:
        metadata_rows = list(csv.DictReader(handle))
    metadata_by_id = {row["contract_id"]: row for row in metadata_rows}
    counts: dict[str, Counter] = defaultdict(Counter)
    for row in preview_rows:
        contract_id = row["contract_id"]
        counts[contract_id]["rows"] += 1
        counts[contract_id][row["annotation_status"] or "MISSING_STATUS"] += 1
        metadata = metadata_by_id.get(contract_id)
        is_new_row = row["clause_id"] not in base_by_id
        metadata_incomplete = (
            metadata is None
            or not metadata.get("source_id")
            or not metadata.get("file_name")
        )
        if is_new_row and metadata_incomplete:
            counts[contract_id]["missing_source_metadata"] += 1
            if metadata is None:
                counts[contract_id]["metadata_missing"] += 1
            result.release_blockers.append(f"{contract_id}: new preview row has incomplete source metadata")
        if metadata is None and not is_new_row:
            counts[contract_id]["metadata_missing"] += 1
        elif metadata is not None:
            if metadata.get("dataset_version") != "v07":
                counts[contract_id]["metadata_not_v07"] += 1
            if metadata.get("dataset_status") != "ANNOTATED":
                counts[contract_id]["metadata_not_annotated"] += 1
        try:
            raw_text = (raw_text_dir / f"{contract_id}.txt").read_text(encoding="utf-8")
            start, end = int(row["start_offset"]), int(row["end_offset"])
            if not (0 <= start < end <= len(raw_text)):
                raise ValueError("invalid bounds")
            normalized_span = " ".join(raw_text[start:end].split())
            normalized_clause = " ".join(row["clause_text"].split())
            if row["offset_quality"] == "EXACT" and normalized_span != normalized_clause:
                raise ValueError("EXACT text mismatch")
            if row["offset_quality"] not in {"EXACT", "CONTEXT"}:
                raise ValueError("unknown offset quality")
            if metadata is not None:
                result.valid_spans += 1
                counts[contract_id]["valid_span"] += 1
            else:
                counts[contract_id]["span_structural_only"] += 1
        except (OSError, KeyError, TypeError, ValueError) as error:
            result.span_errors += 1
            counts[contract_id]["span_error"] += 1
            result.structural_errors.append(
                f"{row['clause_id']}: source span check failed ({type(error).__name__})"
            )

    result.row_counts_by_contract = {
        contract_id: dict(sorted(row_counts.items()))
        for contract_id, row_counts in sorted(counts.items())
    }

    base_contracts = {row["contract_id"] for row in base_rows}
    strict = validate_dataset(preview_path, metadata_path, raw_text_dir)
    for error in strict.errors:
        unknown = re.fullmatch(r"clauses:(\d+): unknown contract_id (HDLD\d{3})", error)
        if unknown:
            index = int(unknown.group(1)) - 2
            if 0 <= index < len(preview_rows):
                row = preview_rows[index]
                if row["clause_id"] not in base_by_id and row["annotation_status"] == "NEEDS_REVIEW":
                    result.release_blockers.append(error)
                    continue
        mismatch = re.fullmatch(r"metadata:(HDLD\d{3}): dataset_version mismatch", error)
        if mismatch and mismatch.group(1) in base_contracts:
            result.release_blockers.append(error)
            continue
        result.structural_errors.append(error)
    return result


def summarize_blockers(blockers: list[str]) -> list[str]:
    """Collapse repeated unknown-contract rows into one PII-free count per ID."""
    unique = sorted(set(blockers))
    counts: Counter[str] = Counter()
    for blocker in unique:
        match = re.fullmatch(r"clauses:\d+: unknown contract_id (HDLD\d{3})", blocker)
        if match:
            counts[match.group(1)] += 1
    summarized = [f"{contract_id}: {count} rows lack a metadata record"
                  for contract_id, count in sorted(counts.items())]
    summarized.extend(
        blocker for blocker in unique
        if not re.fullmatch(r"clauses:\d+: unknown contract_id HDLD\d{3}", blocker)
    )
    return summarized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=ROOT / "data/processed/clauses_v06.csv")
    parser.add_argument("--preview", type=Path, default=ROOT / "data/processed/clauses_v07.csv")
    parser.add_argument("--metadata", type=Path, default=ROOT / "data/contracts_metadata.csv")
    parser.add_argument("--raw-text-dir", type=Path, default=ROOT / "data/processed/raw_text")
    parser.add_argument("--details", action="store_true", help="print each error and blocker")
    args = parser.parse_args()
    audit = audit_preview_dataset(args.base, args.preview, args.metadata, args.raw_text_dir)
    print(f"New rows: {audit.new_rows}; NEEDS_REVIEW: {audit.pending_rows}")
    grouped_blockers = summarize_blockers(audit.release_blockers)
    print(f"Structural errors: {len(audit.structural_errors)}; release blocker groups: {len(grouped_blockers)}")
    print(f"Valid code-point spans: {audit.valid_spans}; span errors: {audit.span_errors}")
    for contract_id, counts in audit.row_counts_by_contract.items():
        print(f"{contract_id}: {counts}")
    if args.details:
        for error in audit.structural_errors:
            print(f"ERROR: {error}")
        for blocker in summarize_blockers(audit.release_blockers):
            print(f"BLOCKER: {blocker}")
    return 1 if audit.structural_errors else 2 if audit.release_blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
