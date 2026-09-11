from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EGWEE_COMMIT = "5e16e861a769ab56da5bef14c68b0297dea05ef5"


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {n}: {old!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Human-facing routers.
replace_once(
    "README.md",
    "| EGWEE | when does an empirical measurement earn state/proxy status? | `zuizui0223/egwee` | independent empirical programme |",
    "| EGWEE | do natural fragmentation responses separate across biological layers, and which process/cohort moderators explain discordance? | `zuizui0223/egwee` | **empirical multilevel meta-analysis; screening/extraction in progress** |",
)
replace_once(
    "manuscript/README.md",
    "| EGWEE | empirical state/proxy adequacy | independent `zuizui0223/egwee` programme |",
    "| EGWEE | empirical cross-layer fragmentation response / process moderators | **multilevel meta-analysis in `zuizui0223/egwee`; protocol locked, screening/extraction pending** |",
)
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "| EGWEE | when does an empirical measurement earn state/proxy status? | `zuizui0223/egwee` | independent empirical programme |",
    "| EGWEE | do natural fragmentation effects separate across interaction, movement, reproduction and genetic layers, and what explains the discordance? | `zuizui0223/egwee` multilayer meta-analysis | **independent empirical synthesis; protocol locked, screening/extraction pending** |",
)
replace_once(
    "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md",
    "| EGWEE natural-data gates | `zuizui0223/egwee` | independent empirical programme | Ecological Indicators route remains separate |",
    "| EGWEE multilayer natural meta-analysis | `zuizui0223/egwee` | **protocol locked; screening/extraction pending** | empirical counterpart to NEE state separation; final venue not yet fixed |",
)
replace_once(
    "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md",
    "`zuizui0223/egwee` remains the authoritative empirical-gate repository.",
    "`zuizui0223/egwee` remains the authoritative natural-data repository, now routed to the multilayer fragmentation meta-analysis; the former four-gate programme is retained there as QC/provenance."
)

# Machine publication router. Preserve the former four-gate record as historical QC,
# and add a new active empirical-development programme without changing submission exclusivity.
reg_path = ROOT / "manuscript/publication_lanes.json"
reg = json.loads(reg_path.read_text(encoding="utf-8"))
for layer in reg["series_decomposition"]["layers"]:
    if layer["layer"] == "EGWEE":
        layer["question"] = (
            "do natural fragmentation responses separate across biological layers, "
            "and which process/cohort moderators explain discordance?"
        )
        layer["current_role"] = "empirical_multilevel_meta_analysis_counterpart_to_NEE_Q1_Q2"

historical = reg["independent_development_programs"]["natural_data_four_gate_program"]
historical["current_role"] = "historical_qc_and_provenance_only_not_active_publication"
reg["independent_development_programs"]["empirical_multilayer_meta_analysis"] = {
    "authoritative_repository": "zuizui0223/egwee",
    "repository_commit": EGWEE_COMMIT,
    "submission_spine": "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md",
    "protocol": "manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md",
    "effect_schema": "manuscript/meta_analysis_effect_schema.json",
    "status": "protocol_locked_screening_and_extraction_pending",
    "publication_structure": "systematic_review_and_multilevel_meta_analysis",
    "final_target": "not_yet_fixed",
    "questions": [
        "cross_layer_fragmentation_state_separation_in_nature",
        "process_and_cohort_moderators_of_cross_layer_discordance"
    ],
    "claim_ceiling": (
        "No meta-analytic numerical result is yet available. EGWEE may support or challenge NEE predictions "
        "only after deduplicated study screening, effect extraction, dependence modelling and locked synthesis."
    )
}
reg_path.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# NEE source manifest: keep the four natural anchors as projection material, but make
# the downstream empirical programme and its no-results-yet boundary explicit.
manifest_path = ROOT / "manuscript/nee_flagship_source_manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
proj = manifest["projection_sources"][0]
proj["role"] = "natural_process_anchors_plus_empirical_meta_analysis_handoff"
proj["repository"] = "zuizui0223/egwee"
proj["commit"] = EGWEE_COMMIT
proj["required_paths"] = [
    "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md",
    "manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md",
    "background/empirical_e3_crepis_audit.md",
    "background/empirical_e4_miyake_audit.md",
    "background/empirical_e5_conospermum_audit.md",
    "background/empirical_e6_spondias_audit.md"
]
proj["empirical_program_status"] = "protocol_locked_screening_and_extraction_pending"
proj["claim_ceiling"] = (
    "Current NEE Discussion uses only the four audited natural systems as projections. "
    "The EGWEE multilayer meta-analysis is a downstream empirical test and contributes no numerical validation claim until synthesis is complete."
)
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print("synchronized EGWEE empirical meta-analysis route into EGWE/NEE")
