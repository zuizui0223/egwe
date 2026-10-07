from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Edmonton")
MIN_DAILY_INDIVIDUALS = 10
MIN_ELIGIBLE_DAYS_PER_YEAR = 30
PRIMARY_WINDOW_START = (9, 15)
PRIMARY_WINDOW_END = (11, 15)
MAX_NOON_OFFSET_HOURS = 6.5\nVISIBLE_FALSE = {"false", "f", "0", "no", "n"}


@dataclass(frozen=True)
class CoverageRow:
    year: int
    eligible_days: int
    days_in_window_with_any_data: int
    max_daily_individuals: int
    mean_daily_individuals_on_eligible_days: float | None
    eligible_year: bool


def _parse_timestamp(value: str) -> datetime:
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include an explicit timezone/UTC offset")
    return dt.astimezone(LOCAL_TZ)


def _in_primary_window(dt: datetime) -> bool:
    md = (dt.month, dt.day)
    return PRIMARY_WINDOW_START <= md <= PRIMARY_WINDOW_END


def _hours_from_local_noon(dt: datetime) -> float:
    noon = datetime.combine(dt.date(), time(12, 0), tzinfo=LOCAL_TZ)
    return abs((dt - noon).total_seconds()) / 3600.0


def coverage_from_rows(
    rows: list[dict[str, str]],
    *,
    timestamp_col: str = "timestamp",
    individual_col: str = "individual-local-identifier",
) -> dict[str, Any]:
    # day -> individual -> nearest-noon offset
    daily: dict[tuple[int, str], dict[str, float]] = defaultdict(dict)

    for row in rows:
        if timestamp_col not in row or individual_col not in row:
            raise KeyError(f"required columns missing: {timestamp_col}, {individual_col}")
        individual = str(row[individual_col]).strip()
        if not individual:
            continue

        visible = str(row.get("visible", "")).strip().casefold()
        if visible in VISIBLE_FALSE:
            continue

        sensor = str(row.get("sensor-type", row.get("sensor_type", ""))).strip().casefold()
        if sensor and sensor != "gps":
            continue

        dt = _parse_timestamp(str(row[timestamp_col]))
        if not _in_primary_window(dt):
            continue
        offset = _hours_from_local_noon(dt)
        if offset > MAX_NOON_OFFSET_HOURS:
            continue
        key = (dt.year, dt.date().isoformat())
        previous = daily[key].get(individual)
        if previous is None or offset < previous:
            daily[key][individual] = offset

    by_year: dict[int, list[int]] = defaultdict(list)
    for (year, _date), individuals in daily.items():
        by_year[year].append(len(individuals))

    years: list[CoverageRow] = []
    for year in sorted(by_year):
        counts = by_year[year]
        eligible_counts = [n for n in counts if n >= MIN_DAILY_INDIVIDUALS]
        years.append(
            CoverageRow(
                year=year,
                eligible_days=len(eligible_counts),
                days_in_window_with_any_data=len(counts),
                max_daily_individuals=max(counts),
                mean_daily_individuals_on_eligible_days=(
                    sum(eligible_counts) / len(eligible_counts) if eligible_counts else None
                ),
                eligible_year=len(eligible_counts) >= MIN_ELIGIBLE_DAYS_PER_YEAR,
            )
        )

    eligible_years = [r.year for r in years if r.eligible_year]
    return {
        "status": "movement_only_schema_and_coverage_gate_no_demographic_values_opened",
        "window": "Sep15-Nov15 America/Edmonton",
        "nearest_noon_max_offset_hours": MAX_NOON_OFFSET_HOURS,
        "minimum_daily_individuals": MIN_DAILY_INDIVIDUALS,
        "minimum_eligible_days_per_year": MIN_ELIGIBLE_DAYS_PER_YEAR,
        "years": [r.__dict__ for r in years],
        "eligible_years": eligible_years,
        "n_eligible_years": len(eligible_years),
        "primary_temporal_replication_gate_passed_on_movement_side": len(eligible_years) >= 11,
    }


def read_movebank_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_coverage(path: str | Path, output: str | Path) -> None:
    summary = coverage_from_rows(read_movebank_csv(path))
    dest = Path(output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
