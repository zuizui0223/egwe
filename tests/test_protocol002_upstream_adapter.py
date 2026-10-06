import pytest

from eco_genetic_warning_extensions.mutation_coordinates import MutationCoordinates
from eco_genetic_warning_extensions.protocol002_stage0 import (
    LIFECYCLE_MUTATION_POSITION,
    UPSTREAM_COMMIT,
    UPSTREAM_MODULE,
    UPSTREAM_REPOSITORY,
)
from eco_genetic_warning_extensions.protocol002_upstream_adapter import (
    PINNED_UPSTREAM_LIFECYCLE,
    apply_protocol002_mutation,
    apply_symmetric_bridge,
    symmetric_bridge_coordinate,
    symmetric_bridge_differences,
    upstream_symmetric_reference,
    validate_frequency_sequence,
)


def test_upstream_lifecycle_lock_matches_stage0_certificate() -> None:
    assert PINNED_UPSTREAM_LIFECYCLE.repository == UPSTREAM_REPOSITORY
    assert PINNED_UPSTREAM_LIFECYCLE.commit == UPSTREAM_COMMIT
    assert PINNED_UPSTREAM_LIFECYCLE.module == UPSTREAM_MODULE
    assert PINNED_UPSTREAM_LIFECYCLE.mutation_position == LIFECYCLE_MUTATION_POSITION


def test_protocol002_adapter_changes_only_mutation_transform() -> None:
    frequencies = (0.0, 0.2, 0.5, 0.9, 1.0)
    coordinate = MutationCoordinates(kappa_mu=0.20, p_star=0.75)
    assert apply_protocol002_mutation(frequencies, coordinate) == pytest.approx(
        tuple(0.20 * 0.75 + 0.80 * value for value in frequencies)
    )


def test_symmetric_bridge_matches_pinned_upstream_reference() -> None:
    frequencies = (0.0, 0.2, 0.5, 0.9, 1.0)
    mu = 0.10
    assert apply_symmetric_bridge(frequencies, symmetric_mutation_rate=mu) == pytest.approx(
        tuple(upstream_symmetric_reference(value, symmetric_mutation_rate=mu) for value in frequencies)
    )
    assert symmetric_bridge_differences(frequencies, symmetric_mutation_rate=mu) == pytest.approx((0.0,) * len(frequencies))


def test_symmetric_bridge_coordinate_has_expected_rates() -> None:
    coordinate = symmetric_bridge_coordinate(symmetric_mutation_rate=0.10)
    assert coordinate.kappa_mu == pytest.approx(0.20)
    assert coordinate.p_star == pytest.approx(0.50)
    assert coordinate.low_to_high == pytest.approx(0.10)
    assert coordinate.high_to_low == pytest.approx(0.10)


def test_adapter_validates_frequency_inputs() -> None:
    with pytest.raises(ValueError, match="at least one"):
        validate_frequency_sequence(())
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        validate_frequency_sequence((0.1, 1.2))
    with pytest.raises(ValueError, match=r"\[0, 0.5\)"):
        symmetric_bridge_coordinate(symmetric_mutation_rate=0.50)
