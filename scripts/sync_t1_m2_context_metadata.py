"""Record T1 segmentation-only CONTEXT references in M2 manifest, metadata only."""

import csv
import json
from pathlib import Path


def sync_context(root: Path) -> dict:
    restricted = root / "data/intake/restricted"
    packet = root / "data/intake/private/m2_review_submissions_2026-11-13/t1_m2_risk_review_packet_v04_adjudicated.csv"
    manifest_path = restricted / "T1_m2_risk_gold_v02/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    with packet.open(encoding="utf-8-sig", newline="") as stream:
        packet_refs = {row["clause_id"] for row in csv.DictReader(stream)}
    context_refs = []
    for number in range(5, 14):
        doc = f"HDLD{number:03d}"
        seg = json.loads((restricted / "T1_segmentation_gold_v01" /
                          f"{doc}.gold_segmentation.json").read_text(encoding="utf-8"))
        labels = json.loads((restricted / "T1_clause_label_gold_v01" /
                             f"{doc}.gold_clause_labels.json").read_text(encoding="utf-8"))
        seg_refs = {item["gold_clause_ref"] for item in seg["segments"]}
        label_refs = {item["clause_id"] for item in labels["items"]}
        if label_refs - seg_refs:
            raise ValueError("clause-label reference absent from segmentation Gold")
        context_refs.extend(sorted(seg_refs - label_refs))
    if len(context_refs) != 95 or len(packet_refs & set(context_refs)) != 0:
        raise ValueError("T1 context/packet coverage differs from approved metadata")
    manifest.update({
        "context_reference_segments": len(context_refs),
        "context_reference_role_units": 2 * len(context_refs),
        "context_segmentation_refs": context_refs,
        "context_scope_unit_ids": [f"{ref}::{role}" for ref in context_refs
                                   for role in ("EMPLOYEE", "EMPLOYER")],
        "context_scope_rows": 0,
        "context_scope_rows_in_packet": 0,
        "context_policy": "Segmentation-only references are absent from the 747-clause M2 packet; do not include their two-role projections in M2 scoring.",
    })
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    return manifest


if __name__ == "__main__":
    result = sync_context(Path(__file__).resolve().parents[1])
    print(json.dumps({key: result[key] for key in (
        "context_reference_segments", "context_reference_role_units",
        "context_scope_rows_in_packet")}))
