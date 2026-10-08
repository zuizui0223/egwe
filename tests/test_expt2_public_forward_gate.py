from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("expt2_source_gate",ROOT/"scripts/check_expt2_public_forward_gate.py")
assert SPEC and SPEC.loader
AUDIT=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)

def source() -> dict:
    return json.loads(AUDIT.SOURCE.read_text(encoding="utf-8"))

def test_expt2_field_measurements_are_not_claimed_as_public_keyed_panel() -> None:
    r=AUDIT.validate(source())
    assert r["not_biological_null"] is True
    assert r["same_plot_longitudinal_join_verified"] is False
    assert r["future_outcomes_opened"] is False

def test_reject_renaming_expt1_core_to_expt2() -> None:
    r=copy.deepcopy(source())
    r["key_checks"]["proposed_expt1_core"]["value"]="exPt2"
    with pytest.raises(AssertionError):
        AUDIT.validate(r)

def test_reject_unverified_2018_to_2019_join() -> None:
    r=copy.deepcopy(source())
    r["key_checks"]["pearson_2018_to_2019plus_individual_id_crosswalk"]["status"]="verified"
    with pytest.raises(AssertionError):
        AUDIT.validate(r)

def test_no_outcome_or_ecological_null_inference_from_catalogue_gap() -> None:
    r=copy.deepcopy(source())
    r["empirical_loss_claim"]=True
    with pytest.raises(AssertionError):
        AUDIT.validate(r)
    r=copy.deepcopy(source())
    r["key_checks"]["direct_expt2_future_functional_endpoint"]["outcomes_opened"]=True
    with pytest.raises(AssertionError):
        AUDIT.validate(r)
