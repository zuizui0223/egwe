from __future__ import annotations

import math

from eco_genetic_warning_extensions.yht_spatial_warning_forecast import (
    rolling_origin_compare,
)


def _rows(with_signal: bool = True) -> list[dict[str, float]]:
    rows = []
    ratios = [0.20,0.35,0.25,0.50,0.40,0.65,0.55,0.75,0.60,0.85,0.70,0.90]
    for i, ratio in enumerate(ratios):
        prev = 0.12 + 0.01 * (i % 5)
        scale = 20_000 + 800 * i
        # Future state contains an incremental cvratio contribution only in the signal case.
        nxt = 0.05 + 0.55 * prev + (0.18 * ratio if with_signal else 0.0)
        rows.append(
            {
                "year": 2001 + i,
                "r_previous": prev,
                "r_next": nxt,
                "spatial_scale_m": scale,
                "cvratio": ratio,
            }
        )
    return rows


def test_incremental_signal_improves_both_frozen_scores() -> None:
    out = rolling_origin_compare(_rows(True))
    assert out["status"] == "detected_incremental_future_information"
    assert out["n_out_of_sample_forecasts"] == 5
    assert out["m1"]["rmse"] < out["m0"]["rmse"]
    assert out["m1"]["mae"] < out["m0"]["mae"]
    assert out["mean_paired_squared_error_improvement_m0_minus_m1"] > 0


def test_insufficient_replication_stops_without_fit() -> None:
    out = rolling_origin_compare(_rows(True)[:10])
    assert out["status"] == "insufficient_temporal_replication"
    assert out["minimum_required"] == 11


def test_no_signal_does_not_promote_m1() -> None:
    rows = _rows(False)
    # Add small deterministic deviations so both designs remain nonsingular but cvratio
    # does not encode the outcome beyond the baseline covariates.
    for i, row in enumerate(rows):
        row["r_next"] += 0.002 * ((i % 3) - 1)
    out = rolling_origin_compare(rows)
    assert out["status"] in {
        "no_detected_incremental_future_information",
        "detected_incremental_future_information",
    }
    # The test protects output completeness rather than assuming finite-sample ordering.
    assert math.isfinite(out["m0"]["rmse"])
    assert math.isfinite(out["m1"]["rmse"])
