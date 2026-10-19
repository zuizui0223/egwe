"""Pinned EGC joint high-trait / high-allele absorption and mutation lag.

No natural re-evolution claims. This module distinguishes:
* zero phenotype with a nonzero resident latent allele (one-step recoverable);
* zero phenotype AND zero allele, mutation=0 (joint absorbing class);
* zero phenotype AND zero allele, mutation>0 (first allele appearance
  after drift, phenotype recovery only in subsequent recruitment).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from types import SimpleNamespace

from egc_high_trait_reappearance import PIN, conditional_reappearance, load_source


def mutation_unlock_probability(parameters, next_population, next_interaction,
                                symmetric_mutation_rate):
    """Exact P(any high allele survives drift at t+1 | all resident p_t=0).

    In the EGC source p_sel=0, internal migration leaves p=0, mutation
    produces p_mut=mu, then each patch draws Binomial(gene_copies, mu).
    No new high phenotype is recruited in that same step from p_t=0.
    """
    mu=float(symmetric_mutation_rate)
    if not math.isfinite(mu) or not 0<=mu<.5:
        raise ValueError("source symmetric mutation requires 0<=mu<0.5")
    if len(next_population)!=len(next_interaction) or not next_population:
        raise ValueError("matching nonempty next population and q required")
    # Required by the fixed external EGC source, never approximated by N.
    load_source()
    from causal_model.multipatch_criticality_dynamics import _effective_size
    copies=[]
    for n,q in zip(next_population,next_interaction):
        if not isinstance(n,int) or n<1 or not math.isfinite(q) or not 0<=q<=1:
            raise ValueError("next N must be positive integer and next q in [0,1]")
        n_eff=_effective_size(n,q,parameters)
        copies.append(max(2,round(2*n_eff)))
    number=sum(copies)
    probability=-math.expm1(number*math.log1p(-mu))
    return {
        "resident_all_high_allele_frequencies_zero":True,
        "resident_all_high_trait_abundances_zero_required":True,
        "gene_copies_by_patch":copies,
        "total_gene_copies":number,
        "symmetric_mutation_rate":mu,
        "probability_any_mutant_allele_after_drift":probability,
        "probability_high_trait_returns_during_this_generation":0.,
        "phenotypic_reappearance_can_begin_next_recruitment_only":mu>0,
        "closed_population_no_external_allele_import":True,
        "strict_source_identity":PIN,
        "no_field_evolution_inferred":True,
    }


def source_absent_state(parameters, allele, interaction):
    from causal_model.multipatch_criticality_dynamics import trait_grid
    grid=trait_grid(parameters)
    low=[0.]*len(grid)
    low[0]=1.
    occupancy=[SimpleNamespace(distribution=tuple(low),
                               high_trait_abundance=0)
               for _ in allele]
    return SimpleNamespace(trait_occupancy=occupancy,
                           high_allele_frequency=list(allele),
                           interaction=list(interaction))


def joint_absence_witness():
    Params,_=load_source()
    params=Params(
        patch_areas=(1.,),generations=2,
        trait_grid_size=11,
        genotype_trait_recruitment="two_kernel_recruitment",
        inheritance_weight=.5,
        trait_occupancy_mode="finite_trait_bin_recruitment")
    q=.2  # high-trait source fitness at z=1 is below viability threshold.
    without_allele=source_absent_state(params,[0.],[q])
    with_allele=source_absent_state(params,[.4],[q])
    no=conditional_reappearance(params,without_allele,[20])
    yes=conditional_reappearance(params,with_allele,[20])
    from causal_model.multipatch_criticality_dynamics import trait_fitness
    W=trait_fitness(1.,q,params)
    if not W<params.viability_threshold:
        raise AssertionError("counterexample q must be below high-trait viability")
    unlock=mutation_unlock_probability(params,[20],[q],.02)
    return {
        "provenance":"PINNED_EGC_SYNTHETIC_SOURCE_OPERATOR_ONLY",
        "same_visible_trait_state":True,
        "same_interaction_and_population":True,
        "resident_allele_state_differs":True,
        "focal_interaction_q":q,
        "high_trait_performance_at_q":W,
        "high_trait_viability_threshold":params.viability_threshold,
        "allele_zero_one_step_reappearance_probability":
            no["conditional_any_high_recruits_next_generation"],
        "allele_present_one_step_reappearance_probability":
            yes["conditional_any_high_recruits_next_generation"],
        "mutant_allele_unlock_from_joint_zero":unlock,
        "claim_scope":"conditional next-step phenotype recovery and mutation-before-next-recruitment lag",
        "full_ecological_fate_probability_computed":False,
        "anthocyanin_reactivation_in_nature_tested":False,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    value=joint_absence_witness()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(value,indent=2)+"\n",encoding="utf-8")
    print("JOINT_GENE_TRAIT_ABSORPTION "+json.dumps({
        "source_commit":PIN,
        "no_resident_allele_reappearance_p":
            value["allele_zero_one_step_reappearance_probability"],
        "latent_allele_reappearance_p":
            value["allele_present_one_step_reappearance_probability"],
        "mutation_allele_unlock_p":
            value["mutant_allele_unlock_from_joint_zero"]["probability_any_mutant_allele_after_drift"],
        "high_trait_performance":
            value["high_trait_performance_at_q"],
        "no_field_validation":not value["anthocyanin_reactivation_in_nature_tested"]
    },sort_keys=True))


if __name__=="__main__":
    main()
