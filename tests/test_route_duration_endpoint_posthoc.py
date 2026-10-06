from __future__ import annotations

import math

from eco_genetic_warning_extensions.route_duration_endpoint_posthoc import (
    ANALYSIS_STATUS,
    summarise,
)


def _record(
    master: int,
    rep: int,
    trajectory_seed: int,
    condition: str,
    *,
    loss: bool,
    duration: int,
) -> dict:
    return {
        "master_seed": master,
        "replicate": rep,
        "trajectory_seed": trajectory_seed,
        "condition": condition,
        "loss_by_endpoint": loss,
        "positive_margin_refuge_generations": duration,
    }


def test_route_duration_endpoint_audit_marks_posthoc_and_pairs_exactly() -> None:
    records = []
    # Locked-shape synthetic ensemble: 6 master seeds x 500 paired keys x 4 conditions.
    # Full feedback helps the endpoint in both AA/RR but shortens route duration.
    for master in range(6):
        for rep in range(500):
            seed = master * 100_000 + rep
            aa_q_loss = rep < 350
            aa_full_loss = rep < 330
            rr_q_loss = rep < 380
            rr_full_loss = rep < 350
            records.extend(
                [
                    _record(master, rep, seed, "AA_full", loss=aa_full_loss, duration=1),
                    _record(master, rep, seed, "AA_q_only", loss=aa_q_loss, duration=2),
                    _record(master, rep, seed, "RR_full", loss=rr_full_loss, duration=1),
                    _record(master, rep, seed, "RR_q_only", loss=rr_q_loss, duration=2),
                ]
            )

    out = summarise(records)
    assert out["analysis_status"] == ANALYSIS_STATUS
    assert out["n_trajectories"] == 12_000
    assert out["n_paired_keys"] == 3_000
    assert out["same_ensemble_sign_reversal"] is True
    assert out["all_endpoint_rescues_lack_duration_extension"] is True
    assert math.isclose(
        out["states"]["AA"]["endpoint_benefit_qonly_minus_full"]["mean"],
        0.04,
        abs_tol=1e-15,
    )
    assert math.isclose(
        out["states"]["RR"]["endpoint_benefit_qonly_minus_full"]["mean"],
        0.06,
        abs_tol=1e-15,
    )
    assert out["states"]["AA"]["positive_margin_duration_full_minus_qonly"]["mean"] == -1.0
    assert out["states"]["RR"]["positive_margin_duration_full_minus_qonly"]["mean"] == -1.0
