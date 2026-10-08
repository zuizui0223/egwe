"""Reproducible, fail-closed audit for project-documented exPt2 source scope.

This validates source-label, cohort and access-status distinctions only.
It never reads biological observations and is independent of model outcomes.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"artifacts/empirical/expt2_forward_source_eligibility_20261008.json"

def validate(record: dict) -> dict:
    assert record["schema_version"] == 1
    assert record["audit_level"].startswith("public source")
    assert record["natural_hr_status"] == "NOT_IDENTIFIABLE_NO_VERIFIED_MATCHED_FORWARD_DATA"
    q=record["key_checks"]
    assert q["exposure_plot"]["value"] == "exPt2"
    assert q["proposed_expt1_core"]["value"] == "exPt1"
    assert q["proposed_expt1_core"]["status"] == "confirmed_not_same_plot"
    assert q["public_catalog"]["public_core"] == "exPt1"
    assert q["public_catalog"]["status"] == "no_positively_identified_expt2_individual_2019_plus_panel"
    assert q["expt2_2019_operational_observations"]["status"] == "confirmed_aggregate_only"
    assert q["expt2_2024_operational_observations"]["status"] == "confirmed_aggregate_only"
    assert q["expt2_2024_raw_locations"]["status"] == "operational_locations_not_public_download_verified"
    assert q["pearson_2018_to_2019plus_individual_id_crosswalk"]["status"] == "not_verified"
    assert q["pearson_2018_to_2019plus_individual_id_crosswalk"]["raw_join_performed"] is False
    assert q["direct_expt2_future_functional_endpoint"]["status"] == "not_verified"
    assert q["direct_expt2_future_functional_endpoint"]["outcomes_opened"] is False
    assert q["independent_heldout_future_units"]["status"] == "not_verified"
    assert record["route_decision"] == "STOP_EXPT1_JOIN; HOLD_EXPT2_MATCHED_PUBLIC_FORWARD_DATA"
    assert record["empirical_loss_claim"] is False
    return {"route_decision":record["route_decision"],"future_outcomes_opened":False,
            "same_plot_longitudinal_join_verified":False,"not_biological_null":True}

def main() -> None:
    value=json.loads(SOURCE.read_text(encoding="utf-8"))
    print("EXPT2_PUBLIC_FORWARD_GATE "+json.dumps(validate(value),sort_keys=True))

if __name__=="__main__":
    main()
