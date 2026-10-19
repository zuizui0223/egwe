"""Sanity-test source-receipt integrity and cohort-safe exploratory contrasts."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT=Path(__file__).resolve().parents[1]/"scripts/summarize_egc_reexpression_gate.py"
SPEC=importlib.util.spec_from_file_location("summary_gate",SCRIPT)
assert SPEC and SPEC.loader
SUMMARY=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SUMMARY)


def fixture():
    seeds=[50001,50002,50003,50004]
    conditions={
        "q0.20_p0.04":[0,0,0,1],
        "q0.20_p0.40":[1,1,1,1],
        "q0.80_p0.04":[0,0,1,1],
        "q0.80_p0.40":[1,1,1,1],
    }
    scenarios={}
    for label,flags in conditions.items():
        rows=[]
        for seed,x in zip(seeds,flags):
            rows.append({
                "seed":seed,
                "expressed_at_generation_1":bool(x),
                "three_consecutive_expressed_generations":bool(x),
                "final_expressed":bool(x),
                "ever_joint_zero":not bool(x),
            })
        counts={outcome:sum(bool(r[outcome]) for r in rows)
                for outcome in SUMMARY.ENDPOINTS}
        scenarios[label]={
            "initial_q":.2 if "q0.20" in label else .8,
            "initial_allele_frequency":.04 if "p0.04" in label else .4,
            "source_initial_high_trait_fitness":.66 if "q0.20" in label else 1.14,
            "summary":{
                "n":len(rows),
                "events":counts,
                "initial_one_step_expression_probability":sum(flags)/len(flags),
                "mean_q_at_generation_1":.2,
                "mean_q_at_generation_2":.1,
                "mean_expressed_snapshots":2.,
                "mean_latent_but_unexpressed_snapshots":1.,
            },
            "case_receipts":rows,
        }
    return {
        "pinned_egc_source_commit":"dd8ee379d0d3518194c767d16402042525bc00dc",
        "cohort":seeds,
        "horizon":12,
        "scenarios":scenarios,
    }


def test_exact_seed_group_contrast_and_bootstrap_reproducibility():
    raw=fixture()
    a=SUMMARY.audit(raw,bootstrap_reps=300,bootstrap_seed=20261019)
    b=SUMMARY.audit(raw,bootstrap_reps=300,bootstrap_seed=20261019)
    assert a==b
    assert a["seed_count"]==4
    assert a["seed_group_bootstrap"]["predeclared_confirmatory_test"] is False
    assert a["seed_group_bootstrap"]["do_not_treat_generations_as_independent"] is True
    assert a["no_natural_flower_or_pollen_observations"] is True
    contrast=a["contrasts"]["allele_p040_minus_p004_at_q020"]
    o=contrast["outcomes"]["final_expressed"]
    assert o["difference_A_minus_B"]==.75
    assert o["A_only"]==3
    assert o["B_only"]==0
    assert -1<=o["seed_bootstrap_percentile_95_interval"][0]<=1
    assert -1<=o["seed_bootstrap_percentile_95_interval"][1]<=1


def test_source_pin_and_case_numbers_can_never_be_silently_changed():
    raw=fixture()
    raw["pinned_egc_source_commit"]="different"
    with pytest.raises(ValueError,match="source"):
        SUMMARY.audit(raw,100)


def test_missing_or_changed_case_level_results_are_rejected():
    raw=fixture()
    raw["scenarios"]["q0.20_p0.04"]["case_receipts"].pop()
    with pytest.raises(ValueError,match="seed"):
        SUMMARY.audit(raw,100)
    raw=fixture()
    raw["scenarios"]["q0.20_p0.04"]["summary"]["events"]["final_expressed"]=0
    with pytest.raises(ValueError,match="summary"):
        SUMMARY.audit(raw,100)


def test_all_four_cells_and_full_cohort_are_required():
    raw=fixture()
    raw["scenarios"].pop("q0.80_p0.40")
    with pytest.raises(ValueError,match="four"):
        SUMMARY.audit(raw,100)
    raw=fixture()
    raw["cohort"]=[50001,50002,50003,50003]
    with pytest.raises(ValueError,match="cohort"):
        SUMMARY.audit(raw,100)


def test_reject_uninformative_bootstrap():
    with pytest.raises(ValueError):
        SUMMARY.audit(fixture(),10)
