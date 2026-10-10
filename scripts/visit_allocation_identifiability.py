"""Sharp partial-identification bounds for plant-level interaction × genetic state.

Only observes a site-wide total visit count V and individually measured
pre-outcome genetic/trait coordinates G_i and effort E_i; plant-specific visits
v_i are *not* observed. The bounds do not impute visits or fit outcomes.

C(v,G) = (1/n) sum_i (G_i - mean(G)) (v_i/E_i).
Subject to sum(v_i)=V and 0 <= v_i <= upper_i, where upper_i is optional.
The linear objective is extremized by greedy allocation in ascending or
descending order of coefficient (G_i - mean(G))/(n E_i).
"""
from __future__ import annotations

import argparse
import json
import math
from typing import Sequence


def _values(name: str, values: Sequence[float]) -> list[float]:
    out=[float(v) for v in values]
    if not out or any(not math.isfinite(v) for v in out):
        raise ValueError(f"{name} must be nonempty and all finite")
    return out


def _greedy(weights: list[float], total: float, caps: list[float],
            largest: bool) -> tuple[float,list[float]]:
    remaining=total
    allocated=[0.0]*len(weights)
    for i in sorted(range(len(weights)),key=lambda j:weights[j],reverse=largest):
        amount=min(remaining,caps[i])
        allocated[i]=amount
        remaining-=amount
        if remaining<=1e-10:
            remaining=0.0
            break
    if remaining>1e-8:
        raise ValueError("total exceeds feasible per-plant visit caps")
    return sum(a*b for a,b in zip(allocated,weights)),allocated


def sharp_covariance_bounds(
    genetic_state: Sequence[float],
    site_total_visits: float,
    effort: Sequence[float] | None = None,
    visit_caps: Sequence[float] | None = None,
) -> dict:
    """Bound population covariance of unknown local visit rates and G.

    These are *algebraic feasibility bounds*, not statistical confidence
    intervals. Equal-weight plants/patches are assumed; optional effort
    converts visit counts to rates. Caps represent externally justified upper
    bounds on counts, not estimated or chosen from future function outcomes.
    """
    g=_values("genetic_state",genetic_state)
    n=len(g)
    v=float(site_total_visits)
    if not math.isfinite(v) or v<0:
        raise ValueError("site_total_visits must be finite and nonnegative")
    e=_values("effort",effort if effort is not None else [1.0]*n)
    if len(e)!=n or any(x<=0 for x in e):
        raise ValueError("effort must be positive and match genetic_state length")
    caps=_values("visit_caps",visit_caps) if visit_caps is not None else [v]*n
    if len(caps)!=n or any(x<0 for x in caps):
        raise ValueError("visit_caps must be nonnegative and match state length")
    if sum(caps)+1e-8<v:
        raise ValueError("total exceeds feasible per-plant visit caps")

    gbar=sum(g)/n
    weight=[(gi-gbar)/(n*ei) for gi,ei in zip(g,e)]
    lower,min_allocation=_greedy(weight,v,caps,largest=False)
    upper,max_allocation=_greedy(weight,v,caps,largest=True)
    if lower>upper+1e-10:
        raise AssertionError("invalid linear-programming bounds")
    # Allocating visits proportional to *effort* yields a constant plant-level
    # rate; only a hypothetical imputation, and possibly cap-infeasible.
    naive=[v*ei/sum(e) for ei in e]
    naive_feasible=all(x<=c+1e-9 for x,c in zip(naive,caps))
    naive_cov=sum(x*w for x,w in zip(naive,weight))
    tol=1e-10
    if lower<-tol and upper>tol:
        status="sign_not_identified"
    elif abs(lower)<=tol and abs(upper)<=tol:
        status="point_identified_zero"
    elif lower>=-tol:
        status="nonnegative_only"
    elif upper<=tol:
        status="nonpositive_only"
    else:
        status="not_identified"

    return {
        "status":status,
        "number_of_units":n,
        "site_total_visits":v,
        "covariance_lower_sharp":lower,
        "covariance_upper_sharp":upper,
        "minimum_witness_visits":min_allocation,
        "maximum_witness_visits":max_allocation,
        "constant_rate_imputation_covariance":naive_cov,
        "constant_rate_imputation_feasible":naive_feasible,
        "local_visits_observed":False,
        "future_function_observed":False,
        "empirical_effect_estimated":False,
        "statement":"Feasible allocation bounds only; not a biological result or a predictive test.",
    }


def demonstration() -> dict:
    # Synthetic 4-patch example, NEVER Ulex genotypes or visits.
    result=sharp_covariance_bounds(
        genetic_state=[0.1,0.3,0.7,0.9],
        site_total_visits=20,
        effort=[1,1,1,1],
        visit_caps=[8,8,8,8],
    )
    result["data_provenance"]="SYNTHETIC_4_PATCH_ILLUSTRATION_ONLY"
    return result


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    result=demonstration()
    from pathlib import Path
    p=Path(args.output)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("ALLOCATION_BOUNDS "+json.dumps({
        "status":result["status"],
        "sharp_interval":[result["covariance_lower_sharp"],result["covariance_upper_sharp"]],
        "zero_from_site_average":result["constant_rate_imputation_covariance"],
        "provenance":result["data_provenance"],
    },sort_keys=True))


if __name__=="__main__":
    main()
