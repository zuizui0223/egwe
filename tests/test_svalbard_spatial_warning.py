from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

from eco_genetic_warning_extensions.svalbard_spatial_warning import (
    abundance_from_rows,
    annual_spatial_summaries,
    build_transitions,
    rolling_forecast,
)


def _gps_rows(year: int, days: int = 30, n: int = 10):
    start = datetime(year, 9, 15, 12, tzinfo=timezone.utc)
    rows = []
    for d in range(days):
        for i in range(n):
            dt = start + timedelta(days=d, minutes=i)
            rows.append({
                "id": f"R{i:02d}",
                "datetime": dt.isoformat(),
                "x": str(i * 1000.0 + d),
                "y": str((i % 3) * 1500.0 + d),
            })
    return rows


def test_annual_spatial_gate_and_metrics() -> None:
    rows = _gps_rows(2010, 30, 10) + _gps_rows(2011, 29, 10)
    out = annual_spatial_summaries(rows)
    assert sorted(out) == [2010]
    assert out[2010]["eligible_days"] == 30
    assert out[2010]["cvratio"] > 0
    assert out[2010]["spatial_scale"] > 0


def test_abundance_requires_one_unique_value_per_year() -> None:
    rows = [
        {"Date": "08/01/2010", "N.tot": 100},
        {"Date": "08/02/2010", "N.tot": 100},
        {"Date": "08/01/2011", "N.tot": 110},
    ]
    assert abundance_from_rows(rows) == {2010: 100.0, 2011: 110.0}


def test_build_transitions_only_adjacent_years() -> None:
    spatial = {
        2010: {"spatial_scale": 5.0, "cvratio": 0.5},
        2012: {"spatial_scale": 6.0, "cvratio": 0.6},
    }
    abundance = {2010: 100.0, 2011: 110.0, 2012: 120.0, 2013: 90.0}
    out = build_transitions(spatial, abundance)
    assert [r["year"] for r in out] == [2010, 2012]
    assert math.isclose(out[0]["g_next"], math.log(1.1))


def test_rolling_forecast_fail_closed_under_11_transitions() -> None:
    rows = []
    for year in range(2009, 2019):
        rows.append({
            "year": year,
            "log_n_current": math.log(100 + year - 2009),
            "log_spatial_scale": math.log(10 + 0.1 * (year - 2009)),
            "cvratio": 0.4 + 0.01 * (year - 2009),
            "g_next": 0.02,
        })
    out = rolling_forecast(rows)
    assert out["status"] == "insufficient_temporal_replication"


def test_rolling_forecast_runs_on_locked_minimum() -> None:
    rows = []
    for j, year in enumerate(range(2009, 2020)):
        rows.append({
            "year": year,
            "log_n_current": math.log(100 + 2*j),
            "log_spatial_scale": math.log(10 + 0.2*j + (0.05 if j % 2 else 0)),
            "cvratio": 0.4 + 0.015*j + (0.01 if j % 3 == 0 else -0.005),
            "g_next": 0.01 + 0.002*j + (0.003 if j % 2 else -0.002),
        })
    out = rolling_forecast(rows)
    assert out["status"] == "completed_primary_temporal_validation"
    assert out["n_transitions"] == 11
    assert out["n_forecasts"] == 4
    assert out["decision"] in {
        "detected_incremental_future_information",
        "no_detected_incremental_future_information",
    }
