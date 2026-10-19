"""Frozen machine-record consistency for executed four-cell EGC result."""
from __future__ import annotations

import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from egc_latent_ecological_support_gate import next_q

RECEIPT=ROOT/"artifacts/egc_trait_reappearance/establishment_window_4cell_256seed_20261019_summary.json"


def test_source_receipt_and_four_cell_denominators_are_stable():
    d=json.loads(RECEIPT.read_text())
    assert d["source"]["commit"]=="dd8ee379d0d3518194c767d16402042525bc00dc"
    assert d["experiment"]["seed_first"]==50001
    assert d["experiment"]["seed_last"]==50256
    assert d["experiment"]["seed_count_per_cell"]==256
    assert len(d["scenario_results"])==4
    assert len(d["receipt"]["source_full_json_sha256"])==64
    assert d["scope_limits"]["no_field_validation"] is True
    assert d["scope_limits"]["source_frozen_NEE_unchanged"] is True


def test_mean_q1_exactly_matches_one_step_source_equation():
    d=json.loads(RECEIPT.read_text())
    for row in d["scenario_results"]:
        assert row["n_simulations"]==256
        assert row["initial_high_trait_count"]==0
        assert math.isclose(row["mean_q_generation_1"],next_q(
            row["q0"],row["p0"],.5,0.),rel_tol=0.,abs_tol=1e-12)
        assert (row["consecutive_three_generation_presence_count"]
                <=row["consecutive_two_generation_presence_count"]
                <=row["first_generation_expression_count"])
        assert 0<=row["high_trait_present_at_generation_12_count"]<=256
        assert 0<=row["ever_joint_genetic_and_trait_zero_count"]<=256


def test_descriptive_bootstrap_is_not_claimed_as_new_confirmatory_ecology():
    d=json.loads(RECEIPT.read_text())
    x=d["exploratory_descriptive_statistics"]
    assert "NOT" in x["method"]
    assert x["endpoint"]=="high trait present at generation 12"
    assert len(x["contrasts"])==4
    for row in x["contrasts"]:
        lo,hi=row["exploratory_seed_bootstrap_interval_95"]
        assert -1<=lo<=row["final_occupancy_proportion_difference"]<=hi<=1
    assert d["scope_limits"]["trait_expression_not_reproductive_success"]
    assert d["scope_limits"]["three_consecutive_occupancy_not_evolutionary_establishment"]
    assert d["scope_limits"]["high_allele_frequency_not_verified_molecular_regulatory_capability"]
