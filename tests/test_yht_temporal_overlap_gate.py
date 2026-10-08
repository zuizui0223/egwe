from __future__ import annotations

from datetime import date
import json
from pathlib import Path

from eco_genetic_warning_extensions.yht_temporal_overlap_gate import (
    ANALYSIS_ID, MINIMUM_ANNUAL_OBSERVATIONS,
    NOMINAL_GPS_CANDIDATE_YEARS, SOURCE_VERSION_PUBLISHED, assess, assess_from_protocol,
)


def test_locked_2020_dryad_archive_fails_frozen_primary_without_opening_outcomes() -> None:
    assert SOURCE_VERSION_PUBLISHED == date(2020, 7, 21)
    assert MINIMUM_ANNUAL_OBSERVATIONS == 11
    assert len(NOMINAL_GPS_CANDIDATE_YEARS) == 11
    out = assess()
    assert out["analysis_id"] == ANALYSIS_ID
    assert out["basis"] == "metadata_only_before_any_demographic_outcome_values"
    assert out["stop"] is True
    assert out["status"] == "STOP_PRIMARY_NOT_IDENTIFIABLE_ARCHIVE_TEMPORAL_OVERLAP"
    assert out["n_possible_years_upper_bound"] == 10
    assert out["impossible_years_from_publication_cutoff"] == [2020]
    assert out["possible_years_upper_bound"] == [
        2004, 2005, 2006, 2013, 2014, 2015, 2016, 2017, 2018, 2019
    ]


def test_new_publication_year_would_require_new_source_and_still_not_prove_coverage() -> None:
    later = assess(published=date(2021, 4, 1))
    assert later["stop"] is False
    assert later["n_possible_years_upper_bound"] == 11
    assert later["status"] == "TEMPORAL_UPPER_BOUND_PASSES_AWAIT_RAW_YEAR_JOIN"


def test_earlier_version_cannot_increase_available_years() -> None:
    older = assess(published=date(2019, 7, 21))
    assert older["stop"] is True
    assert older["n_possible_years_upper_bound"] < 10


def test_committed_metadata_stop_matches_frozen_protocol_and_function() -> None:
    root = Path(__file__).resolve().parents[1]
    result = json.loads(
        (root / "artifacts/yht_spatial_warning/primary_temporal_overlap_stop.json")
        .read_text(encoding="utf-8")
    )
    assert result == assess_from_protocol(
        root / "experiments/yht_spatial_warning_protocol.json"
    )
