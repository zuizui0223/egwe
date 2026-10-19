"""Pinned EGC tests of expression, short-term retention and genetic-capacity closure.

Do NOT equate transient source-high-trait occupancy with natural evolutionary
establishment or floral function. Fixed q0={0.2,0.8}, p0={0.04,0.4};
all runs start with zero high-trait individuals. The model updates q,
population, allele frequency, and recruited trait bins via pinned EGC.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from egc_high_trait_reappearance import PIN, load_source, initial_trait_row


def observed_state(snapshot) -> str:
    high=any(row.high_trait_abundance>0 for row in snapshot.trait_occupancy)
    latent=any(p>0 for p in snapshot.high_allele_frequency)
    if high and latent:
        return "expressed_with_allele"
    if high and not latent:
        return "expressed_without_allele"
    if latent:
        return "unexpressed_with_latent_allele"
    return "joint_zero_absorbing_without_mutation_or_allele_import"


def conditional_high_next(params, snapshot, next_pop) -> float:
    """Exact probability of ANY high-bin recruit in the next generation.

    For an arbitrary current resident trait distribution, not only a zero
    phenotype. This uses the pinned recruit_trait_distribution, trait_grid
    and trait_fitness, and N(t+1) *as already produced by the original source*.
    """
    from causal_model.multipatch_criticality_dynamics import (
        recruit_trait_distribution, trait_fitness, trait_grid,
    )
    if params.trait_occupancy_mode!="finite_trait_bin_recruitment" or params.realised_high_trait_abundance_threshold!=1:
        raise ValueError("requires source finite trait bin occupancy threshold=1")
    if len(snapshot.trait_occupancy)!=len(next_pop):
        raise ValueError("next population size mismatch")
    grid=trait_grid(params)
    no_high_probability=1.
    for old, p, q, N in zip(
        snapshot.trait_occupancy,snapshot.high_allele_frequency,
        snapshot.interaction,next_pop
    ):
        if not isinstance(N,int) or N<1:
            raise ValueError("next population must be a positive integer")
        dist=recruit_trait_distribution(old.distribution,p,params)
        weights=[
            mass*max(params.trait_selection_floor,trait_fitness(z,q,params))
            for z,mass in zip(grid,dist)
        ]
        total=sum(weights)
        if total<=0:
            raise ValueError("source fitness weights invalid")
        high_probability=sum(v for v,z in zip(weights,grid) if z>=params.high_trait_cutoff)/total
        if not 0<=high_probability<=1+1e-12:
            raise ValueError("trait probabilities not normalized")
        no_high_probability*=max(0.,1-high_probability)**N
    return 1-no_high_probability


def source_params(Params,seed,initial_q,initial_p,horizon):
    if not 0<=initial_q<=1 or not 0<=initial_p<=1:
        raise ValueError("initial eco-genetic states outside [0,1]")
    return Params(
        patch_areas=(1.,),generations=horizon,
        initial_population=(20,),
        initial_interaction=(initial_q,),
        initial_high_allele_frequency=(initial_p,),
        initial_trait_distribution=(initial_trait_row(0.),),
        density_capacity=40.,area_reference=1.,
        interaction_feedback=4.5,interaction_barrier=.5025,
        q_feedback_alpha=.6,q_feedback_beta_trait=.3,
        q_feedback_gamma_allele=.1,
        genotype_trait_recruitment="two_kernel_recruitment",
        inheritance_weight=.5,
        trait_occupancy_mode="finite_trait_bin_recruitment",
        migration_rate=0.,
        random_seed=int(seed),
    )


def analyze_one(Params,run,seed,q,p,horizon):
    params=source_params(Params,seed,q,p,horizon)
    sims=run(params,mutation_rate=0.)
    snapshots=sims.snapshots
    states=[observed_state(s) for s in snapshots]
    occupied=[s.trait_occupancy[0].high_trait_abundance>0 for s in snapshots]
    if occupied[0]:
        raise AssertionError("source should start with NO expressed high trait")
    if horizon<3 or len(snapshots)!=horizon+1:
        raise ValueError("three generations of retention observation required")
    predicted=[
        conditional_high_next(params,snapshots[t],snapshots[t+1].population)
        for t in range(horizon)]
    first_return=next((t for t in range(1,horizon+1) if occupied[t]),None)
    joint_zero=next((t for t in range(1,horizon+1)
                     if states[t]=="joint_zero_absorbing_without_mutation_or_allele_import"),None)
    recovered_t1=occupied[1]
    return {
        "seed":seed,
        "initial_q":q,"initial_p":p,
        "initial_potential_fitness_high":.5+.8*q,
        "initial_potential_viable_high":(.5+.8*q)>=1.,
        "q_at_generation_1":snapshots[1].interaction[0],
        "q_at_generation_2":snapshots[2].interaction[0],
        "first_high_expression_generation":first_return,
        "expressed_by_horizon":first_return is not None,
        "expressed_at_generation_1":recovered_t1,
        "two_consecutive_expressed_generations":all(occupied[1:3]),
        "three_consecutive_expressed_generations":all(occupied[1:4]),
        "final_expressed":occupied[-1],
        "ever_joint_zero":joint_zero is not None,
        "first_joint_zero_generation":joint_zero,
        "joint_zero_at_end":states[-1]=="joint_zero_absorbing_without_mutation_or_allele_import",
        "number_of_expressed_snapshots":sum(occupied[1:]),
        "number_of_allele_positive_but_high_trait_absent_snapshots":
            sum(z=="unexpressed_with_latent_allele" for z in states[1:]),
        "exact_first_generation_expression_probability":predicted[0],
        "source_conditioned_next_generation_expression_probability_sum":sum(predicted),
        "actual_next_generation_expression_count":sum(occupied[1:]),
        "initial_and_final_genetic_state":[snapshots[0].high_allele_frequency[0],
                                          snapshots[-1].high_allele_frequency[0]],
        "source_kernel_not_reconstructed":True,
    }


def summarize(cases):
    if not cases:
        raise ValueError("no cases")
    n=len(cases)
    binary=[
        "expressed_by_horizon","expressed_at_generation_1",
        "two_consecutive_expressed_generations",
        "three_consecutive_expressed_generations","final_expressed",
        "ever_joint_zero","joint_zero_at_end",
    ]
    return {
        "n":n,
        "events":{k:sum(bool(row[k]) for row in cases) for k in binary},
        "rates":{k:sum(bool(row[k]) for row in cases)/n for k in binary},
        "initial_one_step_expression_probability":sum(
            row["exact_first_generation_expression_probability"] for row in cases)/n,
        "first_generation_actual_expression_count":sum(
            bool(row["expressed_at_generation_1"]) for row in cases),
        "mean_expressed_snapshots":sum(
            row["number_of_expressed_snapshots"] for row in cases)/n,
        "mean_latent_but_unexpressed_snapshots":sum(
            row["number_of_allele_positive_but_high_trait_absent_snapshots"] for row in cases)/n,
        "mean_q_at_generation_1":sum(
            row["q_at_generation_1"] for row in cases)/n,
        "mean_q_at_generation_2":sum(
            row["q_at_generation_2"] for row in cases)/n,
        "mean_conditional_expected_expressed_snapshots":sum(
            row["source_conditioned_next_generation_expression_probability_sum"] for row in cases)/n,
        "no_independent_generation_claim":True,
    }


def run_experiment(seeds,horizon=12):
    if not 3<=horizon<=30 or not seeds or len(seeds)!=len(set(seeds)):
        raise ValueError("invalid independent seed block or horizon")
    if any(not isinstance(seed,int) or seed<0 for seed in seeds):
        raise ValueError("seeds must be nonnegative integers")
    Params,source_runner=load_source()
    scenarios={}
    for q0 in (.2,.8):
        for p0 in (.04,.4):
            label=f"q{q0:.2f}_p{p0:.2f}"
            cases=[analyze_one(Params,source_runner,seed,q0,p0,horizon)
                   for seed in seeds]
            scenarios[label]={
                "initial_q":q0,"initial_allele_frequency":p0,
                "initial_high_trait_abundance":0,
                "source_initial_high_trait_fitness":.5+.8*q0,
                "summary":summarize(cases),
                "case_receipts":cases,
            }
    return {
        "status":"EXPLORATORY_REAPPEARANCE_VS_SHORT_TERM_RETENTION_IN_PINNED_EGC",
        "pinned_egc_source_commit":PIN,
        "cohort":list(seeds),
        "horizon":horizon,
        "initial_population":20,
        "density_capacity":40,
        "fixed_barrier":.5025,
        "mutation_rate":0.,
        "genotype_trait_recruitment":"two_kernel_recruitment",
        "inheritance_weight":.5,
        "scenarios":scenarios,
        "expression_not_biological_establishment":True,
        "high_trait_performance_above_one_not_long_term_establishment_certificate":True,
        "no_permanent_population_extinction_claim":True,
        "stochastic_model_not_real_flower_data":True,
        "unmodified_frozen_NEE_manuscript":True,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    parser.add_argument("--seed-start",type=int,default=50001)
    parser.add_argument("--seed-count",type=int,default=256)
    args=parser.parse_args()
    if args.seed_start<=30128 or not 1<=args.seed_count<=256:
        raise ValueError("fresh, bounded seed block required")
    result=run_experiment(
        list(range(args.seed_start,args.seed_start+args.seed_count)))
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    compact={
        label:{
            "initial_q":group["initial_q"],
            "initial_p":group["initial_allele_frequency"],
            "initial_w_high":group["source_initial_high_trait_fitness"],
            "summary":group["summary"],
        } for label,group in result["scenarios"].items()
    }
    print("REEXPRESSION_ESTABLISHMENT_GATE "+json.dumps(compact,sort_keys=True))


if __name__=="__main__":
    main()
