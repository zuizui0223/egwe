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
