from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime, time, timezone
from pathlib import Path
from statistics import fmean
from typing import Any, Iterable, Sequence

from eco_genetic_warning_extensions.love_otto_spatial_metrics import cvind, cvpop, cvratio

WINDOW_START = (9, 15)
WINDOW_END = (11, 15)
TARGET_HOUR_UTC = 12
MAX_OFFSET_HOURS = 6.0
MIN_DAILY_INDIVIDUALS = 10
MIN_ELIGIBLE_DAYS_PER_YEAR = 30
FIXED_N = 10
N_SUBSAMPLES = 100
INITIAL_TRAINING_TRANSITIONS = 7
MIN_TRANSITIONS = 11


def _parse_utc(value: str) -> datetime:
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    attempts = []
    try:
        dt = datetime.fromisoformat(raw)
        attempts.append(dt)
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            attempts.append(datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc))
        except ValueError:
            pass
    if not attempts:
        raise ValueError(f"unparseable datetime: {value!r}")
    dt = attempts[0]
    if dt.tzinfo is None:
        # Dryad README explicitly defines datetime as UTC.
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _in_window(dt: datetime) -> bool:
    md = (dt.month, dt.day)
    return WINDOW_START <= md <= WINDOW_END


def _offset_from_noon(dt: datetime) -> float:
    noon = datetime.combine(dt.date(), time(TARGET_HOUR_UTC), tzinfo=timezone.utc)
    return abs((dt - noon).total_seconds()) / 3600.0


def _mean_pairwise_distance(points: Sequence[Sequence[float]]) -> float:
    values: list[float] = []
    for i in range(len(points)):
        xi, yi = float(points[i][0]), float(points[i][1])
        for j in range(i):
            xj, yj = float(points[j][0]), float(points[j][1])
            values.append(math.hypot(xi - xj, yi - yj))
    if not values:
        raise ValueError("pairwise distance requires at least two points")
    mean = fmean(values)
    if not math.isfinite(mean) or mean <= 0:
        raise ValueError("mean pairwise distance must be finite and positive")
    return float(mean)


def _deterministic_ids(ids: Sequence[str], day: str, replicate: int) -> list[str]:
    keyed = []
    for individual in ids:
        token = f"{day}|{replicate}|{individual}".encode("utf-8")
        keyed.append((hashlib.sha256(token).hexdigest(), individual))
    keyed.sort()
    return [individual for _digest, individual in keyed[:FIXED_N]]


def annual_spatial_summaries(rows: Iterable[dict[str, str]]) -> dict[int, dict[str, float | int]]:
    # (year, date) -> individual -> (offset, timestamp, x, y)
    daily: dict[tuple[int, str], dict[str, tuple[float, datetime, float, float]]] = defaultdict(dict)

    for row in rows:
        for required in ("id", "datetime", "x", "y"):
            if required not in row:
                raise KeyError(f"GPS file missing required column {required!r}")
        individual = str(row["id"]).strip()
        if not individual:
            continue
        dt = _parse_utc(str(row["datetime"]))
        if not _in_window(dt):
            continue
        offset = _offset_from_noon(dt)
        if offset > MAX_OFFSET_HOURS:
            continue
        try:
            x, y = float(row["x"]), float(row["y"])
        except (TypeError, ValueError) as exc:
            raise ValueError("GPS coordinates must be numeric") from exc
        if not (math.isfinite(x) and math.isfinite(y)):
            raise ValueError("GPS coordinates must be finite")
        key = (dt.year, dt.date().isoformat())
        prev = daily[key].get(individual)
        candidate = (offset, dt, x, y)
        if prev is None or offset < prev[0] or (offset == prev[0] and dt < prev[1]):
            daily[key][individual] = candidate

    by_year: dict[int, list[tuple[str, dict[str, tuple[float, datetime, float, float]]]]] = defaultdict(list)
    for (year, day), observed in daily.items():
        if len(observed) >= MIN_DAILY_INDIVIDUALS:
            by_year[year].append((day, observed))

    out: dict[int, dict[str, float | int]] = {}
    for year in sorted(by_year):
        days = sorted(by_year[year], key=lambda x: x[0])
        if len(days) < MIN_ELIGIBLE_DAYS_PER_YEAR:
            continue

        day_ratio: list[float] = []
        day_pop: list[float] = []
        day_ind: list[float] = []
        day_scale: list[float] = []
        day_all_ratio: list[float] = []

        for day, observed in days:
            ids = sorted(observed)
            all_points = [(observed[i][2], observed[i][3]) for i in ids]
            day_all_ratio.append(cvratio(all_points))

            reps = 1 if len(ids) == FIXED_N else N_SUBSAMPLES
            ratios: list[float] = []
            pops: list[float] = []
            inds: list[float] = []
            scales: list[float] = []
            for replicate in range(reps):
                chosen = ids if len(ids) == FIXED_N else _deterministic_ids(ids, day, replicate)
                points = [(observed[i][2], observed[i][3]) for i in chosen]
                ratios.append(cvratio(points))
                pops.append(cvpop(points))
                inds.append(cvind(points))
                scales.append(_mean_pairwise_distance(points))
            day_ratio.append(fmean(ratios))
            day_pop.append(fmean(pops))
            day_ind.append(fmean(inds))
            day_scale.append(fmean(scales))

        out[year] = {
            "eligible_days": len(days),
            "cvratio": float(fmean(day_ratio)),
            "cvpop": float(fmean(day_pop)),
            "cvind": float(fmean(day_ind)),
            "spatial_scale": float(fmean(day_scale)),
            "full_sample_cvratio": float(fmean(day_all_ratio)),
        }
    return out


def read_gps_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def abundance_from_rows(rows: Iterable[dict[str, Any]]) -> dict[int, float]:
    values: dict[int, set[float]] = defaultdict(set)
    for row in rows:
        date = row.get("Date")
        n_raw = row.get("N.tot")
        if date in (None, "") or n_raw in (None, ""):
            continue
        if isinstance(date, datetime):
            year = date.year
        else:
            raw = str(date).strip()
            parsed = None
            for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%Y/%m/%d"):
                try:
                    parsed = datetime.strptime(raw, fmt)
                    break
                except ValueError:
                    continue
            if parsed is None:
                raise ValueError(f"unparseable abundance date: {date!r}")
            year = parsed.year
        n = float(n_raw)
        if not math.isfinite(n) or n <= 0:
            raise ValueError(f"N.tot must be finite and positive: {n_raw!r}")
        values[year].add(n)

    out: dict[int, float] = {}
    for year, observed in sorted(values.items()):
        if len(observed) != 1:
            raise RuntimeError(f"{year}: expected exactly one unique N.tot, found {sorted(observed)}")
        out[year] = next(iter(observed))
    return out


def read_abundance_xlsx(path: str | Path) -> dict[int, float]:
    try:
        import openpyxl  # type: ignore
    except ImportError as exc:
        raise RuntimeError("openpyxl is required to read the frozen Dryad workbook") from exc

    workbook = openpyxl.load_workbook(path, data_only=True, read_only=True)
    matches: list[list[dict[str, Any]]] = []
    for sheet in workbook.worksheets:
        rows = list(sheet.iter_rows(values_only=True))
        for header_index, row in enumerate(rows[:20]):
            names = [str(value).strip() if value is not None else "" for value in row]
            if "Date" not in names or "N.tot" not in names:
                continue
            if names.count("Date") != 1 or names.count("N.tot") != 1:
                raise RuntimeError("ambiguous Date/N.tot header in workbook")
            mapped: list[dict[str, Any]] = []
            for values in rows[header_index + 1 :]:
                mapped.append({name: value for name, value in zip(names, values) if name})
            matches.append(mapped)
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one worksheet table with Date and N.tot, found {len(matches)}")
    return abundance_from_rows(matches[0])


def build_transitions(
    spatial: dict[int, dict[str, float | int]],
    abundance: dict[int, float],
) -> list[dict[str, float | int]]:
    transitions: list[dict[str, float | int]] = []
    for year in sorted(spatial):
        if year not in abundance or year + 1 not in abundance:
            continue
        scale = float(spatial[year]["spatial_scale"])
        ratio = float(spatial[year]["cvratio"])
        n_now = float(abundance[year])
        n_next = float(abundance[year + 1])
        transitions.append(
            {
                "year": year,
                "log_n_current": math.log(n_now),
                "log_spatial_scale": math.log(scale),
                "cvratio": ratio,
                "g_next": math.log(n_next / n_now),
            }
        )
    return transitions


def _solve(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    aug = [list(map(float, a[i])) + [float(b[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-10:
            raise RuntimeError("singular OLS normal equations")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [aug[i][-1] for i in range(n)]


def _fit_predict(train: list[dict[str, float | int]], test: dict[str, float | int], features: list[str]) -> float:
    means: dict[str, float] = {}
    sds: dict[str, float] = {}
    for feature in features:
        vals = [float(r[feature]) for r in train]
        mean = fmean(vals)
        variance = fmean((v - mean) ** 2 for v in vals)
        sd = math.sqrt(variance)
        if sd < 1e-10:
            raise RuntimeError(f"training predictor has zero variance: {feature}")
        means[feature] = mean
        sds[feature] = sd

    x: list[list[float]] = []
    y: list[float] = []
    for row in train:
        x.append([1.0] + [(float(row[f]) - means[f]) / sds[f] for f in features])
        y.append(float(row["g_next"]))
    p = len(features) + 1
    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    xty = [0.0 for _ in range(p)]
    for xi, yi in zip(x, y):
        for j in range(p):
            xty[j] += xi[j] * yi
            for k in range(p):
                xtx[j][k] += xi[j] * xi[k]
    beta = _solve(xtx, xty)
    test_x = [1.0] + [(float(test[f]) - means[f]) / sds[f] for f in features]
    return float(sum(b * v for b, v in zip(beta, test_x)))


def rolling_forecast(transitions: list[dict[str, float | int]]) -> dict[str, Any]:
    transitions = sorted(transitions, key=lambda r: int(r["year"]))
    if len(transitions) < MIN_TRANSITIONS:
        return {
            "status": "insufficient_temporal_replication",
            "n_transitions": len(transitions),
            "minimum_required": MIN_TRANSITIONS,
        }

    base_features = ["log_n_current", "log_spatial_scale"]
    full_features = base_features + ["cvratio"]
    forecasts: list[dict[str, float | int]] = []
    for index in range(INITIAL_TRAINING_TRANSITIONS, len(transitions)):
        train = transitions[:index]
        test = transitions[index]
        p0 = _fit_predict(train, test, base_features)
        p1 = _fit_predict(train, test, full_features)
        observed = float(test["g_next"])
        forecasts.append(
            {
                "year": int(test["year"]),
                "observed_g_next": observed,
                "m0_prediction": p0,
                "m1_prediction": p1,
                "m0_error": p0 - observed,
                "m1_error": p1 - observed,
                "squared_error_gain_m0_minus_m1": (p0 - observed) ** 2 - (p1 - observed) ** 2,
            }
        )

    if len(forecasts) < 4:
        return {
            "status": "insufficient_out_of_sample_forecasts",
            "n_transitions": len(transitions),
            "n_forecasts": len(forecasts),
        }

    rmse0 = math.sqrt(fmean(float(r["m0_error"]) ** 2 for r in forecasts))
    rmse1 = math.sqrt(fmean(float(r["m1_error"]) ** 2 for r in forecasts))
    mae0 = fmean(abs(float(r["m0_error"])) for r in forecasts)
    mae1 = fmean(abs(float(r["m1_error"])) for r in forecasts)
    decision = (
        "detected_incremental_future_information"
        if rmse1 < rmse0 and mae1 < mae0
        else "no_detected_incremental_future_information"
    )
    return {
        "status": "completed_primary_temporal_validation",
        "decision": decision,
        "n_transitions": len(transitions),
        "n_forecasts": len(forecasts),
        "m0_rmse": rmse0,
        "m1_rmse": rmse1,
        "m0_mae": mae0,
        "m1_mae": mae1,
        "rmse_improvement_m0_minus_m1": rmse0 - rmse1,
        "mae_improvement_m0_minus_m1": mae0 - mae1,
        "forecasts": forecasts,
    }


def run(gps_csv: str | Path, abundance_xlsx: str | Path) -> dict[str, Any]:
    spatial = annual_spatial_summaries(read_gps_csv(gps_csv))
    abundance = read_abundance_xlsx(abundance_xlsx)
    transitions = build_transitions(spatial, abundance)
    primary = rolling_forecast(transitions)
    return {
        "analysis_id": "svalbard_love_otto_future_population_v1",
        "analysis_status": "locked_retrospective_temporal_validation",
        "spatial_years": spatial,
        "abundance_years": abundance,
        "transitions": transitions,
        "primary": primary,
        "claim_boundary": (
            "One wild population and a public GPS archive with intentionally reduced coordinate precision; "
            "positive performance would not establish causality or cross-species generality."
        ),
    }


def write(gps_csv: str | Path, abundance_xlsx: str | Path, output: str | Path) -> None:
    result = run(gps_csv, abundance_xlsx)
    dest = Path(output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
