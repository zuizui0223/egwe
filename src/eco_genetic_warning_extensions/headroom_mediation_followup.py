from __future__ import annotations

import json
from math import exp
from pathlib import Path
from random import Random
from statistics import fmean
from typing import Any

from eco_genetic_warning_extensions.branching_headroom_theorem import switch_offset
from eco_genetic_warning_extensions.pathway_edge_decomposition import (
    _condition_values,
    _loss_indicator,
    _mean_ci,
    _parameters,
    _seed,
    _trait_update,
    barrier_schedule,
)

PROTOCOL_PATH = Path(__file__).resolve().parents[2] / "experiments" / "headroom_mediation_followup_protocol.json"


def load_protocol(path: str | Path = PROTOCOL_PATH) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("status") != "prospective_locked_before_run":
        raise RuntimeError("headroom mediation protocol is not prospectively locked")
    if tuple(payload.get("conditions", {})) != (
        "baseline_local_allele_selection",
        "delete_local_allele_selection",
    ):
        raise RuntimeError("headroom mediation follow-up requires exactly two locked conditions")
    if int(payload["replication"]["pairs_per_condition"]) != 6000:
        raise RuntimeError("headroom mediation follow-up requires exactly 6000 paired keys per condition")
    if int(payload["primary_endpoint"]["horizon"]) != 40:
        raise RuntimeError("primary endpoint horizon drifted")
    if int(payload["primary_mediator"]["horizon"]) != 20:
        raise RuntimeError("primary mediator horizon drifted")
    return payload


def _trajectory_seed(master_seed: int, replicate: int) -> int:
    return _seed(master_seed, replicate, 0)


def _simulate_one_headroom(
    protocol: dict[str, Any],
    proof_condition: str,
    intervention: dict[str, Any],
    assignment: str,
    master_seed: int,
    replicate: int,
) -> dict[str, Any]:
    from causal_model.multipatch_criticality_dynamics import (
        SimulationResult,
        _binomial,
        _effective_size,
        _initial_values,
        _normalise_distribution,
        _snapshot,
        sigmoid,
        tau_trait_realised,
        trait_fitness,
    )

    generations = int(protocol["forcing"]["generations"])
    horizons = tuple(int(x) for x in protocol["forcing"]["report_horizons"])
    barriers = barrier_schedule(generations)
    seed = _trajectory_seed(master_seed, replicate)
    params = _parameters(protocol, intervention, assignment, seed, generations)
    rng = Random(seed)
    population, interaction, frequency, trait_distribution, trait_abundance = _initial_values(params)
    snapshots = [_snapshot(0, population, interaction, frequency, trait_distribution, trait_abundance, params)]

    headroom_by_generation: dict[str, dict[str, Any]] = {}
    first_all_negative: int | None = None
    c_star = switch_offset()

    for generation in range(1, generations + 1):
        barrier = barriers[generation - 1]
        carrying = tuple(params.density_capacity * area for area in params.patch_areas)
        density = tuple(min(1.0, n / k) for n, k in zip(population, carrying))
        headrooms = tuple(dens * q - barrier - c_star for dens, q in zip(density, interaction))
        if first_all_negative is None and all(h < 0.0 for h in headrooms):
            first_all_negative = generation
        if generation in horizons:
            headroom_by_generation[str(generation)] = {
                "mean_headroom": fmean(headrooms),
                "max_headroom": max(headrooms),
                "positive_headroom_count": sum(h > 0.0 for h in headrooms),
                "headroom_vector": headrooms,
            }

        q_next = tuple(
            sigmoid(params.interaction_feedback * ((area / params.area_reference) * dens * q - barrier))
            for area, dens, q in zip(params.patch_areas, density, interaction)
        )

        q_for_allele = q_next
        if str(intervention["allele_selection_mode"]) == "spatial_mean_q":
            mean_q = fmean(q_next)
            q_for_allele = tuple(mean_q for _ in q_next)

        selected_allele: list[float] = []
        for q_sel, p in zip(q_for_allele, frequency):
            high_margin = trait_fitness(1.0, q_sel, params) - params.viability_threshold
            high_fitness = max(1e-12, 1.0 + params.selection_strength * high_margin)
            mean_fitness = p * high_fitness + (1.0 - p)
            selected_allele.append(p * high_fitness / mean_fitness)

        next_population: list[int] = []
        carrying = tuple(params.density_capacity * area for area in params.patch_areas)
        for n, k, q, p_selected in zip(population, carrying, q_next, selected_allele):
            exponent = params.baseline_growth + params.interaction_growth * q + params.high_allele_growth * p_selected - n / k
            next_population.append(max(1, round(n * exp(exponent))))

        q_for_trait = interaction
        if str(intervention["trait_selection_mode"]) == "spatial_mean_q":
            mean_q_trait = fmean(interaction)
            q_for_trait = tuple(mean_q_trait for _ in interaction)

        next_trait_abundance = tuple(
            _trait_update(abundance, q_sel, p, n_next, params, rng)
            for abundance, q_sel, p, n_next in zip(trait_abundance, q_for_trait, frequency, next_population)
        )
        next_trait_distribution = tuple(_normalise_distribution(row) for row in next_trait_abundance)

        next_frequency: list[float] = []
        for n, q, p in zip(next_population, q_next, selected_allele):
            n_eff = _effective_size(n, q, params)
            gene_copies = max(2, round(2.0 * n_eff))
            next_frequency.append(_binomial(rng, gene_copies, p) / gene_copies)

        population = tuple(next_population)
        interaction = tuple(q_next)
        frequency = tuple(next_frequency)
        trait_distribution = next_trait_distribution
        trait_abundance = next_trait_abundance
        snapshots.append(_snapshot(generation, population, interaction, frequency, trait_distribution, trait_abundance, params))

    result = SimulationResult(params, tuple(snapshots))
    loss_time = tau_trait_realised(result)
    states: dict[str, Any] = {}
    for horizon in horizons:
        snap = result.snapshots[horizon]
        states[str(horizon)] = {
            **headroom_by_generation[str(horizon)],
            "mean_population": fmean(snap.population),
            "mean_q": fmean(snap.interaction),
            "max_q": max(snap.interaction),
        }

    return {
        "intervention": proof_condition,
        "condition": assignment,
        "master_seed": int(master_seed),
        "replicate": int(replicate),
        "trajectory_seed": int(seed),
        "last_refuge_loss_time": None if loss_time in {None, 0} else int(loss_time),
        "first_all_negative_headroom_generation": first_all_negative,
        "states": states,
    }


def simulate(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    rep = protocol["replication"]
    for master_seed in (int(x) for x in rep["master_seeds"]):
        for replicate in range(int(rep["replicates_per_seed"])):
            for proof_condition, intervention in protocol["conditions"].items():
                for assignment in ("AA", "RR"):
                    records.append(
                        _simulate_one_headroom(
                            protocol,
                            proof_condition,
                            intervention,
                            assignment,
                            master_seed,
                            replicate,
                        )
                    )
    return records


def _paired_loss_effects(records: list[dict[str, Any]], proof_condition: str, horizon: int) -> dict[tuple[int, int], int]:
    by = {
        (r["condition"], int(r["master_seed"]), int(r["replicate"])): r
        for r in records
        if r["intervention"] == proof_condition
    }
    keys = sorted((master, rep) for condition, master, rep in by if condition == "AA")
    return {
        key: _loss_indicator(by[("RR", *key)], horizon) - _loss_indicator(by[("AA", *key)], horizon)
        for key in keys
    }


def _paired_metric_effects(
    records: list[dict[str, Any]], proof_condition: str, horizon: int, metric: str
) -> dict[tuple[int, int], float]:
    by = {
        (r["condition"], int(r["master_seed"]), int(r["replicate"])): r
        for r in records
        if r["intervention"] == proof_condition
    }
    keys = sorted((master, rep) for condition, master, rep in by if condition == "AA")
    return {
        key: float(by[("AA", *key)]["states"][str(horizon)][metric])
        - float(by[("RR", *key)]["states"][str(horizon)][metric])
        for key in keys
    }


def _did_from_pair_maps(baseline: dict[tuple[int, int], float], deletion: dict[tuple[int, int], float]) -> dict[str, Any]:
    if baseline.keys() != deletion.keys():
        raise RuntimeError("baseline and deletion paired keys differ")
    values = [baseline[key] - deletion[key] for key in baseline]
    effect, ci = _mean_ci(values)
    return {"n_paired_keys": len(values), "DID": effect, "paired_ci95": ci}


def summarise(protocol: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    endpoint_horizon = int(protocol["primary_endpoint"]["horizon"])
    mediator_horizon = int(protocol["primary_mediator"]["horizon"])

    baseline_loss = _paired_loss_effects(records, "baseline_local_allele_selection", endpoint_horizon)
    deletion_loss = _paired_loss_effects(records, "delete_local_allele_selection", endpoint_horizon)
    loss_did = _did_from_pair_maps(baseline_loss, deletion_loss)

    baseline_h = _paired_metric_effects(records, "baseline_local_allele_selection", mediator_horizon, "max_headroom")
    deletion_h = _paired_metric_effects(records, "delete_local_allele_selection", mediator_horizon, "max_headroom")
    headroom_did = _did_from_pair_maps(baseline_h, deletion_h)

    loss_positive = float(loss_did["paired_ci95"][0]) > 0.0
    headroom_positive = float(headroom_did["paired_ci95"][0]) > 0.0
    decision = "resolved_selection_headroom_fate_pathway" if loss_positive and headroom_positive else "unresolved_stop"

    secondary: dict[str, Any] = {}
    for horizon in (5, 10, 20, 40):
        secondary[str(horizon)] = {}
        for metric in ("max_headroom", "mean_headroom", "positive_headroom_count", "mean_population"):
            b = _paired_metric_effects(records, "baseline_local_allele_selection", horizon, metric)
            d = _paired_metric_effects(records, "delete_local_allele_selection", horizon, metric)
            secondary[str(horizon)][metric] = {
                "baseline_AA_minus_RR": _mean_ci(b.values()),
                "deletion_AA_minus_RR": _mean_ci(d.values()),
                "baseline_minus_deletion_DID": _did_from_pair_maps(b, d),
            }

    return {
        "experiment_id": protocol["experiment_id"],
        "status": "completed_from_locked_protocol",
        "primary_generation_40_loss_DID": loss_did,
        "primary_generation_20_max_headroom_DID": headroom_did,
        "decision": decision,
        "secondary": secondary,
        "claim_boundary": protocol["claim_boundary"],
        "stop_rule": protocol["stop_rule"],
    }


def run(protocol_path: str | Path = PROTOCOL_PATH) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    protocol = load_protocol(protocol_path)
    records = simulate(protocol)
    return summarise(protocol, records), records


def write(summary_path: str | Path, records_path: str | Path, protocol_path: str | Path = PROTOCOL_PATH) -> None:
    summary, records = run(protocol_path)
    summary_path = Path(summary_path)
    records_path = Path(records_path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    records_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    records_path.write_text(json.dumps(records, separators=(",", ":")) + "\n", encoding="utf-8")
