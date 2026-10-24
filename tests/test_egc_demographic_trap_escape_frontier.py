"""Sharp baseline-growth attainability frontier in original source."""
from __future__ import annotations

import importlib.util
import math
import os
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0,str(SCRIPTS))
SPEC=importlib.util.spec_from_file_location(
    "egc_escape_frontier",SCRIPTS/"egc_demographic_trap_escape_frontier.py")
assert SPEC and SPEC.loader
FRONT=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FRONT)


def test_sharp_source_rounding_frontier():
    f=FRONT.analytical_growth_frontier()
    assert f["growth_baseline_at_frozen_run"]==.3
    assert f["q1_global_max_from_initial_T0_zero"]==pytest.approx(.708632149106754)
    assert f["real_N1_required_if_all_next_high_and_all_alleles"]==pytest.approx(
        29.860992060594704)
    assert f["minimum_integer_N1_for_q2_crossing"]==30
    assert f["baseline_growth_critical_to_round_N1_to_30"]==pytest.approx(
        .31205794958913624)
    assert f["r_below_boundary_global_q2_switch_impossible"] is True
    assert f["r_above_boundary_some_source_trajectory_can_cross_q2_switch"] is True
    assert f["possible_does_not_mean_probable"] is True


def test_binomial_tail_matches_direct_finite_combinatorics():
    for n in [1,5,20,36]:
        for p in [.01,.4,.5,.99]:
            for k in [0,1,n//2,n,n+1]:
                expected=sum(math.comb(n,i)*p**i*(1-p)**(n-i)
                             for i in range(k,n+1))
                assert FRONT.binomial_tail(n,p,k)==pytest.approx(
                    expected,rel=1e-11,abs=1e-13)


@pytest.mark.parametrize("r,N1,K_count",[
    (.3,29,None),
    (.35,31,28),
    (.45,34,23),
    (.5,36,20),
    (.55,37,18),
    (.65,41,13),
])
def test_original_source_exact_high_recruit_probabilities(r,N1,K_count):
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("source-locked EGC checkout needed")
    Params,_=FRONT.load_source()
    o=FRONT.fixed_extreme_cell(Params,r)
    assert o["N1_exact"]==N1
    assert o["required_high_bin_count_for_q2_switch"]==K_count
    assert o["source_high_bin_recruit_probability"]==pytest.approx(
        .4954618015503168,abs=1e-11)
    assert o["switch_attainable_with_positive_probability"]==(K_count is not None)
    assert o["q2_if_all_high_recruited"]>=.625 if K_count is not None else o["q2_if_all_high_recruited"]<.625
    if r==.3:
        assert o["exact_probability_q2_at_or_above_0625"]==0
    if r==.35:
        assert o["exact_probability_q2_at_or_above_0625"]<1e-4
    if r==.5:
        assert o["exact_probability_q2_at_or_above_0625"]==pytest.approx(
            .28982487626779796,abs=1e-10)


def test_near_the_critical_boundary_is_possible_but_extremely_unlikely():
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("source-locked EGC checkout needed")
    Params,_=FRONT.load_source()
    rcrit=FRONT.analytical_growth_frontier()[
        "baseline_growth_critical_to_round_N1_to_30"]
    below=FRONT.fixed_extreme_cell(Params,rcrit-.001)
    above=FRONT.fixed_extreme_cell(Params,rcrit+.001)
    assert below["N1_exact"]==29
    assert below["required_high_bin_count_for_q2_switch"] is None
    assert below["exact_probability_q2_at_or_above_0625"]==0
    assert above["N1_exact"]==30
    assert above["required_high_bin_count_for_q2_switch"]==30
    assert 0<above["exact_probability_q2_at_or_above_0625"]<1e-8


def test_actual_pinned_EGC_simulations_calibrate_q2_probability():
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("source-locked EGC checkout needed")
    Params,run=FRONT.load_source()
    for r in (.3,.45,.5,.55):
        o=FRONT.fixed_extreme_cell(Params,r)
        result=FRONT.source_simulation_check(
            Params,run,o,list(range(80001,80257)))
        assert result["seeds"]==256
        assert result["first_population_unique_values"]==[o["N1_exact"]]
        assert result["not_confirmatory_or_natural_validation"] is True
        if r==.3:
            assert result["observed_q2_switch_crossings"]==0


def test_invalid_parameter_and_source_contracts_stop():
    with pytest.raises(ValueError):
        FRONT.binomial_tail(20,float("nan"),10)
    with pytest.raises(ValueError):
        FRONT.binomial_tail(20,.3,-2)
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("source-locked EGC checkout needed")
    Params,_=FRONT.load_source()
    with pytest.raises(ValueError):
        FRONT.source_parameters(Params,3.0,123)
    with pytest.raises(ValueError):
        FRONT.source_simulation_check(Params,None,{"baseline_growth":.3},[])
