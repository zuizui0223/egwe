"""Multigeneration eco-genetic sorting versus homogenization: bounded theorems.

This mathematical module generalizes the original ONE-STEP local selection
log-odds identity without committing the biologically false replacement
'allele-frequency migration = mixing log-odds'.

Parts:
1. Exact causal q-dependent selection contrast under actual p-frequency
   mixing and affine q mixing. Does not imply total Cov(q,p) must rise.
2. Repeated local selection under fixed q: log-odds covariance grows while
   allele-frequency covariance can vanish by fixation.
3. Dobrushin oscillation contraction for a nonnegative row-stochastic
   interaction-mixing kernel P, with additive heterogeneity source eta:
   R(q[t]) <= delta^t R(q0) + sum delta^(t-1-s) R(eta[s]).
   Hence |Cov(q[t],p[t])| <= R_bound/4 whenever p[t] in [0,1].
   This is a universal COVARIANCE UPPER BOUND inside the declared
   partially decoupled update; NOT a persistence/loss or causality theorem.

No natural data, NEE random trials, or biological future outcomes are opened.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable, Sequence


def _finite(values: Sequence[float], name: str) -> list[float]:
    values=[float(x) for x in values]
    if not values or not all(math.isfinite(v) for v in values):
        raise ValueError(f"{name}: need nonempty finite data")
    return values


def covariance(x: Sequence[float],y: Sequence[float]) -> float:
    a=_finite(x,"x")
    b=_finite(y,"y")
    if len(a)!=len(b) or len(a)<2:
        raise ValueError("equal length at least 2 required")
    ma=sum(a)/len(a)
    mb=sum(b)/len(b)
    return sum((ai-ma)*(bi-mb) for ai,bi in zip(a,b))/len(a)


def _p(x:Sequence[float]) -> list[float]:
    p=_finite(x,"allele_frequency")
    if not all(0<=v<=1 for v in p):
        raise ValueError("allele frequencies must be in [0,1]")
    return p


def _q(x:Sequence[float]) -> list[float]:
    q=_finite(x,"interaction")
    if not all(0<=v<=1 for v in q):
        raise ValueError("interaction values must be in [0,1]")
    return q


def logistic(x:float) -> float:
    if x>=0:
        z=math.exp(-x)
        return 1/(1+z)
    z=math.exp(x)
    return z/(1+z)


def relative_fitness(q:float) -> float:
    """The frozen EGWE local allele-selection relative fitness."""
    return .75+.4*q


def selection(p:float,q:float,w:Callable[[float],float]=relative_fitness) -> float:
    if not (math.isfinite(p) and math.isfinite(q) and 0<=p<=1 and 0<=q<=1):
        raise ValueError("finite p,q in [0,1] required")
    fitness=float(w(q))
    if not (math.isfinite(fitness) and fitness>0):
        raise ValueError("relative fitness must be positive and finite")
    return p*fitness/(1-p+p*fitness)


def _homogenize(values:Sequence[float],rate:float) -> list[float]:
    if not (math.isfinite(rate) and 0<=rate<=1):
        raise ValueError("mixing rate must lie in [0,1]")
    vec=_finite(values,"mixing vector")
    mean=sum(vec)/len(vec)
    return [(1-rate)*v+rate*mean for v in vec]


def selection_vs_uniform_q(
    q:Sequence[float],
    p:Sequence[float],
    q_mixing_rate:float=0.,
    allele_mixing_rate:float=0.,
    w:Callable[[float],float]=relative_fitness,
    fitness_direction:str="increasing",
) -> dict:
    """Freeze q,p; compare real local selection with reference q_i=mean(q).

    Both counterfactual arms receive identical true allele-frequency mixing,
    and the same ecological q homogenization. The direct edge contrast is
    lambda*Cov(q, selection(p,q)-selection(p,mean(q))).
    Monotone fitness direction fixes its sign for arbitrary heterogeneous p.
    This does NOT imply total Cov(q,p) increases over a time step.
    """
    qq=_q(q)
    pp=_p(p)
    if len(qq)!=len(pp) or len(qq)<2:
        raise ValueError("matched patch vectors required")
    if fitness_direction not in {"increasing","decreasing","constant","unspecified"}:
        raise ValueError("fitness_direction invalid")
    qm=sum(qq)/len(qq)
    selected=[selection(pi,qi,w) for pi,qi in zip(pp,qq)]
    control=[selection(pi,qm,w) for pi in pp]
    next_q=_homogenize(qq,q_mixing_rate)
    next_p=_homogenize(selected,allele_mixing_rate)
    next_control=_homogenize(control,allele_mixing_rate)
    observed=covariance(next_q,next_p)-covariance(next_q,next_control)
    lambda_factor=(1-q_mixing_rate)*(1-allele_mixing_rate)
    theoretical=lambda_factor*covariance(
        qq,[a-b for a,b in zip(selected,control)])
    if fitness_direction!="unspecified":
        values=[float(w(qi)) for qi in sorted(set(qq))]
        if not all(math.isfinite(z) and z>0 for z in values):
            raise ValueError("invalid fitness values")
        diff=[values[i+1]-values[i] for i in range(len(values)-1)]
        if fitness_direction=="increasing" and any(x<-1e-12 for x in diff):
            raise ValueError("declared fitness direction contradicted")
        if fitness_direction=="decreasing" and any(x>1e-12 for x in diff):
            raise ValueError("declared fitness direction contradicted")
        if fitness_direction=="constant" and any(abs(x)>1e-12 for x in diff):
            raise ValueError("declared fitness direction contradicted")
    return {
        "prior_frequency_covariance":covariance(qq,pp),
        "after_frequency_covariance":covariance(next_q,next_p),
        "after_counterfactual_uniform_q_covariance":covariance(next_q,next_control),
        "direct_selection_edge_covariance_effect":observed,
        "exact_decomposition_effect":theoretical,
        "mixing_attenuation_product":lambda_factor,
        "declared_fitness_direction":fitness_direction,
        "allele_mixing_on_frequencies_not_log_odds":True,
        "later_fate_inferred":False,
        "natural_ecological_estimate":False,
    }


def fixed_q_selection_trajectory(
    q:Sequence[float],p0:Sequence[float],horizons:Sequence[int],
    w:Callable[[float],float]=relative_fitness,
) -> list[dict]:
    """Analytic deterministic u_i(t)=u_i(0)+t log w(q_i), with q frozen.

    Use log odds formula rather than iterating rounded allele frequencies,
    so exact mathematical long-time behavior is not obscured by rounding.
    """
    qq=_q(q);pp=_p(p0)
    if len(qq)!=len(pp) or len(qq)<2 or any(not 0<pi<1 for pi in pp):
        raise ValueError("interior matching frequencies required for log odds")
    u=[math.log(pi/(1-pi)) for pi in pp]
    fitness=[float(w(qi)) for qi in qq]
    if any(not math.isfinite(v) or v<=0 for v in fitness):
        raise ValueError("positive fitness needed")
    h=[math.log(x) for x in fitness]
    gh=covariance(qq,h)
    q_range=max(qq)-min(qq)
    result=[]
    for t in horizons:
        if not isinstance(t,int) or isinstance(t,bool) or t<0:
            raise ValueError("nonnegative integer horizon required")
        u_t=[ui+t*hi for ui,hi in zip(u,h)]
        p_t=[logistic(z) for z in u_t]
        bound=None
        if all(v>1 for v in fitness):
            max_deficit_bound=max((1-pi)/pi*math.exp(-t*math.log(wi))
                                  for pi,wi in zip(pp,fitness))
            bound=q_range*min(1.,max_deficit_bound)/4
        result.append({
            "generation":t,
            "allele_frequency_covariance":covariance(qq,p_t),
            "allele_log_odds_covariance":covariance(qq,u_t),
            "log_odds_slope_per_generation":gh,
            "all_fitness_above_one":all(v>1 for v in fitness),
            "gruss_fixation_bound_when_all_favored":bound,
            "gene_frequency_values_for_synthetic_audit":p_t,
            "no_stochastic_drift_or_migration":True,
        })
    return result


def validate_stochastic_matrix(matrix:Sequence[Sequence[float]]) -> list[list[float]]:
    rows=[_finite(row,"stochastic_matrix row") for row in matrix]
    n=len(rows)
    if n<2 or any(len(row)!=n or any(x<0 for x in row)
                  or abs(sum(row)-1)>1e-10 for row in rows):
        raise ValueError("require square nonnegative row-stochastic matrix")
    return rows


def dobrushin_coefficient(matrix:Sequence[Sequence[float]]) -> float:
    P=validate_stochastic_matrix(matrix)
    return .5*max(sum(abs(a-b) for a,b in zip(P[i],P[j]))
                   for i in range(len(P)) for j in range(len(P)))


def _range(x:Sequence[float]) -> float:
    return max(x)-min(x)


def _matrix_vec(P:list[list[float]],v:list[float]) -> list[float]:
    return [sum(a*b for a,b in zip(row,v)) for row in P]


def mixing_trajectory(
    q0:Sequence[float],
    p0:Sequence[float],
    matrix:Sequence[Sequence[float]],
    allele_mixing_rate:float,
    eta_by_step:Sequence[Sequence[float]],
    w:Callable[[float],float]=relative_fitness,
) -> dict:
    """Evaluate q[t+1]=P q[t]+eta[t], p[t+1]=(1-m)S(p[t],q[t])+m mean S.

    eta can represent an independently bounded spatial source of local
    interaction heterogeneity; the theorem does NOT assert it was causally
    produced by any particular recruitment, pollinator, or eco-feedback edge.
    """
    P=validate_stochastic_matrix(matrix)
    q=_q(q0);p=_p(p0)
    n=len(q)
    if len(p)!=n or len(P)!=n:
        raise ValueError("matching plant/patch count required")
    m=float(allele_mixing_rate)
    if not math.isfinite(m) or not 0<=m<=1:
        raise ValueError("allele-frequency mixing rate outside [0,1]")
    delta=dobrushin_coefficient(P)
    bound_r=_range(q)
    rows=[{
        "generation":0,
        "actual_interaction_range":_range(q),
        "certified_interaction_range_bound":bound_r,
        "actual_allele_frequency_covariance":covariance(q,p),
        "certified_covariance_absolute_upper":bound_r/4,
        "interlayer_functional_fate_evaluated":False,
    }]
    for time,source in enumerate(eta_by_step,start=1):
        eta=_finite(source,"heterogeneity_source")
        if len(eta)!=n:
            raise ValueError("forcing vector incompatible with patches")
        # The allele step is physical allele-frequency averaging, not
        # synthetic log-odds mixing.
        selected=[selection(pi,qi,w) for pi,qi in zip(p,q)]
        p=_homogenize(selected,m)
        q_raw=_matrix_vec(P,q)
        q=[v+e for v,e in zip(q_raw,eta)]
        _q(q)
        bound_r=delta*bound_r+_range(eta)
        actual_r=_range(q)
        actual_c=abs(covariance(q,p))
        if actual_r>bound_r+1e-9 or actual_c>bound_r/4+1e-9:
            raise AssertionError("Dobrushin / Gruss bound violated")
        rows.append({
            "generation":time,
            "actual_interaction_range":actual_r,
            "certified_interaction_range_bound":bound_r,
            "actual_allele_frequency_covariance":covariance(q,p),
            "certified_covariance_absolute_upper":bound_r/4,
            "heterogeneity_source_range":_range(eta),
            "interlayer_functional_fate_evaluated":False,
        })
    return {
        "status":"EXACT_MIXING_SOURCE_COVARIANCE_BOUND",
        "dobrushin_delta":delta,
        "kernel_is_row_stochastic":True,
        "allele_migration_on_frequencies":True,
        "trajectory":rows,
        "last_covariance_upper":bound_r/4,
        "all_future_function_unobserved":True,
        "interpretation":"Conditional bounds on covariance, not a survival/loss theorem",
    }


def demonstration() -> dict:
    q=[.7,.9]
    p=[.5,.999]
    edge=selection_vs_uniform_q(q,p,fitness_direction="increasing")
    fixed=fixed_q_selection_trajectory(q,p,[0,10,100,1000])
    matrix=[
        [.8,.2,0],
        [.15,.7,.15],
        [0,.2,.8],
    ]
    zero=mixing_trajectory([.2,.7,.9],[.3,.7,.9],matrix,.15,
                           [[0,0,0] for _ in range(30)])
    sourced=mixing_trajectory([.2,.7,.9],[.3,.7,.9],matrix,.15,
                              [[-.01,0,.01] for _ in range(30)])
    return {
        "provenance":"ALGEBRA_AND_SYNTHETIC_DETERMINISTIC_LIFECYCLE_ONLY",
        "local_real_frequency_counterexample":edge,
        "frozen_q_multigeneration":fixed,
        "network_homogenization_no_source":zero,
        "network_mixing_with_heterogeneity_source":sourced,
        "natural_HR_validated":False,
        "long_horizon_ecological_function_predicted":False,
        "frozen_NEE_model_mutated":False,
    }


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    result=demonstration()
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    effect=result["local_real_frequency_counterexample"]
    print("MULTIGENERATION_SORTING_MIXING "+json.dumps({
        "causal_q_selection_edge":effect["direct_selection_edge_covariance_effect"],
        "total_allele_frequency_covariance_change":(
            effect["after_frequency_covariance"]-
            effect["prior_frequency_covariance"]),
        "fixed_q_log_odds_covariance_t1000":result["frozen_q_multigeneration"][-1]["allele_log_odds_covariance"],
        "fixed_q_allele_frequency_covariance_t1000":result["frozen_q_multigeneration"][-1]["allele_frequency_covariance"],
        "network_dobrushin":zero["dobrushin_delta"],
        "no_natural_result":not result["natural_HR_validated"],
    },sort_keys=True))


if __name__=="__main__":
    main()
