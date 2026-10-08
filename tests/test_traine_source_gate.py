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
