"""Build a private OCR review packet and a public, text-free metadata queue."""

import argparse
import csv
import hashlib
import json
from datetime import date
from pathlib import Path

PUBLIC_FIELDS = (
    "node_id", "source_id", "source_url", "source_sha256", "candidate_sha256",
    "accessed_on", "article", "clause", "point", "source_pages",
    "candidate_text_sha256", "review_status",
)
PRIVATE_FIELDS = (*PUBLIC_FIELDS, "ocr_candidate_text", "verified_text", "amendment_chain",
                  "effective_from", "effective_to", "reviewer_n2", "reviewer_independent",
                  "reviewed_on", "decision_note")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_review_packet(
    candidates: Path,
    source_pdf: Path,
    public_output: Path,
    private_output: Path,
    *,
    article_numbers: set[int],
    source_id: str,
    source_url: str,
    accessed_on: str,
) -> int:
    """Select priority articles without turning an OCR candidate into approved law."""
    date.fromisoformat(accessed_on)
    if not article_numbers or public_output.resolve() == private_output.resolve():
        raise ValueError("article selection and separate outputs are required")
    source_sha = _sha256(source_pdf)
    candidate_sha = _sha256(candidates)
    public_rows: list[dict[str, str]] = []
    private_rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in candidates.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if not str(row.get("article_no", "")).isdigit() or int(row["article_no"]) not in article_numbers:
            continue
        if row.get("source_id") != source_id or row.get("source_sha256") != source_sha:
            raise ValueError("candidate source SHA-256 or source ID does not match official file")
        if row.get("runtime_eligible") or row.get("legal_review_status") != "PENDING_LEGAL_REVIEW":
            raise ValueError("review packet accepts only unapproved candidates")
        node_id = row["node_id"]
        if node_id in seen:
            raise ValueError(f"duplicate candidate node ID: {node_id}")
        seen.add(node_id)
        candidate_text = row["ocr_text_candidate"]
        if not isinstance(candidate_text, str) or not candidate_text.strip():
            raise ValueError(f"empty OCR candidate: {node_id}")
        pages = row["candidate_text_pages"]
        if not isinstance(pages, list) or not pages or any(not isinstance(p, int) or p < 1 for p in pages):
            raise ValueError(f"invalid page reference: {node_id}")
        item = {
            "node_id": node_id,
            "source_id": source_id,
            "source_url": source_url,
            "source_sha256": source_sha,
            "candidate_sha256": candidate_sha,
            "accessed_on": accessed_on,
            "article": row["article_no"],
            "clause": row["clause_no"],
            "point": row["point_label"],
            "source_pages": ";".join(str(p) for p in pages),
            "candidate_text_sha256": hashlib.sha256(candidate_text.encode("utf-8")).hexdigest(),
            "review_status": "PENDING_REVIEW",
        }
        public_rows.append(item)
        private_rows.append({
            **item, "ocr_candidate_text": candidate_text, "verified_text": "",
            "amendment_chain": "", "effective_from": "", "effective_to": "",
            "reviewer_n2": "", "reviewer_independent": "", "reviewed_on": "",
            "decision_note": "",
        })
    if not public_rows:
        raise ValueError("no candidate nodes matched requested articles")
    public_rows.sort(key=lambda x: (int(x["article"]), x["node_id"]))
    private_rows.sort(key=lambda x: (int(x["article"]), x["node_id"]))
    _write_csv(private_output, PRIVATE_FIELDS, private_rows)
    _write_csv(public_output, PUBLIC_FIELDS, public_rows)
    return len(public_rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--source-pdf", type=Path, required=True)
    parser.add_argument("--public-output", type=Path, required=True)
    parser.add_argument("--private-output", type=Path, required=True)
    parser.add_argument("--articles", required=True, help="Comma-separated article numbers")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--accessed-on", required=True)
    args = parser.parse_args()
    count = build_review_packet(
        args.candidates, args.source_pdf, args.public_output, args.private_output,
        article_numbers={int(x) for x in args.articles.split(",")},
        source_id=args.source_id, source_url=args.source_url, accessed_on=args.accessed_on,
    )
    print(f"Prepared {count} unapproved legal-source candidates")
