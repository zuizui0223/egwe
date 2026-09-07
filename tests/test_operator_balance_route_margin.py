from __future__ import annotations

import math
from pathlib import Path

from eco_genetic_warning_extensions.operator_balance_route_margin import (
    classify_margin,
    continuous_static_crossing_generation,
    critical_bundle_for_target,
    eco_genetic_bundle,
    first_static_unsafe_generation,
    initial_matched_marginal_certificate,
    next_interaction_from_state,
    q_only_route_margin,
    repair_shift,
    route_margin,
    selected_high_allele_frequency,
    support_signal,
    target_headroom,
)


def test_route_margin_sign_exactly_matches_next_q_side() -> None:
    theta = 0.58
    for q in (0.2, 0.5, 0.8, 0.95):
        for t in (0.1, 0.6, 0.9):
            for g in (0.2, 0.7):
                for d in (0.4, 0.8, 1.0):
                    margin = route_margin(q, t, g, d, theta)
                    q_next = next_interaction_from_state(q, t, g, d, theta)
                    if margin > 1e-12:
                        assert q_next > 0.625
                    elif margin < -1e-12:
                        assert q_next < 0.625
                    else:
                        assert math.isclose(q_next, 0.625, abs_tol=1e-12)


def test_margin_sign_synchronizes_allele_selection_and_trait_viability_switch() -> None:
    theta = 0.55
    p = 0.4
    for q, t, g, d in [(0.9, 0.9, 0.9, 1.0), (0.4, 0.2, 0.2, 0.8)]:
        margin = route_margin(q, t, g, d, theta)
        q_next = next_interaction_from_state(q, t, g, d, theta)
        p_sel = selected_high_allele_frequency(p, q_next)
        trait_fitness = 0.5 + 0.8 * q_next
        if margin > 0:
            assert q_next > 0.625
            assert p_sel > p
            assert trait_fitness > 1.0
        else:
            assert q_next < 0.625
            assert p_sel < p
            assert trait_fitness < 1.0


def test_exact_equality_boundary_hits_all_three_switches() -> None:
    theta = 0.60
    q = 0.8
    density = 1.0
    bundle = critical_bundle_for_target(q, density, theta)
    margin = route_margin(q, bundle, bundle, density, theta)
    q_next = next_interaction_from_state(q, bundle, bundle, density, theta)
    assert math.isclose(margin, 0.0, abs_tol=1e-12)
    assert math.isclose(q_next, 0.625, abs_tol=1e-12)
    p = 0.4
    assert math.isclose(selected_high_allele_frequency(p, q_next), p, abs_tol=1e-12)
    assert math.isclose(0.5 + 0.8 * q_next, 1.0, abs_tol=1e-12)


def test_full_feedback_margin_equals_qonly_plus_exact_repair_shift() -> None:
    theta = 0.58
    for q, t, g, d in [(0.4, 0.9, 0.8, 0.8), (0.8, 0.2, 0.3, 1.0), (0.6, 0.6, 0.6, 0.5)]:
        full = route_margin(q, t, g, d, theta)
        base = q_only_route_margin(q, d, theta)
        shift = repair_shift(q, t, g, d)
        assert math.isclose(full, base + shift, abs_tol=1e-12)


def test_critical_bundle_is_exact_repair_boundary() -> None:
    theta = 0.60
    q = 0.65
    density = 0.95
    bcrit = critical_bundle_for_target(q, density, theta)
    assert 0.0 < bcrit < 1.0
    assert classify_margin(route_margin(q, bcrit, bcrit, density, theta)) == "on_switch"
    assert route_margin(q, bcrit + 1e-6, bcrit + 1e-6, density, theta) > 0
    assert route_margin(q, bcrit - 1e-6, bcrit - 1e-6, density, theta) < 0


def test_repair_wedge_can_rescue_qonly_below_switch() -> None:
    theta = 0.60
    q = 0.65
    density = 0.95
    base = q_only_route_margin(q, density, theta)
    assert base < 0
    bcrit = critical_bundle_for_target(q, density, theta)
    bundle = min(1.0, bcrit + 0.05)
    assert bundle > q
    full = route_margin(q, bundle, bundle, density, theta)
    assert full > 0
    assert repair_shift(q, bundle, bundle, density) > -base


def test_feedback_can_also_suppress_when_bundle_is_below_q() -> None:
    theta = 0.50
    q = 0.8
    density = 1.0
    base = q_only_route_margin(q, density, theta)
    assert base > 0
    bundle = 0.0
    full = route_margin(q, bundle, bundle, density, theta)
    assert full < 0
    assert repair_shift(q, bundle, bundle, density) < 0


def test_locked_weight_decomposition_is_exact() -> None:
    q, t, g = 0.7, 0.9, 0.1
    b = eco_genetic_bundle(t, g)
    s = support_signal(q, t, g)
    assert math.isclose(b, 0.75 * t + 0.25 * g, abs_tol=1e-12)
    assert math.isclose(s, 0.6 * q + 0.4 * b, abs_tol=1e-12)
    assert math.isclose(s - q, 0.4 * (b - q), abs_tol=1e-12)


def test_locked_headroom_constant_is_preserved() -> None:
    assert math.isclose(target_headroom(0.0), 0.11351680528133122, abs_tol=1e-12)


def test_opening_certificate_is_exact_coverage_reserve_tradeoff() -> None:
    cert = initial_matched_marginal_certificate()
    aa = cert["conditions"]["AA"]
    rr = cert["conditions"]["RR"]
    assert all(math.isclose(got, expected, abs_tol=1e-12) for got, expected in zip(aa["support"], (0.47, 0.61, 0.75, 0.89)))
    assert all(math.isclose(got, expected, abs_tol=1e-12) for got, expected in zip(rr["support"], (0.71, 0.69, 0.67, 0.65)))
    assert math.isclose(aa["support_mean"], 0.68, abs_tol=1e-12)
    assert math.isclose(rr["support_mean"], 0.68, abs_tol=1e-12)
    assert math.isclose(aa["margin_mean"], rr["margin_mean"], abs_tol=1e-12)
    assert math.isclose(aa["margin_variance"] / rr["margin_variance"], 49.0, abs_tol=1e-10)
    assert aa["positive_margin_patch_count"] == 2
    assert rr["positive_margin_patch_count"] == 4
    assert aa["maximum_margin"] > 2.9 * rr["maximum_margin"]
    assert aa["frozen_state_first_unsafe_generation"] == (1, 1, 55, 111)
    assert rr["frozen_state_first_unsafe_generation"] == (39, 31, 23, 15)


def test_frozen_crossing_benchmark_is_not_dynamic_but_is_exact_algebraically() -> None:
    assert math.isclose(continuous_static_crossing_generation(0.71), 38.59327788746751, abs_tol=1e-10)
    assert first_static_unsafe_generation(0.71) == 39
    assert first_static_unsafe_generation(0.89) == 111


def test_theorem_document_preserves_claim_ceiling() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "OPERATOR_BALANCE_ROUTE_MARGIN_THEOREM_2026-09-06.md").read_text().casefold()
    assert "operator-balance route margin" in text
    assert "0.1135168053" in text
    assert "repair wedge" in text
    assert "coverage–reserve trade-off" in text
    assert "not asserted as a universal natural state variable" in text
    assert "long-horizon sufficient statistic" in text
    assert "not a dynamic trajectory prediction" in text
