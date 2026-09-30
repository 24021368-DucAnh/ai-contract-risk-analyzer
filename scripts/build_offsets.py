"""Create the next clause snapshot with offsets into extracted contract text.

Only whitespace normalization is allowed when matching. Annotated text that
rephrases or splits a source sentence remains unaligned for manual review.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "data" / "processed" / "clauses_v03.csv"
OUTPUT_CSV = ROOT / "data" / "processed" / "clauses_v04.csv"
RAW_TEXT_DIR = ROOT / "data" / "processed" / "raw_text"
UNVERIFIED_NOTE = "OFFSET_UNVERIFIED: no contiguous source span matches after whitespace normalization"


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def _normalized_with_spans(value: str) -> tuple[str, list[tuple[int, int]]]:
    chars: list[str] = []
    spans: list[tuple[int, int]] = []
    for index, char in enumerate(value):
        if char.isspace():
            if chars and chars[-1] == " ":
                spans[-1] = (spans[-1][0], index + 1)
            else:
                chars.append(" ")
                spans.append((index, index + 1))
        else:
            chars.append(char)
            spans.append((index, index + 1))
    return "".join(chars), spans


def align_rows(rows: list[dict[str, str]], raw_text_by_contract: dict[str, str]) -> list[dict[str, str]]:
    normalized = {key: _normalized_with_spans(text) for key, text in raw_text_by_contract.items()}
    cursors = {key: 0 for key in raw_text_by_contract}
    aligned: list[dict[str, str]] = []
    for row in rows:
        contract_id = row["contract_id"]
        if contract_id not in normalized:
            raise ValueError(f"Missing raw text for {contract_id}")
        text, spans = normalized[contract_id]
        query = normalize_whitespace(row["clause_text"])
        position = text.find(query, cursors[contract_id]) if query else -1
        result = dict(row)
        if position < 0:
            result["start_offset"] = ""
            result["end_offset"] = ""
            notes = result.get("notes", "").strip()
            result["notes"] = f"{notes}; {UNVERIFIED_NOTE}" if notes else UNVERIFIED_NOTE
        else:
            result["start_offset"] = str(spans[position][0])
            result["end_offset"] = str(spans[position + len(query) - 1][1])
            cursors[contract_id] = position + len(query)
        aligned.append(result)
    return aligned


def main() -> None:
    with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as source_file:
        reader = csv.DictReader(source_file)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or []) + ["start_offset", "end_offset"]
    contract_ids = {row["contract_id"] for row in rows}
    raw_text = {
        contract_id: (RAW_TEXT_DIR / f"{contract_id}.txt").read_text(encoding="utf-8")
        for contract_id in contract_ids
    }
    aligned = align_rows(rows, raw_text)

    if OUTPUT_CSV.exists():
        raise FileExistsError(f"Snapshot already exists: {OUTPUT_CSV}")
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(aligned)
    valid = sum(bool(row["start_offset"]) for row in aligned)
    print(f"Wrote {OUTPUT_CSV}: {valid}/{len(aligned)} verified spans")


if __name__ == "__main__":
    main()
