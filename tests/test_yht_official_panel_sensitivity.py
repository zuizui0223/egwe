from __future__ import annotations

import math
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from eco_genetic_warning_extensions.yht_official_panel_sensitivity import (
    _fixed_ids, _parse_official_timestamp, summarise
)


def _daily(year: int, n: int, n_days: int) -> dict[str, dict[str, tuple[float,float]]]:
    out = {}
    for day in range(n_days):
        date = datetime(year,9,15,tzinfo=ZoneInfo("America/Edmonton")).date()
        from datetime import timedelta
        label=(date+timedelta(days=day)).isoformat()
        points = {}
        for i in range(n):
            # An asymmetric configuration with nonzero CV for both statistics.
            points[f"elk{i:02d}"] = (
                i * 123.0 + (i%3)*31.0 + day*5,
                (i*i%17)*97.0 + (i%4)*14.0 + day*9,
            )
        out[label] = points
    return out


def test_official_utc_normalisation_is_explicitly_source_specific() -> None:
    naive = _parse_official_timestamp("2004-09-15T18:00:00")
    aware = _parse_official_timestamp("2004-09-15T18:00:00+00:00")
    assert naive == aware
    assert naive.hour == 12


def test_fixed_panel_choice_is_deterministic_and_order_independent() -> None:
    ids=tuple(f"E{i:02d}" for i in range(22))
    a=_fixed_ids("2017-10-01",ids,31)
    b=_fixed_ids("2017-10-01",tuple(reversed(ids)),31)
    assert a==b
    assert len(a)==10
    assert len(set(a))==10


def test_synthetic_30_day_10_vs_12_collar_audit() -> None:
    daily = _daily(2004,10,30)
    daily.update(_daily(2013,12,30))
    out = summarise(daily, expected_years=(2004,2013), expected_days={2004:30,2013:30})
    assert out["status"] == "outcome_free_exploratory_not_a_future_demography_test"
    assert out["overall"]["number_of_eligible_days"] == 60
    assert out["overall"]["days_with_subsample_choice"] == 30
    a,b = out["years"]
    assert a["days_with_sample_choice"] == 0
    assert math.isclose(a["annual_mean_fixed10_ratio"],a["annual_mean_all_collared_ratio"],abs_tol=1e-15)
    assert b["days_with_sample_choice"] == 30
    assert b["median_daily_conditional_subset_sd_for_n_gt10"] > 0
    assert 0 <= out["overall"]["fraction_direction_disagreements"] <= 1
    assert "coordinate" not in str(out)


def test_changed_annual_gate_fails_closed() -> None:
    daily = _daily(2004,10,30)
    with pytest.raises(RuntimeError,match="day-count mismatch"):
        summarise(daily, expected_years=(2004,), expected_days={2004:40})
    with pytest.raises(RuntimeError,match="source coverage changed"):
        summarise(daily, expected_years=(2004,2013), expected_days={2004:30})
