"""Audit structural evidence before counting executed employment contracts.

This gate checks that claimed approvals have inspectable receipts. It cannot
substitute for a human legal, signature, authorization, or privacy review.
"""

import csv
import hashlib
import re
from datetime import date
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DECISIONS = {"HOLD", "ACCEPTED_T1", "ACCEPTED_ADDITIONAL"}
REQUIRED_APPROVALS = {
    "signed_check": "VERIFIED",
    "distinct_document_check": "PASS",
    "rights_authority_check": "VERIFIED",
    "rights_store_process": "GRANTED",
    "rights_share_internal": "GRANTED",
    "rights_eval_derivative": "GRANTED",
    "visual_redaction": "PASS",
    "text_redaction": "PASS",
    "metadata_redaction": "PASS",
    "second_review_decision": "APPROVED",
    "leakage_check": "PASS",
}
UNVERIFIED_GROUPS = {"", "unknown", "unknown_scan", "unknown_provisional", "independent_provisional"}


def load_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_digest(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def evaluate_units(manifest_rows, unit_rows, root):
    """Return (errors, accepted counts); errors make all counts inadmissible."""
    manifest = {row["candidate_id"]: row for row in manifest_rows}
    errors = []
    seen_ids = set()
    accepted = []
    family_splits = {}
    t1_groups = set()
    page_counts = {}
    candidate_spans = {}

    for row in unit_rows:
        unit_id = row.get("unit_id", "").strip()
        candidate_id = row.get("candidate_id", "").strip()
        decision = row.get("decision", "").strip()
        tag = unit_id or "<missing unit_id>"
        if not unit_id or unit_id in seen_ids:
            errors.append(f"{tag}: missing or duplicate unit_id")
        seen_ids.add(unit_id)
        if candidate_id not in manifest:
            errors.append(f"{tag}: unknown candidate_id {candidate_id}")
        span = re.fullmatch(r"([1-9]\d*)-([1-9]\d*)", row.get("source_pages", ""))
        if span is None or int(span.group(1)) > int(span.group(2)):
            errors.append(f"{tag}: invalid source_pages")
        else:
            start, end = map(int, span.groups())
            for existing_start, existing_end, existing_id in candidate_spans.get(candidate_id, []):
                if start <= existing_end and existing_start <= end:
                    errors.append(f"{tag}: overlapping source_pages with {existing_id}")
            candidate_spans.setdefault(candidate_id, []).append((start, end, tag))

            source = manifest.get(candidate_id)
            if source and source.get("local_path", "").lower().endswith(".pdf"):
                if candidate_id not in page_counts:
                    path = root / source["local_path"]
                    if path.is_file():
                        try:
                            page_counts[candidate_id] = len(PdfReader(path).pages)
                        except Exception as exc:
                            errors.append(f"{tag}: unreadable source PDF ({type(exc).__name__})")
                            page_counts[candidate_id] = None
                    else:
                        page_counts[candidate_id] = None
                total = page_counts[candidate_id]
                if total is not None and end > total:
                    errors.append(f"{tag}: source_pages exceed source PDF ({total} pages)")
        if decision not in ALLOWED_DECISIONS:
            errors.append(f"{tag}: invalid decision {decision}")
            continue
        if decision == "HOLD":
            continue

        for key, required in REQUIRED_APPROVALS.items():
            if row.get(key, "").strip() != required:
                errors.append(f"{tag}: {key} must be {required}")
        if decision == "ACCEPTED_T1" and row.get("template_independence_check") != "PASS":
            errors.append(f"{tag}: template_independence_check must be PASS for T1")
        if not row.get("prepared_by_id") or not row.get("second_reviewer_id"):
            errors.append(f"{tag}: preparer and independent reviewer IDs required")
        elif row["prepared_by_id"] == row["second_reviewer_id"]:
            errors.append(f"{tag}: independent reviewer must differ from preparer")
        try:
            date.fromisoformat(row.get("second_review_date", ""))
        except ValueError:
            errors.append(f"{tag}: second_review_date must be ISO date")

        group = row.get("similarity_group", "").strip()
        split = row.get("split", "").strip()
        if group.lower() in UNVERIFIED_GROUPS:
            errors.append(f"{tag}: reviewed similarity_group required")
        if decision == "ACCEPTED_T1":
            if split != "T1":
                errors.append(f"{tag}: T1 must use T1 split")
            if group in t1_groups:
                errors.append(f"{tag}: multiple T1 contracts share similarity_group")
            t1_groups.add(group)
        elif split not in {"TRAIN", "DEV", "TEST"}:
            errors.append(f"{tag}: additional contract requires TRAIN/DEV/TEST split")
        if group in family_splits and family_splits[group] != split:
            errors.append(f"{tag}: similarity_group crosses dataset splits")
        family_splits[group] = split

        source = manifest.get(candidate_id)
        if source:
            if decision == "ACCEPTED_T1" and source.get("t1_eligible") != "yes":
                errors.append(f"{tag}: parent manifest is not t1_eligible=yes")
            path = root / source.get("local_path", "")
            if not source.get("local_path") or not path.is_file():
                errors.append(f"{tag}: source file missing")
            else:
                if file_digest(path) != source.get("sha256", "").lower():
                    errors.append(f"{tag}: source hash mismatch")
                if str(path.stat().st_size) != source.get("bytes", ""):
                    errors.append(f"{tag}: source size mismatch")

        for path_field, hash_field, label in (
            ("rights_evidence_path", None, "rights evidence"),
            ("derivative_path", "derivative_sha256", "derivative"),
        ):
            path_text = row.get(path_field, "").strip()
            path = (root / path_text).resolve()
            if label == "rights evidence":
                restricted_roots = (
                    (root / "data/intake/restricted").resolve(),
                    (root / "data/intake/private").resolve(),
                )
                if not any(path.is_relative_to(base) for base in restricted_roots):
                    errors.append(f"{tag}: rights evidence requires restricted location")
            elif not path.is_relative_to(root.resolve()):
                errors.append(f"{tag}: derivative must stay inside project root")
            if label == "derivative" and source and source.get("local_path"):
                original = (root / source["local_path"]).resolve()
                if path == original or (path.is_file() and original.is_file()
                                        and file_digest(path) == file_digest(original)):
                    errors.append(f"{tag}: derivative must be distinct from source")
            if not path_text or not path.is_file():
                errors.append(f"{tag}: {label} file missing")
            elif hash_field and file_digest(path) != row.get(hash_field, "").lower():
                errors.append(f"{tag}: {label} hash mismatch")

        accepted.append((decision, candidate_id))

    # Any candidate flagged T1-eligible must have an independently gated unit.
    gated_t1 = {candidate for decision, candidate in accepted if decision == "ACCEPTED_T1"}
    for candidate_id, source in manifest.items():
        if source.get("t1_eligible") == "yes" and candidate_id not in gated_t1:
            errors.append(f"{candidate_id}: parent has t1_eligible=yes but no accepted T1 unit")

    summary = {
        "screened_units": len(unit_rows),
        "accepted_t1": 0 if errors else sum(d == "ACCEPTED_T1" for d, _ in accepted),
        "accepted_additional": 0 if errors else sum(d == "ACCEPTED_ADDITIONAL" for d, _ in accepted),
    }
    return errors, summary


if __name__ == "__main__":
    manifest_rows = load_csv(ROOT / "data/intake/manifest.csv")
    unit_rows = load_csv(ROOT / "data/intake/contract_unit_review_queue.csv")
    issues, totals = evaluate_units(manifest_rows, unit_rows, ROOT)
    print(f"Unit queue: {totals['screened_units']}; accepted T1: {totals['accepted_t1']}/10; "
          f"accepted additional: {totals['accepted_additional']}/20")
    for issue in issues:
        print("ERROR:", issue)
    raise SystemExit(bool(issues))
