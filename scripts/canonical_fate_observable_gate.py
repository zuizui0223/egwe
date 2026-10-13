"""Canonical EGWE deterministic next-q functional threshold observables.

Imports the actual pinned update, rather than inventing a Markov transition
kernel. Does not infer future loss or a stochastic hitting probability.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from eco_genetic_warning_extensions.operator_balance_route_margin import next_interaction_from_state

def compare():
    q=[.65,.75,.85,.95]
    bundle=[.2,.4,.6,.8]
    out={}
    for name,bb in (("aligned",bundle),("reversed",list(reversed(bundle)))):
        values=[next_interaction_from_state(x,y,y,1.,.5025) for x,y in zip(q,bb)]
        out[name]={
            "next_q":values,
            "mean_next_q":sum(values)/4,
            "patches_above_0625":sum(v>=.625 for v in values),
            "max_next_q":max(values),
            "min_next_q":min(values),
        }
    return {
        "input_q_marginals":q,"input_trait_and_allele_bundle_marginals":bundle,
        "same_marginals":True,
        "canonical_operator_imported":True,
        "one_step_threshold_count_difference":out["reversed"]["patches_above_0625"]-out["aligned"]["patches_above_0625"],
        "states":out,
        "threshold_is_a_deterministic_next_q_diagnostic_not_loss":True,
        "stochastic_transition_kernel_available":False,
        "future_hitting_probability_computed":False,
        "natural_validation":False,
    }

if __name__=="__main__":
    print(json.dumps(compare(),indent=2))
