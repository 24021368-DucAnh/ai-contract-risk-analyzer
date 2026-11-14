"""Prepare a restricted D2 clause-label review queue from source-pinned D1 Gold."""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

FIELDS = (
    "document_id", "d2_source_sha256", "d2_gold_clause_ref", "start_char", "end_char",
    "span_sha256", "d1_source_sha256", "d1_gold_clause_ref", "taxonomy_version",
    "suggested_labels", "adjudicated_labels", "transfer_status", "reviewer_n1",
    "reviewer_n2", "reviewed_on", "decision", "decision_note",
)


def _read_gold(text_path: Path, gold_path: Path) -> tuple[str, str, list[dict]]:
    raw = text_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    if gold.get("source_sha256") != digest:
        raise ValueError(f"Gold/source SHA-256 mismatch: {gold_path}")
    return raw.decode("utf-8"), digest, gold["segments"]


def _span(text: str, item: dict) -> str:
    start, end = item["start_char"], item["end_char"]
    if (item.get("offset_unit") != "unicode_code_point" or not isinstance(start, int)
            or not isinstance(end, int) or start < 0 or end <= start or end > len(text)):
        raise ValueError("invalid Gold code-point span")
    return text[start:end]


def build_queue(
    documents: list[tuple[str, Path, Path, Path, Path, Path]], output: Path,
) -> dict[str, int]:
    """Suggest labels only for exact unique spans; leave all decisions empty."""
    rows: list[dict[str, str]] = []
    seen_documents: set[str] = set()
    for doc_id, d1_text_path, d1_gold_path, d1_labels_path, d2_text_path, d2_gold_path in documents:
        if doc_id in seen_documents:
            raise ValueError(f"duplicate document: {doc_id}")
        seen_documents.add(doc_id)
        d1_text, d1_sha, d1_segments = _read_gold(d1_text_path, d1_gold_path)
        d2_text, d2_sha, d2_segments = _read_gold(d2_text_path, d2_gold_path)
        d1_labels = json.loads(d1_labels_path.read_text(encoding="utf-8"))
        if d1_labels.get("taxonomy_version", "clause_taxonomy_v03") != "clause_taxonomy_v03":
            raise ValueError("D1 Gold taxonomy is not clause_taxonomy_v03")
        labels_by_ref = {}
        for item in d1_labels["items"]:
            ref = item["clause_id"]
            if ref in labels_by_ref or not isinstance(item["labels"], list):
                raise ValueError(f"duplicate or invalid D1 Gold label: {ref}")
            labels_by_ref[ref] = item["labels"]
        candidates: dict[str, list[str]] = defaultdict(list)
        for segment in d1_segments:
            ref = segment["gold_clause_ref"]
            if ref in labels_by_ref:
                candidates[_span(d1_text, segment)].append(ref)
        for segment in d2_segments:
            text = _span(d2_text, segment)
            matches = candidates.get(text, [])
            matched_ref = matches[0] if len(matches) == 1 else ""
            status = "EXACT_UNIQUE_PENDING_REVIEW" if matched_ref else "UNMATCHED_PENDING_REVIEW"
            rows.append({
                "document_id": doc_id, "d2_source_sha256": d2_sha,
                "d2_gold_clause_ref": segment["gold_clause_ref"],
                "start_char": str(segment["start_char"]), "end_char": str(segment["end_char"]),
                "span_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "d1_source_sha256": d1_sha, "d1_gold_clause_ref": matched_ref,
                "taxonomy_version": "clause_taxonomy_v03",
                "suggested_labels": ";".join(labels_by_ref[matched_ref]) if matched_ref else "",
                "adjudicated_labels": "",
                "transfer_status": status, "reviewer_n1": "", "reviewer_n2": "",
                "reviewed_on": "", "decision": "", "decision_note": "",
            })
    if not rows:
        raise ValueError("no D2 Gold segments")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return dict(Counter(row["transfer_status"] for row in rows))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restricted-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.restricted_root
    paths = [(
        f"HDLD{number:03}",
        root / f"D1_m1_runtime_predictions_v01/HDLD{number:03}.canonical_nfc.txt",
        root / f"D1_m1_gold_v01/HDLD{number:03}.gold_segmentation.json",
        root / f"D1_clause_label_gold_v01/HDLD{number:03}.gold_clause_labels.json",
        root / f"D2_candidate_v02/HDLD{number:03}.d2_candidate.txt",
        root / f"D2_segmentation_gold_v02/HDLD{number:03}.gold_segmentation.json",
    ) for number in range(1, 5)]
    print(build_queue(paths, args.output))
