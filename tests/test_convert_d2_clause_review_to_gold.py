"""A review suggestion cannot become D2 Gold before human adjudication."""

import csv
import hashlib
import json
from datetime import date

import pytest

from scripts.build_d2_clause_label_review_queue import FIELDS
from scripts.convert_d2_clause_review_to_gold import convert_reviewed_queue


def _fixture(tmp_path):
    source = tmp_path / "DOC.txt"
    source.write_text("Alpha. Beta.", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    gold = tmp_path / "DOC.gold_segmentation.json"
    gold.write_text(json.dumps({"source_sha256": digest, "segments": [
        {"gold_clause_ref": "d2seg_0001", "start_char": 0, "end_char": 6,
         "offset_unit": "unicode_code_point"},
        {"gold_clause_ref": "d2seg_0002", "start_char": 7, "end_char": 12,
         "offset_unit": "unicode_code_point"},
    ]}), encoding="utf-8")
    packet = tmp_path / "review.csv"
    rows = []
    for ref, start, end, span, label in [
        ("d2seg_0001", 0, 6, "Alpha.", "JOB_INFO"),
        ("d2seg_0002", 7, 12, "Beta.", "OTHER"),
    ]:
        row = dict.fromkeys(FIELDS, "")
        row.update({
            "document_id": "DOC", "d2_source_sha256": digest,
            "d2_gold_clause_ref": ref, "start_char": str(start), "end_char": str(end),
            "span_sha256": hashlib.sha256(span.encode("utf-8")).hexdigest(),
            "taxonomy_version": "clause_taxonomy_v03", "suggested_labels": label,
            "adjudicated_labels": label, "reviewer_n1": "A", "reviewer_n2": "B",
            "reviewed_on": date.today().isoformat(), "decision": "APPROVED",
        })
        rows.append(row)
    with packet.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    return packet, source, gold


def test_two_person_review_creates_source_pinned_gold(tmp_path):
    packet, source, gold = _fixture(tmp_path)
    result = convert_reviewed_queue(packet, {"DOC": (source, gold)})
    assert [item["labels"] for item in result["DOC"]["items"]] == [["JOB_INFO"], ["OTHER"]]
    assert result["DOC"]["status"] == "GOLD_ADJUDICATED"
    assert result["DOC"]["approval_governance_mode"] == "DUAL_HUMAN_REVIEW_V1"


def test_single_owner_mode_accepts_single_owner_and_blocks_second_reviewer_or_ai(tmp_path):
    packet, source, gold = _fixture(tmp_path)
    with packet.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for r in rows:
        r["reviewer_n1"] = "DucAnh_Owner"
        r["reviewer_n2"] = ""
    with packet.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)

    result = convert_reviewed_queue(
        packet,
        {"DOC": (source, gold)},
        approval_mode="OWNER_SINGLE_APPROVER_AI_ASSISTED_V1",
    )
    assert result["DOC"]["status"] == "GOLD_ADJUDICATED"
    assert result["DOC"]["approval_governance_mode"] == "OWNER_SINGLE_APPROVER_AI_ASSISTED_V1"

    # Non-empty reviewer_n2 in single-owner mode must fail
    rows[0]["reviewer_n2"] = "Second_Person"
    with packet.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="single-owner adjudication invalid"):
        convert_reviewed_queue(
            packet,
            {"DOC": (source, gold)},
            approval_mode="OWNER_SINGLE_APPROVER_AI_ASSISTED_V1",
        )

    # AI token in reviewer_n1 must fail
    for r in rows:
        r["reviewer_n1"] = "ChatGPT_Auditor"
        r["reviewer_n2"] = ""
    with packet.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="single-owner adjudication invalid"):
        convert_reviewed_queue(
            packet,
            {"DOC": (source, gold)},
            approval_mode="OWNER_SINGLE_APPROVER_AI_ASSISTED_V1",
        )


@pytest.mark.parametrize("field,value", [
    ("adjudicated_labels", ""), ("reviewer_n2", "A"),
    ("decision", "PENDING"), ("span_sha256", "0" * 64),
    ("taxonomy_version", "wrong"),
])
def test_incomplete_or_changed_review_fails_closed(tmp_path, field, value):
    packet, source, gold = _fixture(tmp_path)
    with packet.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows[0][field] = value
    with packet.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError):
        convert_reviewed_queue(packet, {"DOC": (source, gold)})


def test_single_owner_rejects_different_names_across_rows(tmp_path):
    packet, source, gold = _fixture(tmp_path)
    with packet.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row, name in zip(rows, ("Human_First", "Human_Second")):
        row["reviewer_n1"] = name
        row["reviewer_n2"] = ""
    with packet.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="inconsistent owner_approver"):
        convert_reviewed_queue(
            packet, {"DOC": (source, gold)},
            approval_mode="OWNER_SINGLE_APPROVER_AI_ASSISTED_V1",
        )


@pytest.mark.parametrize("owner", ["", "Gemini", "owner_approver", "pending"])
def test_owner_mode_never_approves_unreviewed_or_placeholder_rows(tmp_path, owner):
    packet, source, gold = _fixture(tmp_path)
    with packet.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["reviewer_n1"] = owner
        row["reviewer_n2"] = ""
        row["decision"] = "PENDING"
    with packet.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="single-owner adjudication invalid"):
        convert_reviewed_queue(
            packet, {"DOC": (source, gold)},
            approval_mode="OWNER_SINGLE_APPROVER_AI_ASSISTED_V1",
        )


@pytest.mark.parametrize("owner", ["ChatGPT4", "GPT4", "ChatGPT/AI", "Gemini-2.5"])
def test_owner_mode_blocks_ai_aliases_even_on_approved_fixture_rows(tmp_path, owner):
    packet, source, gold = _fixture(tmp_path)
    with packet.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["reviewer_n1"] = owner
        row["reviewer_n2"] = ""
    with packet.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="single-owner adjudication invalid"):
        convert_reviewed_queue(
            packet, {"DOC": (source, gold)},
            approval_mode="OWNER_SINGLE_APPROVER_AI_ASSISTED_V1",
        )
