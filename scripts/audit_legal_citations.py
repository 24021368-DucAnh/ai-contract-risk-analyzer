"""Produce a PII-free review queue of article references in local contract text.

This is a locator, not a legal-risk model or a determination of legal validity.
Contract text is read locally and never copied to the CSV or console output.
"""

import argparse
import csv
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = re.compile(r"(?<!\w)điều\s+([0-9]{1,3})(?!\w)", re.IGNORECASE)
OUTPUT_COLUMNS = (
    "contract_id", "source_kind", "source_text", "source_sha256", "source_line", "article_number",
    "char_offset", "linked_clause_ids", "citation_context", "suspected_issue",
    "candidate_correct_article", "legal_instrument_to_check", "review_status",
    "human_reviewer", "human_review_date",
)

# Provenance-bound hypotheses from 2026-10-28 QC. Not approved legal labels.
KNOWN_QC = {
    ("HDLD003", 81, "38"): ("EMPLOYER_TERMINATION_ARTICLE", "36", "45/2019/QH14"),
    ("HDLD003", 85, "33"): ("RETURN_AFTER_SUSPENSION_ARTICLE", "31", "45/2019/QH14"),
}


def clause_spans(path):
    if not path.is_file():
        return {}
    grouped = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            try:
                start, end = int(row["start_offset"]), int(row["end_offset"])
            except (ValueError, KeyError, TypeError):
                continue
            if start < end:
                grouped.setdefault(row["contract_id"], []).append(
                    (start, end, row["clause_id"])
                )
    return grouped


def collect_references(text_dir, annotations_path, root):
    """Return only non-personal locators. A reference is not legal verification."""
    spans = clause_spans(annotations_path)
    records = []
    for path in sorted(text_dir.glob("HDLD[0-9][0-9][0-9].txt")):
        contract_id = path.stem
        contents = path.read_text(encoding="utf-8-sig")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        offset = 0
        for line_no, line in enumerate(contents.splitlines(keepends=True), 1):
            for match in ARTICLE.finditer(line):
                # Bare section headings such as "Điều 1: ..." are contract
                # structure, not necessarily references to legislation.
                if not line[:match.start()].strip():
                    continue
                article = match.group(1)
                found = KNOWN_QC.get((contract_id, line_no, article))
                absolute = offset + match.start()
                linked = sorted({clause_id for start, end, clause_id in
                                 spans.get(contract_id, []) if start <= absolute < end})
                vicinity = line[max(0, match.start() - 90):match.end() + 90]
                explicitly_law = bool(re.search(
                    r"\b(?:bộ\s*luật|luật|nghị\s*định|thông\s*tư)\b",
                    vicinity, re.IGNORECASE))
                records.append({
                    "contract_id": contract_id,
                    "source_kind": "RAW_TEXT_REFERENCE",
                    "source_text": path.relative_to(root).as_posix(),
                    "source_sha256": digest,
                    "source_line": line_no,
                    "article_number": article,
                    "char_offset": absolute,
                    "linked_clause_ids": ";".join(linked),
                    "citation_context": "LAW_MENTION_NEARBY" if explicitly_law
                                        else "SOURCE_CONTEXT_UNVERIFIED",
                    "suspected_issue": found[0] if found else "UNCLASSIFIED",
                    "candidate_correct_article": found[1] if found else "",
                    "legal_instrument_to_check": found[2] if found else "",
                    "review_status": "HUMAN_LEGAL_REVIEW_REQUIRED",
                    "human_reviewer": "",
                    "human_review_date": "",
                })
            offset += len(line)
    if annotations_path.is_file():
        annotations_hash = hashlib.sha256(annotations_path.read_bytes()).hexdigest()
        with annotations_path.open(encoding="utf-8-sig", newline="") as f:
            for csv_line, row in enumerate(csv.DictReader(f), 2):
                for match in ARTICLE.finditer(row.get("notes", "")):
                    records.append({
                        "contract_id": row["contract_id"],
                        "source_kind": "ANNOTATION_NOTE_REFERENCE",
                        "source_text": annotations_path.relative_to(root).as_posix(),
                        "source_sha256": annotations_hash,
                        "source_line": csv_line,
                        "article_number": match.group(1),
                        "char_offset": "",
                        "linked_clause_ids": row["clause_id"],
                        "citation_context": "ANNOTATION_NOTE_UNVERIFIED",
                        "suspected_issue": "UNCLASSIFIED",
                        "candidate_correct_article": "",
                        "legal_instrument_to_check": "",
                        "review_status": "HUMAN_LEGAL_REVIEW_REQUIRED",
                        "human_reviewer": "",
                        "human_review_date": "",
                    })
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path,
                        default=Path("data/intake/legal_citation_review_queue.csv"))
    args = parser.parse_args()
    root = args.root.resolve()
    records = collect_references(root / "data/processed/raw_text",
                                 root / "data/processed/clauses_v06.csv", root)
    dest = args.output if args.output.is_absolute() else root / args.output
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(records)
    flagged = sum(bool(r["candidate_correct_article"]) for r in records)
    print(f"Citation locators: {len(records)}; suspected mismatches: {flagged}; "
          f"human-reviewed: 0 (queue only)")


if __name__ == "__main__":
    main()
