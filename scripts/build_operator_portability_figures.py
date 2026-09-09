from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)


def svg_text(x: float, y: float, text: str, size: int = 16, weight: str = "normal", anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(text)}</text>'


def build_fig1() -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640">',
        '<rect width="1200" height="640" fill="white"/>',
        svg_text(60, 55, "Figure 1 | Evidence architecture: replication versus operator substitution", 24, "bold"),
        svg_text(60, 100, "Historical reference ensemble (seeds 20290410–20290414)", 18, "bold"),
        '<rect x="70" y="125" width="360" height="90" rx="10" fill="#f2f2f2" stroke="#333"/>',
        svg_text(250, 160, "No connectivity", 18, "bold", "middle"),
        svg_text(250, 190, "shared historical observations", 14, "normal", "middle"),
        '<rect x="470" y="125" width="360" height="90" rx="10" fill="#f2f2f2" stroke="#333"/>',
        svg_text(650, 160, "Allele-only m=.10", 18, "bold", "middle"),
        svg_text(650, 190, "shared historical observations", 14, "normal", "middle"),
        svg_text(900, 100, "One fresh replication", 18, "bold"),
        '<rect x="885" y="125" width="250" height="90" rx="10" fill="#eef6ff" stroke="#333"/>',
        svg_text(1010, 158, "Phase U", 18, "bold", "middle"),
        svg_text(1010, 186, "new seeds, same operator", 14, "normal", "middle"),
        '<line x1="830" y1="170" x2="885" y2="170" stroke="#333" stroke-width="2" marker-end="url(#a)"/>',
        '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>',
        svg_text(60, 285, "Two process substitutions against the same historical reference", 18, "bold"),
        '<line x1="250" y1="215" x2="250" y2="340" stroke="#555" stroke-width="2"/>',
        '<line x1="650" y1="215" x2="650" y2="340" stroke="#555" stroke-width="2"/>',
        '<line x1="250" y1="340" x2="650" y2="340" stroke="#555" stroke-width="2"/>',
        '<line x1="450" y1="340" x2="450" y2="380" stroke="#555" stroke-width="2"/>',
        '<rect x="130" y="390" width="390" height="95" rx="10" fill="#f7f7ff" stroke="#333"/>',
        svg_text(325, 425, "Phase R: whole-individual d=.10", 18, "bold", "middle"),
        svg_text(325, 454, "process arm only; historical refs reused", 14, "normal", "middle"),
        '<rect x="590" y="390" width="390" height="95" rx="10" fill="#fff7f1" stroke="#333"/>',
        svg_text(785, 425, "Phase S: pollen-only g=.20", 18, "bold", "middle"),
        svg_text(785, 454, "process arm only; historical refs reused", 14, "normal", "middle"),
        '<line x1="450" y1="380" x2="325" y2="390" stroke="#555" stroke-width="2" marker-end="url(#a)"/>',
        '<line x1="450" y1="380" x2="785" y2="390" stroke="#555" stroke-width="2" marker-end="url(#a)"/>',
        '<rect x="120" y="530" width="900" height="70" rx="12" fill="#fafafa" stroke="#222" stroke-width="2"/>',
        svg_text(570, 563, "Evidence count: 1 independent fresh replication + 2 shared-reference operator substitutions", 18, "bold", "middle"),
        svg_text(570, 588, "R and S are not independent baseline replications", 15, "normal", "middle"),
        '</svg>'
    ]
    return "\n".join(parts)


def load_groups():
    u = json.loads((ROOT / "artifacts/fresh_connectivity_replication/phase_u_locked_summary.json").read_text())
    r = json.loads((ROOT / "artifacts/process_resolved_movement/phase_r_locked_summary.json").read_text())
    s = json.loads((ROOT / "artifacts/process_resolved_pollen/phase_s_locked_summary.json").read_text())

    u_by = {float(row["migration_rate"]): row for row in u["condition_summaries"]}
    r_by = {row["condition"]: row for row in r["conditions"]}
    s_by = {row["condition"]: row for row in s["conditions"]}

    def u_rates(row):
        return [float(x["rate"]) for x in row["blocks"]]

    def rs_rates(row):
        return [losses / eligible for losses, eligible in row["blocks"]]

    return [
        ("U m=0", u_rates(u_by[0.0]), float(u_by[0.0]["pooled_loss_rate"]), float(u_by[0.0]["pearson_equal_rate_p"])),
        ("U m=.10", u_rates(u_by[0.1]), float(u_by[0.1]["pooled_loss_rate"]), float(u_by[0.1]["pearson_equal_rate_p"])),
        ("Hist. none", rs_rates(r_by["no_connectivity"]), float(r_by["no_connectivity"]["pooled_loss_rate"]), float(r_by["no_connectivity"]["equal_rate_p"])),
        ("Hist. m=.10", rs_rates(r_by["allele_only_m010"]), float(r_by["allele_only_m010"]["pooled_loss_rate"]), float(r_by["allele_only_m010"]["equal_rate_p"])),
        ("R d=.10", rs_rates(r_by["individual_dispersal_d010"]), float(r_by["individual_dispersal_d010"]["pooled_loss_rate"]), float(r_by["individual_dispersal_d010"]["equal_rate_p"])),
        ("S g=.20", rs_rates(s_by["pollen_only_g020"]), float(s_by["pollen_only_g020"]["pooled_loss_rate"]), float(s_by["pollen_only_g020"]["equal_rate_p"])),
    ]


def build_fig2() -> str:
    groups = load_groups()
    width, height = 1200, 700
    left, right, top, bottom = 90, 80, 90, 150
    plot_w = width - left - right
    plot_h = height - top - bottom
    ymin, ymax = 0.35, 0.80

    def y(v):
        return top + (ymax - v) / (ymax - ymin) * plot_h

    step = plot_w / len(groups)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        svg_text(55, 45, "Figure 2 | Block-rate heterogeneity in the locked portability programme", 24, "bold"),
    ]
    for tick in [0.4, 0.5, 0.6, 0.7, 0.8]:
        yy = y(tick)
        parts += [f'<line x1="{left}" y1="{yy}" x2="{width-right}" y2="{yy}" stroke="#dddddd"/>', svg_text(left-12, yy+5, f"{tick:.1f}", 14, "normal", "end")]
    parts.append(svg_text(28, top + plot_h/2, "block loss rate", 16, "bold"))

    offsets = [-18, -9, 0, 9, 18]
    for i, (label, rates, pooled, pval) in enumerate(groups):
        x = left + step*(i+0.5)
        for off, rate in zip(offsets, rates, strict=True):
            parts.append(f'<circle cx="{x+off}" cy="{y(rate)}" r="5.5" fill="#333"/>')
        parts.append(f'<line x1="{x-32}" y1="{y(pooled)}" x2="{x+32}" y2="{y(pooled)}" stroke="#000" stroke-width="4"/>')
        parts.append(svg_text(x, top+plot_h+35, label, 15, "bold", "middle"))
        parts.append(svg_text(x, top+plot_h+58, f"p={pval:.3f}", 13, "normal", "middle"))

    note_y = height - 55
    parts += [
        '<rect x="120" y="600" width="960" height="70" rx="10" fill="#fafafa" stroke="#444"/>',
        svg_text(600, 628, "Design sensitivity (not an equivalence margin):", 15, "bold", "middle"),
        svg_text(600, 652, "80% power w≈0.163 ≈ 8.1–8.2 pp weighted RMS block-rate deviation near pooled p=.5", 14, "normal", "middle"),
        '</svg>'
    ]
    return "\n".join(parts)


def main() -> int:
    (OUT / "operator_portability_fig1.svg").write_text(build_fig1(), encoding="utf-8")
    (OUT / "operator_portability_fig2.svg").write_text(build_fig2(), encoding="utf-8")
    print("wrote operator-portability figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
