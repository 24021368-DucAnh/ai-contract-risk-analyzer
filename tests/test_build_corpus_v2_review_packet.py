import csv
import hashlib
import json
from pathlib import Path

import pytest

from scripts.build_corpus_v2_review_packet import build_review_packet


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_review_packet_keeps_ocr_text_private_and_requires_human_decision(tmp_path):
    source = tmp_path / "official.pdf"
    source.write_bytes(b"%PDF-test")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    candidates = tmp_path / "candidates.jsonl"
    candidates.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in [
        {
            "node_type": "clause", "node_id": "LAW:art:25:clause:1",
            "article_no": "25", "clause_no": "1", "point_label": "",
            "candidate_text_pages": [11], "ocr_text_candidate": "Chữ OCR chưa soát",
            "source_id": "LAW", "source_sha256": digest,
            "legal_review_status": "PENDING_LEGAL_REVIEW", "runtime_eligible": False,
        },
        {
            "node_type": "article", "node_id": "LAW:art:99",
            "article_no": "99", "clause_no": "", "point_label": "",
            "candidate_text_pages": [30], "ocr_text_candidate": "Ngoài phạm vi",
            "source_id": "LAW", "source_sha256": digest,
            "legal_review_status": "PENDING_LEGAL_REVIEW", "runtime_eligible": False,
        },
    ]) + "\n", encoding="utf-8")
    public, private = tmp_path / "metadata.csv", tmp_path / "restricted.csv"

    count = build_review_packet(
        candidates, source, public, private, article_numbers={25},
        source_id="LAW", source_url="https://official.example/law",
        accessed_on="2026-11-15",
    )

    assert count == 1
    assert "Chữ OCR chưa soát" not in public.read_text(encoding="utf-8")
    assert "Chữ OCR chưa soát" in private.read_text(encoding="utf-8")
    assert _rows(public)[0]["review_status"] == "PENDING_REVIEW"
    assert _rows(private)[0]["verified_text"] == ""
    assert _rows(private)[0]["reviewer_n2"] == ""
    assert _rows(private)[0]["reviewer_independent"] == ""


def test_review_packet_rejects_unmatched_source_hash(tmp_path):
    source = tmp_path / "official.pdf"
    source.write_bytes(b"other")
    candidates = tmp_path / "candidates.jsonl"
    candidates.write_text(json.dumps({
        "node_type": "clause", "node_id": "LAW:art:25:clause:1",
        "article_no": "25", "clause_no": "1", "point_label": "",
        "candidate_text_pages": [11], "ocr_text_candidate": "candidate",
        "source_id": "LAW", "source_sha256": "0" * 64,
        "legal_review_status": "PENDING_LEGAL_REVIEW", "runtime_eligible": False,
    }) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="source SHA-256"):
        build_review_packet(
            candidates, source, tmp_path / "public.csv", tmp_path / "private.csv",
            article_numbers={25}, source_id="LAW",
            source_url="https://official.example/law", accessed_on="2026-11-15",
        )
    assert not (tmp_path / "public.csv").exists()
