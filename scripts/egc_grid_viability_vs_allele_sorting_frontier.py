"""Pinned EGC high-trait GRID viability frontier versus endpoint allele sorting.

A distinct frontier from PR #234's q(z=1)=0.625 allele-relative-fitness
switch. Viability of ANY z>=0.7 on the ACTUAL EGC 101-bin grid starts at
q≈0.5992. This script reuses the original exact source trait_fitness and
trait_space_summary, and the source-calibrated binomial calculation already
locked by PR #234. No genotype/trait outcomes are inferred from field data.

The extreme attainable witness q0=p0=1, N0=40, T0=0 is mathematical and
not an estimate of typical fragmentation or pollinator behaviour.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from egc_demographic_trap_escape_frontier import (
    INITIAL_Q, INITIAL_P, INITIAL_N, K,
    analytical_growth_frontier, binomial_tail,
    fixed_extreme_cell, source_parameters,
    sigmoid, SOURCE_TEST_GROWTH_VALUES,
)
from egc_trait_absence_demographic_trap import PARAMS, Q_ENDPOINT_SWITCH
from run_pinned_egc_aa_rr_lifecycle import PIN, load_source


def exact_grid_viability_threshold(Params) -> dict:
    """Derive q_crit from source fitness values at q=0,1, not a surrogate."""
    from causal_model.multipatch_criticality_dynamics import (
        trait_fitness, trait_grid, trait_space_summary,
    )
    params=source_parameters(Params,.30,99000)
    options=[]
    for z in trait_grid(params):
        if z<params.high_trait_cutoff:
            continue
        w0=trait_fitness(z,0.,params)
        w1=trait_fitness(z,1.,params)
        slope=w1-w0
        if slope<=0:
            raise ValueError("positive q benefit required for exact root")
        root=(params.viability_threshold-w0)/slope
        if 0<=root<=1:
            options.append((root,z))
    if not options:
        raise ValueError("high-trait viability never attainable in q in [0,1]")
    root,z=min(options)
    epsilon=1e-8
    assert not trait_space_summary(root-epsilon,params).high_trait_component_present
    assert trait_space_summary(root+epsilon,params).high_trait_component_present
    return {
        "grid_size":params.trait_grid_size,
        "high_trait_cutoff":params.high_trait_cutoff,
        "critical_q_for_any_potentially_viable_high_trait":root,
        "critical_high_trait_bin_z":z,
        "high_trait_fitness_at_grid_q_critical":trait_fitness(z,root,params),
        "endpoint_allele_fitness_switch_q":Q_ENDPOINT_SWITCH,
        "whole_grid_viability_begins_below_allele_endpoint_switch":
            root<Q_ENDPOINT_SWITCH,
        "exact_source_trait_space_summary_checked":True,
        "not_a_future_occupancy_or_reproduction_threshold":True,
    }


def precise_growth_boundary(grid_q:float) -> dict:
    """Necessary/sufficient-for-possibility demographic growth boundary.

    q1 and max first-population over arbitrary positive starting population
    are attained jointly at q0=p0=1,N0=K=40 while T0=0.
    Endpoint r_crit comparison comes from PR #234.
    """
    if not 0<grid_q<Q_ENDPOINT_SWITCH:
        raise ValueError("the source high-grid threshold must precede 0.625")
    prior=analytical_growth_frontier()
    q1=prior["q1_global_max_from_initial_T0_zero"]
    a=PARAMS
    threshold=a["interaction_barrier"]+(
        math.log(grid_q/(1-grid_q))/a["interaction_feedback"])
    best_support=(a["q_feedback_alpha"]*q1+
                  a["q_feedback_beta_trait"]+
                  a["q_feedback_gamma_allele"])
    real_need=K*threshold/best_support
    integer_need=math.ceil(real_need)
    if integer_need!=29:
        raise AssertionError("source high-grid threshold expected N1 >= 29")
    rcrit=(math.log((integer_need-.5)/K)
           +1-a["interaction_growth"]*q1-a["high_allele_growth"])
    return {
        "pinned_source":PIN,
        "q1_max_with_initial_high_trait_absent":q1,
        "grid_q_critical":grid_q,
        "grid_density_weighted_support_required":threshold,
        "real_first_population_needed_at_best_trait_and_allele":real_need,
        "minimal_integer_first_population_for_viability":integer_need,
        "growth_critical_for_high_grid_viability_at_t2":rcrit,
        "growth_critical_for_allele_endpoint_switch_at_t2":
            prior["baseline_growth_critical_to_round_N1_to_30"],
        "strictly_nonempty_growth_window_grid_viable_but_allele_disfavored":
            rcrit<prior["baseline_growth_critical_to_round_N1_to_30"],
        "source_rounding_tie_at_exact_critical_growth":True,
        "statement":"These are t=2 attainability frontiers, not long-horizon fate guarantees.",
    }


def exact_two_event_cell(Params,r:float,qcrit:float) -> dict:
    """Exact source-conditioned binomial mass for q2 grid viability and q2>=.625."""
    from causal_model.multipatch_criticality_dynamics import trait_space_summary
    cell=fixed_extreme_cell(Params,r)
    N=cell["N1_exact"]
    q1=cell["q1_exact"]
    source=source_parameters(Params,r,90000)
    s=cell["source_high_bin_recruit_probability"]
    d=min(1.,N/source.density_capacity)
    def q2_from_high_count(k:int)->float:
        return sigmoid(source.interaction_feedback*(
            d*(source.q_feedback_alpha*q1+
               source.q_feedback_beta_trait*(k/N)+
               source.q_feedback_gamma_allele*1.0)-
            source.interaction_barrier))
    grid_threshold_count=next((
        k for k in range(N+1)
        if trait_space_summary(q2_from_high_count(k),source).high_trait_component_present
    ),None)
    allele_threshold_count=cell["required_high_bin_count_for_q2_switch"]
    chance_grid=binomial_tail(N,s,grid_threshold_count)
    chance_allele=cell["exact_probability_q2_at_or_above_0625"]
    if chance_grid+1e-13<chance_allele:
        raise AssertionError("whole high grid viability should begin at lower q")
    wedge=max(0.,chance_grid-chance_allele)
    if grid_threshold_count is not None:
        q_at_first=q2_from_high_count(grid_threshold_count)
        if q_at_first+1e-13<qcrit:
            raise AssertionError("wrong high-grid viability threshold")
    else:
        q_at_first=None
    return {
        "baseline_growth":r,
        "first_population_N1":N,
        "q1_source_exact":q1,
        "source_high_recruit_bin_probability":s,
        "grid_viability_required_high_bin_count":grid_threshold_count,
        "allele_endpoint_required_high_bin_count":allele_threshold_count,
        "grid_viability_exact_probability":chance_grid,
        "allele_positive_selection_exact_probability":chance_allele,
        "grid_viable_but_allele_selected_against_exact_probability":wedge,
        "source_trait_space_summary_verified":True,
        "q2_at_first_grid_viable_count":q_at_first,
        "q2_if_all_high":cell["q2_if_all_high_recruited"],
        "true_model_trait_function_or_loss_probability_estimated":False,
    }


def validate_original_EGC_draws(Params,run,cell:dict,seeds:list[int])->dict:
    """2-generation original stochastic EGC, full validation of both events."""
    from causal_model.multipatch_criticality_dynamics import trait_space_summary
    critical_q=exact_grid_viability_threshold(Params)["critical_q_for_any_potentially_viable_high_trait"]
    r=cell["baseline_growth"]
    if not seeds or len(set(seeds))!=len(seeds):
        raise ValueError("nonempty unique independent validation seeds")
    c_grid=c_allele=c_wedge=0
    for seed in seeds:
        params=source_parameters(Params,r,seed)
        snapshots=run(params,mutation_rate=0.).snapshots
        if len(snapshots)!=3:
            raise AssertionError("unexpected pinned horizon")
        s0,s1,s2=snapshots
        if s0.trait_occupancy[0].high_trait_abundance!=0:
            raise AssertionError("initial trait must be absent")
        if s1.population[0]!=cell["first_population_N1"]:
            raise AssertionError("original population N1 mismatched")
        if s1.high_allele_frequency[0]!=1:
            raise AssertionError("p1=1 required by extreme witness without mutation")
        high=bool(s2.trait_space[0].high_trait_component_present)
        allele=(s2.interaction[0]>=Q_ENDPOINT_SWITCH)
        if high!=(s2.interaction[0]>=critical_q):
            raise AssertionError("actual EGC potential-trait criterion mismatches")
        if allele and not high:
            raise AssertionError("allele endpoint cannot be positive without high-grid viability")
        c_grid+=int(high)
        c_allele+=int(allele)
        c_wedge+=int(high and not allele)
        K1=s1.trait_occupancy[0].high_trait_abundance
        required=cell["grid_viability_required_high_bin_count"]
        if high!=(required is not None and K1>=required):
            raise AssertionError("source high-bin count does not recover q2 grid event")
    expected={
        "grid_viable":cell["grid_viability_exact_probability"],
        "allele_nonnegative":cell["allele_positive_selection_exact_probability"],
        "grid_viable_allele_negative":cell["grid_viable_but_allele_selected_against_exact_probability"],
    }
    observed={"grid_viable":c_grid,"allele_nonnegative":c_allele,
              "grid_viable_allele_negative":c_wedge}
    for name,p in expected.items():
        rate=observed[name]/len(seeds)
        tolerance=5*math.sqrt(p*(1-p)/len(seeds))+.02
        if abs(rate-p)>tolerance:
            raise AssertionError("source stochastic sample deviated strongly from exact binomial calibration")
    return {
        "seed_count":len(seeds),
        "observed_counts":observed,
        "source_conditional_expected_probs":expected,
        "original_source_case_conformity_checked":True,
        "repeated_stochastic_generations_not_independent_replicates":True,
        "not_natural_or_confirmatory_evidence":True,
    }


def build_report(seeds:list[int]) -> dict:
    if not seeds or len(set(seeds))!=len(seeds) or len(seeds)>1024:
        raise ValueError("nonempty unique, bounded seed block required")
    Params,run=load_source()
    grid=exact_grid_viability_threshold(Params)
    boundary=precise_growth_boundary(
        grid["critical_q_for_any_potentially_viable_high_trait"])
    lower=boundary["growth_critical_for_high_grid_viability_at_t2"]
    higher=boundary["growth_critical_for_allele_endpoint_switch_at_t2"]
    growth_values=[
        .27,lower-.001,lower+.001,.30,higher-.001,higher+.001,
        .35,.45,.50,.55,.65,
    ]
    source_validation={.30,.35,.45,.50,.55,.65}
    cells=[]
    for r in growth_values:
        cell=exact_two_event_cell(Params,r,grid[
            "critical_q_for_any_potentially_viable_high_trait"])
        if r in source_validation:
            cell["original_EGC_validation"]=validate_original_EGC_draws(
                Params,run,cell,seeds)
        cells.append(cell)
    return {
        "status":"SOURCE_EXACT_GRID_VIABILITY_AND_ALLELE_SWITCH_TWO_FRONTIERS",
        "pinned_source":PIN,
        "grid_viability":grid,
        "growth_frontiers":boundary,
        "seed_block":seeds,
        "source_validation_growth_values":sorted(source_validation),
        "scenarios":cells,
        "source_fixed_extreme_initial_condition":{
            "N0":40,"q0":1.0,"p0":1.0,"T0":0.0,
            "purpose":"mathematical attainability witness not a typical ecological initial state",
        },
        "source_baseline_growth_03_t3_irreversible_trap_proven_in_pr233":True,
        "claims_t2_viability_only_not_future_persistence":True,
        "natural_evolutionary_or_pollination_data_used":False,
        "frozen_NEE_scientific_evidence_changed":False,
    }


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--seed-start",type=int,default=90001)
    parser.add_argument("--seed-count",type=int,default=512)
    args=parser.parse_args()
    if args.seed_start<90001 or not 1<=args.seed_count<=1024:
        raise ValueError("fresh bounded source-validation seed block required")
    result=build_report(list(range(args.seed_start,args.seed_start+args.seed_count)))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("GRID_VIABILITY_VS_ALLELE_SORTING "+json.dumps({
        "source":PIN,
        "q_grid":result["grid_viability"]["critical_q_for_any_potentially_viable_high_trait"],
        "r_grid":result["growth_frontiers"]["growth_critical_for_high_grid_viability_at_t2"],
        "r_allele":result["growth_frontiers"]["growth_critical_for_allele_endpoint_switch_at_t2"],
        "cells":[{"r":round(x["baseline_growth"],8),
                  "N1":x["first_population_N1"],
                  "required_grid":x["grid_viability_required_high_bin_count"],
                  "required_allele":x["allele_endpoint_required_high_bin_count"],
                  "grid_prob":x["grid_viability_exact_probability"],
                  "allele_prob":x["allele_positive_selection_exact_probability"],
                  "wedge_prob":x["grid_viable_but_allele_selected_against_exact_probability"],
                  "observed":x.get("original_EGC_validation",{}).get("observed_counts")
                 } for x in result["scenarios"]],
        "no_natural_data":True,
    },sort_keys=True))


if __name__=="__main__":
    main()
