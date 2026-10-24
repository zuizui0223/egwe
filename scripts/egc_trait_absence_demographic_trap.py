"""Certified EGC pathwise demographic–interaction trap after high-trait absence.

All statements are restricted to the EXACT pinned deterministic q and N
operators with specific fixed parameters. Stochastic trait recruitment,
allele drift, and mutation may proceed, but their effects are bounded by
trait high mass and allele frequency in [0,1].

The source code is NOT vendored or reconstructed. A dedicated source-locked
test checks the actual original EGC simulator and trait fitness grid.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

PARAMS={
    "area_ratio":1.0,"density_capacity":40.0,
    "interaction_feedback":4.5,"interaction_barrier":0.5025,
    "q_feedback_alpha":0.6,"q_feedback_beta_trait":0.3,
    "q_feedback_gamma_allele":0.1,
    "baseline_growth":0.3,"interaction_growth":0.4,
    "high_allele_growth":0.1,
    "low_base":1.1,"low_cost":0.8,
    "high_base":0.2,"high_interaction_benefit":0.8,
    "high_peak_width":0.15,"trait_grid_size":101,
    "high_trait_cutoff":0.7,"viability_threshold":1.0,
}
Q_ENDPOINT_SWITCH=0.625
Q_INVARIANT_CAP=0.59
N_INVARIANT_CAP=29


def sigmoid(v:float)->float:
    if v>=0:
        x=math.exp(-v)
        return 1/(1+x)
    x=math.exp(v)
    return x/(1+x)


def q_upper_bound(q:float,n_upper:float,high_mass:float=1.0,
                  high_allele:float=1.0)->float:
    """Worst-case next interaction given upper bounds for ALL q,T,p,N."""
    a=PARAMS
    if not (0<=q<=1 and n_upper>=1 and 0<=high_mass<=1 and
            0<=high_allele<=1):
        raise ValueError("invalid state envelope")
    density=min(1.0,n_upper/a["density_capacity"])
    support=(a["q_feedback_alpha"]*q+
             a["q_feedback_beta_trait"]*high_mass+
             a["q_feedback_gamma_allele"]*high_allele)
    return sigmoid(a["interaction_feedback"]*(
        density*support-a["interaction_barrier"]))


def real_population_upper(q_next_upper:float)->float:
    """Universal N(t+1) upper over ALL positive N(t).

    For source demographic map n exp(A - n/K), maximum for n>0
    occurs at n=K, and equals K exp(A-1).
    """
    if not 0<=q_next_upper<=1:
        raise ValueError("invalid q upper")
    a=PARAMS
    return a["density_capacity"]*math.exp(
        a["baseline_growth"]+
        a["interaction_growth"]*q_next_upper+
        a["high_allele_growth"]-1)


def real_population_upper_when_n_bounded(q_next_upper:float,
                                          n_upper:float)->float:
    """A valid bound when 1<=N<=n_upper<=K, where demographic map grows."""
    K=PARAMS["density_capacity"]
    if not 1<=n_upper<=K or not 0<=q_next_upper<=1:
        raise ValueError("requires upper N<=K and bounded interaction")
    a=PARAMS
    return n_upper*math.exp(
        a["baseline_growth"]+
        a["interaction_growth"]*q_next_upper+
        a["high_allele_growth"]-n_upper/K)


def numeric_round_upper(x:float)->int:
    """Upper on max(1,round(s)) when 0<=s<=x.

    Only use if x has certified margin away from 0.5 ties. Nonnegative
    nearest-integer rounding is monotone, so ceil(x+1/2) is conservative;
    when x is strictly below a half-integer, floor(x+1/2) suffices.
    """
    if not math.isfinite(x) or x<0:
        raise ValueError("nonnegative finite bound required")
    if abs((x+0.5)-round(x+0.5))<1e-9:
        raise ValueError("cannot certify rounded bound at a half-integer")
    return max(1,math.floor(x+0.5))


def high_trait_fitness(z:float,q:float)->float:
    """Source-pinned grid fitness, separately cross-checked with EGC in CI."""
    a=PARAMS
    if not 0<=z<=1 or not 0<=q<=1:
        raise ValueError("trait fitness arguments outside [0,1]")
    return (
        a["low_base"]-a["low_cost"]*z*z+
        (a["high_base"]+a["high_interaction_benefit"]*q)*
        math.exp(-((z-1)/a["high_peak_width"])**2)
    )


def certificate()->dict:
    """Valid for arbitrary initial integer N>=1, q,p in [0,1], T0=0.

    A wholly model-specific pathwise theorem. The core inequality uses
    no statistical independence and no simulated RNG draws.
    """
    a=PARAMS
    q1_max=sigmoid(a["interaction_feedback"]*(
        a["q_feedback_alpha"]+a["q_feedback_gamma_allele"]-
        a["interaction_barrier"]))
    n1_real=real_population_upper(q1_max)
    n1_max=numeric_round_upper(n1_real)
    q2_max=q_upper_bound(q1_max,n1_max)
    n2_real=real_population_upper_when_n_bounded(q2_max,n1_max)
    n2_max=numeric_round_upper(n2_real)
    q3_max=q_upper_bound(q2_max,n2_max)
    n3_real=real_population_upper_when_n_bounded(q3_max,n2_max)
    n3_max=numeric_round_upper(n3_real)

    # Prove {N<=29,q<=0.59} is forward-invariant for ALL possible
    # trait masses and allele frequencies in [0,1].
    qnext_invariant=q_upper_bound(Q_INVARIANT_CAP,N_INVARIANT_CAP)
    nnext_real=real_population_upper_when_n_bounded(
        qnext_invariant,N_INVARIANT_CAP)
    nnext_invariant=numeric_round_upper(nnext_real)

    grid=[i/(a["trait_grid_size"]-1)
          for i in range(a["trait_grid_size"])]
    high=[z for z in grid if z>=a["high_trait_cutoff"]]
    upper_fitness=max(high_trait_fitness(z,Q_INVARIANT_CAP) for z in high)
    maximizing_z=max(high,key=lambda z:high_trait_fitness(z,Q_INVARIANT_CAP))

    assert n1_max==29 and n2_max==27
    assert q2_max<Q_ENDPOINT_SWITCH
    assert q3_max<Q_INVARIANT_CAP
    assert n3_max<=N_INVARIANT_CAP
    assert qnext_invariant<Q_INVARIANT_CAP
    assert nnext_invariant<=N_INVARIANT_CAP
    assert upper_fitness<a["viability_threshold"]

    return {
        "status":"SOURCE_SPECIFIC_ANALYTICAL_INVARIANCE_CERTIFICATE",
        "source":"zuizui0223/egc",
        "pinned_commit":"dd8ee379d0d3518194c767d16402042525bc00dc",
        "validity_conditions":{
            "patch_area_and_reference":1.0,
            "initial_high_trait_mass":0.0,
            "initial_interaction_and_allele":[0.0,1.0],
            "initial_population":"any positive integer",
            "parameter_contract":a,
            "no_forcing_barrier_change":True,
            "no_demographic_immigration_or_individual_dispersal":True,
            "allele_mutation_and_allele_only_migration_allowed_if_p_stays_in_unit_interval":True,
        },
        "first_step":{
            "uniform_q1_upper":q1_max,
            "real_N1_continuous_upper":n1_real,
            "integer_N1_upper":n1_max,
        },
        "second_step":{
            "uniform_q2_upper":q2_max,
            "real_N2_continuous_upper":n2_real,
            "integer_N2_upper":n2_max,
            "all_realized_q2_below_endpoint_switch":q2_max<Q_ENDPOINT_SWITCH,
        },
        "third_step":{
            "uniform_q3_upper":q3_max,
            "real_N3_continuous_upper":n3_real,
            "integer_N3_upper":n3_max,
        },
        "forward_invariant_region_from_t3":{
            "q_upper":Q_INVARIANT_CAP,
            "N_upper":N_INVARIANT_CAP,
            "next_q_upper_with_any_trait_and_allele":qnext_invariant,
            "next_N_upper_with_any_trait_and_allele":nnext_invariant,
        },
        "potential_high_trait_viability":{
            "from_generation":3,
            "tested_high_trait_grid_count":len(high),
            "maximum_fitness_under_q_0_59":upper_fitness,
            "argmax_trait_bin":maximizing_z,
            "viability_threshold":a["viability_threshold"],
            "no_high_bin_viable_for_all_future_generations_under_contract":True,
        },
        "interpretation":"Potential high-bin viability absent from t>=3; stochastic realised high-bin expression can still recur from alleles.",
        "field_data_used":False,
        "biological_fitness_measured":False,
        "new_NEE_AUC_or_confirmatory_evidence":False,
        "all_future_trait_bin_occupancy_guaranteed_absent":False,
        "all_plant_population_extinct":False,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    result=certificate()
    target=Path(args.output)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("EGC_DEMOGRAPHIC_SUPPORT_TRAP "+json.dumps({
        "max_q1":result["first_step"]["uniform_q1_upper"],
        "max_N1":result["first_step"]["integer_N1_upper"],
        "max_q2":result["second_step"]["uniform_q2_upper"],
        "max_N2":result["second_step"]["integer_N2_upper"],
        "max_q3":result["third_step"]["uniform_q3_upper"],
        "invariant_q_cap_from_t3":result["forward_invariant_region_from_t3"]["q_upper"],
        "max_high_bin_fitness_t3_plus":result["potential_high_trait_viability"]["maximum_fitness_under_q_0_59"],
        "natural_claim":result["field_data_used"]
    },sort_keys=True))


if __name__=="__main__":
    main()
