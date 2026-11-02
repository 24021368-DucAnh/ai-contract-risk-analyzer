"""Create a page-marked OCR candidate from a scanned legal PDF in restricted storage."""

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_candidate(source_name: str, source_hash: str, pages: list[str]) -> str:
    """Add explicit OCR-only/page provenance without claiming legal verification."""
    blocks = [
        "STATUS: OCR_CANDIDATE_UNPROOFREAD",
        f"SOURCE_FILE: {source_name}",
        f"SOURCE_SHA256: {source_hash}",
        f"PAGE_COUNT: {len(pages)}",
        "OCR_ENGINE: Tesseract 5 / language vie; rendered page images",
        "REVIEW: Every page and character requires visual comparison with source PDF.",
        "",
    ]
    for page_no, text in enumerate(pages, 1):
        blocks.extend((f"===== PDF_PAGE {page_no:03d} | OCR_CANDIDATE =====", text.rstrip(), ""))
    return "\n".join(blocks)


def make_checkpoint(metadata: dict, pages: dict[str, str]) -> dict:
    """Build a JSON-safe checkpoint payload for an interrupted OCR run."""
    return {"metadata": dict(metadata), "pages": dict(pages)}


def checkpoint_pages(checkpoint: object, expected_metadata: dict) -> dict[int, str]:
    """Validate checkpoint provenance and page entries before resuming."""
    if not isinstance(checkpoint, dict) or checkpoint.get("metadata") != expected_metadata:
        raise ValueError("OCR checkpoint metadata mismatch")
    raw_pages = checkpoint.get("pages")
    page_count = expected_metadata.get("page_count")
    if not isinstance(raw_pages, dict) or not isinstance(page_count, int):
        raise ValueError("OCR checkpoint has invalid page entries")
    pages: dict[int, str] = {}
    for raw_page_no, page_text in raw_pages.items():
        try:
            page_no = int(raw_page_no)
        except (TypeError, ValueError) as exc:
            raise ValueError("OCR checkpoint has invalid page entries") from exc
        if (
            str(page_no) != raw_page_no
            or page_no < 1
            or page_no > page_count
            or not isinstance(page_text, str)
            or page_no in pages
        ):
            raise ValueError("OCR checkpoint has invalid page entries")
        pages[page_no] = page_text
    return pages


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent,
            prefix=f"{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
        temp_path.replace(path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def _run(command: list[str]) -> str:
    completed = subprocess.run(
        command, check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    return completed.stdout


def ocr_pdf_candidate(
    pdf_path: Path,
    output_path: Path,
    tessdata_dir: Path,
    *,
    pdftoppm: str = "pdftoppm",
    pdfinfo: str = "pdfinfo",
    tesseract: str = "tesseract",
    scale_to: int = 2200,
    progress: Callable[[int, int], None] | None = None,
) -> dict:
    """OCR all pages sequentially; refuse overwrite and report aggregate-only results."""
    pdf_path, output_path, tessdata_dir = map(Path, (pdf_path, output_path, tessdata_dir))
    if not pdf_path.is_file():
        raise ValueError("source PDF does not exist")
    if not (tessdata_dir / "vie.traineddata").is_file():
        raise ValueError("Vietnamese Tesseract model is missing")
    if output_path.exists():
        raise ValueError("refusing to overwrite existing OCR candidate")
    if isinstance(scale_to, bool) or not isinstance(scale_to, int) or scale_to < 1000:
        raise ValueError("scale_to must be an integer >= 1000")

    info = _run([pdfinfo, str(pdf_path)])
    page_match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
    if page_match is None:
        raise ValueError("could not determine source PDF page count")
    page_count = int(page_match.group(1))
    source_hash = sha256_file(pdf_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    model_hash = sha256_file(tessdata_dir / "vie.traineddata")
    engine = _run([tesseract, "--version"]).splitlines()[0].strip()
    metadata = {
        "source_sha256": source_hash,
        "tessdata_sha256": model_hash,
        "page_count": page_count,
        "scale_to": scale_to,
        "engine": f"{engine}/vie/psm3",
    }
    checkpoint_path = output_path.with_suffix(output_path.suffix + ".partial.json")
    if checkpoint_path.exists():
        try:
            checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("OCR checkpoint is unreadable; preserve it and inspect manually") from exc
        pages = checkpoint_pages(checkpoint, metadata)
    else:
        pages: dict[int, str] = {}

    with tempfile.TemporaryDirectory(prefix="legal_ocr_") as temp_dir:
        temp_root = Path(temp_dir)
        for page_no in range(1, page_count + 1):
            if page_no in pages:
                continue
            prefix = temp_root / f"page_{page_no:03d}"
            _run([
                pdftoppm, "-f", str(page_no), "-l", str(page_no),
                "-scale-to", str(scale_to), "-png", "-singlefile",
                str(pdf_path), str(prefix),
            ])
            image_path = prefix.with_suffix(".png")
            page_text = _run([
                tesseract, str(image_path), "stdout", "-l", "vie",
                "--tessdata-dir", str(tessdata_dir), "--psm", "3",
            ])
            pages[page_no] = page_text
            _atomic_write_json(
                checkpoint_path,
                make_checkpoint(metadata, {str(no): pages[no] for no in sorted(pages)}),
            )
            completed = len(pages)
            if progress is not None and (completed % 10 == 0 or completed == page_count):
                progress(completed, page_count)

    ordered_pages = [pages[page_no] for page_no in range(1, page_count + 1)]
    candidate = format_candidate(pdf_path.name, source_hash, ordered_pages)
    temp_output = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        temp_output.write_text(candidate, encoding="utf-8", newline="\n")
        temp_output.replace(output_path)
    finally:
        temp_output.unlink(missing_ok=True)
    checkpoint_path.unlink(missing_ok=True)
    return {
        "status": "OCR_CANDIDATE_UNPROOFREAD",
        "page_count": page_count,
        "nonempty_pages": sum(bool(page.strip()) for page in ordered_pages),
        "characters": sum(len(page) for page in ordered_pages),
        "source_sha256": source_hash,
        "output": str(output_path),
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    restricted = root / "data/intake/restricted/legal_sources"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=restricted / "BLLD_18_VBHN_2026.pdf")
    parser.add_argument(
        "--output", type=Path,
        default=restricted / "BLLD_18_VBHN_2026_ocr_candidate.txt",
    )
    parser.add_argument("--tessdata", type=Path, default=restricted / "tessdata")
    parser.add_argument("--pdftoppm", default="pdftoppm")
    parser.add_argument("--pdfinfo", default="pdfinfo")
    parser.add_argument("--tesseract", default=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    parser.add_argument("--scale-to", type=int, default=2200)
    args = parser.parse_args()
    result = ocr_pdf_candidate(
        args.pdf,
        args.output,
        args.tessdata,
        pdftoppm=args.pdftoppm,
        pdfinfo=args.pdfinfo,
        tesseract=args.tesseract,
        scale_to=args.scale_to,
        progress=lambda done, total: print(f"OCR pages: {done}/{total}", flush=True),
    )
    print(
        "OCR complete: {page_count} pages; {nonempty_pages} non-empty; "
        "{characters} characters; status={status}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
