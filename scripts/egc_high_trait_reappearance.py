"""Pinned EGC high-trait regeneration after temporary global absence.

Mathematics/source bridge, not evidence of biological trait re-evolution.
All simulation runs use the exact EGC pinned code and disclose latent p_t
with resident q_t and subsequent N[t+1] in the source trait update.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from run_pinned_egc_aa_rr_lifecycle import PIN, initial_trait_row, load_source


def conditional_reappearance(parameters, snapshot, next_population):
    """Probability of >0 high trait recruits from a global zero state.

    Directly matches update_trait_abundance() distribution in pinned EGC.
    Patch-wise multinomial draws make P(any high)=1-prod(1-s_i)**N_i.
    It only applies when realised_high_trait_abundance_threshold=1,
    the finite trait-bin mode is active and all high counts equal zero.
    """
    if parameters.trait_occupancy_mode != "finite_trait_bin_recruitment":
        raise ValueError("requires finite trait-bin recruitment")
    if parameters.realised_high_trait_abundance_threshold != 1:
        raise ValueError("formula requires threshold of at least one high bin")
    if not all(x.high_trait_abundance == 0 for x in snapshot.trait_occupancy):
        raise ValueError("source state must be globally high-trait absent")
    if len(next_population)!=len(snapshot.interaction):
        raise ValueError("population length differs from source snapshot")
    from causal_model.multipatch_criticality_dynamics import (
        trait_grid, trait_fitness, recruit_trait_distribution,
    )
    grid=trait_grid(parameters)
    survival_patches=[]
    per_patch=[]
    for resident, allele, q, n in zip(snapshot.trait_occupancy,
                                      snapshot.high_allele_frequency,
                                      snapshot.interaction,next_population):
        if not isinstance(n,int) or n<1:
            raise ValueError("finite positive next_population required")
        recruited=recruit_trait_distribution(
            resident.distribution,allele,parameters)
        selected=[v*max(parameters.trait_selection_floor,
                        trait_fitness(z,q,parameters))
                  for z,v in zip(grid,recruited)]
        denominator=sum(selected)
        if denominator<=0:raise ValueError("invalid source trait selection")
        s=sum(a for z,a in zip(grid,selected)
              if z>=parameters.high_trait_cutoff)/denominator
        s=max(0.,min(1.,s))
        survival_patches.append((1-s)**n)
        per_patch.append({"resident_p":allele,"resident_q":q,
                          "next_population":n,
                          "high_trait_recruit_probability_per_individual":s,
                          "probability_no_high_recruits":(1-s)**n})
    probability=1-math.prod(survival_patches)
    return {
        "conditional_any_high_recruits_next_generation":probability,
        "probability_all_remain_without_high_trait":math.prod(survival_patches),
        "patch_conditions":per_patch,
        "source_mode":parameters.genotype_trait_recruitment,
        "uses_resident_allele_before_migration_mutation_drift":True,
        "source_high_trait_count_at_start":0,
        "nonabsorbing_if_probability_positive":probability>0,
        "not_natural_trait_reexpression_data":True,
    }


def parameters_for_arm(egc_params, arm, seed, generations, mode):
    q=(.65,.75,.85,.95)
    b=(.2,.4,.6,.8)
    trait=b if arm=="AA" else tuple(reversed(b))
    return egc_params(
        patch_areas=(1.,)*4,generations=generations,
        initial_population=(40,)*4,
        initial_interaction=q,
        initial_high_allele_frequency=trait,
        initial_trait_distribution=tuple(initial_trait_row(t) for t in trait),
        density_capacity=40.,area_reference=1.,
        interaction_feedback=4.5,interaction_barrier=.5025,
        q_feedback_alpha=.6,q_feedback_beta_trait=.3,
        q_feedback_gamma_allele=.1,
        genotype_trait_recruitment=mode,
        inheritance_weight=.5,
        trait_occupancy_mode="finite_trait_bin_recruitment",
        migration_rate=.1,
        random_seed=int(seed),
    )


def one_case(parameters, simulation):
    snapshots=simulation.snapshots
    high=[any(x.realised_high_trait_occupied
              for x in s.trait_occupancy) for s in snapshots]
    if not high[0]:
        raise ValueError("initial trait occupancy absent; cannot define loss")
    if len(high)!=parameters.generations+1:
        raise ValueError("incorrect trajectory length")
    recoveries=[]
    absence_windows=0
    for t in range(1,len(high)-1):
        if not high[t]:
            absence_windows+=1
            info=conditional_reappearance(
                parameters,snapshots[t],snapshots[t+1].population)
            recoveries.append({
                "from_generation":t,
                "observed_next_generation_reappearance":bool(high[t+1]),
                "predicted_conditional_probability":
                    info["conditional_any_high_recruits_next_generation"],
                "resident_positive_allele_patches":sum(
                    x["resident_p"]>0 for x in info["patch_conditions"]),
            })
    return {
        "seed":parameters.random_seed,
        "first_temporary_absence":next(
            (t for t in range(1,len(high)) if not high[t]),None),
        "ever_absent":not all(high),
        "final_occupied":high[-1],
        "ever_returned_after_absence":any(
            not high[t-1] and high[t] for t in range(2,len(high))),
        "absent_at_end":not high[-1],
        "total_absent_generations":sum(not x for x in high[1:]),
        "return_transition_count":sum(
            not high[t-1] and high[t] for t in range(2,len(high))),
        "conditional_recovery_opportunity_count":absence_windows,
        "conditional_recovery_probability_sum":sum(
            r["predicted_conditional_probability"] for r in recoveries),
        "actual_immediate_recovery_count":sum(
            r["observed_next_generation_reappearance"] for r in recoveries),
        "conditional_recovery_audit":recoveries,
        "future_field_function_observed":False,
    }


def summarize(cases,horizon,mode):
    if not cases:raise ValueError("no simulations")
    n=len(cases)
    return {
        "horizon":horizon,"n_seeds":n,
        "ever_absent":sum(x["ever_absent"] for x in cases),
        "final_occupied":sum(x["final_occupied"] for x in cases),
        "ever_returned_after_absence":sum(
            x["ever_returned_after_absence"] for x in cases),
        "ever_absent_but_final_occupied":sum(
            x["ever_absent"] and x["final_occupied"] for x in cases),
        "return_transition_count":sum(x["return_transition_count"] for x in cases),
        "conditional_recovery_opportunities":sum(
            x["conditional_recovery_opportunity_count"] for x in cases),
        "conditional_expected_immediate_recoveries":sum(
            x["conditional_recovery_probability_sum"] for x in cases),
        "conditional_observed_immediate_recoveries":sum(
            x["actual_immediate_recovery_count"] for x in cases),
        "mean_absent_generations":sum(
            x["total_absent_generations"] for x in cases)/n,
        "high_trait_zero_set_structurally_absorbing":mode=="resident_trait_only",
        "allele_seeded_reappearance_possible_conditionally":mode=="two_kernel_recruitment",
        "no_population_extinction_claim":True,
    }


def run_report(seeds,generations=24):
    if not seeds or len(set(seeds))!=len(seeds) or not 2<=generations<=60:
        raise ValueError("invalid independent-seed/horizon contract")
    Params,simulate=load_source()
    report={
        "source":"zuizui0223/egc","pinned_commit":PIN,
        "seed_block":seeds,"generations":generations,
        "modes":{},
        "parameter_setting":"same as PR229 except recruitment mode in ablation",
        "mechanism_only_exploratory":True,
        "field_anthocyanin_reactivation_claim":False,
        "frozen_NEE_claims_unchanged":True,
    }
    for mode in ("two_kernel_recruitment","resident_trait_only"):
        arms={}
        for arm in ("AA","RR"):
            cases=[]
            for seed in seeds:
                params=parameters_for_arm(Params,arm,seed,generations,mode)
                trajectory=simulate(params,mutation_rate=0.)
                cases.append(one_case(params,trajectory))
            arms[arm]={
                "summary":summarize(cases,generations,mode),
                "cases":cases,
            }
        report["modes"][mode]=arms
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    parser.add_argument("--seed-start",type=int,default=30001)
    parser.add_argument("--seed-count",type=int,default=128)
    args=parser.parse_args()
    if args.seed_start<=20128 or not 1<=args.seed_count<=128:
        raise ValueError("use new independent seeds and bounded batch")
    seeds=list(range(args.seed_start,args.seed_start+args.seed_count))
    result=run_report(seeds)
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    summary={
        mode:{
            arm:result["modes"][mode][arm]["summary"]
            for arm in ("AA","RR")}
        for mode in result["modes"]}
    print("HIGH_TRAIT_REAPPEARANCE "+json.dumps(summary,sort_keys=True))


if __name__=="__main__":
    main()
