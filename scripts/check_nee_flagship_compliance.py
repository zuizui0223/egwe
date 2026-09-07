from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "manuscript/nee_flagship_article.md"
DISPLAY = ROOT / "manuscript/nee_flagship_display_plan.md"
REFERENCES = ROOT / "manuscript/nee_flagship_references.md"
MANIFEST = ROOT / "manuscript/nee_flagship_source_manifest.json"
MECHANISM = ROOT / "artifacts/relational_mechanism_decomposition/locked_result.json"
EDGE = ROOT / "artifacts/pathway_edge_decomposition/locked_result.json"
FOCUSED = ROOT / "artifacts/allele_sorting_single_edge/locked_result.json"
RECOUPLING = ROOT / "artifacts/direct_feedback_recoupling/locked_derived_result.json"
DENSITY = ROOT / "artifacts/density_feedback_gate/locked_derived_result.json"


def words(text: str) -> list[str]:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return re.findall(r"[A-Za-z0-9_α-ωΑ-Ω]+(?:[-–—'][A-Za-z0-9_α-ωΑ-Ω]+)*", text)


def between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def main() -> None:
    article = ARTICLE.read_text(encoding="utf-8")
    display = DISPLAY.read_text(encoding="utf-8")
    refs = REFERENCES.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
    edge = json.loads(EDGE.read_text(encoding="utf-8"))
    focused = json.loads(FOCUSED.read_text(encoding="utf-8"))
    recoupling = json.loads(RECOUPLING.read_text(encoding="utf-8"))
    density_derived = json.loads(DENSITY.read_text(encoding="utf-8"))

    title = "Eco-genetic sorting and buffering shape functional vulnerability under fragmentation"
    assert article.startswith(f"# {title}\n")
    for heading in ("## Abstract", "## Results", "## Discussion", "## Methods"):
        assert heading in article, heading

    abstract_block = between(article, "## Abstract\n", "## Results\n")
    abstract = abstract_block.strip().split("\n\n", 1)[0]
    abstract_n = len(words(abstract))
    after_abstract = article.index("## Abstract\n") + len("## Abstract\n")
    abstract_end = article.index("\n\n", after_abstract)
    methods_start = article.index("## Methods\n")
    main_n = len(words(article[abstract_end + 2:methods_start]))
    results = between(article, "## Results\n", "## Discussion\n")
    discussion = between(article, "## Discussion\n", "## Methods\n")

    assert abstract_n <= 200, abstract_n
    assert main_n <= 3500, main_n
    figures = re.findall(r"^## Figure (\d+)\s", display, flags=re.M)
    assert figures == ["1", "2", "3", "4"], figures
    ref_entries = [p for p in refs.split("\n\n") if p.strip() and not p.lstrip().startswith("#")]
    assert len(ref_entries) <= 50, len(ref_entries)

    # Require only claims that remain load-bearing in the final main-text spine.
    # The older joint-local-selection +7.27-pp intermediate result remains in
    # provenance/Extended Data but has been superseded in main text by the
    # focused single-edge causal proof.
    required = (
        "K > 4",
        "1,037/1,037",
        "T_I=g\\circ\\phi",
        "0.2543",
        "49-fold difference",
        "+5.33",
        "+5.20",
        "6.23 points",
        "4.70 points",
        "+4.20 points",
        "+4.40 points",
        "+13.20 points",
        "+12.73 points",
        "recruitment-mediated buffering",
        "failure gate and amplifier",
        "q*=0.625",
        "6,000 paired AA/RR keys per condition",
        "+6.65 points",
        "-0.23 points",
        "+6.883",
        "+5.800,+7.967",
        "resolved single-edge causal contributor",
        "contracts trait–allele mismatch by exactly **50%**",
        "contracts interaction–bundle mismatch by exactly **40%**",
        "+8.53 points",
        "+7.80 points",
        "+7.93 points",
        "+6.33 points",
        "0.1135168053",
        "57.47 points",
        "59.60 points",
        "35 observed losses",
        "48 inherited non-event",
        "33 losses",
        "49 fresh non-events",
        "specificity `0`",
        "binary-marker AUC `0.5`",
    )
    for token in required:
        assert token in article, token

    for token in (
        "Crepis", "Miyake", "Zosterops", "Conospermum", "Spondias",
        "Honshu", "Zurich", "Toronto", "Oenothera", "Eschscholzia",
        "Mallorca", "Campanula americana",
    ):
        assert token not in results, f"natural projection leaked into Results: {token}"
    for token in ("Crepis", "Miyake", "Conospermum", "Spondias", "urban–island"):
        assert token in discussion or token in article[: article.index("## Results")], token

    lower = article.casefold()
    for forbidden in (
        "natural examples validate the model",
        "natural data validate the simulator",
        "alignment caused warning failure",
        "fragmentation caused the anti-aligned",
        "generation 20 is a universal",
        "positive alignment is universally protective",
        "support variance is a universal risk score",
        "matching-dependent recruitment pathway",
        "allele-linked recruitment generates the matching advantage",
        "density feedback causes the matching advantage",
        "direct feedback always increases q",
    ):
        assert forbidden not in lower, forbidden
    assert "does not establish q-dependent allele sorting as a universal natural mechanism" in lower
    assert "does not assert a universal natural recruitment or recoupling law" in lower
    assert "not a separately predeclared primary estimand" in lower

    assert manifest["schema_version"] == 7
    assert len(manifest["load_bearing_sources"]) == 8
    layers = {entry["layer"] for entry in manifest["load_bearing_sources"]}
    for required in (
        "prospective_operator_balance_route_margin",
        "prospective_sorting_headroom_followup",
        "prospective_continuous_last_refuge_warning_holdout",
    ):
        assert required in layers
    assert len(manifest["projection_sources"]) == 1
    assert len(manifest["claim_firewalls"]) >= 18
    for rel in manifest["mechanistic_synthesis_paths"]:
        assert (ROOT / rel).is_file(), rel

    assert mechanism["source"]["workflow_run"] == 34012983845
    assert mechanism["source"]["artifact_id"] == 9983093178
    assert abs(mechanism["analytic_headline"]["AA_RR_support_variance_ratio"] - 49.0) < 1e-12
    assert mechanism["full_feedback_factorial"]["generation_20"]["mismatched_minus_matched_risk"] > 0

    assert edge["source"]["workflow_run"] == 34014537015
    assert edge["source"]["artifact_id"] == 9983623440
    assert edge["fresh_q_only_baseline"]["generation_20"]["RR_minus_AA_risk_difference"] > 0
    assert edge["fresh_q_only_baseline"]["generation_40"]["RR_minus_AA_risk_difference"] > 0
    recruitment = edge["edge_deletions"]["allele_linked_recruitment"]
    assert recruitment["decision"] == "resolved_countervailing_buffer"
    assert recruitment["generation_20"]["baseline_minus_deletion_DID"] < 0
    assert recruitment["generation_40"]["baseline_minus_deletion_DID"] < 0
    # Preserve the earlier joint-block result in provenance even though the
    # focused single-edge proof supersedes it in the main manuscript.
    joint = edge["edge_deletions"]["joint_local_allele_and_trait_selection"]
    assert joint["generation_40"]["DID_ci95"][0] > 0

    assert focused["source"]["workflow_run"] == 34016797940
    assert focused["source"]["artifact_id"] == 9984306657
    assert abs(focused["operator_certificate"]["q_switch"] - 0.625) < 1e-12
    primary = focused["primary_generation_40_DID"]
    assert primary["decision"] == "resolved_positive_sorting_contribution"
    assert primary["n_paired_keys"] == 6000
    assert primary["paired_ci95"][0] > 0
    assert abs(primary["baseline_minus_deletion_DID"] - 0.06883333333333333) < 1e-12

    assert recoupling["status"] == "derived_from_successful_prospective_workflow_artifact_no_new_simulation"
    assert recoupling["source"]["workflow_run"] == 34012983845
    assert recoupling["source"]["paired_keys"] == 1500
    assert recoupling["operator_certificate"]["support_mismatch_reduction_fraction"] == 0.4
    assert recoupling["generation_20"]["RR"]["paired_ci95"][0] > 0
    assert recoupling["generation_20"]["DID_ci95"][0] > 0
    assert recoupling["generation_40"]["RR"]["paired_ci95"][0] > 0
    assert recoupling["generation_40"]["DID_ci95"][0] > 0

    assert density_derived["status"] == "derived_from_locked_pathway_edge_artifact"
    assert density_derived["source"]["workflow_run"] == 34014537015
    assert density_derived["generation_20"]["AA"]["delete_density_loss_rate"] == 0.0
    assert density_derived["generation_20"]["RR"]["delete_density_loss_rate"] == 0.0
    assert density_derived["generation_40"]["AA"]["paired_ci95"][0] > 0.54
    assert density_derived["generation_40"]["RR"]["paired_ci95"][0] > 0.56

    print(f"NEE abstract words: {abstract_n}")
    print(f"NEE main-text words: {main_n}")
    print(f"Main displays: {len(figures)}")
    print(f"References: {len(ref_entries)}")
    print("Four-operator NEE flagship compliance: PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"Four-operator NEE flagship compliance: FAIL — {exc}", file=sys.stderr)
        raise
