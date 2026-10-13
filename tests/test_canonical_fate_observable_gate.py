import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("canonical_gate",Path(__file__).resolve().parents[1]/"scripts/canonical_fate_observable_gate.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_actual_operator_and_matched_marginals():
    r=m.compare()
    assert r["canonical_operator_imported"]
    assert r["same_marginals"]
    assert r["states"]["aligned"]["patches_above_0625"]==2
    assert r["states"]["reversed"]["patches_above_0625"]==4
    assert r["one_step_threshold_count_difference"]==2
    assert abs(r["states"]["aligned"]["mean_next_q"]-.6715314616718732)<1e-12
    assert abs(r["states"]["reversed"]["mean_next_q"]-.6892968516234685)<1e-12
    assert r["states"]["aligned"]["max_next_q"]>r["states"]["reversed"]["max_next_q"]
    assert not r["future_hitting_probability_computed"]
    assert not r["natural_validation"]
