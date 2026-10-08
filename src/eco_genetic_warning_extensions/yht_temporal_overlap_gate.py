"""Metadata-only feasibility gate for the frozen Ya Ha Tinda forecasting protocol.

No movement locations, calf:cow observations, or other biological outcome values
are accessed by this module. A publication-date upper bound cannot prove that
a year is represented in the data; it can only prove that later observations
were unavailable in that archived version.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

ANALYSIS_ID = "yht_primary_outcome_temporal_overlap_gate_v1"
SOURCE_DOI = "10.5061/dryad.6wwpzgmw7"
SOURCE_VERSION_PUBLISHED = date(2020, 7, 21)
SOURCE_VERSION_LABEL = "Dryad version dated 2020-07-21"
NOMINAL_GPS_CANDIDATE_YEARS = (
    2004, 2005, 2006, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
)
MINIMUM_ANNUAL_OBSERVATIONS = 11


def assess(
    *,
    published: date = SOURCE_VERSION_PUBLISHED,
    candidate_years: tuple[int, ...] = NOMINAL_GPS_CANDIDATE_YEARS,
    minimum_annual_observations: int = MINIMUM_ANNUAL_OBSERVATIONS,
) -> dict[str, Any]:
    """Compute a strict upper bound on usable annual observations from dates only.

    The frozen autumn (calendar year t) score predicts a February-March
    (calendar year t+1) calf:cow survey. Survey observations have to precede
    the publication of the pinned archival version. The full survey interval
    ends on March 31; the reported limit is an optimistic necessary condition,
    *not* evidence of any actual survey record being present.
    """
    years = tuple(sorted(set(int(y) for y in candidate_years)))
    if not years:
        raise ValueError("candidate year set must be nonempty")
    if minimum_annual_observations < 1:
        raise ValueError("minimum annual observations must be positive")
    if any(y < 1900 or y >= 9999 for y in years):
        raise ValueError("invalid candidate year")

    possible = tuple(
        y for y in years if date(y + 1, 3, 31) <= published
    )
    impossible = tuple(y for y in years if y not in possible)
    stopped = len(possible) < minimum_annual_observations
    return {
        "analysis_id": ANALYSIS_ID,
        "status": (
            "STOP_PRIMARY_NOT_IDENTIFIABLE_ARCHIVE_TEMPORAL_OVERLAP"
            if stopped else "TEMPORAL_UPPER_BOUND_PASSES_AWAIT_RAW_YEAR_JOIN"
        ),
        "basis": "metadata_only_before_any_demographic_outcome_values",
        "source_doi": SOURCE_DOI,
        "source_version": SOURCE_VERSION_LABEL,
        "source_published_on": published.isoformat(),
        "forecast_exposure": "September 15 through November 15 of year t",
        "forecast_outcome": "observed February-March calf:cow ratio of year t+1",
        "frozen_required_annual_observations": minimum_annual_observations,
        "published_nominal_gps_candidate_years": list(years),
        "possible_years_upper_bound": list(possible),
        "impossible_years_from_publication_cutoff": list(impossible),
        "n_possible_years_upper_bound": len(possible),
        "stop": stopped,
        "limitations": (
            "This uses only the publication date of the pinned Dryad version, "
            "the frozen endpoint timing, and pre-acquisition nominal GPS year counts. "
            "Any eligible year in the upper bound may still fail official movement "
            "coverage, survey availability, or demographic join. This is not a "
            "forecast result, ecological null, or original-source row-level audit."
        ),
        "decision": (
            "Do not request GPS bytes or open the calf:cow outcomes to rescue "
            "the frozen primary: its 11-year minimum cannot be met using this "
            "2020-07-21 Dryad archival version. Do not lower n, change outcome, "
            "shift time, or use post-2020 sources within this registered route."
            if stopped else
            "Temporal dates alone do not rule out the registered primary; "
            "official source, movement and outcome join gates are still required."
        ),
    }


def assess_from_protocol(path: str | Path) -> dict[str, Any]:
    protocol = json.loads(Path(path).read_text(encoding="utf-8"))
    if protocol["sources"]["demographic_doi"] != SOURCE_DOI:
        raise RuntimeError("demographic DOI no longer matches the locked primary")
    if protocol["primary_models"]["minimum_total_eligible_annual_observations"] != MINIMUM_ANNUAL_OBSERVATIONS:
        raise RuntimeError("minimum annual observation count changed from the locked primary")
    if protocol["primary_outcome"]["name"] != "following_late_winter_calf_cow_ratio":
        raise RuntimeError("the locked outcome is no longer the intended survey")
    return assess()


def write(protocol_path: str | Path, output_path: str | Path) -> None:
    result = assess_from_protocol(protocol_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
