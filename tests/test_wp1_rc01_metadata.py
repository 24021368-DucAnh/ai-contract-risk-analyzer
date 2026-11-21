"""Public metadata must describe the approved artifact without activating runtime."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/intake/corpus_v2_wp1_rc01_release_metadata_2026-11-21.json"
REG = ROOT / "data/intake/corpus_v2_source_register_2026-11-15.csv"


def test_rc01_metadata_records_exact_scope_and_approval_boundary():
    meta = json.loads(META.read_text(encoding="utf-8"))
    assert meta["schema_version"] == "wp1_rc01_release_metadata_v1"
    assert meta["approval_status"] == "OWNER_APPROVED_LOCAL_ARTIFACT"
    assert meta["approval_policy"] == "OWNER_SINGLE_APPROVER_AI_ASSISTED_V1"
    assert meta["runtime_counts"] == {
        "provisions": 30, "articles": 8, "manual_edges": 2,
        "structural_parent_edges": 13, "clause_labels": 9, "label_citation_pairs": 19,
    }
    assert meta["pipeline_runtime_pin_changed"] is False
    assert meta["data_remote_commit_pin"] is None
    assert meta["gold_d2_approved"] is False
    assert meta["dev_m8_v2_measured"] is False
    assert meta["automated_scan_status"] == "PENDING_MANUAL_REVIEW_SCAN_PDF"
    assert "provisions" not in meta and "content" not in meta


def test_registry_decisions_are_scoped_and_tt10_is_not_active():
    with REG.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 9 and len({r["source_id"] for r in rows}) == 9
    for r in rows:
        if r["source_id"].startswith("LAW-BLLD-"):
            assert r["legal_review_status"] == "OWNER_APPROVED_WP1_RC01_SCOPE_ONLY"
            assert r["rights_status"] == "INTERNAL_REPO_ONLY"
        else:
            assert r["rights_status"] == "HOLD_OR_METADATA_ONLY"
    tt10 = next(r for r in rows if r["source_id"] == "LAW-TT-10-2020")
    assert tt10["legal_review_status"] == "HOLD_OR_METADATA_ONLY"
    meta = json.loads(META.read_text(encoding="utf-8"))
    assert "LAW-TT-10-2020" not in meta["runtime_source_ids"]
    assert len(meta["runtime_source_ids"]) == 3
    assert all(len(v) == 64 for v in meta["release_checksums"].values())
