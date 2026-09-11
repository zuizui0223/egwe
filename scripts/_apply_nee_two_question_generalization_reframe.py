from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "manuscript/nee_flagship_article.md"
COVER = ROOT / "manuscript/nee_flagship_cover_letter.md"
META = ROOT / "manuscript/nee_flagship_submission_metadata.md"
DISPLAY = ROOT / "manuscript/nee_flagship_display_plan.md"
CHECKER = ROOT / "scripts/check_nee_flagship_compliance.py"

OLD_TITLE = "Eco-genetic sorting and buffering shape functional vulnerability under fragmentation"
NEW_TITLE = "Fragmentation does not generate a single biological state, and local coupling shapes functional fate"

NEW_ABSTRACT = """Fragmentation is often treated as a single gradient of biological deterioration, yet ecological and genetic layers need not move together. In a finite eco-genetic model, subdividing fixed area eliminated potential high-trait viability in 1,037/1,037 cases at every tested subdivision while realised occupancy remained 99.6–100%; realised high-trait mass declined and then partially recovered at high subdivision. We then asked what determines divergent futures once state separation occurs. Constructive matched-marginal states showed that conventional ecological and genetic marginals are not transition-sufficient. Prospectively locked interventions resolved q-dependent allele sorting, recruitment buffering, direct recoupling and a density-mediated collapse gate. Marginal diversity thresholds preceded every observed loss yet had specificity 0, showing that temporal precedence need not imply fate discrimination. By contrast, continuous strongest-refuge reserve added ranking information beyond co-timed maximum interaction state (AUC difference +0.02135, 95% CI +0.01770,+0.02501). Fragmentation therefore need not generate one biological state, and functional fate depends on cross-layer organization, life-cycle operators and remaining local reserve. Numerical thresholds, effect sizes and horizons are closure-specific."""

NEW_ROADMAP = """We organize the paper around two biological questions. **Question 1 asks whether fragmentation produces one biological deterioration state.** We derive the canonical interaction-state geometry and test a fixed-area fragmentation gradient in which potential viability, realised occupancy, interaction support, demography and trait state can separate. **Question 2 asks what determines divergent futures once that separation is acknowledged.** We construct matched-marginal states, identify hidden cross-layer organization that changes exact transitions, intervene on life-cycle operators responsible for sorting, buffering, recoupling and collapse entry, and distinguish stress sensitivity from fate information using the continuous reserve of the strongest remaining local refuge. The two questions form one argument: fragmentation first separates biological layers, then local organization and life-cycle operators determine how that separation is propagated into fate."""

DISCUSSION_OPEN = """Fragmentation did not generate one biological deterioration state in this model family. Potential high-trait viability disappeared under every tested subdivision while realised occupancy remained nearly complete, and interaction, demography and realised trait mass followed distinct, partly non-monotonic trajectories. This is the central result of Question 1: habitat subdivision can separate biological layers before demographic disappearance, so fragmentation intensity cannot by itself stand in for biological state.

Question 2 asks what then determines fate. The matched-marginal counterexample shows that conventional marginal summaries can be identical while exact next transitions differ, and the intervention programme resolves how q-dependent sorting, recruitment buffering, direct recoupling and density feedback transform that hidden organization through time. The monitoring result is a consequence of the same architecture: fate-relevant information is retained in the depth of the strongest remaining local reserve beyond what is carried by a co-timed interaction maximum."""

PREDICTION_PARAGRAPH = """These finite results make two testable natural-system predictions rather than claims of external validation. First, responses to fragmentation should differ systematically among demographic/resource, interaction, movement, reproductive and genetic layers in magnitude or timing. Second, that discordance should covary with independently measured processes such as movement-mediated compensation, reproductive assurance, pollination mode and cohort or landscape history. The four natural systems used here define archetypes for those tests: *Crepis sancta* represents uncompensated interaction limitation; Miyake-jima *Camellia–Zosterops* movement-mediated compensation; *Conospermum undulatum* contemporary-process deterioration with adult-genetic lag; and *Spondias purpurea* coordinated multilayer deterioration. A separately protocol-locked multilayer meta-analysis is testing these predictions. Until that synthesis is complete, these systems are mechanistic projections, not validation data for the finite model."""

GENERALITY_SECTION = """### Generality differs for counterexamples and positive mechanisms

Two kinds of result require different claim ceilings. The transition-sufficiency result is constructive: if two admissible states share the declared marginal representation but have different exact transitions, then those marginals cannot be universally sufficient for every system admitted by that representation. Likewise, temporal precedence does not logically entail fate discrimination, because sensitivity 1 and specificity 0 can coexist. These are **non-implication results**. Their force does not depend on the numerical values `0.2543`, `q*=0.625` or any particular generation generalizing to nature.

The positive mechanism results have a narrower ceiling. The operator weights, switch value, intervention effect sizes, route-margin coefficients, generation horizons and absolute warning AUC belong to the declared finite closure. They show how one biologically motivated system realizes state separation and fate divergence; they do not establish universal natural sorting, buffering, recoupling, density thresholds or warning performance. The nontrivial predictive comparison is therefore the **incremental information beyond a co-timed summary**—the prospectively locked route margin exceeded co-timed maximum q by `+0.02135` AUC—rather than the absolute AUC as a portable performance benchmark."""

METHODS_PROVENANCE = """### Provenance of Question 1

Question 1 incorporates the canonical interaction map and fixed-area fragmentation programme historically developed in the repository `zuizui0223/eco-genetic-criticality`. That material is unpublished and has no separate active submission; it is part of the present study. The exact fixed-point geometry and fragmentation-gradient evidence are presented in this manuscript and pinned to source commit `b7ee738767c92307d6d23a85a3eeb857faf6ddfb` in the evidence manifest. The historical repository label is provenance, not a separate theory invoked without presentation here."""


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly one match, got {n}"
    return text.replace(old, new, 1)


def main() -> None:
    article = ARTICLE.read_text(encoding="utf-8")
    cover = COVER.read_text(encoding="utf-8")
    meta = META.read_text(encoding="utf-8")
    display = DISPLAY.read_text(encoding="utf-8")
    checker = CHECKER.read_text(encoding="utf-8")

    article = replace_once(article, f"# {OLD_TITLE}\n", f"# {NEW_TITLE}\n", "article title")
    cover = cover.replace(OLD_TITLE, NEW_TITLE)
    meta = replace_once(meta, f"- **Title:** {OLD_TITLE}", f"- **Title:** {NEW_TITLE}", "metadata title")
    checker = replace_once(checker, f'title = "{OLD_TITLE}"', f'title = "{NEW_TITLE}"', "checker title")

    m = re.search(r"(?s)(## Abstract\n\n)(.*?)(\n\nEcological fragmentation changes more than habitat amount\.)", article)
    assert m, "abstract anchor not found"
    article = article[:m.start(2)] + NEW_ABSTRACT + article[m.end(2):]

    m = re.search(r"(?s)We organize the paper around two biological questions\..*?Natural examples return only in the Discussion as projections of these mechanisms\.", article)
    assert m, "roadmap paragraph not found"
    article = article[:m.start()] + NEW_ROADMAP + article[m.end():]

    article = replace_once(article, "The parent framework begins with the canonical interaction map", "Question 1 begins with the canonical interaction map", "Q1 ownership")

    m = re.search(r"(?s)(## Discussion\n\n)(.*?)(\n\n)", article)
    assert m, "Discussion opening not found"
    article = article[:m.start(2)] + DISCUSSION_OPEN + article[m.end(2):]

    m = re.search(r"(?s)(Monitoring follows the same principle\..*?)(\n\n)", article)
    assert m, "monitoring paragraph not found"
    article = article[:m.end(1)] + "\n\n" + PREDICTION_PARAGRAPH + article[m.end(1):]

    assert "### Generality differs for counterexamples and positive mechanisms" not in article
    article = article.replace("\n## Methods\n", "\n\n" + GENERALITY_SECTION + "\n\n## Methods\n", 1)
    article = article.replace("## Methods\n", "## Methods\n\n" + METHODS_PROVENANCE + "\n", 1)

    old_ceiling = "## Claim ceilings\n\n- q-dependent allele sorting is not asserted as a universal natural mechanism."
    new_ceiling = """## Claim ceilings\n\n### Logical non-implication claims\n\n- the matched-marginal construction is a constructive counterexample to universal sufficiency of the declared marginal representation; its logic does not require the model-specific numerical transition difference to generalize to nature.\n- temporal precedence does not imply fate discrimination: sensitivity 1 can coexist with specificity 0. This is a non-implication result, not a universal natural threshold claim.\n\n### Closure-specific positive mechanism claims\n\n- q-dependent allele sorting is not asserted as a universal natural mechanism."""
    meta = replace_once(meta, old_ceiling, new_ceiling, "metadata claim ceiling split")
    meta = meta.replace(
        "- last-refuge warning AUC, observation generation and route-margin weights are finite-closure results, not universal natural warning performance or thresholds.",
        "- absolute last-refuge warning AUC, observation generation and route-margin weights are finite-closure results, not universal natural warning performance or thresholds; the main comparative claim is the prospectively locked incremental ranking beyond co-timed max q."
    )
    meta = meta.replace(
        "- natural examples remain Discussion-level projections only.",
        "- natural examples remain Discussion-level projections only; a separate protocol-locked multilayer meta-analysis tests the predicted cross-layer discordance and moderators without contributing validation claims to the present paper yet."
    )

    display = display.replace(
        "# NEE flagship display plan — four-operator mechanism",
        "# NEE flagship display plan — two questions, one causal argument"
    )
    display = display.replace(
        "## Figure 2 — Fragmentation separates functional support from persistence",
        "## Figure 2 — Question 1: fragmentation does not generate one biological deterioration state"
    )
    display = display.replace(
        "- route-margin AUC **0.92734** `[0.92433,0.93035]`;\n- co-timed max-q AUC **0.90598** `[0.90078,0.91118]`;\n- predeclared lower-is-higher-risk `H_alpha` comparator AUC **0.23253** (directionally inverted; no post-hoc sign rescue);\n- paired AUC gain **+0.02135** `[+0.01770,+0.02501]`;",
        "- **primary comparison:** paired route-margin minus co-timed max-q AUC gain **+0.02135** `[+0.01770,+0.02501]`;\n- absolute route-margin AUC **0.92734** `[0.92433,0.93035]` and max-q AUC **0.90598** `[0.90078,0.91118]` are closure-specific diagnostics;\n- predeclared lower-is-higher-risk `H_alpha` comparator AUC **0.23253** (directionally inverted; no post-hoc sign rescue);"
    )

    old_cover = "Fragmentation ecology often tracks habitat geometry, abundance, interactions and genetic diversity as separate indicators of deterioration. Our study asks a mechanistic question: **why can systems retaining the same marginal ecological and genetic quantities nevertheless reach different functional outcomes?** We combine exact results with prospectively locked intervention experiments to identify the life-cycle operators that sort, buffer, recouple and amplify those differences."
    new_cover = "Fragmentation is often treated as a single gradient of biological deterioration. Our study asks two linked questions: **does fragmentation actually generate one biological state, and, once biological layers separate, what determines their divergent functional futures?** We combine an exact fragmentation-state analysis, a constructive transition-sufficiency counterexample and prospectively locked intervention experiments to identify what is logically insufficient and which life-cycle operators sort, buffer, recouple and amplify the remaining differences."
    cover = replace_once(cover, old_cover, new_cover, "cover opening")

    insert = '''\n    for token in (\n        "Question 1 — Does fragmentation produce one biological deterioration state?",\n        "Generality differs for counterexamples and positive mechanisms",\n        "non-implication results",\n        "AUC difference +0.02135",\n        "protocol-locked multilayer meta-analysis",\n        "Provenance of Question 1",\n    ):\n        assert token in article, token\n    assert "Using the EGC theorem" not in article\n    assert "Using EGWE" not in article\n'''
    anchor = '    assert abstract_n <= 200, abstract_n\n'
    assert anchor in checker
    checker = checker.replace(anchor, anchor + insert, 1)

    ARTICLE.write_text(article, encoding="utf-8")
    COVER.write_text(cover, encoding="utf-8")
    META.write_text(meta, encoding="utf-8")
    DISPLAY.write_text(display, encoding="utf-8")
    CHECKER.write_text(checker, encoding="utf-8")

    print("Applied NEE two-question/generalization reframe")


if __name__ == "__main__":
    main()
