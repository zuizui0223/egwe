import pytest

from eco_genetic_warning_extensions.mutation_coordinates import MutationCoordinates
from eco_genetic_warning_extensions.protocol002_mutation_slot_fixture import (
    MutationSlotFixture,
    iterate_mutation_slot,
    protocol002_mutation_slot_trajectory,
    symmetric_slot_bridge_differences,
    upstream_symmetric_slot_trajectory,
)


def test_mutation_slot_fixture_is_inclusive_and_deterministic() -> None:
    fixture = MutationSlotFixture(initial_frequency=0.25, generations=3)
    trajectory = iterate_mutation_slot(fixture, lambda value: value + 0.10)
    assert trajectory == pytest.approx((0.25, 0.35, 0.45, 0.55))


def test_protocol002_mutation_slot_trajectory_applies_coordinate_map_only() -> None:
    fixture = MutationSlotFixture(initial_frequency=0.40, generations=2)
    coordinate = MutationCoordinates(kappa_mu=0.20, p_star=0.75)
    trajectory = protocol002_mutation_slot_trajectory(fixture, coordinate)
    expected_1 = 0.20 * 0.75 + 0.80 * 0.40
    expected_2 = 0.20 * 0.75 + 0.80 * expected_1
    assert trajectory == pytest.approx((0.40, expected_1, expected_2))


def test_symmetric_slot_bridge_matches_upstream_across_generations() -> None:
    fixture = MutationSlotFixture(initial_frequency=0.13, generations=12)
    assert symmetric_slot_bridge_differences(fixture, symmetric_mutation_rate=0.10) == pytest.approx((0.0,) * 13)


def test_symmetric_slot_trajectories_match_directly() -> None:
    fixture = MutationSlotFixture(initial_frequency=0.91, generations=8)
    protocol = protocol002_mutation_slot_trajectory(
        fixture,
        MutationCoordinates(kappa_mu=0.20, p_star=0.50),
    )
    upstream = upstream_symmetric_slot_trajectory(fixture, symmetric_mutation_rate=0.10)
    assert protocol == pytest.approx(upstream)


def test_mutation_slot_fixture_validates_inputs() -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        MutationSlotFixture(initial_frequency=1.2, generations=1)
    with pytest.raises(ValueError, match="non-negative"):
        MutationSlotFixture(initial_frequency=0.2, generations=-1)
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        iterate_mutation_slot(MutationSlotFixture(initial_frequency=0.95, generations=1), lambda value: value + 0.10)
