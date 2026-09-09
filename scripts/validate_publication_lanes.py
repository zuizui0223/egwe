from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "manuscript" / "publication_lanes.json"
HOLDOUT = ROOT / "artifacts" / "last_refuge_warning_holdout" / "locked_result.json"


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["schema_version"] == 5
    assert registry["current_submission_strategy"] == "flagship_first_no_simultaneous_overlap"

    active = registry["active_lanes"]
    assert set(active) == {"nee_flagship"}
    flagship = active["nee_flagship"]
    assert flagship["status"] == "active_primary_submission"
    assert flagship["primary_target"] == "Nature Ecology & Evolution"
    for field in ("manuscript", "cover_letter", "references", "display_plan", "source_manifest", "submission_metadata"):
        assert (ROOT / flagship[field]).is_file(), flagship[field]

    fallbacks = registry["frozen_fallback_lanes"]
    assert set(fallbacks) == {"warning_validity", "state_validity"}
    assert all(lane["status"] == "frozen_fallback_not_for_simultaneous_submission" for lane in fallbacks.values())
    fallback_paths = [lane["manuscript"] for lane in fallbacks.values()]
    assert len(fallback_paths) == len(set(fallback_paths)) == 2
    for path in fallback_paths:
        assert (ROOT / path).is_file(), path

    independent = registry["independent_output_lanes"]
    assert set(independent) == {"operator_portability"}
    portability = independent["operator_portability"]
    assert portability["status"] == "active_development_nonoverlap_candidate"
    assert portability["submission_state"] == "package_ready_pending_author_metadata_and_final_policy_check"
    assert portability["development_allowed_while_flagship_under_consideration"] is True
    assert set(portability["owned_claims"]) == {
        "process_specific_portability",
        "connectivity_operator_nonexchangeability",
        "historical_m010_heterogeneity_nonreplication",
    }
    for field in ("manuscript", "development_note", "cover_letter", "highlights", "display_plan", "submission_metadata", "submission_checklist", "overlap_audit", "submission_checker", "bundle_builder", "figure_builder", "submission_package_ci"):
        assert (ROOT / portability[field]).is_file(), portability[field]
    for figure in portability["figures"]:
        assert (ROOT / figure).is_file(), figure
    assert portability["provisional_target"] == "Ecological Modelling"
    assert portability["provisional_article_type"] == "Short Communication"
    assert portability["target_policy_checked_on"] == "2026-09-09"
    evidence_structure = portability["evidence_structure"]
    assert evidence_structure == {
        "independent_fresh_replications": 1,
        "shared_reference_operator_substitutions": 2,
        "phase_r_s_share_no_connectivity_and_allele_m010_blocks": True,
    }
    precision_boundary = portability["precision_boundary"]
    assert precision_boundary["interpretation"] == "precision_bounded_null_not_equivalence"
    assert 0.16 < precision_boundary["n447_w80"] < 0.17
    assert 0.16 < precision_boundary["n452_w80"] < 0.17
    for field in ("manuscript", "references", "precision_audit", "precision_summary"):
        assert (ROOT / portability[field]).is_file(), portability[field]

    exclusivity = registry["exclusivity_policy"]
    assert exclusivity["simultaneous_overlapping_submission_allowed"] is False
    assert set(exclusivity["active_lane_blocks_fallbacks"]) == {"warning_validity", "state_validity"}

    reused = flagship["reused_fallback_evidence"]
    assert set(reused) == {"state_validity", "warning_validity"}
    assert {"0.2543", "+5.33_pp_g20", "+5.20_pp_g40"} <= set(reused["state_validity"])
    assert {"35/35", "48/48", "33/33", "49/49", "specificity_0", "binary_auc_0.5"} <= set(reused["warning_validity"])
    flagship_only = set(flagship["flagship_only_load_bearing_evidence"])
    assert {
        "allele_sorting_single_edge_DID_+6.883_pp",
        "sorting_headroom_followup",
        "operator_balance_exact_transition_audit_1920000_of_1920000",
        "continuous_last_refuge_auc_0.92734",
        "route_margin_minus_max_q_auc_+0.02135",
    } <= flagship_only

    flagship_text = _flat(_read(flagship["manuscript"]))
    for token in (
        "0.2543",
        "+5.33",
        "+5.20",
        "+6.883",
        "1,920,000",
        "specificity 0",
        "AUC 0.5",
        "0.92734",
        "+0.02135",
        "0.23253",
        "directionally inverted",
    ):
        assert token in flagship_text, f"flagship missing governance-critical result: {token}"

    flagship_cover = _flat(_read(flagship["cover_letter"]))
    assert "substantially overlapping standalone manuscript" in flagship_cover
    assert "simultaneously submitted" in flagship_cover
    assert "flagship is under consideration" in flagship_cover

    state_cover = _flat(_read(fallbacks["state_validity"]["cover_letter"]))
    assert "FROZEN FALLBACK" in state_cover
    assert "REACTIVATION GATE" in state_cover
    assert "flagship" in state_cover.lower()

    warning_text = _flat(_read(fallbacks["warning_validity"]["manuscript"]))
    assert "FROZEN FALLBACK" in warning_text
    assert "last-refuge" in warning_text
    assert "active warning-validity manuscript" not in warning_text
    assert "sole active publication lane" not in warning_text
    for token in ("35/35", "48/48", "33/33", "49/49", "specificity was 0", "binary-marker AUC was 0.5"):
        assert token in warning_text, token

    state_text = _flat(_read(fallbacks["state_validity"]["manuscript"]))
    assert "FROZEN FALLBACK" in state_text
    assert "active state-validity manuscript" not in state_text
    assert "current process-portability development ownership is routed separately" in state_text
    for token in ("0.2543", "+5.33", "+5.20"):
        assert token in state_text, token

    development_text = _flat(_read(portability["development_note"]))
    for token in (
        "ACTIVE DEVELOPMENT LANE",
        "historical_m010_heterogeneity_not_freshly_replicated",
        "one independent fresh replication plus two process substitutions on a shared historical reference ensemble",
        "not two independent replications",
        "outcome summaries retained for protocol provenance",
        "no equivalence margin was preregistered",
        "Ecological Modelling",
        "Short Communication",
        "8.17",
        "8.12",
    ):
        assert token.lower() in development_text.lower(), token

    portability_text = _flat(_read(portability["manuscript"]))
    for token in (
        "## Abstract",
        "## Keywords",
        "one independent fresh replication",
        "same historical reference observations",
        "deterministic classifications",
        ".693686",
        ".811309",
        ".728205",
        "8.17",
        "8.12",
        "not equivalence",
    ):
        assert token.lower() in portability_text.lower(), token
    for forbidden in ("0.2543", "+5.33", "+5.20", "35/35", "48/48", "0.92734", "+6.883", "1,920,000"):
        assert forbidden not in portability_text, f"flagship/state/warning claim leaked into portability lane: {forbidden}"

    phase_r = json.loads((ROOT / "artifacts/process_resolved_movement/phase_r_locked_summary.json").read_text(encoding="utf-8"))
    phase_s = json.loads((ROOT / "artifacts/process_resolved_pollen/phase_s_locked_summary.json").read_text(encoding="utf-8"))
    r_conditions = {row["condition"]: row for row in phase_r["conditions"]}
    s_conditions = {row["condition"]: row for row in phase_s["conditions"]}
    assert r_conditions["no_connectivity"]["blocks"] == s_conditions["no_connectivity"]["blocks"]
    assert r_conditions["allele_only_m010"]["blocks"] == s_conditions["allele_only_m010"]["blocks"]
    precision = json.loads((ROOT / portability["precision_summary"]).read_text(encoding="utf-8"))
    assert precision["evidence_structure"]["phase_r_s_reference_blocks_identical"] is True
    assert abs(precision["precision"]["447"]["w_80"] - portability["precision_boundary"]["n447_w80"]) < 1e-12
    assert abs(precision["precision"]["452"]["w_80"] - portability["precision_boundary"]["n452_w80"]) < 1e-12

    holdout = json.loads(HOLDOUT.read_text(encoding="utf-8"))
    assert holdout["decision"] == "confirmed_route_margin_adds_ranking_beyond_q"
    assert abs(holdout["continuous_last_refuge_route_margin"]["mean_seed_block_auc"] - 0.9273378729277683) < 1e-15
    assert abs(holdout["route_margin_minus_co_timed_max_q_auc"]["mean"] - 0.02135425266165288) < 1e-15
    assert abs(holdout["comparators"]["co_timed_H_alpha_auc"] - 0.23253096665858794) < 1e-15

    holdout_note = _flat(_read("docs/LAST_REFUGE_WARNING_HOLDOUT_RESULTS_2026-09-07.md"))
    assert "0.23253" in holdout_note
    assert "directionally inverted" in holdout_note
    assert "not" in holdout_note and "post hoc" in holdout_note

    metadata = _flat(_read(flagship["submission_metadata"]))
    assert "0.23253" in metadata
    assert "flagship-first" in metadata.lower()

    status = _flat(_read("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md"))
    assert "operational submission-status source of truth" in status
    assert "aa579f5262cf1403e4a6fc4e3937d64fbb1f2a80" in status
    assert "one active EGWE submission lane" in status
    assert "frozen fallback" in status.lower()

    old_status = _flat(_read("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-05.md"))
    assert "SUPERSEDED" in old_status
    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-08.md" in old_status

    ownership = _flat(_read("manuscript/PUBLICATION_LANES.md"))
    for token in (
        "Active submission lane — NEE flagship",
        "Frozen fallback — state validity",
        "Frozen fallback — warning validity",
        "no simultaneous overlapping submission",
        "0.92734",
        "0.23253",
        "Independent development lane — operator portability",
        "operator_portability.md",
    ):
        assert token in ownership, token

    grand = _flat(_read("manuscript/grand_synthesis_flagship.md"))
    assert "SUPERSEDED INITIAL FLAGSHIP SPINE" in grand
    assert "nee_flagship_article.md" in grand
    assert "does not supersede the submission-ready" not in grand
    assert "submission-ready EGC, EGWE-state, EGWE-warning" not in grand

    router = _flat(_read("README.md"))
    assert "one active EGWE submission lane" in router
    assert "nee_flagship_article.md" in router
    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-08.md" in router
    assert "frozen fallback" in router.lower()
    assert "Publication crosswalk" in router
    assert "operator_portability.md" in router

    manuscript_router = _flat(_read("manuscript/README.md"))
    assert "nee_flagship_article.md" in manuscript_router
    assert "frozen fallback" in manuscript_router.lower()
    assert "operator_portability.md" in manuscript_router

    checklist = _flat(_read("manuscript/submission_checklist.md"))
    assert "one active EGWE submission lane" in checklist
    assert "flagship" in checklist.lower()

    natural = registry["independent_development_programs"]["natural_data_four_gate_program"]
    assert natural["status"] == "migrated_authoritative_in_egwee"
    assert natural["authoritative_repository"] == "zuizui0223/egwee"
    assert (ROOT / natural["manuscript"]).is_file()

    archive = registry["archive"]
    assert archive["status"] == "integrated_source_archive_not_for_submission"
    assert (ROOT / archive["manuscript"]).is_file()

    print(
        "Publication-governance validation passed: one active NEE flagship lane; "
        "state and warning manuscripts frozen as non-simultaneous fallbacks; "
        "operator portability has an independent non-submission development owner; "
        "stale active-status phrases are forbidden; H_alpha inversion reported."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
