from __future__ import annotations

import math

import pytest

from eco_genetic_warning_extensions.love_otto_spatial_metrics import (
    LOVE_OTTO_COMMIT,
    cvind,
    cvpop,
    cvratio,
)


def test_pinned_love_otto_commit() -> None:
    assert LOVE_OTTO_COMMIT == "e38982570c76161593a44b70569aad70f283b5aa"


def test_three_collinear_points_match_closed_form() -> None:
    # Pairwise distances are 1, 2, 3: mean=2, sample SD=1 -> CV_pop=0.5.
    # Individual mean distances are 2, 1.5, 2.5: mean=2, sample SD=0.5
    # -> CV_ind=0.25 and ratio=0.5.
    points = [(0, 0), (1, 0), (3, 0)]
    assert math.isclose(cvpop(points), 0.5, rel_tol=0, abs_tol=1e-15)
    assert math.isclose(cvind(points), 0.25, rel_tol=0, abs_tol=1e-15)
    assert math.isclose(cvratio(points), 0.5, rel_tol=0, abs_tol=1e-15)


def test_metrics_are_translation_and_scale_invariant() -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (3.0, 0.0), (2.0, 4.0)]
    transformed = [(10.0 + 7.0*x, -3.0 + 7.0*y) for x, y in points]
    for fn in (cvpop, cvind, cvratio):
        assert math.isclose(fn(points), fn(transformed), rel_tol=0, abs_tol=1e-12)


def test_degenerate_inputs_fail_closed() -> None:
    with pytest.raises(ValueError):
        cvpop([(0, 0), (1, 0)])
    with pytest.raises(ValueError):
        cvratio([(0, 0), (0, 0), (0, 0)])
