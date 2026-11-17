#!/usr/bin/env python3
"""Post-outcome DESCRIPTIVE audit of original fixed cross-closure v1 artifact.

No new seeds, simulation, hypothesis test, AUC threshold or model selection.
Checks provenance and the full 15,360-record denominator before printing
condition-level descriptive rates and boundary/semantic diagnostics.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean


SOURCE_RUN = 44012157673
SOURCE_ARTIFACT = 14296518638
FREEZE_COMMIT = "efc3baa6868e705974235b35df70d1c3fee5b7a9"
CLOSURES = ("aggregate_support_analogue", "partner_encounter_and_mating_limited")
ARRANGEMENTS = ("AA", "RR")
STRENGTHS = (0.0, 1.0)
REPAIR = (0.25, 0.75)
MASTERS = (901171, 901187, 901199, 901213, 901229, 901237)
REPS = 160
EXPECTED_ROWS = 15360
ASSERT_TOL = 1e-12


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_manifest(root: Path) -> dict:
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    if manifest["experiment_id"] != "cross_closure_sorting_repair_v1":
        raise ValueError("Wrong experiment artifact")
    if manifest["frozen_commit"] != FREEZE_COMMIT:
        raise ValueError("Artifact did not pin original protocol-only commit")
    for name, digest in manifest["files_sha256"].items():
        if name not in ("locked_result.json", "all_trajectories.csv", "protocol_frozen_copy.json"):
            raise ValueError("Unexpected source manifest member")
        if sha256(root / name) != digest:
            raise ValueError("Source member hash mismatch: " + name)
    if set(manifest["files_sha256"]) != {
        "locked_result.json", "all_trajectories.csv", "protocol_frozen_copy.json"
    }:
        raise ValueError("Required source files missing from manifest")
    protocol = json.loads((root / "protocol_frozen_copy.json").read_text(encoding="utf-8"))
    if protocol["replication"]["master_seeds"] != list(MASTERS):
        raise ValueError("Original master-seed list changed")
    if protocol["replication"]["replicates_per_master_seed"] != REPS:
        raise ValueError("Original per-seed replication changed")
    if protocol["replication"]["total_trajectories"] != 7680:
        raise ValueError("Original protocol arithmetic typo was overwritten")
    return manifest


def load_and_validate(root: Path) -> tuple[dict, list[dict]]:
    validate_manifest(root)
    locked = json.loads((root / "locked_result.json").read_text(encoding="utf-8"))
    if locked["n_records"] != EXPECTED_ROWS:
        raise ValueError("Incorrect number of original trajectories")
    if locked["primary_decision"] != "cross_closure_direction_not_established_no_retuning":
        raise ValueError("Unexpected scientific decision in source result")
    with (root / "all_trajectories.csv").open(newline="", encoding="utf-8") as f:
        raw = list(csv.DictReader(f))
    if len(raw) != EXPECTED_ROWS:
        raise ValueError("Row denominator mismatch")
    seen = set()
    cells = Counter()
    records = []
    for row in raw:
        closure, arrangement = row["closure"], row["arrangement"]
        s, h = float(row["s"]), float(row["h"])
        master, rep = int(row["master_seed"]), int(row["replicate"])
        if not (closure in CLOSURES and arrangement in ARRANGEMENTS and
                s in STRENGTHS and h in REPAIR and master in MASTERS and 0 <= rep < REPS):
            raise ValueError("Unexpected factorial entry")
        key = (closure, arrangement, s, h, master, rep)
        if key in seen:
            raise ValueError("Duplicate complete trajectory key")
        seen.add(key)
        cells[key[:5]] += 1
        loss = int(row["loss_by_40"])
        t = None if row["first_loss_t"] in ("", "None") else int(row["first_loss_t"])
        recovered = row["recovered_after_first_loss"] == "True"
        if row["recovered_after_first_loss"] not in ("True", "False"):
            raise ValueError("Unparseable recovery status")
        if loss not in (0, 1) or loss != int(t is not None):
            raise ValueError("First-passage event indicator inconsistent with loss")
        if t is not None and not 1 <= t <= 40:
            raise ValueError("Unexpected first loss generation")
        if recovered and t is None:
            raise ValueError("Recovery without recorded first loss")
        opp = float(row["modeled_opportunity_g40"])
        mass = float(row["final_high_trait_mass"])
        if not (math.isfinite(opp) and math.isfinite(mass) and 0 <= opp <= 1 and 0 <= mass <= 1):
            raise ValueError("Functional readouts out of range")
        records.append({
            "closure": closure, "arrangement": arrangement,
            "s": s, "h": h, "master": master, "rep": rep,
            "loss": loss, "first_loss_t": t, "recovered": int(recovered),
            "opportunity": opp, "trait_mass": mass,
        })
    if (len(seen) != EXPECTED_ROWS or len(cells) != 96 or
        any(n != REPS for n in cells.values())):
        raise ValueError("Not a complete 2x2x2x2x6x160 roster")
    return locked, records


def summarize(locked: dict, records: list[dict]) -> dict:
    by = defaultdict(list)
    for r in records:
        by[(r["closure"], r["s"], r["h"], r["arrangement"])].append(r)
    report = {}
    for closure in CLOSURES:
        entries = []
        for s in STRENGTHS:
            for h in REPAIR:
                cs = {}
                for arrangement in ARRANGEMENTS:
                    rows = by[(closure, s, h, arrangement)]
                    if len(rows) != 960:
                        raise ValueError("Missing one condition")
                    cs[arrangement] = {
                        "n": len(rows),
                        "n_loss": sum(r["loss"] for r in rows),
                        "loss_rate": fmean(r["loss"] for r in rows),
                        "n_first_loss_by_g10": sum(r["first_loss_t"] is not None and r["first_loss_t"] <= 10 for r in rows),
                        "n_reappeared_after_first_loss": sum(r["recovered"] for r in rows),
                        "mean_modeled_opportunity_g40": fmean(r["opportunity"] for r in rows),
                        "mean_final_high_trait_mass": fmean(r["trait_mass"] for r in rows),
                    }
                    source_key = f"s={s:g},h={h:.2f}"
                    orig = locked["primary"][closure]["factorial"][source_key]["arrangements"][arrangement]
                    for field, original in (
                        ("loss_rate", orig["loss_rate"]),
                        ("mean_modeled_opportunity_g40", orig["mean_opportunity_g40"]),
                        ("n_first_loss_by_g10", orig["early_loss_by_g10"]),
                        ("n_reappeared_after_first_loss", orig["recovered_after_first_loss"]),
                    ):
                        if abs(cs[arrangement][field] - original) > ASSERT_TOL:
                            raise ValueError(f"Locked summary divergence {closure} {source_key} {arrangement}: {field}")
                rd = cs["RR"]["loss_rate"] - cs["AA"]["loss_rate"]
                original_rd = locked["primary"][closure]["factorial"][f"s={s:g},h={h:.2f}"]["RD_RR_minus_AA"]
                if abs(rd - original_rd) > ASSERT_TOL:
                    raise ValueError("Locked condition RD diverged")
                entries.append({"s": s, "h": h, "arrangements": cs, "RD_RR_minus_AA": rd})
        def get_rd(s, h):
            return next(x["RD_RR_minus_AA"] for x in entries if x["s"] == s and x["h"] == h)
        D = (get_rd(1, .75) - get_rd(0, .75)) - (get_rd(1, .25) - get_rd(0, .25))
        original_D = locked["primary"][closure]["repair_modification_D"]["mean"]
        if abs(D - original_D) > ASSERT_TOL:
            raise ValueError("Locked preregistered D diverged")
        report[closure] = {
            "cells": entries,
            "preregistered_D": D,
            "preregistered_CI95": locked["primary"][closure]["repair_modification_D"]["ci95"],
            "any_no_event_or_all_event_cell": [
                {"s": x["s"], "h": x["h"], "arrangement": a, "events": z["n_loss"]}
                for x in entries for a, z in x["arrangements"].items()
                if z["n_loss"] in (0, 960)
            ],
            "first_passage_can_reappear": sum(
                z["n_reappeared_after_first_loss"]
                for x in entries for z in x["arrangements"].values()
            ),
        }
    return {
        "schema": 1,
        "status": "post_outcome_descriptive_diagnostic_not_independent_confirmation",
        "source_run": SOURCE_RUN,
        "source_artifact_id": SOURCE_ARTIFACT,
        "n_trajectories": EXPECTED_ROWS,
        "original_primary_decision": locked["primary_decision"],
        "diagnostics": report,
        "method_boundary": [
            "No new master seeds, trial trajectories, model parameters, or statistical thresholds",
            "Exact original six-block primary interval and decision are reproduced, not replaced",
            "No causal mediation is identified from the different closure model laws",
            "A first-passage absence of realized focal trait may be followed by reappearance",
            "Synthetic encounter fraction and aggregate support q are not equivalent field measurements",
        ],
    }


def render_markdown(data: dict) -> str:
    lines = [
        "# Cross-closure v1: descriptive forensic diagnostic",
        "",
        "**POST-OUTCOME**, no new independent experiment and no new confirmatory test.",
        f"Source run: {SOURCE_RUN}; source artifact ID: {SOURCE_ARTIFACT}.",
        f"All {EXPECTED_ROWS:,} original trajectories passed provenance and source-summary checks.",
        "",
        "These are **first-passage realized focal-trait-absence risks**, not species extinction.",
        "",
        "| Closure | Selection s | Resident weight h | AA loss | RR loss | RR−AA (pp) | AA recovery after first absence | RR recovery |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for closure, block in data["diagnostics"].items():
        for cell in block["cells"]:
            aa, rr = cell["arrangements"]["AA"], cell["arrangements"]["RR"]
            lines.append(
                f"| {closure} | {cell['s']:g} | {cell['h']:.2f} | "
                f"{aa['n_loss']}/960 ({aa['loss_rate']*100:.1f}%) | "
                f"{rr['n_loss']}/960 ({rr['loss_rate']*100:.1f}%) | "
                f"{cell['RD_RR_minus_AA']*100:+.2f} | "
                f"{aa['n_reappeared_after_first_loss']} | "
                f"{rr['n_reappeared_after_first_loss']} |"
            )
    lines += [
        "",
        "## Declared primary outcome retained",
        "",
        f"**{data['original_primary_decision']}**. No selected cell, alternative endpoint, or sign flip replaces the registered primary DID.",
        "",
        "## Diagnostic limitations",
        "",
        "Only descriptive cell rates and fixed secondary modeled readouts are compared.",
        "Non-absorbing first-passage loss, closure-dependent meanings of q, and unequal direct feedback",
        "are **potential explanations**, not identified mediators or cross-system causal mechanisms.",
        "No original natural dataset or external pollinator effectiveness measurement was introduced.",
        "",
        "## Boundary for the next test",
        "",
        "Record visit frequency, *per-visit effective pollen deposition*, mate compatibility and",
        "same-cohort viable offspring separately. Conditioning on visit count alone is not assumed",
        "to close the effective mating state. That issue has prior empirical precedents and is",
        "not presented as a new discovery here.",
        "",
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    original, rows = load_and_validate(args.source)
    diagnostic = summarize(original, rows)
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    (out / "diagnostic.json").write_text(json.dumps(diagnostic, indent=2, sort_keys=True) + "\n")
    (out / "diagnostic.md").write_text(render_markdown(diagnostic), encoding="utf-8")
    print(render_markdown(diagnostic), flush=True)


if __name__ == "__main__":
    main()
