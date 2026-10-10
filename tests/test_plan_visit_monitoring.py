from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
import sys
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0,str(SCRIPTS))
SPEC=importlib.util.spec_from_file_location("plan_visit_monitoring",SCRIPTS/"plan_visit_monitoring.py")
assert SPEC is not None and SPEC.loader is not None
PLAN=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLAN)


def _cov(g: list[float], visits: tuple[int,...], e: list[float]) -> float:
    mean=sum(g)/len(g)
    return sum((x-mean)*v/t for x,v,t in zip(g,visits,e))/len(g)


def _integer_allocations(caps: list[int], total: int):
    for counts in itertools.product(*(range(c+1) for c in caps)):
        if sum(counts)==total:
            yield counts


def test_minimax_design_selects_same_tail_in_four_patch_example() -> None:
    result=PLAN.demonstration()
    assert result["data_provenance"]=="SYNTHETIC_ONLY_NOT_ULEX_OR_ANY_FIELD_DATA"
    assert result["baseline_sharp_interval"]==pytest.approx([-1,1])
    assert result["baseline_width"]==pytest.approx(2)
    assert result["optimal_worst_case_width"]==pytest.approx(0.4)
    assert result["minimum_guaranteed_width_reduction"]==pytest.approx(1.6)
    assert result["selected_plant_ids"]==["g_lowest","g_low"]
    assert result["tied_optimal_subsets"]==[
        ["g_lowest","g_low"],["g_high","g_highest"]]
    assert result["plan_count_checked"]==6
    assert result["all_subsets_checked"] is True
    assert result["outcomes_opened"] is False
    assert result["local_visits_observed"] is False


@pytest.mark.parametrize("budget,best_width",[(0,2.0),(1,1.2),(2,0.4),(3,0.0),(4,0.0)])
def test_each_budget_against_exhaustive_integer_feasible_allocations(budget,best_width) -> None:
    g=[0.1,0.3,0.7,0.9]
    e=[1.,1.,1.,1.]
    caps=[8,8,8,8]
    total=20
    full=list(_integer_allocations(caps,total))
    assert full
    expected_minimax=None
    for subset in itertools.combinations(range(4),budget):
        by_observation={}
        for v in full:
            tagged=tuple(v[i] for i in subset)
            by_observation.setdefault(tagged,[]).append(_cov(g,v,e))
        worst=max(max(vals)-min(vals) for vals in by_observation.values())
        computed=PLAN.worst_case_width(
            [(x-sum(g)/len(g))/len(g) for x in g],
            total,caps,subset)
        assert computed["worst_case_sharp_width"]==pytest.approx(worst)
        if expected_minimax is None or worst<expected_minimax:
            expected_minimax=worst
    design=PLAN.select_monitored_plants(g,total,budget,e,caps)
    assert design["optimal_worst_case_width"]==pytest.approx(best_width)
    assert design["optimal_worst_case_width"]==pytest.approx(expected_minimax)


@pytest.mark.parametrize("visits",[
    {0:8,1:4},{0:5,1:5},{2:8,3:8},{0:0,3:4},
])
def test_conditional_interval_is_exact_against_full_bruteforce(visits) -> None:
    g=[0.1,0.3,0.7,0.9]
    e=[1.0,1.0,1.0,1.0]
    caps=[8,8,8,8]
    vals=[_cov(g,v,e) for v in _integer_allocations(caps,20)
          if all(v[i]==x for i,x in visits.items())]
    assert vals
    r=PLAN.conditional_bounds_after_monitoring(g,20,visits,e,caps)
    assert r["covariance_lower_sharp"]==pytest.approx(min(vals))
    assert r["covariance_upper_sharp"]==pytest.approx(max(vals))
    assert r["future_function_observed"] is False
    assert r["predictive_test_performed"] is False


def test_unequal_effort_and_fractional_caps_breakpoint_certificate() -> None:
    g=[0.0,0.25,0.7,1.]
    e=[1.,2.,1.5,4.]
    caps=[2.5,3.0,4.5,3.0]
    total=7.2
    for k in range(4):
        result=PLAN.select_monitored_plants(g,total,k,e,caps)
        assert result["all_subsets_checked"] is True
        assert result["baseline_width"]+1e-9>=result["optimal_worst_case_width"]
        for plan in result["ranked_plans"]:
            assert plan["worst_case_width"]>=-1e-10


@pytest.mark.parametrize("kwargs",[
    {"monitor_budget":-1},
    {"monitor_budget":5},
    {"monitor_budget":1.5},
    {"monitor_budget":True},
    {"monitor_budget":2,"plant_ids":["x","x","y","z"]},
    {"monitor_budget":2,"visit_caps":[1,1,1,1]},
    {"monitor_budget":2,"effort":[1,0,1,1]},
])
def test_fails_closed_for_invalid_design(kwargs) -> None:
    args={"genetic_state":[.1,.3,.7,.9],"site_total_visits":20,
          "monitor_budget":2,"visit_caps":[8]*4}
    args.update(kwargs)
    with pytest.raises(ValueError):
        PLAN.select_monitored_plants(**args)


@pytest.mark.parametrize("visits",[
    {0:9},
    {0:8,1:8,2:8},
    {7:2},
    {0:float("nan")},
])
def test_invalid_tagged_count_is_not_imputed(visits) -> None:
    with pytest.raises(ValueError):
        PLAN.conditional_bounds_after_monitoring(
            [.1,.3,.7,.9],20,visits,visit_caps=[8]*4)


def test_exact_search_rejects_large_combinatorics_without_silent_heuristic() -> None:
    with pytest.raises(ValueError,match="too many exact subsets"):
        PLAN.select_monitored_plants(
            [i/35 for i in range(35)],
            20,5,visit_caps=[5]*35)


def test_no_ulex_or_future_fate_claim_leaks_into_monitoring_plan() -> None:
    contract=json.loads(
        (ROOT/"artifacts/design/relational_visit_grain_contract_20261010.json")
        .read_text(encoding="utf-8"))
    assert contract["applicability_gate"]["bound_not_calculated_on_real_ulex_rows"] is True
    assert contract["protocol_requirements"]["independent_holdout_unit"]=="site_or_independent_landscape_cohort"
    r=PLAN.demonstration()
    assert r["no_real_ulex_allocation_inferred"] is True
    assert r["claim_ceiling"].startswith("Conditional math")


def test_five_camera_eight_plant_synthetic_design() -> None:
    r=PLAN.demonstration_five_cameras()
    assert r["data_provenance"]=="SYNTHETIC_8_PLANT_5_CAMERA_ONLY"
    assert r["monitor_budget"]==5
    assert r["plan_count_checked"]==56
    assert r["selected_plant_ids"]==["P01","P02","P03","P07","P08"]
    assert r["baseline_width"]==pytest.approx(2.142)
    assert r["optimal_worst_case_width"]==pytest.approx(.285)
    assert r["all_subsets_checked"] is True
    assert not r["outcomes_opened"]
    assert r["no_real_ulex_allocation_inferred"] is True


def test_predeployment_optimal_five_camera_plan_without_future_total() -> None:
    r=PLAN.demonstration_five_cameras_before_total_known()
    assert r["data_provenance"]=="SYNTHETIC_8_PLANT_PREDEPLOYMENT_UNKNOWN_VISIT_TOTAL"
    assert r["scenario_count"]==65
    assert r["total_visit_scenarios"]==list(range(65))
    assert r["monitor_budget"]==5
    assert r["number_of_subsets_checked"]==56
    assert r["all_requested_subsets_and_totals_checked"] is True
    assert r["selected_plant_ids"]==["P01","P02","P03","P07","P08"]
    assert r["minimax_worst_case_width_over_scenarios"]==pytest.approx(.285)
    assert r["local_visits_observed"] is False
    assert r["future_total_observed"] is False
    assert r["natural_HR_test_performed"] is False


def test_predeclared_scenarios_are_not_extrapolated_to_missing_totals() -> None:
    r=PLAN.select_monitored_plants_for_total_scenarios(
        [.1,.3,.7,.9],[4,20,28],2,
        effort=[1]*4,visit_caps=[8]*4)
    assert r["scenario_count"]==3
    assert "Only enumerated totals" in r["scenario_coverage_claim"]
    assert all(v in [4,20,28] for v in r["total_visit_scenarios"])


@pytest.mark.parametrize("totals,caps",[
    ([],[8]*4),
    ([-1,20],[8]*4),
    ([20,20],[8]*4),
    ([100],[8]*4),
])
def test_invalid_future_total_scenarios_stop(totals,caps) -> None:
    with pytest.raises(ValueError):
        PLAN.select_monitored_plants_for_total_scenarios(
            [.1,.3,.7,.9],totals,2,visit_caps=caps)


def test_predeployment_search_explosion_stops_instead_of_heuristic() -> None:
    with pytest.raises(ValueError,match="too many exact scenario evaluations"):
        PLAN.select_monitored_plants_for_total_scenarios(
            [i/19 for i in range(20)],list(range(101)),5,
            visit_caps=[5]*20)
