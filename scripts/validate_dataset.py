"""Validate the current clause dataset against metadata and committed raw text.

Run from the repository root: python -m scripts.validate_dataset
"""

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from scripts.build_offsets import normalize_whitespace


ROOT = Path(__file__).resolve().parents[1]
CLAUSE_COLUMNS = (
    "clause_id", "contract_id", "section_title", "clause_text", "clause_type",
    "annotation_status", "notes", "start_offset", "end_offset", "offset_quality",
)
METADATA_COLUMNS = (
    "contract_id", "source_id", "original_name", "file_name", "contract_type",
    "file_format", "page_count", "similarity_group", "dataset_status",
    "clause_count", "dataset_version", "notes",
)
CLAUSE_TYPES = frozenset({
    "COMPENSATION_BENEFITS", "CONTRACT_TERM", "EMPLOYEE_OBLIGATIONS_DISCIPLINE",
    "EMPLOYER_RIGHTS_OBLIGATIONS", "INSURANCE_SAFETY", "JOB_INFO", "LEAVE",
    "OTHER", "TERMINATION", "TRAINING", "WORKING_CONDITIONS", "WORKING_TIME",
})
STATUSES = frozenset({"REVIEWED", "NEEDS_REVIEW"})
DATASET_STATUSES = frozenset({"ANNOTATED", "TO_ANNOTATE", "HOLD_NEAR_DUPLICATE", "EXCLUDED"})
CLAUSE_ID = re.compile(r"^(HDLD\d{3})_C\d{3}[A-Z]?$")
CONTRACT_ID = re.compile(r"^HDLD\d{3}$")


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    clause_count: int = 0
    contract_count: int = 0
    class_counts: dict[str, int] = field(default_factory=dict)
    annotation_status_counts: dict[str, int] = field(default_factory=dict)
    offset_quality_counts: dict[str, int] = field(default_factory=dict)
    context_clause_ids: list[str] = field(default_factory=list)
    duplicate_text_count: int = 0


def _read_csv(path: Path, columns: tuple[str, ...], report: ValidationReport) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != columns:
                report.errors.append(f"{path}: expected columns {','.join(columns)}")
                return []
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as error:
        report.errors.append(f"{path}: cannot read CSV: {error}")
        return []
    for line, row in enumerate(rows, start=2):
        if None in row or any(value is None for value in row.values()):
            report.errors.append(f"{path}:{line}: malformed CSV row")
    return rows


def validate_dataset(clauses_path: Path, metadata_path: Path, raw_text_dir: Path) -> ValidationReport:
    """Return all structural errors and a summary; CONTEXT rows remain review items."""
    report = ValidationReport()
    clauses = _read_csv(clauses_path, CLAUSE_COLUMNS, report)
    metadata = _read_csv(metadata_path, METADATA_COLUMNS, report)
    if not clauses and not report.errors:
        report.errors.append(f"{clauses_path}: no clause rows")
    if not clauses or not metadata:
        return report

    metadata_by_id: dict[str, dict[str, str]] = {}
    source_dir = raw_text_dir.parent.parent / "raw" / "contracts"
    for line, row in enumerate(metadata, start=2):
        contract_id = (row.get("contract_id") or "").strip()
        if not CONTRACT_ID.fullmatch(contract_id):
            report.errors.append(f"metadata:{line}: invalid contract_id {contract_id!r}")
        if contract_id in metadata_by_id:
            report.errors.append(f"metadata:{line}: duplicate contract_id {contract_id}")
        metadata_by_id[contract_id] = row
        for key in ("source_id", "file_name", "contract_type", "file_format", "similarity_group"):
            if not (row.get(key) or "").strip():
                report.errors.append(f"metadata:{line}: empty {key}")
        if row.get("dataset_status") not in DATASET_STATUSES:
            report.errors.append(f"metadata:{line}: invalid dataset_status")
        file_name = row.get("file_name") or ""
        if file_name and Path(file_name).name != file_name:
            report.errors.append(f"metadata:{line}: invalid file_name {file_name!r}")
        elif file_name and not (source_dir / file_name).is_file():
            report.errors.append(f"metadata:{line}: missing source file {file_name}")

    seen_ids: set[str] = set()
    clause_counts: Counter[str] = Counter()
    class_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    quality_counts: Counter[str] = Counter()
    text_counts: Counter[str] = Counter()
    raw_cache: dict[str, str | None] = {}
    for line, row in enumerate(clauses, start=2):
        clause_id = (row.get("clause_id") or "").strip()
        contract_id = (row.get("contract_id") or "").strip()
        label = (row.get("clause_type") or "").strip()
        clause_text = row.get("clause_text") or ""
        quality = (row.get("offset_quality") or "").strip()
        if not CLAUSE_ID.fullmatch(clause_id) or not clause_id.startswith(f"{contract_id}_"):
            report.errors.append(f"clauses:{line}: invalid clause_id {clause_id!r}")
        if clause_id in seen_ids:
            report.errors.append(f"clauses:{line}: duplicate clause_id {clause_id}")
        seen_ids.add(clause_id)
        if contract_id not in metadata_by_id:
            report.errors.append(f"clauses:{line}: unknown contract_id {contract_id}")
        if not (row.get("section_title") or "").strip():
            report.errors.append(f"clauses:{line}: empty section_title")
        if not clause_text.strip():
            report.errors.append(f"clauses:{line}: empty clause_text")
        else:
            text_counts[normalize_whitespace(clause_text)] += 1
        if label not in CLAUSE_TYPES:
            report.errors.append(f"clauses:{line}: invalid clause_type {label!r}")
        else:
            class_counts[label] += 1
        if row.get("annotation_status") not in STATUSES:
            report.errors.append(f"clauses:{line}: invalid annotation_status")
        else:
            status_counts[row["annotation_status"]] += 1
        if quality not in ("EXACT", "CONTEXT"):
            report.errors.append(f"clauses:{line}: invalid offset_quality {quality!r}")
        else:
            quality_counts[quality] += 1
        if quality == "CONTEXT":
            report.context_clause_ids.append(clause_id)
            if "OFFSET_CONTEXT" not in (row.get("notes") or ""):
                report.errors.append(f"clauses:{line}: CONTEXT requires OFFSET_CONTEXT note")

        clause_counts[contract_id] += 1
        offsets: list[int] = []
        for key in ("start_offset", "end_offset"):
            value = row.get(key) or ""
            try:
                offsets.append(int(value))
            except ValueError:
                report.errors.append(f"clauses:{line}: invalid {key} {value!r}")
        if len(offsets) != 2:
            continue
        start, end = offsets
        if contract_id not in raw_cache:
            try:
                with (raw_text_dir / f"{contract_id}.txt").open(encoding="utf-8", newline="") as handle:
                    raw_cache[contract_id] = handle.read()
            except (OSError, UnicodeError):
                raw_cache[contract_id] = None
                report.errors.append(f"clauses:{line}: missing or unreadable raw text for {contract_id}")
        raw_text = raw_cache[contract_id]
        if raw_text is None:
            continue
        if not 0 <= start < end <= len(raw_text):
            report.errors.append(f"clauses:{line}: offset out of bounds")
        elif quality == "CONTEXT" and not raw_text[start:end].strip():
            report.errors.append(f"clauses:{line}: CONTEXT span is blank for {clause_id}")
        elif quality == "EXACT" and normalize_whitespace(raw_text[start:end]) != normalize_whitespace(clause_text):
            report.errors.append(f"clauses:{line}: EXACT span mismatch for {clause_id}")

    for contract_id, row in metadata_by_id.items():
        count = clause_counts[contract_id]
        expected = (row.get("clause_count") or "").strip()
        if expected:
            if not expected.isdecimal() or int(expected) != count:
                report.errors.append(f"metadata:{contract_id}: clause_count mismatch ({expected} vs {count})")
        elif row.get("dataset_status") == "ANNOTATED":
            report.errors.append(f"metadata:{contract_id}: missing clause_count")
        if row.get("dataset_status") == "ANNOTATED" and count == 0:
            report.errors.append(f"metadata:{contract_id}: ANNOTATED contract has no clauses")
        if count and row.get("dataset_status") != "ANNOTATED":
            report.errors.append(f"metadata:{contract_id}: clauses exist but status is not ANNOTATED")
        if count and row.get("dataset_version") != clauses_path.stem.removeprefix("clauses_"):
            report.errors.append(f"metadata:{contract_id}: dataset_version mismatch")

    report.clause_count = len(clauses)
    report.contract_count = len(clause_counts)
    report.class_counts = dict(sorted(class_counts.items()))
    report.annotation_status_counts = dict(sorted(status_counts.items()))
    report.offset_quality_counts = dict(sorted(quality_counts.items()))
    report.duplicate_text_count = sum(count - 1 for count in text_counts.values() if count > 1)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clauses", type=Path, default=ROOT / "data/processed/clauses_v05.csv")
    parser.add_argument("--metadata", type=Path, default=ROOT / "data/contracts_metadata.csv")
    parser.add_argument("--raw-text-dir", type=Path, default=ROOT / "data/processed/raw_text")
    args = parser.parse_args()
    report = validate_dataset(args.clauses, args.metadata, args.raw_text_dir)
    print(f"Contracts: {report.contract_count}; clauses: {report.clause_count}; duplicate texts: {report.duplicate_text_count}")
    print("Clause types: " + ", ".join(f"{key}={count}" for key, count in report.class_counts.items()))
    print("Annotation status: " + ", ".join(f"{key}={count}" for key, count in report.annotation_status_counts.items()))
    print("Offsets: " + ", ".join(f"{key}={count}" for key, count in report.offset_quality_counts.items()))
    print("CONTEXT for manual review: " + (", ".join(report.context_clause_ids) or "none"))
    for error in report.errors:
        print(f"ERROR: {error}")
    print(f"Critical errors: {len(report.errors)}")
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
