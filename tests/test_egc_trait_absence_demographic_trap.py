"""Pure proof/certificate and actual pinned EGC trajectory regression tests."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0,str(SCRIPTS))
SPEC=importlib.util.spec_from_file_location(
    "egc_demographic_trap",SCRIPTS/"egc_trait_absence_demographic_trap.py")
assert SPEC and SPEC.loader
TRAP=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRAP)


def test_source_specific_global_analytic_bounds() -> None:
    d=TRAP.certificate()
    assert d["status"]=="SOURCE_SPECIFIC_ANALYTICAL_INVARIANCE_CERTIFICATE"
    a=d["first_step"]
    b=d["second_step"]
    c=d["third_step"]
    assert a["uniform_q1_upper"]==pytest.approx(.708632149106754)
    assert a["real_N1_continuous_upper"]==pytest.approx(29.146426457048918)
    assert a["integer_N1_upper"]==29
    assert b["uniform_q2_upper"]==pytest.approx(.6060879465033897)
    assert b["integer_N2_upper"]==27
    assert c["uniform_q3_upper"]==pytest.approx(.5145821841717118)
    assert c["uniform_q3_upper"]<.59
    assert c["integer_N3_upper"]<=29
    assert d["potential_high_trait_viability"]["tested_high_trait_grid_count"]==31
    assert d["potential_high_trait_viability"]["maximum_fitness_under_q_0_59"]==pytest.approx(
        .9929305031103611)
    assert d["potential_high_trait_viability"]["argmax_trait_bin"]==pytest.approx(.97)
    assert not d["new_NEE_AUC_or_confirmatory_evidence"]
    assert not d["all_future_trait_bin_occupancy_guaranteed_absent"]


def test_invariant_region_suffices_for_all_future_generations():
    d=TRAP.certificate()
    r=d["forward_invariant_region_from_t3"]
    assert r["q_upper"]==pytest.approx(.59)
    assert r["N_upper"]==29
    assert r["next_q_upper_with_any_trait_and_allele"]==pytest.approx(
        .5495060162450139)
    assert r["next_q_upper_with_any_trait_and_allele"]<r["q_upper"]
    assert r["next_N_upper_with_any_trait_and_allele"]<=r["N_upper"]


def test_population_calculus_upper_for_any_initial_abundance_sampled():
    proof=TRAP.certificate()
    q1max=proof["first_step"]["uniform_q1_upper"]
    realbound=proof["first_step"]["real_N1_continuous_upper"]
    for n0 in [1,5,20,29,39,40,41,49,80,150,500,1500,10000]:
        n1=n0*__import__("math").exp(
            .3+.4*q1max+.1-n0/40)
        assert n1<=realbound+1e-12
        assert max(1,round(n1))<=29


def test_invariant_fitness_under_real_pinned_trait_grid_source():
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("pinned source available in dedicated CI")
    from run_pinned_egc_aa_rr_lifecycle import load_source
    Params,_=load_source()
    from causal_model.multipatch_criticality_dynamics import (
        trait_grid,trait_fitness,trait_space_summary)
    prm=_source_params(Params,(40,),(1.,),(1.,),5)
    src=TRAP.PARAMS
    for key in (
        "interaction_feedback","interaction_barrier",
        "q_feedback_alpha","q_feedback_beta_trait","q_feedback_gamma_allele",
        "baseline_growth","interaction_growth","high_allele_growth",
        "density_capacity","low_base","low_cost","high_base",
        "high_interaction_benefit","high_peak_width",
        "high_trait_cutoff","viability_threshold","trait_grid_size",
    ):
        assert getattr(prm,key)==src[key],f"pinned EGC parameter drift: {key}"
    for q in (.1,.3,.5145821841717118,.59):
        for z in trait_grid(prm):
            assert TRAP.high_trait_fitness(z,q)==pytest.approx(
                trait_fitness(z,q,prm),abs=1e-14)
    assert trait_space_summary(.59,prm).high_trait_component_present is False
    assert not trait_space_summary(.59,prm).high_trait_margin>=0


def _source_params(Params, N0, q0, p0, generations,seed=101,migration=0.):
    from run_pinned_egc_aa_rr_lifecycle import initial_trait_row
    n=len(N0)
    return Params(
        patch_areas=(1.,)*n,generations=generations,
        initial_population=tuple(N0),
        initial_interaction=tuple(q0),
        initial_high_allele_frequency=tuple(p0),
        initial_trait_distribution=tuple(initial_trait_row(0.) for _ in range(n)),
        density_capacity=40.,area_reference=1.,
        interaction_feedback=4.5,interaction_barrier=.5025,
        q_feedback_alpha=.6,q_feedback_beta_trait=.3,q_feedback_gamma_allele=.1,
        baseline_growth=.3,interaction_growth=.4,high_allele_growth=.1,
        genotype_trait_recruitment="two_kernel_recruitment",
        inheritance_weight=.5,trait_occupancy_mode="finite_trait_bin_recruitment",
        migration_rate=migration,random_seed=seed)


@pytest.mark.parametrize("N0", [1,20,29,39,40,45,49,80,250])
@pytest.mark.parametrize("q0,p0",[(.2,.04),(.8,.4),(1.,1.)])
def test_actual_pinned_stochastic_trajectories_respect_global_bounds(
    N0,q0,p0) -> None:
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("pinned source available in dedicated CI")
    from run_pinned_egc_aa_rr_lifecycle import load_source
    Params,run=load_source()
    prm=_source_params(Params,(N0,),(q0,),(p0,),6)
    snapshots=run(prm,mutation_rate=.02).snapshots
    c=TRAP.certificate()
    assert snapshots[0].trait_occupancy[0].high_trait_mass==0
    assert snapshots[1].population[0]<=c["first_step"]["integer_N1_upper"]
    assert snapshots[1].interaction[0]<=c["first_step"]["uniform_q1_upper"]+1e-12
    assert snapshots[2].population[0]<=c["second_step"]["integer_N2_upper"]
    assert snapshots[2].interaction[0]<=c["second_step"]["uniform_q2_upper"]+1e-12
    for s in snapshots[3:]:
        assert s.population[0]<=29
        assert s.interaction[0]<=.59
        assert s.trait_space[0].high_trait_component_present is False


def test_multpatch_allele_migration_cannot_rescue_perturbed_eco_support():
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("pinned source available in dedicated CI")
    from run_pinned_egc_aa_rr_lifecycle import load_source
    Params,run=load_source()
    prm=_source_params(
        Params,(40,20,250),(1.,.8,.2),(1.,.4,0.),7,
        seed=299,migration=.5)
    s=run(prm,mutation_rate=.1).snapshots
    for snap in s[3:]:
        assert all(q<.59 for q in snap.interaction)
        assert all(not x.high_trait_component_present for x in snap.trait_space)


def test_recruitment_can_show_trait_after_potential_viability_lost():
    if not os.getenv("EGC_PINNED_ROOT"):
        pytest.skip("pinned source available in dedicated CI")
    from run_pinned_egc_aa_rr_lifecycle import load_source
    Params,run=load_source()
    prm=_source_params(Params,(40,),(1.,),(1.,),7)
    result=run(prm,mutation_rate=0.)
    assert any(s.trait_occupancy[0].realised_high_trait_occupied
               for s in result.snapshots[3:])
    assert all(not s.trait_space[0].high_trait_component_present
               for s in result.snapshots[3:])


def test_proof_fails_closed_on_bad_inputs() -> None:
    with pytest.raises(ValueError):
        TRAP.high_trait_fitness(1.1,.5)
    with pytest.raises(ValueError):
        TRAP.real_population_upper(1.1)
    with pytest.raises(ValueError):
        TRAP.numeric_round_upper(float("nan"))
