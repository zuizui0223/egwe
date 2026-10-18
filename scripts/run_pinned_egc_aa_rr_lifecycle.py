"""Pinned EGC full life-cycle matched-marginal AA/RR comparison.

Requires external source at EGC_PINNED_ROOT; never vendors/reconstructs EGC.
No simulation runs when imported. Frozen source:
zuizui0223/egc@dd8ee379d0d3518194c767d16402042525bc00dc
"""
from __future__ import annotations
import argparse
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sys

PIN="dd8ee379d0d3518194c767d16402042525bc00dc"
def load_source():
    root=Path(os.environ["EGC_PINNED_ROOT"]).resolve()
    sha=(root/".git").exists()
    if not sha:
        raise ValueError("EGC_PINNED_ROOT must be a git checkout")
    import subprocess
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    if head!=PIN:
        raise ValueError(f"EGC commit mismatch: {head}")
    sys.path.insert(0,str(root))
    from causal_model.multipatch_criticality_dynamics import DynamicsParameters
    from causal_model.symmetric_allele_mutation_closure import simulate_with_symmetric_allele_mutation
    return DynamicsParameters,simulate_with_symmetric_allele_mutation

def initial_trait_row(mass:float,grid_size:int=101)->tuple[float,...]:
    if not 0<=mass<=1:raise ValueError("trait mass out of range")
    row=[0.0]*grid_size
    row[0]=1-mass
    row[-1]=mass
    return tuple(row)

def compare(generations:int,seeds:list[int],mutation_rate:float=0.0)->dict:
    if not 1<=generations<=200 or not seeds or len(set(seeds))!=len(seeds):
        raise ValueError("invalid horizon or seeds")
    DynamicsParameters,run=load_source()
    q=(.65,.75,.85,.95)
    b=(.2,.4,.6,.8)
    summary={}
    for mode,trait in (("AA",b),("RR",tuple(reversed(b)))):
        cases=[]
        for seed in seeds:
            p=DynamicsParameters(
                patch_areas=(1.,)*4,generations=generations,
                initial_population=(40,)*4,
                initial_interaction=q,
                initial_high_allele_frequency=trait,
                initial_trait_distribution=tuple(initial_trait_row(t) for t in trait),
                density_capacity=40.,area_reference=1.,
                interaction_feedback=4.5,interaction_barrier=.5025,
                q_feedback_alpha=.6,q_feedback_beta_trait=.3,q_feedback_gamma_allele=.1,
                genotype_trait_recruitment="two_kernel_recruitment",
                inheritance_weight=.5,
                trait_occupancy_mode="finite_trait_bin_recruitment",
                migration_rate=.1,
                random_seed=int(seed),
            )
            result=run(p,mutation_rate=mutation_rate)
            snaps=result.snapshots
            occupied=[any(x.realised_high_trait_occupied for x in s.trait_occupancy) for s in snaps]
            first_loss=next((i for i,v in enumerate(occupied) if i>0 and not v),None)
            cases.append({
                "seed":seed,
                "first_no_high_trait_occupancy_generation":first_loss,
                "event_by_horizon":first_loss is not None,
                "initial_occupied":occupied[0],
                "final_occupied":occupied[-1],
                "final_mean_q":sum(snaps[-1].interaction)/4,
                "final_max_q":max(snaps[-1].interaction),
                "final_population_total":sum(snaps[-1].population),
                "population_extinction_claim":False,
            })
        summary[mode]={
            "cases":cases,
            "event_count":sum(c["event_by_horizon"] for c in cases),
            "event_rate":sum(c["event_by_horizon"] for c in cases)/len(cases),
            "final_occupancy_rate":sum(c["final_occupied"] for c in cases)/len(cases),
        }
    return {
        "source_repo":"zuizui0223/egc","pinned_commit":PIN,
        "closure":"simulate_with_symmetric_allele_mutation",
        "generations":generations,"seeds":seeds,"mutation_rate":mutation_rate,
        "same_marginal_q":True,"same_marginal_trait_and_allele":True,
        "event_definition":"first generation >=1 with no patch having realised_high_trait_occupied",
        "event_is_absorbing":False,
        "event_is_first_passage_not_permanent_loss":True,
        "source_initial_high_trait_occupancy_required":True,
        "AA_minus_RR_event_rate":summary["AA"]["event_rate"]-summary["RR"]["event_rate"],
        "arms":summary,
        "natural_field_validation":False,
        "frozen_NEE_empirical_claims_changed":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--generations",type=int,default=12)
    p.add_argument("--seeds",type=int,nargs="+",default=[101,102,103,104])
    p.add_argument("--mutation-rate",type=float,default=0.)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    r=compare(a.generations,a.seeds,a.mutation_rate)
    Path(a.output).write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps({"AA_event_rate":r["arms"]["AA"]["event_rate"],
        "RR_event_rate":r["arms"]["RR"]["event_rate"],
        "event_difference":r["AA_minus_RR_event_rate"],
        "pinned_commit":r["pinned_commit"]},sort_keys=True))
if __name__=="__main__":
    main()
