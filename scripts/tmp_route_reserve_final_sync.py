from pathlib import Path
import json


def replace_once(path, old, new):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected one match, got {n}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "scripts/build_nee_sorting_buffering_figures.py",
    'box(L, 490, 155, 520, 115, "Pathway mechanism", "q-dependent allele sorting <-> buffering")',
    'box(L, 490, 155, 520, 115, "Pathway mechanism", "sorting / recruitment buffering / direct recoupling")',
)
replace_once(
    "scripts/build_nee_sorting_buffering_figures.py",
    'box(L, 400, 430, 700, 125, "Positive synthesis", "functional fate depends on whether sorting outruns buffering")',
    'box(L, 400, 430, 700, 125, "Positive synthesis", "fate reflects sorting, buffering, recoupling and remaining refuge reserve")',
)

p = Path("scripts/build_nee_sorting_buffering_figures.py")
text = p.read_text(encoding="utf-8")
start = text.index("def fig4(root, path):")
end = text.index("\ndef main():", start)
new_fig4 = r'''def fig4(root, flagship, path):
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
'''
text = text[:start] + new_fig4 + text[end:]
old_call = 'fig4(Path(args.egwe_root), out / "figure4_warning_discrimination.svg")'
new_call = 'fig4(Path(args.egwe_root), Path(args.flagship_root), out / "figure4_warning_discrimination.svg")'
if text.count(old_call) != 1:
    raise RuntimeError("Figure 4 call anchor drifted")
text = text.replace(old_call, new_call, 1)
p.write_text(text, encoding="utf-8")

replace_once(
    "scripts/build_nee_four_operator_figure3.py",
    "Four-panel causal decomposition of immediate covariance, q-dependent allele sorting, two repair operators and a density feedback collapse gate.",
    "Four-panel causal decomposition of immediate covariance, q-dependent allele sorting, recruitment buffering, direct eco-genetic recoupling and a density feedback collapse gate.",
)
replace_once(
    "scripts/build_nee_four_operator_figure3.py",
    'panel(L, 45, 520, 690, 430, "C", "Two repair operators counter spatial mismatch")',
    'panel(L, 45, 520, 690, 430, "C", "Buffering and recoupling act on different mismatches")',
)
replace_once(
    "scripts/build_nee_four_operator_figure3.py",
    '        txt(390, 910, "recruitment repairs trait–allele mismatch; direct feedback repairs interaction–bundle mismatch", 12),\n',
    '        txt(390, 850, "fresh route-duration DID: −0.677 gen [−0.694,−0.660]", 12, weight="bold"),\n        txt(390, 880, "recoupling does not imply generic above-switch refuge extension", 11),\n        txt(390, 918, "recruitment buffers trait–allele mismatch; direct feedback recouples interaction–bundle state", 11),\n',
)
replace_once(
    "scripts/build_nee_four_operator_figure3.py",
    '        txt(1310, 447, "[+5.800,+7.967]", 12),\n',
    '        txt(1310, 447, "[+5.800,+7.967]", 12),\n        txt(1110, 474, "fresh 24k: g20 max-headroom DID +0.0007906; g40 DID +8.60 pp", 10, weight="bold"),\n',
)
replace_once(
    "scripts/build_nee_four_operator_figure3.py",
    'txt(750, 1052, "covariance creates divergence  →  sorting  ↔  repair (buffering + recoupling)  →  density-feedback collapse gate", 15, weight="bold"),',
    'txt(750, 1052, "covariance creates divergence  →  sorting  ↔  buffering + recoupling  →  density-feedback collapse gate", 15, weight="bold"),',
)

replace_once(
    "manuscript/nee_flagship_cover_letter.md",
    "identify the life-cycle operators that create, repair and amplify those differences.",
    "identify the life-cycle operators that sort, buffer, recouple and amplify those differences.",
)

manifest_path = Path("manuscript/nee_flagship_source_manifest.json")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
target = next(x for x in manifest["load_bearing_sources"] if x["layer"] == "prospective_continuous_last_refuge_warning_holdout")
req = target["required_flagship_paths"]
art = "artifacts/last_refuge_warning_holdout/locked_result.json"
if art not in req:
    req.insert(1, art)
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

wf = Path(".github/workflows/nee-math-first-flagship.yml")
text = wf.read_text(encoding="utf-8")
text = text.replace(
    "      - 'artifacts/density_feedback_gate/**'\n",
    "      - 'artifacts/density_feedback_gate/**'\n      - 'artifacts/operator_balance_route_margin/**'\n      - 'artifacts/headroom_mediation_followup/**'\n      - 'artifacts/last_refuge_warning_holdout/**'\n",
    1,
)
text = text.replace(
    "      - 'docs/DENSITY_FEEDBACK_FAILURE_GATE_THEOREM_2026-09-06.md'\n",
    "      - 'docs/DENSITY_FEEDBACK_FAILURE_GATE_THEOREM_2026-09-06.md'\n      - 'docs/OPERATOR_BALANCE_ROUTE_MARGIN_THEOREM_2026-09-06.md'\n      - 'docs/OPERATOR_BALANCE_ROUTE_MARGIN_RESULT_2026-09-07.md'\n      - 'docs/HEADROOM_MEDIATION_FOLLOWUP_RESULT_2026-09-06.md'\n      - 'docs/LAST_REFUGE_WARNING_HOLDOUT_RESULTS_2026-09-07.md'\n      - 'docs/NEE_ROUTE_RESERVE_CAUSAL_BRIDGE_2026-09-08.md'\n",
    1,
)
text = text.replace(
    "      - 'experiments/allele_sorting_single_edge_protocol.json'\n",
    "      - 'experiments/allele_sorting_single_edge_protocol.json'\n      - 'experiments/operator_balance_margin_fate_protocol.json'\n      - 'experiments/headroom_mediation_followup_protocol.json'\n      - 'experiments/last_refuge_warning_holdout_protocol.json'\n",
    1,
)
old_locked = "            'prospective_allele_sorting_single_edge_proof': (34016797940,9984306657,'sha256:61a07cc6a8680a59185537b03abdca85d0f172a65d068ee9661dd9f2fb448c2d'),\n"
new_locked = old_locked + "            'prospective_operator_balance_route_margin': (34127034037,10021317930,'sha256:1e5ecb658a66e78ffa0ea7eb0cf073323a2173eca7c55461a11aa91b8bd4eb69'),\n            'prospective_sorting_headroom_followup': (34029794984,9988541984,'sha256:f8150ea9c7bc8e6e68aff3fbf3a572267204fc7882af11280f360f576fc01f2c'),\n            'prospective_continuous_last_refuge_warning_holdout': (34130457262,10022340904,'sha256:46a6b03d3d93a0fb5d03c2e9e27b087605b0cf5dda281fd27ed4581ab3640447'),\n"
if text.count(old_locked) != 1:
    raise RuntimeError("flagship locked dict anchor drifted")
text = text.replace(old_locked, new_locked, 1)
old_if = "if source.get('source_type') == 'locked_workflow_artifact_materialized_in_flagship_repository':"
new_if = "if source.get('source_type') in {'locked_workflow_artifact_materialized_in_flagship_repository', 'prospectively_locked_workflow_artifact_materialized_in_flagship_repository'}:"
if text.count(old_if) != 1:
    raise RuntimeError("flagship source_type verifier anchor drifted")
text = text.replace(old_if, new_if, 1)
old_grep = "          grep -q 'AUC=0.5' nee_packet/figures/figure4_warning_discrimination.svg\n"
new_grep = "          grep -q '1,920,000' nee_packet/figures/figure4_warning_discrimination.svg\n          grep -q 'AUC=0.5' nee_packet/figures/figure4_warning_discrimination.svg\n          grep -q '0.92734' nee_packet/figures/figure4_warning_discrimination.svg\n          grep -q '+0.02135' nee_packet/figures/figure4_warning_discrimination.svg\n          grep -q 'transition-exactness does not imply fate-predictiveness' nee_packet/figures/figure4_warning_discrimination.svg\n"
if text.count(old_grep) != 1:
    raise RuntimeError("Figure 4 grep anchor drifted")
text = text.replace(old_grep, new_grep, 1)
packet_anchor = "          cp flagship/docs/MECHANISTIC_OPERATOR_SYNTHESIS_2026-09-06.md nee_packet/provenance/mechanistic_operator_synthesis.md\n"
packet_add = packet_anchor + "          cp flagship/artifacts/operator_balance_route_margin/locked_result.json nee_packet/provenance/operator_balance_route_margin_locked_result.json\n          cp flagship/docs/OPERATOR_BALANCE_ROUTE_MARGIN_THEOREM_2026-09-06.md nee_packet/provenance/operator_balance_route_margin_theorem.md\n          cp flagship/docs/OPERATOR_BALANCE_ROUTE_MARGIN_RESULT_2026-09-07.md nee_packet/provenance/operator_balance_route_margin_result.md\n          cp flagship/experiments/operator_balance_margin_fate_protocol.json nee_packet/provenance/operator_balance_route_margin_protocol.json\n          cp flagship/artifacts/headroom_mediation_followup/locked_result.json nee_packet/provenance/headroom_mediation_locked_result.json\n          cp flagship/docs/HEADROOM_MEDIATION_FOLLOWUP_RESULT_2026-09-06.md nee_packet/provenance/headroom_mediation_result.md\n          cp flagship/experiments/headroom_mediation_followup_protocol.json nee_packet/provenance/headroom_mediation_protocol.json\n          cp flagship/artifacts/last_refuge_warning_holdout/locked_result.json nee_packet/provenance/last_refuge_warning_locked_result.json\n          cp flagship/docs/LAST_REFUGE_WARNING_HOLDOUT_RESULTS_2026-09-07.md nee_packet/provenance/last_refuge_warning_result.md\n          cp flagship/experiments/last_refuge_warning_holdout_protocol.json nee_packet/provenance/last_refuge_warning_protocol.json\n          cp flagship/docs/NEE_ROUTE_RESERVE_CAUSAL_BRIDGE_2026-09-08.md nee_packet/provenance/route_reserve_causal_bridge.md\n"
if text.count(packet_anchor) != 1:
    raise RuntimeError("flagship packet anchor drifted")
text = text.replace(packet_anchor, packet_add, 1)
wf.write_text(text, encoding="utf-8")
