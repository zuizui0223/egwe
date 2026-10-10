from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0,str(SCRIPTS))
SPEC=importlib.util.spec_from_file_location(
    "truth_bridge",SCRIPTS/"audit_pollipi_independent_visits.py")
assert SPEC and SPEC.loader
TRUTH=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRUTH)


def _manifest() -> dict:
    plants=[]
    for i,score in enumerate([.1,.3,.7,.9],start=1):
        plants.append({
            "site_id":"site_A","patch_id":f"patch_{i}",
            "plant_id":f"plant_{i}","cohort":"2026",
            "pre_state_time_utc":"2026-10-09T12:00:00Z",
            "pre_state_score":score,
            "genetic_assay_type":"synthetic",
            "planned_observation_effort_seconds":600,
            "externally_defined_visit_cap":8,
            "cap_provenance":"synthetic_capacity_not_empirical"
        })
    runs=[]
    for i in (1,4):
        runs.append({
            "run_id":f"R{i}","site_id":"site_A","patch_id":f"patch_{i}",
            "plant_id":f"plant_{i}","cohort":"2026",
            "window_end_utc":"2026-10-10T01:10:00Z",
            "offset_origin_utc":"2026-10-10T01:00:00Z",
            "independent_reference_file":f"reference_R{i}.mp4",
            "visits_csv":f"visits_R{i}.csv",
            "truth_source":"continuous_reference_video",
            "complete_independent_coverage_confirmed":True,
            "all_focal_flowers_visible_confirmed":True,
            "unresolved_reference_intervals":0,
        })
    return {
        "schema_version":1,
        "mode":"NO_COMPLETE_SITE_TOTAL",
        "analysis_unit":{
            "site_id":"site_A","cohort":"2026",
            "window_start_utc":"2026-10-10T01:00:00Z",
            "window_end_utc":"2026-10-10T01:10:00Z",
        },
        "plants":plants,"reference_runs":runs
    }


def _independent_csvs() -> dict:
    return {
        "visits_R1.csv":[{"event_id":f"V{i:02d}","start":float(i*10),
                          "end":float(i*10+3),
                          "truth_source":"continuous_reference_video",
                          "visitor_group":"bee"} for i in range(1,4)],
        "visits_R4.csv":[{"event_id":f"V{i:02d}","start":float(i*12),
                          "end":float(i*12+3),
                          "truth_source":"continuous_reference_video",
                          "visitor_group":"fly"} for i in range(1,8)]
    }


def _audit(payload: dict, rows: dict|None=None):
    events=_independent_csvs() if rows is None else rows
    def reader(filename):
        return list(TRUTH.REQUIRED_EVENT_COLUMNS|{"visitor_group"}),events[filename]
    return TRUTH.audit(payload,reader)


def test_synthetic_independent_video_source_yields_conditional_only_bounds() -> None:
    r=_audit(_manifest())
    assert r["status"]=="STRUCTURAL_INDEPENDENT_VISIT_ALIGNMENT_PASS"
    assert r["independent_reference_run_count"]==2
    assert r["tagged_run_event_count"]==10
    assert r["tagged_focal_unit_count"]==4
    assert r["sharp_no_total_interval_width"]==pytest.approx(.8/600)
    assert r["site_total_imputed"] is False
    assert r["future_reproduction_outcome_opened"] is False
    assert r["natural_HR_validated"] is False
    assert r["field_effect_inference_licensed"] is False
    assert r["uses_synthetic_state"] is True
    assert r["includes_controlled_event_schedule"] is False


def test_independent_full_reference_with_no_events_is_true_zero() -> None:
    manifest=_manifest()
    rows=_independent_csvs()
    rows["visits_R1.csv"]=[]
    r=_audit(manifest,rows)
    assert r["status"]=="STRUCTURAL_INDEPENDENT_VISIT_ALIGNMENT_PASS"
    assert r["tagged_run_event_count"]==7
    assert r["reference_runs"][0]["independently_annotated_visit_count"]==0


@pytest.mark.parametrize("mutate",[
    lambda x:x["reference_runs"][0].update(plant_id="another"),
    lambda x:x["reference_runs"][0].update(truth_source="pollipi_selected_image"),
    lambda x:x["reference_runs"][0].update(complete_independent_coverage_confirmed=False),
    lambda x:x["reference_runs"][0].update(all_focal_flowers_visible_confirmed=False),
    lambda x:x["reference_runs"][0].update(unresolved_reference_intervals=2),
    lambda x:x["reference_runs"][0].update(independent_reference_file="selected.jpg"),
    lambda x:x["reference_runs"][0].update(offset_origin_utc="2026-10-10T01:01:00Z"),
    lambda x:x["reference_runs"][0].update(window_end_utc="2026-10-10T01:09:00Z"),
    lambda x:x["reference_runs"][0].update(visits_csv="../secret.csv"),
    lambda x:x["plants"][0].update(pre_state_time_utc="2026-10-11T12:00:00Z"),
    lambda x:x["plants"][0].update(externally_defined_visit_cap=1),
    lambda x:x["plants"][0].update(cap_provenance="post_outcome_seed_set"),
    lambda x:x["plants"][0].update(planned_observation_effort_seconds=300),
    lambda x:x["plants"][1].update(plant_id="plant_1",patch_id="patch_1"),
    lambda x:x.update(mode="COMPLETE_SITE_TOTAL"),
])
def test_false_field_alignment_blocks(mutate) -> None:
    m=_manifest()
    mutate(m)
    with pytest.raises(ValueError):
        _audit(m)


@pytest.mark.parametrize("broken_event",[
    {"event_id":"V01","start":"-1","end":"2","truth_source":"continuous_reference_video"},
    {"event_id":"V01","start":"1","end":"0","truth_source":"continuous_reference_video"},
    {"event_id":"V01","start":"599","end":"605","truth_source":"continuous_reference_video"},
    {"event_id":"V01","start":"1","end":"2","truth_source":"pollipi_stills"},
    {"event_id":"","start":"1","end":"2","truth_source":"continuous_reference_video"},
])
def test_bad_true_visit_event_cannot_drive_covariance_bounds(broken_event) -> None:
    rows=_independent_csvs()
    rows["visits_R1.csv"][0]=broken_event
    with pytest.raises(ValueError):
        _audit(_manifest(),rows)


def test_duplicate_event_ids_rejected() -> None:
    rows=_independent_csvs()
    rows["visits_R1.csv"][1]["event_id"]="V01"
    with pytest.raises(ValueError,match="duplicate"):
        _audit(_manifest(),rows)


def test_missing_required_pollipi_event_columns_rejected() -> None:
    with pytest.raises(ValueError,match="mandatory"):
        TRUTH._parse_independent_reference(
            ["event_id","start","end"],[],600,"continuous_reference_video")


def test_same_visit_event_can_be_counted_once_per_distinct_reference_run() -> None:
    # PolliPi event IDs only need to be unique *within* each run.
    r=_audit(_manifest())
    assert r["reference_runs"][0]["independently_annotated_visit_count"]==3
    assert r["reference_runs"][1]["independently_annotated_visit_count"]==7


def test_project_field_contract_and_pollipi_truth_source_not_confused() -> None:
    source=json.loads(
        (ROOT/"artifacts/design/relational_visit_grain_contract_20261010.json")
        .read_text(encoding="utf-8"))
    assert source["pre_outcome_tables"]["visit_exposure"]["zero_observation_intervals_required"]
    assert "continuous_reference_video" in TRUTH.ALLOWED_TRUTH
    assert "high_frequency_reference_video" in TRUTH.ALLOWED_TRUTH
    assert "pollipi_selected_stills" not in TRUTH.ALLOWED_TRUTH
