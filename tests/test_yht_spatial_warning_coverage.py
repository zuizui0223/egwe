from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from eco_genetic_warning_extensions.yht_spatial_warning_coverage import coverage_from_rows


def _rows_for_year(year: int, n_days: int, n_animals: int) -> list[dict[str, str]]:
    start = datetime(year, 9, 15, 18, 0, tzinfo=timezone.utc)  # noon MDT
    rows: list[dict[str, str]] = []
    for day in range(n_days):
        for animal in range(n_animals):
            dt = start + timedelta(days=day, minutes=animal % 5)
            rows.append(
                {
                    "timestamp": dt.isoformat(),
                    "individual-local-identifier": f"E{animal:02d}",
                }
            )
    return rows


def test_frozen_coverage_gates() -> None:
    rows = []
    rows += _rows_for_year(2010, 30, 10)
    rows += _rows_for_year(2011, 29, 10)
    rows += _rows_for_year(2012, 35, 9)
    out = coverage_from_rows(rows)

    by_year = {r["year"]: r for r in out["years"]}
    assert by_year[2010]["eligible_year"] is True
    assert by_year[2010]["eligible_days"] == 30
    assert by_year[2011]["eligible_year"] is False
    assert by_year[2011]["eligible_days"] == 29
    assert by_year[2012]["eligible_year"] is False
    assert by_year[2012]["eligible_days"] == 0
    assert out["eligible_years"] == [2010]
    assert out["primary_temporal_replication_gate_passed_on_movement_side"] is False


def test_duplicate_fixes_do_not_inflate_daily_individual_count() -> None:
    rows = _rows_for_year(2010, 30, 10)
    rows.append(
        {
            "timestamp": "2010-09-15T18:30:00+00:00",
            "individual-local-identifier": "E00",
        }
    )
    out = coverage_from_rows(rows)
    row = out["years"][0]
    assert row["eligible_days"] == 30
    assert row["max_daily_individuals"] == 10


def test_timezone_naive_timestamp_fails_closed() -> None:
    rows = [{
        "timestamp": "2010-09-15T12:00:00",
        "individual-local-identifier": "E00",
    }]
    with pytest.raises(ValueError, match="explicit timezone"):
        coverage_from_rows(rows)


def test_source_managed_outliers_and_non_gps_rows_are_excluded() -> None:
    rows = _rows_for_year(2010, 30, 10)
    # Knock one animal out on every day via source-managed visibility.
    for row in rows:
        if row["individual-local-identifier"] == "E00":
            row["visible"] = "false"
    out = coverage_from_rows(rows)
    assert out["years"][0]["eligible_days"] == 0

    rows = _rows_for_year(2010, 30, 10)
    for row in rows:
        row["visible"] = "true"
        if row["individual-local-identifier"] == "E00":
            row["sensor-type"] = "acceleration"
        else:
            row["sensor-type"] = "GPS"
    out = coverage_from_rows(rows)
    assert out["years"][0]["eligible_days"] == 0
