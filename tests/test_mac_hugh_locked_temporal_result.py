from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "artifacts/mac_hugh_recruitment/temporal_result_locked.json"
CONTRACT = ROOT / "experiments/mac_hugh_recruitment_temporal_protocol.json"


def test_temporal_result_is_locked_to_published_source_and_before_outcome_contract() -> None:
    stored = json.loads(SUMMARY.read_text(encoding="utf-8"))
    result = stored["scientific_result"]
    provenance = stored["provenance"]
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert result["experiment_id"] == contract["experiment_id"]
    assert contract["status"] == "frozen_after_published_conclusion_and_schema_exposure_before_outcome_row_fit"
    assert result["analysis_contract_frozen_before_outcomes"] is True
    assert provenance["frozen_protocol_commit"] == "66ea48a7844135e0305129b25a4535ab8b2e6e57"
    assert provenance["workflow_run"] == 37725277766
    assert provenance["source_workflow_artifact_id"] == 11527433443
    assert provenance["artifact_digest"] == (
        "sha256:00431c80be5c733160d56bc1a02856bc35148c5e3ce7a26536d92f60bfba3210"
    )
    assert result["source_doi"] == "10.5683/SP3/0ROESU"
    assert result["source_file_id"] == 984869
    assert result["source_md5"] == "3ac1d2d5c7f64b182567829c0f2e28ac"


def test_result_records_negative_incremental_prediction_without_cv_extrapolation() -> None:
    stored = json.loads(SUMMARY.read_text(encoding="utf-8"))
    d = stored["scientific_result"]
    assert d["status"] == "no_incremental_temporal_forecast_gain_detected"
    assert d["n_source_raw_rows"] == 26
    assert d["n_complete_consecutive_lagged_years"] == 23
    assert d["n_heldout_forecasts"] == 16
    assert d["heldout_years"] == list(range(2004, 2020))
    assert d["no_missing_year_imputation"] is True
    assert d["outcome_rows_or_predictions_redistributed"] is False
    assert d["direct_love_otto_cv_test"] is False
    assert d["M1"]["RMSE"] > d["M0"]["RMSE"]
    assert d["M1"]["MAE"] > d["M0"]["MAE"]
    assert math.isclose(d["M0"]["RMSE"], 13.308863419134783, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(d["M1"]["RMSE"], 13.814877313250095, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(d["M0"]["MAE"], 11.464726764922005, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(d["M1"]["MAE"], 11.514393286547115, rel_tol=0, abs_tol=1e-12)
    assert d["mean_paired_squared_error_difference_M0_minus_M1"] < 0
