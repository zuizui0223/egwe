"""Exact worst-case planning for which tagged plants to monitor.

Extends sharp visit/genotype covariance bounds. The measurement set is chosen
using pre-outcome G, effort and externally justified visit caps. This is NOT
a posterior outcome fit or real-plant data analysis.

When a set S is monitored with exact, matching-window counts v_S, the
uncertainty width depends only on R=V-sum(v_S), the remaining visit total.
For fixed S, R lies in [max(0,V-sum(caps_S)), min(V,sum(caps_notS))].
The extrema over R of the piecewise-linear interval width occur at endpoints
or at cumulative caps in ascending/descending remaining coefficient order.
Enumerating those finitely many knots gives an EXACT continuous min-max plan.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Sequence

from visit_allocation_identifiability import (
    _greedy,
    _values,
    sharp_covariance_bounds,
)

MAX_COMBINATIONS=250_000
TOL=1e-9


def _prepare(
    genetic_state: Sequence[float], total_visits: float,
    effort: Sequence[float] | None,
    caps: Sequence[float] | None,
) -> tuple[list[float],float,list[float],list[float],list[float]]:
    g=_values("genetic_state", genetic_state)
    total=float(total_visits)
    if not math.isfinite(total) or total<0:
        raise ValueError("total_visits must be finite and nonnegative")
    n=len(g)
    e=_values("effort", effort if effort is not None else [1.0]*n)
    if len(e)!=n or any(x<=0 for x in e):
        raise ValueError("positive effort required for each plant")
    u=_values("caps", caps if caps is not None else [total]*n)
    if len(u)!=n or any(x<0 for x in u):
        raise ValueError("finite nonnegative visit caps required for each plant")
    if sum(u)+TOL<total:
        raise ValueError("visit caps cannot accommodate the observed total")
    mean=sum(g)/n
    weights=[(x-mean)/(n*t) for x,t in zip(g,e)]
    return g,total,e,u,weights


def _remaining_bounds(
    weights: list[float], caps: list[float], remaining: Sequence[int],
    unassigned_total: float,
) -> tuple[float,float,list[float],list[float]]:
    low, allocation_lo=_greedy(
        [weights[i] for i in remaining],unassigned_total,
        [caps[i] for i in remaining],largest=False)
    high, allocation_hi=_greedy(
        [weights[i] for i in remaining],unassigned_total,
        [caps[i] for i in remaining],largest=True)
    return low,high,allocation_lo,allocation_hi


def worst_case_width(
    weights: Sequence[float],
    total_visits: float,
    caps: Sequence[float],
    monitored: Sequence[int],
) -> dict:
    """Exact supremum of residual covariance interval width before monitoring.

    This maximizes over all *feasible values* for as-yet-unobserved tagged
    visits, not over a guessed probability distribution of visiting insects.
    """
    w=list(weights)
    u=list(caps)
    n=len(w)
    chosen=tuple(monitored)
    if len(set(chosen))!=len(chosen) or any(i<0 or i>=n for i in chosen):
        raise ValueError("monitored indices must be unique and in range")
    remaining=[i for i in range(n) if i not in chosen]
    s=float(total_visits)
    lower_r=max(0.0,s-sum(u[i] for i in chosen))
    upper_r=min(s,sum(u[i] for i in remaining))
    if lower_r>upper_r+TOL:
        raise ValueError("no feasible allocation under visit caps")
    knots={lower_r,upper_r}
    for reverse in (False,True):
        running=0.0
        for i in sorted(remaining,key=lambda j:w[j],reverse=reverse):
            running+=u[i]
            if lower_r-TOL<=running<=upper_r+TOL:
                knots.add(max(lower_r,min(upper_r,running)))

    evaluations=[]
    for r in sorted(knots):
        lo,hi,_,_=_remaining_bounds(w,u,remaining,r)
        evaluations.append((max(0.0,hi-lo),r))
    width,r_star=max(evaluations,key=lambda pair:(pair[0],-pair[1]))
    return {
        "monitored_indices":list(chosen),
        "unmonitored_indices":remaining,
        "worst_case_sharp_width":width,
        "worst_case_remaining_total":r_star,
        "possible_remaining_total_range":[lower_r,upper_r],
        "evaluated_knot_count":len(evaluations),
        "all_monitored_counts_unobserved_at_plan_time":True,
        "criterion":"minimize maximum post-measurement sharp interval width",
    }


def select_monitored_plants(
    genetic_state: Sequence[float], site_total_visits: float,
    monitor_budget: int, effort: Sequence[float] | None = None,
    visit_caps: Sequence[float] | None = None,
    plant_ids: Sequence[str] | None = None,
) -> dict:
    """Minimax-optimal *simultaneous exact-count* monitoring subset.

    A single visit counter per tagged plant is assumed to cover exactly the
    same interval and visit-total denominator. A five-camera allocation is
    NOT five statistically independent replicate sites.
    """
    g,v,e,u,weights=_prepare(genetic_state,site_total_visits,effort,visit_caps)
    n=len(g)
    if not isinstance(monitor_budget,int) or isinstance(monitor_budget,bool) or not (0<=monitor_budget<=n):
        raise ValueError("monitor budget must be an integer from zero to n")
    ids=list(plant_ids) if plant_ids is not None else [f"plant_{i+1}" for i in range(n)]
    if len(ids)!=n or len(set(ids))!=n or not all(isinstance(i,str) and i for i in ids):
        raise ValueError("plant ids must be unique nonblank strings of length n")
    if math.comb(n,monitor_budget)>MAX_COMBINATIONS:
        raise ValueError("too many exact subsets; no heuristic plan silently substituted")
    baseline=sharp_covariance_bounds(g,v,e,u)
    baseline_width=baseline["covariance_upper_sharp"]-baseline["covariance_lower_sharp"]
    plans=[worst_case_width(weights,v,u,subset)
           for subset in itertools.combinations(range(n),monitor_budget)]
    optimal=min(p["worst_case_sharp_width"] for p in plans)
    winners=[p for p in plans if p["worst_case_sharp_width"]<=optimal+TOL]
    selected=winners[0]
    return {
        "status":"EXACT_MINIMAX_DESIGN_SYNTHETIC_OR_DECLARED_INPUT",
        "monitor_budget":monitor_budget,
        "unit_ids":ids,
        "selected_indices":selected["monitored_indices"],
        "selected_plant_ids":[ids[i] for i in selected["monitored_indices"]],
        "tied_optimal_subsets":[[ids[i] for i in p["monitored_indices"]]
                                for p in winners],
        "baseline_sharp_interval":[baseline["covariance_lower_sharp"],baseline["covariance_upper_sharp"]],
        "baseline_width":baseline_width,
        "optimal_worst_case_width":optimal,
        "minimum_guaranteed_width_reduction":baseline_width-optimal,
        "plan_count_checked":len(plans),
        "all_subsets_checked":len(plans)==math.comb(n,monitor_budget),
        "ranked_plans":[{
            "selected_plant_ids":[ids[i] for i in p["monitored_indices"]],
            "worst_case_width":p["worst_case_sharp_width"],
            "worst_case_remaining_total":p["worst_case_remaining_total"]
        } for p in sorted(plans,
            key=lambda d:(d["worst_case_sharp_width"],d["monitored_indices"]))],
        "local_visits_observed":False,
        "outcomes_opened":False,
        "no_real_ulex_allocation_inferred":True,
        "claim_ceiling":"Conditional math planning only; no detection-error or ecological effect estimate.",
    }


def conditional_bounds_after_monitoring(
    genetic_state: Sequence[float],
    site_total_visits: float,
    tagged_exact_visits: dict[int,float],
    effort: Sequence[float] | None = None,
    visit_caps: Sequence[float] | None = None,
) -> dict:
    """Update sharp interval when exact same-window individual counts arrive."""
    g,v,e,u,weights=_prepare(genetic_state,site_total_visits,effort,visit_caps)
    keys=list(tagged_exact_visits)
    if any(not isinstance(i,int) or isinstance(i,bool) or i<0 or i>=len(g) for i in keys):
        raise ValueError("tagged visit map must use valid integer plant indices")
    fixed=0.0
    for i,x in tagged_exact_visits.items():
        if not math.isfinite(float(x)) or float(x)<0 or float(x)>u[i]+TOL:
            raise ValueError("tagged count is invalid or above prespecified cap")
        fixed+=float(x)
    residual=v-fixed
    remaining=[i for i in range(len(g)) if i not in tagged_exact_visits]
    if residual< -TOL or residual>sum(u[i] for i in remaining)+TOL:
        raise ValueError("tagged counts incompatible with site total")
    residual=max(0.0,residual)
    lo,hi,_,_=_remaining_bounds(weights,u,remaining,residual)
    known=sum(weights[i]*float(x) for i,x in tagged_exact_visits.items())
    return {
        "status":"SHARP_CONDITIONAL_INTERVAL_FROM_EXACT_TAGGED_COUNTS",
        "monitored_indices":sorted(keys),
        "remaining_total_visits":residual,
        "covariance_lower_sharp":known+lo,
        "covariance_upper_sharp":known+hi,
        "interval_width":hi-lo,
        "future_function_observed":False,
        "predictive_test_performed":False,
        "claim_ceiling":"Exact-count measurement assumption; not field-ready under unvalidated camera errors.",
    }


def demonstration() -> dict:
    result=select_monitored_plants(
        [.1,.3,.7,.9],20,2,effort=[1]*4,visit_caps=[8]*4,
        plant_ids=["g_lowest","g_low","g_high","g_highest"])
    result["data_provenance"]="SYNTHETIC_ONLY_NOT_ULEX_OR_ANY_FIELD_DATA"
    return result


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    args=p.parse_args()
    report=demonstration()
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("MONITOR_PLACEMENT "+json.dumps({
        "selected":report["selected_plant_ids"],
        "baseline_width":report["baseline_width"],
        "minimax_worst_width":report["optimal_worst_case_width"],
        "number_of_optimal_subsets":len(report["tied_optimal_subsets"]),
        "provenance":report["data_provenance"],
    },sort_keys=True))


if __name__=="__main__":
    main()
