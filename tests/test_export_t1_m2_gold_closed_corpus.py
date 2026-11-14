"""Synthetic scope-gate checks; no held-out text is used."""

import csv
import json

import pytest

from scripts.export_t1_m2_gold_closed_corpus import export

FIELDS = (
    "annotation_unit_id", "contract_id", "clause_id", "role", "start_char",
    "end_char", "source_sha256", "candidate_outcome", "candidate_risk_label_1",
    "candidate_basis_type_1", "candidate_citation_id_1", "annotator_id",
    "reviewer_id", "adjudicator_id", "review_status", "scope_status", "notes",
)


def packet_rows():
    rows = []
    for number in range(5, 14):
        doc = f"HDLD{number:03d}"
        for index in range(83):
            clause = f"{doc}_C{index:03d}"
            for role in ("EMPLOYEE", "EMPLOYER"):
                ordinal = len(rows)
                positive = 17 <= ordinal < 20
                exception = ordinal < 17
                rows.append({
                    "annotation_unit_id": f"{clause}::{role}",
                    "contract_id": doc, "clause_id": clause, "role": role,
                    "start_char": str(index * 20), "end_char": str(index * 20 + 10),
                    "source_sha256": "a" * 64,
                    "candidate_outcome": "RISK" if positive else "NO_RISK",
                    "candidate_risk_label_1": "BONUS_BENEFITS" if positive else "",
                    "candidate_basis_type_1": "AMBIGUOUS" if positive else "",
                    "candidate_citation_id_1": "BLLD2019:art21:cl1:ptđ" if positive else "",
                    "annotator_id": "DucAnh_N2", "reviewer_id": "argon",
                    "adjudicator_id": "Minh_N1", "review_status": "ADJUDICATED",
                    "scope_status": ("CORPUS_V1_SCOPE_EXCEPTION" if exception else
                                     "IN_CORPUS_ADJUDICATED" if positive else
                                     "IN_CORPUS_VERIFIED"),
                    "notes": "outside closed corpus" if exception else "",
                })
    return rows


def write_packet(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_export_preserves_scope_exclusions(tmp_path):
    packet, corpus, output = tmp_path / "packet.csv", tmp_path / "corpus.jsonl", tmp_path / "gold"
    write_packet(packet, packet_rows())
    corpus.write_text(json.dumps({"citation_id": "BLLD2019:art21:cl1:ptđ"}), encoding="utf-8")
    result = export(packet, corpus, output)
    assert result["evaluation_ready"] is True
    assert len(result["excluded_corpus_scope_unit_ids"]) == 17
    assert result["scope_counts"]["IN_CORPUS_VERIFIED"] == 1474
    assert result["positive_items"] == 3
    with pytest.raises(ValueError, match="already exists"):
        export(packet, corpus, output)


def test_export_rejects_exception_without_note(tmp_path):
    packet, corpus = tmp_path / "packet.csv", tmp_path / "corpus.jsonl"
    rows = packet_rows()
    rows[0]["notes"] = ""
    write_packet(packet, rows)
    corpus.write_text(json.dumps({"citation_id": "BLLD2019:art21:cl1:ptđ"}), encoding="utf-8")
    with pytest.raises(ValueError, match="invalid corpus exception"):
        export(packet, corpus, tmp_path / "gold")
