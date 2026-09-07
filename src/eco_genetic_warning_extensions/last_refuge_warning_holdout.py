from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import fmean, stdev
from typing import Any, Iterable

PROTOCOL_PATH = Path(__file__).resolve().parents[2] / "experiments" / "last_refuge_warning_holdout_protocol.json"
T_CRIT_DF11_95 = 2.200985160082949
HEADROOM_OFFSET = math.log(0.625 / 0.375) / 4.5


def load_protocol(path: str | Path = PROTOCOL_PATH) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("status") != "prospective_locked_before_implementation_and_outcomes":
        raise RuntimeError("last-refuge holdout is not prospectively locked")
    rep = payload["replication"]
    seeds = tuple(int(x) for x in rep["master_seeds"])
    if len(seeds) != 12 or len(set(seeds)) != 12:
        raise RuntimeError("holdout requires exactly 12 distinct master seeds")
    if int(rep["replicates_per_seed"]) != 500 or int(rep["total_trajectories"]) != 12000:
        raise RuntimeError("holdout replication contract drifted")
    forcing = payload["forcing"]
    if int(forcing["observation_generation"]) != 10 or int(forcing["endpoint_generation"]) != 40:
        raise RuntimeError("holdout time contract drifted")
    return payload


def _assignment(kind: str) -> tuple[float, ...]:
    values = (0.20, 0.40, 0.60, 0.80)
    if kind == "AA":
        return values
    if kind == "RR":
        return tuple(reversed(values))
    raise ValueError(kind)


def _trait_abundance(values: tuple[float, ...], grid_size: int = 31) -> tuple[tuple[int, ...], ...]:
    rows: list[tuple[int, ...]] = []
    for fraction in values:
        high = int(round(40 * fraction))
        row = [0] * grid_size
        row[0] = 40 - high
        row[-1] = high
        rows.append(tuple(row))
    return tuple(rows)


def _seed(master_seed: int, replicate: int) -> int:
    return (master_seed * 1_000_003 + replicate * 103 + 71) % (2**31 - 1)


def barrier_schedule(generations: int) -> tuple[float, ...]:
    return tuple(0.50 + 0.15 * generation / 60.0 for generation in range(1, generations + 1))


def _parameters(assignment: str, seed: int, generations: int):
    from causal_model.multipatch_criticality_dynamics import DynamicsParameters

    values = _assignment(assignment)
    return DynamicsParameters(
        patch_areas=(1.0, 1.0, 1.0, 1.0),
        generations=generations,
        initial_population=(40, 40, 40, 40),
        initial_interaction=(0.65, 0.75, 0.85, 0.95),
        initial_high_allele_frequency=values,
        initial_trait_abundance=_trait_abundance(values),
        density_capacity=40.0,
        area_reference=1.0,
        interaction_feedback=4.5,
        interaction_barrier=0.50,
        trait_grid_size=31,
        trait_occupancy_mode="finite_trait_bin_recruitment",
        genotype_trait_recruitment="two_kernel_recruitment",
        inheritance_weight=0.5,
        q_feedback_alpha=0.6,
        q_feedback_beta_trait=0.3,
        q_feedback_gamma_allele=0.1,
        migration_rate=0.0,
        random_seed=seed,
    )


def patch_route_margin(q: float, trait_mass: float, allele_frequency: float, density: float, theta: float) -> float:
    support = 0.6 * q + 0.3 * trait_mass + 0.1 * allele_frequency
    return density * support - (theta + HEADROOM_OFFSET)


def _trajectory_record(protocol: dict[str, Any], assignment: str, master_seed: int, replicate: int) -> dict[str, Any]:
    from causal_model.multipatch_criticality_dynamics import sigmoid, tau_trait_realised
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
    observed_next = result.snapshots[observation_generation]
    theta = barriers[observation_generation - 1]
    carrying = tuple(params.density_capacity * area for area in params.patch_areas)
    density = tuple(min(1.0, n / k) for n, k in zip(current.population, carrying))
    trait_mass = tuple(x.high_trait_mass for x in current.trait_occupancy)
    margins = tuple(
        patch_route_margin(q, t, g, d, theta)
        for q, t, g, d in zip(current.interaction, trait_mass, current.high_allele_frequency, density)
    )

    predicted_next = tuple(sigmoid(4.5 * (margin + HEADROOM_OFFSET)) for margin in margins)
    max_abs_q_audit_error = max(abs(a - b) for a, b in zip(predicted_next, observed_next.interaction))
    if max_abs_q_audit_error > 1e-12:
        raise RuntimeError(
            f"co-timed route-margin audit failed assignment={assignment} seed={seed}: {max_abs_q_audit_error}"
        )

    loss_time = tau_trait_realised(result)
    endpoint = int(forcing["endpoint_generation"])
    event = bool(loss_time is not None and int(loss_time) <= endpoint)
    already_lost = bool(loss_time is not None and int(loss_time) <= snapshot_generation)

    return {
        "assignment": assignment,
        "master_seed": int(master_seed),
        "replicate": int(replicate),
        "trajectory_seed": int(seed),
        "observation_snapshot_generation": int(snapshot_generation),
        "loss_time": None if loss_time is None else int(loss_time),
        "loss_by_generation_40": event,
        "loss_already_occurred_by_observation": already_lost,
        "max_route_margin": float(max(margins)),
        "max_q": float(max(current.interaction)),
        "mean_q": float(fmean(current.interaction)),
        "mean_population": float(fmean(current.population)),
        "H_alpha": float(current.h_alpha),
        "H_gamma": float(current.h_gamma),
        "max_abs_q_audit_error": float(max_abs_q_audit_error),
    }


def simulate(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    rep = protocol["replication"]
    for master_seed in (int(x) for x in rep["master_seeds"]):
        for replicate in range(int(rep["replicates_per_seed"])):
            for assignment in ("AA", "RR"):
                records.append(_trajectory_record(protocol, assignment, master_seed, replicate))
    if len(records) != int(rep["total_trajectories"]):
        raise RuntimeError("holdout trajectory count mismatch")
    return records


def roc_auc(risks: Iterable[float], events: Iterable[bool]) -> float:
    pairs = [(float(score), bool(event)) for score, event in zip(risks, events)]
    n_pos = sum(event for _, event in pairs)
    n_neg = len(pairs) - n_pos
    if n_pos == 0 or n_neg == 0:
        raise ValueError("ROC AUC requires both event and non-event observations")
    ordered = sorted(pairs, key=lambda x: x[0])
    rank_sum_pos = 0.0
    i = 0
    while i < len(ordered):
        j = i + 1
        while j < len(ordered) and ordered[j][0] == ordered[i][0]:
            j += 1
        average_rank = ((i + 1) + j) / 2.0
        rank_sum_pos += average_rank * sum(event for _, event in ordered[i:j])
        i = j
    u = rank_sum_pos - n_pos * (n_pos + 1) / 2.0
    return u / (n_pos * n_neg)


def _block_summary(values: list[float]) -> dict[str, Any]:
    if len(values) != 12:
        raise RuntimeError("primary uncertainty requires 12 master-seed blocks")
    mean = fmean(values)
    se = stdev(values) / math.sqrt(len(values))
    half = T_CRIT_DF11_95 * se
    return {
        "mean": float(mean),
        "ci95": [float(mean - half), float(mean + half)],
        "n_master_seed_blocks": len(values),
        "block_values": [float(x) for x in values],
    }


def _risk(record: dict[str, Any], metric: str) -> float:
    # Every predeclared candidate/comparator has lower state = higher future risk.
    return -float(record[metric])


def _seed_block_aucs(records: list[dict[str, Any]], metric: str) -> dict[int, float]:
    out: dict[int, float] = {}
    for master_seed in sorted({int(r["master_seed"]) for r in records}):
        block = [r for r in records if int(r["master_seed"]) == master_seed]
        out[master_seed] = roc_auc(
            (_risk(r, metric) for r in block),
            (bool(r["loss_by_generation_40"]) for r in block),
        )
    return out


def _condition_auc(records: list[dict[str, Any]], assignment: str, metric: str) -> float:
    selected = [r for r in records if r["assignment"] == assignment]
    return roc_auc(
        (_risk(r, metric) for r in selected),
        (bool(r["loss_by_generation_40"]) for r in selected),
    )


def _event_score_summary(records: list[dict[str, Any]], metric: str) -> dict[str, float]:
    events = [float(r[metric]) for r in records if r["loss_by_generation_40"]]
    non_events = [float(r[metric]) for r in records if not r["loss_by_generation_40"]]
    return {
        "event_mean": float(fmean(events)),
        "non_event_mean": float(fmean(non_events)),
        "difference_event_minus_non_event": float(fmean(events) - fmean(non_events)),
    }


def summarise(protocol: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = {
        "max_route_margin": "continuous_last_refuge_route_margin",
        "max_q": "co_timed_max_q",
        "mean_q": "co_timed_mean_q",
        "mean_population": "co_timed_mean_population",
        "H_alpha": "co_timed_H_alpha",
        "H_gamma": "co_timed_H_gamma",
    }
    block_aucs: dict[str, dict[int, float]] = {
        metric: _seed_block_aucs(records, metric) for metric in metrics
    }
    aucs = {
        label: {
            **_block_summary(list(block_aucs[metric].values())),
            "pooled_auc": float(
                roc_auc(
                    (_risk(r, metric) for r in records),
                    (bool(r["loss_by_generation_40"]) for r in records),
                )
            ),
            "AA_auc": float(_condition_auc(records, "AA", metric)),
            "RR_auc": float(_condition_auc(records, "RR", metric)),
            "score_summary": _event_score_summary(records, metric),
        }
        for metric, label in metrics.items()
    }

    margin_blocks = block_aucs["max_route_margin"]
    q_blocks = block_aucs["max_q"]
    paired_differences = [margin_blocks[seed] - q_blocks[seed] for seed in sorted(margin_blocks)]
    incremental = _block_summary(paired_differences)

    events = [r for r in records if r["loss_by_generation_40"]]
    non_events = [r for r in records if not r["loss_by_generation_40"]]
    already = sum(bool(r["loss_already_occurred_by_observation"]) for r in events)
    timeliness_fraction = already / len(events) if events else None

    primary = aucs["continuous_last_refuge_route_margin"]
    confirmed = bool(
        primary["ci95"][0] > 0.75
        and timeliness_fraction is not None
        and timeliness_fraction < 0.05
    )
    adds_beyond_q = bool(incremental["ci95"][0] > 0.0)
    if not confirmed:
        decision = "candidate_not_confirmed"
    elif adds_beyond_q:
        decision = "confirmed_route_margin_adds_ranking_beyond_q"
    else:
        decision = "confirmed_discriminator_without_incremental_ranking_over_q"

    max_audit_error = max(float(r["max_abs_q_audit_error"]) for r in records)
    return {
        "experiment_id": protocol["experiment_id"],
        "status": "completed_from_prospectively_locked_holdout",
        "n_records": len(records),
        "events": len(events),
        "non_events": len(non_events),
        "event_prevalence": len(events) / len(records),
        "observation_snapshot_generation": int(protocol["forcing"]["observation_generation"]) - 1,
        "max_route_transition_audit_error": max_audit_error,
        "auc_by_predeclared_score": aucs,
        "route_margin_minus_co_timed_max_q_auc": incremental,
        "timeliness": {
            "eventual_g40_losses": len(events),
            "already_lost_by_observation": already,
            "fraction": timeliness_fraction,
            "required_upper_bound": 0.05,
        },
        "decision": decision,
        "claim_ceiling": protocol["claim_ceiling"],
    }


def run(protocol_path: str | Path = PROTOCOL_PATH) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    protocol = load_protocol(protocol_path)
    records = simulate(protocol)
    return summarise(protocol, records), records


def write(summary_path: str | Path, records_path: str | Path, protocol_path: str | Path = PROTOCOL_PATH) -> None:
    summary, records = run(protocol_path)
    summary_dest = Path(summary_path)
    records_dest = Path(records_path)
    summary_dest.parent.mkdir(parents=True, exist_ok=True)
    records_dest.parent.mkdir(parents=True, exist_ok=True)
    summary_dest.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    records_dest.write_text(json.dumps(records, separators=(",", ":")) + "\n", encoding="utf-8")
