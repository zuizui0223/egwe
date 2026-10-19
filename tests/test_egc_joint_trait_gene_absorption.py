"""Source-locked joint genetic/phenotypic loss classification."""
from __future__ import annotations

import importlib.util
import math
import os
from pathlib import Path
from random import Random
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0,str(SCRIPTS))
SPEC=importlib.util.spec_from_file_location(
    "joint_gene_trait_absorption",SCRIPTS/"egc_joint_trait_gene_absorption.py")
assert SPEC and SPEC.loader
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


@pytest.fixture(scope="module")
def pinned():
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("requires source-locked EGC checkout in dedicated CI")
    return MOD.load_source()


def test_same_visible_trait_absence_different_resident_gene_changes_recovery(pinned):
    value=MOD.joint_absence_witness()
    assert value["same_visible_trait_state"] is True
    assert value["same_interaction_and_population"] is True
    assert value["resident_allele_state_differs"] is True
    assert value["allele_zero_one_step_reappearance_probability"]==0
    assert 0<value["allele_present_one_step_reappearance_probability"]<1
    assert value["high_trait_performance_at_q"]<value["high_trait_viability_threshold"]
    assert value["full_ecological_fate_probability_computed"] is False
    assert value["anthocyanin_reactivation_in_nature_tested"] is False


def test_exact_mutant_unlock_probability_from_pinned_gene_copy_count(pinned):
    Params,_=pinned
    params=Params(patch_areas=(1.,),generations=2)
    result=MOD.mutation_unlock_probability(params,[20],[.2],.02)
    assert result["gene_copies_by_patch"]==[24]
    assert result["total_gene_copies"]==24
    assert result["probability_any_mutant_allele_after_drift"]==pytest.approx(
        1-.98**24,abs=1e-14)
    assert result["probability_high_trait_returns_during_this_generation"]==0
    assert result["phenotypic_reappearance_can_begin_next_recruitment_only"]
    zero=MOD.mutation_unlock_probability(params,[20],[.2],0.)
    assert zero["probability_any_mutant_allele_after_drift"]==0
    assert zero["phenotypic_reappearance_can_begin_next_recruitment_only"] is False


def test_exact_mutation_unlock_matches_source_binomial_draws(pinned):
    from causal_model.multipatch_criticality_dynamics import _binomial
    Params,_=pinned
    params=Params(patch_areas=(1.,),generations=2)
    source=MOD.mutation_unlock_probability(params,[20],[.2],.02)
    copies=source["gene_copies_by_patch"][0]
    n=3000
    observed=sum(_binomial(Random(seed),copies,.02)>0
                 for seed in range(50001,50001+n))
    assert abs(observed/n-source["probability_any_mutant_allele_after_drift"])<.03


def test_without_mutation_joint_gene_and_trait_absence_is_absorbing(pinned):
    Params,run=pinned
    params=Params(
        patch_areas=(1.,),generations=7,
        initial_population=(40,),initial_interaction=(.8,),
        initial_high_allele_frequency=(0.,),
        initial_trait_distribution=(_initial_low_only(101),),
        genotype_trait_recruitment="two_kernel_recruitment",
        inheritance_weight=.5,
        trait_occupancy_mode="finite_trait_bin_recruitment",
        random_seed=101)
    result=run(params,mutation_rate=0.)
    assert all(s.high_allele_frequency==(0.,) for s in result.snapshots)
    assert all(s.trait_occupancy[0].high_trait_abundance==0
               for s in result.snapshots)


def _initial_low_only(n):
    return tuple(1. if i==0 else 0. for i in range(n))


def test_mutation_recreates_allele_one_generation_before_possible_trait(pinned):
    Params,run=pinned
    params=Params(
        patch_areas=(1.,),generations=2,
        initial_population=(40,),initial_interaction=(.8,),
        initial_high_allele_frequency=(0.,),
        initial_trait_distribution=(_initial_low_only(101),),
        genotype_trait_recruitment="two_kernel_recruitment",
        inheritance_weight=.5,
        trait_occupancy_mode="finite_trait_bin_recruitment",
        random_seed=101)
    snaps=run(params,mutation_rate=.2).snapshots
    assert snaps[1].high_allele_frequency[0]>0
    assert snaps[1].trait_occupancy[0].high_trait_abundance==0
    first=MOD.conditional_reappearance(params,snaps[0],snaps[1].population)
    second=MOD.conditional_reappearance(params,snaps[1],snaps[2].population)
    assert first["conditional_any_high_recruits_next_generation"]==0
    assert second["conditional_any_high_recruits_next_generation"]>0


@pytest.mark.parametrize("mu",[-.1,.5,float("nan")])
def test_invalid_mutation_rate_stops(pinned,mu):
    Params,_=pinned
    p=Params(patch_areas=(1.,),generations=2)
    with pytest.raises(ValueError):
        MOD.mutation_unlock_probability(p,[20],[.2],mu)


def test_missing_external_source_is_not_silently_reconstructed(monkeypatch):
    monkeypatch.delenv("EGC_PINNED_ROOT",raising=False)
    with pytest.raises(KeyError):
        MOD.joint_absence_witness()
