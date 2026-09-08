"""Deterministic precision audit for the locked Phase U/R/S portability tests.

This module opens no simulations. It reads locked block counts and characterizes
asymptotic power for the five-block Pearson equal-rate test.
"""
from __future__ import annotations

import json
from math import exp, factorial, sqrt
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
CRITICAL_CHI2_DF4_ALPHA05 = 9.487729036781154


def chi2_cdf_even(x: float, df: int) -> float:
    if x < 0 or df < 2 or df % 2:
        raise ValueError("x must be nonnegative and df a positive even integer")
    z = x / 2.0
    return 1.0 - exp(-z) * sum((z**j) / factorial(j) for j in range(df // 2))


def noncentral_chi2_cdf_even(x: float, df: int, noncentrality: float) -> float:
    if noncentrality < 0:
        raise ValueError("noncentrality must be nonnegative")
    mean = noncentrality / 2.0
    weight = exp(-mean)
    total = weight * chi2_cdf_even(x, df)
    j = 0
    # Poisson-mixture representation; the locked design needs lambda ~12-16.
    while j < 1000:
        j += 1
        if mean == 0.0:
            break
        weight *= mean / j
        total += weight * chi2_cdf_even(x, df + 2 * j)
        if j > mean + 20 and weight < 1e-16:
            break
    return min(1.0, max(0.0, total))


def power_for_w(total_n: int, w: float, *, df: int = 4) -> float:
    lam = float(total_n) * float(w) ** 2
    return 1.0 - noncentral_chi2_cdf_even(CRITICAL_CHI2_DF4_ALPHA05, df, lam)


def minimum_detectable_w(total_n: int, power: float, *, df: int = 4) -> float:
    if total_n <= 0 or not 0.0 < power < 1.0:
        raise ValueError("invalid total_n or power")
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if power_for_w(total_n, mid, df=df) < power:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def pearson_statistic(blocks: Iterable[tuple[int, int]]) -> tuple[float, int, float, int]:
    block_tuple = tuple((int(losses), int(eligible)) for losses, eligible in blocks)
    total_n = sum(eligible for _, eligible in block_tuple)
    total_losses = sum(losses for losses, _ in block_tuple)
    pooled = total_losses / total_n
    statistic = 0.0
    for losses, eligible in block_tuple:
        expected_loss = eligible * pooled
        expected_nonloss = eligible * (1.0 - pooled)
        statistic += ((losses - expected_loss) ** 2) / expected_loss
        statistic += (((eligible - losses) - expected_nonloss) ** 2) / expected_nonloss
    return statistic, len(block_tuple) - 1, pooled, total_n


def observed_w(blocks: Iterable[tuple[int, int]]) -> float:
    statistic, _, _, total_n = pearson_statistic(blocks)
    return sqrt(statistic / total_n)


def _phase_u_blocks(payload: dict, migration_rate: float) -> tuple[tuple[int, int], ...]:
    row = next(item for item in payload["condition_summaries"] if float(item["migration_rate"]) == migration_rate)
    return tuple((int(block["losses"]), int(block["eligible"])) for block in row["blocks"])


def _condition_blocks(payload: dict, condition: str) -> tuple[tuple[int, int], ...]:
    row = next(item for item in payload["conditions"] if item["condition"] == condition)
    return tuple((int(losses), int(eligible)) for losses, eligible in row["blocks"])


def build_summary(repo_root: Path = ROOT) -> dict:
    phase_u = json.loads((repo_root / "artifacts/fresh_connectivity_replication/phase_u_locked_summary.json").read_text())
    phase_r = json.loads((repo_root / "artifacts/process_resolved_movement/phase_r_locked_summary.json").read_text())
    phase_s = json.loads((repo_root / "artifacts/process_resolved_pollen/phase_s_locked_summary.json").read_text())

    shared_no_r = _condition_blocks(phase_r, "no_connectivity")
    shared_no_s = _condition_blocks(phase_s, "no_connectivity")
    shared_m_r = _condition_blocks(phase_r, "allele_only_m010")
    shared_m_s = _condition_blocks(phase_s, "allele_only_m010")
    if shared_no_r != shared_no_s or shared_m_r != shared_m_s:
        raise RuntimeError("Phase R/S historical comparator blocks are no longer identical")

    condition_blocks = {
        "phase_u_m0": _phase_u_blocks(phase_u, 0.0),
        "phase_u_m010": _phase_u_blocks(phase_u, 0.1),
        "shared_historical_no_connectivity": shared_no_r,
        "shared_historical_allele_only_m010": shared_m_r,
        "phase_r_individual_d010": _condition_blocks(phase_r, "individual_dispersal_d010"),
        "phase_s_pollen_g020": _condition_blocks(phase_s, "pollen_only_g020"),
    }

    observed = {}
    for name, blocks in condition_blocks.items():
        statistic, df, pooled, total_n = pearson_statistic(blocks)
        observed[name] = {
            "total_n": total_n,
            "pooled_rate": pooled,
            "pearson_statistic": statistic,
            "df": df,
            "observed_w": sqrt(statistic / total_n),
        }

    precision = {}
    for total_n in (447, 452):
        w80 = minimum_detectable_w(total_n, 0.80)
        w90 = minimum_detectable_w(total_n, 0.90)
        precision[str(total_n)] = {
            "w_80": w80,
            "weighted_rms_pp_at_p0_5_80": 50.0 * w80,
            "w_90": w90,
            "weighted_rms_pp_at_p0_5_90": 50.0 * w90,
        }

    return {
        "analysis_type": "deterministic_post_result_precision_characterization",
        "opens_new_simulation": False,
        "changes_preregistered_decision": False,
        "alpha": 0.05,
        "df": 4,
        "critical_chi2": CRITICAL_CHI2_DF4_ALPHA05,
        "evidence_structure": {
            "independent_fresh_replications": 1,
            "shared_reference_operator_substitutions": 2,
            "phase_r_s_reference_blocks_identical": True,
        },
        "precision": precision,
        "observed": observed,
        "claim_boundary": "Precision-bounded null only; no equivalence margin was preregistered and smaller heterogeneity remains compatible with the data.",
    }


if __name__ == "__main__":
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
