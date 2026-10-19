"""Compact, explicitly exploratory uncertainty audit of pinned EGC results.

The four scenarios and three occupancy endpoints were fixed before the source
runner opened 256-seed outcomes. Comparisons and resampling intervals are
POST-HOC DESCRIPTIVE; never upgrade to confirmatory ecological evidence.

Bootstrap samples entire seed IDs in sync across all parameter cells, not
individual simulated generations (the latter would be pseudoreplication).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from random import Random

CONTRASTS=(
    ("allele_p040_minus_p004_at_q020","q0.20_p0.40","q0.20_p0.04"),
    ("allele_p040_minus_p004_at_q080","q0.80_p0.40","q0.80_p0.04"),
    ("interaction_q080_minus_q020_at_p004","q0.80_p0.04","q0.20_p0.04"),
    ("interaction_q080_minus_q020_at_p040","q0.80_p0.40","q0.20_p0.40"),
)
ENDPOINTS=(
    "expressed_at_generation_1",
    "three_consecutive_expressed_generations",
    "final_expressed",
    "ever_joint_zero",
)
REQUIRED_SCENARIOS=frozenset({
    "q0.20_p0.04","q0.20_p0.40","q0.80_p0.04","q0.80_p0.40",
})


def audit(raw:dict,bootstrap_reps:int=4096,bootstrap_seed:int=20261019) -> dict:
    if not isinstance(bootstrap_reps,int) or bootstrap_reps<100:
        raise ValueError("bootstrap count must be >=100")
    if raw.get("pinned_egc_source_commit")!="dd8ee379d0d3518194c767d16402042525bc00dc":
        raise ValueError("different EGC upstream source")
    scenarios=raw.get("scenarios",{})
    if set(scenarios)!=REQUIRED_SCENARIOS:
        raise ValueError("exact four preregistered cells required")
    seeds=list(raw.get("cohort",[]))
    n=len(seeds)
    if n<2 or len(set(seeds))!=n or raw.get("horizon")!=12:
        raise ValueError("independent, fixed twelve-generation seed cohort required")
    cases={}
    compact={}
    for name,group in scenarios.items():
        case=group["case_receipts"]
        if len(case)!=n or [x["seed"] for x in case]!=seeds:
            raise ValueError("matched full seed set missing for scenario")
        cases[name]=case
        measured=group["summary"]
        if measured["n"]!=n:
            raise ValueError("summary denominator inconsistent with exact rows")
        for endpoint in ENDPOINTS:
            if sum(bool(x[endpoint]) for x in case)!=measured["events"][endpoint]:
                raise ValueError("summary vs case-level source disagreement")
        compact[name]={
            "initial_q":group["initial_q"],
            "initial_allele_frequency":group["initial_allele_frequency"],
            "initial_fitness_z1":group["source_initial_high_trait_fitness"],
            "events":{name:measured["events"][name] for name in ENDPOINTS},
            "rates":{name:measured["events"][name]/n for name in ENDPOINTS},
            "first_return_conditional_probability":measured["initial_one_step_expression_probability"],
            "mean_next_q":measured["mean_q_at_generation_1"],
            "mean_second_q":measured["mean_q_at_generation_2"],
            "mean_expressed_snapshots":measured["mean_expressed_snapshots"],
            "mean_genetic_latent_unexpressed_snapshots":measured["mean_latent_but_unexpressed_snapshots"],
        }
    # Pre-create common seed-index bootstrap resamples. All scenarios use
    # identical resampled seed indices, reflecting grouping by seed number.
    rng=Random(bootstrap_seed)
    draws=[[rng.randrange(n) for _ in range(n)] for _ in range(bootstrap_reps)]
    contrasts={}
    for contrast,a,b in CONTRASTS:
        outcomes={}
        for endpoint in ENDPOINTS:
            diffs=[int(cases[a][i][endpoint])-int(cases[b][i][endpoint])
                   for i in range(n)]
            estimates=sorted(
                sum(diffs[j] for j in sample)/n for sample in draws)
            lower=estimates[int(.025*(bootstrap_reps-1))]
            upper=estimates[int(.975*(bootstrap_reps-1))]
            outcomes[endpoint]={
                "difference_A_minus_B":sum(diffs)/n,
                "seed_bootstrap_percentile_95_interval":[lower,upper],
                "A_only":sum(x>0 for x in diffs),
                "B_only":sum(x<0 for x in diffs),
                "neither_discordant":sum(x==0 for x in diffs),
                "bootstrap_not_confirmatory":True,
            }
        contrasts[contrast]={
            "A":a,"B":b,
            "comparison_type":"exploratory_posthoc_source_simulation",
            "outcomes":outcomes,
        }
    return {
        "status":"EXECUTED_SOURCE_RECEIPT_VERIFIED_EXPLORATORY_SUMMARY",
        "pinned_egc_source_commit":raw["pinned_egc_source_commit"],
        "cohort_min":min(seeds),"cohort_max":max(seeds),
        "seed_count":n,
        "horizon":raw["horizon"],
        "scenarios":compact,
        "seed_group_bootstrap":{"reps":bootstrap_reps,"seed":bootstrap_seed,
           "unit":"complete simulated seed across all four scenarios",
           "confidence_interval":"empirical 2.5 and 97.5 percentile order statistics",
           "predeclared_confirmatory_test":False,
           "do_not_treat_generations_as_independent":True},
        "contrasts":contrasts,
        "no_natural_flower_or_pollen_observations":True,
        "no_evolutionary_establishment_claim":True,
        "frozen_NEE_numerical_evidence_unchanged":True,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--bootstrap-reps",type=int,default=4096)
    args=p.parse_args()
    raw_bytes=args.input.read_bytes()
    result=audit(json.loads(raw_bytes),args.bootstrap_reps)
    result["input_full_source_receipt_sha256"]=hashlib.sha256(raw_bytes).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    short={
        "seed_count":result["seed_count"],
        "final_occupancy_counts":{
            k:v["events"]["final_expressed"] for k,v in result["scenarios"].items()},
        "final_effects":{
            k:round(c["outcomes"]["final_expressed"]["difference_A_minus_B"],5)
            for k,c in result["contrasts"].items()},
        "not_confirmatory":True,
    }
    print("EGC_REEXPRESSION_EXPLORATORY_SUMMARY "+json.dumps(short,sort_keys=True))


if __name__=="__main__":
    main()
