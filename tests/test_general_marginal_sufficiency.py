from __future__ import annotations

import fractions
import importlib.util
import itertools
import json
import math
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location(
    "general_marginal_sufficiency",
    ROOT/"scripts/general_marginal_sufficiency.py")
assert SPEC and SPEC.loader
THEORY=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(THEORY)


def test_exact_iff_separability_for_finite_product_table() -> None:
    additive=[[f"{i*7+j*3}/7" for j in range(3)] for i in range(4)]
    result=THEORY.exact_grid_additivity(additive)
    assert result["additively_separable"] is True
    assert result["global_pairing_invariance_for_all_marginals"] is True
    for i,j in itertools.product(range(4),range(3)):
        a=fractions.Fraction(result["x_component"][i])
        b=fractions.Fraction(result["y_component"][j])
        assert a+b==fractions.Fraction(additive[i][j])


def test_nonadditive_grid_gives_exact_rectangle_witness() -> None:
    r=THEORY.exact_grid_additivity([
        ["0","0","0"],["0","1","2"],["0","2","4"]])
    assert not r["additively_separable"]
    assert not r["global_pairing_invariance_for_all_marginals"]
    assert r["witness_rectangle_indices"]==[0,1,0,1]
    assert r["witness_exact_mixed_difference"]=="1"


def test_binary_table_gap_is_exact_not_float_rounding() -> None:
    r=THEORY.exact_grid_additivity([
        ["1/3","1/7"],["3/11","5/13"]])
    difference=(fractions.Fraction(1,3)+fractions.Fraction(5,13)
        -fractions.Fraction(1,7)-fractions.Fraction(3,11))
    assert fractions.Fraction(r["witness_exact_mixed_difference"])==difference


def test_additive_aggregate_invariance_does_not_mean_labeled_patch_state_invariance() -> None:
    x=[0,1];y=[1,2]
    f=lambda a,b:a+b
    paired=[f(a,b) for a,b in zip(x,y)]
    swapped=[f(a,b) for a,b in zip(x,reversed(y))]
    assert paired!=swapped
    assert sum(paired)==sum(swapped)
    r=THEORY.exhaustive_pairing_extrema(x,y,f)
    assert r["minimum_sum"]==pytest.approx(r["maximum_sum"])
    assert r["one_step_aggregate_only"] is True


def test_logistic_rectangles_have_opposite_sign_below_and_above_inflection() -> None:
    x=(.2,.4);y=(.2,.4)
    low=THEORY.logistic_rectangle_regime(*x,*y,theta=.8)
    high=THEORY.logistic_rectangle_regime(*x,*y,theta=.1)
    crossing=THEORY.logistic_rectangle_regime(*x,*y,theta=.3)
    assert low=="strictly_supermodular_below_inflection"
    assert high=="strictly_submodular_above_inflection"
    assert crossing=="mixed_or_touching_threshold_no_global_order"
    for theta,sign in ((.8,1),(.1,-1)):
        f=lambda a,b:THEORY.logistic_update(a,b,theta=theta)
        gap=THEORY.swap_gap(f,*x,*y)
        assert sign*gap>0
    assert THEORY.swap_gap(lambda a,b:a+b,*x,*y)==pytest.approx(0)


@pytest.mark.parametrize("x,y,theta",[
    (.1,.2,.8),(.25,.3,.1),(.8,.7,.5),(.3,.9,.4),(.4,.6,.6)
])
def test_exact_analytic_cross_partial_matches_symmetric_finite_difference(
        x,y,theta) -> None:
    eps=1e-4
    f=lambda a,b:THEORY.logistic_update(a,b,theta=theta)
    approx=(f(x+eps,y+eps)-f(x+eps,y-eps)
            -f(x-eps,y+eps)+f(x-eps,y-eps))/(4*eps*eps)
    theory=THEORY.logistic_cross_partial(x,y,theta=theta)
    assert approx==pytest.approx(theory,rel=2e-6,abs=1e-8)


def test_supermodular_sorted_is_global_max_and_submodular_sorted_is_min() -> None:
    x=[.2,.25,.35,.4]; y=[.2,.21,.3,.4]
    for theta,orientation in ((.8,"max"),(.1,"min")):
        f=lambda a,b:THEORY.logistic_update(a,b,theta=theta)
        r=THEORY.exhaustive_pairing_extrema(x,y,f)
        assert r["permutations_tested"]==24
        if orientation=="max":
            assert r["aligned_sum"]==pytest.approx(r["maximum_sum"])
            assert r["reversed_sum"]==pytest.approx(r["minimum_sum"])
        else:
            assert r["aligned_sum"]==pytest.approx(r["minimum_sum"])
            assert r["reversed_sum"]==pytest.approx(r["maximum_sum"])


def test_original_EGWE_canonical_template_aggregate_direction_is_not_absolute() -> None:
    q=[.65,.75,.85,.95];b=[.2,.4,.6,.8]
    r=THEORY.exhaustive_pairing_extrema(q,b,
        lambda x,y:THEORY.logistic_update(x,y,theta=.5025))
    assert r["aligned_pairing"]==[0,1,2,3]
    assert r["reversed_pairing"]==[3,2,1,0]
    assert r["aligned_sum"]/4==pytest.approx(.6715314616718732)
    assert r["reversed_sum"]/4==pytest.approx(.6892968516234685)
    assert (r["aligned_sum"]-r["reversed_sum"])/4==pytest.approx(
        -.01776538995159538)
    assert r["maximum_sum"]>r["minimum_sum"]
    # Opposite ordering under a different, explicitly chosen threshold.
    s=THEORY.exhaustive_pairing_extrema(q,b,
        lambda x,y:THEORY.logistic_update(x,y,theta=.8))
    assert s["aligned_sum"]>s["reversed_sum"]


def test_monotone_fitness_sorting_positive_and_covariance_pair_identity() -> None:
    q=[.65,.75,.85,.95]
    p=[.22,.4,.66,.73]
    r=THEORY.selection_covariance_identity(q,p)
    assert r["selection_induced_delta"]>0
    assert r["nonnegative_fitness_difference_ordered"]
    assert r["selection_induced_delta"]==pytest.approx(
        r["pairwise_covariance_identity"],abs=1e-14)


def test_general_negative_and_constant_fitness_gradient_falsify_universal_sorting() -> None:
    q=[.2,.4,.7,.9];p=[.1,.25,.75,.92]
    negative=THEORY.selection_covariance_identity(
        q,p,w=lambda z:1.6-.4*z)
    assert negative["selection_induced_delta"]<0
    assert negative["pairwise_covariance_identity"]<0
    constant=THEORY.selection_covariance_identity(
        q,p,w=lambda z:1.1)
    assert constant["selection_induced_delta"]==pytest.approx(0,abs=1e-14)


@pytest.mark.parametrize("kwargs",[
    {"alpha":0},{"beta":-1},{"kappa":0},{"theta":float("nan")}
])
def test_invalid_sigmoid_sign_assumptions_fail_closed(kwargs) -> None:
    with pytest.raises(ValueError):
        THEORY.logistic_update(.3,.4,**kwargs)


def test_exact_grid_input_validation() -> None:
    with pytest.raises(ValueError):
        THEORY.exact_grid_additivity([[1,2],[3]])
    with pytest.raises(ValueError):
        THEORY.exact_grid_additivity([[1,2]])


def test_demo_is_math_only_and_does_not_refit_frozen_nee() -> None:
    result=THEORY.demonstration()
    assert result["data_provenance"]=="ALGEBRA_AND_DECLARED_EGWE_SYNTHETIC_CLOSURE_ONLY"
    assert result["finite_grid_example"]["additively_separable"] is False
    assert result["sigmoid_sign_reversal_examples"][0]["aligned_minus_swapped"]<0
    assert result["sigmoid_sign_reversal_examples"][1]["aligned_minus_swapped"]>0
    assert result["long_horizon_fate_claim"] is False
    assert result["natural_empirical_validation_claim"] is False

