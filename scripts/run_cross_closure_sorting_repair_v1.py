#!/usr/bin/env python3
"""Run once: locked two-closure prospective experiment and preserve full records."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from eco_genetic_warning_extensions.cross_closure_sorting_repair import (
    FROZEN_PROTOCOL_COMMIT, PROTOCOL_PATH, run,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary, records = run()
    root = args.output
    root.mkdir(parents=True, exist_ok=True)
    summary_path = root / "locked_result.json"
    rows_path = root / "all_trajectories.csv"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
    with rows_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "closure", "arrangement", "s", "h", "master_seed", "replicate", "trajectory_seed",
            "first_loss_t", "loss_by_40", "recovered_after_first_loss",
            "final_high_trait_mass", "modeled_opportunity_g40",
            "t10_reserve_risk", "t10_max_q_risk", "t10_mean_population",
        ])
        writer.writeheader()
        for record in records:
            r = dict(record)
            snap = r.pop("snapshot_t10")
            r.update({f"t10_{k}": v for k, v in snap.items()})
            writer.writerow(r)
    (root / "protocol_frozen_copy.json").write_bytes(PROTOCOL_PATH.read_bytes())
    manifest = {
        "experiment_id": summary["experiment_id"],
        "source_type": "new prospective model analogue, not parent EGC main outcomes",
        "frozen_commit": FROZEN_PROTOCOL_COMMIT,
        "files_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (summary_path, rows_path, root / "protocol_frozen_copy.json")},
    }
    (root / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n",
                                        encoding="utf-8")
    print(json.dumps({
        "experiment_id": summary["experiment_id"],
        "trajectories": summary["n_records"],
        "decision": summary["primary_decision"],
        "closure_primary": {
            k: {
                "decision": v["closure_specific_decision"],
                "D": v["repair_modification_D"]["mean"],
                "CI95": v["repair_modification_D"]["ci95"],
            } for k, v in summary["primary"].items()
        },
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
