from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path


def t(x, y, s, size=15, anchor="middle", weight="normal", rotate=None):
    tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Arial,Helvetica,sans-serif" font-size="{size}" '
        f'font-weight="{weight}"{tr}>{html.escape(str(s))}</text>'
    )


def start(w, h, title, desc):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(title)}</title>',
        f'<desc id="desc">{html.escape(desc)}</desc>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" '
        'orient="auto"><path d="M0,0 L0,9 L9,4.5 z" fill="#222"/></marker></defs>',
    ]


def done(lines, path):
    lines.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def box(lines, x, y, w, h, label, sub=""):
    lines.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
        'fill="white" stroke="#222" stroke-width="2"/>'
    )
    lines.append(t(x + w / 2, y + 34, label, 16, weight="bold"))
    if sub:
        lines.append(t(x + w / 2, y + 61, sub, 12))


def fig1(path):
    L = start(
        1500, 780,
        "Sorting and buffering mechanism",
        "State separation, q-dependent allele sorting, buffering and warning discrimination.",
    )
    L.append(t(750, 45, "Fragmentation changes pathway balance, not one deterioration score", 28, weight="bold"))
    box(L, 65, 155, 340, 115, "State separation", "persistence != functional support")
    box(L, 490, 155, 520, 115, "Pathway mechanism", "sorting / recruitment buffering / direct recoupling")
    box(L, 1095, 155, 340, 115, "Warning discrimination", "early response != fate discrimination")
    L += [
        '<line x1="405" y1="212" x2="480" y2="212" stroke="#222" stroke-width="2" marker-end="url(#arrow)"/>',
        '<line x1="1010" y1="212" x2="1085" y2="212" stroke="#222" stroke-width="2" marker-end="url(#arrow)"/>',
        t(235, 335, "fixed-area fragmentation separates biological states", 13),
        t(750, 335, "exact allele sorting / recruitment buffering / feedback recoupling", 13),
        t(1265, 335, "full denominator exposes false-positive behaviour", 13),
    ]
    box(L, 400, 430, 700, 125, "Positive synthesis", "fate reflects sorting, buffering, recoupling and remaining refuge reserve")
    L += [
        t(750, 610, "density -> interaction feedback acts as a collapse/amplification gate", 15, weight="bold"),
        t(750, 665, "Natural systems enter only as ecological projections of limited buffering, recoupling or memory.", 13),
        t(750, 725, "No landscape label, alignment score or natural allele-sorting law is assumed universal.", 12),
    ]
    done(L, path)


def fig2(egc, path):
    rows = list(csv.DictReader(
        (egc / "artifacts/h3_fragmentation_gradient/h3_fragmentation_gradient_pooled_summary.csv").open()
    ))
    assert [int(r["patch_count"]) for r in rows] == [1, 2, 3, 4, 6, 8, 12, 16]
    assert int(rows[0]["projection_supported"]) == 1037

    L = start(
        1500, 800,
        "Fragmentation separates functional support from persistence",
        "Fixed-area fragmentation gradient with distinct biological-state responses.",
    )
    L += [
        t(750, 42, "Fragmentation separates functional support from persistence", 28, weight="bold"),
        t(350, 90, "A  Potential viability and realised occupancy", 18, weight="bold"),
        t(1110, 90, "B  Retained state ratios", 18, weight="bold"),
    ]

    left, right, top, bottom = 90, 670, 150, 610
    for p in [0, 25, 50, 75, 100]:
        y = bottom - p / 100 * (bottom - top)
        L.append(f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#ddd"/>')
        L.append(t(left - 8, y + 4, p, 11, anchor="end"))
    xs = [left + i * (right - left) / 7 for i in range(8)]
    pts = []
    for x, p, n in zip(xs, [100] + [0] * 7, [1, 2, 3, 4, 6, 8, 12, 16]):
        y = bottom - p / 100 * (bottom - top)
        pts.append((x, y))
        L.append(f'<circle cx="{x}" cy="{y}" r="5" fill="white" stroke="#111"/>')
        L.append(t(x, bottom + 23, n, 11))
    L.append(
        '<polyline points="' + " ".join(f"{x},{y}" for x, y in pts)
        + '" fill="none" stroke="#111" stroke-width="2.3"/>'
    )
    L += [
        t(380, 132, "realised occupancy at generation 30 ~99.6-100%", 12),
        t(30, 390, "supported outcomes (%)", 12, rotate=-90),
        t(380, 665, "number of isolated equal patches", 12),
        t(380, 710, "potential viability: 1,037/1,037 -> 0/1,037 after first split", 14, weight="bold"),
    ]

    l, r, tt, b = 820, 1430, 150, 610
    keys = [
        ("final_interaction_mean_ratio_to_n1_median", "interaction", ""),
        ("final_effective_size_mean_ratio_to_n1_median", "local effective size", "8 5"),
        ("realised_high_trait_mass_mean_ratio_to_n1_median", "realised high-trait mass", "3 4"),
    ]
    for q in [0, .25, .5, .75, 1]:
        y = b - q * (b - tt)
        L.append(f'<line x1="{l}" y1="{y}" x2="{r}" y2="{y}" stroke="#ddd"/>')
        L.append(t(l - 8, y + 4, f"{q:.2g}", 11, anchor="end"))
    x2 = [l + i * (r - l) / 7 for i in range(8)]
    for idx, (key, label, dash) in enumerate(keys):
        vals = [float(row[key]) for row in rows]
        pts = [(x, b - v * (b - tt)) for x, v in zip(x2, vals)]
        d = f' stroke-dasharray="{dash}"' if dash else ""
        L.append(
            '<polyline points="' + " ".join(f"{x},{y}" for x, y in pts)
            + f'" fill="none" stroke="#111" stroke-width="2.2"{d}/>'
        )
        ly = 655 + idx * 24
        L.append(f'<line x1="850" y1="{ly-4}" x2="890" y2="{ly-4}" stroke="#111" stroke-width="2.2"{d}/>')
        L.append(t(900, ly, label, 12, anchor="start"))
    for x, n in zip(x2, [1, 2, 3, 4, 6, 8, 12, 16]):
        L.append(t(x, b + 23, n, 11))
    L.append(t(1120, 745, "same structural fragmentation != one biological deterioration coordinate", 15, weight="bold"))
    done(L, path)


def fig3(egwe, flagship, path):
    phase = json.loads((egwe / "artifacts/cross_layer_alignment/phase_v_locked_summary.json").read_text())
    edge = json.loads((flagship / "artifacts/pathway_edge_decomposition/locked_result.json").read_text())
    focused = json.loads((flagship / "artifacts/allele_sorting_single_edge/locked_result.json").read_text())
    cert = phase["opening_certificate"]
    assert abs(cert["maximum_patchwise_generation1_difference"] - 0.25433292878878405) < 1e-12
    assert edge["edge_deletions"]["allele_linked_recruitment"]["decision"] == "resolved_countervailing_buffer"
    assert focused["primary_generation_40_DID"]["decision"] == "resolved_positive_sorting_contribution"
    assert focused["primary_generation_40_DID"]["n_paired_keys"] == 6000

    L = start(
        1500, 1020,
        "Relational state resolves into allele sorting and buffering",
        "Exact covariance mechanism, allele sorting theorem, pathway edge deletion, and focused 6000-pair proof.",
    )
    L.append(t(750, 42, "Relational state resolves into a causal sorting edge and buffering", 27, weight="bold"))

    L.append(t(250, 88, "A  Exact immediate mechanism", 17, weight="bold"))
    box(L, 55, 145, 180, 88, "AA support", ".47 .61 .75 .89")
    box(L, 275, 145, 180, 88, "RR support", ".71 .69 .67 .65")
    L += [
        t(255, 275, "mean support = 0.68 in both", 13, weight="bold"),
        t(255, 310, "Var(S): .0245 vs .0005 = 49 x", 15, weight="bold"),
        t(255, 350, "cross-layer covariance changes where support is concentrated", 12),
        t(255, 402, "max exact next-q difference = 0.2543", 16, weight="bold"),
    ]

    L.append(t(750, 88, "B  Exact q-dependent allele sorting", 17, weight="bold"))
    box(L, 520, 145, 460, 100, "Local allele operator", "logit(p+) - logit(p) = log(0.75 + 0.4q)")
    L += [
        t(750, 290, "d p+ / d q > 0 for every interior p", 14, weight="bold"),
        t(750, 330, "exact sorting switch q*=0.625", 16, weight="bold"),
        t(750, 365, "same threshold as declared high-trait viability", 12),
        t(750, 405, "Cov(q,logit p+) - Cov(q,logit p) > 0", 13, weight="bold"),
        t(750, 435, "whenever q varies among patches", 12),
    ]

    L.append(t(1235, 88, "C  Pathway context", 17, weight="bold"))
    box(L, 1035, 145, 400, 95, "Fresh q-only baseline", "RR-AA = +4.20 / +4.40 pp")
    L += [
        t(1235, 292, "delete allele recruitment", 12),
        t(1235, 320, "RR-AA = +13.20 / +12.73 pp", 13, weight="bold"),
        t(1235, 350, "DID = -9.00 / -8.33 pp -> buffering", 12),
        t(1235, 395, "delete local selection block", 12),
        t(1235, 423, "g40 DID +7.27 pp [+2.67,+11.87]", 13, weight="bold"),
        t(1235, 468, "delete density -> q: no losses by g20", 12, weight="bold"),
    ]

    L.append(t(750, 540, "D  Focused 6,000-pair single-edge proof", 18, weight="bold"))
    box(L, 120, 600, 360, 105, "Baseline local allele selection", "g40 RR-AA +6.65 pp  [+5.07,+8.23]")
    box(L, 570, 600, 360, 105, "Delete only q -> allele selection", "g40 RR-AA -0.23 pp  [-1.80,+1.34]")
    box(L, 1020, 600, 360, 105, "Predeclared causal DID", "+6.883 pp  [+5.800,+7.967]")
    L += [
        '<line x1="480" y1="652" x2="560" y2="652" stroke="#222" stroke-width="2" marker-end="url(#arrow)"/>',
        '<line x1="930" y1="652" x2="1010" y2="652" stroke="#222" stroke-width="2" marker-end="url(#arrow)"/>',
        t(750, 750, "single-edge endpoint contribution resolved", 16, weight="bold"),
        t(750, 790, "secondary g20 DID +6.783 pp  [+5.478,+8.088]", 13),
        t(350, 845, "g40 AA-RR allele variance: +0.01238 -> -0.00081", 12, weight="bold"),
        t(750, 845, "max high-trait mass: +0.06440 -> -0.00439", 12, weight="bold"),
        t(1150, 845, "refugia: +0.08033 -> +0.00133", 12, weight="bold"),
        t(750, 900, "q-dependent allele sorting is causal; recruitment buffers mismatch; density feedback gates collapse", 15, weight="bold"),
        t(750, 955, "All endpoint claims are bounded to the declared finite q-only closure.", 12),
    ]
    done(L, path)


def fig4(root, flagship, path):
    rows = list(csv.DictReader((root / "manuscript/tables/warning_validity_audit.csv").open()))
    by = {}
    for row in rows:
        by.setdefault(row["ensemble"], []).append(row)
    for ens, events, non_events in [("inherited_202611", 35, 48), ("fresh_202911", 33, 49)]:
        assert len(by[ens]) == 6
        assert all(
            int(r["events"]) == events
            and int(r["right_censored_non_events"]) == non_events
            and float(r["lead_sensitivity"]) == 1
            and float(r["full_horizon_specificity"]) == 0
            and float(r["full_horizon_binary_auc"]) == .5
            for r in by[ens]
        )

    route = json.loads((flagship / "artifacts/operator_balance_route_margin/locked_result.json").read_text())
    warning = json.loads((flagship / "artifacts/last_refuge_warning_holdout/locked_result.json").read_text())
    audit = route["exact_transition_audit"]
    marker = route["full_denominator_marker_generation_20_to_loss_generation_40"]["pooled_full"]
    auc = warning["continuous_last_refuge_route_margin"]
    maxq = warning["co_timed_max_q"]
    gain = warning["route_margin_minus_co_timed_max_q_auc"]
    timely = warning["timeliness"]
    assert audit["patch_generations_checked"] == 1_920_000 and audit["mismatches"] == 0
    assert marker["events"] == 3943 and marker["non_events"] == 2057
    assert marker["sensitivity"] == 1 and marker["specificity"] == 0 and marker["binary_auc"] == .5
    assert warning["decision"] == "confirmed_route_margin_adds_ranking_beyond_q"
    assert auc["ci95"][0] > .92 and gain["ci95"][0] > 0

    L = start(
        1500, 920,
        "Transition exactness, threshold saturation and continuous fate information",
        "Marginal diversity and a transition-exact binary route sign saturate, whereas continuous strongest-refuge reserve discriminates later functional fate.",
    )
    L.append(t(750, 42, "Early, exact and predictive are different properties", 27, weight="bold"))

    box(L, 55, 105, 675, 300, "A  Marginal erosion", "early stress signal; no fate discrimination")
    L += [
        t(392, 205, "Inherited: 35/35 losses preceded; 48/48 non-events also fired", 14, weight="bold"),
        t(392, 250, "Fresh: 33/33 losses preceded; 49/49 non-events also fired", 14, weight="bold"),
        t(392, 305, "sensitivity=1   specificity=0   AUC=0.5", 17, weight="bold"),
        t(392, 350, "being early is not the same as distinguishing fate", 13),
    ]

    box(L, 770, 105, 675, 300, "B  Exact route sign", "next-transition exact; binary horizon marker saturates")
    L += [
        t(1107, 190, "sign(M) = sign(q_next − 0.625)", 17, weight="bold"),
        t(1107, 230, "1,920,000 patch-generations; 0 sign mismatches", 14, weight="bold"),
        t(1107, 278, "g20 all-M<0: 3,943/3,943 events; 2,057/2,057 non-events", 13),
        t(1107, 320, "sensitivity=1   specificity=0   AUC=0.5", 16, weight="bold"),
        t(1107, 365, "transition-exactness does not imply fate-predictiveness", 13, weight="bold"),
    ]

    box(L, 55, 455, 675, 345, "C  Continuous last-refuge reserve", "fresh prospective 12,000-trajectory holdout")
    L += [
        t(392, 545, f"route-margin AUC {auc['mean_seed_block_auc']:.5f}", 20, weight="bold"),
        t(392, 580, f"95% CI [{auc['ci95'][0]:.5f}, {auc['ci95'][1]:.5f}]", 13),
        t(392, 625, f"co-timed max-q AUC {maxq['mean_seed_block_auc']:.5f}", 15),
        t(392, 665, f"paired AUC gain +{gain['mean']:.5f}", 17, weight="bold"),
        t(392, 698, f"95% CI [+{gain['ci95'][0]:.5f}, +{gain['ci95'][1]:.5f}]", 13),
        t(392, 745, f"only {100*timely['fraction']:.3f}% of eventual losses already occurred", 13, weight="bold"),
    ]

    box(L, 770, 455, 675, 345, "D  Representation hierarchy", "what each observable actually tells us")
    L += [
        t(1107, 545, "marginal erosion  →  stress sensitivity", 16, weight="bold"),
        t(1107, 605, "exact route sign  →  next-transition side", 16, weight="bold"),
        t(1107, 665, "continuous strongest-local reserve  →  later-fate ranking", 16, weight="bold"),
        t(1107, 725, "thresholding can discard reserve depth even when the coordinate is exact", 12),
        t(1107, 765, "finite-closure result; not a universal natural warning variable", 12),
    ]
    L.append(t(750, 875, "stress sensitivity ≠ transition exactness ≠ fate information", 20, weight="bold"))
    done(L, path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--egc-root", required=True)
    parser.add_argument("--egwe-root", required=True)
    parser.add_argument("--flagship-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    fig1(out / "figure1_mathematical_boundaries.svg")
    fig2(Path(args.egc_root), out / "figure2_state_separation.svg")
    fig3(Path(args.egwe_root), Path(args.flagship_root), out / "figure3_relational_state.svg")
    fig4(Path(args.egwe_root), Path(args.flagship_root), out / "figure4_warning_discrimination.svg")
    print("Generated four resolved-sorting flagship figures")


if __name__ == "__main__":
    main()
