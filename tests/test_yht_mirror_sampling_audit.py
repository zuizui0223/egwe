from __future__ import annotations

import math

import pytest

from eco_genetic_warning_extensions.yht_mirror_sampling_audit import (
    _linear_quantile,
    blob_sha,
    cv_ratio,
    utm11_nad83,
)


def test_projected_coordinate_matches_pyproj_reference() -> None:
    x, y = utm11_nad83(-115.49652, 51.67146)
    assert abs(x - 603965.856) < 0.5
    assert abs(y - 5725568.260) < 0.5


def test_ratio_matches_closed_form_and_scale_invariance() -> None:
    points = ((0.0, 0.0), (1.0, 0.0), (3.0, 0.0))
    assert math.isclose(cv_ratio(points), 0.5, abs_tol=1e-12)
    enlarged = tuple((x * 100 + 50, y * 100 - 50) for x, y in points)
    assert math.isclose(cv_ratio(points), cv_ratio(enlarged), abs_tol=1e-12)


def test_quantile_integer_index_and_blob_integrity() -> None:
    assert _linear_quantile([0.6, 0.4, 0.5], 0.5) == 0.5
    assert blob_sha(b"abc") == "f2ba8f84ab5c1bce84a7b441cb1959cfc7093b7f"


def test_degenerate_geometry_fails_closed() -> None:
    with pytest.raises(ValueError):
        cv_ratio(((0.0, 0.0), (0.0, 0.0), (0.0, 0.0)))
