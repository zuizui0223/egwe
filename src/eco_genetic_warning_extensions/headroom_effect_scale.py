from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import fmean, stdev
from typing import Any, Iterable

ANALYSIS_ID = "headroom_effect_scale_posthoc_v1"
ANALYSIS_STATUS = "post_hoc_descriptive_scale_audit"


def _sample_sd(values: Iterable[float]) -> float:
    values = [float(x) for x in values]
    if len(values) < 2:
        raise ValueError("sample SD requires at least two values")
    return float(stdev(values))


def _g20_value(record: dict[str, Any], metric: str) -> float:
    return float(record["states"]["20"][metric])


def summarise(records: list[dict[str, Any]]) -> dict[str, Any]:
    if len(records) != 24_000:
        raise RuntimeError("locked headroom artifact must contain exactly 24,000 trajectories")

    expected_interventions = {
        "baseline_local_allele_selection",
        "delete_local_allele_selection",
    }
    expected_assignments = {"AA", "RR"}
    if {str(r["intervention"]) for r in records} != expected_interventions:
        raise RuntimeError("unexpected intervention set")
    if {str(r["condition"]) for r in records} != expected_assignments:
        raise RuntimeError("unexpected assignment set")

    values = [_g20_value(r, "max_headroom") for r in records]
    raw_pooled_sd = _sample_sd(values)

    by_cell: dict[tuple[str, str], list[float]] = {}
    by_key: dict[tuple[int, int, str, str], float] = {}
    positive_counts: list[int] = []
    for r in records:
        intervention = str(r["intervention"])
        assignment = str(r["condition"])
        value = _g20_value(r, "max_headroom")
        by_cell.setdefault((intervention, assignment), []).append(value)
        key = (
            int(r["master_seed"]),
            int(r["replicate"]),
            intervention,
            assignment,
        )
        if key in by_key:
            raise RuntimeError(f"duplicate paired key: {key}")
        by_key[key] = value
        positive_counts.append(int(_g20_value(r, "positive_headroom_count")))

    if set(by_cell) != {
        ("baseline_local_allele_selection", "AA"),
        ("baseline_local_allele_selection", "RR"),
        ("delete_local_allele_selection", "AA"),
        ("delete_local_allele_selection", "RR"),
    }:
        raise RuntimeError("incomplete locked cell set")
    if any(len(v) != 6000 for v in by_cell.values()):
        raise RuntimeError("each locked headroom cell must contain 6,000 trajectories")

    within_num = sum((len(v) - 1) * (_sample_sd(v) ** 2) for v in by_cell.values())
    within_den = sum(len(v) - 1 for v in by_cell.values())
    pooled_within_cell_sd = math.sqrt(within_num / within_den)

    paired_dids: list[float] = []
    for master_seed in sorted({int(r["master_seed"]) for r in records}):
        reps = sorted(
            {
                int(r["replicate"])
                for r in records
                if int(r["master_seed"]) == master_seed
            }
        )
        for replicate in reps:
            baseline = (
                by_key[(master_seed, replicate, "baseline_local_allele_selection", "AA")]
                - by_key[(master_seed, replicate, "baseline_local_allele_selection", "RR")]
            )
            deletion = (
                by_key[(master_seed, replicate, "delete_local_allele_selection", "AA")]
                - by_key[(master_seed, replicate, "delete_local_allele_selection", "RR")]
            )
            paired_dids.append(baseline - deletion)

    if len(paired_dids) != 6000:
        raise RuntimeError("expected exactly 6,000 paired DID keys")

    did = float(fmean(paired_dids))
    paired_sd = _sample_sd(paired_dids)
    return {
        "analysis_id": ANALYSIS_ID,
        "analysis_status": ANALYSIS_STATUS,
        "n_trajectories": len(records),
        "n_paired_keys": len(paired_dids),
        "generation": 20,
        "max_headroom_DID": did,
        "raw_pooled_max_headroom_sd": raw_pooled_sd,
        "pooled_within_cell_max_headroom_sd": pooled_within_cell_sd,
        "DID_over_raw_pooled_sd": did / raw_pooled_sd,
        "DID_over_pooled_within_cell_sd": did / pooled_within_cell_sd,
        "paired_DID_sd": paired_sd,
        "paired_standardized_effect": did / paired_sd,
        "all_positive_headroom_counts_zero": all(x == 0 for x in positive_counts),
        "positive_headroom_nonzero_trajectories": sum(x != 0 for x in positive_counts),
        "cell_summaries": {
            f"{intervention}:{assignment}": {
                "n": len(cell),
                "mean": float(fmean(cell)),
                "sd": _sample_sd(cell),
                "min": float(min(cell)),
                "max": float(max(cell)),
            }
            for (intervention, assignment), cell in sorted(by_cell.items())
        },
        "interpretation": (
            "Descriptive post-hoc scaling of a prospectively locked DID. "
            "It does not change the preregistered estimand or its inferential status."
        ),
    }


def run(records_path: str | Path) -> dict[str, Any]:
    records = json.loads(Path(records_path).read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise TypeError("records JSON must be a list")
    return summarise(records)


def write(records_path: str | Path, output_path: str | Path) -> None:
    summary = run(records_path)
    dest = Path(output_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
