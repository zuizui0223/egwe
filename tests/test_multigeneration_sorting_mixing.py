from __future__ import annotations

import importlib.util
import itertools
import math
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location(
    "multigeneration_sorting_mixing",
    ROOT/"scripts/multigeneration_sorting_mixing.py")
assert SPEC and SPEC.loader
THEORY=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(THEORY)


def test_real_allele_frequency_selection_vs_reference_q_exact_decomposition() -> None:
    q=[.2,.4,.65,.9]
    p=[.05,.9,.5,.999]
    for m,r in itertools.product((0,.2,.8,1.),repeat=2):
        data=THEORY.selection_vs_uniform_q(q,p,r,m)
        assert data["direct_selection_edge_covariance_effect"]==pytest.approx(
            data["exact_decomposition_effect"],abs=1e-14)
        assert data["direct_selection_edge_covariance_effect"]>=-1e-14
        assert data["mixing_attenuation_product"]==pytest.approx((1-r)*(1-m))
        assert data["allele_mixing_on_frequencies_not_log_odds"] is True
        if m==1 or r==1:
            assert data["direct_selection_edge_covariance_effect"]==pytest.approx(
                0,abs=1e-14)


def test_isolated_causal_edge_positive_even_when_total_covariance_decreases() -> None:
    # Both patches are above q*=0.625, yet high-q p is almost saturated.
    # The "total covariance increases" shortcut is FALSE on the p scale.
    data=THEORY.selection_vs_uniform_q([.7,.9],[.5,.999])
    actual_increase=(data["after_frequency_covariance"]-
                     data["prior_frequency_covariance"])
    assert actual_increase==pytest.approx(-.00036450763748965137)
    assert data["direct_selection_edge_covariance_effect"]==pytest.approx(
        .0004776350197278449)
    assert data["direct_selection_edge_covariance_effect"]>0
    assert actual_increase<0
    assert data["later_fate_inferred"] is False


def test_causal_edge_sign_flips_under_decreasing_fitness() -> None:
    q=[.2,.4,.9]
    p=[.05,.99,.2]
    negative=THEORY.selection_vs_uniform_q(
        q,p,.1,.3,w=lambda x:1.4-.3*x,fitness_direction="decreasing")
    assert negative["direct_selection_edge_covariance_effect"]<0
    flat=THEORY.selection_vs_uniform_q(
        q,p,.1,.3,w=lambda x:1.1,fitness_direction="constant")
    assert flat["direct_selection_edge_covariance_effect"]==pytest.approx(0,abs=1e-14)


@pytest.mark.parametrize("q,p",[
    ([.2,.8],[.1,.7]),
    ([.05,.5,.8],[.2,.75,.95]),
    ([.7,.9],[.5,.999]),
    ([.8,.8],[.1,.95]),
])
def test_selection_edge_is_nonnegative_for_all_heterogeneous_initial_p(q,p) -> None:
    result=THEORY.selection_vs_uniform_q(q,p,.15,.2)
    assert result["direct_selection_edge_covariance_effect"]>=-1e-14


def test_false_claim_to_migrate_log_odds_not_needed() -> None:
    q=[.2,.8]
    p=[.1,.9]
    real=THEORY.selection_vs_uniform_q(q,p,.3,.4)
    qnext=THEORY._homogenize(q,.3)
    psel=[THEORY.selection(pi,qi) for pi,qi in zip(p,q)]
    realp=THEORY._homogenize(psel,.4)
    assert real["after_frequency_covariance"]==pytest.approx(
        THEORY.covariance(qnext,realp))
    assert 0<=min(realp)<=max(realp)<=1


def test_fixed_q_multigeneration_logit_sorting_grows_but_p_covariance_vanishes() -> None:
    rows=THEORY.fixed_q_selection_trajectory([.7,.9],[.5,.999],
                                              [0,10,100,1000])
    assert rows[0]["allele_frequency_covariance"]>0
    assert rows[1]["allele_frequency_covariance"]<rows[0]["allele_frequency_covariance"]
    assert rows[-1]["allele_frequency_covariance"]<1e-10
    assert rows[-1]["allele_log_odds_covariance"]>rows[0]["allele_log_odds_covariance"]
    slope=rows[0]["log_odds_slope_per_generation"]
    assert slope>0
    for row in rows:
        assert row["allele_log_odds_covariance"]==pytest.approx(
            rows[0]["allele_log_odds_covariance"]+row["generation"]*slope,
            abs=1e-11)
        assert row["all_fitness_above_one"] is True
        assert abs(row["allele_frequency_covariance"])<=(
            row["gruss_fixation_bound_when_all_favored"]+1e-12)


def test_dobrushin_coefficient_matches_global_and_no_mixing_extremes() -> None:
    assert THEORY.dobrushin_coefficient([[1,0],[0,1]])==pytest.approx(1)
    assert THEORY.dobrushin_coefficient([[.5,.5],[.5,.5]])==pytest.approx(0)
    P=[[.8,.2,0],[.15,.7,.15],[0,.2,.8]]
    assert THEORY.dobrushin_coefficient(P)==pytest.approx(.8)
    assert THEORY.dobrushin_coefficient([[.6,.4],[.2,.8]])==pytest.approx(.4)


def test_network_mixing_without_new_source_erases_covariance_upper_bound() -> None:
    q0=[.2,.7,.9]
    P=[[.8,.2,0],[.15,.7,.15],[0,.2,.8]]
    r=THEORY.mixing_trajectory(q0,[.3,.7,.9],P,.15,
                                [[0,0,0] for _ in range(30)])
    delta=r["dobrushin_delta"]
    assert delta==pytest.approx(.8)
    for row in r["trajectory"]:
        t=row["generation"]
        assert row["certified_interaction_range_bound"]==pytest.approx(
            .7*(delta**t),abs=1e-12)
        assert abs(row["actual_allele_frequency_covariance"])<=(
            row["certified_covariance_absolute_upper"]+1e-12)
        assert row["actual_interaction_range"]<=(
            row["certified_interaction_range_bound"]+1e-12)
    assert r["last_covariance_upper"]<.001
    assert r["all_future_function_unobserved"] is True


def test_mixing_with_new_heterogeneity_source_can_leave_nonzero_upper_floor() -> None:
    P=[[.8,.2,0],[.15,.7,.15],[0,.2,.8]]
    r=THEORY.mixing_trajectory([.2,.7,.9],[.3,.7,.9],P,.15,
                                [[-.01,0,.01] for _ in range(30)])
    assert len(r["trajectory"])==31
    delta=.8
    for row in r["trajectory"][1:]:
        t=row["generation"]
        expected=.7*delta**t+.02*(1-delta**t)/(1-delta)
        assert row["certified_interaction_range_bound"]==pytest.approx(
            expected,abs=1e-11)
        assert abs(row["actual_allele_frequency_covariance"])<=(
            row["certified_covariance_absolute_upper"]+1e-12)
    assert r["last_covariance_upper"]>.02
    # A positive bound floor does NOT assert covariance remains nonzero.
    assert r["interpretation"].endswith("not a survival/loss theorem")


@pytest.mark.parametrize("P",[
    [[1,0],[0,.8]],
    [[1.01,-.01],[0,1]],
    [[1,0,0],[0,1,0]],
    [[1,0],[0]],
])
def test_invalid_network_mixing_kernels_rejected(P) -> None:
    with pytest.raises(ValueError):
        THEORY.dobrushin_coefficient(P)


@pytest.mark.parametrize("q,p",[
    ([.2,.8],[.1]),
    ([.2,.8],[.1,1.01]),
    ([.2,.8],[float("nan"),.5]),
])
def test_invalid_allele_state_rejected(q,p) -> None:
    with pytest.raises(ValueError):
        THEORY.selection_vs_uniform_q(q,p)


def test_claim_firewall_for_math_only_demonstration() -> None:
    r=THEORY.demonstration()
    assert r["provenance"]=="ALGEBRA_AND_SYNTHETIC_DETERMINISTIC_LIFECYCLE_ONLY"
    assert r["natural_HR_validated"] is False
    assert r["long_horizon_ecological_function_predicted"] is False
    assert r["frozen_NEE_model_mutated"] is False
    assert r["local_real_frequency_counterexample"]["later_fate_inferred"] is False

