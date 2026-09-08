from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "manuscript" / "natural_data_gate_registry.json"
FIGURES = ROOT / "manuscript" / "natural_data_figure_spec.json"
SPINE = ROOT / "manuscript" / "natural_data_ecological_indicators_spine.md"
LITERATURE = ROOT / "manuscript" / "NATURAL_DATA_NEAREST_NEIGHBOR_AUDIT_2026-09-01.md"
LANES = ROOT / "manuscript" / "publication_lanes.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_locked_registry_has_the_seven_system_four_line_structure() -> None:
    registry = _load(REGISTRY)
    systems = registry["systems"]

    assert len(systems) == 7
    assert Counter(record["line"] for record in systems) == {1: 3, 2: 1, 3: 2, 4: 1}
    assert registry["shared_order"] == [
        "measurement_adequacy",
        "representation_preservation",
        "residual_context",
        "cross_study_identifiability",
    ]
    assert registry["cross_study"]["locked_outcome"] == (
        "cross_origin_convergence_not_identifiable_from_existing_archives"
    )

    required = {
        "system",
        "candidate_state",
        "declared_endpoint",
        "holdout_unit",
        "gate_reached",
        "locked_outcome",
        "evidence_summary",
        "claim_ceiling",
    }
    for record in systems:
        assert required.issubset(record)
        assert all(str(record[key]).strip() for key in required)


def test_figure_specs_are_registry_driven_and_forbid_pooled_effects() -> None:
    registry = _load(REGISTRY)
    figures = _load(FIGURES)

    assert figures["source_registry"] == "manuscript/natural_data_gate_registry.json"
    expected_order = [record["system"] for record in registry["systems"]]
    assert figures["figure_2"]["order"] == expected_order
    assert set(figures["figure_2"]["columns"]) == {
        "system",
        "candidate_state",
        "declared_endpoint",
        "holdout_unit",
        "gate_reached",
        "locked_outcome",
    }
    forbidden = figures["figure_2"]["forbidden_encodings"]
    assert "one pooled effect-size axis" in forbidden
    assert "cross-system severity ranking" in forbidden
    assert "origin-level coefficient" in forbidden

    node_ids = {node["id"] for node in figures["figure_1"]["nodes"]}
    for gate in registry["shared_order"]:
        assert gate in node_ids


def test_manuscript_spine_preserves_locked_outcomes_and_claim_ceilings() -> None:
    text = SPINE.read_text(encoding="utf-8")

    for token in (
        "Test the state before interpreting the residual",
        "Honshu–Izu",
        "Zurich BetterBlooms",
        "Toronto community gardens",
        "Oenothera harringtonii",
        "Eschscholzia californica",
        "Mallorca carob",
        "Campanula americana",
        "1.08774",
        "1.13209",
        "4932.9195",
        "0.11619",
        "0.09187",
        "p=0.00130",
        "Fallow graound",
        "-0.10195",
        "8.88e-16",
        "cross_origin_convergence_not_identifiable_from_existing_archives",
    ):
        assert token in text, token

    for prohibited_warning_denominator in ("35/35", "48/48", "33/33", "49/49"):
        assert prohibited_warning_denominator not in text

    for ceiling in (
        "one pooled cross-system ecological effect",
        "state completeness from a negative residual-context test",
        "predictive validity of the separate EGWE genetic warning statistic",
    ):
        assert ceiling in text


def test_nearest_neighbor_audit_blocks_false_methodological_firstness() -> None:
    text = LITERATURE.read_text(encoding="utf-8")

    for token in (
        "Bockstaller & Girardin",
        "Scrupulous proxies",
        "Schielzeth",
        "Predictive validation",
        "fail-closed interpretation sequence",
        "Do **not** claim",
        "Ecological Indicators — primary",
        "Methods in Ecology and Evolution — conditional stretch only",
        "workflows linking existing methods generally are not considered new methods",
    ):
        assert token in text, token


def test_natural_paper_remains_independent_of_active_egwe_submission_lanes() -> None:
    lanes = _load(LANES)
    active_paths = {lane["manuscript"] for lane in lanes["active_lanes"].values()}
    natural = lanes["independent_development_programs"]["natural_data_four_gate_program"]

    assert natural["status"] == "migrated_authoritative_in_egwee"
    assert natural["authoritative_repository"] == "zuizui0223/egwee"
    assert natural["primary_target"] == "Ecological Indicators"
    assert natural["manuscript"] not in active_paths
    assert "warning_validity.md" not in SPINE.read_text(encoding="utf-8")
