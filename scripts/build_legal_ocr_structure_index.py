"""Build an OCR-derived, metadata-only review index for legal hierarchy."""

from __future__ import annotations

import argparse
import csv
import os
import re
import tempfile
from collections import defaultdict
from pathlib import Path

# Vietnamese legal article headings use a delimiter after the article number.
# Without it, line-start citations such as "Điều 12 của Bộ luật này" become
# false headings and can hide genuinely missed articles.
ARTICLE_RE = re.compile(r"^\s*(?:Ñ\s+)?[ĐD]iều\s+(\d{1,3})\s*[.．:]\s*(.*)$", re.IGNORECASE)
CLAUSE_RE = re.compile(r"^\s*(\d{1,3})\s*[.)]\s+")
POINT_RE = re.compile(r"^\s*([a-zđ])\)\s+", re.IGNORECASE)
HEADER_RE = re.compile(r"^===== PDF_PAGE (\d{3,}) \| OCR_CANDIDATE =====$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

FIELDS = (
    "node_type", "node_id", "parent_id", "source_id", "document_number",
    "article_no", "clause_no", "point_label", "source_pages",
    "occurrence_count", "source_sha256", "structure_evidence",
    "legal_review_status",
)


def parse_candidate(candidate: str) -> tuple[str, dict[int, str]]:
    lines = candidate.lstrip("\ufeff").splitlines()
    if not lines or lines[0] != "STATUS: OCR_CANDIDATE_UNPROOFREAD":
        raise ValueError("Input must be marked OCR_CANDIDATE_UNPROOFREAD")
    hash_headers = [line for line in lines if line.startswith("SOURCE_SHA256: ")]
    page_headers = [line for line in lines if line.startswith("PAGE_COUNT: ")]
    if len(hash_headers) != 1:
        raise ValueError("Missing source hash header")
    source_hash = hash_headers[0].split(":", 1)[1].strip()
    if not SHA_RE.fullmatch(source_hash):
        raise ValueError("Invalid source hash")
    if len(page_headers) != 1:
        raise ValueError("Missing page count header")
    try:
        expected_pages = int(page_headers[0].split(":", 1)[1].strip())
    except ValueError as exc:
        raise ValueError("Invalid page count") from exc
    pages: dict[int, list[str]] = {}
    current_page = None
    for line in lines[3:]:
        match = HEADER_RE.fullmatch(line)
        if match:
            current_page = int(match.group(1))
            if current_page in pages:
                raise ValueError(f"Duplicate page marker: {current_page}")
            pages[current_page] = []
        elif current_page is not None:
            pages[current_page].append(line)
    if len(pages) != expected_pages or list(pages) != list(range(1, expected_pages + 1)):
        raise ValueError("Page markers must be complete, ordered, and match PAGE_COUNT")
    return source_hash, {number: "\n".join(content) for number, content in pages.items()}


def _article_occurrences(pages: dict[int, str]) -> dict[int, list[tuple[int, list[tuple[int, str]]]]]:
    occurrences: dict[int, list[tuple[int, list[tuple[int, str]]]]] = defaultdict(list)
    current_number = None
    current_page = None
    current_lines: list[tuple[int, str]] = []

    def flush() -> None:
        if current_number is not None:
            occurrences[current_number].append((current_page, current_lines.copy()))

    for page_no, content in pages.items():
        for line in content.splitlines():
            match = ARTICLE_RE.match(line)
            if match:
                flush()
                number = int(match.group(1))
                if 1 <= number <= 999:
                    current_number = number
                    current_page = page_no
                    current_lines = [(page_no, line)]
                else:
                    current_number = None
                    current_lines = []
            elif current_number is not None:
                current_lines.append((page_no, line))
    flush()
    return occurrences


def _parse_children(occurrences: list[tuple[int, list[tuple[int, str]]]]):
    # Select the fullest occurrence (typically the body rather than a contents entry).
    _, lines = max(occurrences, key=lambda item: sum(bool(line.strip()) for _, line in item[1]))
    clause_pages: dict[int, set[int]] = defaultdict(set)
    clause_occurrences: dict[int, int] = defaultdict(int)
    point_pages: dict[tuple[int, str], set[int]] = defaultdict(set)
    point_occurrences: dict[tuple[int, str], int] = defaultdict(int)
    current_clause = None
    for page_no, line in lines:
        if ARTICLE_RE.match(line):
            continue
        clause_match = CLAUSE_RE.match(line)
        if clause_match:
            current_clause = int(clause_match.group(1))
            clause_pages[current_clause].add(page_no)
            clause_occurrences[current_clause] += 1
            continue
        point_match = POINT_RE.match(line)
        if current_clause is not None and point_match:
            label = point_match.group(1).lower()
            key = (current_clause, label)
            point_pages[key].add(page_no)
            point_occurrences[key] += 1
    return clause_pages, clause_occurrences, point_pages, point_occurrences


def _page_list(values: set[int]) -> str:
    return ";".join(str(value) for value in sorted(values))


def build_structure_index(
    candidate: str,
    *,
    document_id: str,
    document_number: str,
    article_count: int,
) -> list[dict[str, str]]:
    if article_count < 1:
        raise ValueError("article_count must be positive")
    source_hash, pages = parse_candidate(candidate)
    occurrences = _article_occurrences(pages)
    rows: list[dict[str, str]] = []

    def add(**values: object) -> None:
        row = {field: "" for field in FIELDS}
        row.update({key: str(value) for key, value in values.items()})
        row["source_sha256"] = source_hash
        row["legal_review_status"] = "PENDING_LEGAL_REVIEW"
        rows.append(row)

    add(
        node_type="document", node_id=document_id, parent_id="", source_id=document_id,
        document_number=document_number, article_no="", clause_no="", point_label="",
        source_pages=";".join(map(str, pages)), occurrence_count="1",
        structure_evidence="OCR_SOURCE_METADATA_ONLY",
    )

    for article_no in range(1, article_count + 1):
        article_id = f"{document_id}:art:{article_no}"
        found = occurrences.get(article_no, [])
        selected = (max(found, key=lambda item: sum(bool(line.strip()) for _, line in item[1]))
                    if found else None)
        page_set = {page for page, _ in selected[1]} if selected else set()
        add(
            node_type="article", node_id=article_id, parent_id=document_id,
            source_id=document_id, document_number=document_number, article_no=article_no,
            clause_no="", point_label="", source_pages=_page_list(page_set),
            occurrence_count=len(found),
            structure_evidence=("OCR_HEADING_CANDIDATE" if found else
                                "OCR_ARTICLE_NOT_DETECTED; MANUAL_SEARCH_REQUIRED"),
        )
        if not found:
            continue
        clause_pages, clause_counts, point_pages, point_counts = _parse_children(found)
        for clause_no in sorted(clause_pages):
            clause_id = f"{article_id}:clause:{clause_no}"
            add(
                node_type="clause", node_id=clause_id, parent_id=article_id,
                source_id=document_id, document_number=document_number, article_no=article_no,
                clause_no=clause_no, point_label="", source_pages=_page_list(clause_pages[clause_no]),
                occurrence_count=clause_counts[clause_no],
                structure_evidence="OCR_CLAUSE_NUMBER_CANDIDATE",
            )
            for (point_clause, label) in sorted(point_pages):
                if point_clause != clause_no:
                    continue
                add(
                    node_type="point", node_id=f"{clause_id}:point:{label}", parent_id=clause_id,
                    source_id=document_id, document_number=document_number, article_no=article_no,
                    clause_no=clause_no, point_label=label,
                    source_pages=_page_list(point_pages[(point_clause, label)]),
                    occurrence_count=point_counts[(point_clause, label)],
                    structure_evidence="OCR_POINT_LABEL_CANDIDATE",
                )
    return rows


def write_index(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing index: {output_path}")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{output_path.name}.", suffix=".tmp", dir=output_path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="raise")
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        # Hard-link creation is atomic and fails if another process created the destination.
        os.link(temporary_name, output_path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--document-number", required=True)
    parser.add_argument("--article-count", required=True, type=int)
    args = parser.parse_args()
    candidate = args.candidate.read_text(encoding="utf-8-sig")
    rows = build_structure_index(candidate, document_id=args.document_id,
                                 document_number=args.document_number,
                                 article_count=args.article_count)
    write_index(rows, args.output)
    print(f"Wrote {len(rows)} pending-review hierarchy rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
