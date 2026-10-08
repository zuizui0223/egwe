from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "artifacts/mac_hugh_recruitment/temporal_result_locked.json"
CURRENT = ROOT / "artifacts/mac_hugh_recruitment/temporal_result.json"

KEYS = (
    "analysis_contract",
    "analysis_contract_frozen_before_outcomes",
    "source_doi",
    "source_md5",
    "source_file_id",
    "n_source_raw_rows",
    "n_unique_source_years",
    "n_complete_consecutive_lagged_years",
    "n_heldout_forecasts",
    "heldout_years",
    "eligible_years",
    "no_missing_year_imputation",
    "status",
    "direct_love_otto_cv_test",
    "outcome_rows_or_predictions_redistributed",
)


def verify() -> None:
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))["scientific_result"]
    actual = json.loads(CURRENT.read_text(encoding="utf-8"))
    for key in KEYS:
        if actual.get(key) != expected.get(key):
            raise AssertionError(f"official source rerun changed locked {key}: {actual.get(key)!r}")
    for model in ("M0", "M1"):
        for metric in ("RMSE", "MAE"):
            if not math.isclose(
                float(actual[model][metric]), float(expected[model][metric]),
                rel_tol=0,
                abs_tol=1e-10,
            ):
                raise AssertionError(f"official source rerun changed {model}.{metric}")
    key = "mean_paired_squared_error_difference_M0_minus_M1"
    if not math.isclose(float(actual[key]), float(expected[key]), rel_tol=0, abs_tol=1e-10):
        raise AssertionError(f"official source rerun changed {key}")
    if not actual["M1"]["RMSE"] > actual["M0"]["RMSE"]:
        raise AssertionError("M1 unexpectedly improves RMSE")
    if not actual["M1"]["MAE"] > actual["M0"]["MAE"]:
        raise AssertionError("M1 unexpectedly improves MAE")
    print("MAC_HUGH_OFFICIAL_TEMPORAL_REPRODUCIBILITY: PASS")


if __name__ == "__main__":
    verify()
