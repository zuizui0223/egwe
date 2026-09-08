from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _flat(path: str) -> str:
    return " ".join((ROOT / path).read_text(encoding="utf-8").split())


def test_router_has_one_active_flagship_and_two_frozen_fallbacks() -> None:
    registry = json.loads((ROOT / "manuscript/publication_lanes.json").read_text(encoding="utf-8"))
    assert registry["schema_version"] == 4
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
    current = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md")
    historical = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-05.md")
    assert "operational submission-status source of truth" in current
    assert "one active EGWE submission lane" in current
    assert "aa579f5262cf1403e4a6fc4e3937d64fbb1f2a80" in current
    assert "SUPERSEDED" in historical
    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-08.md" in historical
