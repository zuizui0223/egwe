from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, time, timezone
from pathlib import Path
from statistics import fmean, median, stdev
from typing import Any
from zoneinfo import ZoneInfo

SOURCE_REPOSITORY = "EliGurarie/BrazilMove2024"
SOURCE_COMMIT = "447d2882e8d14a67db429a6ef74c307dd2354866"
SOURCE_PATH = "data/Elk_GPS_data.csv"
SOURCE_BLOB_SHA = "2d5e8b124bc02b63a7b2f171004c7027b412cbe3"
STATUS = "exploratory_measurement_diagnostic_not_future_fate_validation"
TZ = ZoneInfo("America/Edmonton")
N_FIXED = 10
START = (9, 15)
END = (11, 15)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def utm11_nad83(lon: float, lat: float) -> tuple[float, float]:
    """GRS80 Transverse Mercator, NAD83 / UTM zone 11N (EPSG:26911).

    Implements the standard UTM series through order A^6 for the bounded
    Alberta coordinates used by this source. It is a diagnostic, not a
    replacement for the frozen full-archive pyproj workflow.
    """
    if not (math.isfinite(lon) and math.isfinite(lat) and -180 <= lon <= 180 and -90 <= lat <= 90):
        raise ValueError("invalid geographic coordinate")
    a = 6378137.0
    f = 1.0 / 298.257222101
    e2 = f * (2.0 - f)
    e4 = e2 * e2
    e6 = e4 * e2
    ep2 = e2 / (1 - e2)
    k0 = 0.9996
    phi = math.radians(lat)
    lam = math.radians(lon)
    central = math.radians(-117.0)
    sinp, cosp, tanp = math.sin(phi), math.cos(phi), math.tan(phi)
    n = a / math.sqrt(1 - e2 * sinp * sinp)
    t = tanp * tanp
    c = ep2 * cosp * cosp
    aa = (lam - central) * cosp
    m = a * (
        (1 - e2 / 4 - 3 * e4 / 64 - 5 * e6 / 256) * phi
        - (3 * e2 / 8 + 3 * e4 / 32 + 45 * e6 / 1024) * math.sin(2 * phi)
        + (15 * e4 / 256 + 45 * e6 / 1024) * math.sin(4 * phi)
        - 35 * e6 / 3072 * math.sin(6 * phi)
    )
    x = 500000 + k0 * n * (
        aa + (1 - t + c) * aa**3 / 6
        + (5 - 18 * t + t * t + 72 * c - 58 * ep2) * aa**5 / 120
    )
    y = k0 * (
        m + n * tanp * (
            aa * aa / 2
            + (5 - t + 9 * c + 4 * c * c) * aa**4 / 24
            + (61 - 58 * t + t * t + 600 * c - 330 * ep2) * aa**6 / 720
        )
    )
    return x, y


def cv(values: list[float]) -> float:
    if len(values) < 2:
        raise ValueError("sample CV requires at least two values")
    mean = fmean(values)
    if not math.isfinite(mean) or mean <= 0:
        raise ValueError("sample CV requires a positive finite mean")
    return stdev(values) / mean


def cv_ratio(points: tuple[tuple[float, float], ...]) -> float:
    """Match pinned shapeshiftr cvind/cvpop, sample-SD convention."""
    n = len(points)
    if n < 3:
        raise ValueError("need >=3 individuals")
    all_distances: list[float] = []
    per: list[list[float]] = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i):
            d = math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1])
            all_distances.append(d)
            per[i].append(d)
            per[j].append(d)
    return cv([fmean(x) for x in per]) / cv(all_distances)


def _eligible_points(path: str | Path) -> dict[str, dict[str, tuple[float, float]]]:
    daily: dict[str, dict[str, tuple[float, datetime, tuple[float, float]]]] = defaultdict(dict)
    with Path(path).open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"timestamp", "location.long", "location.lat", "sensor.type", "individual.local.identifier"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"unexpected mirror schema: {reader.fieldnames}")
        for row in reader:
            ts = datetime.strptime(row["timestamp"], "%m/%d/%Y %H:%M:%S")
            # Mirror-only interpretation supported by the researcher's teaching
            # code; NOT a relaxation of the official-source timestamp contract.
            ts = ts.replace(tzinfo=timezone.utc)
            local = ts.astimezone(TZ)
            date = local.date()
            if date.year != 2004 or not (START <= (date.month, date.day) <= END):
                continue
            if row["sensor.type"].strip().lower() != "gps":
                continue
            identity = row["individual.local.identifier"].strip()
            if not identity:
                continue
            noon = datetime.combine(date, time(12), tzinfo=TZ)
            offset = abs((local - noon).total_seconds()) / 3600
            if offset > 6.5:
                continue
            lon, lat = float(row["location.long"]), float(row["location.lat"])
            position = utm11_nad83(lon, lat)
            key = date.isoformat()
            old = daily[key].get(identity)
            if old is None or (offset, ts) < (old[0], old[1]):
                daily[key][identity] = (offset, ts, position)
    return {
        day: {identity: val[2] for identity, val in individuals.items()}
        for day, individuals in daily.items()
    }


def _linear_quantile(values: list[float], p: float) -> float:
    z = sorted(values)
    i = (len(z) - 1) * p
    lo, hi = math.floor(i), math.ceil(i)
    if lo == hi:
        return z[lo]
    return z[lo] * (hi - i) + z[hi] * (i - lo)


def summarise(path: str | Path) -> dict[str, Any]:
    raw = Path(path).read_bytes()
    digest = blob_sha(raw)
    if digest != SOURCE_BLOB_SHA:
        raise ValueError(f"mirror source blob changed: {digest}")

    daily = _eligible_points(path)
    cells: list[dict[str, Any]] = []
    for date, identities in sorted(daily.items()):
        n = len(identities)
        if n < N_FIXED:
            continue
        positions = tuple(v for _, v in sorted(identities.items()))
        ratios = [cv_ratio(combo) for combo in itertools.combinations(positions, N_FIXED)]
        if not all(math.isfinite(x) for x in ratios):
            raise RuntimeError("non-finite CV ratio")
        cells.append(
            {
                "date": date,
                "n_unique": n,
                "n_subsamples": len(ratios),
                "fixed_n_ratio_mean": fmean(ratios),
                "fixed_n_ratio_sd": stdev(ratios) if len(ratios) > 1 else 0.0,
                "fixed_n_ratio_min": min(ratios),
                "fixed_n_ratio_max": max(ratios),
            }
        )

    if len(cells) != 43:
        raise RuntimeError(f"expected 43 mirrored 2004 eligible days; got {len(cells)}")
    size_counts = Counter(x["n_unique"] for x in cells)
    if dict(size_counts) != {10: 17, 11: 14, 12: 12}:
        raise RuntimeError(f"unexpected daily sample-size composition: {dict(size_counts)}")
    means = [x["fixed_n_ratio_mean"] for x in cells]
    n_gt_10 = [x for x in cells if x["n_unique"] > N_FIXED]
    subset_sds = [x["fixed_n_ratio_sd"] for x in n_gt_10]
    ranges = [x["fixed_n_ratio_max"] - x["fixed_n_ratio_min"] for x in n_gt_10]
    adjacent = [abs(b - a) for a, b in zip(means, means[1:])]

    return {
        "analysis": "yht_mirror_fixed10_sampling_stability_v1",
        "status": STATUS,
        "source": {
            "repository": SOURCE_REPOSITORY,
            "commit": SOURCE_COMMIT,
            "path": SOURCE_PATH,
            "blob_sha": digest,
            "timestamp_interpretation": "UTC from separate author teaching documentation; mirror-only",
        },
        "methods": {
            "year": 2004,
            "season": "Sep15-Nov15 America/Edmonton",
            "nearest_noon_window_hours": 6.5,
            "source_crs": "WGS84 GPS",
            "diagnostic_projection": "GRS80 UTM11N EPSG:26911 forward series",
            "metric": "Love-Otto CV_ind/CV_pop from Euclidean pairwise projected distances",
            "sampling": "exhaustive 10-of-n subsets of each eligible day's observed collared individuals",
            "note": "Not the protocol's 100 deterministic SHA256 subsamples; an exhaustive measurement-stability sensitivity only.",
        },
        "eligible_days": len(cells),
        "days_with_sample_choice": len(n_gt_10),
        "daily_n_counts": {str(k): v for k, v in sorted(size_counts.items())},
        "total_fixed_n_subsets": sum(x["n_subsamples"] for x in cells),
        "daily_cv_ratio_mean_summary": {
            "annual_mean": fmean(means),
            "median": median(means),
            "between_day_sd": stdev(means),
            "min": min(means),
            "max": max(means),
        },
        "daily_subsample_spread_for_n_gt_10": {
            "median_within_day_sd": median(subset_sds),
            "q25_within_day_sd": _linear_quantile(subset_sds, 0.25),
            "q75_within_day_sd": _linear_quantile(subset_sds, 0.75),
            "max_within_day_sd": max(subset_sds),
            "median_within_day_range": median(ranges),
            "max_within_day_range": max(ranges),
        },
        "absolute_change_between_adjacent_eligible_daily_means": {
            "median": median(adjacent),
            "q75": _linear_quantile(adjacent, 0.75),
            "max": max(adjacent),
        },
        "conclusion": (
            "In this one-year teaching subset, selecting which ten GPS-collared "
            "females to use can cause substantial within-day CV-ratio variation. "
            "This is not evidence about future demographic prediction, nor a "
            "measurement-error estimate for the unobserved whole herd."
        ),
    }


def write(input_path: str | Path, output_path: str | Path) -> None:
    summary = summarise(input_path)
    dest = Path(output_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
