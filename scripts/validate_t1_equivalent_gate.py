"""Validate the owner-approved composite T1 gate without changing BRD intake."""

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_intake_gate import evaluate_units, load_csv
SIGNOFF = ROOT / "data/intake/t1_equivalent_gate_signoff_2026-11-06.json"
ADR = ROOT / "docs/ADR_T1_EQUIVALENT_GATE_V1.md"
MODES = {
    **{f"HDLD{i:03}": "PUBLIC_TEMPLATE_VERIFIED" for i in range(5, 10)},
    **{f"HDLD{i:03}": "REAL_EXECUTED_RESTRICTED" for i in range(10, 14)},
    "HDLD014": "SYNTHETIC_CALIBRATION_CONTROL",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate():
    receipt = json.loads(SIGNOFF.read_text(encoding="utf-8"))
    if receipt.get("gate_id") != "T1_EQUIVALENT_GATE_V1":
        raise ValueError("wrong equivalent gate receipt")
    if receipt.get("document_modes") != MODES or receipt.get("adr_sha256") != digest(ADR):
        raise ValueError("ADR or document-mode receipt changed")
    roles = receipt.get("roles", {})
    if {roles.get("owner"), roles.get("reviewer"), roles.get("adjudicator")} != {
        "DucAnh_N2", "argon", "Minh_N1"
    }:
        raise ValueError("three independent role IDs required")
    with (ROOT / "data/contracts_metadata.csv").open(encoding="utf-8-sig", newline="") as stream:
        metadata = {row["contract_id"]: row for row in csv.DictReader(stream)}
    if set(MODES) - set(metadata):
        raise ValueError("equivalent metadata is incomplete")
    if set(receipt.get("source_receipts", {})) != set(MODES):
        raise ValueError("ten source hashes required")
    checked = []
    for doc, mode in MODES.items():
        row = metadata[doc]
        if row.get("equivalent_gate_mode") != mode or row.get("equivalent_gate_status") != (
            "ACCEPTED_UNDER_EQUIVALENT_GATE_V1"
        ):
            raise ValueError(f"equivalent metadata decision mismatch for {doc}")
        source = receipt["source_receipts"][doc]
        path = (ROOT / source["path"]).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            raise ValueError(f"source file missing or outside repo for {doc}")
        if digest(path) != source["sha256"]:
            raise ValueError(f"source hash mismatch for {doc}")
        if mode == "REAL_EXECUTED_RESTRICTED":
            if row.get("source_pdf_sha256") != source["sha256"] or not row.get("source_document_ref"):
                raise ValueError(f"restricted local PDF receipt missing for {doc}")
        if doc == "HDLD014":
            if row.get("project_status") != "SYNTHETIC_CHALLENGE_NOT_T1":
                raise ValueError("synthetic source promoted into original T1")
            control = ROOT / "data/intake/restricted/HDLD014_synthetic_control_gold_v01/manifest.json"
            manifest = json.loads(control.read_text(encoding="utf-8"))
            if manifest["source_sha256"] != source["sha256"] or manifest["equivalent_signoff_sha256"] != digest(SIGNOFF):
                raise ValueError("synthetic control Gold receipt mismatch")
        else:
            for kind in ("segmentation", "clause_label", "privacy"):
                folder = ROOT / "data/intake/restricted" / f"T1_{kind}_gold_v01"
                files = list(folder.glob(f"{doc}.gold_*.json"))
                if len(files) != 1 or json.loads(files[0].read_text(encoding="utf-8"))["status"] != "GOLD_ADJUDICATED":
                    raise ValueError(f"missing adjudicated {kind} Gold for {doc}")
        checked.append(doc)
    manifest_rows = load_csv(ROOT / "data/intake/manifest.csv")
    unit_rows = load_csv(ROOT / "data/intake/contract_unit_review_queue.csv")
    errors, original = evaluate_units(manifest_rows, unit_rows, ROOT)
    if errors:
        raise ValueError("original intake gate has structural errors")
    return {"status": "ACCEPTED_UNDER_EQUIVALENT_GATE_V1",
            "gate_id": "T1_EQUIVALENT_GATE_V1", "accepted_equivalent": len(checked),
            "required_equivalent": 10, "mode_counts": dict(Counter(MODES.values())),
            "original_brd_accepted": original["accepted_t1"],
            "original_brd_required": 10,
            "slice_unique_8": [doc for doc in checked if doc not in ("HDLD006", "HDLD014")],
            "slice_t1_real_9": [doc for doc in checked if doc != "HDLD014"],
            "slice_composite_10": checked,
            "signoff_receipt_sha256": digest(SIGNOFF), "adr_sha256": digest(ADR),
            "limitation": "Owner-attested academic composite; source execution, rights and external provenance are not independently verified by this script."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = validate()
    if args.report:
        if args.report.exists():
            raise FileExistsError(args.report)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "accepted": result["accepted_equivalent"],
                      "original_brd_accepted": result["original_brd_accepted"]}))


if __name__ == "__main__":
    main()
