"""Create a source-checked synthetic calibration reference, separate from human T1 Gold."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/processed/raw_text/HDLD014.txt"
CANDIDATE = ROOT / "data/intake/private/HDLD014_synthetic_candidate_v01.json"
SIGNOFF = ROOT / "data/intake/t1_equivalent_gate_signoff_2026-11-06.json"
OUTPUT = ROOT / "data/intake/restricted/HDLD014_synthetic_control_gold_v01"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    text = SOURCE.read_text(encoding="utf-8")
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    signoff = json.loads(SIGNOFF.read_text(encoding="utf-8"))
    if candidate["source_sha256"] != digest(SOURCE):
        raise ValueError("synthetic source hash mismatch")
    if signoff["document_modes"].get("HDLD014") != "SYNTHETIC_CALIBRATION_CONTROL":
        raise ValueError("synthetic control not in equivalent-gate decision")
    spans = [*candidate["context_candidates"], *candidate["segmentation_candidates"]]
    spans.sort(key=lambda row: row["start_char"])
    covered = set()
    for row in spans:
        start, end = row["start_char"], row["end_char"]
        if not 0 <= start < end <= len(text) or covered.intersection(range(start, end)):
            raise ValueError("invalid or overlapping synthetic spans")
        covered.update(range(start, end))
    if any(not char.isspace() and index not in covered for index, char in enumerate(text)):
        raise ValueError("synthetic segmentation does not cover nonwhitespace text")
    segmentation = {"schema_version": "gold_segmentation_v1",
                    "status": "SYNTHETIC_CONTROL_REFERENCE",
                    "source_sha256": digest(SOURCE),
                    "segments": [{"start_char": row["start_char"], "end_char": row["end_char"],
                                  "gold_clause_ref": row.get("clause_id", "HDLD014_CONTEXT"),
                                  "offset_unit": "unicode_code_point"} for row in spans]}
    labels = {"schema_version": "clause_labels_v1", "status": "SYNTHETIC_CONTROL_REFERENCE",
              "taxonomy_version": "clause_taxonomy_v03",
              "items": [{"clause_id": row["clause_id"], "labels": [row["candidate_label"]]}
                        for row in candidate["segmentation_candidates"]]}
    privacy = {"schema_version": "privacy_gold_v1", "status": "SYNTHETIC_CONTROL_REFERENCE",
               "offset_unit": "unicode_code_point", "document_coverage": [0, len(text)],
               "pii_spans": [], "preserve_spans": candidate["privacy_candidates"]["preserve_spans"]}
    OUTPUT.mkdir(parents=True)
    payloads = {"HDLD014.gold_segmentation.json": segmentation,
                "HDLD014.gold_clause_labels.json": labels,
                "HDLD014.gold_privacy.json": privacy}
    for name, payload in payloads.items():
        (OUTPUT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
    manifest = {"status": "SYNTHETIC_CONTROL_REFERENCE", "contract_id": "HDLD014",
                "source_sha256": digest(SOURCE), "candidate_sha256": digest(CANDIDATE),
                "equivalent_signoff_sha256": digest(SIGNOFF),
                "artifacts_sha256": {name: digest(OUTPUT / name) for name in payloads},
                "segmentation_spans": len(segmentation["segments"]),
                "clause_labels": len(labels["items"]), "preserve_fields": len(privacy["preserve_spans"]),
                "pii_spans": 0}
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "spans": manifest["segmentation_spans"],
                      "labels": manifest["clause_labels"], "preserve_fields": manifest["preserve_fields"]}))


if __name__ == "__main__":
    main()
