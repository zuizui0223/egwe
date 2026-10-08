from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

from eco_genetic_warning_extensions.yht_spatial_warning_state import (
    project_epsg26911,
    summarise_spatial_state,
)


def test_epsg26911_reference_points() -> None:
    # Reference values from PROJ/pyproj EPSG:4326 -> EPSG:26911.
    refs = [
        ((-115.5, 51.7), (603660.0154708641, 5728737.190026558)),
        ((-116.0, 51.5), (569411.9510900886, 5705903.240104717)),
        ((-114.8, 52.0), (651022.2477736843, 5763323.481345853)),
    ]
    for lonlat, expected in refs:
        got = project_epsg26911(*lonlat)
        assert math.isclose(got[0], expected[0], abs_tol=0.2)
        assert math.isclose(got[1], expected[1], abs_tol=0.2)


def _synthetic_rows(year: int, days: int, animals: int) -> list[dict[str, str]]:
    start = datetime(year, 9, 15, 18, 0, tzinfo=timezone.utc)
    rows = []
    for d in range(days):
        for i in range(animals):
            dt = start + timedelta(days=d, minutes=i)
            rows.append(
                {
                    "timestamp": dt.isoformat(),
                    "location_long": str(-115.5 + 0.01 * i),
                    "location_lat": str(51.7 + 0.004 * (i % 4)),
                    "individual_local_identifier": f"E{i:02d}",
                }
            )
    return rows


def test_annual_state_requires_thirty_days_and_is_deterministic() -> None:
    rows = _synthetic_rows(2018, 30, 12)
    a = summarise_spatial_state(rows)
    b = summarise_spatial_state(rows)
    assert a == b
    assert a["eligible_years"] == [2018]
    annual = a["annual"][0]
    assert annual["eligible_days"] == 30
    assert annual["eligible_year"] is True
    assert annual["cvratio"] is not None
    assert annual["mean_pairwise_distance_m"] > 0
    assert all(x["n_used"] == 10 for x in a["daily"])
    assert all(x["n_subsamples"] == 100 for x in a["daily"])


def test_dot_aliases_and_movebank_utc_semantics() -> None:
    rows = []
    for day in range(30):
        for i in range(10):
            rows.append(
                {
                    "timestamp": f"9/{15 + day}/2018 18:00:00" if 15 + day <= 30 else (
                        f"10/{15 + day - 30}/2018 18:00:00"
                    ),
                    "location.long": str(-115.5 + 0.01 * i),
                    "location.lat": str(51.7 + 0.003 * i),
                    "individual.local.identifier": f"E{i:02d}",
                }
            )
    out = summarise_spatial_state(rows, timestamp_semantics="movebank_utc")
    assert out["eligible_years"] == [2018]
