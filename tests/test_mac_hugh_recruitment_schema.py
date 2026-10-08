from __future__ import annotations

import hashlib

import pytest

from scripts import probe_mac_hugh_recruitment_schema as s


def _mock(raw: bytes) -> dict:
    return {
        "data": {
            "latestVersion": {
                "versionNumber": 1,
                "files": [{
                    "label": s.TARGET,
                    "dataFile": {"id": 984869, "md5": hashlib.md5(raw).hexdigest()},
                }],
            }
        }
    }


def test_schema_gate_uses_only_header_and_count(monkeypatch: pytest.MonkeyPatch) -> None:
    raw = b"Annee\tRecrutement\tVariance_long\tMoyenne_long\tNb_femelle\n1999\t999\t22\t11\t3\n2000\t888\t20\t10\t4\n"
    monkeypatch.setattr(s, "EXPECTED_SOURCE_MD5", hashlib.md5(raw).hexdigest())
    out = s.audit_schema(_mock(raw), raw)
    assert out["raw_row_count_not_independent_year_count"] == 2
    assert out["required_source_fields_present"]
    assert out["candidate_time_field_names"] == ["Annee"]
    assert out["recruitment_row_values_parsed"] == 0
    assert out["forecast_models_fitted"] == 0
    assert "999" not in str(out)
    assert "888" not in str(out)


def test_hash_mismatch_fails_closed() -> None:
    raw = b"Annee\tRecrutement\tVariance_long\tMoyenne_long\tNb_femelle\n"
    with pytest.raises(RuntimeError, match="MD5 mismatch"):
        s.audit_schema(_mock(raw), raw + b"x")
