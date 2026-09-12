from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUM0 = [
    "present_t", "r_local_t", "nplant_t", "sample_rounds_t",
    "occ_t", "mean_support_t", "pooled_partner_t",
]
NUM1 = NUM0 + ["rmax_t"]
CAT = ["transition"]
BOOT_SEED = 20260912
BOOT_N = 10000
EPS = 1e-12


def build_rows(edges: pd.DataFrame, meta: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    meta = meta.copy()
    meta["year"] = meta["year"].astype(int)
    edges = edges.copy()
    edges["year"] = edges["year"].astype(int)

    net_keys = {(r.site, int(r.year)) for r in meta.itertuples(index=False)}
    transitions = sorted(
        (site, year, year + 1)
        for site, year in net_keys
        if year != 2010 and (year + 1) != 2010 and (site, year + 1) in net_keys
    )
    trans_df = pd.DataFrame(transitions, columns=["site", "year", "future_year"])

    # Positive edge lookup and site-year plant richness are source-defined.
    by_sy = {(r.site, int(r.year)): r for r in meta.itertuples(index=False)}
    sy_pollinators: dict[tuple[str, int], set[str]] = {}
    sy_degree: dict[tuple[str, int, str], int] = {}
    sy_partners: dict[tuple[str, int, str], set[str]] = {}
    year_species: dict[int, set[str]] = {}
    year_sites: dict[int, list[str]] = {}
    year_all_plants: dict[int, set[str]] = {}

    for (site, year), g in edges.groupby(["site", "year"], sort=False):
        year = int(year)
        ps = set(g["pollinator"].astype(str))
        sy_pollinators[(site, year)] = ps
        year_species.setdefault(year, set()).update(ps)
        year_all_plants.setdefault(year, set()).update(g["plant"].astype(str))
        for pol, gp in g.groupby("pollinator", sort=False):
            partners = set(gp["plant"].astype(str))
            sy_partners[(site, year, str(pol))] = partners
            sy_degree[(site, year, str(pol))] = len(partners)

    for year, g in meta.groupby("year", sort=False):
        if int(year) == 2010:
            continue
        year_sites[int(year)] = list(g["site"].astype(str))

    # Marginals use all networks available in year t, assigning zeros when species absent.
    marg: dict[tuple[str, int], dict[str, float]] = {}
    for year, species_set in year_species.items():
        if year == 2010 or year not in year_sites:
            continue
        sites = year_sites[year]
        all_plants = year_all_plants.get(year, set())
        denom_plants = len(all_plants)
        for sp in species_set:
            supports = []
            present = 0
            pooled: set[str] = set()
            for site in sites:
                m = by_sy[(site, year)]
                degree = sy_degree.get((site, year, sp), 0)
                if sp in sy_pollinators.get((site, year), set()):
                    present += 1
                supports.append(degree / float(m.nplant))
                pooled.update(sy_partners.get((site, year, sp), set()))
            marg[(sp, year)] = {
                "occ_t": present / len(sites),
                "mean_support_t": float(np.mean(supports)),
                "pooled_partner_t": (len(pooled) / denom_plants) if denom_plants else np.nan,
                "rmax_t": float(np.max(supports)),
            }

    rows = []
    excluded_effort = 0
    for site, year, future_year in transitions:
        m = by_sy[(site, year)]
        effort = float(m.sample_rounds) if pd.notna(m.sample_rounds) else np.nan
        if not np.isfinite(effort) or effort <= 0:
            excluded_effort += 1
            continue
        current_species = year_species.get(year, set())
        future_present = sy_pollinators.get((site, future_year), set())
        current_present = sy_pollinators.get((site, year), set())
        for sp in current_species:
            mm = marg[(sp, year)]
            degree = sy_degree.get((site, year, sp), 0)
            rows.append({
                "species": sp,
                "site": site,
                "year": year,
                "future_year": future_year,
                "transition": f"{year}_to_{future_year}",
                "present_t": int(sp in current_present),
                "r_local_t": degree / float(m.nplant),
                "nplant_t": int(m.nplant),
                "sample_rounds_t": effort,
                "occ_t": mm["occ_t"],
                "mean_support_t": mm["mean_support_t"],
                "pooled_partner_t": mm["pooled_partner_t"],
                "rmax_t": mm["rmax_t"],
                "y_future": int(sp in future_present),
            })

    df = pd.DataFrame(rows)
    info = {
        "n_networks": int(len(meta)),
        "n_sites": int(meta["site"].nunique()),
        "n_retained_transitions_before_effort": int(len(transitions)),
        "n_transition_siteyears_excluded_for_effort": int(excluded_effort),
        "n_prediction_rows": int(len(df)),
        "n_candidate_species": int(df["species"].nunique()) if len(df) else 0,
        "future_prevalence": float(df["y_future"].mean()) if len(df) else None,
    }
    return df, info


def make_model(numeric: list[str]) -> Pipeline:
    pre = ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(drop=None, handle_unknown="error"), CAT),
    ])
    clf = LogisticRegression(
        penalty="l2", C=1.0, solver="lbfgs", max_iter=10000,
        class_weight=None, random_state=None,
    )
    return Pipeline([("pre", pre), ("clf", clf)])


def mean_nll(y: np.ndarray, p: np.ndarray) -> float:
    p = np.clip(p, EPS, 1 - EPS)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def evaluate(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    per_species = []
    scored_rows = []
    omissions = []
    species_list = sorted(df["species"].unique())

    for sp in species_list:
        test = df[df["species"] == sp].copy()
        train = df[df["species"] != sp].copy()
        if train["y_future"].nunique() < 2:
            omissions.append({"species": sp, "reason": "training_response_one_class"})
            continue
        train_levels = set(train["transition"])
        if not set(test["transition"]).issubset(train_levels):
            omissions.append({"species": sp, "reason": "unseen_transition_level"})
            continue
        if train[NUM1].isna().any().any() or test[NUM1].isna().any().any():
            omissions.append({"species": sp, "reason": "nonfinite_or_missing_predictor"})
            continue

        ytr = train["y_future"].to_numpy(dtype=int)
        yte = test["y_future"].to_numpy(dtype=int)
        m0 = make_model(NUM0)
        m1 = make_model(NUM1)
        m0.fit(train[NUM0 + CAT], ytr)
        m1.fit(train[NUM1 + CAT], ytr)
        p0 = m0.predict_proba(test[NUM0 + CAT])[:, 1]
        p1 = m1.predict_proba(test[NUM1 + CAT])[:, 1]
        nll0 = mean_nll(yte, p0)
        nll1 = mean_nll(yte, p1)
        per_species.append({
            "species": sp, "n_rows": int(len(test)),
            "nll_m0": nll0, "nll_m1": nll1,
            "delta_refuge": nll1 - nll0,
        })
        sr = test[["species", "site", "year", "future_year", "transition", "present_t", "y_future"]].copy()
        sr["p_m0"] = p0
        sr["p_m1"] = p1
        scored_rows.append(sr)

    ps = pd.DataFrame(per_species)
    scored = pd.concat(scored_rows, ignore_index=True) if scored_rows else pd.DataFrame()
    if len(ps) == 0:
        result = {
            "decision": "primary_model_not_identifiable",
            "identifiable_species": 0,
            "omissions": omissions,
        }
        return ps, scored, result

    deltas = ps["delta_refuge"].to_numpy(float)
    obs = float(deltas.mean())
    rng = np.random.default_rng(BOOT_SEED)
    boot = np.empty(BOOT_N)
    for b in range(BOOT_N):
        boot[b] = rng.choice(deltas, size=len(deltas), replace=True).mean()
    lo, hi = np.percentile(boot, [2.5, 97.5])
    decision = (
        "strongest_local_refuge_adds_future_occupancy_information"
        if obs < 0 and hi < 0
        else "no_detected_incremental_strongest_refuge_information"
    )

    result = {
        "decision": decision,
        "identifiable_species": int(len(ps)),
        "equal_species_mean_nll_m0": float(ps["nll_m0"].mean()),
        "equal_species_mean_nll_m1": float(ps["nll_m1"].mean()),
        "equal_species_mean_delta_refuge": obs,
        "bootstrap_95pct": [float(lo), float(hi)],
        "bootstrap_seed": BOOT_SEED,
        "bootstrap_draws": BOOT_N,
        "omissions": omissions,
    }
    return ps, scored, result


def secondary(df: pd.DataFrame, scored: pd.DataFrame, ps: pd.DataFrame) -> dict:
    out: dict = {}
    if len(scored):
        for label, mask in {
            "persistence": scored["present_t"] == 1,
            "colonization": scored["present_t"] == 0,
        }.items():
            vals = []
            for sp, g in scored[mask].groupby("species"):
                if len(g):
                    vals.append(mean_nll(g["y_future"].to_numpy(int), g["p_m1"].to_numpy(float)) -
                                mean_nll(g["y_future"].to_numpy(int), g["p_m0"].to_numpy(float)))
            out[f"{label}_equal_species_mean_delta"] = float(np.mean(vals)) if vals else None

        trans = {}
        for tr, g in scored.groupby("transition"):
            vals = []
            for sp, gs in g.groupby("species"):
                vals.append(mean_nll(gs["y_future"].to_numpy(int), gs["p_m1"].to_numpy(float)) -
                            mean_nll(gs["y_future"].to_numpy(int), gs["p_m0"].to_numpy(float)))
            trans[str(tr)] = float(np.mean(vals)) if vals else None
        out["transition_equal_species_mean_delta"] = trans

        bins = np.linspace(0, 1, 11)
        cal = {}
        for model in ["m0", "m1"]:
            pcol = f"p_{model}"
            tmp = scored[[pcol, "y_future"]].copy()
            tmp["bin"] = pd.cut(tmp[pcol], bins=bins, include_lowest=True, duplicates="drop")
            groups = []
            for b, g in tmp.groupby("bin", observed=True):
                groups.append({"bin": str(b), "n": int(len(g)), "mean_pred": float(g[pcol].mean()), "obs_rate": float(g["y_future"].mean())})
            cal[model] = groups
        out["calibration_bins"] = cal

    corr_cols = ["occ_t", "mean_support_t", "pooled_partner_t", "rmax_t"]
    out["predictor_correlation"] = df[corr_cols].corr().round(12).to_dict()
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edges", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    edges = pd.read_csv(args.edges)
    meta = pd.read_csv(args.meta)
    df, build_info = build_rows(edges, meta)
    df.to_csv(outdir / "prediction_rows.csv", index=False)
    ps, scored, result = evaluate(df)
    ps.to_csv(outdir / "per_species_scores.csv", index=False)
    scored.to_csv(outdir / "scored_rows.csv", index=False)
    result["build"] = build_info
    result["secondary"] = secondary(df, scored, ps)
    result["contract"] = "NEE_Q2_NATURAL_STRONGEST_REFUGE_STAGE_B_CONTRACT.md"
    result["result_status"] = "locked_confirmatory_run_complete"
    (outdir / "confirmatory_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result.get(k) for k in ["decision", "identifiable_species", "equal_species_mean_delta_refuge", "bootstrap_95pct", "build"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
