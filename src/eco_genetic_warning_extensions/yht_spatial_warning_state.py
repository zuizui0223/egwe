from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime, time
from pathlib import Path
from statistics import fmean
from typing import Any

from .love_otto_spatial_metrics import cvind, cvpop, cvratio
from .yht_spatial_warning_coverage import (
    LOCAL_TZ,
    MAX_NOON_OFFSET_HOURS,
    MIN_DAILY_INDIVIDUALS,
    MIN_ELIGIBLE_DAYS_PER_YEAR,
    PRIMARY_WINDOW_END,
    PRIMARY_WINDOW_START,
    _parse_timestamp,
)

LONGITUDE_ALIASES = ("location_long", "location.long", "location-long")
LATITUDE_ALIASES = ("location_lat", "location.lat", "location-lat")
INDIVIDUAL_ALIASES = (
    "individual_local_identifier",
    "individual.local.identifier",
    "individual-local-identifier",
)
TIMESTAMP_ALIASES = ("timestamp",)

FIXED_N = 10
N_SUBSAMPLES = 100

# EPSG:26911 NAD83 / UTM zone 11N. NAD83 uses the GRS80 ellipsoid.
_GRS80_A = 6_378_137.0
_GRS80_INV_F = 298.257222101
_UTM_K0 = 0.9996
_UTM_FALSE_EASTING = 500_000.0
_UTM_LON0_RAD = math.radians(-117.0)


def _resolve_column(fieldnames: list[str], aliases: tuple[str, ...]) -> str:
    matches = [name for name in aliases if name in fieldnames]
    if len(matches) != 1:
        raise KeyError(f"expected exactly one column among {aliases}, found {matches}")
    return matches[0]


def project_epsg26911(lon_deg: float, lat_deg: float) -> tuple[float, float]:
    """Project WGS84-like lon/lat to NAD83 / UTM zone 11N using GRS80.

    For this study region WGS84-to-NAD83 frame differences are negligible
    relative to animal-location uncertainty; the projection equations and
    ellipsoid are pinned to EPSG:26911.
    """
    lon = math.radians(float(lon_deg))
    lat = math.radians(float(lat_deg))

    f = 1.0 / _GRS80_INV_F
    e2 = f * (2.0 - f)
    ep2 = e2 / (1.0 - e2)

    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    tan_lat = math.tan(lat)

    n = _GRS80_A / math.sqrt(1.0 - e2 * sin_lat * sin_lat)
    t = tan_lat * tan_lat
    c = ep2 * cos_lat * cos_lat
    a = cos_lat * (lon - _UTM_LON0_RAD)

    e4 = e2 * e2
    e6 = e4 * e2
    m = _GRS80_A * (
        (1 - e2 / 4 - 3 * e4 / 64 - 5 * e6 / 256) * lat
        - (3 * e2 / 8 + 3 * e4 / 32 + 45 * e6 / 1024) * math.sin(2 * lat)
        + (15 * e4 / 256 + 45 * e6 / 1024) * math.sin(4 * lat)
        - (35 * e6 / 3072) * math.sin(6 * lat)
    )

    easting = _UTM_FALSE_EASTING + _UTM_K0 * n * (
        a
        + (1 - t + c) * a**3 / 6
        + (5 - 18 * t + t**2 + 72 * c - 58 * ep2) * a**5 / 120
    )
    northing = _UTM_K0 * (
        m
        + n
        * tan_lat
        * (
            a**2 / 2
            + (5 - t + 9 * c + 4 * c**2) * a**4 / 24
            + (61 - 58 * t + t**2 + 600 * c - 330 * ep2) * a**6 / 720
        )
    )
    return float(easting), float(northing)


def _pairwise_mean(points: list[tuple[float, float]]) -> float:
    values = []
    for i in range(len(points)):
        xi, yi = points[i]
        for j in range(i):
            xj, yj = points[j]
            values.append(math.hypot(xi - xj, yi - yj))
    if not values:
        raise ValueError("pairwise mean requires at least two points")
    return float(fmean(values))


def _fixed_n_ids(date_iso: str, ids: list[str], replicate: int) -> list[str]:
    if len(ids) < FIXED_N:
        raise ValueError("fixed-n sampling requires at least 10 individuals")
    if len(ids) == FIXED_N:
        return sorted(ids)
    ranked = sorted(
        ids,
        key=lambda individual: (
            hashlib.sha256(
                f"{date_iso}|{replicate}|{individual}".encode("utf-8")
            ).hexdigest(),
            individual,
        ),
    )
    return ranked[:FIXED_N]


def _date_in_primary_window(dt: datetime) -> bool:
    md = (dt.month, dt.day)
    return PRIMARY_WINDOW_START <= md <= PRIMARY_WINDOW_END


def _noon_offset_hours(dt: datetime) -> float:
    noon = datetime.combine(dt.date(), time(12, 0), tzinfo=LOCAL_TZ)
    return abs((dt - noon).total_seconds()) / 3600.0


def _select_daily_snapshots(
    rows: list[dict[str, str]],
    *,
    timestamp_semantics: str,
) -> dict[str, dict[str, tuple[float, float]]]:
    if not rows:
        raise ValueError("movement table is empty")
    fieldnames = list(rows[0])
    timestamp_col = _resolve_column(fieldnames, TIMESTAMP_ALIASES)
    individual_col = _resolve_column(fieldnames, INDIVIDUAL_ALIASES)
    lon_col = _resolve_column(fieldnames, LONGITUDE_ALIASES)
    lat_col = _resolve_column(fieldnames, LATITUDE_ALIASES)

    # local-date -> individual -> (offset, timestamp, lon, lat)
    chosen: dict[str, dict[str, tuple[float, datetime, float, float]]] = defaultdict(dict)

    for row in rows:
        individual = str(row.get(individual_col, "")).strip()
        if not individual:
            continue
        dt = _parse_timestamp(
            str(row.get(timestamp_col, "")),
            timestamp_semantics=timestamp_semantics,
        )
        if not _date_in_primary_window(dt):
            continue
        offset = _noon_offset_hours(dt)
        if offset > MAX_NOON_OFFSET_HOURS:
            continue
        try:
            lon = float(row[lon_col])
            lat = float(row[lat_col])
        except (TypeError, ValueError):
            continue
        if not (math.isfinite(lon) and math.isfinite(lat)):
            continue

        date_iso = dt.date().isoformat()
        previous = chosen[date_iso].get(individual)
        candidate = (offset, dt, lon, lat)
        if previous is None or offset < previous[0] or (
            offset == previous[0] and dt < previous[1]
        ):
            chosen[date_iso][individual] = candidate

    return {
        date_iso: {
            individual: (record[2], record[3])
            for individual, record in individuals.items()
        }
        for date_iso, individuals in chosen.items()
    }


def summarise_spatial_state(
    rows: list[dict[str, str]],
    *,
    timestamp_semantics: str = "explicit_timezone",
) -> dict[str, Any]:
    daily = _select_daily_snapshots(rows, timestamp_semantics=timestamp_semantics)

    day_rows: list[dict[str, Any]] = []
    for date_iso in sorted(daily):
        individuals = daily[date_iso]
        n = len(individuals)
        if n < MIN_DAILY_INDIVIDUALS:
            continue

        ids = sorted(individuals)
        replicates = range(N_SUBSAMPLES) if n > FIXED_N else range(1)
        submetrics: list[dict[str, float]] = []
        for replicate in replicates:
            sample_ids = _fixed_n_ids(date_iso, ids, replicate)
            points = [
                project_epsg26911(*individuals[individual])
                for individual in sample_ids
            ]
            submetrics.append(
                {
                    "cvpop": cvpop(points),
                    "cvind": cvind(points),
                    "cvratio": cvratio(points),
                    "mean_pairwise_distance_m": _pairwise_mean(points),
                }
            )

        day_rows.append(
            {
                "date": date_iso,
                "year": int(date_iso[:4]),
                "n_available": n,
                "n_used": FIXED_N,
                "n_subsamples": len(submetrics),
                "cvpop": float(fmean(x["cvpop"] for x in submetrics)),
                "cvind": float(fmean(x["cvind"] for x in submetrics)),
                "cvratio": float(fmean(x["cvratio"] for x in submetrics)),
                "mean_pairwise_distance_m": float(
                    fmean(x["mean_pairwise_distance_m"] for x in submetrics)
                ),
            }
        )

    by_year: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in day_rows:
        by_year[int(row["year"])].append(row)

    annual = []
    for year in sorted(by_year):
        days = by_year[year]
        eligible = len(days) >= MIN_ELIGIBLE_DAYS_PER_YEAR
        annual.append(
            {
                "year": year,
                "eligible_days": len(days),
                "eligible_year": eligible,
                "mean_available_individuals": float(
                    fmean(float(x["n_available"]) for x in days)
                ),
                "cvpop": (
                    float(fmean(float(x["cvpop"]) for x in days))
                    if eligible
                    else None
                ),
                "cvind": (
                    float(fmean(float(x["cvind"]) for x in days))
                    if eligible
                    else None
                ),
                "cvratio": (
                    float(fmean(float(x["cvratio"]) for x in days))
                    if eligible
                    else None
                ),
                "mean_pairwise_distance_m": (
                    float(
                        fmean(float(x["mean_pairwise_distance_m"]) for x in days)
                    )
                    if eligible
                    else None
                ),
            }
        )

    eligible_years = [row["year"] for row in annual if row["eligible_year"]]
    return {
        "status": "movement_only_spatial_state_no_demographic_values_opened",
        "timestamp_semantics": timestamp_semantics,
        "projection": "EPSG:26911 NAD83 / UTM zone 11N (GRS80)",
        "fixed_n": FIXED_N,
        "subsamples_per_day_when_n_gt_10": N_SUBSAMPLES,
        "annual_aggregation": "arithmetic mean of eligible daily fixed-n metrics",
        "n_daily_states": len(day_rows),
        "eligible_years": eligible_years,
        "n_eligible_years": len(eligible_years),
        "primary_temporal_replication_gate_passed_on_movement_side": (
            len(eligible_years) >= 11
        ),
        "annual": annual,
        "daily": day_rows,
    }


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_summary(
    path: str | Path,
    output: str | Path,
    *,
    timestamp_semantics: str = "explicit_timezone",
) -> None:
    result = summarise_spatial_state(
        read_csv(path),
        timestamp_semantics=timestamp_semantics,
    )
    dest = Path(output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
