from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {count}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Machine-readable registry: surface the evidence structure, precision boundary, and provisional outlet.
registry_path = ROOT / "manuscript/publication_lanes.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
if registry.get("schema_version") != 5:
    raise RuntimeError(f"unexpected schema {registry.get('schema_version')}")
portability = registry["independent_output_lanes"]["operator_portability"]
portability.update({
    "references": "manuscript/operator_portability_references.md",
    "precision_audit": "docs/OPERATOR_PORTABILITY_PRECISION_AUDIT_2026-09-09.md",
    "precision_summary": "artifacts/operator_portability_precision/derived_summary.json",
    "provisional_target": "Ecological Modelling",
    "provisional_article_type": "Short Communication",
    "target_policy_checked_on": "2026-09-09",
    "evidence_structure": {
        "independent_fresh_replications": 1,
        "shared_reference_operator_substitutions": 2,
        "phase_r_s_share_no_connectivity_and_allele_m010_blocks": True,
    },
    "precision_boundary": {
        "test": "five-block Pearson equal-rate",
        "alpha": 0.05,
        "n447_w80": 0.16340398762459762,
        "n452_w80": 0.16249769118660848,
        "approx_weighted_rms_pp_at_p0_5": "8.1-8.2",
        "interpretation": "precision_bounded_null_not_equivalence",
    },
    "nearest_neighbor_positioning": "semantic_process_distinctions_are_known; contribution_is_controlled_operator_portability_audit",
})
portability["submission_requires"] = [
    "claim_overlap_audit_against_current_flagship_and_any_reactivated_fallback",
    "final_reference_and_nearest_neighbor_check",
    "independent_cover_letter_display_plan_and_bundle",
    "author_approval",
    "live_Ecological_Modelling_Short_Communication_policy_recheck",
]
registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Human router: do not leave target/precision decisions only in the manuscript.
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "- **Status:** `active_development_nonoverlap_candidate`; **not submission-ready**.\n- **Owned claim:** process-specific portability / semantic identification of connectivity operators.\n- **Locked evidence:** Phase U fresh non-replication of historical allele-only `m=.10` heterogeneity, Phase R whole-individual dispersal, and Phase S pollen-only gene flow.\n- **Parallel-development rule:** development may proceed while the NEE flagship is under consideration because this lane deliberately excludes the flagship's aligned-state, operator-balance and warning/reserve claims.\n- **Submission gate:** fresh claim-overlap audit, nearest-neighbour literature audit, independent submission package, author approval and live journal-policy check.",
    "- **Status:** `active_development_nonoverlap_candidate`; **not submission-ready**.\n- **Provisional outlet:** ***Ecological Modelling* — Short Communication**; live policy/format recheck remains mandatory before submission.\n- **Owned claim:** process-specific portability / semantic identification of connectivity operators.\n- **Evidence structure:** **one independent fresh replication (Phase U) plus two process substitutions on one shared historical reference ensemble (Phases R/S)**. R and S reuse exactly the same no-connectivity and allele-only `m=.10` comparator blocks and must not be counted as independent baseline replications.\n- **Precision boundary:** the five-block equal-rate tests have an 80%-power benchmark of `w≈0.163` at `N=447–452`, approximately **8.1–8.2 pp weighted RMS block-rate deviation near p=.5**. Non-significance is therefore precision-bounded, not equivalence.\n- **Locked evidence:** Phase U fresh non-replication of historical allele-only `m=.10` heterogeneity, Phase R whole-individual dispersal, and Phase S pollen-only gene flow.\n- **Parallel-development rule:** development may proceed while the NEE flagship is under consideration because this lane deliberately excludes the flagship's aligned-state, operator-balance and warning/reserve claims.\n- **Submission gate:** fresh claim-overlap audit, final nearest-neighbour/reference check, independent submission package, author approval and live *Ecological Modelling* Short Communication policy check."
)

replace_once(
    "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md",
    "This is **not** a second active submission. It is an active development lane. The claim is deliberately separated from the flagship's alignment, sorting, buffering, recoupling, density-gate and last-refuge results. Submission requires a fresh overlap audit, literature/nearest-neighbour positioning, an independent package, author approval and a live journal-policy check.",
    "This is **not** a second active submission. It is an active development lane. The claim is deliberately separated from the flagship's alignment, sorting, buffering, recoupling, density-gate and last-refuge results. The evidence is now explicitly counted as **one independent fresh replication plus two process substitutions sharing one historical reference ensemble**, not three independent replications. A deterministic precision audit bounds the non-significant equal-rate results: the present five-block designs have an 80%-power benchmark near `w=0.163` (about **8.1–8.2 pp weighted RMS block-rate deviation near p=.5**), so equivalence is not claimed. The provisional outlet is ***Ecological Modelling* — Short Communication**. Submission still requires a fresh overlap audit, final nearest-neighbour/reference checking, an independent package, author approval and a live journal-policy check."
)

# Top-level README: one sentence is enough; detailed development governance stays in the router.
replace_once(
    "README.md",
    "The historical allele-frequency-mixing `m=.10` equal-rate signal did not reproduce in one independent fresh Phase-U ensemble and did not port to whole-individual or pollen-only movement closures. No robust portable connectivity heterogeneity effect is established. This result now has an explicit independent development surface, [`manuscript/operator_portability.md`](manuscript/operator_portability.md), rather than being orphaned inside the frozen state fallback.",
    "The historical allele-frequency-mixing `m=.10` equal-rate signal did not reproduce in one independent fresh Phase-U ensemble and did not port to whole-individual or pollen-only movement closures. Phases R/S share the same historical reference blocks, so the evidence is **one independent replication plus two shared-reference operator substitutions**, not three replications. No robust portable connectivity heterogeneity effect is established. The precision audit bounds the nulls rather than declaring equivalence, and the result has an explicit independent development surface, [`manuscript/operator_portability.md`](manuscript/operator_portability.md), provisionally scoped as an *Ecological Modelling* Short Communication."
)

# Validator: machine-check the new development decisions and evidence accounting.
validator_path = ROOT / "scripts/validate_publication_lanes.py"
validator = validator_path.read_text(encoding="utf-8")
anchor = '    assert (ROOT / portability["manuscript"]).is_file()\n'
insert = '''    assert portability["provisional_target"] == "Ecological Modelling"\n    assert portability["provisional_article_type"] == "Short Communication"\n    assert portability["target_policy_checked_on"] == "2026-09-09"\n    evidence_structure = portability["evidence_structure"]\n    assert evidence_structure == {\n        "independent_fresh_replications": 1,\n        "shared_reference_operator_substitutions": 2,\n        "phase_r_s_share_no_connectivity_and_allele_m010_blocks": True,\n    }\n    precision_boundary = portability["precision_boundary"]\n    assert precision_boundary["interpretation"] == "precision_bounded_null_not_equivalence"\n    assert 0.16 < precision_boundary["n447_w80"] < 0.17\n    assert 0.16 < precision_boundary["n452_w80"] < 0.17\n    for field in ("manuscript", "references", "precision_audit", "precision_summary"):\n        assert (ROOT / portability[field]).is_file(), portability[field]\n'''
if validator.count(anchor) != 1:
    raise RuntimeError("validator portability file anchor mismatch")
validator = validator.replace(anchor, anchor + insert, 1)

anchor2 = '        ".728",\n    ):\n        assert token.lower() in portability_text.lower(), token\n'
insert2 = '''        "one independent fresh replication plus two process substitutions on a shared historical reference ensemble",\n        "not two independent replications",\n        "outcome summaries retained for protocol provenance",\n        "no equivalence margin was preregistered",\n        "Ecological Modelling",\n        "Short Communication",\n        "8.17",\n        "8.12",\n'''
if validator.count(anchor2) != 1:
    raise RuntimeError("validator portability token anchor mismatch")
validator = validator.replace(anchor2, '        ".728",\n' + insert2 + '    ):\n        assert token.lower() in portability_text.lower(), token\n', 1)

anchor3 = '    for forbidden in ("0.2543", "+5.33", "+5.20", "35/35", "48/48", "0.92734", "+6.883", "1,920,000"):\n        assert forbidden not in portability_text, f"flagship/state/warning claim leaked into portability lane: {forbidden}"\n'
insert3 = '''\n    phase_r = json.loads((ROOT / "artifacts/process_resolved_movement/phase_r_locked_summary.json").read_text(encoding="utf-8"))\n    phase_s = json.loads((ROOT / "artifacts/process_resolved_pollen/phase_s_locked_summary.json").read_text(encoding="utf-8"))\n    r_conditions = {row["condition"]: row for row in phase_r["conditions"]}\n    s_conditions = {row["condition"]: row for row in phase_s["conditions"]}\n    assert r_conditions["no_connectivity"]["blocks"] == s_conditions["no_connectivity"]["blocks"]\n    assert r_conditions["allele_only_m010"]["blocks"] == s_conditions["allele_only_m010"]["blocks"]\n    precision = json.loads((ROOT / portability["precision_summary"]).read_text(encoding="utf-8"))\n    assert precision["evidence_structure"]["phase_r_s_reference_blocks_identical"] is True\n    assert abs(precision["precision"]["447"]["w_80"] - portability["precision_boundary"]["n447_w80"]) < 1e-12\n    assert abs(precision["precision"]["452"]["w_80"] - portability["precision_boundary"]["n452_w80"]) < 1e-12\n'''
if validator.count(anchor3) != 1:
    raise RuntimeError("validator forbidden-token anchor mismatch")
validator = validator.replace(anchor3, anchor3 + insert3, 1)
validator_path.write_text(validator, encoding="utf-8")

print("Synced operator-portability evidence structure, precision boundary and provisional outlet")
