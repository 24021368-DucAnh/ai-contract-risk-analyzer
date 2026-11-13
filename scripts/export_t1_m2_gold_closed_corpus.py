"""Export a reviewed T1 M2 packet for the versioned 16-node corpus scope.

Metadata only. Never reads T1 contract text or silently converts scope exceptions
to verified negative examples.
"""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


def export(packet: Path, corpus: Path, output: Path) -> dict:
    if output.exists():
        raise ValueError("output directory already exists")
    with packet.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 1494:
        raise ValueError("expected 1494 role-specific rows")
    needed = {"annotation_unit_id", "contract_id", "clause_id", "role",
              "start_char", "end_char", "source_sha256", "candidate_outcome",
              "candidate_risk_label_1", "candidate_basis_type_1",
              "candidate_citation_id_1", "annotator_id", "reviewer_id",
              "adjudicator_id", "review_status", "scope_status", "notes"}
    if not needed.issubset(rows[0]):
        raise ValueError("missing review or scope columns")
    citations = {json.loads(line)["citation_id"] for line in
                 corpus.read_text(encoding="utf-8-sig").splitlines() if line.strip()}
    seen = set()
    clause_roles = defaultdict(list)
    by_doc = defaultdict(list)
    excluded = []
    counts = Counter()
    for row in rows:
        unit = row["annotation_unit_id"]
        doc, clause, role = row["contract_id"], row["clause_id"], row["role"]
        if unit in seen or unit != f"{clause}::{role}" or role not in {"EMPLOYEE", "EMPLOYER"}:
            raise ValueError("duplicate or invalid role unit")
        seen.add(unit)
        if row["review_status"] != "ADJUDICATED" or (
            row["annotator_id"], row["reviewer_id"], row["adjudicator_id"]
        ) != ("DucAnh_N2", "argon", "Minh_N1"):
            raise ValueError("review identity/status mismatch")
        start, end = int(row["start_char"]), int(row["end_char"])
        if start < 0 or end <= start or len(row["source_sha256"]) != 64:
            raise ValueError("invalid source offset or hash")
        clause_roles[(doc, clause)].append((role, start, end, row["source_sha256"]))
        scope = row["scope_status"]
        outcome = row["candidate_outcome"]
        label = row["candidate_risk_label_1"]
        basis = row["candidate_basis_type_1"]
        citation = row["candidate_citation_id_1"]
        if scope == "CORPUS_V1_SCOPE_EXCEPTION":
            if outcome != "NO_RISK" or not row["notes"].strip() or any((label, basis, citation)):
                raise ValueError("invalid corpus exception")
            excluded.append({"annotation_unit_id": unit, "document_id": doc,
                             "role": role, "start_char": start, "end_char": end})
        elif scope == "IN_CORPUS_ADJUDICATED":
            if outcome != "RISK" or not label or not basis or citation not in citations:
                raise ValueError("invalid in-corpus positive")
            by_doc[doc].append({"clause_id": clause, "role": role,
                                "risk_label": label, "basis_type": basis,
                                "gold_citation_id": citation,
                                "start_char": start, "end_char": end})
        elif scope == "IN_CORPUS_VERIFIED":
            if outcome != "NO_RISK" or any((label, basis, citation)):
                raise ValueError("invalid in-corpus negative")
        else:
            raise ValueError("unknown scope; CONTEXT needs explicit scope status")
        counts[scope] += 1
    for values in clause_roles.values():
        if len(values) != 2 or {v[0] for v in values} != {"EMPLOYEE", "EMPLOYER"} or len({v[1:] for v in values}) != 1:
            raise ValueError("role pair span mismatch")
    if counts != {"IN_CORPUS_ADJUDICATED": 3,
                  "IN_CORPUS_VERIFIED": 1474,
                  "CORPUS_V1_SCOPE_EXCEPTION": 17}:
        raise ValueError("unexpected scope distribution")
    docs = sorted({row["contract_id"] for row in rows})
    if len(docs) != 9:
        raise ValueError("unexpected document count")
    manifest = {
        "status": "GOLD_ADJUDICATED_CLOSED_CORPUS_V1",
        "evaluation_ready": True,
        "evaluation_scope": "16-node closed corpus; exclude listed role units from M2 scoring",
        "context_scope_rows": 0,
        "context_scope_note": "Packet has no CONTEXT status; reviewers assigned all rows to the three explicit scopes. This is an attested scope, not independently checked against T1 text.",
        "source_csv_sha256": hashlib.sha256(packet.read_bytes()).hexdigest(),
        "rows": len(rows), "documents": docs, "scope_counts": dict(counts),
        "positive_items": sum(map(len, by_doc.values())),
        "excluded_corpus_scope_unit_ids": [item["annotation_unit_id"] for item in excluded],
        "excluded_corpus_scope_regions": excluded,
        "source_text_included": False,
    }
    output.mkdir(parents=True)
    for doc in docs:
        result = {"schema_version": "risk_gold_v1", "status": manifest["status"],
                  "evaluation_scope": manifest["evaluation_scope"], "items": by_doc[doc]}
        (output / f"{doc}.risk_gold.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = export(args.packet, args.corpus, args.output)
    print(json.dumps({key: result[key] for key in ("evaluation_ready", "scope_counts", "positive_items")}))
