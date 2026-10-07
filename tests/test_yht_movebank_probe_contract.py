from __future__ import annotations

from eco_genetic_warning_extensions import yht_spatial_warning_coverage as coverage


def test_candidate_coverage_module_retains_frozen_thresholds() -> None:
    assert coverage.MIN_DAILY_INDIVIDUALS == 10
    assert coverage.MIN_ELIGIBLE_DAYS_PER_YEAR == 30
    assert coverage.PRIMARY_WINDOW_START == (9, 15)
    assert coverage.PRIMARY_WINDOW_END == (11, 15)
    assert coverage.MAX_NOON_OFFSET_HOURS == 6.5
