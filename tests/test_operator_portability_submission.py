from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_checker():
    path = ROOT / "scripts/check_operator_portability_submission.py"
    spec = importlib.util.spec_from_file_location("operator_submission_checker", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_submission_surface_passes_after_figures_are_built() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/build_operator_portability_figures.py")], check=True, cwd=ROOT)
    checker = load_checker()
    assert checker.main() == 0


def test_portability_manuscript_excludes_flagship_claim_tokens() -> None:
    text = (ROOT / "manuscript/operator_portability_short_communication.md").read_text(encoding="utf-8")
    for token in ("0.2543", "+5.33", "+5.20", "35/35", "48/48", "+6.883", "1,920,000", "0.92734", "+0.02135"):
        assert token not in text


def test_bundle_is_fail_closed(tmp_path: Path) -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/build_operator_portability_figures.py")], check=True, cwd=ROOT)
    out = tmp_path / "operator_portability_submission"
    subprocess.run([
        sys.executable,
        str(ROOT / "scripts/build_operator_portability_submission_bundle.py"),
        "--repo-root", str(ROOT),
        "--output", str(out),
    ], check=True, cwd=ROOT)
    manifest = json.loads((out / "bundle_manifest.json").read_text(encoding="utf-8"))
    assert manifest["bundle"] == "operator_portability_short_communication"
    paths = {row["path"] for row in manifest["files"]}
    assert "manuscript/operator_portability_short_communication.md" in paths
    assert "figures/operator_portability_fig1.svg" in paths
    assert "figures/operator_portability_fig2.svg" in paths
    assert not any("nee_flagship" in path for path in paths)
    assert not any("last_refuge" in path for path in paths)


def test_metadata_keeps_human_author_gate() -> None:
    metadata = (ROOT / "manuscript/operator_portability_submission_metadata.md").read_text(encoding="utf-8")
    assert "Author list/order: [pending]" in metadata
    assert "not authorised for submission yet" in metadata
