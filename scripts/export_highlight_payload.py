"""Export one annotated contract with validated character spans for highlighting."""

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.validate_intake_gate import evaluate_units, load_csv

# Frozen development snapshots, not signed intake or redistributable legal gold.
# Reject a replaced fixture rather than accidentally exporting new personal data.
LOCAL_FIXTURE_SHA256 = {
    "HDLD001": "31ea18a5e75bc57beee442d3ef31ab480c558d4c47eb5ab44906474f45cec625",
    "HDLD002": "5342408718b4bde9449427e820e7e6a525df3717fa9c10ad5326c1b525c41711",
    "HDLD003": "f76195cc5da1c65aad45debe3ca44c7dd4df5c077f29b1660555b604197e60f7",
    "HDLD004": "32f363a4e50ff056c6bc062a123fe8d16699055ca7be596175173381cb07afea",
    "HDLD005": "8f6e3d3b10d20f949879e2a7dcd5e27229baa06d661187e299cfa5d9d06ea85f",
}


def _source_text_path(contract_id: str, processed: Path, root: Path, local_fixture: bool) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,100}", contract_id):
        raise ValueError("invalid contract identifier")
    if local_fixture:
        if contract_id not in LOCAL_FIXTURE_SHA256:
            raise ValueError("not a frozen local development fixture")
        path = processed / "raw_text" / f"{contract_id}.txt"
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != LOCAL_FIXTURE_SHA256[contract_id]:
            raise ValueError("local development fixture is missing or changed")
        return path

    manifest_file = root / "data/intake/manifest.csv"
    unit_file = root / "data/intake/contract_unit_review_queue.csv"
    if not manifest_file.is_file() or not unit_file.is_file():
        raise ValueError("contract not accepted: missing intake review records")
    units = load_csv(unit_file)
    unit = next((row for row in units if row.get("unit_id") == contract_id
                 and row.get("decision") in {"ACCEPTED_T1", "ACCEPTED_ADDITIONAL"}), None)
    if unit is None:
        raise ValueError("contract not accepted by the intake review gate")
    errors, _ = evaluate_units(load_csv(manifest_file), units, root)
    if errors:
        raise ValueError("intake gate rejected export: " + "; ".join(errors))
    # No fallback to data/processed/raw_text: it may contain unreviewed PII.
    approved_dir = (root / "data/processed/approved").resolve()
    path = (root / unit["derivative_path"]).resolve()
    if not path.is_relative_to(approved_dir) or path.suffix.lower() != ".txt":
        raise ValueError("approved export requires a reviewed UTF-8 text derivative in data/processed/approved")
    return path


def build_payload(
    contract_id: str, processed: Path = PROCESSED, *, root: Path = ROOT, local_fixture: bool = False
) -> dict:
    raw_path = _source_text_path(contract_id, processed, root, local_fixture)
    if not raw_path.is_file():
        raise ValueError(f"raw text not found for {contract_id}")
    raw_text = raw_path.read_text(encoding="utf-8")
    clauses = []
    with (processed / "clauses_v06.csv").open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["contract_id"] != contract_id:
                continue
            start, end = int(row["start_offset"]), int(row["end_offset"])
            if not 0 <= start < end <= len(raw_text):
                raise ValueError(f"invalid span for {row['clause_id']}")
            highlight_text = raw_text[start:end]
            quality = row["offset_quality"]
            if quality not in {"EXACT", "CONTEXT"}:
                raise ValueError(f"invalid offset quality for {row['clause_id']}")
            if not local_fixture and quality != "EXACT":
                raise ValueError(f"approved export requires EXACT reviewed spans: {row['clause_id']}")
            if quality == "EXACT":
                normalized_source = re.sub(r"\s+", " ", highlight_text).strip()
                normalized_clause = re.sub(r"\s+", " ", row["clause_text"]).strip()
                if normalized_source != normalized_clause:
                    raise ValueError(f"exact span mismatch for {row['clause_id']}")
            elif not highlight_text.strip():
                raise ValueError(f"empty context span for {row['clause_id']}")
            if not local_fixture and row["section_title"].strip() not in raw_text:
                raise ValueError(f"unverified section title for {row['clause_id']}")
            clauses.append({
                "clause_id": row["clause_id"],
                "section_title": row["section_title"],
                "clause_text": row["clause_text"],
                "clause_type": row["clause_type"],
                "start_offset": start,
                "end_offset": end,
                "offset_quality": quality,
                "highlight_text": highlight_text,
            })
    if not clauses:
        raise ValueError(f"no annotated clauses for {contract_id}")
    return {"contract_id": contract_id, "raw_text": raw_text, "clauses": clauses}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract_id", help="accepted signed-unit ID, or frozen dev ID with --local-fixture")
    parser.add_argument("--local-fixture", action="store_true",
                        help="explicitly export frozen development data locally; NOT approved for redistribution")
    args = parser.parse_args()
    try:
        payload = build_payload(args.contract_id, local_fixture=args.local_fixture)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
