from __future__ import annotations

import math

from eco_genetic_warning_extensions.headroom_effect_scale import (
    ANALYSIS_STATUS,
    summarise,
)


def _record(master: int, rep: int, intervention: str, condition: str, value: float) -> dict:
    return {
        "intervention": intervention,
        "condition": condition,
        "master_seed": master,
        "replicate": rep,
        "states": {
            "20": {
                "max_headroom": value,
                "positive_headroom_count": 0,
            }
        },
    }


def test_headroom_scale_summary_uses_locked_pairing_and_marks_posthoc() -> None:
    records = []
    # 12 blocks x 500 keys x 4 cells = 24,000 trajectories.
    for master in range(12):
        for rep in range(500):
            jitter = (master * 500 + rep) * 1e-7
            delta = 1e-5 if rep % 2 == 0 else -1e-5
            records.extend(
                [
                    _record(master, rep, "baseline_local_allele_selection", "AA", 0.004 + jitter + delta),
                    _record(master, rep, "baseline_local_allele_selection", "RR", 0.002 + jitter),
                    _record(master, rep, "delete_local_allele_selection", "AA", 0.003 + jitter),
                    _record(master, rep, "delete_local_allele_selection", "RR", 0.002 + jitter),
                ]
            )

    out = summarise(records)
    assert out["analysis_status"] == ANALYSIS_STATUS
    assert out["n_trajectories"] == 24_000
    assert out["n_paired_keys"] == 6_000
    assert math.isclose(out["max_headroom_DID"], 0.001, abs_tol=1e-15)
    assert out["raw_pooled_max_headroom_sd"] > 0
    assert out["paired_DID_sd"] > 0
    assert out["all_positive_headroom_counts_zero"] is True
