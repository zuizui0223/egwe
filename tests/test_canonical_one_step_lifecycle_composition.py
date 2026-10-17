import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("composition",Path(__file__).resolve().parents[1]/"scripts/canonical_one_step_lifecycle_composition.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def test_pinned_operators_composed_without_loss_claim():
    d=m.run()
    a=d["outcomes"]["AA"];r=d["outcomes"]["RR"]
    assert len(a["conditional_population_next"])==4
    assert len(r["conditional_recruit_high_trait_mass"])==4
    assert a["maximum_population_next"]>r["maximum_population_next"]
    assert r["mean_population_next"]>a["mean_population_next"]
    assert not d["full_model_long_horizon_loss_estimated"]
    assert not d["stochastic_loss_probability_estimated"]
    assert not d["natural_data_used"]
