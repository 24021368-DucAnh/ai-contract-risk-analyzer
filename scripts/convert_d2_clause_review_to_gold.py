"""Convert fully adjudicated, source-pinned D2 clause labels into new Gold files."""

import argparse
import csv
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from scripts.build_d2_clause_label_review_queue import FIELDS
from scripts.validate_d1_label_review_packet import LABELS

ALLOWED_APPROVAL_MODES = (
    "DUAL_HUMAN_REVIEW_V1",
    "OWNER_SINGLE_APPROVER_AI_ASSISTED_V1",
)

FORBIDDEN_APPROVER_TOKENS = {
    "pending",
    "tbd",
    "todo",
    "unknown",
    "none",
    "null",
    "n/a",
    "na",
    "ai",
    "chatgpt",
    "gpt",
    "claude",
    "gemini",
    "codex",
    "copilot",
    "llm",
    "bot",
    "assistant",
    "auto",
    "system",
    "independent_source_auditor",
    "reviewer_n1",
    "reviewer_n2",
    "owner_approver",
}


def _is_forbidden_approver(name: str) -> bool:
    norm = name.strip().lower()
    if not norm:
        return True
    if norm in FORBIDDEN_APPROVER_TOKENS:
        return True
    # Split punctuation without breaking Vietnamese names such as "Mai".
    tokens = re.findall(r"[^\W_]+", norm)
    model_alias = re.compile(r"(?:chatgpt|gpt|gemini|claude|codex|copilot|llm|bot|assistant)\d\w*")
    return any(
        tok in FORBIDDEN_APPROVER_TOKENS or model_alias.fullmatch(tok)
        for tok in tokens
    )


def _date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid review date") from exc
    if parsed.isoformat() != value or parsed > date.today():
        raise ValueError("invalid or future review date")
    return parsed


def convert_reviewed_queue(
    packet: Path,
    documents: dict[str, tuple[Path, Path]],
    *,
    approval_mode: str = "DUAL_HUMAN_REVIEW_V1",
) -> dict[str, dict]:
    """Reject partial approval and any changed source text, span, or taxonomy."""
    if approval_mode not in ALLOWED_APPROVAL_MODES:
        raise ValueError(f"unsupported approval_mode: {approval_mode}")

    with packet.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != set(FIELDS) or len(reader.fieldnames or []) != len(FIELDS):
            raise ValueError("review packet columns differ from D2 v1 schema")
        rows = list(reader)
    if not rows or {row["document_id"] for row in rows} != set(documents):
        raise ValueError("review packet document coverage mismatch")
    checked = {}
    for doc_id, (source_path, gold_path) in documents.items():
        source = source_path.read_bytes()
        source_sha = hashlib.sha256(source).hexdigest()
        text = source.decode("utf-8")
        gold = json.loads(gold_path.read_text(encoding="utf-8"))
        if gold.get("source_sha256") != source_sha:
            raise ValueError(f"D2 segmentation/source SHA-256 mismatch: {doc_id}")
        if gold.get("status", "ADJUDICATED_D2_GOLD_V02") != "ADJUDICATED_D2_GOLD_V02":
            raise ValueError(f"D2 segmentation is not adjudicated: {doc_id}")
        segments = {}
        for item in gold["segments"]:
            ref, start, end = item["gold_clause_ref"], item["start_char"], item["end_char"]
            if (ref in segments or item.get("offset_unit") != "unicode_code_point"
                    or not isinstance(start, int) or not isinstance(end, int)
                    or start < 0 or end <= start or end > len(text)):
                raise ValueError(f"invalid D2 segmentation span: {doc_id}/{ref}")
            segments[ref] = (start, end, hashlib.sha256(text[start:end].encode("utf-8")).hexdigest())
        checked[doc_id] = (source_sha, segments)

    gold_files = {}
    seen_owner_approvers: set[str] = set()
    for doc_id, (source_sha, segments) in checked.items():
        matched: dict[str, list[str]] = {}
        for row in (r for r in rows if r["document_id"] == doc_id):
            ref = row["d2_gold_clause_ref"]
            if ref in matched or ref not in segments:
                raise ValueError(f"duplicate or unknown D2 clause ref: {doc_id}/{ref}")
            start, end, span_sha = segments[ref]
            if (row["d2_source_sha256"] != source_sha or row["span_sha256"] != span_sha
                    or row["start_char"] != str(start) or row["end_char"] != str(end)):
                raise ValueError(f"D2 source/span hash or offsets changed: {doc_id}/{ref}")
            if row["taxonomy_version"] != "clause_taxonomy_v03":
                raise ValueError(f"taxonomy version changed: {doc_id}/{ref}")
            first, second = row["reviewer_n1"].strip(), row["reviewer_n2"].strip()
            if approval_mode == "DUAL_HUMAN_REVIEW_V1":
                if (row["decision"] != "APPROVED" or not first or not second or first == second
                        or _is_forbidden_approver(first) or _is_forbidden_approver(second)
                        or any(mark in first + second for mark in "<>")):
                    raise ValueError(f"two-person adjudication pending: {doc_id}/{ref}")
            else:
                if (row["decision"] != "APPROVED" or not first or second
                        or _is_forbidden_approver(first)
                        or any(mark in first for mark in "<>")):
                    raise ValueError(f"single-owner adjudication invalid or pending: {doc_id}/{ref}")
                seen_owner_approvers.add(first)
                if len(seen_owner_approvers) > 1:
                    raise ValueError(f"inconsistent owner_approver across D2 rows: {sorted(seen_owner_approvers)}")
            _date(row["reviewed_on"])
            labels = [label.strip() for label in row["adjudicated_labels"].split(";")]
            if (not 1 <= len(labels) <= 3 or any(label not in LABELS for label in labels)
                    or len(labels) != len(set(labels)) or ("OTHER" in labels and len(labels) != 1)):
                raise ValueError(f"invalid or missing final label: {doc_id}/{ref}")
            matched[ref] = labels
        if set(matched) != set(segments):
            raise ValueError(f"D2 clause-label review coverage mismatch: {doc_id}")
        source_desc = (
            "D2 clause-label two-person review packet"
            if approval_mode == "DUAL_HUMAN_REVIEW_V1"
            else "D2 clause-label single-owner AI-assisted review packet (OWNER_SINGLE_APPROVER_AI_ASSISTED_V1)"
        )
        gold_files[doc_id] = {
            "schema_version": "clause_labels_v1",
            "status": "GOLD_ADJUDICATED",
            "approval_governance_mode": approval_mode,
            "source": source_desc,
            "taxonomy_version": "clause_taxonomy_v03",
            "items": [{"clause_id": ref, "labels": matched[ref]} for ref in sorted(matched)],
        }
    return gold_files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restricted-root", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument(
        "--approval-mode",
        choices=ALLOWED_APPROVAL_MODES,
        default="DUAL_HUMAN_REVIEW_V1",
    )
    args = parser.parse_args()
    root = args.restricted_root.resolve()
    docs = {f"HDLD{number:03}": (
        root / f"D2_candidate_v02/HDLD{number:03}.d2_candidate.txt",
        root / f"D2_segmentation_gold_v02/HDLD{number:03}.gold_segmentation.json",
    ) for number in range(1, 5)}
    gold = convert_reviewed_queue(args.packet, docs, approval_mode=args.approval_mode)
    if sum(len(payload["items"]) for payload in gold.values()) != 250:
        raise ValueError("D2 Gold must cover all 250 adjudicated segmentation spans")
    if args.check_only:
        print(json.dumps({"status": "READY_TO_WRITE", "items": 250, "documents": 4, "approval_mode": args.approval_mode}))
        return
    output = args.output.resolve()
    if not output.is_relative_to(root) or output.exists():
        raise ValueError("output must be a new directory under the restricted root")
    output.mkdir(parents=True, exist_ok=False)
    for doc_id, payload in gold.items():
        (output / f"{doc_id}.gold_clause_labels.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
    (output / "manifest.json").write_text(json.dumps({
        "schema_version": "d2_clause_label_gold_manifest_v2",
        "dataset_version": output.name,
        "status": "GOLD_ADJUDICATED",
        "approval_governance_mode": args.approval_mode,
        "taxonomy_version": "clause_taxonomy_v03",
        "documents": sorted(gold),
        "items": 250,
        "packet_sha256": hashlib.sha256(args.packet.read_bytes()).hexdigest(),
        "d2_sources_sha256": {doc_id: hashlib.sha256(source.read_bytes()).hexdigest()
                               for doc_id, (source, _) in docs.items()},
        "d2_segmentation_sha256": {doc_id: hashlib.sha256(geometry.read_bytes()).hexdigest()
                                    for doc_id, (_, geometry) in docs.items()},
        "gold_files_sha256": {f"{doc_id}.gold_clause_labels.json": hashlib.sha256(
            (output / f"{doc_id}.gold_clause_labels.json").read_bytes()).hexdigest() for doc_id in docs},
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED_FAIL_CLOSED", "reason": str(exc)}))
        raise SystemExit(1) from exc
