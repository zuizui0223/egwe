"""Verify exact density-dependent support gate and actual pinned EGC update."""
from __future__ import annotations

import importlib.util
import math
import os
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
sys.path.insert(0,str(SCRIPTS))
SPEC=importlib.util.spec_from_file_location(
    "latent_support_gate",SCRIPTS/"egc_latent_ecological_support_gate.py")
assert SPEC and SPEC.loader
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


def test_necessary_density_and_latent_allele_thresholds_for_empty_trait():
    r=GATE.fully_absent_trait_universal_limits()
    assert r["trait_mass"]==0.
    assert r["necessary_density_for_ability_to_reach_next_q_switch"]==pytest.approx(
        .8800240075447588)
    assert r["necessary_p_at_full_density_and_max_q"]==pytest.approx(
        .16016805281331203)
    assert r["maximum_possible_next_q_at_density_half"]<.625
    assert r["next_q_switch_cannot_be_met_at_density_half_for_any_q_or_p"]
    assert GATE.next_q(1.,1.,.5)<.625


def test_strong_initial_q_but_zero_expressed_trait_fails_to_hold_switch():
    r=GATE.viability_gate(.8,.4,.5,0.)
    assert r["next_q"]==pytest.approx(.25138296833150847)
    assert not r["next_q_at_or_above_switch"]
    assert r["critical_density_if_other_states_fixed"]>1.
    assert r["critical_current_q_if_other_states_fixed"]>1.


def test_even_full_density_needs_very_high_q_for_latent_allele_p04():
    low=GATE.viability_gate(1.,.04,1.,0.)
    assert not low["next_q_at_or_above_switch"]
    assert low["critical_current_q_if_other_states_fixed"]>1.
    high=GATE.viability_gate(.8,.4,1.,0.)
    assert not high["next_q_at_or_above_switch"]
    assert high["critical_current_q_if_other_states_fixed"]==pytest.approx(
        .9600280088022186)
    at_threshold=GATE.viability_gate(high["critical_current_q_if_other_states_fixed"],.4,1.,0.)
    assert at_threshold["next_q"]==pytest.approx(.625,abs=1e-12)


def test_source_weighted_trait_mass_can_reopen_next_q_threshold_at_full_density():
    r=GATE.viability_gate(.8,.4,1.,.4)
    assert r["next_q"]>.625
    assert r["next_q_at_or_above_switch"]


def test_evaluated_original_four_cells_all_below_next_q_switch():
    report=GATE.fixed_four_conditions()
    assert set(report["initial_20_over_40"])=={
        "q0.20_p0.04","q0.20_p0.40","q0.80_p0.04","q0.80_p0.40"}
    assert all(not x["next_q_at_or_above_switch"]
               for x in report["initial_20_over_40"].values())
    assert all(not x["next_q_at_or_above_switch"]
               for x in report["density_one_counterfactuals"].values())
    assert report["natural_trait_function_measured"] is False


@pytest.mark.parametrize("q,p,d",[
    (.2,.04,.5),(.2,.4,.5),(.8,.04,.5),(.8,.4,.5),
    (.8,.4,1.),(1.,.4,1.)
])
def test_exact_source_formula_matches_pinned_egc(q,p,d):
    if not os.environ.get("EGC_PINNED_ROOT"):
        pytest.skip("pinned EGC source checked out only in dedicated workflow")
    from run_pinned_egc_aa_rr_lifecycle import load_source
    Params,_=load_source()
    from causal_model.multipatch_criticality_dynamics import (
        interaction_support_signal, sigmoid)
    par=Params(
        patch_areas=(1.,),generations=1,
        interaction_feedback=4.5,interaction_barrier=.5025,
        q_feedback_alpha=.6,q_feedback_beta_trait=.3,q_feedback_gamma_allele=.1)
    s=interaction_support_signal(q,0.,p,par)
    next_from_original=sigmoid(par.interaction_feedback*(d*s-par.interaction_barrier))
    assert GATE.next_q(q,p,d)==pytest.approx(next_from_original,abs=1e-14)


@pytest.mark.parametrize("values",[
    (-.01,.4,.5),(.8,1.1,.5),(.8,.4,1.1),(.8,.4,float("nan"))
])
def test_invalid_source_state_rejected(values):
    with pytest.raises(ValueError):
        GATE.next_q(*values)
