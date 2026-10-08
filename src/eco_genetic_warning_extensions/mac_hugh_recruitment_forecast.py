from __future__ import annotations

import csv
import io
import math
from statistics import fmean, stdev
from typing import Any

MIN_LAGGED_YEARS = 11
INITIAL_TRAIN_YEARS = 7
EXPECTED_COLUMNS = {
    "Annee", "Recrutement", "Variance_long", "Nb_femelle",
}
MISSING_VALUES = {"", "na", "nan", "null", "none"}


def _float_or_none(value: str) -> float | None:
    x = value.strip()
    if x.casefold() in MISSING_VALUES:
        return None
    result = float(x)
    return result if math.isfinite(result) else None


def load_complete_lagged_cases(source: str) -> tuple[list[dict[str, float]], dict[str, Any]]:
    reader = csv.DictReader(io.StringIO(source), delimiter="\t")
    header = set(reader.fieldnames or [])
    if not EXPECTED_COLUMNS.issubset(header):
        raise ValueError(f"missing source-defined columns: {sorted(EXPECTED_COLUMNS - header)}")
    annual: dict[int, dict[str, float | None]] = {}
    rows = 0
    for row in reader:
        rows += 1
        year_raw = _float_or_none(str(row["Annee"]))
        if year_raw is None or int(year_raw) != year_raw:
            raise ValueError("year must be an integer")
        year = int(year_raw)
        if not 1994 <= year <= 2019:
            raise ValueError("outside preregistered source period 1994-2019")
        if year in annual:
            raise ValueError("duplicate annual recruitment response")
        annual[year] = {
            "r": _float_or_none(str(row["Recrutement"])),
            "geo": _float_or_none(str(row["Variance_long"])),
            "effort": _float_or_none(str(row["Nb_femelle"])),
        }

    cases: list[dict[str, float]] = []
    for year in sorted(annual):
        now = annual[year]
        before = annual.get(year - 1)
        if before is None:
            continue
        if any(x is None for x in (before["r"], now["r"], now["geo"], now["effort"])):
            continue
        cases.append({
            "year": float(year),
            "r_previous": float(before["r"]),
            "r_next": float(now["r"]),
            "effort": float(now["effort"]),
            "geo": float(now["geo"]),
        })
    return cases, {
        "n_source_raw_rows": rows,
        "n_unique_source_years": len(annual),
        "n_complete_consecutive_lagged_years": len(cases),
        "eligible_years": [int(x["year"]) for x in cases],
        "rows_with_response_values_opened": rows,
        "no_missing_year_imputation": True,
    }


def _solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    m = [matrix[i][:] + [vector[i]] for i in range(n)]
    for j in range(n):
        p = max(range(j, n), key=lambda k: abs(m[k][j]))
        if abs(m[p][j]) <= 1e-11:
            raise ArithmeticError("singular or near-singular training design")
        m[j], m[p] = m[p], m[j]
        pivot = m[j][j]
        m[j] = [x / pivot for x in m[j]]
        for i in range(n):
            if i == j:
                continue
            scale = m[i][j]
            m[i] = [x - scale * y for x, y in zip(m[i], m[j])]
    return [m[i][n] for i in range(n)]


def _forecast(train: list[dict[str, float]], test: dict[str, float], columns: tuple[str, ...]) -> float:
    mean_sd = []
    for c in columns:
        values = [r[c] for r in train]
        sd = stdev(values)
        if not math.isfinite(sd) or sd <= 0:
            raise ArithmeticError("zero or invalid predictor variation in training-only fold")
        mean_sd.append((fmean(values), sd))

    def vector(rec: dict[str, float]) -> list[float]:
        return [1.0] + [
            (rec[c] - center) / sd
            for c, (center, sd) in zip(columns, mean_sd)
        ]

    design = [vector(r) for r in train]
    dimension = len(columns) + 1
    xtx = [[sum(x[j] * x[k] for x in design) for k in range(dimension)] for j in range(dimension)]
    xty = [sum(x[j] * r["r_next"] for x, r in zip(design, train)) for j in range(dimension)]
    beta = _solve(xtx, xty)
    return float(sum(b * x for b, x in zip(beta, vector(test))))


def audit_forecasts(source: str) -> dict[str, Any]:
    cases, counts = load_complete_lagged_cases(source)
    base = {
        "experiment_id": "mac_hugh_caribou_temporal_recruitment_v1",
        "source_doi": "10.5683/SP3/0ROESU",
        "source_status": "published_null_or_weak_relationship_known_before_audit",
        "method": "single-herd expanding-window forward prediction, source-defined geography",
        **counts,
        "direct_love_otto_cv_test": False,
    }
    if len(cases) < MIN_LAGGED_YEARS:
        return {
            **base,
            "status": "insufficient_temporal_replication_stop_before_model_fit",
            "minimum_lagged_years": MIN_LAGGED_YEARS,
            "fitted_forecast_models": 0,
            "claim_ceiling": "Not an association null; too few consecutive complete annual records.",
        }

    errors0: list[float] = []
    errors1: list[float] = []
    heldout_years: list[int] = []
    try:
        for k in range(INITIAL_TRAIN_YEARS, len(cases)):
            train, test = cases[:k], cases[k]
            pred0 = _forecast(train, test, ("r_previous", "effort"))
            pred1 = _forecast(train, test, ("r_previous", "effort", "geo"))
            errors0.append(pred0 - test["r_next"])
            errors1.append(pred1 - test["r_next"])
            heldout_years.append(int(test["year"]))
    except ArithmeticError as exc:
        return {
            **base,
            "status": "singular_training_fold_stop",
            "reason": str(exc),
            "fitted_forecast_models": 0,
            "claim_ceiling": "Fail closed rather than tune predictors after opening outcomes.",
        }

    def scores(e: list[float]) -> dict[str, float]:
        return {
            "RMSE": float(math.sqrt(fmean(v*v for v in e))),
            "MAE": float(fmean(abs(v) for v in e)),
        }

    m0, m1 = scores(errors0), scores(errors1)
    passed = m1["RMSE"] < m0["RMSE"] and m1["MAE"] < m0["MAE"]
    return {
        **base,
        "status": "incremental_temporal_forecast_gain_detected" if passed else "no_incremental_temporal_forecast_gain_detected",
        "minimum_lagged_years": MIN_LAGGED_YEARS,
        "n_heldout_forecasts": len(heldout_years),
        "heldout_years": heldout_years,
        "M0": m0,
        "M1": m1,
        "mean_paired_squared_error_difference_M0_minus_M1": float(
            fmean(a*a - b*b for a, b in zip(errors0, errors1))
        ),
        "fitted_forecast_models": len(heldout_years)*2,
        "outcome_rows_or_predictions_redistributed": False,
        "claim_ceiling": (
            "Retrospective same-herd temporal prediction of source-defined route "
            "geography only; no Love-Otto IID metric, causality or independent-herd generality."
        ),
    }
