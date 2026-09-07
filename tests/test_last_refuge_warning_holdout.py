from __future__ import annotations

import math
from pathlib import Path

from eco_genetic_warning_extensions.last_refuge_warning_holdout import (
    HEADROOM_OFFSET,
    _block_summary,
    load_protocol,
    patch_route_margin,
    roc_auc,
)


def test_protocol_is_frozen_before_holdout_outcomes() -> None:
    p = load_protocol()
    assert p["experiment_id"] == "last_refuge_warning_holdout_v1"
    assert p["status"] == "prospective_locked_before_implementation_and_outcomes"
    assert p["forcing"]["observation_generation"] == 10
    assert "snapshot at generation 9" in p["forcing"]["observation_state"]
    assert p["forcing"]["endpoint_generation"] == 40
    assert p["replication"]["master_seeds"] == list(range(204701, 204713))
    assert p["replication"]["total_trajectories"] == 12000
    assert "No threshold is selected" in p["stop_rules"][1]
    assert "post-observation variable" in p["stop_rules"][3]


def test_headroom_offset_is_exact_locked_switch_offset() -> None:
    assert math.isclose(HEADROOM_OFFSET, math.log(0.625 / 0.375) / 4.5, abs_tol=1e-15)


def test_patch_margin_exactly_matches_declared_support_identity() -> None:
    q, t, g, d, theta = 0.7, 0.8, 0.4, 0.9, 0.525
    got = patch_route_margin(q, t, g, d, theta)
    expected = d * (0.6 * q + 0.3 * t + 0.1 * g) - (theta + HEADROOM_OFFSET)
    assert math.isclose(got, expected, abs_tol=1e-15)


def test_roc_auc_is_threshold_free_and_tie_aware() -> None:
    assert math.isclose(roc_auc([0.1, 0.2, 0.8, 0.9], [False, False, True, True]), 1.0)
    assert math.isclose(roc_auc([0.9, 0.8, 0.2, 0.1], [False, False, True, True]), 0.0)
    assert math.isclose(roc_auc([0.5, 0.5, 0.5, 0.5], [False, False, True, True]), 0.5)


def test_seed_block_ci_requires_exactly_twelve_blocks() -> None:
    out = _block_summary([0.8 + i * 0.001 for i in range(12)])
    assert out["n_master_seed_blocks"] == 12
    assert out["ci95"][0] < out["mean"] < out["ci95"][1]


def test_source_preserves_co_timed_observation_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "src" / "eco_genetic_warning_extensions" / "last_refuge_warning_holdout.py").read_text()
    assert "snapshot_generation = observation_generation - 1" in text
    assert "current = result.snapshots[snapshot_generation]" in text
    assert "theta = barriers[observation_generation - 1]" in text
    assert "max_route_margin" in text
    assert "max_q" in text
