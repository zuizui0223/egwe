from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def txt(x, y, text, size=14, anchor="middle", weight="normal"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Arial,Helvetica,sans-serif" font-size="{size}" '
        f'font-weight="{weight}">{html.escape(str(text))}</text>'
    )


def rect(x, y, w, h, rx=10, sw=1.8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="white" stroke="#222" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, arrow=False, dash=None):
    extra = ' marker-end="url(#arrow)"' if arrow else ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="1.8"{extra}/>'


def panel(lines, x, y, w, h, label, title):
    lines.append(rect(x, y, w, h, rx=12, sw=2.0))
    lines.append(txt(x + 18, y + 30, label, 16, anchor="start", weight="bold"))
    lines.append(txt(x + w / 2, y + 30, title, 17, weight="bold"))


def build(flagship: Path, egwe: Path, output: Path) -> None:
    phase = json.loads((egwe / "artifacts/cross_layer_alignment/phase_v_locked_summary.json").read_text())
    edge = json.loads((flagship / "artifacts/pathway_edge_decomposition/locked_result.json").read_text())
    focused = json.loads((flagship / "artifacts/allele_sorting_single_edge/locked_result.json").read_text())
    rec = json.loads((flagship / "artifacts/direct_feedback_recoupling/locked_derived_result.json").read_text())
    dens = json.loads((flagship / "artifacts/density_feedback_gate/locked_derived_result.json").read_text())

    exact_q = phase["opening_certificate"]["maximum_patchwise_generation1_difference"]
    assert abs(exact_q - 0.25433292878878405) < 1e-12
    primary = focused["primary_generation_40_DID"]
    assert primary["decision"] == "resolved_positive_sorting_contribution"
    assert primary["n_paired_keys"] == 6000
    assert edge["edge_deletions"]["allele_linked_recruitment"]["decision"] == "resolved_countervailing_buffer"
    assert rec["generation_40"]["DID_ci95"][0] > 0
    assert dens["generation_20"]["AA"]["delete_density_loss_rate"] == 0.0
    assert dens["generation_20"]["RR"]["delete_density_loss_rate"] == 0.0

    W, H = 1500, 1120
    L = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">Why matched eco-genetic marginals reach different functional futures</title>',
        '<desc id="desc">Four-panel causal decomposition of immediate covariance, q-dependent allele sorting, recruitment buffering, direct eco-genetic recoupling and a density feedback collapse gate.</desc>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L0,9 L9,4.5 z" fill="#222"/></marker></defs>',
        txt(750, 42, "Why matched marginals reach different futures", 28, weight="bold"),
        txt(750, 70, "exact operators + prospectively locked finite interventions", 13),
    ]

    # A: immediate divergence.
    panel(L, 45, 100, 690, 390, "A", "Cross-layer covariance creates immediate divergence")
    L += [
        rect(90, 155, 235, 76), txt(208, 184, "State A support", 14, weight="bold"), txt(208, 211, ".47  .61  .75  .89", 13),
        rect(455, 155, 235, 76), txt(572, 184, "State R support", 14, weight="bold"), txt(572, 211, ".71  .69  .67  .65", 13),
        txt(390, 270, "mean(S) = 0.68 in both states", 14, weight="bold"),
        txt(390, 305, "Var(S): 0.0245 vs 0.0005 = 49-fold difference", 16, weight="bold"),
        txt(390, 342, "fixed marginals; covariance changes where support is concentrated", 12),
        txt(390, 385, "max exact next-q difference = 0.2543", 17, weight="bold"),
        txt(390, 425, "same conventional state summaries ≠ same transition", 14),
    ]

    # B: sorting operator + focused proof.
    panel(L, 765, 100, 690, 390, "B", "q-dependent allele selection is the sorting operator")
    L += [
        txt(1110, 160, "logit(p+) − logit(p) = log(0.75 + 0.4q)", 16, weight="bold"),
        txt(1110, 198, "dp+/dq > 0; exact switch q*=0.625", 15, weight="bold"),
        txt(1110, 228, "same threshold as declared high-trait viability", 12),
        txt(1110, 267, "one step increases Cov(q, logit p) when q varies spatially", 12),
        line(860, 318, 1360, 318),
        txt(1110, 350, "Focused 6,000-pair g40 proof", 15, weight="bold"),
        txt(915, 390, "baseline", 12, weight="bold"), txt(915, 418, "RR−AA +6.65 pp", 14),
        txt(1110, 390, "delete q→allele", 12, weight="bold"), txt(1110, 418, "RR−AA −0.23 pp", 14),
        txt(1310, 390, "causal DID", 12, weight="bold"), txt(1310, 418, "+6.883 pp", 16, weight="bold"),
        txt(1310, 447, "[+5.800,+7.967]", 12),
        txt(1110, 474, "fresh 24k: g20 max-headroom DID +0.0007906; g40 DID +8.60 pp", 10, weight="bold"),
    ]

    # C: repair operators.
    panel(L, 45, 520, 690, 430, "C", "Buffering and recoupling act on different mismatches")
    L += [
        txt(220, 580, "Recruitment buffering", 15, weight="bold"),
        txt(220, 616, "r = (m+p)/2", 17, weight="bold"),
        txt(220, 650, "|r−p| = 0.5 |m−p|", 14),
        txt(220, 680, "trait–allele mismatch contracts 50%", 13, weight="bold"),
        txt(220, 722, "deletion DID", 11),
        txt(220, 750, "g20 −9.00 pp", 14, weight="bold"),
        txt(220, 777, "g40 −8.33 pp", 14, weight="bold"),
        line(385, 565, 385, 900, dash="5 5"),
        txt(555, 580, "Direct feedback recoupling", 15, weight="bold"),
        txt(555, 616, "B=.75T+.25G; S=.6q+.4B", 15, weight="bold"),
        txt(555, 650, "|S−B| = .6 |q−B|", 14),
        txt(555, 680, "q–bundle mismatch contracts 40%", 13, weight="bold"),
        txt(555, 715, "Δ logit(q+) = 1.8 d(B−q)", 13),
        txt(555, 758, "RR benefit: +8.53 / +7.80 pp", 13, weight="bold"),
        txt(555, 788, "RR−AA benefit DID", 11),
        txt(555, 817, "+7.93 / +6.33 pp", 14, weight="bold"),
        txt(390, 850, "fresh route-duration DID: −0.677 gen [−0.694,−0.660]", 12, weight="bold"),
        txt(390, 880, "recoupling does not imply generic above-switch refuge extension", 11),
        txt(390, 918, "recruitment buffers trait–allele mismatch; direct feedback recouples interaction–bundle state", 11),
    ]

    # D: failure gate.
    panel(L, 765, 520, 690, 430, "D", "Density feedback opens and amplifies the collapse regime")
    L += [
        txt(1110, 580, "q+ = sigmoid[4.5(dq − θ)]", 17, weight="bold"),
        txt(1110, 618, "below carrying capacity: ∂q+/∂N > 0", 14),
        txt(1110, 654, "q↓  →  N↓  →  density↓  →  q↓", 16, weight="bold"),
        txt(1110, 692, "exact headroom boundary for q+ ≥ .625", 12),
        txt(1110, 724, "d·q ≥ θ + 0.1135168053", 16, weight="bold"),
        txt(1110, 758, "required d·q: 0.6160 (g1) → 0.6635 (g20) → 0.7135 (g40)", 12),
        line(850, 800, 1370, 800),
        txt(1110, 830, "delete density→q", 13, weight="bold"),
        txt(1110, 862, "g20: 0/1,500 loss in AA and RR", 15, weight="bold"),
        txt(1110, 894, "g40 risk reduction: 57.47 pp / 59.60 pp", 14, weight="bold"),
        txt(1110, 925, "failure/amplification gate — not the sorting edge", 12),
    ]

    # Bottom causal synthesis.
    L += [
        rect(115, 985, 1270, 92, rx=14, sw=2.2),
        txt(750, 1018, "Causal architecture", 16, weight="bold"),
        txt(750, 1052, "covariance creates divergence  →  sorting  ↔  buffering + recoupling  →  density-feedback collapse gate", 15, weight="bold"),
        txt(750, 1093, "Natural examples are Discussion-level projections, not validation of these finite operators.", 11),
    ]
    L.append("</svg>")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--flagship-root", type=Path, required=True)
    p.add_argument("--egwe-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    build(args.flagship_root, args.egwe_root, args.output)
    print(f"Wrote four-operator Figure 3: {args.output}")


if __name__ == "__main__":
    main()
