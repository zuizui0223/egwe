from __future__ import annotations

import math
from statistics import fmean, stdev
from typing import Iterable, Sequence

LOVE_OTTO_REPOSITORY = "nicolalove/shapeshiftr"
LOVE_OTTO_COMMIT = "e38982570c76161593a44b70569aad70f283b5aa"


def _as_points(points: Iterable[Sequence[float]]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for row in points:
        if len(row) != 2:
            raise ValueError("each point must contain exactly two coordinates")
        x, y = float(row[0]), float(row[1])
        if not (math.isfinite(x) and math.isfinite(y)):
            raise ValueError("coordinates must be finite")
        out.append((x, y))
    if len(out) < 3:
        raise ValueError("Love-Otto CV metrics require at least three nondegenerate points")
    return out


def _pairwise(points: list[tuple[float, float]]) -> list[list[float]]:
    n = len(points)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        xi, yi = points[i]
        for j in range(i):
            xj, yj = points[j]
            d = math.hypot(xi - xj, yi - yj)
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix


def cvpop(points: Iterable[Sequence[float]]) -> float:
    """Population-level CV of all pairwise inter-individual distances.

    This mirrors shapeshiftr::cvpop() at pinned commit LOVE_OTTO_COMMIT:
    sample SD of the lower-triangle pairwise distances divided by their mean.
    """
    pts = _as_points(points)
    matrix = _pairwise(pts)
    distances = [matrix[i][j] for i in range(len(pts)) for j in range(i)]
    mean_distance = fmean(distances)
    if mean_distance <= 0:
        raise ValueError("mean pairwise distance must be positive")
    return float(stdev(distances) / mean_distance)


def cvind(points: Iterable[Sequence[float]]) -> float:
    """Individual-level CV of each individual's mean distance to all others.

    This mirrors shapeshiftr::cvind() at pinned commit LOVE_OTTO_COMMIT.
    """
    pts = _as_points(points)
    matrix = _pairwise(pts)
    means = []
    for i in range(len(pts)):
        d = [matrix[i][j] for j in range(len(pts)) if j != i]
        mean_distance = fmean(d)
        if mean_distance <= 0:
            raise ValueError("each individual must have positive mean distance to others")
        means.append(mean_distance)
    overall = fmean(means)
    if overall <= 0:
        raise ValueError("mean individual distance must be positive")
    return float(stdev(means) / overall)


def cvratio(points: Iterable[Sequence[float]]) -> float:
    """Ratio CV_ind / CV_pop, matching shapeshiftr::cvratio(log10=FALSE)."""
    pts = _as_points(points)
    pop = cvpop(pts)
    ind = cvind(pts)
    if pop <= 0:
        raise ValueError("population-level CV must be positive for a finite ratio")
    return float(ind / pop)
