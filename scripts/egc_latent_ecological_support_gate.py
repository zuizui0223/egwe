"""Density and latent allele support needed to keep the next q above its
pinned local allele/trait-endpoint switch after the expressed high trait vanishes.

This is an exact one-step inversion of the already established EGWE source
route-margin theorem. No new ecological fitness/field data are fitted.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

Q_SWITCH=.625
KAPPA=4.5
THETA=.5025
ALPHA=.6
BETA_TRAIT=.3
GAMMA_ALLELE=.1


def logistic(x:float)->float:
    return 1/(1+math.exp(-x)) if x>=0 else math.exp(x)/(1+math.exp(x))


def critical_support(q_switch:float=Q_SWITCH,theta:float=THETA,kappa:float=KAPPA)->float:
    if not 0<q_switch<1 or not kappa>0 or not math.isfinite(theta):
        raise ValueError("invalid switch parameters")
    return theta+math.log(q_switch/(1-q_switch))/kappa


def next_q(q:float,p:float,density:float,trait_mass:float=0.)->float:
    if any(not math.isfinite(x) or not 0<=x<=1
           for x in (q,p,density,trait_mass)):
        raise ValueError("source states constrained to [0,1]")
    support=ALPHA*q+BETA_TRAIT*trait_mass+GAMMA_ALLELE*p
    return logistic(KAPPA*(density*support-THETA))


def viability_gate(q:float,p:float,density:float,trait_mass:float=0.)->dict:
    future=next_q(q,p,density,trait_mass)
    required=critical_support()
    support=ALPHA*q+BETA_TRAIT*trait_mass+GAMMA_ALLELE*p
    q_req=(required/density-BETA_TRAIT*trait_mass-GAMMA_ALLELE*p)/ALPHA if density>0 else math.inf
    p_req=(required/density-ALPHA*q-BETA_TRAIT*trait_mass)/GAMMA_ALLELE if density>0 else math.inf
    d_req=required/support if support>0 else math.inf
    return {
        "q_current":q,"p_resident":p,"current_high_trait_mass":trait_mass,
        "density":density,"next_q":future,"switch_next_q":Q_SWITCH,
        "requires_density_weighted_support":required,
        "actual_density_weighted_support":density*support,
        "next_q_at_or_above_switch":future>=Q_SWITCH,
        "critical_current_q_if_other_states_fixed":q_req,
        "critical_resident_p_if_other_states_fixed":p_req,
        "critical_density_if_other_states_fixed":d_req,
        "no_assumption_that_q_is_clamped":True,
        "switch_is_allele_fitness_and_z1_performance_not_permanent_trait_occupancy":True,
    }


def fully_absent_trait_universal_limits():
    support=critical_support()
    # q,p <=1, T=0. Maximum density-weighted support =density*(alpha+gamma).
    density_required=support/(ALPHA+GAMMA_ALLELE)
    p_required_at_max_q_full_density=(support-ALPHA)/GAMMA_ALLELE
    max_next_q_at_dhalf=logistic(KAPPA*(.5*(ALPHA+GAMMA_ALLELE)-THETA))
    return {
        "trait_mass":0.,
        "maximum_possible_resident_q":1.,
        "maximum_possible_resident_p":1.,
        "necessary_density_for_ability_to_reach_next_q_switch":density_required,
        "necessary_p_at_full_density_and_max_q":p_required_at_max_q_full_density,
        "maximum_possible_next_q_at_density_half":max_next_q_at_dhalf,
        "next_q_switch_cannot_be_met_at_density_half_for_any_q_or_p":max_next_q_at_dhalf<Q_SWITCH,
        "calculation":"exact pinned one-step logistic support bound, not multigeneration establishment"
    }


def fixed_four_conditions():
    return {
        "scope":"SYNTHETIC_PINNED_ONE_STEP_GATE_T_ZERO",
        "universal":fully_absent_trait_universal_limits(),
        "initial_20_over_40":{
            f"q{q:.2f}_p{p:.2f}":viability_gate(q,p,.5)
            for q in (.2,.8) for p in (.04,.4)
        },
        "density_one_counterfactuals":{
            f"q{q:.2f}_p{p:.2f}":viability_gate(q,p,1.)
            for q in (.2,.8) for p in (.04,.4)
        },
        "natural_trait_function_measured":False,
        "source_frozen_NEE_updated":False,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    result=fixed_four_conditions()
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+"\n")
    print("LATENT_ECOLOGICAL_SUPPORT_GATE "+json.dumps({
        "minimum_density":result["universal"]["necessary_density_for_ability_to_reach_next_q_switch"],
        "minimum_allele_at_q1_d1":result["universal"]["necessary_p_at_full_density_and_max_q"],
        "q0.8_p0.4_at_density_half":result["initial_20_over_40"]["q0.80_p0.40"]["next_q"],
        "no_trait_density_half_impossible":result["universal"]["next_q_switch_cannot_be_met_at_density_half_for_any_q_or_p"],
        "no_natural_validation":not result["natural_trait_function_measured"],
    },sort_keys=True))


if __name__=="__main__":
    main()
