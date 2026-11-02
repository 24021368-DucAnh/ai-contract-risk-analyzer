"""Build a metadata-only review queue for draft legal corpus provisions."""

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


FIELDS = (
    "document_id",
    "citation_id",
    "article",
    "source_sha256",
    "ocr_candidate_sha256",
    "ocr_article_pages",
    "provision_sha256",
    "text_match_status",
    "verbatim_text_verified",
    "effective_interval_verified",
    "amendment_chain_verified",
    "review_status",
    "data_reviewer",
    "legal_reviewer",
    "review_date",
    "decision",
    "notes",
)
PAGE_MARKER = re.compile(r"^===== PDF_PAGE (\d+)\b.*=====\s*$", re.MULTILINE)
SOURCE_HASH = re.compile(r"^SOURCE_SHA256:\s*([0-9a-fA-F]{64})\s*$", re.MULTILINE)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


def _source_pages(ocr_text: str) -> tuple[str, str, dict[int, str]]:
    receipt = SOURCE_HASH.search(ocr_text)
    if receipt is None:
        raise ValueError("OCR candidate is missing a valid SOURCE_SHA256 receipt")
    markers = list(PAGE_MARKER.finditer(ocr_text))
    if not markers:
        raise ValueError("OCR candidate has no PDF_PAGE markers")
    pages: dict[int, str] = {}
    for index, marker in enumerate(markers):
        page = int(marker.group(1))
        if page in pages:
            raise ValueError("OCR candidate contains duplicate PDF page markers")
        stop = markers[index + 1].start() if index + 1 < len(markers) else len(ocr_text)
        pages[page] = ocr_text[marker.end():stop]
    return receipt.group(1).lower(), hashlib.sha256(ocr_text.encode("utf-8")).hexdigest(), pages


def build_review_queue(provisions: list[dict[str, Any]], ocr_text: str) -> list[dict[str, str]]:
    """Map draft provisions to OCR page hints without copying text or approving it."""
    source_sha256, ocr_sha256, pages = _source_pages(ocr_text)
    seen: set[str] = set()
    page_items = sorted(pages.items())
    all_ocr = _normalize("\n".join(pages[page] for page, _ in page_items))
    rows: list[dict[str, str]] = []

    for provision in provisions:
        citation_id = provision.get("citation_id")
        article = provision.get("article")
        content = provision.get("content")
        document_id = provision.get("document_id")
        if not all(isinstance(value, str) and value.strip() for value in (citation_id, article, content, document_id)):
            raise ValueError("each provision requires non-empty document_id, citation_id, article and content")
        if citation_id in seen:
            raise ValueError(f"duplicate citation_id: {citation_id}")
        seen.add(citation_id)

        article_pattern = re.compile(rf"(?<!\w)Điều\s+{re.escape(article)}\s*[.:]", re.IGNORECASE)
        article_pages = [page for page, page_text in page_items if article_pattern.search(page_text)]
        normalized_content = _normalize(content)
        row = {
            "document_id": document_id,
            "citation_id": citation_id,
            "article": article,
            "source_sha256": source_sha256,
            "ocr_candidate_sha256": ocr_sha256,
            "ocr_article_pages": ";".join(str(page) for page in article_pages),
            "provision_sha256": hashlib.sha256(normalized_content.encode("utf-8")).hexdigest(),
            "text_match_status": "OCR_EXACT_NORMALIZED" if normalized_content in all_ocr else "NO_EXACT_OCR_MATCH",
            "verbatim_text_verified": "NO",
            "effective_interval_verified": "NO",
            "amendment_chain_verified": "NO",
            "review_status": "PENDING_VISUAL_LEGAL_REVIEW",
            "data_reviewer": "",
            "legal_reviewer": "",
            "review_date": "",
            "decision": "",
            "notes": "OCR match and page numbers are navigation hints only; verify against signed PDF and amendment history.",
        }
        rows.append(row)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provisions", required=True, type=Path, help="draft provisions.jsonl")
    parser.add_argument("--ocr", required=True, type=Path, help="OCR candidate with SOURCE_SHA256 and PDF_PAGE markers")
    parser.add_argument("--output", required=True, type=Path, help="new metadata-only CSV path")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {args.output}")
    provisions = [
        json.loads(line, object_pairs_hook=_unique_object)
        for line in args.provisions.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    rows = build_review_queue(provisions, args.ocr.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Review queue rows: {len(rows)}; all pending; output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
