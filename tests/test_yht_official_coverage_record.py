from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "artifacts/yht_spatial_warning/official_movebank_coverage_overlap_stop.json"


def test_official_movebank_coverage_is_provenanced_and_does_not_claim_future_warning() -> None:
    d = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert d["source"]["doi"] == "10.5441/001/1.5g4h5t6c"
    assert d["source"]["source_workflow_run"] == 37641755074
    assert d["source"]["source_workflow_status"] == "success"
    assert d["source"]["original_event_csv_sha256"] == (
        "1069cd7531d1d7a519cb817b09d015be91c552ecafab504869a81eb01eff4201"
    )
    assert d["source"]["raw_locations_in_repository"] is False
    assert d["n_movement_only_eligible_years"] == 8
    assert d["years_meeting_frozen_gates"] == [
        2004, 2013, 2014, 2015, 2016, 2017, 2018, 2019
    ]
    assert d["intersection_of_official_eligible_movement_and_published_primary_outcome_years"] == [
        2004, 2013, 2014, 2015, 2016, 2017
    ]
    assert d["n_maximum_temporally_aligned_primary_years"] == 6
    assert d["protocol_minimum_years"] == 11
    assert d["n_maximum_temporally_aligned_primary_years"] < d["protocol_minimum_years"]
    assert d["decision"] == "insufficient_temporal_replication_stop_before_demographic_outcome_fit"
    assert d["outcome_rows_parsed_for_this_decision"] == 0
    assert d["fitted_forecast_models"] == 0
    assert d["previously_nominal_but_observed_ineligible"]["2005"]["eligible_days"] == 0
    assert d["previously_nominal_but_observed_ineligible"]["2006"]["eligible_days"] == 0
