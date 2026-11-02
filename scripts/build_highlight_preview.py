"""Build a standalone local HTML preview of one annotated contract."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.export_highlight_payload import build_payload

TEMPLATE = ROOT / "preview" / "highlight_template.html"


def build_preview(
    contract_id: str, output: Path, *, local_fixture: bool = False, root: Path = ROOT
) -> Path:
    # HTML embeds the complete contract text; only write to Git-ignored private storage.
    private_dir = (root / "data/intake/private").resolve()
    if not output.resolve().is_relative_to(private_dir):
        raise ValueError("HTML previews must stay under data/intake/private (not shareable output)")
    payload = build_payload(contract_id, processed=root / "data/processed",
                            root=root, local_fixture=local_fixture)
    template = TEMPLATE.read_text(encoding="utf-8")
    encoded = json.dumps(payload, ensure_ascii=False).replace("<", r"\u003c")
    html = template.replace("__PAYLOAD_JSON__", encoded)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract_id", help="approved intake ID, or frozen dev ID with --local-fixture")
    parser.add_argument("--local-fixture", action="store_true",
                        help="use a frozen local development fixture; NOT approved for redistribution")
    parser.add_argument("--output", type=Path, help="HTML output path under data/intake/private")
    args = parser.parse_args()
    output = args.output or ROOT / "data/intake/private/previews" / f"{args.contract_id}.html"
    try:
        result = build_preview(args.contract_id, output, local_fixture=args.local_fixture)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(result)


if __name__ == "__main__":
    main()
