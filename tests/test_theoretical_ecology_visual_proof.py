"""Regression tests for visual proof preflight: no PDF/network required."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw


MODULE = Path(__file__).resolve().parents[1] / "scripts" / "build_theoretical_ecology_visual_proof.py"
spec = importlib.util.spec_from_file_location("te_visual_proof", MODULE)
assert spec and spec.loader
proof = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proof)


class VisualProofTests(unittest.TestCase):
    def test_blank_and_nonblank_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            white = Path(tmp) / "white.jpg"
            inked = Path(tmp) / "inked.jpg"
            Image.new("RGB", (300, 400), "white").save(white)
            image = Image.new("RGB", (300, 400), "white")
            ImageDraw.Draw(image).rectangle((50, 60, 240, 300), fill="black")
            image.save(inked)
            self.assertLess(proof.ink_fraction(white), 0.0002)
            self.assertGreater(proof.ink_fraction(inked), 0.01)

    def test_contact_sheet_contains_multiple_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = []
            for n in range(1, 6):
                image = Image.new("RGB", (300, 400), "white")
                ImageDraw.Draw(image).rectangle((20 * n, 40, 240, 140), fill="black")
                path = root / f"page-{n:02d}.jpg"
                image.save(path)
                source.append(path)
            target = root / "overview.jpg"
            proof.contact_sheet(source, target, columns=4)
            with Image.open(target) as output:
                self.assertGreater(output.width, 1000)
                self.assertGreater(output.height, 1000)
            self.assertGreater(target.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
