from __future__ import annotations

import math

from eco_genetic_warning_extensions.last_refuge_posthoc_decomposition import (
    ANALYSIS_STATUS,
    patch_component_scores,
    summarise,
)


def test_component_scores_match_declared_posthoc_decomposition() -> None:
    q, t, g, d, theta = 0.72, 0.64, 0.41, 0.83, 0.525
    out = patch_component_scores(q, t, g, d, theta)
    support = 0.6 * q + 0.3 * t + 0.1 * g
    assert math.isclose(out["q"], q, abs_tol=1e-15)
    assert math.isclose(out["density_q"], d * q, abs_tol=1e-15)
    assert math.isclose(out["support_no_density"], support, abs_tol=1e-15)
    assert math.isclose(
        out["route_margin"] - out["density_q"],
        d * (0.3 * t + 0.1 * g - 0.4 * q) - theta
        - __import__(
            "eco_genetic_warning_extensions.last_refuge_warning_holdout",
            fromlist=["HEADROOM_OFFSET"],
        ).HEADROOM_OFFSET,
        abs_tol=1e-15,
    )


def test_analysis_is_explicitly_posthoc_and_does_not_relabel_primary_estimand() -> None:
    assert ANALYSIS_STATUS == "post_hoc_exploratory_not_preregistered"


def test_summary_requires_same_twelve_seed_block_structure() -> None:
    records = []
    for seed in range(12):
        for i, event in enumerate((False, False, True, True)):
            q = (0.9, 0.8, 0.2, 0.1)[i]
            records.append(
                {
                    "master_seed": seed,
                    "loss_by_generation_40": event,
                    "max_q": q,
                    "max_density_q": q,
                    "max_support_no_density": q,
                    "max_route_margin": q,
                    "argmax_q": 0,
                    "argmax_route_margin": 0,
                    "all_patch_density_below_one": True,
                }
            )
    protocol = {"experiment_id": "last_refuge_warning_holdout_v1"}
    out = summarise(protocol, records)
    assert out["analysis_status"] == ANALYSIS_STATUS
    assert out["n_records"] == 48
    assert out["argmax_route_margin_equals_argmax_q"]["fraction"] == 1.0
    assert out["observation_density"]["all_trajectories_have_all_patch_density_below_one"] is True
    for cell in out["paired_auc_differences"].values():
        assert math.isclose(cell["mean"], 0.0, abs_tol=1e-15)
        assert cell["positive_blocks"] == 0
        assert cell["all_blocks_positive"] is False
