from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime, time, timezone
from pathlib import Path
from statistics import fmean, median, stdev
from typing import Any
from zoneinfo import ZoneInfo

from eco_genetic_warning_extensions.yht_mirror_sampling_audit import (
    cv_ratio, utm11_nad83, _linear_quantile
)
from eco_genetic_warning_extensions.yht_spatial_warning_coverage import LOCAL_TZ

DOI = "10.5441/001/1.5g4h5t6c"
EVENT_SHA256 = "1069cd7531d1d7a519cb817b09d015be91c552ecafab504869a81eb01eff4201"
EXPECTED_YEARS = (2004, 2013, 2014, 2015, 2016, 2017, 2018, 2019)
EXPECTED_DAYS = {2004:40, **{year:62 for year in range(2013, 2020)}}
STATUS = "outcome_free_exploratory_not_a_future_demography_test"
REQUIRED = {"timestamp", "location-long", "location-lat", "individual-local-identifier"}
VISIBLE_FALSE = {"false", "f", "0", "no", "n"}
N_FIXED = 10
N_REPLICATES = 100


def source_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_official_timestamp(raw: str) -> datetime:
    # The source-specific UTC interpretation was locked in the official
    # acquisition amendment before the full archive was read.
    value = raw.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(LOCAL_TZ)


def _hour_offset(dt: datetime) -> float:
    noon = datetime.combine(dt.date(), time(12), tzinfo=LOCAL_TZ)
    return abs((dt - noon).total_seconds()) / 3600


def eligible_daily_positions(path: str | Path) -> tuple[dict[str, dict[str, tuple[float,float]]], dict[str,float]]:
    # Separate GPS coordinates are used only within the disposable runner.
    # A finite summary with no individual identifiers/coordinates is returned.
    daily: dict[str, dict[str, tuple[float, datetime, tuple[float, float]]]] = defaultdict(dict)
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not REQUIRED.issubset(set(reader.fieldnames or [])):
            raise RuntimeError(f"source schema does not contain {sorted(REQUIRED)}")
        for row in reader:
            ident = (row.get("individual-local-identifier") or "").strip()
            if not ident:
                continue
            visible = (row.get("visible") or "").strip().casefold()
            if visible in VISIBLE_FALSE:
                continue
            sensor = (row.get("sensor-type") or row.get("sensor_type") or "").strip().casefold()
            if sensor and sensor != "gps":
                continue
            dt = _parse_official_timestamp(row["timestamp"])
            if not ((9,15) <= (dt.month,dt.day) <= (11,15)):
                continue
            offset = _hour_offset(dt)
            if offset > 6.5:
                continue
            lon = float(row["location-long"])
            lat = float(row["location-lat"])
            pos = utm11_nad83(lon, lat)
            when = dt.astimezone(timezone.utc)
            key = dt.date().isoformat()
            previous = daily[key].get(ident)
            if previous is None or (offset, when) < (previous[0], previous[1]):
                daily[key][ident] = (offset, when, pos)
    positions = {}
    time_spans = {}
    for day, observed in daily.items():
        if len(observed) < N_FIXED:
            continue
        positions[day] = {ident: row[2] for ident,row in observed.items()}
        times = [row[1] for row in observed.values()]
        time_spans[day] = (max(times) - min(times)).total_seconds() / 3600
    return positions, time_spans


def _fixed_ids(day: str, individuals: tuple[str, ...], replicate: int) -> tuple[str, ...]:
    ranked = sorted(individuals, key=lambda ident: (
        hashlib.sha256(f"{day}|{replicate}|{ident}".encode("utf-8")).hexdigest(),
        ident,
    ))
    return tuple(ranked[:N_FIXED])


def _sign(x: float) -> int:
    return int(x > 0) - int(x < 0)


def _day_summary(day: str, observed: dict[str, tuple[float, float]]) -> dict[str, Any]:
    ids = tuple(sorted(observed))
    n = len(ids)
    if n < N_FIXED:
        raise ValueError("daily gate failed before CV calculation")
    all_ratio = cv_ratio(tuple(observed[i] for i in ids))
    if n == N_FIXED:
        samples = [all_ratio]
    else:
        samples = [
            cv_ratio(tuple(observed[i] for i in _fixed_ids(day, ids, replicate)))
            for replicate in range(N_REPLICATES)
        ]
    if not all(math.isfinite(v) for v in [all_ratio, *samples]):
        raise RuntimeError("invalid Love-Otto CV ratio")
    return {
        "day": day,
        "year": int(day[:4]),
        "n": n,
        "all": float(all_ratio),
        "fixed_mean": float(fmean(samples)),
        "fixed_subset_sd": float(stdev(samples)) if len(samples)>1 else 0.0,
        "fixed_p90_minus_p10": _linear_quantile(samples,0.9)-_linear_quantile(samples,0.1),
    }


def _adjacent_changes(rows: list[dict[str, Any]]) -> tuple[list[float],list[float],float | None]:
    if len(rows)<2:
        return [],[],None
    a=[]; b=[]; discord=0
    for previous,current in zip(rows,rows[1:]):
        da = current["fixed_mean"]-previous["fixed_mean"]
        db = current["all"]-previous["all"]
        a.append(abs(da))
        b.append(abs(db))
        discord += int(_sign(da)!=_sign(db))
    return a,b,discord/len(a)


def summarise(
    daily: dict[str,dict[str,tuple[float,float]]],
    *, expected_years: tuple[int,...] = EXPECTED_YEARS,
    expected_days: dict[int,int] | None = EXPECTED_DAYS,
    time_spans: dict[str,float] | None = None
) -> dict[str,Any]:
    by_year: dict[int,list[dict[str,Any]]] = defaultdict(list)
    for day, observed in sorted(daily.items()):
        by_year[int(day[:4])].append(_day_summary(day,observed))
    if tuple(sorted(by_year)) != expected_years:
        raise RuntimeError(f"source coverage changed: {tuple(sorted(by_year))}; expected {expected_years}")
    if expected_days is not None:
        for year,count in expected_days.items():
            if len(by_year[year])!=count:
                raise RuntimeError(f"source day-count mismatch for {year}: {len(by_year[year])} vs {count}")

    results: list[dict[str,Any]]=[]
    all_spreads=[]; all_changes=[]; total_discord=0; total_comparisons=0
    annual_fixed=[]; annual_all=[]; days_with_choice=0; all_spans=[]
    for year in expected_years:
        rows=by_year[year]
        n_vals=[r["n"] for r in rows]
        fixed=[r["fixed_mean"] for r in rows]
        full=[r["all"] for r in rows]
        choice=[r for r in rows if r["n"]>N_FIXED]
        spans=[time_spans[r["day"]] for r in rows] if time_spans is not None else []
        if spans and (any(x<0 or x>13.00001 for x in spans) or not all(math.isfinite(x) for x in spans)):
            raise RuntimeError("unexpected within-day timestamp span")
        all_spans.extend(spans)
        adjacent_fixed,adjacent_full,discord=_adjacent_changes(rows)
        total_discord+=round(discord*len(adjacent_fixed)) if discord is not None else 0
        total_comparisons+=len(adjacent_fixed)
        all_changes.extend(adjacent_fixed)
        all_spreads.extend(r["fixed_subset_sd"] for r in choice)
        days_with_choice+=len(choice)
        annual_fixed.append(fmean(fixed))
        annual_all.append(fmean(full))
        results.append({
            "year":year,
            "eligible_days":len(rows),
            "mean_collared_n":fmean(n_vals),
            "min_collared_n":min(n_vals),
            "max_collared_n":max(n_vals),
            "days_with_sample_choice":len(choice),
            "median_snapshot_time_span_hours":median(spans) if spans else None,
            "p90_snapshot_time_span_hours":_linear_quantile(spans,0.9) if spans else None,
            "max_snapshot_time_span_hours":max(spans) if spans else None,
            "annual_mean_fixed10_ratio":fmean(fixed),
            "annual_mean_all_collared_ratio":fmean(full),
            "median_daily_conditional_subset_sd_for_n_gt10":median([r["fixed_subset_sd"] for r in choice]) if choice else None,
            "median_daily_conditional_p90_minus_p10_for_n_gt10":median([r["fixed_p90_minus_p10"] for r in choice]) if choice else None,
            "median_absolute_daily_mean_minus_all_collared":median([abs(r["fixed_mean"]-r["all"]) for r in rows]),
            "median_adjacent_eligible_day_change_fixed10":median(adjacent_fixed) if adjacent_fixed else None,
            "median_adjacent_eligible_day_change_all_collared":median(adjacent_full) if adjacent_full else None,
            "fraction_adjacent_eligible_day_direction_disagreements":discord,
        })
    mean_fixed=fmean(annual_fixed); mean_all=fmean(annual_all)
    cov=sum((a-mean_fixed)*(b-mean_all) for a,b in zip(annual_fixed,annual_all))
    vx=sum((a-mean_fixed)**2 for a in annual_fixed)
    vy=sum((b-mean_all)**2 for b in annual_all)
    corr=(cov/math.sqrt(vx*vy)) if vx>0 and vy>0 else None

    return {
        "analysis_id":"yht_official_love_otto_panel_sensitivity_v1",
        "status":STATUS,
        "source":{"doi":DOI,"event_file_sha256":EVENT_SHA256},
        "methods":{
            "fixed_n":N_FIXED,"daily_subsample_replicates":N_REPLICATES,
            "season":"Sep15-Nov15 America/Edmonton","reference":"all GPS-collared individuals; not entire herd",
            "metric":"Love-Otto CV_ind/CV_pop; log10=FALSE",
        },
        "years":results,
        "overall":{
            "number_of_eligible_years":len(results),
            "number_of_eligible_days":sum(len(rows) for rows in by_year.values()),
            "days_with_subsample_choice":days_with_choice,
            "median_snapshot_time_span_hours":median(all_spans) if all_spans else None,
            "p90_snapshot_time_span_hours":_linear_quantile(all_spans,0.9) if all_spans else None,
            "median_of_daily_subset_sd_for_n_gt10":median(all_spreads) if all_spreads else None,
            "median_adjacent_eligible_day_change_fixed10":median(all_changes) if all_changes else None,
            "fraction_direction_disagreements":(total_discord/total_comparisons) if total_comparisons else None,
            "annual_fixed10_vs_all_collared_descriptive_correlation":corr,
        },
        "claim_boundary":"Outcome-free conditional sample sensitivity among observed collars only; no recruitment, survival, demographic warning, whole-herd sampling error or predictive validity inferred.",
    }


def write(source_csv: str | Path, output: str | Path) -> None:
    digest=source_sha256(source_csv)
    if digest!=EVENT_SHA256:
        raise RuntimeError(f"official event file changed: {digest}")
    daily, time_spans = eligible_daily_positions(source_csv)
    result=summarise(daily,time_spans=time_spans)
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
