"""Prospectively locked cross-closure sorting/repair falsification experiment.

This is an independent two-closure analogue, not a direct replay of the pinned
EGC finite life cycle or a substitute for natural field validation.
The only admissible conditions are the JSON protocol frozen at efc3baa...
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import exp, isclose, sqrt
from pathlib import Path
from random import Random
from statistics import fmean, stdev
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = ROOT / "experiments" / "cross_closure_sorting_repair_v1_protocol.json"
FROZEN_PROTOCOL_COMMIT = "efc3baa6868e705974235b35df70d1c3fee5b7a9"
FROZEN_PROTOCOL_FILE = "experiments/cross_closure_sorting_repair_v1_protocol.json"
T_CRIT_95_5DF = 2.570581835636305
CLOSURES = ("aggregate_support_analogue", "partner_encounter_and_mating_limited")
ARRANGEMENTS = ("AA", "RR")
SELECTION = (0.0, 1.0)
INHERITANCE = (0.25, 0.75)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_protocol(*, check_git_lock: bool = True) -> dict:
    raw = PROTOCOL_PATH.read_bytes()
    p = json.loads(raw)
    if p.get("status") != "prospective_locked_before_outcomes":
        raise ValueError("Prospective protocol status is not locked")
    if p.get("experiment_id") != "cross_closure_sorting_repair_v1":
        raise ValueError("Unknown experiment")
    factors = p["fixed_factorial"]
    if (tuple(factors["closures"]) != CLOSURES or
        tuple(factors["arrangements"]) != ARRANGEMENTS or
        tuple(factors["selection_strength"]) != SELECTION or
        tuple(factors["resident_inheritance_weight"]) != INHERITANCE):
        raise ValueError("Fixed factorial modified")
    rep = p["replication"]
    if (tuple(rep["master_seeds"]) !=
        (901171, 901187, 901199, 901213, 901229, 901237) or
        rep["replicates_per_master_seed"] != 160 or
        rep["total_trajectories"] != 7680):
        raise ValueError("Fixed replication modified")
    if p["shared_life_cycle"]["generations"] != 40:
        raise ValueError("Fixed horizon modified")
    if check_git_lock:
        # The protocol was committed separately before the trajectory code.
        # Byte-identical verification also detects unauthorized post-hoc edits.
        frozen = subprocess.check_output(
            ["git", "show", FROZEN_PROTOCOL_COMMIT + ":" + FROZEN_PROTOCOL_FILE],
            cwd=ROOT,
        )
        if _sha(frozen) != _sha(raw):
            raise RuntimeError("Protocol differs from the prospective freeze commit")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", FROZEN_PROTOCOL_COMMIT, "HEAD"],
            cwd=ROOT, check=False,
        )
        if ancestor.returncode != 0:
            raise RuntimeError("Protocol-only freeze commit not in checkout ancestry")
    return p


def logistic(x: float) -> float:
    if x >= 0:
        y = exp(-x)
        return 1.0 / (1.0 + y)
    y = exp(x)
    return y / (1.0 + y)


def binomial(rng: Random, n: int, probability: float) -> int:
    if n < 0 or not (0 <= probability <= 1):
        raise ValueError("Invalid binomial arguments")
    if probability == 0.0:
        return 0
    if probability == 1.0:
        return n
    return sum(rng.random() < probability for _ in range(n))


def allele_selected(p: float, q: float, strength: float) -> float:
    if not (0 <= p <= 1 and 0 <= q <= 1 and strength in SELECTION):
        raise ValueError("Invalid selection state")
    w = (0.75 + 0.4 * q) ** strength
    return p * w / (1.0 - p + p * w)


def recruit_mass(m: float, p_selected: float, h: float) -> float:
    return h * m + (1.0 - h) * p_selected


def first_state(p: dict, arrangement: str) -> tuple[list[int], list[float], list[float], list[float], list[float]]:
    base = p["fixed_initial_state"]
    pair = base["AA_trait_and_allele"] if arrangement == "AA" else base["RR_trait_and_allele"]
    return (
        list(base["population"]),
        list(base["interaction"]),
        list(pair),
        list(pair),
        list(base["partner_availability"]),
    )


def check_matched_initial_marginals(p: dict) -> None:
    a, b = first_state(p, "AA"), first_state(p, "RR")
    for k in range(5):
        if sorted(a[k]) != sorted(b[k]):
            raise RuntimeError(f"Unmatched starting marginal index {k}")
    if a[1] != b[1] or a[0] != b[0] or a[4] != b[4]:
        raise RuntimeError("Interaction, abundance or partner supply not synchronized")
    if len(a[0]) != 4:
        raise RuntimeError("Experiment requires four patches")


def seed(master: int, replicate: int) -> int:
    return (master * 1_000_003 + replicate * 101 + 97) % (2**31 - 1)


def simulate_one(p: dict, closure: str, arrangement: str,
                 s: float, h: float, master: int, replicate: int) -> dict:
    if closure not in CLOSURES or arrangement not in ARRANGEMENTS:
        raise ValueError("Unknown closure/arrangement")
    if s not in SELECTION or h not in INHERITANCE:
        raise ValueError("Condition not preregistered")
    rng = Random(seed(master, replicate))
    n, q, allele, trait, partner = first_state(p, arrangement)
    loss_t = None
    recovered = False
    snapshot = None
    for t in range(1, 41):
        theta = 0.50 + 0.15 * t / 60.0
        q_next = []
        partner_next = []
        for j in range(4):
            density = min(1.0, n[j] / 40.0)
            if closure == "aggregate_support_analogue":
                support = 0.6 * q[j] + 0.3 * trait[j] + 0.1 * allele[j]
                q_j = logistic(4.5 * (density * support - theta))
                v_j = partner[j]
            else:
                # Partner supply responds to local focal floral resources.
                v_j = 0.8 * partner[j] + 0.2 * (
                    n[j] * trait[j] / (n[j] * trait[j] + 8.0)
                )
                rate = 3.0 * exp(-theta) * v_j * (trait[j] + 0.1) * density
                visit_p = 1.0 - exp(-rate)
                q_j = binomial(rng, n[j], visit_p) / n[j]
            q_next.append(q_j)
            partner_next.append(v_j)
        selected = []
        next_n = []
        next_a = []
        next_m = []
        for j in range(4):
            psel = allele_selected(allele[j], q_next[j], s)
            selected.append(psel)
            r = recruit_mass(trait[j], psel, h)
            w_high = 0.5 + 0.8 * q_next[j]
            phen_prob = (r * w_high) / (1.0 - r + r * w_high)
            pop = n[j] * exp(0.8 + 0.4 * q_next[j] + 0.1 * psel - n[j] / 40.0)
            n_new = max(1, min(80, round(pop)))
            next_n.append(n_new)
            gene_copies = max(2, round(2 * n_new * (0.5 + 0.5 * q_next[j])))
            next_a.append(binomial(rng, gene_copies, psel) / gene_copies)
            next_m.append(binomial(rng, n_new, phen_prob) / n_new)
        n, q, allele, trait, partner = next_n, q_next, next_a, next_m, partner_next
        all_high_absent = all(m == 0.0 for m in trait)
        if all_high_absent and loss_t is None:
            loss_t = t
        if loss_t is not None and not all_high_absent:
            recovered = True
        if t == 10:
            # Higher joint reserve means lower event risk; negate for ROC.
            snapshot = {
                "reserve_risk": -max(q[j] * trait[j] * (0.2 + 0.8 * allele[j])
                                     for j in range(4)),
                "max_q_risk": -max(q),
                "mean_population": fmean(n),
            }
    direct = sum(n[j] * trait[j] * q[j] for j in range(4)) / sum(n)
    return {
        "closure": closure, "arrangement": arrangement, "s": s, "h": h,
        "master_seed": master, "replicate": replicate, "trajectory_seed": seed(master, replicate),
        "first_loss_t": loss_t, "loss_by_40": int(loss_t is not None),
        "recovered_after_first_loss": recovered,
        "final_high_trait_mass": fmean(trait), "modeled_opportunity_g40": direct,
        "snapshot_t10": snapshot,
    }


def auc_with_ties(risk_labels: list[tuple[float, int]]) -> float | None:
    """Exact rank-based ROC AUC; no sklearn and no fitted threshold."""
    pos = sum(y for _, y in risk_labels)
    neg = len(risk_labels) - pos
    if not pos or not neg:
        return None
    ordered = sorted(risk_labels)
    wins = 0.0
    negatives_before = 0
    i = 0
    while i < len(ordered):
        j = i + 1
        while j < len(ordered) and ordered[j][0] == ordered[i][0]:
            j += 1
        group_pos = sum(y for _, y in ordered[i:j])
        group_neg = j - i - group_pos
        wins += group_pos * (negatives_before + 0.5 * group_neg)
        negatives_before += group_neg
        i = j
    return wins / (pos * neg)


def ci_six_blocks(values: list[float]) -> dict:
    if len(values) != 6:
        raise RuntimeError("Six independent seed blocks required")
    mean = fmean(values)
    halfwidth = T_CRIT_95_5DF * stdev(values) / sqrt(6)
    return {"mean": mean, "ci95": [mean - halfwidth, mean + halfwidth],
            "block_values": values, "n_blocks": 6}


def analyze(p: dict, records: list[dict]) -> dict:
    by = defaultdict(list)
    by_block = defaultdict(list)
    for rec in records:
        key = (rec["closure"], rec["s"], rec["h"], rec["arrangement"])
        by[key].append(rec)
        by_block[(rec["closure"], rec["master_seed"], rec["s"], rec["h"], rec["arrangement"])].append(rec)

    strata = {}
    decision = {}
    for closure in CLOSURES:
        table = {}
        deltas = []
        for s in SELECTION:
            for h in INHERITANCE:
                cell_key = f"s={s:g},h={h:.2f}"
                cell = {}
                for a in ARRANGEMENTS:
                    rows = by[(closure, s, h, a)]
                    if len(rows) != 960:
                        raise RuntimeError(f"Missing records {closure} {cell_key} {a}: {len(rows)}")
                    cell[a] = {
                        "n": len(rows),
                        "loss_by_g40": sum(r["loss_by_40"] for r in rows),
                        "loss_rate": fmean(r["loss_by_40"] for r in rows),
                        "mean_opportunity_g40": fmean(r["modeled_opportunity_g40"] for r in rows),
                        "early_loss_by_g10": sum(r["first_loss_t"] is not None and r["first_loss_t"] <= 10 for r in rows),
                        "recovered_after_first_loss": sum(bool(r["recovered_after_first_loss"]) for r in rows),
                    }
                table[cell_key] = {
                    "arrangements": cell,
                    "RD_RR_minus_AA": cell["RR"]["loss_rate"] - cell["AA"]["loss_rate"],
                }
        # Infer on independent master blocks, not on thousands of correlated
        # trajectory rows: each block supplies one prespecified factorial DID.
        for master in p["replication"]["master_seeds"]:
            def rd(s: float, h: float) -> float:
                rr = by_block[(closure, master, s, h, "RR")]
                aa = by_block[(closure, master, s, h, "AA")]
                if len(rr) != 160 or len(aa) != 160:
                    raise RuntimeError("Unbalanced seed-block cells")
                return fmean(r["loss_by_40"] for r in rr) - fmean(r["loss_by_40"] for r in aa)

            d = (rd(1.0, 0.75) - rd(0.0, 0.75)) - (
                rd(1.0, 0.25) - rd(0.0, 0.25)
            )
            deltas.append(d)
        infer = ci_six_blocks(deltas)
        if infer["ci95"][0] > 0.0 and infer["mean"] > 0.02:
            verdict = "passes_declared_positive_sign_and_2pp_gate"
        elif infer["ci95"][1] < 0.0:
            verdict = "sign_reversal"
        elif infer["ci95"][0] > 0.0 and infer["mean"] <= 0.02:
            verdict = "positive_below_minimum_effect"
        else:
            verdict = "unresolved_or_infeasible"
        strata[closure] = {"factorial": table, "repair_modification_D": infer,
                           "closure_specific_decision": verdict}
        decision[closure] = verdict

    # Secondary: zero-calibration ROC comparison at t10, restricted to risk
    # sets not already experiencing the declared first-passage loss.
    secondary = {}
    for closure in CLOSURES:
        for s in SELECTION:
            for h in INHERITANCE:
                key = f"{closure}:s={s:g}:h={h:.2f}"
                block_auc = []
                for master in p["replication"]["master_seeds"]:
                    rows = [
                        r for a in ARRANGEMENTS
                        for r in by_block[(closure, master, s, h, a)]
                        if r["first_loss_t"] is None or r["first_loss_t"] > 10
                    ]
                    labels = [r["loss_by_40"] for r in rows]
                    res = auc_with_ties([(r["snapshot_t10"]["reserve_risk"], lab)
                                         for r, lab in zip(rows, labels)])
                    comp = auc_with_ties([(r["snapshot_t10"]["max_q_risk"], lab)
                                          for r, lab in zip(rows, labels)])
                    block_auc.append({
                        "master_seed": master, "n_at_risk": len(rows),
                        "n_future_loss": sum(labels),
                        "joint_state_auc": res, "max_q_auc": comp,
                        "paired_delta_auc": None if res is None or comp is None else res - comp,
                    })
                evaluable = [v["paired_delta_auc"] for v in block_auc
                             if v["paired_delta_auc"] is not None]
                secondary[key] = {
                    "block_auc": block_auc, "n_evaluable_blocks": len(evaluable),
                    "delta_auc_report": ci_six_blocks(evaluable)
                    if len(evaluable) == 6 else "not_estimable_no_substitution",
                }
    if all(x == "passes_declared_positive_sign_and_2pp_gate" for x in decision.values()):
        overall = "cross_closure_direction_supported_in_two_declared_models_only"
    else:
        overall = "cross_closure_direction_not_established_no_retuning"
    return {
        "experiment_id": p["experiment_id"],
        "status": "complete_from_immutable_protocol",
        "protocol_freeze_commit": FROZEN_PROTOCOL_COMMIT,
        "n_records": len(records),
        "primary": strata,
        "primary_decision": overall,
        "secondary_exploratory_t10": secondary,
        "nonclaims": [
            "Neither closure exactly replays the pinned EGC finite life cycle",
            "The visit encounter rate is a synthetic partner-state representation, not measured pollinator richness",
            "No field validation, no universal threshold, no new genetic early-warning accuracy claim",
            "An unusable event incidence is an actual feasibility boundary; do not rerun new conditions",
        ],
    }


def run() -> tuple[dict, list[dict]]:
    p = load_protocol(check_git_lock=True)
    check_matched_initial_marginals(p)
    records = []
    for closure in CLOSURES:
        for master in p["replication"]["master_seeds"]:
            for rep in range(p["replication"]["replicates_per_master_seed"]):
                for s in SELECTION:
                    for h in INHERITANCE:
                        for arrangement in ARRANGEMENTS:
                            records.append(simulate_one(p, closure, arrangement, s, h, master, rep))
    # Arithmetic erratum fixed before any outcome summary was inspected:
    # 2 closures * 2 arrangements * 2 s * 2 h * 6 seed blocks * 160 replicates
    # = 15360. The immutable JSON's 7680 count was a mistaken product.
    if p["replication"]["total_trajectories"] != 7680:
        raise AssertionError("Original protocol count was silently edited")
    expected = (
        len(CLOSURES) * len(ARRANGEMENTS) * len(SELECTION) *
        len(INHERITANCE) * len(p["replication"]["master_seeds"]) *
        p["replication"]["replicates_per_master_seed"]
    )
    if expected != 15360 or len(records) != expected:
        raise AssertionError("Actual factorial count differs from 15,360-slot erratum")
    summary = analyze(p, records)
    summary["arithmetic_erratum"] = {
        "original_protocol_count_typo": 7680,
        "correct_factorial_count": expected,
        "basis": "2 closures x 2 arrangements x 2 sorting x 2 repair x 6 seed blocks x 160 reps",
        "erratum_path": "docs/CROSS_CLOSURE_SORTING_REPAIR_V1_ARITHMETIC_ERRATUM.md",
        "outcome_conditioned_changes": False,
    }
    return summary, records, records
