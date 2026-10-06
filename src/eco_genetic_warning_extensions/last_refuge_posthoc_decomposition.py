from __future__ import annotations

import json
from pathlib import Path
from statistics import fmean
from typing import Any, Iterable

from eco_genetic_warning_extensions.last_refuge_warning_holdout import (
    HEADROOM_OFFSET,
    _block_summary,
    _parameters,
    _seed,
    barrier_schedule,
    load_protocol,
    patch_route_margin,
    roc_auc,
)

ANALYSIS_ID = "last_refuge_posthoc_component_decomposition_v1"
ANALYSIS_STATUS = "post_hoc_exploratory_not_preregistered"


def patch_component_scores(
    q: float,
    trait_mass: float,
    allele_frequency: float,
    density: float,
    theta: float,
) -> dict[str, float]:
    """Return the post-hoc score components without changing the locked predictor."""
    support = 0.6 * q + 0.3 * trait_mass + 0.1 * allele_frequency
    return {
        "q": float(q),
        "density_q": float(density * q),
        "support_no_density": float(support),
        "route_margin": float(patch_route_margin(q, trait_mass, allele_frequency, density, theta)),
        "density": float(density),
    }


def _argmax_first(values: Iterable[float]) -> int:
    values = tuple(float(x) for x in values)
    if not values:
        raise ValueError("argmax requires at least one value")
    return max(range(len(values)), key=values.__getitem__)


def _trajectory_record(
    protocol: dict[str, Any],
    assignment: str,
    master_seed: int,
    replicate: int,
) -> dict[str, Any]:
    from causal_model.multipatch_criticality_dynamics import tau_trait_realised
    from causal_model.symmetric_allele_mutation_closure import simulate_with_symmetric_allele_mutation

    forcing = protocol["forcing"]
    generations = int(forcing["generations"])
    observation_generation = int(forcing["observation_generation"])
    snapshot_generation = observation_generation - 1
    seed = _seed(master_seed, replicate)
    params = _parameters(assignment, seed, generations)
    barriers = barrier_schedule(generations)
    result = simulate_with_symmetric_allele_mutation(
        params,
        mutation_rate=0.0,
        interaction_barrier_schedule=barriers,
    )

    current = result.snapshots[snapshot_generation]
    theta = barriers[observation_generation - 1]
    carrying = tuple(params.density_capacity * area for area in params.patch_areas)
    density = tuple(min(1.0, n / k) for n, k in zip(current.population, carrying))
    trait_mass = tuple(x.high_trait_mass for x in current.trait_occupancy)

    patches = tuple(
        patch_component_scores(q, t, g, d, theta)
        for q, t, g, d in zip(
            current.interaction,
            trait_mass,
            current.high_allele_frequency,
            density,
        )
    )
    q_values = tuple(p["q"] for p in patches)
    density_q_values = tuple(p["density_q"] for p in patches)
    support_values = tuple(p["support_no_density"] for p in patches)
    margin_values = tuple(p["route_margin"] for p in patches)

    loss_time = tau_trait_realised(result)
    endpoint = int(forcing["endpoint_generation"])
    event = bool(loss_time is not None and int(loss_time) <= endpoint)

    return {
        "assignment": assignment,
        "master_seed": int(master_seed),
        "replicate": int(replicate),
        "trajectory_seed": int(seed),
        "loss_by_generation_40": event,
        "max_q": float(max(q_values)),
        "max_density_q": float(max(density_q_values)),
        "max_support_no_density": float(max(support_values)),
        "max_route_margin": float(max(margin_values)),
        "argmax_q": int(_argmax_first(q_values)),
        "argmax_route_margin": int(_argmax_first(margin_values)),
        "all_patch_density_below_one": bool(all(p["density"] < 1.0 for p in patches)),
    }


def simulate(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    """Re-run the exact locked holdout ensemble for exploratory score decomposition."""
    records: list[dict[str, Any]] = []
    rep = protocol["replication"]
    for master_seed in (int(x) for x in rep["master_seeds"]):
        for replicate in range(int(rep["replicates_per_seed"])):
            for assignment in ("AA", "RR"):
                records.append(_trajectory_record(protocol, assignment, master_seed, replicate))
    if len(records) != int(rep["total_trajectories"]):
        raise RuntimeError("post-hoc decomposition trajectory count mismatch")
    return records


def _risk(record: dict[str, Any], metric: str) -> float:
    # Keep the frozen holdout orientation: lower state means higher future-loss risk.
    return -float(record[metric])


def _seed_block_aucs(records: list[dict[str, Any]], metric: str) -> dict[int, float]:
    out: dict[int, float] = {}
    for master_seed in sorted({int(r["master_seed"]) for r in records}):
        block = [r for r in records if int(r["master_seed"]) == master_seed]
        out[master_seed] = roc_auc(
            (_risk(r, metric) for r in block),
            (bool(r["loss_by_generation_40"]) for r in block),
        )
    if len(out) != 12:
        raise RuntimeError("post-hoc decomposition requires 12 master-seed blocks")
    return out


def _auc_summary(records: list[dict[str, Any]], metric: str) -> dict[str, Any]:
    blocks = _seed_block_aucs(records, metric)
    values = [blocks[seed] for seed in sorted(blocks)]
    summary = _block_summary(values)
    return {
        "mean_seed_block_auc": summary["mean"],
        "ci95": summary["ci95"],
        "block_values": summary["block_values"],
        "pooled_auc": float(
            roc_auc(
                (_risk(r, metric) for r in records),
                (bool(r["loss_by_generation_40"]) for r in records),
            )
        ),
    }


def _paired_auc_difference(
    records: list[dict[str, Any]],
    numerator_metric: str,
    denominator_metric: str,
) -> dict[str, Any]:
    a = _seed_block_aucs(records, numerator_metric)
    b = _seed_block_aucs(records, denominator_metric)
    seeds = sorted(a)
    differences = [a[seed] - b[seed] for seed in seeds]
    summary = _block_summary(differences)
    positive = sum(x > 0.0 for x in differences)
    return {
        "mean": summary["mean"],
        "ci95": summary["ci95"],
        "block_values": summary["block_values"],
        "positive_blocks": positive,
        "all_blocks_positive": positive == len(differences),
    }


def summarise(protocol: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = (
        "max_q",
        "max_density_q",
        "max_support_no_density",
        "max_route_margin",
    )
    auc = {metric: _auc_summary(records, metric) for metric in metrics}
    same_argmax = sum(
        int(r["argmax_q"]) == int(r["argmax_route_margin"]) for r in records
    )
    density_violations = sum(not bool(r["all_patch_density_below_one"]) for r in records)
    events = sum(bool(r["loss_by_generation_40"]) for r in records)

    return {
        "analysis_id": ANALYSIS_ID,
        "analysis_status": ANALYSIS_STATUS,
        "preregistration_role": (
            "Exploratory decomposition conducted after the prospectively locked "
            "max-route-margin versus max-q comparison was opened. It must not be "
            "used to redefine or upgrade the preregistered primary estimand."
        ),
        "source_experiment_id": protocol["experiment_id"],
        "n_records": len(records),
        "events": events,
        "non_events": len(records) - events,
        "auc": auc,
        "paired_auc_differences": {
            "density_only_max_dq_minus_max_q": _paired_auc_difference(
                records, "max_density_q", "max_q"
            ),
            "trait_genetic_support_max_S_minus_max_q": _paired_auc_difference(
                records, "max_support_no_density", "max_q"
            ),
            "trait_genetic_support_added_on_density_max_M_minus_max_dq": _paired_auc_difference(
                records, "max_route_margin", "max_density_q"
            ),
            "density_added_on_support_max_M_minus_max_S": _paired_auc_difference(
                records, "max_route_margin", "max_support_no_density"
            ),
        },
        "argmax_route_margin_equals_argmax_q": {
            "count": same_argmax,
            "fraction": float(same_argmax / len(records)),
        },
        "observation_density": {
            "all_trajectories_have_all_patch_density_below_one": density_violations == 0,
            "trajectory_violations": density_violations,
        },
        "interpretation_ceiling": (
            "This decomposition diagnoses where the incremental ranking in this fixed "
            "holdout comes from. It does not create a new preregistered comparator, "
            "prove causal attribution of AUC gain, or establish portability beyond "
            "the declared finite closure."
        ),
    }


def run(protocol_path: str | Path | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    protocol = load_protocol() if protocol_path is None else load_protocol(protocol_path)
    records = simulate(protocol)
    return summarise(protocol, records), records


def write(
    summary_path: str | Path,
    records_path: str | Path | None = None,
    protocol_path: str | Path | None = None,
) -> None:
    summary, records = run(protocol_path)
    summary_dest = Path(summary_path)
    summary_dest.parent.mkdir(parents=True, exist_ok=True)
    summary_dest.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if records_path is not None:
        records_dest = Path(records_path)
        records_dest.parent.mkdir(parents=True, exist_ok=True)
        records_dest.write_text(json.dumps(records, separators=(",", ":")) + "\n", encoding="utf-8")
