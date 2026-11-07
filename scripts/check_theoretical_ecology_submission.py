#!/usr/bin/env python3
"""Fail-closed scientific and editorial structure audit of active TE manuscript."""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "manuscript/theoretical_ecology_article.md"
COVER = ROOT / "manuscript/theoretical_ecology_cover_letter.md"
REFS = ROOT / "manuscript/theoretical_ecology_references.md"
ROUTER = ROOT / "manuscript/publication_lanes.json"
FIGURE_PLAN = ROOT / "manuscript/nee_flagship_display_plan.md"

def main() -> None:
    registry = json.loads(ROUTER.read_text(encoding="utf-8"))
    assert len(registry["active_lanes"]) == 1
    active = registry["active_lanes"]["nee_flagship"]  # retained legacy key
    assert active["primary_target"] == "Theoretical Ecology"
    assert active["manuscript"] == "manuscript/theoretical_ecology_article.md"
    paper = PAPER.read_text(encoding="utf-8")
    cover = COVER.read_text(encoding="utf-8")
    assert paper.startswith("# Fragmentation separates biological states")
    assert paper.index("## Abstract") < paper.index("## Keywords") < paper.index("## Results")
    assert paper.index("## Results") < paper.index("## Discussion") < paper.index("## Methods")
    assert paper.index("## Figure captions") < paper.index("## References") < paper.index("## Statements and Declarations")
    abstract = paper.split("## Abstract", 1)[1].split("## Keywords", 1)[0].strip()
    words = len(abstract.split())
    assert 150 <= words <= 250, words
    kw_line = paper.split("## Keywords", 1)[1].splitlines()[2]
    keywords = [x.strip() for x in kw_line.split(";")]
    assert 4 <= len(keywords) <= 6 and all(keywords)
    assert max(len(m.group(1)) for m in re.finditer(r"(?m)^(#+) ", paper)) <= 3
    main = paper.split("## References", 1)[0]
    for n in range(1, 5):
        assert f"**Fig. {n}**" in main, n
        assert re.search(rf"\bFig\. {n}\b", main), n
    first_occurrence = [main.index(f"(Fig. {n}") for n in range(1, 5)]
    assert first_occurrence == sorted(first_occurrence), first_occurrence
    refs = paper.split("## References", 1)[1].split("## Statements and Declarations", 1)[0].strip()
    independent = REFS.read_text(encoding="utf-8").split("\n\n", 1)[1].strip()
    assert refs == independent, "Standalone reference file and article diverged"
    entries = [line for line in refs.splitlines() if line.strip()]
    assert len(entries) >= 15
    assert len(entries) == len(set(entries))
    assert all("https://doi.org/10." in e for e in entries)
    surname_years = []
    for e in entries:
        m = re.match(r"^(\S+).*?\((19|20)\d{2}\)", e)
        assert m, e
        name = m.group(1)
        year = re.search(r"\((\d{4})\)", e).group(1)
        surname_years.append((name,year))
        if name == "Boettiger" and year == "2013":
            assert "Boettiger and Hastings 2012, 2013" in main
        else:
            assert re.search(re.escape(name) + r".{0,40}" + year, main), f"Uncited reference: {name} {year}"
    assert all(a <= b for a,b in zip([n for n,_ in surname_years], [n for n,_ in surname_years][1:])), "Reference list not alphabetical"
    assert all(key in paper for key in ("1,037/1,037", "0.2543", "+6.883",
                                        "1,920,000", "0.92734", "+0.02135",
                                        "0.23253", "directionally inverted"))
    assert "specificity 1" not in paper
    assert "0.92734" in FIGURE_PLAN.read_text(encoding="utf-8")
    for n in range(1, 6):
        assert re.search(rf"(?m)^{n}\. ", cover), f"Suggested reviewer {n} missing"
    assert "conflict" in cover.lower()
    assert "author" in cover.lower()
    assert "not externally validated" in paper or "natural strongest-refuge test" in paper
    assert "Funding:" in paper and "Competing interests:" in paper
    print(f"Theoretical Ecology content gate passed: {words} abstract words, "
          f"{len(keywords)} keywords, {len(entries)} cited references, "
          "four linked figure captions, five tentative reviewers; "
          "authors' approval and true journal-layout visual check still pending.")
if __name__ == "__main__":
    main()
