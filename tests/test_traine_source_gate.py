from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from urllib.error import HTTPError
import pytest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"scripts/probe_traine_plant_source_headers.py"
SPEC=importlib.util.spec_from_file_location("traine_headers",PATH)
assert SPEC and SPEC.loader
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

def test_probe_reads_header_only_never_outcomes() -> None:
    payload=b"plant,matrix,bee_flower_visits,seed_number\nCONFIDENTIAL_OUTCOME_ROW\n"
    assert MOD._header(payload)==[
        "plant","matrix","bee_flower_visits","seed_number"]
    assert "CONFIDENTIAL_OUTCOME_ROW" not in str(MOD._header(payload))

def test_metadata_host_restricted_before_network() -> None:
    with pytest.raises(ValueError,match="allowlisted"):
        MOD._json("https://example.org/api/v2/articles/31239511")

def test_failed_raw_download_does_not_become_biological_null(monkeypatch) -> None:
    def unavailable(url: str):
        raise HTTPError(url,403,"Forbidden",None,None)
    monkeypatch.setattr(MOD,"_json",unavailable)
    for source in (MOD.dryad,MOD.figshare):
        result=source()
        assert result["status"]=="ACCESS_OR_SCHEMA_STOP"
        assert result["raw_verified"] is False
        assert result["outcome_rows_opened"] is False
        assert result["http_status"]==403

def test_source_registry_is_partial_not_full_hr() -> None:
    src=json.loads(
        (ROOT/"artifacts/empirical/traine_plant_assay_source_20261008.json")
        .read_text(encoding="utf-8"))
    assert src["independent_full_HR_verified"] is False
    assert src["candidate"]["eligibility"]["full_HR"] is False
    assert src["candidate"]["eligibility"]["outcome_rows_opened"] is False
    assert src["context_figshare"]["no_cross_study_ID_join"] is True
    assert src["prior_archive"]["already_attempted_in_egwe"] is True
    assert src["prior_archive"]["historical_result"]=="not_identifiable_from_archive"

def test_required_genetic_history_is_a_label_not_a_molecular_genotype() -> None:
    required=MOD.TRAINE_REQUIRED
    assert {"plant","matrix","cohort","temp_genotype","poll_genotype",
            "bee_flower_visits","seed_number"} <= required
    assert "microsatellite_genotype" not in required
    assert "F_ST" not in required


def test_dryad_file_id_from_api_download_relation() -> None:
    entry={
        "path":"data_local_adapt_traits.csv","size":288058,
        "_links":{
            "self":{"href":"/api/v2/files/5123456"},
            "stash:download":{"href":"/api/v2/files/5123456/download"},
        },
    }
    assert MOD._dryad_file_id(entry)==5123456
    assert MOD._dryad_file_id({"id":5123457,"_links":{}})==5123457


def test_missing_file_id_is_a_schema_stop_not_a_biology_null() -> None:
    with pytest.raises(ValueError,match="file_id_missing"):
        MOD._dryad_file_id({"path":"data_local_adapt_traits.csv","_links":{}})
