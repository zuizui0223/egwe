"""Fail-closed EGWE bridge to PolliPi independent visit-event truth CSVs.

PolliPi contract: docs/VISIT_EVENT_TRUTH_CONTRACT.md at zuizui0223/pollipi.
The PolliPi event file has event_id,start,end,truth_source, with second
offsets from the first reference probe. It has NO plant ID: the run manifest
must uniquely bind the file to one pre-tagged focal plant and a synchronized
observation window. Frames, shadow decisions and image-level visit_labels
are NOT independent visit truth.

This audit does NOT read future fruits/seeds or estimate any ecological
predictive effect. Conditional covariance bounds are mathematical and depend
on exact-count, independently bounded visitor opportunities.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from plan_visit_monitoring import conditional_bounds_without_site_total

ALLOWED_TRUTH={
    "continuous_reference_video",
    "high_frequency_reference_video",
    "controlled_event_schedule",
    "independent_sensor",
}
REQUIRED_EVENT_COLUMNS={"event_id","start","end","truth_source"}


def _time(value: str) -> datetime:
    if not isinstance(value,str) or not value:
        raise ValueError("window and pre-state times require explicit UTC ISO timestamp")
    try:
        parsed=datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError as err:
        raise ValueError("invalid ISO timestamp") from err
    if parsed.tzinfo is None or parsed.utcoffset()!=timezone.utc.utcoffset(parsed):
        raise ValueError("all time windows must use timezone-aware UTC")
    return parsed.astimezone(timezone.utc)


def _finite_float(row: dict,key: str, minimum: float | None = None) -> float:
    try:
        out=float(row[key])
    except (KeyError,TypeError,ValueError) as err:
        raise ValueError(f"{key} missing or nonnumeric") from err
    if not math.isfinite(out) or (minimum is not None and out<minimum):
        raise ValueError(f"{key} must be finite and at least {minimum}")
    return out


def _key(row: dict) -> str:
    return "/".join(str(row[x]) for x in ("site_id","patch_id","plant_id","cohort"))


def _nonblank(row: dict,key: str) -> str:
    value=row.get(key)
    if not isinstance(value,str) or not value.strip():
        raise ValueError(f"{key} must be nonblank")
    return value


def _parse_independent_reference(
    fields: list[str] | None, events: list[dict], duration: float,
    expected_truth_source: str,
) -> dict:
    if fields is None or not REQUIRED_EVENT_COLUMNS.issubset(fields):
        raise ValueError("PolliPi visit truth CSV missing mandatory columns")
    if expected_truth_source not in ALLOWED_TRUTH:
        raise ValueError("reference truth source is not independent PolliPi truth")
    event_ids=set()
    groups={}
    for ev in events:
        eid=_nonblank(ev,"event_id")
        if eid in event_ids:
            raise ValueError("duplicate event ID within one reference run")
        event_ids.add(eid)
        if ev.get("truth_source")!=expected_truth_source:
            raise ValueError("event truth source differs from independent reference run")
        start=_finite_float(ev,"start",0)
        end=_finite_float(ev,"end",0)
        if end<start or end>duration+1e-7:
            raise ValueError("visit interval outside independent observation coverage")
        guild=str(ev.get("visitor_group") or "unknown")
        groups[guild]=groups.get(guild,0)+1
    return {
        "independently_annotated_visit_count":len(events),
        "visitor_groups":groups,
        "event_file_has_required_columns":True,
        "zero_events_accepted_only_under_independent_full_coverage":True,
    }


def audit(
    payload: dict,
    event_reader: Callable[[str],tuple[list[str]|None,list[dict]]],
) -> dict:
    """Audit one site+cohort with synced, individually named run windows.

    Any STOP prevents promoting camera/still metadata to effective visits.
    The returned bounds depend only on the declared *state score*, cap,
    exposure and independently annotated direct visits; not seed success.
    """
    if payload.get("schema_version")!=1:
        raise ValueError("unsupported manifest schema")
    if payload.get("mode")!="NO_COMPLETE_SITE_TOTAL":
        raise ValueError("this bridge explicitly forbids inventing site visit totals")
    unit=payload.get("analysis_unit")
    if not isinstance(unit,dict):
        raise ValueError("missing site/cohort analysis unit")
    site=_nonblank(unit,"site_id")
    cohort=_nonblank(unit,"cohort")
    start=_time(_nonblank(unit,"window_start_utc"))
    end=_time(_nonblank(unit,"window_end_utc"))
    duration=(end-start).total_seconds()
    if duration<=0:
        raise ValueError("nonpositive common visit observation window")
    plants=payload.get("plants")
    runs=payload.get("reference_runs")
    if not isinstance(plants,list) or len(plants)<2 or not isinstance(runs,list) or not runs:
        raise ValueError("need at least two plants and one independent reference run")
    ids=[]
    g=[]
    efforts=[]
    caps=[]
    keyed={}
    for index,plant in enumerate(plants):
        for name in ("site_id","patch_id","plant_id","cohort","genetic_assay_type","cap_provenance"):
            _nonblank(plant,name)
        if plant["site_id"]!=site or plant["cohort"]!=cohort:
            raise ValueError("plant in another site or cohort")
        if _time(_nonblank(plant,"pre_state_time_utc"))>=start:
            raise ValueError("genetic/trait state measured after visit window begins")
        if plant["cap_provenance"].lower().startswith(("post_outcome","seed","fruit")):
            raise ValueError("visit cap cannot be selected using future reproduction")
        key=_key(plant)
        if key in keyed:
            raise ValueError("duplicate focal plant/patch/cohort key")
        keyed[key]=index
        ids.append(key)
        g.append(_finite_float(plant,"pre_state_score"))
        effort=_finite_float(plant,"planned_observation_effort_seconds",1e-12)
        if abs(effort-duration)>1e-6:
            raise ValueError("every focal plant must have the same full observation opportunity")
        efforts.append(effort)
        caps.append(_finite_float(plant,"externally_defined_visit_cap",0))

    visited={}
    seen_run_ids=set()
    evidence=[]
    for run in runs:
        for key in ("site_id","patch_id","plant_id","cohort","run_id",
                    "independent_reference_file","visits_csv",
                    "offset_origin_utc","truth_source"):
            _nonblank(run,key)
        if _key(run) not in keyed:
            raise ValueError("reference run has no exact tagged focal plant key")
        idx=keyed[_key(run)]
        if idx in visited:
            raise ValueError("duplicate reference run for same focal plant/window")
        if run["run_id"] in seen_run_ids:
            raise ValueError("duplicate run ID")
        seen_run_ids.add(run["run_id"])
        if _time(run["offset_origin_utc"])!=start:
            raise ValueError("event offsets do not begin at common synchronized UTC window")
        if _time(_nonblank(run,"window_end_utc"))!=end:
            raise ValueError("reference run does not cover full synchronized window")
        if run.get("complete_independent_coverage_confirmed") is not True:
            raise ValueError("independent reference coverage must include zero-visit periods")
        if run.get("all_focal_flowers_visible_confirmed") is not True:
            raise ValueError("cannot count all plant visits without complete flower visibility")
        if run.get("unresolved_reference_intervals",None)!=0:
            raise ValueError("unresolved independent-reference intervals remain")
        reference_file=run["independent_reference_file"].lower()
        if reference_file.endswith((".jpg",".jpeg",".png")):
            raise ValueError("a selected still image cannot serve as independent event truth")
        if run["truth_source"] not in ALLOWED_TRUTH:
            raise ValueError("forbidden nonindependent truth source")
        filename=run["visits_csv"]
        if not filename.endswith(".csv") or "/" in filename or "\\" in filename or filename.startswith("."):
            raise ValueError("visits csv must be a single local CSV filename")
        fields,events=event_reader(filename)
        result=_parse_independent_reference(fields,events,duration,run["truth_source"])
        count=result["independently_annotated_visit_count"]
        if count>caps[idx]+1e-7:
            raise ValueError("observed true visit count exceeds predeclared visit cap")
        visited[idx]=count
        evidence.append({
            "run_id":run["run_id"],
            "focal_unit_key":ids[idx],
            "truth_source":run["truth_source"],
            "independent_reference_file":run["independent_reference_file"],
            "observation_duration_seconds":duration,
            **result,
        })
    # Deliberately no synthetic site-wide count. This branch only needs
    # independently justified visit caps on all unmonitored plants.
    bound=conditional_bounds_without_site_total(
        g,visited,effort=efforts,visit_caps=caps)
    synthetic=any(plant["genetic_assay_type"].lower()=="synthetic"
                  for plant in plants)
    controlled=any(run["truth_source"]=="controlled_event_schedule" for run in runs)
    return {
        "status":"STRUCTURAL_INDEPENDENT_VISIT_ALIGNMENT_PASS",
        "analysis_site":site,
        "cohort":cohort,
        "observation_start_utc":start.isoformat(),
        "observation_end_utc":end.isoformat(),
        "tagged_focal_unit_count":len(plants),
        "independent_reference_run_count":len(runs),
        "tagged_run_event_count":sum(visited.values()),
        "reference_runs":evidence,
        "sharp_no_total_covariance_interval":[
            bound["covariance_lower_sharp"],
            bound["covariance_upper_sharp"],
        ],
        "sharp_no_total_interval_width":bound["interval_width"],
        "site_total_imputed":False,
        "future_reproduction_outcome_opened":False,
        "natural_HR_validated":False,
        "uses_synthetic_state":synthetic,
        "includes_controlled_event_schedule":controlled,
        "field_effect_inference_licensed":False,
        "field_validation_qualification":"Structural checks only. External camera truth, cap, effort and observer calibration still require independent verification.",
    }


def _read_csv_in(directory: Path, filename: str) -> tuple[list[str]|None,list[dict]]:
    path=(directory/filename)
    if not path.is_file():
        raise ValueError("independent visits CSV is absent")
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        return list(reader.fieldnames or []),list(reader)


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--manifest",type=Path,required=True)
    parser.add_argument("--visits-dir",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    try:
        data=json.loads(args.manifest.read_text(encoding="utf-8"))
        report=audit(data,lambda name:_read_csv_in(args.visits_dir,name))
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        report={
            "status":"STOP_SOURCE_ID_TIME_OR_REFERENCE_TRUTH",
            "error_type":type(exc).__name__,
            "error_detail":str(exc)[:300],
            "site_total_imputed":False,
            "natural_HR_validated":False,
            "future_reproduction_outcome_opened":False,
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("POLLIPI_EGWE_TRUTH_BRIDGE "+json.dumps({
        "status":report["status"],
        "total_imputed":report["site_total_imputed"],
        "natural_HR_validated":report["natural_HR_validated"],
        "reference_runs":report.get("independent_reference_run_count"),
        "error_type":report.get("error_type"),
    },sort_keys=True))


if __name__=="__main__":
    main()
