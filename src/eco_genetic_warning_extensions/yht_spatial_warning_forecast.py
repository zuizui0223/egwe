from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import fmean, stdev
from typing import Any

MIN_OBSERVATIONS = 11
INITIAL_TRAINING_OBSERVATIONS = 7


def _solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    m = [list(map(float, row)) + [float(b[i])] for i, row in enumerate(a)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-12:
            raise RuntimeError("OLS design is singular under the frozen training fold")
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [x / scale for x in m[col]]
        for r in range(n):
            if r == col:
                continue
            factor = m[r][col]
            if factor:
                m[r] = [x - factor * y for x, y in zip(m[r], m[col])]
    return [m[i][-1] for i in range(n)]


def _ols_fit(x: list[list[float]], y: list[float]) -> list[float]:
    if len(x) != len(y) or not x:
        raise ValueError("non-empty X and y must have the same length")
    p = len(x[0]) + 1
    design = [[1.0] + list(map(float, row)) for row in x]
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for row, target in zip(design, y):
        for i in range(p):
            xty[i] += row[i] * float(target)
            for j in range(p):
                xtx[i][j] += row[i] * row[j]
    return _solve_linear(xtx, xty)


def _predict(beta: list[float], row: list[float]) -> float:
    return float(beta[0] + sum(b * x for b, x in zip(beta[1:], row)))


def _standardize_train_test(
    train: list[list[float]],
    test: list[float],
) -> tuple[list[list[float]], list[float]]:
    p = len(train[0])
    means: list[float] = []
    sds: list[float] = []
    for j in range(p):
        col = [float(row[j]) for row in train]
        means.append(float(fmean(col)))
        sd = float(stdev(col))
        if not math.isfinite(sd) or sd <= 0:
            raise RuntimeError("frozen predictor has zero/invalid training-fold SD")
        sds.append(sd)
    train_z = [
        [(float(row[j]) - means[j]) / sds[j] for j in range(p)]
        for row in train
    ]
    test_z = [(float(test[j]) - means[j]) / sds[j] for j in range(p)]
    return train_z, test_z


def _metrics(errors: list[float]) -> dict[str, float]:
    return {
        "rmse": math.sqrt(fmean(e * e for e in errors)),
        "mae": fmean(abs(e) for e in errors),
    }


def rolling_origin_compare(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(rows) < MIN_OBSERVATIONS:
        return {
            "status": "insufficient_temporal_replication",
            "n_observations": len(rows),
            "minimum_required": MIN_OBSERVATIONS,
        }

    ordered = sorted(rows, key=lambda r: int(r["year"]))
    years = [int(r["year"]) for r in ordered]
    if len(set(years)) != len(years):
        raise ValueError("year must be unique in the normalized forecast table")

    normalized = []
    for r in ordered:
        previous = float(r["r_previous"])
        nxt = float(r["r_next"])
        scale = float(r["spatial_scale_m"])
        ratio = float(r["cvratio"])
        if not all(math.isfinite(x) for x in (previous, nxt, scale, ratio)):
            raise ValueError("all normalized forecast values must be finite")
        if scale <= 0:
            raise ValueError("spatial_scale_m must be positive")
        normalized.append(
            {
                "year": int(r["year"]),
                "r_previous": previous,
                "r_next": nxt,
                "log_spatial_scale": math.log(scale),
                "cvratio": ratio,
            }
        )

    forecasts = []
    errors0: list[float] = []
    errors1: list[float] = []
    squared_improvements: list[float] = []

    for i in range(INITIAL_TRAINING_OBSERVATIONS, len(normalized)):
        train = normalized[:i]
        test = normalized[i]

        y_train = [r["r_next"] for r in train]
        x0_train = [[r["r_previous"], r["log_spatial_scale"]] for r in train]
        x1_train = [
            [r["r_previous"], r["log_spatial_scale"], r["cvratio"]]
            for r in train
        ]
        x0_test = [test["r_previous"], test["log_spatial_scale"]]
        x1_test = [test["r_previous"], test["log_spatial_scale"], test["cvratio"]]

        x0z, x0testz = _standardize_train_test(x0_train, x0_test)
        x1z, x1testz = _standardize_train_test(x1_train, x1_test)

        b0 = _ols_fit(x0z, y_train)
        b1 = _ols_fit(x1z, y_train)
        pred0 = _predict(b0, x0testz)
        pred1 = _predict(b1, x1testz)
        e0 = pred0 - test["r_next"]
        e1 = pred1 - test["r_next"]
        errors0.append(e0)
        errors1.append(e1)
        squared_improvements.append(e0 * e0 - e1 * e1)

        forecasts.append(
            {
                "year": test["year"],
                "n_training": i,
                "observed_r_next": test["r_next"],
                "m0_prediction": pred0,
                "m1_prediction": pred1,
                "m0_error": e0,
                "m1_error": e1,
                "squared_error_improvement_m0_minus_m1": e0 * e0 - e1 * e1,
            }
        )

    m0 = _metrics(errors0)
    m1 = _metrics(errors1)
    improved_both = m1["rmse"] < m0["rmse"] and m1["mae"] < m0["mae"]

    return {
        "status": (
            "detected_incremental_future_information"
            if improved_both
            else "no_detected_incremental_future_information"
        ),
        "n_observations": len(normalized),
        "n_out_of_sample_forecasts": len(forecasts),
        "initial_training_observations": INITIAL_TRAINING_OBSERVATIONS,
        "standardization": "training-fold mean and sample SD only",
        "m0": m0,
        "m1": m1,
        "mean_paired_squared_error_improvement_m0_minus_m1": float(
            fmean(squared_improvements)
        ),
        "forecast_rows": forecasts,
        "claim_ceiling": (
            "Single-herd rolling temporal transfer only; no universal threshold, "
            "causal direction or cross-species warning law is inferred."
        ),
    }


def read_normalized_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_result(path: str | Path, output: str | Path) -> None:
    result = rolling_origin_compare(read_normalized_csv(path))
    dest = Path(output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
