"""Build a metadata-only visual-review queue from an OCR-only legal candidate."""

import argparse
import csv
import re
import tempfile
from collections import defaultdict
from pathlib import Path

PAGE_MARKER = re.compile(r"^===== PDF_PAGE (\d{3}) \| OCR_CANDIDATE =====$", re.MULTILINE)
ARTICLE_HEADING = re.compile(r"^\s*(?:Ñ\s+)?Điều\s+(\d{1,3})\b", re.MULTILINE | re.IGNORECASE)
SHA256 = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)
FIELDS = (
    "article_no",
    "occurrence_count",
    "pages",
    "detection_status",
    "review_status",
    "source_sha256",
)


def parse_ocr_candidate(candidate: str) -> tuple[str, list[str]]:
    """Read page blocks only from a hash-labelled, explicitly unproofread OCR file."""
    if not isinstance(candidate, str):
        raise TypeError("OCR candidate must be text")
    status = re.search(r"(?m)^STATUS: (.+)$", candidate)
    source_hash = re.search(r"(?m)^SOURCE_SHA256: ([0-9a-fA-F]{64})$", candidate)
    page_count_match = re.search(r"(?m)^PAGE_COUNT: (\d+)$", candidate)
    if status is None or status.group(1) != "OCR_CANDIDATE_UNPROOFREAD":
        raise ValueError("input must be an unproofread OCR candidate")
    if source_hash is None or page_count_match is None:
        raise ValueError("OCR candidate is missing source or page metadata")
    page_count = int(page_count_match.group(1))
    markers = list(PAGE_MARKER.finditer(candidate))
    page_numbers = [int(marker.group(1)) for marker in markers]
    if page_numbers != list(range(1, page_count + 1)):
        raise ValueError("OCR candidate must have ordered page markers")
    pages = []
    for index, marker in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(candidate)
        pages.append(candidate[marker.end():end].strip())
    return source_hash.group(1).lower(), pages


def build_review_rows(
    pages: list[str], article_count: int, source_sha256: str
) -> list[dict[str, str]]:
    """Return one metadata-only review row per expected article number."""
    if isinstance(article_count, bool) or not isinstance(article_count, int) or article_count < 1:
        raise ValueError("article_count must be a positive integer")
    if not isinstance(source_sha256, str) or SHA256.fullmatch(source_sha256) is None:
        raise ValueError("source SHA-256 must be 64 hexadecimal characters")
    if not isinstance(pages, list) or any(not isinstance(page, str) for page in pages):
        raise ValueError("pages must be a list of text blocks")

    occurrences: dict[int, list[int]] = defaultdict(list)
    for page_no, page_text in enumerate(pages, 1):
        for match in ARTICLE_HEADING.finditer(page_text):
            article_no = int(match.group(1))
            if article_no <= article_count:
                occurrences[article_no].append(page_no)

    rows = []
    for article_no in range(1, article_count + 1):
        found_pages = occurrences.get(article_no, [])
        rows.append({
            "article_no": str(article_no),
            "occurrence_count": str(len(found_pages)),
            "pages": ";".join(str(page_no) for page_no in sorted(set(found_pages))),
            "detection_status": "OCR_HEADING_CANDIDATE" if found_pages else "NOT_DETECTED_BY_OCR",
            "review_status": "PENDING_VISUAL_REVIEW",
            "source_sha256": source_sha256.lower(),
        })
    return rows


def write_review_queue(output_path: Path, rows: list[dict[str, str]]) -> None:
    """Write the non-text review queue atomically and never overwrite a file."""
    output_path = Path(output_path)
    if output_path.exists():
        raise ValueError("refusing to overwrite existing article review queue")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=output_path.parent,
            prefix=f"{output_path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        temp_path.replace(output_path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    restricted = root / "data/intake/restricted/legal_sources"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path,
        default=restricted / "BLLD_18_VBHN_2026_ocr_candidate_utf8.txt",
    )
    parser.add_argument(
        "--output", type=Path,
        default=restricted / "BLLD_18_VBHN_2026_article_review_queue.csv",
    )
    parser.add_argument("--article-count", type=int, default=220)
    args = parser.parse_args()
    source_hash, pages = parse_ocr_candidate(args.input.read_text(encoding="utf-8"))
    rows = build_review_rows(pages, args.article_count, source_hash)
    write_review_queue(args.output, rows)
    detected = sum(row["detection_status"] == "OCR_HEADING_CANDIDATE" for row in rows)
    occurrences = sum(int(row["occurrence_count"]) for row in rows)
    print(
        f"Review queue written: {len(rows)} articles; {detected} detected; "
        f"{len(rows) - detected} not detected; {occurrences} heading matches; "
        "all rows pending visual review."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
