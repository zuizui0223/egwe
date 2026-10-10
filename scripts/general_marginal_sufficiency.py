"""Classical mixed-difference / rearrangement generalization of EGWE Q2.

Scope: aggregate ONE-STEP observable sum F(x_i,y_{pi(i)}) over patches
with equal weights and freely permutable pairings. Not a result about
labelled next-state vectors, multi-generation stochastic fate or nature.

Provides:
* an exact rational table criterion for aggregate marginal sufficiency;
* local swap difference and exhaustive pairing extrema;
* analytic logistic curvature sign including threshold reversal;
* monotone selection log-odds spatial covariance identity.
All numerical demonstrations are mathematical/synthetic, not field data.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
import math
from typing import Callable, Sequence


def exact_grid_additivity(values: Sequence[Sequence[int|str|Fraction]]) -> dict:
    """Exact if-and-only-if finite-product-grid separability check.

    Rows index potential x_i and columns potential y_j. Inputs are exact
    integers, rational strings (e.g. '3/7') or Fraction objects, never
    binary floating-point approximations. Additivity on the full product
    grid is equivalent to ALL rectangle mixed differences being zero.
    """
    table=[[Fraction(x) for x in row] for row in values]
    if len(table)<2 or len(table[0])<2:
        raise ValueError("must supply at least a 2 by 2 product grid")
    cols=len(table[0])
    if any(len(row)!=cols for row in table):
        raise ValueError("ragged product grid")
    x_component=[table[i][0] for i in range(len(table))]
    y_component=[table[0][j]-table[0][0] for j in range(cols)]
    for i,row in enumerate(table):
        for j,v in enumerate(row):
            residual=v-x_component[i]-y_component[j]
            if residual:
                return {
                    "additively_separable":False,
                    "global_pairing_invariance_for_all_marginals":False,
                    "witness_rectangle_indices":[0,i,0,j],
                    "witness_exact_mixed_difference":str(residual),
                    "claim_scope":"aggregate one-step sum, not labelled-vector sufficiency",
                }
    return {
        "additively_separable":True,
        "global_pairing_invariance_for_all_marginals":True,
        "x_component":[str(a) for a in x_component],
        "y_component":[str(b) for b in y_component],
        "claim_scope":"aggregate one-step sum, not labelled-vector sufficiency",
    }


def swap_gap(
    f: Callable[[float,float],float],
    x_low: float,x_high: float,y_low: float,y_high: float,
) -> float:
    """Aligned minus swapped aggregate contribution, given strict orders."""
    if not (x_low<x_high and y_low<y_high):
        raise ValueError("swap requires strictly increasing x and y pairs")
    return (f(x_low,y_low)+f(x_high,y_high)
            -f(x_low,y_high)-f(x_high,y_low))


def logistic(value: float) -> float:
    """Stable sigmoid."""
    if value>=0:
        exp=math.exp(-value)
        return 1/(1+exp)
    exp=math.exp(value)
    return exp/(1+exp)


def logistic_update(
    x: float,y: float,*,alpha:float=0.6,beta:float=0.4,
    kappa:float=4.5,theta:float=0.5025,
) -> float:
    if not all(math.isfinite(z) for z in (x,y,alpha,beta,kappa,theta)):
        raise ValueError("all logistic parameters must be finite")
    if not (alpha>0 and beta>0 and kappa>0):
        raise ValueError("positive coefficients required by curvature signs")
    return logistic(kappa*(alpha*x+beta*y-theta))


def logistic_cross_partial(
    x:float,y:float,*,alpha:float=0.6,beta:float=0.4,
    kappa:float=4.5,theta:float=0.5025,
) -> float:
    """Exact cross partial for sigmoid(kappa*(alpha*x+beta*y-theta))."""
    output=logistic_update(x,y,alpha=alpha,beta=beta,kappa=kappa,theta=theta)
    return (kappa*kappa*alpha*beta*
            output*(1-output)*(1-2*output))


def logistic_rectangle_regime(
    x_low:float,x_high:float,y_low:float,y_high:float,*,
    alpha:float=0.6,beta:float=0.4,kappa:float=4.5,theta:float=0.5025,
) -> str:
    """Rigorous sufficient sign regime; crossing threshold is NOT a sign proof."""
    if not (x_low<x_high and y_low<y_high):
        raise ValueError("rectangle requires strict ordering")
    if not (alpha>0 and beta>0 and kappa>0):
        raise ValueError("positive coefficients are necessary")
    lo=alpha*x_low+beta*y_low
    hi=alpha*x_high+beta*y_high
    if hi<theta:
        return "strictly_supermodular_below_inflection"
    if lo>theta:
        return "strictly_submodular_above_inflection"
    return "mixed_or_touching_threshold_no_global_order"


def exhaustive_pairing_extrema(
    x:Sequence[float], y:Sequence[float],f:Callable[[float,float],float],
) -> dict:
    """Small-n verification; does not claim a unique optimum when tied."""
    xx=list(map(float,x));yy=list(map(float,y))
    if len(xx)!=len(yy) or len(xx)<2 or len(xx)>8:
        raise ValueError("need 2..8 paired units")
    if not all(math.isfinite(z) for z in xx+yy):
        raise ValueError("nonfinite components")
    items=[]
    for pairing in itertools.permutations(range(len(xx))):
        total=sum(f(xx[i],yy[j]) for i,j in enumerate(pairing))
        items.append((total,list(pairing)))
    mi=min(item[0] for item in items);ma=max(item[0] for item in items)
    # Sorted/counter-sorted pairings for strict x rank; based on
    # stable sort, no assumptions about identical states.
    ix=sorted(range(len(xx)),key=lambda i:xx[i])
    iy=sorted(range(len(yy)),key=lambda i:yy[i])
    aligned=[0]*len(xx);reversed_match=[0]*len(xx)
    for i,j in zip(ix,iy):
        aligned[i]=j
    for i,j in zip(ix,reversed(iy)):
        reversed_match[i]=j
    def score(pair):
        return sum(f(xx[i],yy[j]) for i,j in enumerate(pair))
    return {
        "n":len(xx),
        "permutations_tested":len(items),
        "minimum_sum":mi,
        "maximum_sum":ma,
        "aligned_sum":score(aligned),
        "reversed_sum":score(reversed_match),
        "aligned_pairing":aligned,
        "reversed_pairing":reversed_match,
        "one_step_aggregate_only":True,
    }


def population_covariance(x:Sequence[float],y:Sequence[float]) -> float:
    if len(x)!=len(y) or len(x)<2:
        raise ValueError("matching at least two samples required")
    mx=sum(x)/len(x);my=sum(y)/len(y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/len(x)


def selection_covariance_identity(
    q:Sequence[float],p:Sequence[float],*,
    w:Callable[[float],float]=lambda x:0.75+0.4*x,
) -> dict:
    """Deterministic log-odds selection only, before migration/drift/mutation."""
    qq=list(map(float,q));pp=list(map(float,p))
    if len(qq)!=len(pp) or len(qq)<2:
        raise ValueError("q and p must be matched patches")
    if any(not math.isfinite(x) for x in qq+pp) or any(not 0<x<1 for x in pp):
        raise ValueError("finite q and interior allele frequencies required")
    fitness=[float(w(x)) for x in qq]
    if any(not math.isfinite(a) or a<=0 for a in fitness):
        raise ValueError("positive fitness multipliers required")
    u=[math.log(a/(1-a)) for a in pp]
    h=[math.log(a) for a in fitness]
    before=population_covariance(qq,u)
    after=population_covariance(qq,[a+b for a,b in zip(u,h)])
    n=len(qq)
    pair_sum=sum(
        (qq[i]-qq[j])*(h[i]-h[j])
        for i in range(n) for j in range(n))/(2*n*n)
    return {
        "before_covariance":before,
        "after_covariance":after,
        "selection_induced_delta":after-before,
        "pairwise_covariance_identity":pair_sum,
        "nonnegative_fitness_difference_ordered":all(
            (qq[i]-qq[j])*(h[i]-h[j])>=-1e-12
            for i in range(n) for j in range(n)),
        "claim_scope":"deterministic local selection log-odds step only",
    }


def demonstration() -> dict:
    alpha=.6;beta=.4;kappa=4.5
    x=(.2,.4); y=(.2,.4)
    two=[]
    for theta in (.1,.8):
        f=lambda xx,yy,th=theta:logistic_update(
            xx,yy,alpha=alpha,beta=beta,kappa=kappa,theta=th)
        two.append({
            "theta":theta,
            "regime":logistic_rectangle_regime(*x,*y,
                 alpha=alpha,beta=beta,kappa=kappa,theta=theta),
            "aligned_minus_swapped":swap_gap(f,*x,*y),
        })
    q=[.65,.75,.85,.95]; b=[.2,.4,.6,.8]
    local=exhaustive_pairing_extrema(
        q,b,lambda a,t:logistic_update(a,t))
    local["actual_canonical_input_template_only"]=True
    local["future_fate_predicted"]=False
    selection=selection_covariance_identity(
        q,[.25,.4,.6,.75])
    return {
        "data_provenance":"ALGEBRA_AND_DECLARED_EGWE_SYNTHETIC_CLOSURE_ONLY",
        "finite_grid_example":exact_grid_additivity(
            [["0","0","0"],["0","1","2"],["0","2","4"]]),
        "sigmoid_sign_reversal_examples":two,
        "locked_operator_one_step_aggregate_example":local,
        "selection_operator_identity_example":selection,
        "long_horizon_fate_claim":False,
        "natural_empirical_validation_claim":False,
    }


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    args=p.parse_args()
    from pathlib import Path
    result=demonstration()
    file=Path(args.output)
    file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("GENERAL_COUPLING_AUDIT "+json.dumps({
        "discrete_grid_separable":result["finite_grid_example"]["additively_separable"],
        "logistic_signs":[r["aligned_minus_swapped"] for r in result["sigmoid_sign_reversal_examples"]],
        "canonical_aggregate_difference":(
          result["locked_operator_one_step_aggregate_example"]["aligned_sum"]-
          result["locked_operator_one_step_aggregate_example"]["reversed_sum"]),
        "selection_covariance_delta":result["selection_operator_identity_example"]["selection_induced_delta"],
        "no_natural_validation":not result["natural_empirical_validation_claim"],
    },sort_keys=True))


if __name__=="__main__":
    main()
