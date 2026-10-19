"""Tests of source-exact trait reappearance; field/genetic claims forbidden."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from random import Random
import sys
from types import SimpleNamespace

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0,str(SCRIPTS))
SPEC=importlib.util.spec_from_file_location(
    "egc_trait_reappearance",SCRIPTS/"egc_high_trait_reappearance.py")
assert SPEC is not None and SPEC.loader is not None
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


@pytest.fixture(scope="module")
def pinned():
    if not os.environ.get("EGC_PINNED_ROOT"):
        pytest.skip("requires pinned EGC checkout in dedicated source-integrated CI")
    return MOD.load_source()


def _context(pinned, mode, allele, n=1, h=.5, grid=11):
    Params,_=pinned
    params=Params(
        patch_areas=(1.,),generations=2,
        initial_population=(40,),
        initial_high_allele_frequency=(allele,),
        initial_interaction=(.8,),
        trait_grid_size=grid,
        genotype_trait_recruitment=mode,
        inheritance_weight=h,
        trait_occupancy_mode="finite_trait_bin_recruitment")
    resident=[0.]*grid
    resident[0]=1.
    snap=SimpleNamespace(
        trait_occupancy=[SimpleNamespace(
            distribution=tuple(resident),high_trait_abundance=0)],
        high_allele_frequency=[allele],
        interaction=[.8])
    result=MOD.conditional_reappearance(params,snap,[n])
    return params,snap,result,tuple(int(40 if i==0 else 0)
                                 for i in range(grid))


def test_one_step_reappearance_probability_exact_source_modes(pinned):
    _,_,resident,_=_context(pinned,"resident_trait_only",.5,12)
    _,_,two,_=_context(pinned,"two_kernel_recruitment",.5,12)
    _,_,no_allele,_=_context(pinned,"two_kernel_recruitment",0.,12)
    _,_,no_allele_seeding,_=_context(
        pinned,"two_kernel_recruitment",.5,12,h=1.)
    assert resident["conditional_any_high_recruits_next_generation"]==0
    assert no_allele["conditional_any_high_recruits_next_generation"]==0
    assert no_allele_seeding["conditional_any_high_recruits_next_generation"]==0
    assert 0<two["conditional_any_high_recruits_next_generation"]<1
    assert two["uses_resident_allele_before_migration_mutation_drift"]
    assert two["source_high_trait_count_at_start"]==0
    assert two["not_natural_trait_reexpression_data"] is True


def test_probability_matches_original_pinned_multinomial_draws(pinned):
    _,_=pinned
    from causal_model.multipatch_criticality_dynamics import update_trait_abundance
    params,snap,theoretical,abundance=_context(
        pinned,"two_kernel_recruitment",.1,n=1,grid=11)
    expected=theoretical["conditional_any_high_recruits_next_generation"]
    trials=2000
    observed=0
    for seed in range(10001,10001+trials):
        sample=update_trait_abundance(
            abundance,.8,.1,1,params,Random(seed))
        high=sum(x for index,x in enumerate(sample)
                 if index/(len(sample)-1)>=params.high_trait_cutoff)
        observed+=int(high>=1)
    assert .01<expected<.15
    assert abs(observed/trials-expected)<.03


def test_resident_only_high_trait_absence_is_absorbing_under_pinned_source(pinned):
    Params,run=pinned
    params=Params(
        patch_areas=(1.,),generations=5,
        initial_population=(40,),
        initial_interaction=(.8,),
        initial_high_allele_frequency=(.8,),
        initial_trait_distribution=(MOD.initial_trait_row(0.),),
        genotype_trait_recruitment="resident_trait_only",
        trait_occupancy_mode="finite_trait_bin_recruitment",
        random_seed=101)
    result=run(params,mutation_rate=.2)
    assert all(
        s.trait_occupancy[0].high_trait_abundance==0
        for s in result.snapshots)


def test_regen_lag_uses_resident_allele_before_mutation(pinned):
    Params,run=pinned
    params=Params(
        patch_areas=(1.,),generations=2,
        initial_population=(40,),
        initial_interaction=(.8,),
        initial_high_allele_frequency=(0.,),
        initial_trait_distribution=(MOD.initial_trait_row(0.),),
        genotype_trait_recruitment="two_kernel_recruitment",
        inheritance_weight=.5,
        trait_occupancy_mode="finite_trait_bin_recruitment",
        random_seed=101)
    result=run(params,mutation_rate=.2)
    snaps=result.snapshots
    assert snaps[0].high_allele_frequency[0]==0
    assert snaps[1].trait_occupancy[0].high_trait_abundance==0
    assert snaps[1].high_allele_frequency[0]>0
    a=MOD.conditional_reappearance(params,snaps[0],snaps[1].population)
    b=MOD.conditional_reappearance(params,snaps[1],snaps[2].population)
    assert a["conditional_any_high_recruits_next_generation"]==0
    assert b["conditional_any_high_recruits_next_generation"]>0


def test_reappearance_runner_matches_locked_AA_RR_source_settings(pinned):
    from run_pinned_egc_aa_rr_lifecycle import compare
    existing=compare(12,[101,102],0.)
    current=MOD.run_report([101,102],12)["modes"]["two_kernel_recruitment"]
    for arm in ("AA","RR"):
        for old,new in zip(existing["arms"][arm]["cases"],current[arm]["cases"]):
            assert old["seed"]==new["seed"]
            assert old["event_by_horizon"]==new["ever_absent"]
            assert old["final_occupied"]==new["final_occupied"]


def test_summary_recovery_is_not_permanent_extinction():
    cases=[{
        "ever_absent":True,"final_occupied":True,
        "ever_returned_after_absence":True,"return_transition_count":1,
        "conditional_recovery_opportunity_count":1,
        "conditional_recovery_probability_sum":.6,
        "actual_immediate_recovery_count":1,
        "total_absent_generations":1,
    },{
        "ever_absent":True,"final_occupied":False,
        "ever_returned_after_absence":False,"return_transition_count":0,
        "conditional_recovery_opportunity_count":1,
        "conditional_recovery_probability_sum":0.,
        "actual_immediate_recovery_count":0,
        "total_absent_generations":2,
    }]
    r=MOD.summarize(cases,24,"two_kernel_recruitment")
    assert r["ever_absent"]==2
    assert r["ever_returned_after_absence"]==1
    assert r["ever_absent_but_final_occupied"]==1
    assert r["final_occupied"]==1
    assert not r["high_trait_zero_set_structurally_absorbing"]
    assert r["no_population_extinction_claim"]

    resident=MOD.summarize(cases,24,"resident_trait_only")
    assert resident["high_trait_zero_set_structurally_absorbing"]


def test_bad_contracts_rejected():
    with pytest.raises(ValueError):
        MOD.run_report([],24)
    with pytest.raises(ValueError):
        MOD.run_report([101,101],24)
    with pytest.raises(ValueError):
        MOD.run_report([101],1)
