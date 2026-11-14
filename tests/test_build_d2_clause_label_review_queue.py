"""D1 labels may be suggested for D2 only on identical, source-pinned spans."""

import csv
import hashlib
import json

from scripts.build_d2_clause_label_review_queue import build_queue


def _write_gold(path, source_text, segments):
    path.write_text(json.dumps({
        "source_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        "segments": segments,
    }), encoding="utf-8")


def test_exact_unique_spans_only_and_no_automatic_gold(tmp_path):
    d1, d2 = tmp_path / "d1", tmp_path / "d2"
    d1.mkdir()
    d2.mkdir()
    (d1 / "text.txt").write_text("Alpha. Beta.", encoding="utf-8")
    (d2 / "text.txt").write_text("Alpha. Changed.", encoding="utf-8")
    _write_gold(d1 / "seg.json", "Alpha. Beta.", [
        {"gold_clause_ref": "C1", "start_char": 0, "end_char": 6, "offset_unit": "unicode_code_point"},
        {"gold_clause_ref": "C2", "start_char": 7, "end_char": 12, "offset_unit": "unicode_code_point"},
    ])
    _write_gold(d2 / "seg.json", "Alpha. Changed.", [
        {"gold_clause_ref": "D1", "start_char": 0, "end_char": 6, "offset_unit": "unicode_code_point"},
        {"gold_clause_ref": "D2", "start_char": 7, "end_char": 15, "offset_unit": "unicode_code_point"},
    ])
    (d1 / "labels.json").write_text(json.dumps({"items": [
        {"clause_id": "C1", "labels": ["JOB_INFO"]},
        {"clause_id": "C2", "labels": ["OTHER"]},
    ]}), encoding="utf-8")
    output = tmp_path / "review.csv"
    summary = build_queue([("DOC", d1 / "text.txt", d1 / "seg.json", d1 / "labels.json",
                            d2 / "text.txt", d2 / "seg.json")], output)
    with output.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert summary == {"EXACT_UNIQUE_PENDING_REVIEW": 1, "UNMATCHED_PENDING_REVIEW": 1}
    assert rows[0]["suggested_labels"] == "JOB_INFO"
    assert rows[0]["reviewer_n1"] == rows[0]["reviewer_n2"] == ""
    assert rows[0]["decision"] == ""
    assert rows[0]["adjudicated_labels"] == ""
    assert rows[1]["suggested_labels"] == ""


def test_source_hash_mismatch_rejected(tmp_path):
    source = tmp_path / "text.txt"
    source.write_text("text", encoding="utf-8")
    seg = tmp_path / "seg.json"
    seg.write_text(json.dumps({"source_sha256": "0" * 64, "segments": []}), encoding="utf-8")
    labels = tmp_path / "labels.json"
    labels.write_text('{"items":[]}', encoding="utf-8")
    try:
        build_queue([("DOC", source, seg, labels, source, seg)], tmp_path / "out.csv")
    except ValueError as exc:
        assert "SHA-256" in str(exc)
    else:
        raise AssertionError("mismatched Gold source hash was accepted")
