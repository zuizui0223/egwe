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
    assert registry["schema_version"] == 4
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
    assert "no overlapping standalone manuscript will be simultaneously submitted" in flagship_cover

    state_cover = _flat(_read(fallbacks["state_validity"]["cover_letter"]))
    assert "FROZEN FALLBACK" in state_cover
    assert "REACTIVATION GATE" in state_cover
    assert "flagship" in state_cover.lower()

    warning_text = _flat(_read(fallbacks["warning_validity"]["manuscript"]))
    assert "FROZEN FALLBACK" in warning_text
    assert "last-refuge" in warning_text
    for token in ("35/35", "48/48", "33/33", "49/49", "specificity was 0", "binary-marker AUC was 0.5"):
        assert token in warning_text, token

    state_text = _flat(_read(fallbacks["state_validity"]["manuscript"]))
    for token in ("0.2543", "+5.33", "+5.20"):
        assert token in state_text, token

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
    ):
        assert token in ownership, token

    grand = _flat(_read("manuscript/grand_synthesis_flagship.md"))
    assert "SUPERSEDED INITIAL FLAGSHIP SPINE" in grand
    assert "nee_flagship_article.md" in grand

    router = _flat(_read("README.md"))
    assert "one active EGWE submission lane" in router
    assert "nee_flagship_article.md" in router
    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-08.md" in router
    assert "frozen fallback" in router.lower()
    assert "Publication crosswalk" in router

    manuscript_router = _flat(_read("manuscript/README.md"))
    assert "nee_flagship_article.md" in manuscript_router
    assert "frozen fallback" in manuscript_router.lower()

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
        "flagship overlap and unique evidence explicitly registered; H_alpha inversion reported."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
