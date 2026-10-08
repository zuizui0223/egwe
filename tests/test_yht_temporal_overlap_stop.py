from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_yht_temporal_overlap_stop_is_fail_closed() -> None:
    stop = json.loads((ROOT / "artifacts/yht_spatial_warning/temporal_overlap_stop.json").read_text())
    protocol = json.loads((ROOT / "experiments/yht_spatial_warning_protocol.json").read_text())
    assert stop["maximum_nominal_n"] == 8
    assert stop["minimum_required_n"] == 11
    assert stop["stop_triggered"] is True
    assert stop["outcome_values_parsed_for_decision"] == 0
    assert protocol["status"] == "stopped_before_outcome_fit_insufficient_temporal_overlap"
    assert protocol["stop_result"]["outcome_rows_parsed"] == 0
