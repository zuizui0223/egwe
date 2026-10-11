import importlib.util
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("finite_fate",Path(__file__).resolve().parents[1]/"scripts/finite_fate_lumpability.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_delayed_loss_divergence():
    r=m.example()
    assert not r["strong_lumpability"]
    assert r["first_hit"][0]["risk"][:2]==["0","0"]
    assert r["first_hit"][1]["risk"][:2]==["1","0"]

def test_lumpability_suffices():
    P=[["1/2",0,"1/2"],[0,"1/2","1/2"],[0,0,1]]
    r=m.analyze(P,["A","A","LOSS"],{2})
    assert r["strong_lumpability"]
    assert all(x["max_block_gap"]=="0" for x in r["first_hit"])

def test_loss_must_be_coarse_measurable():
    with pytest.raises(ValueError,match="measurable"):
        m.analyze([[1,0],[0,1]],["A","A"],{1})
