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
UTC = ZoneInfo("UTC")
MIN_DAILY_INDIVIDUALS = 10
MIN_ELIGIBLE_DAYS_PER_YEAR = 30
PRIMARY_WINDOW_START = (9, 15)
PRIMARY_WINDOW_END = (11, 15)
MAX_NOON_OFFSET_HOURS = 6.5
TIMESTAMP_SEMANTICS = {"explicit_timezone", "movebank_utc"}
TIMESTAMP_ALIASES = ("timestamp",)
INDIVIDUAL_ALIASES = (
    "individual_local_identifier",
    "individual.local.identifier",
    "individual-local-identifier",
)


@dataclass(frozen=True)
class CoverageRow:
    year: int
    eligible_days: int
    days_in_window_with_any_data: int
    max_daily_individuals: int
    mean_daily_individuals_on_eligible_days: float | None
    eligible_year: bool


def _parse_timestamp(value: str, *, timestamp_semantics: str = "explicit_timezone") -> datetime:
    if timestamp_semantics not in TIMESTAMP_SEMANTICS:
        raise ValueError(f"unknown timestamp semantics: {timestamp_semantics!r}")

    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"

    dt: datetime | None = None
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        # Public Ya Ha Tinda teaching mirrors preserve an older Movebank-style
        # m/d/Y clock representation whose source workflow documents UTC.
        for fmt in ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M"):
            try:
                dt = datetime.strptime(raw, fmt)
                break
            except ValueError:
                pass
    if dt is None:
        raise ValueError(f"unsupported timestamp format: {value!r}")

    if dt.tzinfo is None:
        if timestamp_semantics == "movebank_utc":
            dt = dt.replace(tzinfo=UTC)
        else:
            raise ValueError("timestamp must include an explicit timezone/UTC offset")

    return dt.astimezone(LOCAL_TZ)


def _in_primary_window(dt: datetime) -> bool:
    md = (dt.month, dt.day)
    return PRIMARY_WINDOW_START <= md <= PRIMARY_WINDOW_END


def _hours_from_local_noon(dt: datetime) -> float:
    noon = datetime.combine(dt.date(), time(12, 0), tzinfo=LOCAL_TZ)
    return abs((dt - noon).total_seconds()) / 3600.0


def _resolve_column(
    rows: list[dict[str, str]],
    explicit: str | None,
    aliases: tuple[str, ...],
) -> str:
    if not rows:
        raise ValueError("movement table is empty")
    keys = set(rows[0])
    if explicit is not None:
        if explicit not in keys:
            raise KeyError(f"required column missing: {explicit}")
        return explicit
    matches = [name for name in aliases if name in keys]
    if len(matches) != 1:
        raise KeyError(f"expected exactly one column among {aliases}, found {matches}")
    return matches[0]


def coverage_from_rows(
    rows: list[dict[str, str]],
    *,
    timestamp_col: str | None = None,
    individual_col: str | None = None,
    timestamp_semantics: str = "explicit_timezone",
) -> dict[str, Any]:
    timestamp_col = _resolve_column(rows, timestamp_col, TIMESTAMP_ALIASES)
    individual_col = _resolve_column(rows, individual_col, INDIVIDUAL_ALIASES)

    # day -> individual -> nearest-noon offset
    daily: dict[tuple[int, str], dict[str, float]] = defaultdict(dict)

    for row in rows:
        individual = str(row[individual_col]).strip()
        if not individual:
            continue
        dt = _parse_timestamp(
            str(row[timestamp_col]),
            timestamp_semantics=timestamp_semantics,
        )
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
        "timestamp_semantics": timestamp_semantics,
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


def write_coverage(
    path: str | Path,
    output: str | Path,
    *,
    timestamp_semantics: str = "explicit_timezone",
) -> None:
    summary = coverage_from_rows(
        read_movebank_csv(path),
        timestamp_semantics=timestamp_semantics,
    )
    dest = Path(output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
