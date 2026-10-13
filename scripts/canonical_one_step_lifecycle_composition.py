"""Actual EGWE one-step q, selection, population and recruitment composition.

No claim of complete stochastic multigeneration model or ecological extinction.
"""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from eco_genetic_warning_extensions.operator_balance_route_margin import next_interaction_from_state,selected_high_allele_frequency
from eco_genetic_warning_extensions.density_feedback_gate_theorem import continuous_population_next
from eco_genetic_warning_extensions.recruitment_buffer_theorem import recruit_high_trait_mass

def run():
    q=[.65,.75,.85,.95]
    b=[.2,.4,.6,.8]
    p=[.2,.4,.6,.8]
    outcomes={}
    for label,traits in (("AA",b),("RR",list(reversed(b)))):
        nxt=[next_interaction_from_state(x,t,t,1.,.5025) for x,t in zip(q,traits)]
        selected=[selected_high_allele_frequency(pi,qi) for pi,qi in zip(p,nxt)]
        # Conditional diagnostic only: equal initial N=40 and K=40, consistent with the
        # unit-density assumption that generated q_next above.
        populations=[continuous_population_next(40.,qi,pi,capacity=40.)
                     for qi,pi in zip(nxt,selected)]
        recruited=[recruit_high_trait_mass(t,pi,.5)
                   for t,pi in zip(traits,selected)]
        outcomes[label]={
            "q_next":nxt,"selected_allele":selected,
            "conditional_population_next":populations,
            "conditional_recruit_high_trait_mass":recruited,
            "mean_population_next":sum(populations)/4,
            "minimum_population_next":min(populations),
            "maximum_population_next":max(populations),
            "mean_recruit_mass":sum(recruited)/4,
        }
    return {"status":"CONDITIONAL_ONE_STEP_OPERATOR_COMPOSITION",
            "operator_sources":["operator_balance_route_margin","density_feedback_gate_theorem","recruitment_buffer_theorem"],
            "assumptions":"q update at density 1 from N=K=40, then allele selection, population growth and recruitment; no iterated trait-density feedback",
            "outcomes":outcomes,
            "full_model_long_horizon_loss_estimated":False,
            "stochastic_loss_probability_estimated":False,
            "natural_data_used":False}

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
