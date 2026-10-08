from __future__ import annotations

import pytest
from scripts import probe_mac_hugh_rsf_iid_schema as s


def _metadata() -> dict:
    return {"data":{"latestVersion":{"files":[{
        "label":s.TARGET,
        "dataFile":{
            "id":s.EXPECTED_FILE_ID,
            "md5":s.EXPECTED_SOURCE_MD5_FROM_MANIFEST,
            "filesize":106240906
        }
    }]}}}


def test_source_schema_detects_possible_synchronous_locations() -> None:
    row=b"animal_id\ttimestamp\tlongitude\tlatitude\tAnnee\nF1\t2004-01-01T00:00:00Z\t0\t0\t2004\n"
    result=s.inspect_manifest_and_header(_metadata(),row.splitlines(keepends=True)[0])
    assert result["possible_same_time_IID_reconstruction"] is True
    assert result["source_data_rows_parsed"]==0
    assert result["source_outcome_rows_parsed"]==0


def test_source_schema_fails_if_year_only_no_clock() -> None:
    out=s.inspect_manifest_and_header(_metadata(),b"Annee\telkID\tX\tY\n")
    assert out["possible_same_time_IID_reconstruction"] is False
    assert out["clock_field_candidates"]==[]


def test_manifest_fingerprint_change_fails_closed() -> None:
    data=_metadata()
    data["data"]["latestVersion"]["files"][0]["dataFile"]["md5"]="other"
    with pytest.raises(RuntimeError,match="manifest digest mismatch"):
        s.inspect_manifest_and_header(data,b"Annee\tID\tX\tY\n")
