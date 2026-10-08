from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "experiments/yht_spatial_warning_protocol.json"
COVERAGE = ROOT / "artifacts/yht_spatial_warning/official_movebank_coverage_overlap_stop.json"


def test_yht_official_primary_stops_before_demographic_outcome_fit() -> None:
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    c = json.loads(COVERAGE.read_text(encoding="utf-8"))
    assert p["initial_lock_status"] == "design_locked_after_public_summary_exposure_before_row_level_join_and_model_fit"
    assert p["status"] == "stopped_before_outcome_fit_insufficient_temporal_overlap"
    assert p["result_source"]["official_coverage_summary"] == str(COVERAGE.relative_to(ROOT))
    assert p["result_source"]["official_workflow_run"] == 37724527236
    years = c["years_meeting_frozen_gates"]
    cutoff = c["primary_demography"]["maximum_allowed_autumn_year"]
    intersection = [year for year in years if year <= cutoff]
    assert intersection == [2004, 2013, 2014, 2015, 2016, 2017]
    assert c["intersection_of_official_eligible_movement_and_published_primary_outcome_years"] == intersection
    assert p["result_source"]["observed_eligible_forecast_years"] == intersection
    assert len(intersection) == 6 < p["primary_models"]["minimum_total_eligible_annual_observations"] == 11
    assert p["result_source"]["future_outcome_rows_opened"] == 0
    assert p["result_source"]["future_forecast_models_fit"] == 0
    assert c["fitted_forecast_models"] == 0
