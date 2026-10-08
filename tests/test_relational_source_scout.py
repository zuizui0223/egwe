from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts/validate_relational_source_scout.py"
SPEC = importlib.util.spec_from_file_location("source_scout_gate", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _registry() -> dict:
    return json.loads(MODULE.REGISTRY.read_text(encoding="utf-8"))


def test_published_archive_metadata_does_not_count_as_raw_verification() -> None:
    result = MODULE.validate_registry(_registry())
    assert result["metadata_screened"] == 5
    assert result["raw_archives_verified"] == 0
    assert result["full_HR_confirmed"] == 0
    assert not result["confirmed_ids"]


def test_partial_brassica_cannot_pass_spatial_relational_gate() -> None:
    record = next(r for r in _registry()["records"] if r["id"] == "brassica_leventhal_2026")
    assert record["gates"]["same_unit_genetic_or_parentage"] == "pass"
    assert record["gates"]["patch_resolved_effective_interaction"] == "fail"
    assert record["gates"]["patch_relational_join_verified"] == "fail"
    assert record["full_HR_classification"] != "ELIGIBLE_FULL_HR"


def test_prevent_eligibility_promotion_from_only_relabeled_claim() -> None:
    registry = copy.deepcopy(_registry())
    registry["records"][0]["full_HR_classification"] = "ELIGIBLE_FULL_HR"
    with pytest.raises(AssertionError):
        MODULE.validate_registry(registry)


def test_prevent_hidden_eligibility_without_matching_registry_count() -> None:
    registry = copy.deepcopy(_registry())
    registry["records"][0]["gates"] = dict.fromkeys(MODULE.REQUIRED, "pass")
    registry["records"][0]["full_HR_classification"] = "ELIGIBLE_FULL_HR"
    with pytest.raises(AssertionError, match="eligible-count"):
        MODULE.validate_registry(registry)


def test_source_id_and_gate_schema_integrity() -> None:
    registry = copy.deepcopy(_registry())
    registry["records"][1]["id"] = registry["records"][0]["id"]
    with pytest.raises(AssertionError, match="duplicate"):
        MODULE.validate_registry(registry)
    registry = copy.deepcopy(_registry())
    registry["records"][0]["gates"]["patch_relational_join_verified"] = "likely"
    with pytest.raises(AssertionError, match="invalid gate"):
        MODULE.validate_registry(registry)


def test_brassica_actual_access_stop_is_not_ecological_negative() -> None:
    source = next(r for r in _registry()["records"] if r["id"] == "brassica_leventhal_2026")
    attempt = source["acquisition_attempt"]
    assert attempt["source_file_id"] == 4959416
    assert attempt["expected_archive_bytes"] == 1670300
    assert [x["http_status"] for x in attempt["methods"]] == [401, 403]
    assert attempt["source_access_decision"] == "ACCESS_OR_SCHEMA_STOP"
    assert attempt["raw_archive_received"] is False
    assert attempt["outcome_values_opened"] is False
    assert source["gates"]["raw_bytes_inspected"] == "unknown"
    assert source["full_HR_classification"] != "ELIGIBLE_FULL_HR"


def test_pearson_expt2_cannot_join_expt1_longitudinal_core() -> None:
    record = next(r for r in _registry()["records"] if r["id"] == "echinacea_pearson_2023")
    link = record["potential_longitudinal_link"]
    assert link["exposure_plot"] == "exPt2"
    assert link["target_plot"] == "exPt1"
    assert link["distinct_plots_confirmed"] is True
    assert link["same_plot"] is False
    assert link["prior_proposal_invalidated"] is True
    assert link["status"].startswith("STOP_PLOT_MISMATCH")
    assert link["published_2024_12_11_target_year_coverage"] == {
        "survival_and_flowering_through": 2024,
        "achene_count_through": 2017,
    }
    assert link["valid_2018_to_2019_seed_set_in_proposed_target"] is False
    assert link["independent_expt2_forward_panel_publicly_verified"] is False
    assert record["full_HR_classification"] != "ELIGIBLE_FULL_HR"


def test_pearson_ineligible_even_if_somebody_claims_expt1_join() -> None:
    registry = copy.deepcopy(_registry())
    rec = next(r for r in registry["records"] if r["id"] == "echinacea_pearson_2023")
    rec["full_HR_classification"] = "ELIGIBLE_FULL_HR"
    with pytest.raises(AssertionError):
        MODULE.validate_registry(registry)
