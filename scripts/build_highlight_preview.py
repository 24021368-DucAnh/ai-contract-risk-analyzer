"""Build a standalone local HTML preview of one annotated contract."""

import argparse
import json
from pathlib import Path

from export_highlight_payload import build_payload


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "preview" / "highlight_template.html"


def build_preview(contract_id: str, output: Path) -> Path:
    payload = build_payload(contract_id)
    template = TEMPLATE.read_text(encoding="utf-8")
    encoded = json.dumps(payload, ensure_ascii=False).replace("<", r"\u003c")
    html = template.replace("__PAYLOAD_JSON__", encoded)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract_id", help="HDLD001 through HDLD005")
    parser.add_argument("--output", type=Path, help="HTML output path")
    args = parser.parse_args()
    output = args.output or ROOT / "preview" / f"{args.contract_id}.html"
    try:
        result = build_preview(args.contract_id, output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(result)


if __name__ == "__main__":
    main()
