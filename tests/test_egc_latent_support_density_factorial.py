"""Exact-source safety and preregistered eight-cell EGC design tests."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0,str(SCRIPTS))
SPEC=importlib.util.spec_from_file_location(
    "egc_density_factorial",SCRIPTS/"egc_latent_support_density_factorial.py")
assert SPEC and SPEC.loader
MODEL=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)

from egc_latent_ecological_support_gate import viability_gate
from egc_reexpression_establishment_gate import analyze_one,source_params


def test_exact_feedback_gate_crossed_by_only_one_of_eight_declared_cells():
    expected={}
    for q in MODEL.Q_VALUES:
        for p in MODEL.P_VALUES:
            for n in MODEL.N_VALUES:
                expected[MODEL.cell_name(q,p,n)]=viability_gate(q,p,n/40.,0.)[
                    "next_q_at_or_above_switch"]
    assert sum(expected.values())==1
    assert expected["q0.98_p0.40_N40"]
    assert not expected["q0.98_p0.04_N40"]
    assert not expected["q0.80_p0.40_N40"]
    assert not expected["q0.98_p0.40_N20"]
    assert all(not yes for name,yes in expected.items() if name.endswith("N20"))
    assert viability_gate(.98,.4,1.,0.)["actual_density_weighted_support"]==pytest.approx(.628)


@pytest.fixture(scope="module")
def pinned():
    if not os.environ.get("EGC_PINNED_ROOT"):
        pytest.skip("source-pinned EGC checkout is required in dedicated CI only")
    return MODEL.load_source()


def test_actual_q1_matches_exact_route_margin_and_no_high_trait_initially(pinned):
    Params,runner=pinned
    for q,p,n in ((.98,.4,40),(.98,.4,20),(.8,.4,40),(.98,.04,40)):
        case=MODEL.one_seed(Params,runner,70001,q,p,n,4)
        analytical=viability_gate(q,p,n/40.,0.)
        assert case["q1"]==pytest.approx(analytical["next_q"],abs=1e-13)
        assert case["q1_above_0625"] is analytical["next_q_at_or_above_switch"]
        assert case["q1_analytic_gate_value"]==pytest.approx(case["q1"])
        assert 0<=case["first_generation_high_expression_probability"]<=1
        assert case["source_order_preserved"]
        assert case["fixed_N1"]>=1
        assert case["q2"]<=case["q2_conservative_upper_bound"]+1e-12
        assert case["q2_high_grid_viability_impossible_by_bound"] is True
        assert case["grid_viable_at_generation_2"] is False
        assert case["any_grid_viability_from_generation_3"] is False
        if case["ever_joint_trait_allele_zero"]:
            assert case["first_joint_zero_generation"] is not None
            assert not case["high_at_final_generation"]


def test_previous_q08_p04_N20_source_result_is_unmodified(pinned):
    Params,runner=pinned
    old=analyze_one(Params,runner,70002,.8,.04,4)
    case=MODEL.one_seed(Params,runner,70002,.8,.04,20,4)
    assert case["q1"]==pytest.approx(old["q_at_generation_1"])
    assert case["q2"]==pytest.approx(old["q_at_generation_2"])
    assert case["expressed_at_generation_1"]==old["expressed_at_generation_1"]
    assert case["three_consecutive_high_snapshots"]==old["three_consecutive_expressed_generations"]
    assert case["high_at_final_generation"]==old["final_expressed"]
    assert case["ever_joint_trait_allele_zero"]==old["ever_joint_zero"]


def test_all_eight_source_scenarios_have_new_coherent_seed_cohort(pinned):
    r=MODEL.run_experiment([70001,70002],4)
    assert r["source_commit"]==MODEL.PIN
    assert len(r["scenarios"])==8
    assert r["seed_block"]==[70001,70002]
    assert r["no_natural_field_validation"] is True
    assert r["N0_change_combines_density_population_and_finite_drift"] is True
    assert r["frozen_NEE_numerical_results_unchanged"]
    assert r["design_not_tuned_after_outcomes"]
    for key,cell in r["scenarios"].items():
        assert cell["summary"]["n_seeds"]==2
        assert [x["seed"] for x in cell["cases"]]==[70001,70002]
        assert cell["summary"]["q1"]==pytest.approx(cell["initial_expected_q1"])
        assert cell["initial_high_trait_count"]==0
        assert cell["summary"]["grid_viable_at_generation_2_count"]==0
        assert cell["summary"]["grid_viable_at_generation_12_count"]==0
        assert cell["summary"]["grid_viable_any_generation_3_to_final_count"]==0
        assert cell["summary"]["maximum_q2_high_trait_grid_viability_certified_impossible"] is True
        assert "cases" in cell
    contrasts=r["descriptive_density_contrasts"]
    assert len(contrasts["contrasts"])==4
    assert contrasts["no_generation_pseudoreplication"]
    assert contrasts["not_independent_holdout_or_natural_validation"]


def test_seed_group_bootstrap_differences_only_use_matched_seeds():
    seeds=[70001,70002,70003]
    def cases(flags):
        return [{"seed":seed,**{outcome:bool(f)
                 for outcome in MODEL.PRIMARY_OUTCOMES}}
                for seed,f in zip(seeds,flags)]
    cells={}
    for q in MODEL.Q_VALUES:
        for p in MODEL.P_VALUES:
            for n in MODEL.N_VALUES:
                cells[MODEL.cell_name(q,p,n)]={"cases":cases(
                    [0,0,1] if n==20 else [1,1,1])}
    r=MODEL.descriptive_contrasts(cells,seeds,100)
    comparison=r["contrasts"]["density_at_q0.80_p0.04"]
    for outcome in MODEL.PRIMARY_OUTCOMES:
        x=comparison["outcomes"][outcome]
        assert x["N40_minus_N20"]==pytest.approx(2/3)
        assert x["N40_only"]==2
        assert x["N20_only"]==0
        assert x["not_confirmatory"]
        assert x["paired_seed_bootstrap_percentile_95"][0]>=0
    assert r==MODEL.descriptive_contrasts(cells,seeds,100)


def test_seed_order_failure_blocks_resampling():
    cells={}
    seeds=[70001,70002]
    for q in MODEL.Q_VALUES:
        for p in MODEL.P_VALUES:
            for n in MODEL.N_VALUES:
                ids=seeds[::-1] if n==40 and p==.4 else seeds
                cells[MODEL.cell_name(q,p,n)]={"cases":[{
                    "seed":seed,
                    **{outcome:False for outcome in MODEL.PRIMARY_OUTCOMES}
                } for seed in ids]}
    with pytest.raises(ValueError,match="pairing"):
        MODEL.descriptive_contrasts(cells,seeds,100)


def test_reject_duplicate_seeds_or_invalid_horizon():
    with pytest.raises(ValueError):
        MODEL.run_experiment([70001,70001])
    with pytest.raises(ValueError):
        MODEL.run_experiment([70001],2)


def test_no_source_checkout_fails_closed(monkeypatch):
    monkeypatch.delenv("EGC_PINNED_ROOT",raising=False)
    with pytest.raises(KeyError):
        MODEL.run_experiment([70001],4)


def test_exact_two_step_ceiling_uses_pinned_N1_growth_and_full_trait_grid(pinned):
    Params,_=pinned
    from dataclasses import replace
    from egc_reexpression_establishment_gate import source_params
    from causal_model.multipatch_criticality_dynamics import trait_space_summary
    for q in MODEL.Q_VALUES:
        for p in MODEL.P_VALUES:
            for n in MODEL.N_VALUES:
                params=replace(source_params(Params,70001,q,p,4),initial_population=(n,))
                report=MODEL.conservative_two_step_ceiling(params,q,p,n)
                qceil=report["maximum_possible_q2_under_T1_p1_le_one"]
                assert report["uses_source_fitness_population_and_feedback"]
                assert report["bound_may_not_be_jointly_attainable"]
                assert qceil<.5991975107
                assert report["maximum_high_bin_fitness_at_q2_ceiling"]<params.viability_threshold
                assert not trait_space_summary(qceil,params).high_trait_component_present
                assert report["all_high_bins_potentially_nonviable_by_t2_certified"]
                assert report["trait_grid_size"]==101


def test_future_grid_viability_is_not_equivalent_to_positive_expressed_trait(pinned):
    Params,runner=pinned
    r=MODEL.run_experiment([70001,70002],4)
    for cell in r["scenarios"].values():
        assert all(not c["grid_viable_at_generation_2"] for c in cell["cases"])
        assert all(not c["any_grid_viability_from_generation_3"] for c in cell["cases"])
    chosen=r["scenarios"]["q0.98_p0.40_N40"]
    assert chosen["summary"]["initial_one_step_q_threshold_met"] is True
    assert chosen["summary"]["grid_viable_at_generation_1_count"]==2
    assert chosen["summary"]["grid_viable_at_generation_2_count"]==0
    assert chosen["summary"]["q2_source_derived_upper_bound"]<.5991975107
