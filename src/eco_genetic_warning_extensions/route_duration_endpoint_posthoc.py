from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import fmean, stdev
from typing import Any

ANALYSIS_ID = "route_duration_endpoint_sign_reversal_posthoc_v1"
ANALYSIS_STATUS = "post_hoc_descriptive_not_preregistered"
SOURCE_WORKFLOW_RUN = 34127034037
SOURCE_ARTIFACT_ID = 10021317930
SOURCE_ARTIFACT_DIGEST = "sha256:1e5ecb658a66e78ffa0ea7eb0cf073323a2173eca7c55461a11aa91b8bd4eb69"
_T95_DF5 = 2.570581835636305


def _block_summary(values: list[float]) -> dict[str, Any]:
    if len(values) != 6:
        raise RuntimeError("locked route-duration experiment must contain exactly six master-seed blocks")
    mean = float(fmean(values))
    se = float(stdev(values) / math.sqrt(len(values)))
    return {
        "mean": mean,
        "ci95": [mean - _T95_DF5 * se, mean + _T95_DF5 * se],
        "n_seed_blocks": 6,
        "all_positive": all(x > 0 for x in values),
        "all_negative": all(x < 0 for x in values),
        "seed_block_values": [float(x) for x in values],
    }


def summarise(records: list[dict[str, Any]]) -> dict[str, Any]:
    if len(records) != 12_000:
        raise RuntimeError("locked route-duration artifact must contain exactly 12,000 trajectories")

    expected_conditions = {"AA_full", "AA_q_only", "RR_full", "RR_q_only"}
    if {str(r["condition"]) for r in records} != expected_conditions:
        raise RuntimeError("unexpected condition set")

    seeds = sorted({int(r["master_seed"]) for r in records})
    if len(seeds) != 6:
        raise RuntimeError("locked route-duration experiment must contain six master seeds")

    by_key: dict[tuple[int, int, int], dict[str, dict[str, Any]]] = {}
    for record in records:
        key = (
            int(record["master_seed"]),
            int(record["replicate"]),
            int(record["trajectory_seed"]),
        )
        condition = str(record["condition"])
        cell = by_key.setdefault(key, {})
        if condition in cell:
            raise RuntimeError(f"duplicate condition within paired key: {key} {condition}")
        cell[condition] = record

    if len(by_key) != 3000:
        raise RuntimeError("locked route-duration artifact must contain exactly 3,000 paired keys")
    if any(set(cell) != expected_conditions for cell in by_key.values()):
        raise RuntimeError("incomplete four-condition paired key")

    per_state: dict[str, Any] = {}
    endpoint_benefit_by_state_seed: dict[str, dict[int, float]] = {}

    for state in ("AA", "RR"):
        endpoint_benefit_blocks: list[float] = []
        duration_delta_blocks: list[float] = []
        rescue_total = 0
        harm_total = 0
        rescue_shorter_total = 0
        rescue_same_total = 0
        rescue_longer_total = 0
        seed_rows: list[dict[str, Any]] = []

        full_losses: list[int] = []
        qonly_losses: list[int] = []
        endpoint_benefit_by_state_seed[state] = {}

        for seed in seeds:
            cells = [
                cell
                for (master_seed, _replicate, _trajectory_seed), cell in by_key.items()
                if master_seed == seed
            ]
            if len(cells) != 500:
                raise RuntimeError(f"master seed {seed} must contain exactly 500 paired keys")

            endpoint_diffs: list[float] = []
            duration_diffs: list[float] = []
            rescue = 0
            harm = 0
            rescue_shorter = 0
            rescue_same = 0
            rescue_longer = 0

            for cell in cells:
                full = cell[f"{state}_full"]
                qonly = cell[f"{state}_q_only"]

                full_loss = bool(full["loss_by_endpoint"])
                qonly_loss = bool(qonly["loss_by_endpoint"])
                full_losses.append(int(full_loss))
                qonly_losses.append(int(qonly_loss))

                endpoint_diff = float(int(qonly_loss) - int(full_loss))
                duration_diff = float(
                    full["positive_margin_refuge_generations"]
                    - qonly["positive_margin_refuge_generations"]
                )
                endpoint_diffs.append(endpoint_diff)
                duration_diffs.append(duration_diff)

                is_rescue = qonly_loss and not full_loss
                is_harm = full_loss and not qonly_loss
                rescue += int(is_rescue)
                harm += int(is_harm)

                if is_rescue:
                    if duration_diff < 0:
                        rescue_shorter += 1
                    elif duration_diff == 0:
                        rescue_same += 1
                    else:
                        rescue_longer += 1

            benefit = float(fmean(endpoint_diffs))
            duration = float(fmean(duration_diffs))
            endpoint_benefit_blocks.append(benefit)
            duration_delta_blocks.append(duration)
            endpoint_benefit_by_state_seed[state][seed] = benefit

            rescue_total += rescue
            harm_total += harm
            rescue_shorter_total += rescue_shorter
            rescue_same_total += rescue_same
            rescue_longer_total += rescue_longer

            seed_rows.append(
                {
                    "master_seed": seed,
                    "endpoint_benefit_qonly_minus_full": benefit,
                    "duration_delta_full_minus_qonly": duration,
                    "rescue_count": rescue,
                    "harm_count": harm,
                    "rescues_with_shorter_duration": rescue_shorter,
                    "rescues_with_same_duration": rescue_same,
                    "rescues_with_longer_duration": rescue_longer,
                }
            )

        per_state[state] = {
            "full_feedback_loss_rate": float(fmean(full_losses)),
            "q_only_loss_rate": float(fmean(qonly_losses)),
            "endpoint_benefit_qonly_minus_full": _block_summary(endpoint_benefit_blocks),
            "positive_margin_duration_full_minus_qonly": _block_summary(duration_delta_blocks),
            "paired_outcome_switch_counts": {
                "rescue_qonly_loss_full_survive": rescue_total,
                "harm_full_loss_qonly_survive": harm_total,
            },
            "rescue_duration_relation": {
                "shorter": rescue_shorter_total,
                "same": rescue_same_total,
                "longer": rescue_longer_total,
            },
            "seed_blocks": seed_rows,
        }

    did_blocks = [
        endpoint_benefit_by_state_seed["RR"][seed]
        - endpoint_benefit_by_state_seed["AA"][seed]
        for seed in seeds
    ]

    same_ensemble_sign_reversal = all(
        per_state[state]["endpoint_benefit_qonly_minus_full"]["all_positive"]
        and per_state[state]["positive_margin_duration_full_minus_qonly"]["all_negative"]
        for state in ("AA", "RR")
    )

    return {
        "analysis_id": ANALYSIS_ID,
        "analysis_status": ANALYSIS_STATUS,
        "source": {
            "workflow_run": SOURCE_WORKFLOW_RUN,
            "artifact_id": SOURCE_ARTIFACT_ID,
            "artifact_digest": SOURCE_ARTIFACT_DIGEST,
            "prospective_primary_estimand": "full_minus_qonly positive-margin refuge duration",
            "posthoc_estimand": "q-only minus full-feedback generation-40 realised functional-loss rate",
        },
        "n_trajectories": len(records),
        "n_paired_keys": len(by_key),
        "n_seed_blocks": len(seeds),
        "states": per_state,
        "RR_minus_AA_endpoint_benefit_DID": _block_summary(did_blocks),
        "same_ensemble_sign_reversal": same_ensemble_sign_reversal,
        "all_endpoint_rescues_lack_duration_extension": all(
            per_state[state]["rescue_duration_relation"]["longer"] == 0
            for state in ("AA", "RR")
        ),
        "interpretation": (
            "Post-hoc descriptive audit of the same prospectively locked raw records. "
            "Full feedback reduced generation-40 loss in both AA and RR while the preregistered "
            "positive-margin refuge-duration effect was negative in both states. "
            "This demonstrates estimand decoupling within one fresh ensemble; it does not convert "
            "the endpoint comparison into a preregistered confirmatory test."
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
