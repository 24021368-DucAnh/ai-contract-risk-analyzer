"""Add auditable parent-context spans for split or normalized v04 clauses.

EXACT spans remain clause-text matches. CONTEXT spans identify the relevant
source phrase for a split or normalized annotation; consumers must not treat
them as exact clause quotations or use them for exact-span evaluation.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
SOURCE_CSV = PROCESSED / "clauses_v04.csv"
OUTPUT_CSV = PROCESSED / "clauses_v05.csv"
RAW_TEXT_DIR = PROCESSED / "raw_text"

# start anchor and optional inclusive end anchor in the original extracted text.
# None means the remainder of the source line. These anchors identify the
# parent sentence or bullet before selecting the relevant highlight phrase.
CONTEXT_ANCHORS = {
    "HDLD001_C014": ("- Từ ngày Thứ 2 đến ngày Thứ 7", "+ Buổi chiều: 13h00 - 17h00."),
    "HDLD003_C018": ("g) Đóng các loại bảo hiểm, các khoản thuế", None),
    "HDLD003_C018A": ("g) Đóng các loại bảo hiểm, các khoản thuế", None),
    "HDLD004_C023": ("- Về nghỉ ngơi; hỗ trợ học nghề", None),
    "HDLD004_C024": ("- Về nghỉ ngơi; hỗ trợ học nghề", None),
    "HDLD004_C025": ("- Về bố trí chỗ ăn, ở; trang bị", None),
    "HDLD004_C026": ("- Về bố trí chỗ ăn, ở; trang bị", None),
    "HDLD004_C027": ("- Về bố trí chỗ ăn, ở; trang bị", None),
    "HDLD004_C043": ("Hợp đồng này được lập thành 02 bản", None),
}

# For shared source bullets, highlight the unique phrase behind each semantic
# annotation. The annotation may repeat surrounding grammar that is absent here.
HIGHLIGHT_PHRASES = {
    "HDLD003_C018": "các loại bảo hiểm",
    "HDLD003_C018A": "các khoản thuế",
    "HDLD004_C023": "nghỉ ngơi",
    "HDLD004_C024": "hỗ trợ học nghề, học văn hóa",
    "HDLD004_C025": "bố trí chỗ ăn, ở",
    "HDLD004_C026": "trang bị bảo hộ lao động",
    "HDLD004_C027": "bồi thường thiệt hại",
    "HDLD004_C043": "có hiệu lực từ ngày ......... tháng ........... năm ..........",
}


def _context_span(raw_text: str, start_anchor: str, end_anchor: str | None) -> tuple[int, int]:
    start = raw_text.find(start_anchor)
    if start < 0 or raw_text.find(start_anchor, start + 1) >= 0:
        raise ValueError(f"context anchor missing or ambiguous: {start_anchor}")
    if end_anchor is None:
        end = raw_text.find("\n", start)
        if end < 0:
            end = len(raw_text)
    else:
        end_start = raw_text.find(end_anchor, start)
        if end_start < 0:
            raise ValueError(f"context end anchor missing: {end_anchor}")
        end = end_start + len(end_anchor)
    if end <= start:
        raise ValueError(f"invalid context span: {start_anchor}")
    return start, end


def fill_context_offsets(
    rows: list[dict[str, str]], raw_text_by_contract: dict[str, str]
) -> list[dict[str, str]]:
    result = []
    seen_context = set()
    for row in rows:
        updated = dict(row)
        if updated["start_offset"] and updated["end_offset"]:
            updated["offset_quality"] = "EXACT"
        else:
            clause_id = updated["clause_id"]
            if clause_id not in CONTEXT_ANCHORS:
                raise ValueError(f"missing reviewed context anchor: {clause_id}")
            raw_text = raw_text_by_contract[updated["contract_id"]]
            start, end = _context_span(raw_text, *CONTEXT_ANCHORS[clause_id])
            phrase = HIGHLIGHT_PHRASES.get(clause_id)
            if phrase is not None:
                parent = raw_text[start:end]
                relative = parent.find(phrase)
                if relative < 0 or parent.find(phrase, relative + 1) >= 0:
                    raise ValueError(f"highlight phrase missing or ambiguous: {clause_id}")
                start += relative
                end = start + len(phrase)
            updated["start_offset"] = str(start)
            updated["end_offset"] = str(end)
            updated["offset_quality"] = "CONTEXT"
            updated["notes"] = (
                updated.get("notes", "").split("; OFFSET_UNVERIFIED:")[0]
                + "; OFFSET_CONTEXT: highlights relevant original source text, "
                "not the full normalized clause text"
            ).lstrip("; ")
            seen_context.add(clause_id)
        result.append(updated)
    if seen_context != set(CONTEXT_ANCHORS):
        raise ValueError("some reviewed context anchors were not used")
    return result


def main() -> None:
    with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or []) + ["offset_quality"]
    raw = {
        contract_id: (RAW_TEXT_DIR / f"{contract_id}.txt").read_text(encoding="utf-8")
        for contract_id in {row["contract_id"] for row in rows}
    }
    output = fill_context_offsets(rows, raw)
    if OUTPUT_CSV.exists():
        raise FileExistsError(f"snapshot already exists: {OUTPUT_CSV}")
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output)
    print(f"Wrote {OUTPUT_CSV}: 174 EXACT, 9 CONTEXT spans")


if __name__ == "__main__":
    main()
