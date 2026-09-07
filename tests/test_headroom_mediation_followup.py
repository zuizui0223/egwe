from __future__ import annotations

import json
from pathlib import Path

from eco_genetic_warning_extensions.headroom_mediation_followup import (
    _did_from_pair_maps,
    _simulate_one_headroom,
    load_protocol,
)
from eco_genetic_warning_extensions.pathway_edge_decomposition import _simulate_one


def test_protocol_is_locked_and_fresh() -> None:
    protocol = load_protocol()
    assert protocol["experiment_id"] == "headroom_mediation_followup_v1"
    assert protocol["status"] == "prospective_locked_before_run"
    assert protocol["starting_main_commit"] == "ad6df58fa19e990f4b824173a1b3f344bfb1b7fa"
    assert protocol["primary_endpoint"]["horizon"] == 40
    assert protocol["primary_mediator"]["horizon"] == 20
    assert protocol["primary_mediator"]["metric"] == "maximum patchwise pre-update branch headroom H across the four patches"
    assert tuple(protocol["conditions"]) == (
        "baseline_local_allele_selection",
        "delete_local_allele_selection",
    )
    seeds = tuple(protocol["replication"]["master_seeds"])
    assert len(seeds) == 12
    assert len(set(seeds)) == 12
    assert protocol["replication"]["replicates_per_seed"] == 500
    assert protocol["replication"]["pairs_per_condition"] == 6000
    assert protocol["replication"]["total_trajectories"] == 24000


def test_instrumented_simulator_matches_existing_dynamics() -> None:
    protocol = load_protocol()
    master_seed = int(protocol["replication"]["master_seeds"][0])
    replicate = 0
    for proof_condition, intervention in protocol["conditions"].items():
        for assignment in ("AA", "RR"):
            new = _simulate_one_headroom(
                protocol,
                proof_condition,
                intervention,
                assignment,
                master_seed,
                replicate,
            )
            old = _simulate_one(
                protocol,
                proof_condition,
                intervention,
                assignment,
                master_seed,
                replicate,
                intervention_index=0,
            )
            assert new["trajectory_seed"] == old["trajectory_seed"]
            assert new["last_refuge_loss_time"] == old["last_refuge_loss_time"]
            for horizon in (1, 5, 10, 20, 40):
                assert new["states"][str(horizon)]["mean_q"] == old["states"][str(horizon)]["mean_q"]
                assert new["states"][str(horizon)]["max_q"] == old["states"][str(horizon)]["max_q"]
                assert new["states"][str(horizon)]["mean_population"] == old["states"][str(horizon)]["mean_population"]


def test_headroom_recording_uses_only_exact_zero_surface() -> None:
    protocol = load_protocol()
    master_seed = int(protocol["replication"]["master_seeds"][1])
    record = _simulate_one_headroom(
        protocol,
        "baseline_local_allele_selection",
        protocol["conditions"]["baseline_local_allele_selection"],
        "AA",
        master_seed,
        1,
    )
    for horizon in (1, 5, 10, 20, 40):
        state = record["states"][str(horizon)]
        vec = tuple(float(x) for x in state["headroom_vector"])
        assert state["max_headroom"] == max(vec)
        assert state["positive_headroom_count"] == sum(x > 0.0 for x in vec)
        assert 0 <= state["positive_headroom_count"] <= 4


def test_did_helper_is_direction_agnostic() -> None:
    positive = _did_from_pair_maps({(1, 1): 1.0, (1, 2): 0.5}, {(1, 1): 0.0, (1, 2): 0.0})
    negative = _did_from_pair_maps({(1, 1): 0.0, (1, 2): 0.0}, {(1, 1): 1.0, (1, 2): 0.5})
    assert positive["DID"] > 0
    assert negative["DID"] < 0
    assert positive["n_paired_keys"] == negative["n_paired_keys"] == 2


def test_protocol_forbids_post_result_search() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = json.loads((root / "experiments" / "headroom_mediation_followup_protocol.json").read_text())
    stop = payload["stop_rule"].casefold()
    for phrase in (
        "do not add seeds",
        "alternative headroom thresholds",
        "alternative primary horizons",
        "alternative endpoint definitions",
        "new interventions",
    ):
        assert phrase in stop
