from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_frontier_retains_primary_yht_stop_and_no_fate_fit() -> None:
    ledger = load("artifacts/spatial_warning_validation/source_gate_registry.json")
    official = load("artifacts/yht_spatial_warning/official_movebank_coverage_overlap_stop.json")

    by_id = {row["id"]: row for row in ledger["entries"]}
    y = by_id["YHT_original_primary"]
    assert y["status"] == "STOP_INSUFFICIENT_TEMPORAL_OVERLAP_BEFORE_OUTCOME_FIT"
    assert y["temporal_match"]["forecast_eligible_years"] == official[
        "intersection_of_official_eligible_movement_and_published_primary_outcome_years"
    ]
    assert y["temporal_match"]["n_eligible"] == official[
        "n_maximum_temporally_aligned_primary_years"
    ] == 6
    assert y["temporal_match"]["frozen_minimum"] == official["protocol_minimum_years"] == 11
    assert y["future_model_fitted"] is False
    assert official["fitted_forecast_models"] == 0
    assert official["outcome_rows_parsed_for_this_decision"] == 0


def test_frontier_does_not_promote_panel_or_other_proxy_to_love_otto_fate_warning() -> None:
    ledger = load("artifacts/spatial_warning_validation/source_gate_registry.json")
    panel = load("artifacts/yht_spatial_warning/official_panel_sensitivity_result.json")
    mac = load("artifacts/mac_hugh_recruitment/temporal_result_locked.json")[
        "scientific_result"
    ]
    by_id = {row["id"]: row for row in ledger["entries"]}

    p = by_id["YHT_measurement_panel"]
    assert p["status"] == "OUTCOME_FREE_EXPLORATORY_MEASUREMENT_SENSITIVITY"
    assert p["n_days"] == panel["overall"]["number_of_eligible_days"] == 474
    assert p["n_future_demographic_fits"] == 0
    assert panel["provenance"]["source_outcome_rows_opened"] == 0

    m = by_id["MacHugh_recruitment_temporal"]
    assert m["status"] == "NO_INCREMENTAL_TRANSFERABLE_GAIN_FOR_DIFFERENT_SPATIAL_PROXY"
    assert m["direct_love_otto_cv_test"] is False
    assert mac["direct_love_otto_cv_test"] is False
    assert m["n_heldout_years"] == mac["n_heldout_forecasts"] == 16
    assert m["rmse_M1"] > m["rmse_M0"]


def test_candidate_access_constraints_remain_explicit() -> None:
    ledger = load("artifacts/spatial_warning_validation/source_gate_registry.json")
    by_id = {row["id"]: row for row in ledger["entries"]}
    assert by_id["Bathurst"]["status"].startswith("HOLD_")
    assert by_id["CentralArctic"]["status"] == "HOLD_GPS_NOT_PUBLIC_UNDER_STATE_RESTRICTION"
    assert len(ledger["claim_boundaries"]) >= 5
