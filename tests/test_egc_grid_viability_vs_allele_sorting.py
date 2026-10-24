"""Pinned-source tests: viable high-trait grid before high-allele selection switch.

The source's trait_space_summary is the actual definition of a potentially
viable high trait; allele selection instead references z=1 endpoint fitness.
"""
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
    "egc_grid_viability_allele_frontier",
    SCRIPTS/"egc_grid_viability_vs_allele_sorting_frontier.py")
assert SPEC and SPEC.loader
FRONT=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FRONT)


@pytest.fixture(scope="module")
def pinned():
    if not os.environ.get("EGC_PINNED_ROOT"):
        pytest.skip("exact pinned EGC source is required in dedicated CI")
    return FRONT.load_source()


def test_exact_original_101_grid_threshold_is_below_allele_endpoint(pinned):
    Params,_=pinned
    d=FRONT.exact_grid_viability_threshold(Params)
    assert d["grid_size"]==101
    assert d["high_trait_cutoff"]==.7
    assert d["critical_high_trait_bin_z"]==pytest.approx(.97)
    assert d["critical_q_for_any_potentially_viable_high_trait"]==pytest.approx(
        .5991975106635694,abs=1e-12)
    assert d["endpoint_allele_fitness_switch_q"]==.625
    assert d["whole_grid_viability_begins_below_allele_endpoint_switch"]
    assert d["exact_source_trait_space_summary_checked"]


def test_two_distinct_sharp_demographic_growth_boundaries(pinned):
    Params,_=pinned
    grid=FRONT.exact_grid_viability_threshold(Params)
    d=FRONT.precise_growth_boundary(
        grid["critical_q_for_any_potentially_viable_high_trait"])
    assert d["real_first_population_needed_at_best_trait_and_allele"]==pytest.approx(
        28.690034609949976)
    assert d["minimal_integer_first_population_for_viability"]==29
    assert d["growth_critical_for_high_grid_viability_at_t2"]==pytest.approx(
        .277571773517967,abs=1e-12)
    assert d["growth_critical_for_allele_endpoint_switch_at_t2"]==pytest.approx(
        .31205794958913624,abs=1e-12)
    assert d["strictly_nonempty_growth_window_grid_viable_but_allele_disfavored"]
    assert d["statement"].startswith("These are t=2")


def test_baseline_r03_potential_grid_occasionally_viable_but_allele_selected_against(pinned):
    Params,_=pinned
    qcrit=FRONT.exact_grid_viability_threshold(Params)[
        "critical_q_for_any_potentially_viable_high_trait"]
    d=FRONT.exact_two_event_cell(Params,.30,qcrit)
    assert d["first_population_N1"]==29
    assert d["grid_viability_required_high_bin_count"]==29
    assert d["allele_endpoint_required_high_bin_count"] is None
    assert d["grid_viability_exact_probability"]==pytest.approx(
        1.429865364098991e-9,rel=2e-8)
    assert d["allele_positive_selection_exact_probability"]==0
    assert d["grid_viable_but_allele_selected_against_exact_probability"]==pytest.approx(
        d["grid_viability_exact_probability"])
    assert qcrit<d["q2_if_all_high"]<.625
    params=FRONT.source_parameters(Params,.30,90000)
    from causal_model.multipatch_criticality_dynamics import (
        trait_fitness,trait_space_summary)
    q=d["q2_if_all_high"]
    assert trait_space_summary(q,params).high_trait_component_present
    assert trait_fitness(.97,q,params)>1.
    # Source allele selector uses endpoint z=1 fitness, NOT best z=.97.
    w=1+params.selection_strength*(trait_fitness(1.,q,params)-params.viability_threshold)
    assert w==pytest.approx(.75+.4*q,abs=1e-12)
    assert w<1.


def test_sharp_grid_frontier_rounding_with_source_params(pinned):
    Params,_=pinned
    qcrit=FRONT.exact_grid_viability_threshold(Params)[
        "critical_q_for_any_potentially_viable_high_trait"]
    frontier=FRONT.precise_growth_boundary(qcrit)
    rg=frontier["growth_critical_for_high_grid_viability_at_t2"]
    re=frontier["growth_critical_for_allele_endpoint_switch_at_t2"]
    below=FRONT.exact_two_event_cell(Params,rg-.001,qcrit)
    above=FRONT.exact_two_event_cell(Params,rg+.001,qcrit)
    assert below["first_population_N1"]==28
    assert below["grid_viability_required_high_bin_count"] is None
    assert below["grid_viability_exact_probability"]==0
    assert above["first_population_N1"]==29
    assert above["grid_viability_required_high_bin_count"]==29
    assert above["allele_endpoint_required_high_bin_count"] is None
    assert 0<above["grid_viability_exact_probability"]<1e-8
    allele_below=FRONT.exact_two_event_cell(Params,re-.001,qcrit)
    allele_above=FRONT.exact_two_event_cell(Params,re+.001,qcrit)
    assert allele_below["allele_endpoint_required_high_bin_count"] is None
    assert allele_above["first_population_N1"]==30
    assert allele_above["allele_endpoint_required_high_bin_count"]==30


@pytest.mark.parametrize("r",[.3,.35,.45,.50,.55,.65])
def test_grid_viability_probability_cannot_be_lower_than_endpoint(pinned,r):
    Params,_=pinned
    qcrit=FRONT.exact_grid_viability_threshold(Params)[
        "critical_q_for_any_potentially_viable_high_trait"]
    d=FRONT.exact_two_event_cell(Params,r,qcrit)
    assert d["grid_viability_exact_probability"]>=(
        d["allele_positive_selection_exact_probability"]-1e-12)
    assert d["grid_viable_but_allele_selected_against_exact_probability"]>=0
    assert d["true_model_trait_function_or_loss_probability_estimated"] is False


def test_original_two_generation_source_agrees_with_both_event_types(pinned):
    Params,run=pinned
    qcrit=FRONT.exact_grid_viability_threshold(Params)[
        "critical_q_for_any_potentially_viable_high_trait"]
    for r in (.30,.45,.55):
        d=FRONT.exact_two_event_cell(Params,r,qcrit)
        checked=FRONT.validate_original_EGC_draws(
            Params,run,d,list(range(90001,90129)))
        assert checked["seed_count"]==128
        assert checked["original_source_case_conformity_checked"]
        assert checked["not_natural_or_confirmatory_evidence"]
        observed=checked["observed_counts"]
        assert observed["grid_viable"]>=observed["allele_nonnegative"]
        assert observed["grid_viable_allele_negative"]==(
            observed["grid_viable"]-observed["allele_nonnegative"])


def test_grid_threshold_not_a_long_horizon_recruitment_or_fate_certificate(pinned):
    result=FRONT.build_report(list(range(90001,90017)))
    assert result["source_baseline_growth_03_t3_irreversible_trap_proven_in_pr233"]
    assert result["claims_t2_viability_only_not_future_persistence"]
    assert not result["natural_evolutionary_or_pollination_data_used"]
    assert not result["frozen_NEE_scientific_evidence_changed"]
    assert result["source_fixed_extreme_initial_condition"]["T0"]==0
    assert set(result["source_validation_growth_values"])=={
        .30,.35,.45,.50,.55,.65}


def test_invalid_grid_critical_range_and_duplicate_seeds_fail():
    with pytest.raises(ValueError):
        FRONT.precise_growth_boundary(.625)
    with pytest.raises(ValueError):
        FRONT.build_report([])
    with pytest.raises(ValueError):
        FRONT.build_report([90001,90001])


def test_locked_source_receipt_preserves_distinct_event_denominators_and_limits():
    import json
    ledger=json.loads(
        (ROOT/"artifacts/theory/egc_grid_viability_allele_selection_20261024.json")
        .read_text(encoding="utf-8"))
    assert ledger["schema_version"]==1
    assert ledger["source"]["pinned_commit"]==FRONT.PIN
    assert ledger["source"]["nominal_each_n"]==512
    assert ledger["source"]["full_receipt_sha256"]=="e8370e4083047c48e6badd58adc3ac19c40f201c8f82c033a12f952c3f391cf9"
    cells=ledger["source_analytical_cells"]
    assert len(cells)==11
    assert sum("observed_grid" in c for c in cells)==6
    assert ledger["science_interpretation"]["witness_p1_fixed_at_one"] is True
    assert ledger["science_interpretation"]["relative_fitness_below_one_does_not_imply_observed_p_decrease_in_fixed_witness"] is True
    assert ledger["science_interpretation"]["no_long_horizon_fate_probability_test"] is True
    assert ledger["science_interpretation"]["no_natural_trait_revolution_or_pollination_effect_claim"] is True
    for c in cells:
        assert c["P_grid"]+1e-12>=c["P_allele"]
        assert c["P_grid_viable_allele_w_below_1"]==pytest.approx(
            c["P_grid"]-c["P_allele"],abs=1e-12)
        if "observed_grid" in c:
            assert c["observed_grid"]-c["observed_allele"]==c["observed_wedge"]
            assert 0<=c["observed_allele"]<=c["observed_grid"]<=512


def test_ledger_probabilities_are_rederived_from_pinned_source_without_refitting(pinned):
    import json
    ledger=json.loads(
        (ROOT/"artifacts/theory/egc_grid_viability_allele_selection_20261024.json")
        .read_text(encoding="utf-8"))
    Params,_=pinned
    qcrit=ledger["thresholds"]["q_any_potentially_viable_high_bin"]
    for expected in ledger["source_analytical_cells"]:
        row=FRONT.exact_two_event_cell(Params,expected["r"],qcrit)
        assert row["first_population_N1"]==expected["N1"]
        assert row["grid_viability_required_high_bin_count"]==expected["k_grid"]
        assert row["allele_endpoint_required_high_bin_count"]==expected["k_allele"]
        assert row["grid_viability_exact_probability"]==pytest.approx(
            expected["P_grid"],abs=1e-12)
        assert row["allele_positive_selection_exact_probability"]==pytest.approx(
            expected["P_allele"],abs=1e-12)
        assert row["grid_viable_but_allele_selected_against_exact_probability"]==pytest.approx(
            expected["P_grid_viable_allele_w_below_1"],abs=1e-12)
        assert row["allele_status_refers_to_relative_fitness_sign_not_realized_p_change"]
        assert row["extreme_witness_p1_equals_one_so_allele_remains_fixed"]
