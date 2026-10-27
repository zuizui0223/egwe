"""A predeclared 2x2x2 initial-state test of latent support and density.

Reuses the exact pinned upstream EGC stochastic life cycle, no new simulator.
Tests whether satisfying a necessary T=0 q-threshold condition at t=1
is associated with later phenotype occupancy. In this source experiment N0
changes BOTH density and population/demographic drift; it is NOT a pure
isolated density-feedback causal intervention.

All numeric outcomes are in-model stochastic replicates, never natural data.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path
from random import Random

from egc_reexpression_establishment_gate import (
    PIN,load_source,source_params,observed_state,conditional_high_next
)
from egc_latent_ecological_support_gate import viability_gate, Q_SWITCH

Q_VALUES=(.8,.98)
P_VALUES=(.04,.4)
N_VALUES=(20,40)
PRIMARY_OUTCOMES=(
    "expressed_at_generation_1",
    "three_consecutive_high_snapshots",
    "high_at_final_generation",
    "ever_joint_trait_allele_zero",
)


def cell_name(q:float,p:float,n:int)->str:
    return f"q{q:.2f}_p{p:.2f}_N{n}"


def one_seed(Params,run,seed:int,q:float,p:float,n:int,generations:int)->dict:
    basic=source_params(Params,seed,q,p,generations)
    params=replace(basic,initial_population=(n,))
    snapshots=run(params,mutation_rate=0.).snapshots
    if len(snapshots)!=generations+1:
        raise AssertionError("source trajectory length drifted")
    if snapshots[0].population!=(n,) or snapshots[0].high_allele_frequency!=(p,):
        raise AssertionError("source resident N or p does not equal declared input")
    high=[snapshot.trait_occupancy[0].high_trait_abundance>0 for snapshot in snapshots]
    if high[0]:
        raise AssertionError("all experiments require initially absent high trait")
    analytic=viability_gate(q,p,n/40.,trait_mass=0.)
    first_q=snapshots[1].interaction[0]
    if abs(first_q-analytic["next_q"])>1e-13:
        raise AssertionError("upstream source q1 differs from exact feedback gate")
    first_prob=conditional_high_next(params,snapshots[0],snapshots[1].population)
    state=[observed_state(s) for s in snapshots]
    return {
        "seed":seed,
        "q1":first_q,
        "q2":snapshots[2].interaction[0],
        "q1_above_0625":first_q>=Q_SWITCH,
        "q2_above_0625":snapshots[2].interaction[0]>=Q_SWITCH,
        "q1_analytic_gate_value":analytic["next_q"],
        "first_generation_high_expression_probability":first_prob,
        "expressed_at_generation_1":high[1],
        "three_consecutive_high_snapshots":all(high[1:4]),
        "high_at_final_generation":high[-1],
        "ever_joint_trait_allele_zero":any(x.startswith("joint_zero") for x in state[1:]),
        "first_joint_zero_generation":next(
            (t for t,x in enumerate(state[1:],start=1) if x.startswith("joint_zero")),None),
        "mean_occupancy_over_12_generations":sum(high[1:])/generations,
        "initial_density":n/40.,
        "source_order_preserved":True,
    }


def concise(cases:list[dict])->dict:
    n=len(cases)
    if n<1:
        raise ValueError("no simulated seeds")
    return {
        "n_seeds":n,
        "counts":{outcome:sum(bool(c[outcome]) for c in cases)
                  for outcome in PRIMARY_OUTCOMES},
        "rates":{outcome:sum(bool(c[outcome]) for c in cases)/n
                 for outcome in PRIMARY_OUTCOMES},
        "initial_one_step_q_threshold_met":all(c["q1_above_0625"] for c in cases),
        "q1":sum(c["q1"] for c in cases)/n,
        "mean_q2":sum(c["q2"] for c in cases)/n,
        "mean_expressed_fraction_over_horizon":
            sum(c["mean_occupancy_over_12_generations"] for c in cases)/n,
        "conditional_first_generation_high_expression_probability":
            sum(c["first_generation_high_expression_probability"] for c in cases)/n,
    }


def descriptive_contrasts(cells:dict,seeds:list[int],reps:int=2048,
                          bootstrap_seed:int=20261028)->dict:
    """All density contrasts are PREDECLARED; seed-group resampling descriptive."""
    if not 100<=reps<=10000:
        raise ValueError("invalid bootstrap repetitions")
    draws=Random(bootstrap_seed)
    n=len(seeds)
    boot=[[draws.randrange(n) for _ in range(n)] for _ in range(reps)]
    contrasts={}
    for q in Q_VALUES:
        for p in P_VALUES:
            low=cell_name(q,p,20);high=cell_name(q,p,40)
            a=cells[high]["cases"]
            b=cells[low]["cases"]
            if [x["seed"] for x in a]!=seeds or [x["seed"] for x in b]!=seeds:
                raise ValueError("seed pairing contract broken")
            outcomes={}
            for key in PRIMARY_OUTCOMES:
                difference=[int(a[i][key])-int(b[i][key]) for i in range(n)]
                bootstrap=sorted(sum(difference[i] for i in idx)/n for idx in boot)
                outcomes[key]={
                    "N40_minus_N20":sum(difference)/n,
                    "paired_seed_bootstrap_percentile_95":[
                        bootstrap[int(.025*(reps-1))],
                        bootstrap[int(.975*(reps-1))]
                    ],
                    "N40_only":sum(x>0 for x in difference),
                    "N20_only":sum(x<0 for x in difference),
                    "not_confirmatory":True,
                }
            contrasts[f"density_at_q{q:.2f}_p{p:.2f}"]={
                "N40":high,"N20":low,"outcomes":outcomes,
                "density_also_changes_population_size_and_finite_drift":True,
            }
    return {
        "bootstrap_seed":bootstrap_seed,"bootstrap_reps":reps,
        "sampling_unit":"simulated seed matched across the eight scenarios",
        "no_generation_pseudoreplication":True,
        "contrasts":contrasts,
        "not_independent_holdout_or_natural_validation":True,
    }


def run_experiment(seeds:list[int],generations:int=12)->dict:
    if not 3<=generations<=30 or not seeds or len(set(seeds))!=len(seeds):
        raise ValueError("invalid seed and horizon specification")
    if any(not isinstance(seed,int) or seed<0 for seed in seeds):
        raise ValueError("seeds must be distinct nonnegative integers")
    Params,runner=load_source()
    cells={}
    for q in Q_VALUES:
        for p in P_VALUES:
            for n in N_VALUES:
                name=cell_name(q,p,n)
                cases=[one_seed(Params,runner,seed,q,p,n,generations)
                       for seed in seeds]
                cells[name]={
                    "q0":q,"p0":p,"N0":n,
                    "initial_density":n/40.,
                    "initial_high_trait_count":0,
                    "initial_expected_q1":viability_gate(q,p,n/40.,0.)["next_q"],
                    "source_parameter_note":"all other parameters sourced from the merged PR232 runner",
                    "summary":concise(cases),
                    "cases":cases,
                }
    return {
        "status":"EXPLORATORY_PINNED_EGC_LATENT_Q_DENSITY_FACTORIAL",
        "source_commit":PIN,
        "seed_block":seeds,
        "generations":generations,
        "scenarios":cells,
        "descriptive_density_contrasts":descriptive_contrasts(cells,seeds),
        "design_not_tuned_after_outcomes":True,
        "q_crossing_is_only_a_one_step_ecological_support_diagnostic":True,
        "N0_change_combines_density_population_and_finite_drift":True,
        "high_trait_occupancy_not_reproductive_function_or_establishment":True,
        "no_natural_field_validation":True,
        "frozen_NEE_numerical_results_unchanged":True,
    }


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--seed-start",type=int,default=70001)
    parser.add_argument("--seed-count",type=int,default=256)
    args=parser.parse_args()
    if not 1<=args.seed_count<=256 or args.seed_start<=50256:
        raise ValueError("use a new bounded seed block after the prior study")
    result=run_experiment(
        list(range(args.seed_start,args.seed_start+args.seed_count)))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("LATENT_SUPPORT_DENSITY_FACTORIAL "+json.dumps({
        "source":result["source_commit"],
        "n_seed":len(result["seed_block"]),
        "results":{k:{
            "q1_above_switch":v["summary"]["initial_one_step_q_threshold_met"],
            "q1":v["summary"]["q1"],
            "mean_q2":v["summary"]["mean_q2"],
            "first_trait_count":v["summary"]["counts"]["expressed_at_generation_1"],
            "three_snapshot_count":v["summary"]["counts"]["three_consecutive_high_snapshots"],
            "final_trait_count":v["summary"]["counts"]["high_at_final_generation"],
            "joint_zero_count":v["summary"]["counts"]["ever_joint_trait_allele_zero"]
        } for k,v in result["scenarios"].items()},
        "no_field_validation":True,
    },sort_keys=True))


if __name__=="__main__":
    main()
