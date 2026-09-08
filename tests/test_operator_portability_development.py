from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_precision_module():
    path = ROOT / "scripts/operator_portability_precision.py"
    spec = importlib.util.spec_from_file_location("operator_portability_precision", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_phase_r_s_share_reference_blocks_but_not_process_arm() -> None:
    phase_r = json.loads((ROOT / "artifacts/process_resolved_movement/phase_r_locked_summary.json").read_text())
    phase_s = json.loads((ROOT / "artifacts/process_resolved_pollen/phase_s_locked_summary.json").read_text())
    by_r = {row["condition"]: row for row in phase_r["conditions"]}
    by_s = {row["condition"]: row for row in phase_s["conditions"]}
    assert by_r["no_connectivity"]["blocks"] == by_s["no_connectivity"]["blocks"]
    assert by_r["allele_only_m010"]["blocks"] == by_s["allele_only_m010"]["blocks"]
    assert "individual_dispersal_d010" in by_r
    assert "pollen_only_g020" in by_s


def test_precision_summary_recomputes_from_locked_artifacts() -> None:
    module = _load_precision_module()
    observed = module.build_summary(ROOT)
    frozen = json.loads((ROOT / "artifacts/operator_portability_precision/derived_summary.json").read_text())
    assert observed["evidence_structure"] == frozen["evidence_structure"]
    for n in ("447", "452"):
        for key in ("w_80", "weighted_rms_pp_at_p0_5_80", "w_90", "weighted_rms_pp_at_p0_5_90"):
            assert abs(observed["precision"][n][key] - frozen["precision"][n][key]) < 1e-10
    for condition in frozen["observed"]:
        assert abs(observed["observed"][condition]["observed_w"] - frozen["observed"][condition]["observed_w"]) < 1e-12


def test_manuscript_counts_evidence_correctly_and_does_not_claim_equivalence() -> None:
    text = (ROOT / "manuscript/operator_portability.md").read_text(encoding="utf-8")
    lower = text.lower()
    assert "one independent fresh replication plus two process substitutions on a shared historical reference ensemble" in lower
    assert "not two independent replications" in lower
    assert "outcome summaries retained for protocol provenance" in lower
    assert "8.17" in text and "8.12" in text
    assert "no equivalence margin was preregistered" in lower
    assert "ecological modelling" in lower and "short communication" in lower


def test_nearest_neighbor_positioning_does_not_claim_semantic_novelty() -> None:
    refs = (ROOT / "manuscript/operator_portability_references.md").read_text(encoding="utf-8")
    manuscript = (ROOT / "manuscript/operator_portability.md").read_text(encoding="utf-8")
    assert "not** be framed as discovering" in refs
    assert "The semantic problem is not new" in manuscript
    for token in ("Tischendorf", "Lowe", "Cramer", "Liczner"):
        assert token in refs and token in manuscript
