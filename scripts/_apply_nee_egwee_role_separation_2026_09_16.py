from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "manuscript/nee_flagship_article.md"
COVER = ROOT / "manuscript/nee_flagship_cover_letter.md"
META = ROOT / "manuscript/nee_flagship_submission_metadata.md"
DISPLAY = ROOT / "manuscript/nee_flagship_display_plan.md"
MANIFEST = ROOT / "manuscript/nee_flagship_source_manifest.json"
CHECKER = ROOT / "scripts/check_nee_flagship_compliance.py"
WORKFLOW = ROOT / ".github/workflows/nee-math-first-flagship.yml"

EGWEE_COMMIT = "16308cf6d6e4aec274504ba81bbf6e71be465099"

NEW_ABSTRACT = """Fragmentation is often treated as a single gradient of biological deterioration, yet ecological and genetic layers need not move together. In a finite eco-genetic model, subdividing fixed area eliminated potential high-trait viability in 1,037/1,037 cases at every tested subdivision while realised occupancy remained 99.6–100%; realised high-trait mass declined and then partially recovered at high subdivision. We then asked what determines divergent futures once state separation occurs. Constructive matched-marginal states showed that conventional ecological and genetic marginals are not transition-sufficient. Prospectively locked interventions resolved q-dependent allele sorting, recruitment buffering, direct recoupling and a density-mediated collapse gate. Marginal diversity thresholds preceded every observed loss yet had specificity 0, showing that temporal precedence need not imply fate discrimination. By contrast, continuous strongest-refuge reserve added ranking information beyond co-timed maximum interaction state (AUC difference +0.02135, 95% CI +0.01770,+0.02501). Fragmentation therefore need not generate one biological state, and functional fate depends on cross-layer organization, life-cycle operators and remaining local reserve. Numerical thresholds, effect sizes and horizons are closure-specific."""

NEW_ROADMAP = """We organize the paper around two biological questions. **Question 1 asks whether fragmentation produces one biological deterioration state.** We derive the canonical interaction-state geometry and test a fixed-area fragmentation gradient in which potential viability, realised occupancy, interaction support, demography and trait state can separate. **Question 2 asks what determines divergent futures once that separation is acknowledged.** We construct matched-marginal states, identify hidden cross-layer organization that changes exact transitions, intervene on life-cycle operators responsible for sorting, buffering, recoupling and collapse entry, and distinguish stress sensitivity from fate information using the continuous reserve of the strongest remaining local refuge. The two questions form one argument: fragmentation first separates biological layers, then local organization and life-cycle operators determine how that separation is propagated into fate."""

DISCUSSION_OPEN = """Fragmentation did not generate one biological deterioration state in this model family. Potential high-trait viability disappeared under every tested subdivision while realised occupancy remained nearly complete, and interaction, demography and realised trait mass followed distinct, partly non-monotonic trajectories. This is the central result of Question 1: habitat subdivision can separate biological layers before demographic disappearance, so fragmentation intensity cannot by itself stand in for biological state.

Question 2 asks what then determines fate. The matched-marginal counterexample shows that conventional marginal summaries can be identical while exact next transitions differ, and the intervention programme resolves how q-dependent sorting, recruitment buffering, direct recoupling and density feedback transform that hidden organization through time. The monitoring result follows from the same architecture: fate-relevant information is retained in the depth of the strongest remaining local reserve beyond what is carried by a co-timed interaction maximum."""

NATURAL_DISCUSSION = """A separately protocol-locked five-cluster natural synthesis provides bounded external-consistency evidence rather than validation. Under its source-supported paired-dependence reconstruction, the global intersection test gave Fisher `p=0.0121`; omitting *Serapias* gave `p=0.1819`. A zero-covariance sensitivity remained below 0.05 (`p=0.0386`), but a covariance-free Cauchy–Schwarz certification bound did not (`p=0.2806`). The natural inference is therefore conditional on within-system dependence information and is reported in full separately; it is not used to validate the finite operators here.

Separately, the first locked natural prospective transfer of the specific strongest-refuge predictor did not establish incremental future-occupancy information after contemporaneous marginals (`delta NLL M1-M0=-0.0003211`, species-bootstrap 95% CI `[-0.0009825,+0.0003422]`). We retain that result as a portability boundary rather than promoting its secondary persistence-only direction or treating the finite AUC 0.9273 as naturally validated."""

PREDICTION_PARAGRAPH = """These finite results make two testable natural-system predictions rather than claims of external validation. First, fragmentation responses should differ among interaction, reproductive, demographic and genetic layers in magnitude or timing. Second, the degree and timing of discordance should covary with independently measured movement, reproductive assurance, pollination mode and cohort or landscape history. The separate natural synthesis evaluates the first prediction; future moderator analyses can address the second without converting either result into validation of the finite operators."""

GENERALITY_SECTION = """### Generality differs for counterexamples and positive mechanisms

Two kinds of result require different claim ceilings. The transition-sufficiency result is constructive: if two admissible states share the declared marginal representation but have different exact transitions, then those marginals cannot be universally sufficient for every system admitted by that representation. Likewise, temporal precedence does not logically entail fate discrimination, because sensitivity 1 and specificity 0 can coexist. These are **non-implication results**. Their force does not depend on the numerical values `0.2543`, `q*=0.625` or any particular generation generalizing to nature.

The positive mechanism results have a narrower ceiling. The operator weights, switch value, intervention effect sizes, route-margin coefficients, generation horizons and absolute warning AUC belong to the declared finite closure. They show how one biologically motivated system realizes state separation and fate divergence; they do not establish universal natural sorting, buffering, recoupling, density thresholds or warning performance. The nontrivial predictive comparison is therefore the **incremental information beyond a co-timed summary**—the prospectively locked route margin exceeded co-timed maximum q by `+0.02135` AUC—rather than the absolute AUC as a portable performance benchmark."""

METHODS_PROVENANCE = """### Provenance of Question 1

Question 1 incorporates the canonical interaction map and fixed-area fragmentation programme historically developed in the repository `zuizui0223/eco-genetic-criticality`. That material is unpublished and has no separate active submission; it is part of the present study. The exact fixed-point geometry and fragmentation-gradient evidence are presented in this manuscript and pinned to source commit `b7ee738767c92307d6d23a85a3eeb857faf6ddfb` in the evidence manifest. The historical repository label is provenance, not a separate theorem invoked without presentation here."""


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly one match, got {n}"
    return text.replace(old, new, 1)


def sub_once(text: str, pattern: str, replacement: str, label: str) -> str:
    new, n = re.subn(pattern, replacement, text, count=1, flags=re.S)
    assert n == 1, f"{label}: expected one regex match, got {n}"
    return new


def update_article(article: str) -> str:
    article = sub_once(
        article,
        r"(?s)(## Abstract\n\n).*?(\n\nEcological fragmentation changes more than habitat amount\.)",
        r"\1" + NEW_ABSTRACT + r"\2",
        "abstract",
    )

    article = sub_once(
        article,
        r"\n\nNatural fragmentation provides an independent test of the same premise\..*?operator-level causation remains a finite-model question\.",
        "",
        "old natural introduction paragraph",
    )

    article = sub_once(
        article,
        r"We organize the paper around two biological questions\..*?operator-level natural analogies remain Discussion-level projections rather than validation of the finite mechanisms\.",
        NEW_ROADMAP,
        "roadmap",
    )

    article = replace_once(
        article,
        "The parent framework begins with the canonical interaction map",
        "Question 1 begins with the canonical interaction map",
        "Q1 ownership",
    )

    article = sub_once(
        article,
        r"\n### Natural corpus-level evidence supported layer non-exchangeability\n\n.*?\n### Question 2 — Given state separation, what determines divergent futures and predicts fate\?",
        "\n### Question 2 — Given state separation, what determines divergent futures and predicts fate?",
        "natural Results subsection",
    )

    article = article.replace(
        "\n\nNatural data provide independent, bounded evidence that state separation is not peculiar to the finite construction; the finite closure is then used to identify why separated states diverge.\n",
        "\n",
        1,
    )

    article = sub_once(
        article,
        r"(?s)(## Discussion\n\n).*?(?=\n\nThis decomposition matters because several intuitive explanations failed\.)",
        r"\1" + DISCUSSION_OPEN,
        "Discussion opening",
    )

    article = sub_once(
        article,
        r"The natural and finite results carry different inferential loads\..*?treating the finite AUC 0\.9273 as naturally validated\.",
        NATURAL_DISCUSSION,
        "old natural Discussion paragraph",
    )

    article = replace_once(
        article,
        "\n\nThe claim remains bounded.",
        "\n\n" + PREDICTION_PARAGRAPH + "\n\nThe claim remains bounded.",
        "natural predictions insertion",
    )

    assert "### Generality differs for counterexamples and positive mechanisms" not in article
    article = article.replace("\n## Methods\n", "\n\n" + GENERALITY_SECTION + "\n\n## Methods\n", 1)
    article = article.replace("## Methods\n", "## Methods\n\n" + METHODS_PROVENANCE + "\n", 1)

    article = article.replace(
        "Load-bearing evidence is restricted to the theorem-guided parent framework,",
        "Load-bearing evidence is restricted to the canonical interaction-map geometry and fixed-area fragmentation programme,",
        1,
    )
    article = article.replace(
        "EGWEE supplies independent natural evidence for Question 1 only; the natural strongest-refuge test remains a null portability boundary, and all operator-level causal claims remain finite-closure results.",
        "The separate natural synthesis is cited only as bounded Discussion-level external-consistency evidence for Question 1; it is not load-bearing for the finite Question-1 demonstration and is not used to validate any finite operator. The natural strongest-refuge test remains a null portability boundary, and all operator-level causal claims remain finite-closure results.",
        1,
    )

    assert "Natural corpus-level evidence supported layer non-exchangeability" not in article
    assert "Three-system natural evidence" not in article
    assert "p=0.00621" not in article
    assert "Fisher chi-square(6)=18.01" not in article
    assert "Using the EGC theorem" not in article
    assert "Using EGWE" not in article
    assert "p=0.0121" in article and "p=0.1819" in article
    assert "p=0.0386" in article and "p=0.2806" in article
    results = article.split("## Results\n", 1)[1].split("## Discussion\n", 1)[0]
    abstract = article.split("## Abstract\n", 1)[1].split("\n\n", 1)[0]
    for token in ("Serapias", "0.0121", "0.1819", "0.0386", "0.2806"):
        assert token not in results, f"bounded natural evidence leaked into Results: {token}"
    assert "natural synthesis" not in abstract.casefold()
    return article


def update_cover(cover: str) -> str:
    old = "Fragmentation ecology often tracks habitat geometry, abundance, interactions and genetic diversity as separate indicators of deterioration. Our study asks a mechanistic question: **why can systems retaining the same marginal ecological and genetic quantities nevertheless reach different functional outcomes?** We combine exact results with prospectively locked intervention experiments to identify the life-cycle operators that sort, buffer, recouple and amplify those differences."
    new = "Fragmentation is often treated as a single gradient of biological deterioration. Our study asks two linked questions: **does fragmentation actually generate one biological state, and, once biological layers separate, what determines their divergent functional futures?** We combine an exact fragmentation-state analysis, a constructive transition-sufficiency counterexample and prospectively locked intervention experiments to identify what is logically insufficient and which life-cycle operators sort, buffer, recouple and amplify the remaining differences."
    cover = replace_once(cover, old, new, "cover opening")
    cover = sub_once(
        cover,
        r"Independent natural evidence now strengthens the first question without being used to validate the finite mechanisms\..*?remain bounded finite-model findings\.",
        "A separately protocol-locked five-cluster natural synthesis is now treated as bounded external-consistency evidence rather than a load-bearing result of this Article. Its source-supported paired-dependence analysis gives Fisher `p=0.0121`, but omitting *Serapias* gives `p=0.1819`; a zero-covariance sensitivity gives `p=0.0386`, whereas a covariance-free certification bound gives `p=0.2806`. The first locked natural prospective transfer of the specific strongest-refuge predictor also remained null after contemporaneous marginals (`delta NLL M1-M0=-0.0003211`, 95% CI `-0.0009825` to `+0.0003422`). We therefore use natural evidence only to define external consistency and portability boundaries; sorting, buffering, recoupling, density feedback and warning performance remain finite-model findings.",
        "cover natural paragraph",
    )
    assert "p=0.00621" not in cover
    assert "three primary" not in cover
    return cover


def update_metadata(meta: str) -> str:
    meta = meta.replace("1. EGC exact interaction-state geometry + fresh fixed-area fragmentation gradient.", "1. Canonical interaction-state geometry + fresh fixed-area fragmentation gradient.", 1)
    meta = meta.replace("2. EGWE transition-sufficiency counterexample + original locked propagation experiment.", "2. Matched-marginal transition-sufficiency counterexample + original locked propagation experiment.", 1)
    meta = sub_once(
        meta,
        r"### Independent natural Q1 evidence\n\n.*?\n\n### Natural Q2 portability boundary",
        "### Bounded natural external-consistency evidence\n\nEGWEE contributes five independent primary fragmented-versus-reference programme/study clusters / 17 marginal Hedges-g effects, with ML015 retained separately as Fisher-z gradient generalisation evidence. Under the source-supported paired-dependence reconstruction, the five-cluster global intersection test gives Fisher `X=22.6477`, `df=10`, `p=0.01212432`; omitting ML001 *Serapias* gives `p=0.18194353`. A zero-covariance working sensitivity gives `p=0.03860161`, whereas the covariance-free Cauchy–Schwarz certification bound gives `p=0.28061178`. The natural result is therefore conditional state separation, materially ML001-dependent and not certifiable from marginal effects alone. It is Discussion-level external-consistency evidence, not a load-bearing NEE Result and not validation of the finite operators.\n\n### Natural Q2 portability boundary",
        "metadata natural Q1 block",
    )
    meta = meta.replace(
        "- natural Q1 state separation is independently supported by EGWEE; natural Q2 strongest-refuge portability is not established.",
        "- the completed EGWEE synthesis provides bounded external-consistency evidence only: its five-cluster rejection is ML001-dependent and is not covariance-free certified; natural Q2 strongest-refuge portability is not established.",
        1,
    )
    meta = meta.replace(
        "- natural data enter Results only through the completed EGWEE Question-1 state-separation synthesis;",
        "- natural data do not enter the main Results; the completed EGWEE synthesis appears only in Discussion as bounded external-consistency evidence with its influence and covariance limits;",
        1,
    )
    assert "three independent primary" not in meta
    assert "p=0.00621" not in meta
    return meta


def update_display(display: str) -> str:
    display = display.replace(
        "The four main figures remain focused on exact mathematics and locked finite-model mechanism. The completed EGWEE state-separation synthesis enters Question 1 as independent numerical evidence in text; it receives no new main-data panel, and the natural strongest-refuge null remains a Discussion portability boundary.",
        "The four main figures remain focused on exact mathematics and locked finite-model mechanism. The completed EGWEE synthesis is not a main Result and receives no main-data panel; its latest five-cluster result appears only in Discussion as bounded external-consistency evidence, while the natural strongest-refuge null remains a portability boundary.",
        1,
    )
    display = display.replace("Source: pinned EGC fixed-area fragmentation gradient.", "Source: pinned canonical fixed-area fragmentation gradient.", 1)
    display = display.replace(
        "15. EGWEE three-primary-cluster state-separation synthesis, evidence-role map and natural-Q2 strongest-refuge null boundary.",
        "15. EGWEE five-cluster state-separation synthesis, covariance-robustness boundary, evidence-role map and natural-Q2 strongest-refuge null boundary.",
        1,
    )
    return display


def update_manifest(manifest: dict) -> dict:
    manifest["schema_version"] = 9
    manifest["purpose"] = "Pin the evidence architecture for the four-operator Nature Ecology & Evolution flagship while keeping the completed natural state-separation synthesis as bounded, non-load-bearing external-consistency evidence."
    source = manifest["natural_state_separation_source"]
    source.update({
        "role": "bounded_external_consistency_evidence_not_load_bearing",
        "repository": "zuizui0223/egwee",
        "commit": EGWEE_COMMIT,
        "required_paths": [
            "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md",
            "manuscript/COVARIANCE_ROBUSTNESS_RESULT.md",
            "manuscript/tables/table_s2_covariance_robustness.csv",
            "manuscript/tables/table_s3_primary_marginal_effects.csv",
            "scripts/synthesize_state_separation.py",
            "scripts/check_covariance_robustness.py",
            "scripts/check_primary_effect_supplement.py",
            "evidence/meta_extraction/multilayer_cluster_registry_v1.csv",
            "evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv",
        ],
        "n_primary_effects": 17,
        "decision": "conditional_state_separation_under_source_supported_dependence",
        "claim_ceiling": "Five direct Hedges-g programme/study clusters reject the global intersection null under the frozen source-supported paired dependence reconstruction, but the result is materially ML001 Serapias-dependent and is not certifiable from marginal effects alone under the covariance-free Cauchy-Schwarz bound. ML015 remains separate Fisher-z gradient generalisation evidence. This natural synthesis is Discussion-level external-consistency evidence only and does not validate the finite NEE operators.",
        "n_independent_primary_clusters": 5,
        "primary_fisher_statistic": 22.64771647,
        "primary_fisher_df": 10,
        "primary_combined_p": 0.01212432410511315,
        "gradient_generalisation_cluster": "ML015",
        "gradient_generalisation_cluster_p": 0.00256953,
        "primary_leave_one_cluster_out": {
            "omit_ML001_combined_p": 0.18194352880824008,
            "omit_ML002_combined_p": 0.01276794,
            "omit_ML003_combined_p": 0.01407214,
            "omit_ML014_combined_p": 0.02116199,
            "omit_ML020_combined_p": 0.00384724,
            "influential_cluster_dependency_detected": True,
            "influential_cluster": "ML001",
        },
        "covariance_robustness": {
            "canonical_source_supported_p": 0.01212432,
            "zero_covariance_p": 0.03860161,
            "cauchy_schwarz_covariance_free_bound_p": 0.28061178,
            "zero_covariance_omit_ML001_p": 0.57123438,
            "covariance_free_bound_omit_ML001_p": 0.92060125,
        },
    })
    firewalls = manifest["claim_firewalls"]
    firewalls[0] = "EGWEE is bounded Discussion-level external-consistency evidence for natural Q1 and is not load-bearing for the finite Question-1 demonstration or any simulator/mechanism claim."
    if not any("covariance-free" in x for x in firewalls):
        firewalls.insert(1, "The completed natural state-separation synthesis is not covariance-free certified: its Cauchy-Schwarz certification bound does not reject the global intersection null.")
    return manifest


def update_checker(checker: str) -> str:
    old_natural = '''    for token in ("Fisher chi-square(6)=18.01", "p=0.00621", "p=0.00257", "delta NLL M1-M0=-0.0003211"):\n        assert token in article, token\n\n    # Natural data may now enter Results only through the completed EGWEE Q1 synthesis.\n    for token in (\n        "Crepis", "Miyake", "Zosterops", "Conospermum",\n        "Honshu", "Zurich", "Toronto", "Oenothera", "Eschscholzia",\n        "Mallorca", "Campanula americana",\n    ):\n        assert token not in results, f"non-Q1 natural projection leaked into Results: {token}"\n    for token in ("Serapias", "Brosimum", "Spondias", "Eucalyptus wandoo", "p=0.00621", "p=0.00257"):\n        assert token in results, f"natural Q1 synthesis missing from Results: {token}"\n    # Qualitative natural anchors are superseded in the flagship by the formal EGWEE Q1 synthesis.\n    for token in ("Serapias", "Brosimum", "Spondias", "Eucalyptus wandoo"):\n        assert token in results or token in article[: article.index("## Results")], token\n'''
    new_natural = '''    # Natural evidence is intentionally non-load-bearing in the flagship.\n    # Latest EGWEE values must appear only in Discussion with their influence\n    # and covariance limitations; the older three-cluster values are forbidden.\n    for token in ("p=0.0121", "p=0.1819", "p=0.0386", "p=0.2806", "delta NLL M1-M0=-0.0003211"):\n        assert token in discussion, token\n    for token in ("Serapias", "0.0121", "0.1819", "0.0386", "0.2806"):\n        assert token not in results, f"bounded natural evidence leaked into Results: {token}"\n    for token in ("p=0.00621", "Fisher chi-square(6)=18.01", "three-system natural evidence"):\n        assert token not in article, f"stale EGWEE claim survived: {token}"\n    for token in (\n        "Generality differs for counterexamples and positive mechanisms",\n        "Provenance of Question 1",\n        "bounded external-consistency evidence",\n    ):\n        assert token in article, token\n    assert "Using the EGC theorem" not in article\n    assert "Using EGWE" not in article\n'''
    checker = replace_once(checker, old_natural, new_natural, "checker natural-role block")

    checker = checker.replace('assert manifest["schema_version"] == 8', 'assert manifest["schema_version"] == 9', 1)
    old_manifest = '''    natural_q1 = manifest["natural_state_separation_source"]\n    assert natural_q1["decision"] == "reject_primary_binary_layer_exchangeability_with_separate_gradient_support"\n    assert natural_q1["n_independent_primary_clusters"] == 3\n    assert natural_q1["n_primary_effects"] == 9\n    assert abs(natural_q1["primary_combined_p"] - 0.00621) < 1e-12\n    assert abs(natural_q1["gradient_generalisation_cluster_p"] - 0.00256953) < 1e-12\n    loo = natural_q1["primary_leave_one_cluster_out"]\n    assert loo["influential_cluster_dependency_detected"] is True\n    assert loo["influential_cluster"] == "ML001"\n    assert abs(loo["omit_ML001_combined_p"] - 0.15119208) < 1e-8\n    assert "omitting ML001" in article\n    assert "p=0.151" in article\n'''
    new_manifest = '''    natural_q1 = manifest["natural_state_separation_source"]\n    assert natural_q1["role"] == "bounded_external_consistency_evidence_not_load_bearing"\n    assert natural_q1["commit"] == "16308cf6d6e4aec274504ba81bbf6e71be465099"\n    assert natural_q1["decision"] == "conditional_state_separation_under_source_supported_dependence"\n    assert natural_q1["n_independent_primary_clusters"] == 5\n    assert natural_q1["n_primary_effects"] == 17\n    assert abs(natural_q1["primary_combined_p"] - 0.01212432410511315) < 1e-12\n    assert abs(natural_q1["gradient_generalisation_cluster_p"] - 0.00256953) < 1e-12\n    loo = natural_q1["primary_leave_one_cluster_out"]\n    assert loo["influential_cluster_dependency_detected"] is True\n    assert loo["influential_cluster"] == "ML001"\n    assert abs(loo["omit_ML001_combined_p"] - 0.18194352880824008) < 1e-12\n    cov = natural_q1["covariance_robustness"]\n    assert abs(cov["zero_covariance_p"] - 0.03860161) < 1e-10\n    assert abs(cov["cauchy_schwarz_covariance_free_bound_p"] - 0.28061178) < 1e-10\n'''
    checker = replace_once(checker, old_manifest, new_manifest, "checker natural manifest block")
    return checker


def update_workflow(workflow: str) -> str:
    workflow = workflow.replace(
        "ref: 74d5336242bfaa4ccbbf54f0343c8d058c161d79",
        f"ref: {EGWEE_COMMIT}",
        1,
    )
    workflow = workflow.replace(
        "'zuizui0223/egwee': (Path('egwee_source'),'74d5336242bfaa4ccbbf54f0343c8d058c161d79'),",
        f"'zuizui0223/egwee': (Path('egwee_source'),'{EGWEE_COMMIT}'),",
        1,
    )
    old = '''          source=manifest['natural_state_separation_source']\n          root, expected=roots[source['repository']]\n          got=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()\n          assert got==expected,(source['repository'],got,expected)\n          assert source['commit']==expected\n          for rel in source['required_paths']:\n            assert (root/rel).is_file(), f"missing {source['repository']}:{rel}"\n          assert manifest['natural_q2_boundary']['status']=='no_detected_incremental_strongest_refuge_information'\n          print('Pinned scientific sources + EGWEE natural Q1 + locked route-reserve evidence: PASS')\n'''
    new = '''          source=manifest['natural_state_separation_source']\n          root, expected=roots[source['repository']]\n          got=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()\n          assert got==expected,(source['repository'],got,expected)\n          assert source['commit']==expected\n          for rel in source['required_paths']:\n            assert (root/rel).is_file(), f"missing {source['repository']}:{rel}"\n\n          # Re-run the pinned upstream canonical synthesis rather than merely\n          # confirming that an old commit still exists.\n          raw=subprocess.check_output(['python','scripts/synthesize_state_separation.py'],cwd=root,text=True)\n          line=next(x for x in raw.splitlines() if x.startswith('EGWEE_STATE_SEPARATION '))\n          observed=json.loads(line.split(' ',1)[1])\n          assert observed['n_primary_independent_clusters']==source['n_independent_primary_clusters']\n          assert observed['n_primary_effects']==source['n_primary_effects']\n          assert abs(observed['primary_fisher_statistic']-source['primary_fisher_statistic']) < 1e-8\n          assert observed['primary_fisher_df']==source['primary_fisher_df']\n          assert abs(observed['primary_combined_p']-source['primary_combined_p']) < 1e-12\n          loo={x['dropped_cluster']:x['combined_p'] for x in observed['primary_leave_one_cluster_out']}\n          assert abs(loo['ML001']-source['primary_leave_one_cluster_out']['omit_ML001_combined_p']) < 1e-12\n\n          raw_cov=subprocess.check_output(['python','scripts/check_covariance_robustness.py'],cwd=root,text=True)\n          cov_line=next(x for x in raw_cov.splitlines() if x.startswith('COVARIANCE_ROBUSTNESS '))\n          observed_cov=json.loads(cov_line.split(' ',1)[1])\n          declared=source['covariance_robustness']\n          assert abs(observed_cov['zero_covariance']['fisher_p']-declared['zero_covariance_p']) < 5e-8\n          assert abs(observed_cov['cauchy_schwarz_certification_bound']['fisher_p']-declared['cauchy_schwarz_covariance_free_bound_p']) < 5e-8\n          assert abs(observed_cov['zero_covariance']['leave_one_out_p']['ML001']-declared['zero_covariance_omit_ML001_p']) < 5e-8\n          assert abs(observed_cov['cauchy_schwarz_certification_bound']['leave_one_out_p']['ML001']-declared['covariance_free_bound_omit_ML001_p']) < 5e-8\n\n          assert manifest['natural_q2_boundary']['status']=='no_detected_incremental_strongest_refuge_information'\n          print('Pinned scientific sources + re-executed EGWEE natural boundary + locked route-reserve evidence: PASS')\n'''
    workflow = replace_once(workflow, old, new, "workflow EGWEE verifier")

    old_copy = '''          cp egwee_source/manuscript/STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-13.md nee_packet/provenance/egwee_state_separation_result.md\n          cp egwee_source/manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-13_STATE_SEPARATION_SYNTHESIS.md nee_packet/provenance/egwee_state_separation_protocol.md\n          cp egwee_source/evidence/meta_extraction/multilayer_cluster_registry_v1.csv nee_packet/provenance/egwee_multilayer_cluster_registry.csv\n'''
    new_copy = '''          cp egwee_source/manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md nee_packet/provenance/egwee_state_separation_manuscript.md\n          cp egwee_source/manuscript/COVARIANCE_ROBUSTNESS_RESULT.md nee_packet/provenance/egwee_covariance_robustness_result.md\n          cp egwee_source/manuscript/tables/table_s2_covariance_robustness.csv nee_packet/provenance/egwee_covariance_robustness_table.csv\n          cp egwee_source/manuscript/tables/table_s3_primary_marginal_effects.csv nee_packet/provenance/egwee_primary_marginal_effects.csv\n          cp egwee_source/scripts/synthesize_state_separation.py nee_packet/provenance/egwee_synthesize_state_separation.py\n          cp egwee_source/scripts/check_covariance_robustness.py nee_packet/provenance/egwee_check_covariance_robustness.py\n          cp egwee_source/evidence/meta_extraction/multilayer_cluster_registry_v1.csv nee_packet/provenance/egwee_multilayer_cluster_registry.csv\n          cp egwee_source/evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv nee_packet/provenance/egwee_multilayer_cluster_registry_extension_ml020.csv\n'''
    workflow = replace_once(workflow, old_copy, new_copy, "workflow packet copy")
    return workflow


def main() -> None:
    article = update_article(ARTICLE.read_text(encoding="utf-8"))
    cover = update_cover(COVER.read_text(encoding="utf-8"))
    meta = update_metadata(META.read_text(encoding="utf-8"))
    display = update_display(DISPLAY.read_text(encoding="utf-8"))
    manifest = update_manifest(json.loads(MANIFEST.read_text(encoding="utf-8")))
    checker = update_checker(CHECKER.read_text(encoding="utf-8"))
    workflow = update_workflow(WORKFLOW.read_text(encoding="utf-8"))

    ARTICLE.write_text(article, encoding="utf-8")
    COVER.write_text(cover, encoding="utf-8")
    META.write_text(meta, encoding="utf-8")
    DISPLAY.write_text(display, encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CHECKER.write_text(checker, encoding="utf-8")
    WORKFLOW.write_text(workflow, encoding="utf-8")

    print("Applied NEE/EGWEE claim-ownership separation and upstream synchronization")


if __name__ == "__main__":
    main()
