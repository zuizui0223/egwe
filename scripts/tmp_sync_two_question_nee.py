from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {n}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Reframe the active NEE manuscript as two biological questions: EGC first, EGWE second.
replace_once(
    "manuscript/nee_flagship_article.md",
    "We address those questions in four steps. First, we test whether a single fragmentation gradient corresponds to a single biological deterioration coordinate. Second, we construct matched-marginal states and identify the exact source of their next-transition difference. Third, we prospectively intervene on individual life-cycle edges and derive the exact operators responsible for sorting, buffering, recoupling and collapse entry. Fourth, we separate stress sensitivity from fate information: after testing whether early marginal genetic erosion discriminates later fate, we prospectively test whether the continuous reserve of the strongest remaining local refuge does. Natural examples return only in the Discussion as projections of these mechanisms.",
    "We organize the paper around two biological questions. **Question 1 asks whether fragmentation produces one biological deterioration state.** Using the EGC theorem and fixed-area fragmentation evidence, we test whether potential viability, realised occupancy, interaction support, demography and trait state collapse onto one axis. **Question 2 asks what determines divergent futures once state separation is acknowledged.** Using EGWE, we construct matched-marginal states, identify the hidden cross-layer organization that changes transitions, intervene on life-cycle operators responsible for sorting, buffering, recoupling and collapse entry, and then distinguish stress sensitivity from fate information using the continuous reserve of the strongest remaining local refuge. Natural examples return only in the Discussion as projections of these mechanisms."
)
replace_once(
    "manuscript/nee_flagship_article.md",
    "## Results\n\n### Fragmentation separated persistence from functional support",
    "## Results\n\n### Question 1 — Does fragmentation produce one biological deterioration state?\n\n#### Fragmentation separated persistence from functional support"
)
replace_once(
    "manuscript/nee_flagship_article.md",
    "### Matched marginals concealed an exact transition difference",
    "### Question 2 — Given state separation, what determines divergent futures and predicts fate?\n\n#### Matched marginals concealed an exact transition difference"
)
replace_once(
    "manuscript/nee_flagship_article.md",
    "### Four life-cycle operators explained divergence, repair and collapse entry",
    "#### Four life-cycle operators explained divergence, repair and collapse entry"
)
for old, new in (
    ("#### q-dependent allele selection is the sorting operator", "##### q-dependent allele selection is the sorting operator"),
    ("#### Allele-linked recruitment is an exact mismatch buffer", "##### Allele-linked recruitment is an exact mismatch buffer"),
    ("#### Direct eco-genetic feedback is a recoupling operator", "##### Direct eco-genetic feedback is a recoupling operator"),
    ("#### Density feedback is a failure gate and amplifier", "##### Density feedback is a failure gate and amplifier"),
    ("### Marginal genetic erosion did not identify fate, but last-refuge reserve did", "#### Marginal genetic erosion did not identify fate, but last-refuge reserve did"),
):
    replace_once("manuscript/nee_flagship_article.md", old, new)

# Human routing: EGC is no longer a separate active publication in this programme.
replace_once(
    "README.md",
    "| EGC | what biological states separate under fragmentation? | `zuizui0223/eco-genetic-criticality` | independent parent paper |",
    "| EGC | **NEE Question 1:** does fragmentation produce one biological deterioration state? | `zuizui0223/eco-genetic-criticality` evidence imported into `nee_flagship_article.md` | **load-bearing NEE source; no separate active submission** |"
)
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "- **Core question:** why can systems retaining the same conventional ecological/genetic marginals have different functional futures, and what representation retains information about those futures?",
    "- **Two-question spine:** **Q1 (EGC)** asks whether fragmentation produces one biological deterioration state; **Q2 (EGWE)** asks what hidden organization and life-cycle operators determine divergent futures and what continuous reserve carries fate information."
)
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "- **scientific decomposition:** EGC → state validity → warning validity → empirical measurement gate;",
    "- **scientific decomposition inside the flagship:** **Q1 = EGC state separation**; **Q2 = EGWE representation → operators → warning/reserve**; EGWEE remains the downstream natural measurement programme;"
)
replace_once(
    "manuscript/PUBLICATION_LANES.md",
    "| EGC | what biological states separate under fragmentation? | `zuizui0223/eco-genetic-criticality` | independent parent paper |",
    "| EGC | **NEE Question 1:** does fragmentation produce one biological deterioration state? | `zuizui0223/eco-genetic-criticality` canonical evidence used directly by `nee_flagship_article.md` | **absorbed into active NEE flagship; no separate active submission** |"
)

# Machine router: make the two-question role explicit without changing evidence ownership/provenance.
reg_path = ROOT / "manuscript/publication_lanes.json"
reg = json.loads(reg_path.read_text(encoding="utf-8"))
reg["active_lanes"]["nee_flagship"]["question_structure"] = {
    "Q1_EGC": "Does fragmentation produce one biological deterioration state?",
    "Q2_EGWE": "Given state separation, what hidden organization and life-cycle operators determine divergent futures, and what continuous reserve carries fate information?",
}
for layer in reg["series_decomposition"]["layers"]:
    if layer["layer"] == "EGC":
        layer["current_role"] = "load_bearing_NEE_question_1_absorbed_into_flagship_no_separate_active_submission"
    elif layer["layer"] == "EGWE_state":
        layer["current_role"] = "NEE_question_2_representation_and_propagation_evidence; process_portability_extracted_to_independent_output_lane"
    elif layer["layer"] == "EGWE_warning":
        layer["current_role"] = "NEE_question_2_warning_and_reserve_evidence; standalone_warning_fallback_frozen"
reg_path.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print("synchronized two-question NEE architecture")
