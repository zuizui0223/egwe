from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "manuscript/publication_lanes.json"
PUBLIC = ROOT / "manuscript/PUBLICATION_LANES.md"
README = ROOT / "README.md"
MREADME = ROOT / "manuscript/README.md"
OLD_STATUS = ROOT / "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md"
NEW_STATUS = ROOT / "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-16.md"
META = ROOT / "manuscript/nee_flagship_submission_metadata.md"
STORY = ROOT / "manuscript/main_story_revision.md"
VALIDATOR = ROOT / "scripts/validate_publication_lanes.py"
TEST = ROOT / "tests/test_publication_governance.py"

EGWEE_COMMIT = "16308cf6d6e4aec274504ba81bbf6e71be465099"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected 1 match, got {n}"
    return text.replace(old, new, 1)


def main() -> None:
    registry = json.loads(ROUTER.read_text(encoding="utf-8"))
    assert registry["schema_version"] == 5
    registry["schema_version"] = 6

    flagship = registry["active_lanes"]["nee_flagship"]
    flagship["claim_ceiling"] = (
        "All operator, route-margin, headroom and AUC results are finite-closure results. "
        "The completed EGWEE synthesis appears only as bounded Discussion-level external-consistency evidence; "
        "its paired-dependence global rejection is ML001-dependent and not covariance-free certified, and it does not validate any finite operator."
    )
    flagship["natural_evidence_role"] = "bounded_discussion_external_consistency_not_load_bearing"

    egwee_layer = next(x for x in registry["series_decomposition"]["layers"] if x["layer"] == "EGWEE")
    egwee_layer["current_role"] = (
        "independent_empirical_owner_Journal_of_Ecology_submission_ready_except_author_metadata; "
        "NEE_uses_only_bounded_Discussion_external_consistency"
    )

    empirical = registry["independent_development_programs"]["empirical_multilayer_meta_analysis"]
    empirical.update({
        "repository_commit": EGWEE_COMMIT,
        "status": "submission_ready_pending_author_metadata",
        "publication_structure": "targeted_protocol_first_cluster_synthesis",
        "final_target": "Journal of Ecology",
        "submission_package_state": "ready_except_author_metadata",
        "primary_direct_clusters": 5,
        "primary_marginal_effects": 17,
        "primary_fisher_p": 0.01212432,
        "omit_ML001_p": 0.18194353,
        "zero_covariance_p": 0.03860161,
        "covariance_free_bound_p": 0.28061178,
        "gradient_generalisation_cluster": "ML015",
        "claim_ceiling": (
            "The completed natural synthesis supports conditional state separation under source-supported paired dependence, "
            "not a universal fragmentation syndrome. The five-cluster result is materially ML001-dependent and is not covariance-free certified; "
            "the targeted recovery universe does not estimate global prevalence. ML015 remains a separate Fisher-z gradient generalisation family."
        ),
    })
    empirical["owned_claims"] = [
        "natural_cross_layer_fragmentation_state_separation",
        "influential_cluster_sensitivity",
        "within_cluster_covariance_robustness_boundary",
        "concordant_multilayer_deterioration_without_detected_separation",
    ]
    ROUTER.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    public = PUBLIC.read_text(encoding="utf-8")
    public = replace_once(
        public,
        "- **Two-question spine:** **Q1 (EGC)** asks whether fragmentation produces one biological deterioration state; **Q2 (EGWE)** asks what hidden organization and life-cycle operators determine divergent futures and what continuous reserve carries fate information.",
        "- **Two-question spine:** **Q1** asks whether fragmentation produces one biological deterioration state; **Q2** asks what hidden organization and life-cycle operators determine divergent futures and what continuous reserve carries fate information. The historical EGC/EGWE labels are provenance, not separate evidentiary authorities invoked by the manuscript.",
        "public two-question spine",
    )
    public = replace_once(
        public,
        "All operator, route-margin, headroom and warning-performance results are bounded to the declared finite closure. Natural systems remain projection/measurement examples. The flagship does not establish a universal natural warning variable, universal eco-genetic threshold, natural causal mechanism, or portability across taxa and landscapes.",
        "All operator, route-margin, headroom and warning-performance results are bounded to the declared finite closure. The completed EGWEE synthesis appears only as bounded Discussion-level external-consistency evidence: its five-cluster paired-dependence result is ML001-dependent and is not covariance-free certified. It does not validate a finite operator, universal natural warning variable, universal eco-genetic threshold, natural causal mechanism, or portability across taxa and landscapes.",
        "public claim ceiling",
    )
    public = replace_once(
        public,
        "- **scientific decomposition inside the flagship:** **Q1 = EGC state separation**; **Q2 = EGWE representation → operators → warning/reserve**; EGWEE remains the downstream natural measurement programme;",
        "- **scientific decomposition inside the flagship:** **Q1 = finite state separation**; **Q2 = representation → operators → warning/reserve**; historical EGC/EGWE labels are provenance, while EGWEE independently owns the natural empirical synthesis and enters NEE only as bounded Discussion-level external consistency;",
        "public decomposition",
    )
    public = replace_once(
        public,
        "| EGWEE | do natural fragmentation effects separate across interaction, movement, reproduction and genetic layers, and what explains the discordance? | `zuizui0223/egwee` multilayer meta-analysis | **independent empirical synthesis; three-primary-cluster state-separation result complete; ML015 separate gradient support** |",
        "| EGWEE | do natural fragmentation effects separate across interaction, movement, reproduction and genetic layers, and what explains the discordance? | `zuizui0223/egwee` Journal of Ecology package | **5 primary clusters / 17 marginal effects; conditional state separation; submission-ready except author metadata; ML015 separate gradient support** |",
        "public EGWEE row",
    )
    anchor = "\n## Independent development lane — operator portability\n"
    assert anchor in public
    egwee_section = """
## Independent empirical lane — EGWEE

- **Authoritative repository:** `zuizui0223/egwee` at scientific/submission commit `16308cf6d6e4aec274504ba81bbf6e71be465099`.
- **Target:** ***Journal of Ecology***, Research Article.
- **State:** **submission-ready except author metadata / declarations**; anonymous manuscript, supplementary material and anonymous code/data package have been generated and QA-checked.
- **Primary denominator:** **5 independent programme/study clusters / 17 marginal Hedges-g effects**. ML020 is retained as one programme cluster despite `p=1.0`; ML015 remains a separate Fisher-z gradient generalisation family.
- **Current primary result:** source-supported paired-dependence Fisher `p=0.01212432`; omit-ML001 *Serapias* `p=0.18194353`.
- **Dependence boundary:** zero-covariance sensitivity `p=0.03860161`; covariance-free Cauchy–Schwarz certification bound `p=0.28061178`.
- **Claim ceiling:** **conditional state separation**, materially ML001-dependent and not covariance-free certified. The targeted recovery universe does not estimate the global prevalence of separated systems.
- **Ownership firewall:** EGWEE owns the natural empirical existence/robustness claim. NEE cites this result only in Discussion as bounded external-consistency evidence and does not use it to validate finite sorting, buffering, recoupling, density-gate or warning mechanisms.

"""
    public = public.replace(anchor, "\n" + egwee_section + anchor, 1)
    PUBLIC.write_text(public, encoding="utf-8")

    root_readme = README.read_text(encoding="utf-8")
    root_readme = root_readme.replace("EG_SERIES_SUBMISSION_STATUS_2026-09-08.md", "EG_SERIES_SUBMISSION_STATUS_2026-09-16.md")
    root_readme = replace_once(
        root_readme,
        "| EGWEE | do natural fragmentation responses separate across biological layers, and which process/cohort moderators explain discordance? | `zuizui0223/egwee` | **empirical multilevel synthesis complete for the three-primary-cluster result with separate ML015 gradient support** |",
        "| EGWEE | do natural fragmentation responses separate across biological layers, and which process/cohort moderators explain discordance? | `zuizui0223/egwee` | **Journal of Ecology package ready except author metadata; 5 primary clusters / 17 effects; conditional state separation; ML015 separate gradient support** |",
        "root README EGWEE row",
    )
    route_anchor = "The binding machine router is [`manuscript/publication_lanes.json`](manuscript/publication_lanes.json); the human-readable contract is [`manuscript/PUBLICATION_LANES.md`](manuscript/PUBLICATION_LANES.md); the current operational status is [`manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-16.md`](manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-16.md)."
    assert route_anchor in root_readme
    root_readme = root_readme.replace(
        route_anchor,
        route_anchor + "\n\nEGWEE is a separate empirical submission lane rather than a load-bearing NEE Result: the completed five-cluster synthesis is targeted to *Journal of Ecology* and enters the NEE flagship only as bounded Discussion-level external-consistency evidence.",
        1,
    )
    README.write_text(root_readme, encoding="utf-8")

    mreadme = MREADME.read_text(encoding="utf-8")
    mreadme = mreadme.replace("EG_SERIES_SUBMISSION_STATUS_2026-09-08.md", "EG_SERIES_SUBMISSION_STATUS_2026-09-16.md")
    mreadme = replace_once(
        mreadme,
        "| EGWEE | empirical cross-layer fragmentation response / process moderators | **multilevel meta-analysis in `zuizui0223/egwee`; three-primary-cluster state-separation synthesis complete; ML015 separate gradient support** |",
        "| EGWEE | empirical cross-layer fragmentation response / process moderators | **Journal of Ecology package in `zuizui0223/egwee`; 5 primary clusters / 17 effects; conditional state separation; ready except author metadata; ML015 separate gradient support** |",
        "manuscript README EGWEE row",
    )
    MREADME.write_text(mreadme, encoding="utf-8")

    old = OLD_STATUS.read_text(encoding="utf-8")
    assert not old.startswith("# SUPERSEDED")
    OLD_STATUS.write_text(
        "# SUPERSEDED — historical status only\n\n"
        "> This 2026-09-08 operational state is superseded by `EG_SERIES_SUBMISSION_STATUS_2026-09-16.md`, after the completed five-cluster EGWEE synthesis was separated from NEE Results and routed independently to Journal of Ecology. Use the 2026-09-16 file for current submission decisions.\n\n"
        + old,
        encoding="utf-8",
    )

    status = """# EG-series submission status — 2026-09-16

This file is the current **operational submission-status source of truth**. It supersedes `EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`; earlier status files remain historical provenance only.

## Decision now in force

There is one active **EGWE** submission lane: the Nature Ecology & Evolution flagship `manuscript/nee_flagship_article.md`. The standalone EGWE state-validity and warning-validity manuscripts remain frozen fallbacks and cannot be submitted simultaneously with the flagship.

EGWEE is now a **separate empirical submission lane**, not load-bearing evidence inside the NEE Results. PR #184 (merge commit `1603ae26103510b9f7b0c2c7030a9dccd9c54897`) removed the stale three-cluster natural result from the NEE Abstract/Results, moved the completed natural synthesis to Discussion as bounded external-consistency evidence, and made NEE CI re-execute the pinned EGWEE canonical synthesis and covariance-robustness checks.

## Current route

| component | repository | current status | submission role |
|---|---|---|---|
| EGC provenance | `zuizui0223/eco-genetic-criticality` | finite Question-1 source material | absorbed into NEE Question 1; no separate active submission |
| EGWE NEE flagship | `zuizui0223/egwe` | **active primary submission** | **Nature Ecology & Evolution** |
| EGWE state validity | `zuizui0223/egwe` | **frozen fallback** | reactivate only after flagship is no longer under consideration and overlap is resolved |
| EGWE operator portability | `zuizui0223/egwe` | **package-ready development candidate; not yet authorised for submission** | independent Short Communication candidate; author/policy gate remains |
| EGWE warning validity | `zuizui0223/egwe` | **frozen fallback; later holdout evidence required on reactivation** | no simultaneous submission with flagship |
| EGWEE multilayer fragmentation synthesis | `zuizui0223/egwee` | **submission-ready except author metadata/declarations** | **Journal of Ecology**, independent empirical paper |

## EGWEE state now frozen for routing

Authoritative EGWEE submission/scientific commit: `16308cf6d6e4aec274504ba81bbf6e71be465099`.

- primary direct family: **5 independent programme/study clusters / 17 marginal Hedges-g effects**;
- canonical paired-dependence Fisher: `p=0.01212432`;
- omit ML001 *Serapias*: `p=0.18194353`;
- zero-covariance sensitivity: `p=0.03860161`;
- covariance-free Cauchy–Schwarz certification bound: `p=0.28061178`;
- ML020 is retained as one programme cluster with `p=1.0` rather than dropped for weakening the combined result;
- ML015 remains a separate Fisher-z gradient generalisation family.

The empirical claim ceiling is **conditional state separation**. It is materially ML001-dependent, is not covariance-free certified, does not estimate the global prevalence of state separation, and does not validate the finite NEE operators.

No sixth-cluster search is authorised merely to restore stronger significance.

## NEE / EGWEE ownership after separation

**NEE owns:** constructive failure of one-state/marginal representations under the declared finite closure; exact transition insufficiency; q-dependent sorting, recruitment buffering, direct recoupling, density-gate dynamics; transition-exactness versus fate-predictiveness; strongest-refuge reserve ranking.

**EGWEE owns:** whether natural fragmentation responses show cross-layer state separation, the cluster/influence structure of that evidence, covariance robustness, and future natural moderator questions.

NEE may cite the completed EGWEE synthesis only as bounded Discussion-level external consistency. EGWEE is not a validation dataset for NEE mechanisms.

## Remaining submission work

### NEE flagship

Scientific routing and evidence-role firewalls are closed. Remaining blockers are author-controlled metadata/declarations, archive DOI/reviewer-accessible snapshots, final live Nature Ecology & Evolution policy recheck and portal submission.

### EGWEE

The Journal of Ecology anonymous manuscript, supplementary material and anonymous reviewer code/data package are prepared and QA-checked. Remaining blockers are author list/order and affiliations, corresponding-author details, acknowledgements/funding/permits, author contributions, conflicts of interest, final Data Availability wording, all-author approval and portal submission.

## Governance invariant

Do not strengthen either paper by moving evidence across the ownership firewall after outcomes are known. NEE does not reacquire EGWEE as a load-bearing Result, and EGWEE does not claim the finite NEE operator mechanisms as natural validation.
"""
    NEW_STATUS.write_text(status, encoding="utf-8")

    meta = META.read_text(encoding="utf-8")
    meta = meta.replace("publication_lanes.json` schema 5 and `EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`", "publication_lanes.json` schema 6 and `EG_SERIES_SUBMISSION_STATUS_2026-09-16.md`")
    META.write_text(meta, encoding="utf-8")

    story = STORY.read_text(encoding="utf-8")
    story = story.replace("EG_SERIES_SUBMISSION_STATUS_2026-09-08.md", "EG_SERIES_SUBMISSION_STATUS_2026-09-16.md")
    STORY.write_text(story, encoding="utf-8")

    validator = VALIDATOR.read_text(encoding="utf-8")
    validator = validator.replace('assert registry["schema_version"] == 5', 'assert registry["schema_version"] == 6', 1)
    validator = replace_once(
        validator,
        '    status = _flat(_read("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md"))\n    assert "operational submission-status source of truth" in status\n    assert "aa579f5262cf1403e4a6fc4e3937d64fbb1f2a80" in status\n    assert "one active EGWE submission lane" in status\n    assert "frozen fallback" in status.lower()\n\n    old_status = _flat(_read("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-05.md"))\n    assert "SUPERSEDED" in old_status\n    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-08.md" in old_status\n',
        '    status = _flat(_read("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-16.md"))\n    assert "operational submission-status source of truth" in status\n    assert "1603ae26103510b9f7b0c2c7030a9dccd9c54897" in status\n    assert "one active EGWE submission lane" in status\n    assert "Journal of Ecology" in status\n    assert "5 independent programme/study clusters / 17 marginal Hedges-g effects" in status\n    assert "frozen fallback" in status.lower()\n\n    prior_status = _flat(_read("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md"))\n    assert "SUPERSEDED" in prior_status\n    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-16.md" in prior_status\n\n    old_status = _flat(_read("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-05.md"))\n    assert "SUPERSEDED" in old_status\n',
        "validator current status",
    )
    validator = validator.replace('assert "EG_SERIES_SUBMISSION_STATUS_2026-09-08.md" in router', 'assert "EG_SERIES_SUBMISSION_STATUS_2026-09-16.md" in router', 1)
    natural_anchor = '    natural = registry["independent_development_programs"]["natural_data_four_gate_program"]\n'
    assert natural_anchor in validator
    empirical_checks = '''    empirical = registry["independent_development_programs"]["empirical_multilayer_meta_analysis"]\n    assert empirical["authoritative_repository"] == "zuizui0223/egwee"\n    assert empirical["repository_commit"] == "16308cf6d6e4aec274504ba81bbf6e71be465099"\n    assert empirical["status"] == "submission_ready_pending_author_metadata"\n    assert empirical["final_target"] == "Journal of Ecology"\n    assert empirical["submission_package_state"] == "ready_except_author_metadata"\n    assert empirical["primary_direct_clusters"] == 5\n    assert empirical["primary_marginal_effects"] == 17\n    assert abs(empirical["primary_fisher_p"] - 0.01212432) < 1e-12\n    assert abs(empirical["omit_ML001_p"] - 0.18194353) < 1e-12\n    assert abs(empirical["zero_covariance_p"] - 0.03860161) < 1e-12\n    assert abs(empirical["covariance_free_bound_p"] - 0.28061178) < 1e-12\n    assert "conditional state separation" in empirical["claim_ceiling"]\n\n'''
    validator = validator.replace(natural_anchor, empirical_checks + natural_anchor, 1)
    VALIDATOR.write_text(validator, encoding="utf-8")

    test = TEST.read_text(encoding="utf-8")
    test = test.replace('assert registry["schema_version"] == 5', 'assert registry["schema_version"] == 6', 1)
    old_test = '''def test_current_status_supersedes_old_router() -> None:\n    current = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md")\n    historical = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-05.md")\n    assert "operational submission-status source of truth" in current\n    assert "one active EGWE submission lane" in current\n    assert "aa579f5262cf1403e4a6fc4e3937d64fbb1f2a80" in current\n    assert "SUPERSEDED" in historical\n    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-08.md" in historical\n'''
    new_test = '''def test_current_status_supersedes_old_router() -> None:\n    current = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-16.md")\n    prior = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md")\n    historical = _flat("manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-05.md")\n    assert "operational submission-status source of truth" in current\n    assert "one active EGWE submission lane" in current\n    assert "1603ae26103510b9f7b0c2c7030a9dccd9c54897" in current\n    assert "Journal of Ecology" in current\n    assert "5 independent programme/study clusters / 17 marginal Hedges-g effects" in current\n    assert "SUPERSEDED" in prior\n    assert "EG_SERIES_SUBMISSION_STATUS_2026-09-16.md" in prior\n    assert "SUPERSEDED" in historical\n\n\ndef test_egwee_empirical_lane_is_current_and_independent() -> None:\n    registry = json.loads((ROOT / "manuscript/publication_lanes.json").read_text(encoding="utf-8"))\n    lane = registry["independent_development_programs"]["empirical_multilayer_meta_analysis"]\n    assert lane["repository_commit"] == "16308cf6d6e4aec274504ba81bbf6e71be465099"\n    assert lane["status"] == "submission_ready_pending_author_metadata"\n    assert lane["final_target"] == "Journal of Ecology"\n    assert lane["primary_direct_clusters"] == 5\n    assert lane["primary_marginal_effects"] == 17\n    assert lane["primary_fisher_p"] == 0.01212432\n    assert lane["omit_ML001_p"] == 0.18194353\n    assert lane["covariance_free_bound_p"] == 0.28061178\n    assert registry["active_lanes"]["nee_flagship"]["natural_evidence_role"] == "bounded_discussion_external_consistency_not_load_bearing"\n'''
    test = replace_once(test, old_test, new_test, "governance status tests")
    TEST.write_text(test, encoding="utf-8")

    print("Applied EGWEE submission-state governance synchronization")


if __name__ == "__main__":
    main()
