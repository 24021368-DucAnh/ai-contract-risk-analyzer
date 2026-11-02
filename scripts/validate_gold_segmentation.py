"""Validate a human-adjudicated segmentation gold JSON against canonical text."""

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "gold_segmentation_v1"
OFFSET_UNIT = "unicode_code_point"
TOP_LEVEL_KEYS = {
    "schema_version", "doc_id", "source_sha256", "offset_unit", "annotation",
    "segments",
}
ANNOTATION_KEYS = {"annotator_id", "reviewer_id", "adjudicator_id", "adjudicated_at", "decision"}
SEGMENT_KEYS = {"start_char", "end_char", "gold_clause_ref"}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def validate_gold_segmentation(payload: Any, canonical_text: str) -> dict[str, Any]:
    """Fail closed unless schema, provenance and complete non-whitespace partition hold."""
    errors: list[str] = []
    if not isinstance(payload, dict) or set(payload) != TOP_LEVEL_KEYS:
        raise ValueError(f"gold object keys must be exactly {sorted(TOP_LEVEL_KEYS)}")
    if payload["schema_version"] != SCHEMA_VERSION:
        errors.append("unsupported schema_version")
    if not isinstance(payload["doc_id"], str) or not payload["doc_id"].strip():
        errors.append("doc_id must be non-empty")
    if payload["offset_unit"] != OFFSET_UNIT:
        errors.append("offset_unit must be unicode_code_point")
    expected_hash = hashlib.sha256(canonical_text.encode("utf-8")).hexdigest()
    if payload["source_sha256"] != expected_hash:
        errors.append("source_sha256 does not match canonical text")

    annotation = payload["annotation"]
    if not isinstance(annotation, dict) or set(annotation) != ANNOTATION_KEYS:
        errors.append(f"annotation keys must be exactly {sorted(ANNOTATION_KEYS)}")
    else:
        for key in ("annotator_id", "reviewer_id", "adjudicator_id", "adjudicated_at"):
            if not isinstance(annotation[key], str) or not annotation[key].strip():
                errors.append(f"annotation.{key} must be non-empty")
        try:
            adjudicated_at = datetime.fromisoformat(annotation["adjudicated_at"])
            if adjudicated_at.utcoffset() is None:
                errors.append("annotation.adjudicated_at must include a timezone")
        except (TypeError, ValueError):
            errors.append("annotation.adjudicated_at must be ISO-8601")
        if annotation["annotator_id"] == annotation["reviewer_id"]:
            errors.append("annotator and reviewer must be distinct")
        if annotation["decision"] != "ADJUDICATED_ACCEPTED":
            errors.append("annotation.decision must be ADJUDICATED_ACCEPTED")

    segments = payload["segments"]
    if not isinstance(segments, list) or not segments:
        errors.append("segments must be a non-empty array")
        segments = []
    seen_refs: set[str] = set()
    previous_end = 0
    covered_chars = 0
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict) or set(segment) != SEGMENT_KEYS:
            errors.append(f"segments[{index}] keys must be exactly {sorted(SEGMENT_KEYS)}")
            continue
        start, end, clause_ref = segment["start_char"], segment["end_char"], segment["gold_clause_ref"]
        if isinstance(start, bool) or not isinstance(start, int) or isinstance(end, bool) or not isinstance(end, int):
            errors.append(f"segments[{index}] offsets must be integers")
            continue
        if not isinstance(clause_ref, str) or not clause_ref.strip():
            errors.append(f"segments[{index}].gold_clause_ref must be non-empty")
        elif clause_ref in seen_refs:
            errors.append("gold_clause_ref values must be unique")
        else:
            seen_refs.add(clause_ref)
        if not (0 <= start < end <= len(canonical_text)):
            errors.append(f"segments[{index}] span is outside canonical text")
            continue
        if start < previous_end:
            errors.append(f"segments[{index}] overlaps or is out of order")
        elif any(not char.isspace() for char in canonical_text[previous_end:start]):
            errors.append(f"uncovered non-whitespace text before segments[{index}]")
        covered_chars += sum(not char.isspace() for char in canonical_text[start:end])
        previous_end = max(previous_end, end)
    if segments and any(not char.isspace() for char in canonical_text[previous_end:]):
        errors.append("uncovered non-whitespace text after final segment")
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "status": "PASS",
        "doc_id": payload["doc_id"],
        "segment_count": len(segments),
        "covered_non_whitespace_codepoints": covered_chars,
        "source_sha256": expected_hash,
    }


def load_and_validate(gold_path: Path, source_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(gold_path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        source_text = source_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("could not read valid UTF-8 gold/source file") from error
    return validate_gold_segmentation(payload, source_text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gold", type=Path)
    parser.add_argument("source", type=Path, help="exact canonical UTF-8 text used for annotation")
    args = parser.parse_args()
    try:
        result = load_and_validate(args.gold, args.source)
    except ValueError as error:
        print(f"FAIL: {error}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
