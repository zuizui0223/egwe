"""Sharp growth boundary for t=2 interaction support after T0=0, pinned EGC.

A fixed-parameter EGC demographic-feedback trap was certified in PR #233.
Here ONLY baseline population growth r is varied; all other source values
are unchanged. The critical boundary concerns *possibility* of q2>=.625,
NOT multi-generation ecological persistence or natural flower fitness.

The exact nonzero probability uses the original two-kernel EGC recruit
probability and a binomial high-trait count marginal. All source-specific
inputs are imported from the exact pinned upstream source.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from egc_trait_absence_demographic_trap import PARAMS,Q_ENDPOINT_SWITCH,sigmoid
from run_pinned_egc_aa_rr_lifecycle import PIN,load_source,initial_trait_row

K=40
INITIAL_N=40
INITIAL_Q=1.0
INITIAL_P=1.0
INITIAL_HIGH_TRAIT_MASS=0.0
INHERITANCE_WEIGHT=0.5
SOURCE_TEST_GROWTH_VALUES=(0.30,0.35,0.45,0.50,0.55,0.65)


def support_threshold():
    return (PARAMS["interaction_barrier"]+
            math.log(Q_ENDPOINT_SWITCH/(1-Q_ENDPOINT_SWITCH))/
            PARAMS["interaction_feedback"])


def analytical_growth_frontier()->dict:
    """Exact rounding boundary between impossible and possible t=2 crossing.

    The maximum q1 and maximum real N1 are attained together at
    q0=p0=1,N0=K when T0=0, so this is SHARP for the source family.
    Integer first-generation populations use Python nearest-even round.
    At exact half-integer equality the tie-to-even rule matters; the
    interpreted theorem uses strict r<rcrit and strict r>rcrit.
    """
    a=PARAMS
    q1max=sigmoid(a["interaction_feedback"]*(
        a["q_feedback_alpha"]+a["q_feedback_gamma_allele"]-
        a["interaction_barrier"]))
    critical_support=support_threshold()
    max_support_with_T1_and_p1_one=(
        a["q_feedback_alpha"]*q1max+
        a["q_feedback_beta_trait"]+
        a["q_feedback_gamma_allele"])
    real_n_needed=K*critical_support/max_support_with_T1_and_p1_one
    required_N1=math.ceil(real_n_needed)
    # To round to required_N1 instead of required_N1-1, the continuous
    # maximal n1 must exceed required_N1-0.5.
    rcrit=(math.log((required_N1-.5)/K)
           +1-a["interaction_growth"]*q1max-a["high_allele_growth"])
    if required_N1!=30:
        raise AssertionError("unexpected source-pinned N1 threshold")
    return {
        "source_commit":PIN,
        "growth_baseline_at_frozen_run":a["baseline_growth"],
        "q1_global_max_from_initial_T0_zero":q1max,
        "minimum_next_density_weighted_support":critical_support,
        "real_N1_required_if_all_next_high_and_all_alleles":real_n_needed,
        "minimum_integer_N1_for_q2_crossing":required_N1,
        "baseline_growth_critical_to_round_N1_to_30":rcrit,
        "r_below_boundary_global_q2_switch_impossible":True,
        "r_above_boundary_some_source_trajectory_can_cross_q2_switch":True,
        "equality_at_half_integer_uses_nearest_even_source_rounding":True,
        "possible_does_not_mean_probable":True,
        "phenotype_started_absent":True,
        "no_long_horizon_functional_persistence_claim":True,
    }


def source_parameters(Params,r:float,seed:int):
    if not math.isfinite(r) or not -1<=r<=2:
        raise ValueError("bounded source baseline growth range required")
    return Params(
        patch_areas=(1.,),generations=2,
        initial_population=(INITIAL_N,),
        initial_interaction=(INITIAL_Q,),
        initial_high_allele_frequency=(INITIAL_P,),
        initial_trait_distribution=(initial_trait_row(0.),),
        density_capacity=40.,area_reference=1.,
        interaction_feedback=4.5,interaction_barrier=.5025,
        q_feedback_alpha=.6,q_feedback_beta_trait=.3,q_feedback_gamma_allele=.1,
        baseline_growth=r,
        interaction_growth=.4,
        high_allele_growth=.1,
        genotype_trait_recruitment="two_kernel_recruitment",
        inheritance_weight=INHERITANCE_WEIGHT,
        trait_occupancy_mode="finite_trait_bin_recruitment",
        migration_rate=0.,
        random_seed=int(seed),
    )


def source_per_individual_high_recruit_probability(params)->float:
    """The source's actual multinomial high probability when T0=0,p0=q0=1."""
    from causal_model.multipatch_criticality_dynamics import (
        recruit_trait_distribution,trait_fitness,trait_grid)
    resident=initial_trait_row(0.,params.trait_grid_size)
    recruit=recruit_trait_distribution(resident,INITIAL_P,params)
    grid=trait_grid(params)
    masses=[v*max(params.trait_selection_floor,trait_fitness(z,INITIAL_Q,params))
            for z,v in zip(grid,recruit)]
    total=sum(masses)
    s=sum(v for z,v in zip(grid,masses) if z>=params.high_trait_cutoff)/total
    if not 0<s<1:
        raise AssertionError("witness requires positive non-deterministic high-bin recruitment")
    return s


def binomial_tail(n:int,p:float,kmin:int|None)->float:
    """Stable P[Binomial(n,p)>=kmin] using log-combination terms."""
    if not isinstance(n,int) or n<1 or not math.isfinite(p) or not 0<=p<=1:
        raise ValueError("invalid binomial inputs")
    if kmin is None or kmin>n:
        return 0.
    if not isinstance(kmin,int) or kmin<0:
        raise ValueError("invalid threshold")
    if kmin==0:
        return 1.
    if p==0:
        return 0.
    if p==1:
        return 1.
    logs=[
        math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
        +k*math.log(p)+(n-k)*math.log1p(-p)
        for k in range(kmin,n+1)
    ]
    shift=max(logs)
    return min(1.,math.exp(shift)*math.fsum(math.exp(x-shift) for x in logs))


def fixed_extreme_cell(Params,r:float)->dict:
    """Exact one-step source multinomial probability to attain q2 >= .625."""
    p=source_parameters(Params,r,777)
    frontier=analytical_growth_frontier()
    q1=frontier["q1_global_max_from_initial_T0_zero"]
    N1=max(1,round(INITIAL_N*math.exp(
        r+p.interaction_growth*q1+
        p.high_allele_growth*1-INITIAL_N/p.density_capacity)))
    d1=min(1.,N1/p.density_capacity)
    s=source_per_individual_high_recruit_probability(p)
    def upper_q(high_count):
        return sigmoid(p.interaction_feedback*(
            d1*(p.q_feedback_alpha*q1+
                p.q_feedback_beta_trait*(high_count/N1)+
                p.q_feedback_gamma_allele*1.)-
            p.interaction_barrier))
    count_threshold=next(
        (k for k in range(N1+1)
         if upper_q(k)>=Q_ENDPOINT_SWITCH),None)
    chance=binomial_tail(N1,s,count_threshold)
    return {
        "baseline_growth":r,
        "initial_N":INITIAL_N,"initial_q":INITIAL_Q,
        "initial_p":INITIAL_P,"initial_high_trait_mass":0.,
        "q1_exact":q1,"N1_exact":N1,
        "source_high_bin_recruit_probability":s,
        "required_high_bin_count_for_q2_switch":count_threshold,
        "required_high_bin_fraction":(
            None if count_threshold is None else count_threshold/N1),
        "q2_if_all_high_recruited":upper_q(N1),
        "q2_if_no_high_recruited":upper_q(0),
        "exact_probability_q2_at_or_above_0625":chance,
        "switch_attainable_with_positive_probability":chance>0.,
        "high_trait_viability_across_multiple_generations_not_inferred":True,
    }


def source_simulation_check(Params,simulate,scenario:dict,seeds:list[int])->dict:
    r=scenario["baseline_growth"]
    if len(set(seeds))!=len(seeds) or not seeds:
        raise ValueError("distinct validation seeds required")
    crossed=0
    sample_n1=set()
    max_q2=-1.
    q1_expected=scenario["q1_exact"]
    for seed in seeds:
        par=source_parameters(Params,r,seed)
        s=simulate(par,mutation_rate=0.).snapshots
        if len(s)!=3 or s[0].trait_occupancy[0].high_trait_abundance!=0:
            raise AssertionError("unexpected source lifecycle or initial high trait")
        assert abs(s[1].interaction[0]-q1_expected)<1e-12
        N1=s[1].population[0]
        sample_n1.add(N1)
        if N1!=scenario["N1_exact"]:
            raise AssertionError("source population draw differs from deterministic bound")
        if s[1].high_allele_frequency[0]!=1.:
            raise AssertionError("p0=1 must remain p1=1 without mutation")
        trait_count=s[1].trait_occupancy[0].high_trait_abundance
        high_fraction=trait_count/N1
        q2_expected=sigmoid(par.interaction_feedback*(
            min(1.,N1/par.density_capacity)*(
                .6*s[1].interaction[0]+.3*high_fraction+.1*1.)-
            par.interaction_barrier))
        actual_q2=s[2].interaction[0]
        if abs(actual_q2-q2_expected)>1e-12:
            raise AssertionError("source q2 differs from high-count support equation")
        crossed+=int(actual_q2>=Q_ENDPOINT_SWITCH)
        max_q2=max(max_q2,actual_q2)
    predicted=scenario["exact_probability_q2_at_or_above_0625"]
    observed=crossed/len(seeds)
    # This is a descriptive calibration of the source's multinomial kernel;
    # no tuning, inferential p-value or natural accuracy claim.
    descriptive_five_sigma=5*math.sqrt(
        predicted*(1-predicted)/len(seeds))+.02
    if abs(observed-predicted)>descriptive_five_sigma:
        raise AssertionError("real EGC draws unexpectedly disagree with exact source conditional probability")
    return {
        "seeds":len(seeds),
        "observed_q2_switch_crossings":crossed,
        "observed_rate":observed,
        "predicted_source_conditional_probability":predicted,
        "descriptive_five_sigma_tolerance":descriptive_five_sigma,
        "observed_max_q2":max_q2,
        "first_population_unique_values":sorted(sample_n1),
        "not_confirmatory_or_natural_validation":True,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    parser.add_argument("--seed-start",type=int,default=80001)
    parser.add_argument("--seed-count",type=int,default=512)
    args=parser.parse_args()
    if args.seed_start<80001 or not 1<=args.seed_count<=1024:
        raise ValueError("new bounded validation seed block required")
    Params,run=load_source()
    analytic=analytical_growth_frontier()
    near=analytic["baseline_growth_critical_to_round_N1_to_30"]
    r_values=[
        .3, near-.001,near+.001,.35,.45,.50,.55,.65
    ]
    seeds=list(range(args.seed_start,args.seed_start+args.seed_count))
    cells=[]
    for r in r_values:
        cell=fixed_extreme_cell(Params,r)
        if r in SOURCE_TEST_GROWTH_VALUES:
            cell["sampled_original_EGC"]=source_simulation_check(
                Params,run,cell,seeds)
        cells.append(cell)
    # The SOURCE is held fixed except for baseline growth. The extreme
    # q0=p0=1,N0=K state is chosen from the analytic envelope, not by
    # searching the observed stochastic model outcomes.
    result={
        "status":"SOURCE_EXACT_GROWTH_FRONTIER_WITH_STOCHASTIC_CALIBRATION",
        "pinned_source":PIN,
        "parameter_changed_only":"baseline_growth",
        "witness_initial_state":"q0=p0=1, T0=0, N0=K=40",
        "frontier":analytic,
        "source_validation_seeds":seeds,
        "fixed_growth_scenarios":cells,
        "experimental_inference":"exploratory source-kernel calibration, not independent natural forecasting",
        "no_multigeneration_high_trait_persistence_claim":True,
        "no_original_NEE_claim_modified":True,
    }
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("EGC_GROWTH_ESCAPE_FRONTIER "+json.dumps({
        "baseline_critical":near,
        "points":[{
            "r":round(x["baseline_growth"],8),
            "N1":x["N1_exact"],
            "K_required":x["required_high_bin_count_for_q2_switch"],
            "probability":x["exact_probability_q2_at_or_above_0625"],
            "observed_rate":x.get("sampled_original_EGC",{}).get("observed_rate"),
        } for x in cells],
        "no_natural_validation":True,
    },sort_keys=True))


if __name__=="__main__":
    main()
