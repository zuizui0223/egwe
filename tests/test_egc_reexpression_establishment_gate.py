"""Source-pinned distinction among first expression, repeated occupancy and joint-zero lock."""
from __future__ import annotations

import importlib.util
import math
import os
from pathlib import Path
from random import Random
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
SPEC=importlib.util.spec_from_file_location(
    "reexpression_establishment",ROOT/"scripts/egc_reexpression_establishment_gate.py")
assert SPEC and SPEC.loader
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


@pytest.fixture(scope="module")
def pinned():
    if not os.environ.get("EGC_PINNED_ROOT"):
        pytest.skip("actual pinned EGC is checked out only in dedicated GitHub Actions")
    return GATE.load_source()


def test_four_scenario_source_execution_and_fate_ceiling(pinned):
    result=GATE.run_experiment([50001,50002],horizon=4)
    assert set(result["scenarios"])=={
        "q0.20_p0.04","q0.20_p0.40","q0.80_p0.04","q0.80_p0.40"}
    assert result["pinned_egc_source_commit"]==GATE.PIN
    assert result["expression_not_biological_establishment"]
    assert result["stochastic_model_not_real_flower_data"]
    for value in result["scenarios"].values():
        cases=value["case_receipts"]
        summary=value["summary"]
        assert summary["n"]==2
        assert len(cases)==2
        assert cases[0]["initial_potential_viable_high"] == (
            value["initial_q"]>=.625)
        for case in cases:
            assert case["source_kernel_not_reconstructed"]
            assert 0<=case["exact_first_generation_expression_probability"]<=1
            assert (not case["three_consecutive_expressed_generations"]
                    or case["two_consecutive_expressed_generations"])
            assert (not case["two_consecutive_expressed_generations"]
                    or case["expressed_at_generation_1"])
            if case["first_joint_zero_generation"] is not None:
                assert case["joint_zero_at_end"]
                assert not case["final_expressed"]


def test_conditional_next_occurrence_matches_exact_source_multinomial(pinned):
    Params,run=pinned
    params=GATE.source_params(Params,1001,.2,.04,4)
    snapshots=run(params,mutation_rate=0.).snapshots
    p=GATE.conditional_high_next(params,snapshots[0],snapshots[1].population)
    from causal_model.multipatch_criticality_dynamics import update_trait_abundance
    first=tuple(20 if i==0 else 0 for i in range(params.trait_grid_size))
    N=snapshots[1].population[0]
    observed=0
    for seed in range(80001,82001):
        counts=update_trait_abundance(first,.2,.04,N,params,Random(seed))
        high=sum(c for i,c in enumerate(counts)
                 if i/(len(counts)-1)>=params.high_trait_cutoff)
        observed+=int(high>0)
    assert .05<p<.95
    assert abs(observed/2000-p)<.04


def test_latent_allele_and_q_are_causal_inputs_to_source_recruitment(pinned):
    Params,_=pinned
    from types import SimpleNamespace
    params=GATE.source_params(Params,9,.2,.04,3)
    absent=tuple(1. if i==0 else 0. for i in range(params.trait_grid_size))
    def state(q,p):
        return SimpleNamespace(
            trait_occupancy=[SimpleNamespace(distribution=absent)],
            high_allele_frequency=(p,),
            interaction=(q,),
        )
    p_zero=GATE.conditional_high_next(params,state(.2,0.),(20,))
    low=GATE.conditional_high_next(params,state(.2,.04),(20,))
    high=GATE.conditional_high_next(params,state(.8,.04),(20,))
    assert p_zero==0.
    assert 0<low<high<1.
    assert .5+.8*.2<1.
    assert .5+.8*.8>1.


@pytest.mark.parametrize("samples,horizon",[
    ([],12),([50001,50001],12),([50001],2),([50001],31)])
def test_invalid_sampling_contract_rejected(samples,horizon):
    with pytest.raises(ValueError):
        GATE.run_experiment(samples,horizon)


def test_model_state_classification_preserves_hidden_allele_vs_trait():
    from types import SimpleNamespace
    def s(h,p):
        return SimpleNamespace(
            trait_occupancy=[SimpleNamespace(high_trait_abundance=h)],
            high_allele_frequency=[p])
    assert GATE.observed_state(s(0,0)).startswith("joint_zero")
    assert GATE.observed_state(s(0,.4))=="unexpressed_with_latent_allele"
    assert GATE.observed_state(s(1,0))=="expressed_without_allele"
    assert GATE.observed_state(s(1,.4))=="expressed_with_allele"


def test_exact_source_stops_when_pinned_checkout_missing(monkeypatch):
    monkeypatch.delenv("EGC_PINNED_ROOT",raising=False)
    with pytest.raises(KeyError):
        GATE.run_experiment([50001],3)
