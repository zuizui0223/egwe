import importlib.util
import os
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location("pinned_egc",Path(__file__).resolve().parents[1]/"scripts/run_pinned_egc_aa_rr_lifecycle.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_pinned_source_and_initial_occupancy():
    r=m.compare(2,[101,102])
    assert r["pinned_commit"]==m.PIN
    assert r["same_marginal_q"] and r["same_marginal_trait_and_allele"]
    assert r["event_is_absorbing"] is False
    assert r["event_is_first_passage_not_permanent_loss"]
    assert not r["natural_field_validation"]
    assert all(all(x["initial_occupied"] for x in arm["cases"]) for arm in r["arms"].values())
    assert all(len(arm["cases"])==2 for arm in r["arms"].values())

def test_wrong_source_commit_stops(monkeypatch,tmp_path):
    monkeypatch.setenv("EGC_PINNED_ROOT",str(tmp_path))
    with pytest.raises(ValueError,match="git checkout"):
        m.load_source()

def test_invalid_seed_or_horizon_stops():
    with pytest.raises(ValueError):
        m.compare(0,[101])
    with pytest.raises(ValueError):
        m.compare(3,[101,101])
