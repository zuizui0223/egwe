import importlib.util
import sys
from pathlib import Path
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
import pytest

spec=importlib.util.spec_from_file_location("robustness",Path(__file__).resolve().parents[1]/"scripts/egc_aa_rr_paired_robustness.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_exact_discordance_probability():
    assert m.exact_discordant_sign_test(0,0)==1
    assert m.exact_discordant_sign_test(0,5)==pytest.approx(0.0625)
    assert m.exact_discordant_sign_test(2,2)==1

def test_paired_endpoint_direction_and_denominator():
    a=[{"seed":i,"event_by_horizon":x,"final_occupied":not x,
        "final_population_total":40,"final_mean_q":.6}
       for i,x in zip([20001,20002,20003],[False,True,False])]
    b=[{"seed":i,"event_by_horizon":x,"final_occupied":y,
        "final_population_total":35,"final_mean_q":.7}
       for i,x,y in zip([20001,20002,20003],[True,True,False],[True,False,True])]
    x=m.summarize({"generations":12,"arms":{"AA":{"cases":a},"RR":{"cases":b}}})
    assert x["first_passage_ever"]["AA_count"]==1
    assert x["first_passage_ever"]["RR_count"]==2
    assert x["first_passage_ever"]["AA_minus_RR"]==pytest.approx(-1/3)
    assert x["occupied_at_final_snapshot"]["AA_count"]==2
    assert x["occupied_at_final_snapshot"]["RR_count"]==2
    assert x["paired_seed_design_does_not_guarantee_shared_random_draws"]

def test_missing_paired_seed_stops():
    a=[{"seed":20001}]
    b=[{"seed":20002}]
    with pytest.raises(ValueError):
        m.summarize({"generations":12,"arms":{"AA":{"cases":a},"RR":{"cases":b}}})
