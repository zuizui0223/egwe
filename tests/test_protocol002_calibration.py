import pytest

from eco_genetic_warning_extensions.mutation_coordinates import MutationCoordinates
from eco_genetic_warning_extensions.protocol002_calibration import (
    CALIBRATION_BARRIER_INCREASES,
    CALIBRATION_HOLD_GENERATIONS,
    CALIBRATION_MASTER_SEEDS,
    CALIBRATION_RAMP_GENERATIONS,
    CALIBRATION_REPLICATES_PER_CELL,
    Protocol002CalibrationCandidate,
    assert_protocol002_blind_calibration_columns,
    protocol002_calibration_candidate_from_row,
    select_protocol002_calibration_domain,
)


def make_candidate(
    *,
    pooled_rates=(0.4, 0.5, 0.6, 0.5, 0.5),
    hold=90,
    barrier=0.30,
    area=1.0,
    kappa=4.5,
    coordinate=MutationCoordinates(kappa_mu=0.20, p_star=0.50),
):
    return Protocol002CalibrationCandidate(
        coordinate=coordinate,
        area_reference=area,
        kappa=kappa,
        ramp_generations=30,
        hold_generations=hold,
        normalised_barrier_increase=barrier,
        seed_block_trait_loss_rates=tuple(pooled_rates),
    )


def test_protocol002_calibration_constants_match_plan() -> None:
    assert CALIBRATION_RAMP_GENERATIONS == 30
    assert CALIBRATION_HOLD_GENERATIONS == (90, 210)
    assert CALIBRATION_BARRIER_INCREASES == (0.15, 0.30, 0.45)
    assert CALIBRATION_MASTER_SEEDS == (20270310, 20270311, 20270312, 20270313, 20270314)
    assert CALIBRATION_REPLICATES_PER_CELL == 5


def test_candidate_horizon_pooling_and_eligibility() -> None:
    candidate = make_candidate()
    assert candidate.horizon == 120
    assert candidate.pooled_trait_loss_rate == pytest.approx(0.50)
    assert candidate.is_eligible() is True


def test_eligibility_requires_every_seed_block_in_band() -> None:
    assert make_candidate(pooled_rates=(0.30, 0.40, 0.50, 0.60, 0.70)).is_eligible() is True
    assert make_candidate(pooled_rates=(0.29, 0.50, 0.50, 0.50, 0.71)).is_eligible() is False


def test_blind_guard_rejects_warning_and_diversity_fields() -> None:
    for forbidden in ("warning_time", "h_alpha_r05", "usable_lead_time", "genetic_diversity", "event_pair_validity"):
        with pytest.raises(ValueError, match="trait-loss-only"):
            assert_protocol002_blind_calibration_columns(("trait_loss_time", forbidden))


def test_blind_guard_accepts_trait_loss_only_fields() -> None:
    assert_protocol002_blind_calibration_columns(
        ("kappa_mu", "p_star", "trait_loss_time", "trait_loss_observed", "master_seed")
    )


def test_candidate_from_row_is_typed_and_blind() -> None:
    candidate = protocol002_calibration_candidate_from_row(
        {
            "kappa_mu": 0.20,
            "p_star": 0.75,
            "area_reference": 1.2,
            "kappa": 6.0,
            "ramp_generations": 30,
            "hold_generations": 210,
            "normalised_barrier_increase": 0.45,
        },
        seed_block_rates=(0.3, 0.4, 0.5, 0.6, 0.7),
    )
    assert candidate.coordinate == MutationCoordinates(kappa_mu=0.20, p_star=0.75)
    assert candidate.horizon == 240
    assert candidate.is_eligible() is True


def test_deterministic_rank_order_matches_protocol() -> None:
    coordinate = MutationCoordinates(kappa_mu=0.20, p_star=0.50)
    candidates = (
        make_candidate(pooled_rates=(0.4, 0.4, 0.4, 0.4, 0.4), coordinate=coordinate),
        make_candidate(pooled_rates=(0.5, 0.5, 0.5, 0.5, 0.5), hold=210, coordinate=coordinate),
        make_candidate(pooled_rates=(0.5, 0.5, 0.5, 0.5, 0.5), hold=90, barrier=0.45, coordinate=coordinate),
        make_candidate(pooled_rates=(0.5, 0.5, 0.5, 0.5, 0.5), hold=90, barrier=0.15, coordinate=coordinate),
    )
    selected = select_protocol002_calibration_domain(candidates, coordinate=coordinate)
    assert selected is not None
    assert selected.hold_generations == 90
    assert selected.normalised_barrier_increase == pytest.approx(0.15)


def test_selection_ignores_other_coordinates_and_returns_none_without_eligible_domain() -> None:
    target = MutationCoordinates(kappa_mu=0.20, p_star=0.50)
    other = MutationCoordinates(kappa_mu=0.20, p_star=0.75)
    candidates = (
        make_candidate(pooled_rates=(0.1, 0.1, 0.1, 0.1, 0.1), coordinate=target),
        make_candidate(pooled_rates=(0.5, 0.5, 0.5, 0.5, 0.5), coordinate=other),
    )
    assert select_protocol002_calibration_domain(candidates, coordinate=target) is None


def test_candidate_validation_rejects_invalid_rates() -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        make_candidate(pooled_rates=(0.5, 1.1))
