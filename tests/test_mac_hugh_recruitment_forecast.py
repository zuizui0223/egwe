from __future__ import annotations

from eco_genetic_warning_extensions.mac_hugh_recruitment_forecast import (
    audit_forecasts, load_complete_lagged_cases,
)


def _source(years: list[int], *, missing_year: int | None = None) -> str:
    lines = ["Annee\tRecrutement\tMoyenne_long\tVariance_long\tMoyenne_58\tNb_femelle"]
    for y in years:
        geo = ((y * 17) % 23) / 3
        effort = 10 + ((y * 7) % 11)
        ratio = 1 + 0.3 * ((y * 3) % 13) + 0.4 * geo
        if y == missing_year:
            lines.append(f"{y}\tNA\t10\t{geo}\t5\t{effort}")
        else:
            lines.append(f"{y}\t{ratio}\t10\t{geo}\t5\t{effort}")
    return "\n".join(lines) + "\n"


def test_consecutive_lag_no_gap_interpolation() -> None:
    cases, counts = load_complete_lagged_cases(_source([2000, 2001, 2002, 2004, 2005]))
    assert counts["n_complete_consecutive_lagged_years"] == 3
    assert counts["eligible_years"] == [2001, 2002, 2005]


def test_insufficient_years_is_not_a_prediction_null() -> None:
    out = audit_forecasts(_source(list(range(2000, 2010))))
    assert out["status"] == "insufficient_temporal_replication_stop_before_model_fit"
    assert out["fitted_forecast_models"] == 0


def test_complete_source_produces_rolling_predictions_without_raw_value_export() -> None:
    out = audit_forecasts(_source(list(range(1995, 2018))))
    assert out["n_complete_consecutive_lagged_years"] == 22
    assert out["n_heldout_forecasts"] == 15
    assert len(out["heldout_years"]) == 15
    assert out["direct_love_otto_cv_test"] is False
    assert "M0" in out and "M1" in out
    assert "r_next" not in out
    assert out["outcome_rows_or_predictions_redistributed"] is False


def test_missing_recruitment_invalidates_target_and_next_year_lag() -> None:
    cases, counts = load_complete_lagged_cases(
        _source(list(range(2000, 2012)), missing_year=2004)
    )
    assert 2004 not in counts["eligible_years"]
    assert 2005 not in counts["eligible_years"]
    assert 2006 in counts["eligible_years"]
