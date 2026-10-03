"""Export one annotated contract with validated character spans for highlighting."""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def build_payload(contract_id: str, processed: Path = PROCESSED) -> dict:
    raw_path = processed / "raw_text" / f"{contract_id}.txt"
    if not raw_path.is_file():
        raise ValueError(f"raw text not found for {contract_id}")
    raw_text = raw_path.read_text(encoding="utf-8")
    clauses = []
    with (processed / "clauses_v05.csv").open(encoding="utf-8-sig", newline="") as handle:
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
            if quality == "EXACT":
                normalized_source = re.sub(r"\s+", " ", highlight_text).strip()
                normalized_clause = re.sub(r"\s+", " ", row["clause_text"]).strip()
                if normalized_source != normalized_clause:
                    raise ValueError(f"exact span mismatch for {row['clause_id']}")
            elif not highlight_text.strip():
                raise ValueError(f"empty context span for {row['clause_id']}")
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
    parser.add_argument("contract_id", help="e.g. HDLD003")
    args = parser.parse_args()
    try:
        payload = build_payload(args.contract_id)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
