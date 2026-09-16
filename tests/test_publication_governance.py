from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _flat(path: str) -> str:
    return " ".join((ROOT / path).read_text(encoding="utf-8").split())


def test_router_has_one_active_flagship_and_two_frozen_fallbacks() -> None:
    registry = json.loads((ROOT / "manuscript/publication_lanes.json").read_text(encoding="utf-8"))
    assert registry["schema_version"] == 6
    assert registry["current_submission_strategy"] == "flagship_first_no_simultaneous_overlap"
    assert set(registry["active_lanes"]) == {"nee_flagship"}
    assert registry["active_lanes"]["nee_flagship"]["status"] == "active_primary_submission"
    assert set(registry["frozen_fallback_lanes"]) == {"warning_validity", "state_validity"}
    assert all(
        lane["status"] == "frozen_fallback_not_for_simultaneous_submission"
        for lane in registry["frozen_fallback_lanes"].values()
    )
    assert registry["exclusivity_policy"]["simultaneous_overlapping_submission_allowed"] is False


def test_flagship_overlap_and_unique_evidence_are_explicit() -> None:
    registry = json.loads((ROOT / "manuscript/publication_lanes.json").read_text(encoding="utf-8"))
    flagship = registry["active_lanes"]["nee_flagship"]
    assert {"0.2543", "+5.33_pp_g20", "+5.20_pp_g40"} <= set(
        flagship["reused_fallback_evidence"]["state_validity"]
    )
    assert {"35/35", "48/48", "33/33", "49/49", "specificity_0", "binary_auc_0.5"} <= set(
        flagship["reused_fallback_evidence"]["warning_validity"]
    )
    unique = set(flagship["flagship_only_load_bearing_evidence"])
    assert "continuous_last_refuge_auc_0.92734" in unique
    assert "route_margin_minus_max_q_auc_+0.02135" in unique
    assert "allele_sorting_single_edge_DID_+6.883_pp" in unique


def test_cover_letter_exclusivity_is_not_mutually_contradictory() -> None:
    flagship = _flat("manuscript/nee_flagship_cover_letter.md")
    state = _flat("manuscript/cover_letter.md")
    assert "substantially overlapping standalone manuscript" in flagship
    assert "simultaneously submitted" in flagship
    assert "FROZEN FALLBACK" in state
    assert "REACTIVATION GATE" in state
    assert "flagship" in state.lower()


def test_warning_fallback_cannot_hide_later_holdout() -> None:
    warning = _flat("manuscript/warning_validity.md")
    assert "FROZEN FALLBACK" in warning
    assert "0.92734" in warning
    assert "+0.02135" in warning
    assert "0.23253" in warning
    assert "post-hoc sign rescue" in warning


def test_h_alpha_inversion_is_reported_without_sign_flip() -> None:
    artifact = json.loads((ROOT / "artifacts/last_refuge_warning_holdout/locked_result.json").read_text(encoding="utf-8"))
    assert artifact["comparators"]["co_timed_H_alpha_auc"] == 0.23253096665858794
    article = _flat("manuscript/nee_flagship_article.md")
    result = _flat("docs/LAST_REFUGE_WARNING_HOLDOUT_RESULTS_2026-09-07.md")
    for text in (article, result):
        assert "0.23253" in text
        assert "directionally inverted" in text
        assert "post hoc" in text


def test_current_status_supersedes_old_router() -> None:
    current = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-16.md")
    prior = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md")
    historical = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-05.md")
    assert "operational submission-status source of truth" in current
    assert "one active EGWE submission lane" in current
    assert "1603ae26103510b9f7b0c2c7030a9dccd9c54897" in current
    assert "Journal of Ecology" in current
    assert "5 independent programme/study clusters / 17 marginal Hedges-g effects" in current
    assert "SUPERSEDED" in prior
    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-16.md" in prior
    assert "SUPERSEDED" in historical


def test_egwee_empirical_lane_is_current_and_independent() -> None:
    registry = json.loads((ROOT / "manuscript/publication_lanes.json").read_text(encoding="utf-8"))
    lane = registry["independent_development_programs"]["empirical_multilayer_meta_analysis"]
    assert lane["repository_commit"] == "16308cf6d6e4aec274504ba81bbf6e71be465099"
    assert lane["status"] == "submission_ready_pending_author_metadata"
    assert lane["final_target"] == "Journal of Ecology"
    assert lane["primary_direct_clusters"] == 5
    assert lane["primary_marginal_effects"] == 17
    assert lane["primary_fisher_p"] == 0.01212432
    assert lane["omit_ML001_p"] == 0.18194353
    assert lane["covariance_free_bound_p"] == 0.28061178
    assert registry["active_lanes"]["nee_flagship"]["natural_evidence_role"] == "bounded_discussion_external_consistency_not_load_bearing"


def test_frozen_fallbacks_forbid_stale_active_status_phrases() -> None:
    warning = _flat("manuscript/warning_validity.md")
    state = _flat("manuscript/state_validity_and_empirical_measurement_gates.md")
    assert "FROZEN FALLBACK" in warning
    assert "active warning-validity manuscript" not in warning
    assert "sole active publication lane" not in warning
    assert "FROZEN FALLBACK" in state
    assert "active state-validity manuscript" not in state


def test_superseded_spine_forbids_obsolete_submission_ready_claim() -> None:
    grand = _flat("manuscript/grand_synthesis_flagship.md")
    assert "SUPERSEDED INITIAL FLAGSHIP SPINE" in grand
    assert "does not supersede the submission-ready" not in grand
    assert "submission-ready EGC, EGWE-state, EGWE-warning" not in grand


def test_portability_has_package_ready_development_owner_without_flagship_claim_leakage() -> None:
    registry = json.loads((ROOT / "manuscript/publication_lanes.json").read_text(encoding="utf-8"))
    lane = registry["independent_output_lanes"]["operator_portability"]
    assert lane["status"] == "active_development_nonoverlap_candidate"
    assert lane["submission_state"] == "package_ready_pending_author_metadata_and_final_policy_check"
    assert lane["development_allowed_while_flagship_under_consideration"] is True
    assert "process_specific_portability" in lane["owned_claims"]
    assert registry["frozen_fallback_lanes"]["state_validity"]["current_portability_owner"] == "operator_portability"
    assert lane["development_note"] == "manuscript/operator_portability.md"
    assert lane["manuscript"] == "manuscript/operator_portability_short_communication.md"
    for field in ("cover_letter", "highlights", "display_plan", "submission_metadata", "submission_checklist", "overlap_audit", "submission_checker", "bundle_builder", "figure_builder", "submission_package_ci"):
        assert (ROOT / lane[field]).is_file(), lane[field]
    for figure in lane["figures"]:
        assert (ROOT / figure).is_file(), figure

    development = _flat(lane["development_note"])
    for required in ("historical_m010_heterogeneity_not_freshly_replicated", "whole-individual", "pollen-only"):
        assert required in development

    submission = _flat(lane["manuscript"])
    for required in ("one independent fresh replication", "same historical reference observations", "not equivalence"):
        assert required in submission
    for forbidden in ("0.2543", "+5.33", "+5.20", "35/35", "48/48", "0.92734", "+6.883", "1,920,000"):
        assert forbidden not in submission
