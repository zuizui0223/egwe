from __future__ import annotations

import importlib.util
import itertools
import json
import math
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location(
    "allocation_bounds",ROOT/"scripts/visit_allocation_identifiability.py"
)
assert SPEC and SPEC.loader
BOUNDS=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BOUNDS)


def _cov(g: list[float], visits: tuple[int,...], effort: list[float]) -> float:
    mean=sum(g)/len(g)
    return sum((gi-mean)*vi/ei for gi,vi,ei in zip(g,visits,effort))/len(g)


def test_frozen_synthetic_four_patch_example_exact_sharp_witnesses() -> None:
    result=BOUNDS.demonstration()
    assert result["data_provenance"]=="SYNTHETIC_4_PATCH_ILLUSTRATION_ONLY"
    assert result["status"]=="sign_not_identified"
    assert result["covariance_lower_sharp"]==pytest.approx(-1)
    assert result["covariance_upper_sharp"]==pytest.approx(+1)
    assert result["minimum_witness_visits"]==[8,8,4,0]
    assert result["maximum_witness_visits"]==[0,4,8,8]
    assert result["constant_rate_imputation_covariance"]==pytest.approx(0)
    assert result["constant_rate_imputation_feasible"] is True
    assert result["empirical_effect_estimated"] is False


@pytest.mark.parametrize("g,effort,caps,total",[
    ([0,1,2],[1,1,1],[2,3,1],3),
    ([0.2,0.4,0.9],[1,2,4],[3,2,2],4),
    ([0.5,0.5,0.5],[1,3,2],[1,3,2],5),
    ([0,0,1,2],[1,2,1,3],[2,2,2,2],5),
])
def test_bounds_are_sharp_against_exhaustive_integer_allocations(
        g,effort,caps,total) -> None:
    values=[]
    for v in itertools.product(*(range(c+1) for c in caps)):
        if sum(v)==total:
            values.append(_cov(g,v,effort))
    assert values
    result=BOUNDS.sharp_covariance_bounds(g,total,effort,caps)
    assert result["covariance_lower_sharp"]==pytest.approx(min(values))
    assert result["covariance_upper_sharp"]==pytest.approx(max(values))
    for suffix,which in [("minimum","lower"),("maximum","upper")]:
        witness=result[f"{suffix}_witness_visits"]
        assert sum(witness)==pytest.approx(total)
        assert all(0<=x<=cap for x,cap in zip(witness,caps))
        assert _cov(g,tuple(witness),effort)==pytest.approx(
            result[f"covariance_{which}_sharp"])


def test_exact_uncapped_bounds() -> None:
    r=BOUNDS.sharp_covariance_bounds([0.1,0.3,0.7,0.9],20)
    assert r["covariance_lower_sharp"]==pytest.approx(-2)
    assert r["covariance_upper_sharp"]==pytest.approx(+2)
    assert r["local_visits_observed"] is False
    assert r["future_function_observed"] is False


def test_equal_genetic_state_only_identifies_zero() -> None:
    r=BOUNDS.sharp_covariance_bounds([.4,.4,.4],100,[1,2,1])
    assert r["status"]=="point_identified_zero"
    assert r["covariance_lower_sharp"]==pytest.approx(0)
    assert r["covariance_upper_sharp"]==pytest.approx(0)


@pytest.mark.parametrize("g,total,effort,caps",[
    ([0,1],-1,None,None),
    ([0,float("nan")],4,None,None),
    ([0,1],5,[1,0],None),
    ([0,1],5,[1],None),
    ([0,1],5,None,[2,2]),
    ([0,1],5,None,[8,-1]),
    ([],5,None,None),
])
def test_bad_source_inputs_stop(g,total,effort,caps) -> None:
    with pytest.raises(ValueError):
        BOUNDS.sharp_covariance_bounds(g,total,effort,caps)


def test_original_ulex_source_gate_is_not_overridden() -> None:
    source=json.loads((ROOT/"artifacts/empirical/ulex_zenodo_source_gate_20261008.json")
                      .read_text(encoding="utf-8"))
    assert source["status"]=="NOT_IDENTIFIABLE_NO_POLLINATOR_PLANT_ID"
    receipt=source["executed_receipt"]
    assert "ind" not in receipt["csv_headers"]["pollinator.census.csv"]
    assert "ind" in receipt["csv_headers"]["fruits.and.mean.floral.traits.csv"]
    assert source["admission_gates"]["full_HR_admitted"] is False
