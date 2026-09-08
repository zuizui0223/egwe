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


# 1) Remove contradictory in-file status language rather than masking it with banners.
replace_once(
    "manuscript/warning_validity.md",
    "**Publication status:** active warning-validity manuscript. This manuscript is\n"
    "the sole active publication lane for the full-denominator warning result. It\n"
    "does not make a joint-state or cross-system convergence claim.",
    "**Publication status:** frozen fallback, not current-evidence complete for submission. This manuscript preserves the six-rule full-denominator warning result, but it is not an active publication lane while the NEE flagship is under consideration. It does not make a joint-state or cross-system convergence claim.",
)

state_path = ROOT / "manuscript/state_validity_and_empirical_measurement_gates.md"
state = state_path.read_text(encoding="utf-8")
if not state.startswith("# FROZEN FALLBACK"):
    state = (
        "# FROZEN FALLBACK — NOT FOR SIMULTANEOUS SUBMISSION\n\n"
        "> The state/propagation results below remain scientifically valid. Their load-bearing representation and horizon-propagation evidence is reused by the active NEE flagship. Process-portability prose is retained here for provenance, but current portability claim ownership is routed to `operator_portability.md`. Any later reactivation of this fallback must first resolve that overlap and can occur only after the flagship is no longer under consideration.\n\n"
        + state
    )
old_state_status = (
    "**Publication status:** active state-validity manuscript. This manuscript owns the constructive joint-state, exact next-transition, propagation-horizon, and process-portability claims. Natural systems are used only as ecological background and discussion anchors; they are not treated as external validation of the finite closure. The manuscript does not claim validated predictive genetic warning."
)
new_state_status = (
    "**Publication status:** frozen fallback, not for simultaneous submission. This manuscript historically combines the constructive joint-state, exact next-transition, propagation-horizon, and process-portability results. Its state/propagation evidence is reused by the active NEE flagship; current process-portability development ownership is routed separately in `publication_lanes.json`. Natural systems are used only as ecological background and discussion anchors; they are not treated as external validation of the finite closure. The manuscript does not claim validated predictive genetic warning."
)
if state.count(old_state_status) != 1:
    raise RuntimeError("state manuscript active-status anchor missing or duplicated")
state_path.write_text(state.replace(old_state_status, new_state_status, 1), encoding="utf-8")

replace_once(
    "manuscript/grand_synthesis_flagship.md",
    "**Status:** optional flagship synthesis built from the four locked EG publication lanes. This manuscript does not supersede the submission-ready EGC, EGWE-state, EGWE-warning, or EGWEE manuscripts. It owns only the higher-order predictive-validity hierarchy defined in `GRAND_SYNTHESIS_DEPENDENCY_AUDIT_2026-09-05.md`.",
    "**Status:** superseded 2026-09-05 synthesis spine retained for provenance only. It predates the flagship-first routing decision. The standalone EGWE state and warning packages are now frozen fallbacks rather than submission-ready active lanes; `nee_flagship_article.md` is the current EGWE submission source of truth. This file owns no current publication claim.",
)

# 2) Move process-specific portability out of the frozen state fallback into an explicit independent development outlet.
registry_path = ROOT / "manuscript/publication_lanes.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
if registry.get("schema_version") != 4:
    raise RuntimeError(f"unexpected registry schema: {registry.get('schema_version')}")
registry["schema_version"] = 5
state_lane = registry["frozen_fallback_lanes"]["state_validity"]
state_lane["former_owned_claims"] = [
    "joint_state_representation",
    "next_transition_insufficiency",
    "horizon_dependent_loss_risk_propagation",
    "process_specific_portability",
]
if "resolve_operator_portability_claim_overlap" not in state_lane["reactivation_requires"]:
    state_lane["reactivation_requires"].append("resolve_operator_portability_claim_overlap")
state_lane["current_portability_owner"] = "operator_portability"
registry["independent_output_lanes"] = {
    "operator_portability": {
        "manuscript": "manuscript/operator_portability.md",
        "status": "active_development_nonoverlap_candidate",
        "submission_state": "not_submission_ready",
        "development_allowed_while_flagship_under_consideration": True,
        "owned_claims": [
            "process_specific_portability",
            "connectivity_operator_nonexchangeability",
            "historical_m010_heterogeneity_nonreplication",
        ],
        "locked_evidence": [
            "phase_u_fresh_allele_mixing_replication",
            "phase_r_whole_individual_dispersal",
            "phase_s_pollen_only_gene_flow",
        ],
        "submission_requires": [
            "claim_overlap_audit_against_current_flagship_and_any_reactivated_fallback",
            "literature_nearest_neighbor_audit",
            "independent_cover_letter_references_display_plan_and_bundle",
            "author_approval",
            "live_journal_policy_recheck",
        ],
        "relationship_to_flagship": "Development may proceed while the flagship is under consideration because the portability lane deliberately excludes the flagship's state-alignment, sorting, buffering, recoupling, density-gate and warning/reserve claims. Submission is not authorised until a fresh overlap audit passes.",
        "claim_ceiling": "The historical allele-only m=.10 heterogeneity signal failed one independent fresh replication and did not port to the tested whole-individual or pollen-only closures. This does not establish universal non-equivalence, calibrated equality of m/d/g, or a natural connectivity threshold.",
    }
}
# Make the scientific decomposition explicit about where the portability remainder went.
for layer in registry["series_decomposition"]["layers"]:
    if layer["layer"] == "EGWE_state":
        layer["current_role"] = "state_representation_and_propagation_evidence_absorbed_by_flagship; process_portability_extracted_to_independent_development_lane"
registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# 3) Human-readable router/status surfaces.
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "The exact `0.2543` representation counterexample, prospective generation-20/40 propagation contrasts, and process-specific portability boundary remain scientifically valid. They are now absorbed into the active flagship evidence stack rather than treated as a simultaneously submittable paper.",
    "The exact `0.2543` representation counterexample and prospective generation-20/40 propagation contrasts remain scientifically valid and are reused in the active flagship evidence stack. The process-specific portability boundary is also scientifically valid, but it is **not** a flagship-owned result; current ownership is routed to the independent `operator_portability.md` development lane. The frozen state manuscript retains that prose only for provenance."
)
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "**Reactivation gate:** this manuscript may return to an active submission lane only if the NEE flagship is no longer under consideration (withdrawn, rejected without transfer, or explicitly abandoned), followed by author confirmation of exclusivity and a live journal-policy check. Its current cover letter is therefore a frozen fallback, not a declaration that can coexist with an active flagship submission.",
    "**Reactivation gate:** this manuscript may return to an active submission lane only if the NEE flagship is no longer under consideration (withdrawn, rejected without transfer, or explicitly abandoned), followed by author confirmation of exclusivity, a live journal-policy check, and explicit resolution of overlap with the independent operator-portability lane. Its current cover letter is therefore a frozen fallback, not a declaration that can coexist with an active flagship submission."
)
insert_anchor = "## Migrated independent programme — natural-data gates\n"
insert_text = """## Independent development lane — operator portability

- **Development manuscript:** `operator_portability.md`
- **Status:** `active_development_nonoverlap_candidate`; **not submission-ready**.
- **Owned claim:** process-specific portability / semantic identification of connectivity operators.
- **Locked evidence:** Phase U fresh non-replication of historical allele-only `m=.10` heterogeneity, Phase R whole-individual dispersal, and Phase S pollen-only gene flow.
- **Parallel-development rule:** development may proceed while the NEE flagship is under consideration because this lane deliberately excludes the flagship's aligned-state, operator-balance and warning/reserve claims.
- **Submission gate:** fresh claim-overlap audit, nearest-neighbour literature audit, independent submission package, author approval and live journal-policy check.

This lane exists because freezing the old state manuscript otherwise leaves a valid negative portability result without a current publication owner. It is not created by pretending the negative result is already a full paper. The development spine explicitly preserves the main caveats: Phase U is one fresh replication, Phases R/S each test one closure, and `m`, `d` and `g` are not calibrated as equivalent natural movement doses.

"""
p = ROOT / "manuscript/PUBLICATION_LANES.md"
text = p.read_text(encoding="utf-8")
if "## Independent development lane — operator portability" not in text:
    if text.count(insert_anchor) != 1:
        raise RuntimeError("PUBLICATION_LANES insertion anchor mismatch")
    p.write_text(text.replace(insert_anchor, insert_text + insert_anchor, 1), encoding="utf-8")
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "| EGWE state | what representation preserves future-relevant distinctions? | evidence incorporated into `nee_flagship_article.md`; standalone state manuscript retained | **frozen fallback** |\n| EGWE warning |",
    "| EGWE state | what representation preserves future-relevant distinctions? | representation/propagation evidence incorporated into `nee_flagship_article.md`; standalone state manuscript retained | **frozen fallback** |\n| EGWE portability | when can a connectivity label be transported across biological movement operators? | `operator_portability.md` | **active development; not submission-ready** |\n| EGWE warning |"
)

replace_once(
    "README.md",
    "| EGWE state | what representation preserves future-relevant distinctions? | evidence incorporated into `nee_flagship_article.md`; standalone state manuscript retained | frozen fallback |\n| EGWE warning |",
    "| EGWE state | what representation preserves future-relevant distinctions? | representation/propagation evidence incorporated into `nee_flagship_article.md`; standalone state manuscript retained | frozen fallback |\n| EGWE portability | when can a connectivity label be transported across movement operators? | `manuscript/operator_portability.md` | active development; not submission-ready |\n| EGWE warning |"
)
replace_once(
    "README.md",
    "The historical allele-frequency-mixing `m=.10` equal-rate signal did not reproduce in one independent fresh Phase-U ensemble and did not port to whole-individual or pollen-only movement closures. No robust portable connectivity heterogeneity effect is established.",
    "The historical allele-frequency-mixing `m=.10` equal-rate signal did not reproduce in one independent fresh Phase-U ensemble and did not port to whole-individual or pollen-only movement closures. No robust portable connectivity heterogeneity effect is established. This result now has an explicit independent development surface, [`manuscript/operator_portability.md`](manuscript/operator_portability.md), rather than being orphaned inside the frozen state fallback."
)

replace_once(
    "manuscript/README.md",
    "| warning validity | [`warning_validity.md`](warning_validity.md) | **frozen fallback; later holdout evidence must be integrated/reported before reactivation** |",
    "| warning validity | [`warning_validity.md`](warning_validity.md) | **frozen fallback; later holdout evidence must be integrated/reported before reactivation** |\n| operator portability | [`operator_portability.md`](operator_portability.md) | **active development; not submission-ready; non-overlap audit required before submission** |"
)
replace_once(
    "manuscript/README.md",
    "| EGWE state | representation adequacy | incorporated into active flagship; standalone fallback frozen |\n| EGWE warning |",
    "| EGWE state | representation adequacy | representation/propagation incorporated into active flagship; standalone fallback frozen |\n| EGWE portability | connectivity-operator identification / transportability | independent active development lane; not submission-ready |\n| EGWE warning |"
)
replace_once(
    "manuscript/README.md",
    "- **C2c — connectivity representation boundary:** the historical allele-only `m=.10` heterogeneity observation failed one preregistered fresh-seed replication (Phase U) and did not port to whole-individual dispersal (Phase R) or pollen-only gene flow (Phase S). No robust portable connectivity-heterogeneity effect is established.",
    "- **C2c — connectivity representation boundary:** the historical allele-only `m=.10` heterogeneity observation failed one preregistered fresh-seed replication (Phase U) and did not port to whole-individual dispersal (Phase R) or pollen-only gene flow (Phase S). No robust portable connectivity-heterogeneity effect is established. Current publication ownership of this boundary is `operator_portability.md`, not the frozen state fallback or the NEE flagship."
)

replace_once(
    "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md",
    "| EGWE state validity | `zuizui0223/egwe` | **frozen fallback** | reactivate only after flagship is no longer under consideration |\n| EGWE warning validity |",
    "| EGWE state validity | `zuizui0223/egwe` | **frozen fallback** | reactivate only after flagship is no longer under consideration and portability overlap is resolved |\n| EGWE operator portability | `zuizui0223/egwe` | **active development; not submission-ready** | independent non-overlap candidate; development may proceed during flagship review |\n| EGWE warning validity |"
)
status_anchor = "## Evidence that changed the routing decision\n"
status_insert = """## Portability is not orphaned

Freezing the state-validity manuscript would otherwise leave the process-portability result without a current publication owner. That was not intended. `manuscript/operator_portability.md` now owns the distinct question of whether a scalar connectivity label can be transported across allele-frequency mixing, whole-individual dispersal and pollen-only closures.

This is **not** a second active submission. It is an active development lane. The claim is deliberately separated from the flagship's alignment, sorting, buffering, recoupling, density-gate and last-refuge results. Submission requires a fresh overlap audit, literature/nearest-neighbour positioning, an independent package, author approval and a live journal-policy check.

"""
p = ROOT / "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md"
text = p.read_text(encoding="utf-8")
if "## Portability is not orphaned" not in text:
    if text.count(status_anchor) != 1:
        raise RuntimeError("status insertion anchor mismatch")
    p.write_text(text.replace(status_anchor, status_insert + status_anchor, 1), encoding="utf-8")

replace_once(
    "manuscript/claim_evidence_map.md",
    "| frozen state fallback | `state_validity_and_empirical_measurement_gates.md` | representation/propagation claims remain valid as fallback evidence |",
    "| frozen state fallback | `state_validity_and_empirical_measurement_gates.md` | representation/propagation claims remain valid as fallback evidence; historical portability prose is provenance only |\n| operator-portability development | `operator_portability.md` | current owner of process-specific connectivity portability / non-exchangeability claims; not submission-ready |"
)
replace_once(
    "manuscript/claim_evidence_map.md",
    "The router in `publication_lanes.json` is fail-closed: the active flagship explicitly registers reused fallback evidence and flagship-only load-bearing evidence; overlapping fallbacks cannot be simultaneously active. Routing does not modify any evidence status below.",
    "The router in `publication_lanes.json` is fail-closed: the active flagship explicitly registers reused fallback evidence and flagship-only load-bearing evidence; overlapping fallbacks cannot be simultaneously active; and process-specific portability has its own non-submission development owner. Routing does not modify any evidence status below."
)

replace_once(
    "manuscript/artifact_index.md",
    "| frozen state-validity fallback | `manuscript/state_validity_and_empirical_measurement_gates.md` | preserves locked representation/propagation results for possible later reactivation |",
    "| frozen state-validity fallback | `manuscript/state_validity_and_empirical_measurement_gates.md` | preserves locked representation/propagation results; historical portability prose retained for provenance |\n| operator-portability development | `manuscript/operator_portability.md` | current publication owner for Phase U/R/S process-portability evidence; not submission-ready |"
)

# 4) Validator must test absence of stale status claims, not only presence of banners.
validator_path = ROOT / "scripts/validate_publication_lanes.py"
validator = validator_path.read_text(encoding="utf-8")
validator = validator.replace('assert registry["schema_version"] == 4', 'assert registry["schema_version"] == 5', 1)
anchor = "    exclusivity = registry[\"exclusivity_policy\"]\n"
insert = """    independent = registry["independent_output_lanes"]
    assert set(independent) == {"operator_portability"}
    portability = independent["operator_portability"]
    assert portability["status"] == "active_development_nonoverlap_candidate"
    assert portability["submission_state"] == "not_submission_ready"
    assert portability["development_allowed_while_flagship_under_consideration"] is True
    assert set(portability["owned_claims"]) == {
        "process_specific_portability",
        "connectivity_operator_nonexchangeability",
        "historical_m010_heterogeneity_nonreplication",
    }
    assert (ROOT / portability["manuscript"]).is_file()

"""
if insert not in validator:
    if validator.count(anchor) != 1:
        raise RuntimeError("validator independent-lane anchor mismatch")
    validator = validator.replace(anchor, insert + anchor, 1)
old = """    warning_text = _flat(_read(fallbacks["warning_validity"]["manuscript"]))
    assert "FROZEN FALLBACK" in warning_text
    assert "last-refuge" in warning_text
"""
new = """    warning_text = _flat(_read(fallbacks["warning_validity"]["manuscript"]))
    assert "FROZEN FALLBACK" in warning_text
    assert "last-refuge" in warning_text
    assert "active warning-validity manuscript" not in warning_text
    assert "sole active publication lane" not in warning_text
"""
if validator.count(old) != 1:
    raise RuntimeError("validator warning anchor mismatch")
validator = validator.replace(old, new, 1)
old = """    state_text = _flat(_read(fallbacks["state_validity"]["manuscript"]))
    for token in ("0.2543", "+5.33", "+5.20"):
        assert token in state_text, token
"""
new = """    state_text = _flat(_read(fallbacks["state_validity"]["manuscript"]))
    assert "FROZEN FALLBACK" in state_text
    assert "active state-validity manuscript" not in state_text
    assert "current process-portability development ownership is routed separately" in state_text
    for token in ("0.2543", "+5.33", "+5.20"):
        assert token in state_text, token

    portability_text = _flat(_read(portability["manuscript"]))
    for token in (
        "ACTIVE DEVELOPMENT LANE",
        "not yet submission-ready",
        "historical_m010_heterogeneity_not_freshly_replicated",
        "whole-individual",
        "pollen-only",
        "p=.694",
        "p=.811",
        "p=.728",
    ):
        assert token.lower() in portability_text.lower(), token
    for forbidden in ("0.2543", "+5.33", "+5.20", "35/35", "48/48", "0.92734", "+6.883", "1,920,000"):
        assert forbidden not in portability_text, f"flagship/state/warning claim leaked into portability lane: {forbidden}"
"""
if validator.count(old) != 1:
    raise RuntimeError("validator state anchor mismatch")
validator = validator.replace(old, new, 1)
old = """    grand = _flat(_read("manuscript/grand_synthesis_flagship.md"))
    assert "SUPERSEDED INITIAL FLAGSHIP SPINE" in grand
    assert "nee_flagship_article.md" in grand
"""
new = """    grand = _flat(_read("manuscript/grand_synthesis_flagship.md"))
    assert "SUPERSEDED INITIAL FLAGSHIP SPINE" in grand
    assert "nee_flagship_article.md" in grand
    assert "does not supersede the submission-ready" not in grand
    assert "submission-ready EGC, EGWE-state, EGWE-warning" not in grand
"""
if validator.count(old) != 1:
    raise RuntimeError("validator grand anchor mismatch")
validator = validator.replace(old, new, 1)
validator = validator.replace(
    '        "0.23253",\n    ):\n        assert token in ownership, token\n',
    '        "0.23253",\n        "Independent development lane — operator portability",\n        "operator_portability.md",\n    ):\n        assert token in ownership, token\n',
    1,
)
validator = validator.replace(
    '    assert "Publication crosswalk" in router\n',
    '    assert "Publication crosswalk" in router\n    assert "operator_portability.md" in router\n',
    1,
)
validator = validator.replace(
    '    assert "frozen fallback" in manuscript_router.lower()\n',
    '    assert "frozen fallback" in manuscript_router.lower()\n    assert "operator_portability.md" in manuscript_router\n',
    1,
)
validator = validator.replace(
    '"state and warning manuscripts frozen as non-simultaneous fallbacks; "\n        "flagship overlap and unique evidence explicitly registered; H_alpha inversion reported."',
    '"state and warning manuscripts frozen as non-simultaneous fallbacks; "\n        "operator portability has an independent non-submission development owner; "\n        "stale active-status phrases are forbidden; H_alpha inversion reported."',
    1,
)
validator_path.write_text(validator, encoding="utf-8")

# 5) Regression tests: add negative invariants and portability ownership.
test_path = ROOT / "tests/test_publication_governance.py"
tests = test_path.read_text(encoding="utf-8")
tests = tests.replace('assert registry["schema_version"] == 4', 'assert registry["schema_version"] == 5', 1)
append = r'''


def test_frozen_fallbacks_forbid_stale_active_status_phrases() -> None:
    warning = _flat("manuscript/warning_validity.md")
    state = _flat("manuscript/state_validity_and_empirical_measurement_gates.md")
    assert "FROZEN FALLBACK" in warning
    assert "active warning-validity manuscript" not in warning
    assert "sole active publication lane" not in warning
    assert "FROZEN FALLBACK" in state
    assert "active state-validity manuscript" not in state


def test_superseded_spine_forbids_obsolete_submission_ready_claim() -> None:
    grand = _flat("manuscript/grand_synthesis_flagship.md")
    assert "SUPERSEDED INITIAL FLAGSHIP SPINE" in grand
    assert "does not supersede the submission-ready" not in grand
    assert "submission-ready EGC, EGWE-state, EGWE-warning" not in grand


def test_portability_has_independent_development_owner_without_flagship_claim_leakage() -> None:
    registry = json.loads((ROOT / "manuscript/publication_lanes.json").read_text(encoding="utf-8"))
    lane = registry["independent_output_lanes"]["operator_portability"]
    assert lane["status"] == "active_development_nonoverlap_candidate"
    assert lane["submission_state"] == "not_submission_ready"
    assert lane["development_allowed_while_flagship_under_consideration"] is True
    assert "process_specific_portability" in lane["owned_claims"]
    assert registry["frozen_fallback_lanes"]["state_validity"]["current_portability_owner"] == "operator_portability"
    text = _flat(lane["manuscript"])
    for required in ("historical_m010_heterogeneity_not_freshly_replicated", "whole-individual", "pollen-only"):
        assert required in text
    for forbidden in ("0.2543", "+5.33", "+5.20", "35/35", "48/48", "0.92734", "+6.883", "1,920,000"):
        assert forbidden not in text
'''
if "test_frozen_fallbacks_forbid_stale_active_status_phrases" not in tests:
    tests += append

test_path.write_text(tests, encoding="utf-8")

print("Applied status-negative-invariant and portability-owner reconciliation")
