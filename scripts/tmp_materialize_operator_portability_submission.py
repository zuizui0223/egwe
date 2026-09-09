from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {count}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Registry: keep the development note, but make the submission-facing manuscript explicit.
reg_path = ROOT / "manuscript/publication_lanes.json"
reg = json.loads(reg_path.read_text(encoding="utf-8"))
lane = reg["independent_output_lanes"]["operator_portability"]
lane.update({
    "development_note": "manuscript/operator_portability.md",
    "manuscript": "manuscript/operator_portability_short_communication.md",
    "cover_letter": "manuscript/operator_portability_cover_letter.md",
    "highlights": "manuscript/operator_portability_highlights.md",
    "display_plan": "manuscript/operator_portability_display_plan.md",
    "submission_metadata": "manuscript/operator_portability_submission_metadata.md",
    "submission_checklist": "manuscript/operator_portability_submission_checklist.md",
    "overlap_audit": "docs/OPERATOR_PORTABILITY_OVERLAP_AUDIT_2026-09-09.md",
    "submission_checker": "scripts/check_operator_portability_submission.py",
    "bundle_builder": "scripts/build_operator_portability_submission_bundle.py",
    "figure_builder": "scripts/build_operator_portability_figures.py",
    "figures": [
        "figures/operator_portability_fig1.svg",
        "figures/operator_portability_fig2.svg",
    ],
    "submission_package_ci": ".github/workflows/operator-portability-submission.yml",
    "submission_state": "package_ready_pending_author_metadata_and_final_policy_check",
})
lane["submission_requires"] = [
    "author_metadata_and_declarations",
    "author_approval",
    "final_claim_overlap_audit_at_submission",
    "final_reference_crosscheck_at_submission",
    "live_Ecological_Modelling_Guide_for_Authors_recheck",
]
reg_path.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Human routers.
replace_once(
    "README.md",
    "| EGWE portability | when can a connectivity label be transported across movement operators? | `manuscript/operator_portability.md` | active development; not submission-ready |",
    "| EGWE portability | when can a connectivity label be transported across movement operators? | `manuscript/operator_portability_short_communication.md` (submission-facing) + `manuscript/operator_portability.md` (development provenance) | **package-ready development candidate; author/policy gate remains** |",
)
replace_once(
    "README.md",
    "The historical allele-frequency-mixing `m=.10` equal-rate signal did not reproduce in one independent fresh Phase-U ensemble and did not port to whole-individual or pollen-only movement closures. Phases R/S share the same historical reference blocks, so the evidence is **one independent replication plus two shared-reference operator substitutions**, not three replications. No robust portable connectivity heterogeneity effect is established. The precision audit bounds the nulls rather than declaring equivalence, and the result has an explicit independent development surface, [`manuscript/operator_portability.md`](manuscript/operator_portability.md), provisionally scoped as an *Ecological Modelling* Short Communication.",
    "The historical allele-frequency-mixing `m=.10` equal-rate signal did not reproduce in one independent fresh Phase-U ensemble and did not port to whole-individual or pollen-only movement closures. Phases R/S share the same historical reference blocks, so the evidence is **one independent replication plus two shared-reference operator substitutions**, not three replications. No robust portable connectivity heterogeneity effect is established. The precision audit bounds the nulls rather than declaring equivalence. A submission-facing Short Communication now exists at [`manuscript/operator_portability_short_communication.md`](manuscript/operator_portability_short_communication.md), with [`manuscript/operator_portability.md`](manuscript/operator_portability.md) retained as development provenance; the package is prepared for *Ecological Modelling* but still awaits author metadata/approval and a final live policy/overlap check.",
)

replace_once(
    "manuscript/README.md",
    "| operator portability | [`operator_portability.md`](operator_portability.md) | **active development; not submission-ready; non-overlap audit required before submission** |",
    "| operator portability | [`operator_portability_short_communication.md`](operator_portability_short_communication.md) + [`operator_portability.md`](operator_portability.md) provenance | **package-ready development candidate; author/policy gate remains** |",
)
replace_once(
    "manuscript/README.md",
    "| EGWE portability | connectivity-operator identification / transportability | independent active development lane; not submission-ready |",
    "| EGWE portability | connectivity-operator identification / transportability | Short Communication package ready; author metadata/approval + final policy/overlap gate remain |",
)
replace_once(
    "manuscript/README.md",
    "Current publication ownership of this boundary is `operator_portability.md`, not the frozen state fallback or the NEE flagship.",
    "Current publication ownership of this boundary is the submission-facing `operator_portability_short_communication.md`, with `operator_portability.md` retained as development provenance; neither the frozen state fallback nor the NEE flagship owns this claim.",
)

replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "| EGWE portability | when can a connectivity label be transported across biological movement operators? | `operator_portability.md` | **active development; not submission-ready** |",
    "| EGWE portability | when can a connectivity label be transported across biological movement operators? | `operator_portability_short_communication.md` + `operator_portability.md` provenance | **package-ready development candidate; not yet authorised for submission** |",
)
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "- **Development manuscript:** `operator_portability.md`\n- **Status:** `active_development_nonoverlap_candidate`; **not submission-ready**.",
    "- **Submission-facing manuscript:** `operator_portability_short_communication.md`\n- **Development/provenance note:** `operator_portability.md`\n- **Status:** `active_development_nonoverlap_candidate`; **package-ready pending author metadata/approval and final policy/overlap check**.",
)
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "- **Submission gate:** fresh claim-overlap audit, final nearest-neighbour/reference check, independent submission package, author approval and live *Ecological Modelling* Short Communication policy check.",
    "- **Submission package:** dedicated references, highlights, cover letter, 2-figure plan/figures, submission metadata, overlap audit, fail-closed bundle builder and CI are materialized.\n- **Remaining submission gate:** author metadata/declarations, author approval, final reference/claim-overlap confirmation, and a live *Ecological Modelling* Guide for Authors check immediately before submission.",
)

replace_once(
    "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md",
    "| EGWE operator portability | `zuizui0223/egwe` | **active development; not submission-ready** | independent non-overlap candidate; development may proceed during flagship review |",
    "| EGWE operator portability | `zuizui0223/egwe` | **package-ready development candidate; not yet authorised for submission** | independent Short Communication candidate; author/policy gate remains |",
)
replace_once(
    "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md",
    "This is **not** a second active submission. It is an active development lane. The claim is deliberately separated from the flagship's alignment, sorting, buffering, recoupling, density-gate and last-refuge results. The evidence is now explicitly counted as **one independent fresh replication plus two process substitutions sharing one historical reference ensemble**, not three independent replications. A deterministic precision audit bounds the non-significant equal-rate results: the present five-block designs have an 80%-power benchmark near `w=0.163` (about **8.1–8.2 pp weighted RMS block-rate deviation near p=.5**), so equivalence is not claimed. The provisional outlet is ***Ecological Modelling* — Short Communication**. Submission still requires a fresh overlap audit, final nearest-neighbour/reference checking, an independent package, author approval and a live journal-policy check.",
    "This is **not** a second active submission. It is a package-ready development candidate. The claim is deliberately separated from the flagship's alignment, sorting, buffering, recoupling, density-gate and last-refuge results. The evidence is explicitly counted as **one independent fresh replication plus two process substitutions sharing one historical reference ensemble**, not three independent replications. A deterministic precision audit bounds the non-significant equal-rate results: the present five-block designs have an 80%-power benchmark near `w=0.163` (about **8.1–8.2 pp weighted RMS block-rate deviation near p=.5**), so equivalence is not claimed. The submission-facing `operator_portability_short_communication.md`, references, highlights, cover letter, two figures, metadata, overlap audit and fail-closed bundle/CI are now materialized for ***Ecological Modelling* — Short Communication**. Actual submission remains blocked by author metadata/declarations, author approval, and a final live reference/overlap/journal-policy check.",
)

# Checklist: the one-shot job only reaches this point after figure generation, checker, tests, and bundle build succeed.
replace_once(
    "manuscript/operator_portability_submission_checklist.md",
    "- [ ] Materialized final Figure 1 SVG/PDF\n- [ ] Materialized final Figure 2 SVG/PDF\n- [ ] Submission bundle archive generated and validated",
    "- [x] Materialized final Figure 1 SVG\n- [x] Materialized final Figure 2 SVG\n- [x] Submission bundle builder generated and validated a fail-closed package; permanent CI uploads the archive as an artifact",
)

print("Synchronized operator-portability package-ready state")
