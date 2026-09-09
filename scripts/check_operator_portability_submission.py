from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MANUSCRIPT = ROOT / "manuscript/operator_portability_short_communication.md"
SUPPORT = [
    ROOT / "manuscript/operator_portability_references.md",
    ROOT / "manuscript/operator_portability_highlights.md",
    ROOT / "manuscript/operator_portability_cover_letter.md",
    ROOT / "manuscript/operator_portability_display_plan.md",
    ROOT / "manuscript/operator_portability_submission_metadata.md",
    ROOT / "manuscript/operator_portability_submission_checklist.md",
    ROOT / "docs/OPERATOR_PORTABILITY_OVERLAP_AUDIT_2026-09-09.md",
    ROOT / "docs/OPERATOR_PORTABILITY_PRECISION_AUDIT_2026-09-09.md",
    ROOT / "artifacts/operator_portability_precision/derived_summary.json",
    ROOT / "figures/operator_portability_fig1.svg",
    ROOT / "figures/operator_portability_fig2.svg",
]

FORBIDDEN_FLAGSHIP_TOKENS = (
    "0.2543",
    "+5.33",
    "+5.20",
    "35/35",
    "48/48",
    "33/33",
    "49/49",
    "+6.883",
    "1,920,000",
    "0.92734",
    "+0.02135",
)


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w'.=-]+\b", text)


def section(text: str, start: str, end: str | None) -> str:
    if start not in text:
        raise AssertionError(f"missing section {start}")
    tail = text.split(start, 1)[1]
    return tail if end is None else tail.split(end, 1)[0]


def main() -> int:
    assert MANUSCRIPT.is_file()
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert text.startswith("# Connectivity is an operator, not a scalar: a finite-model portability test\n")
    assert "## Abstract" in text
    assert "## Keywords" in text
    assert "## 1. Introduction" in text
    assert "## 2. Methods" in text
    assert "## 3. Results" in text
    assert "## 4. Discussion" in text
    assert "## Data and code availability" in text

    abstract = section(text, "## Abstract", "## Keywords")
    abstract_n = len(words(abstract))
    total_n = len(words(text))
    assert 120 <= abstract_n <= 250, abstract_n
    assert 1400 <= total_n <= 3200, total_n

    for token in FORBIDDEN_FLAGSHIP_TOKENS:
        assert token not in text, f"flagship evidence leaked into portability manuscript: {token}"

    for token in (
        "one independent fresh replication",
        "same historical reference observations",
        "not two independent replications",
        "deterministic classifications",
        "not equivalence",
        "8.17",
        "8.12",
        "Ecological Modelling",
    ):
        assert token.lower() in text.lower(), token

    for path in SUPPORT:
        assert path.is_file(), path

    precision = json.loads((ROOT / "artifacts/operator_portability_precision/derived_summary.json").read_text(encoding="utf-8"))
    assert precision["evidence_structure"]["phase_r_s_reference_blocks_identical"] is True
    assert 0.16 < precision["precision"]["447"]["w_80"] < 0.17
    assert 0.16 < precision["precision"]["452"]["w_80"] < 0.17

    highlights = (ROOT / "manuscript/operator_portability_highlights.md").read_text(encoding="utf-8")
    bullets = [line for line in highlights.splitlines() if line.startswith("- ")]
    assert 3 <= len(bullets) <= 6

    metadata = (ROOT / "manuscript/operator_portability_submission_metadata.md").read_text(encoding="utf-8")
    assert "Package-ready development candidate" in metadata
    assert "Author list/order: [pending]" in metadata
    assert "Short Communication" in metadata

    cover = (ROOT / "manuscript/operator_portability_cover_letter.md").read_text(encoding="utf-8")
    assert "SUBMISSION GATE" in cover
    assert "AUTHOR INPUT REQUIRED" in cover

    checklist = (ROOT / "manuscript/operator_portability_submission_checklist.md").read_text(encoding="utf-8")
    assert "Materialized final Figure 1" in checklist
    assert "Submission bundle archive generated" in checklist

    print(f"Operator-portability submission checker PASS: abstract={abstract_n} words, manuscript={total_n} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
