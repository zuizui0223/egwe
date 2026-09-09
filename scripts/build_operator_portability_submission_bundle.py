from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "manuscript/operator_portability_short_communication.md",
    "manuscript/operator_portability_references.md",
    "manuscript/operator_portability_highlights.md",
    "manuscript/operator_portability_cover_letter.md",
    "manuscript/operator_portability_display_plan.md",
    "manuscript/operator_portability_submission_metadata.md",
    "manuscript/operator_portability_submission_checklist.md",
    "docs/OPERATOR_PORTABILITY_OVERLAP_AUDIT_2026-09-09.md",
    "docs/OPERATOR_PORTABILITY_PRECISION_AUDIT_2026-09-09.md",
    "artifacts/operator_portability_precision/derived_summary.json",
    "artifacts/fresh_connectivity_replication/phase_u_locked_summary.json",
    "artifacts/process_resolved_movement/phase_r_locked_summary.json",
    "artifacts/process_resolved_pollen/phase_s_locked_summary.json",
    "scripts/operator_portability_precision.py",
    "figures/operator_portability_fig1.svg",
    "figures/operator_portability_fig2.svg",
]

FORBIDDEN_PATH_FRAGMENTS = (
    "nee_flagship",
    "last_refuge_warning",
    "operator_balance_route",
    "warning_validity.md",
    "state_validity_and_empirical_measurement_gates.md",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_bundle(repo_root: Path, output: Path) -> Path:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    manifest = []
    for relative in FILES:
        if any(fragment in relative for fragment in FORBIDDEN_PATH_FRAGMENTS):
            raise RuntimeError(f"forbidden overlapping path in portability bundle: {relative}")
        src = repo_root / relative
        if not src.is_file():
            raise FileNotFoundError(src)
        dst = output / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        manifest.append({"path": relative, "sha256": sha256(dst), "bytes": dst.stat().st_size})

    (output / "bundle_manifest.json").write_text(
        json.dumps({
            "bundle": "operator_portability_short_communication",
            "submission_state": "package_ready_pending_author_metadata_and_final_policy_check",
            "files": manifest,
        }, indent=2) + "\n",
        encoding="utf-8",
    )

    # Fail closed if anything outside the declared list was copied.
    actual = sorted(str(p.relative_to(output)).replace("\\", "/") for p in output.rglob("*") if p.is_file())
    expected = sorted(FILES + ["bundle_manifest.json"])
    if actual != expected:
        raise RuntimeError(f"bundle surface drifted: actual={actual}, expected={expected}")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = build_bundle(Path(args.repo_root), Path(args.output))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
