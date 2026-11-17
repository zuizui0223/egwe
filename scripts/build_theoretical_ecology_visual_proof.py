#!/usr/bin/env python3
"""Render the canonical TeX PDF and figures into author-reviewable contact sheets.

Rendering and checksum QA only. This does not constitute human visual approval
or establish scientific validity of the content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from PIL import Image, ImageDraw, ImageOps


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ink_fraction(path: Path, cutoff: int = 245) -> float:
    with Image.open(path) as img:
        grayscale = img.convert("L")
        histogram = grayscale.histogram()
        return sum(histogram[:cutoff]) / max(1, sum(histogram))


def contact_sheet(paths: list[Path], output: Path, columns: int = 4,
                  cell_w: int = 460, cell_h: int = 640) -> None:
    if not paths:
        raise ValueError("No pages to present")
    rows = (len(paths) + columns - 1) // columns
    margin = 18
    gap = 20
    label_h = 30
    canvas = Image.new("RGB", (
        2 * margin + columns * cell_w + (columns - 1) * gap,
        2 * margin + rows * (cell_h + label_h) + (rows - 1) * gap,
    ), "white")
    draw = ImageDraw.Draw(canvas)
    for idx, file in enumerate(paths):
        with Image.open(file) as src:
            thumb = ImageOps.contain(src.convert("RGB"), (cell_w - 10, cell_h - 10))
        x = margin + (idx % columns) * (cell_w + gap)
        y = margin + (idx // columns) * (cell_h + label_h + gap)
        canvas.paste(thumb, (x + (cell_w - thumb.width) // 2,
                             y + (cell_h - thumb.height) // 2))
        draw.rectangle((x, y, x + cell_w, y + cell_h), outline="#b0b0b0", width=2)
        draw.text((x + 6, y + cell_h + 6), f"{idx + 1:02d}  {file.name}", fill="#111111")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "JPEG", quality=86, optimize=True)


def render(pdf: Path, out_dir: Path) -> list[Path]:
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    match = re.search(r"(?m)^Pages:\s*(\d+)\s*$", info)
    if not match:
        raise RuntimeError("Cannot read PDF page count")
    n = int(match.group(1))
    if n < 4:
        raise AssertionError(f"Unexpectedly short manuscript PDF: {n} pages")
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "pdftoppm", "-jpeg", "-jpegopt", "quality=78", "-r", "120",
        str(pdf), str(out_dir / "page"),
    ], check=True)
    paths = sorted(out_dir.glob("page-*.jpg"))
    if len(paths) != n:
        raise AssertionError(f"Page raster count {len(paths)} != PDF page count {n}")
    blank = [(i + 1, ink_fraction(p)) for i, p in enumerate(paths)
             if ink_fraction(p) < 0.0002]
    if blank:
        raise AssertionError(f"Possibly blank pages require review: {blank}")
    return paths


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    packet = args.packet.resolve()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    pdf = packet / "theoretical_ecology_manuscript.pdf"
    if not pdf.is_file():
        raise FileNotFoundError(pdf)
    pages = render(pdf, out / "pages")
    sheet = out / "all_pages_contact_sheet.jpg"
    contact_sheet(pages, sheet, columns=4, cell_w=410, cell_h=550)
    figures = [packet / "figures" / f"Fig{i}.png" for i in range(1, 5)]
    if not all(f.is_file() for f in figures):
        raise FileNotFoundError("One or more of Fig1.png--Fig4.png is missing")
    panels = out / "four_figures_contact_sheet.jpg"
    contact_sheet(figures, panels, columns=2, cell_w=800, cell_h=550)
    manifest = {
        "purpose": "visual PDF author review, not submission approval",
        "pdf_sha256": sha256(pdf),
        "page_count": len(pages),
        "page_ink_fraction": [round(ink_fraction(p), 6) for p in pages],
        "figure_metadata": [],
        "page_contact_sheet_sha256": sha256(sheet),
        "figure_contact_sheet_sha256": sha256(panels),
    }
    for f in figures:
        with Image.open(f) as img:
            info = {"name": f.name, "width": img.width,
                    "height": img.height, "sha256": sha256(f)}
        if info["width"] < 600 or info["height"] < 250:
            raise AssertionError(f"Suspiciously low-resolution figure: {info}")
        manifest["figure_metadata"].append(info)
    (out / "visual_proof_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (out / "AUTHOR_REVIEW_REQUIRED.txt").write_text(
        "This is only a page/figure contact-sheet preview of the canonical TeX PDF.\n"
        "It does NOT replace opening the full PDF at 100% zoom.\n"
        "Check all pages, equations, labels, figures, captions, author metadata,\n"
        "references and Statements/Declarations before publisher submission.\n"
        "Do not use Word-to-PDF output as mathematical rendering proof.\n",
        encoding="utf-8",
    )
    print(f"Visual proof prepared: {len(pages)} rendered pages, 4 figures; "
          f"page ink min={min(manifest['page_ink_fraction']):.5f}; "
          f"PDF SHA256={manifest['pdf_sha256']}", flush=True)


if __name__ == "__main__":
    main()
