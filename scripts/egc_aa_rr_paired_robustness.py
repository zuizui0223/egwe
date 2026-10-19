"""Exploratory independent-seed extension of pinned AA/RR full life cycle.

Fixed two horizons, 128 fresh paired seeds, and two separately declared
endpoints. All comparisons are synthetic stochastic-model experiments.
"""
from __future__ import annotations
import argparse
from collections import Counter
from math import comb
import json
from pathlib import Path
from run_pinned_egc_aa_rr_lifecycle import compare

def exact_discordant_sign_test(aa_only:int,rr_only:int)->float:
    n=aa_only+rr_only
    if n==0:return 1.
    k=min(aa_only,rr_only)
    return min(1.,2*sum(comb(n,i) for i in range(k+1))/(2**n))

def summarize(result:dict)->dict:
    a={r["seed"]:r for r in result["arms"]["AA"]["cases"]}
    b={r["seed"]:r for r in result["arms"]["RR"]["cases"]}
    if set(a)!=set(b):raise ValueError("paired seeds do not match")
    seeds=sorted(a)
    def paired_binary(field):
        aa=sum(bool(a[s][field]) for s in seeds)
        rr=sum(bool(b[s][field]) for s in seeds)
        aa_only=sum(bool(a[s][field]) and not bool(b[s][field]) for s in seeds)
        rr_only=sum(bool(b[s][field]) and not bool(a[s][field]) for s in seeds)
        return {"AA_count":aa,"RR_count":rr,"AA_rate":aa/len(seeds),
                "RR_rate":rr/len(seeds),"AA_minus_RR":(aa-rr)/len(seeds),
                "AA_only":aa_only,"RR_only":rr_only,
                "exact_paired_sign_test_two_sided":exact_discordant_sign_test(aa_only,rr_only),
                "not_independent_arm_binomial":True}
    return {
        "generations":result["generations"],
        "seed_count":len(seeds),
        "seed_min":min(seeds),"seed_max":max(seeds),
        "first_passage_ever":paired_binary("event_by_horizon"),
        "occupied_at_final_snapshot":paired_binary("final_occupied"),
        "mean_final_population_AA":sum(a[s]["final_population_total"] for s in seeds)/len(seeds),
        "mean_final_population_RR":sum(b[s]["final_population_total"] for s in seeds)/len(seeds),
        "mean_final_q_AA":sum(a[s]["final_mean_q"] for s in seeds)/len(seeds),
        "mean_final_q_RR":sum(b[s]["final_mean_q"] for s in seeds)/len(seeds),
        "event_not_absorbing":True,
        "paired_seed_design_does_not_guarantee_shared_random_draws":True,
        "pilot_seeds_101_to_104_excluded":True,
        "exploratory_parameter_setting_not_external_validation":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    p.add_argument("--seed-start",type=int,default=20001)
    p.add_argument("--seed-count",type=int,default=128)
    a=p.parse_args()
    if not 1<=a.seed_count<=512 or a.seed_start<=104:
        raise ValueError("independent follow-up seed block required")
    seeds=list(range(a.seed_start,a.seed_start+a.seed_count))
    results=[summarize(compare(h,seeds,0.)) for h in (12,24)]
    report={
        "status":"EXPLORATORY_SOURCE_PINNED_PAIRED_SEED_ROBUSTNESS",
        "source_commit":"dd8ee379d0d3518194c767d16402042525bc00dc",
        "seed_block":seeds,
        "horizons":[12,24],
        "results":results,
        "no_field_data":True,
        "no_extinction_claim":True,
        "not_confirmatory_preregistration":True,
        "frozen_NEE_evidence_unchanged":True,
    }
    dest=Path(a.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("AA_RR_PAIRED_ROBUSTNESS "+json.dumps({
        "results":[{"horizon":r["generations"],"first_passage":r["first_passage_ever"],
                    "final_occupancy":r["occupied_at_final_snapshot"]} for r in results],
        "no_field_data":True},sort_keys=True))

if __name__=="__main__":
    main()
