#!/usr/bin/env python3
"""Independent DOI metadata audit for the active Theoretical Ecology reference list.

This is a bibliographic QA check, not a biological/evidence validation.
Crossref is an automated discovery source; publisher record remains decisive.
No reference is silently rewritten.
"""
from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import html
import json
import os
from pathlib import Path
import re
import sys
import time
import unicodedata
from urllib import error, parse, request

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "manuscript" / "theoretical_ecology_references.md"
PAPER = ROOT / "manuscript" / "theoretical_ecology_article.md"
DOI_RE = re.compile(r"https://doi\.org/(10\.\S+)$", re.I)
YEAR_RE = re.compile(r"\((\d{4})\)")
VENUE_RE = re.compile(r"(?P<title>.+)\.\s+\*(?P<journal>[^*]+)\*\s+(?P<volume>\d+):")


def normal(value: str) -> str:
    value = re.sub(r"<[^>]*>", " ", html.unescape(str(value)))
    value = re.sub(r"\*+", "", value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def parse_entry(entry: str) -> dict:
    doi_match = DOI_RE.search(entry.strip())
    year_match = YEAR_RE.search(entry)
    if not (doi_match and year_match):
        raise ValueError(f"Reference missing DOI/year: {entry}")
    name = entry.split()[0]
    lead = entry[year_match.end(): doi_match.start()].strip()
    venue = VENUE_RE.search(lead)
    if not venue:
        raise ValueError(f"Cannot identify title/journal/volume: {entry}")
    return {
        "first_author": name,
        "year": int(year_match.group(1)),
        "title": venue.group("title"),
        "journal": venue.group("journal"),
        "volume": venue.group("volume"),
        "doi": doi_match.group(1).rstrip(".,;"),
        "original": entry,
    }


def pub_years(work: dict) -> list[int]:
    years = set()
    for key in ("published-print", "published-online", "published", "issued"):
        block = work.get(key) or {}
        parts = block.get("date-parts") or []
        if parts and parts[0] and isinstance(parts[0][0], int):
            years.add(parts[0][0])
    return sorted(years)


def judge(entry: dict, work: dict) -> dict:
    canonical_title = (work.get("title") or [""])[0]
    authors = work.get("author") or []
    family = authors[0].get("family", "") if authors else ""
    score = round(SequenceMatcher(None, normal(entry["title"]), normal(canonical_title)).ratio(), 4)
    author_ok = normal(entry["first_author"]) == normal(family)
    years = pub_years(work)
    year_ok = entry["year"] in years
    volume_online = str(work.get("volume", "")).strip()
    volume_ok = not volume_online or volume_online == entry["volume"]
    metadata_doi = str(work.get("DOI", "")).lower()
    doi_ok = entry["doi"].lower() == metadata_doi
    flags = []
    if not doi_ok:
        flags.append("doi_mismatch")
    if score < 0.87:
        flags.append("title_mismatch")
    elif score < 0.98:
        flags.append("title_punctuation_or_variant_review")
    if not author_ok:
        flags.append("first_author_mismatch")
    if not year_ok:
        flags.append("year_check_required")
    if not volume_ok:
        flags.append("volume_check_required")
    severe = {"doi_mismatch", "title_mismatch", "first_author_mismatch"}
    verdict = ("mismatch" if severe.intersection(flags)
               else "review" if flags else "verified")
    return {
        "doi": entry["doi"], "first_author": entry["first_author"],
        "year": entry["year"], "verdict": verdict, "flags": flags,
        "crossref_title": canonical_title,
        "crossref_first_author": family, "crossref_years": years,
        "crossref_volume": volume_online, "title_similarity": score,
    }


def lookup(doi: str, retries: int = 2) -> dict:
    url = "https://api.crossref.org/works/" + parse.quote(doi, safe="")
    req = request.Request(
        url, headers={"Accept": "application/json",
                      "User-Agent": "EGWE-bibliography-QA/1.0 (https://github.com/zuizui0223/egwe)"},
    )
    for attempt in range(retries + 1):
        try:
            with request.urlopen(req, timeout=18) as response:
                data = json.load(response)
            return data["message"]
        except (error.HTTPError, error.URLError, TimeoutError, ValueError) as ex:
            retryable = not isinstance(ex, error.HTTPError) or ex.code in (429, 500, 502, 503, 504)
            if not retryable or attempt == retries:
                raise RuntimeError(f"{type(ex).__name__}: {ex}") from ex
            time.sleep(attempt + 1.5)
    raise RuntimeError("Unexpected lookup exhaustion")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("reference_audit"))
    ap.add_argument("--limit", type=int, default=None, help="Optional smoke-test subset")
    args = ap.parse_args()
    refs = REFS.read_text(encoding="utf-8").split("\n\n", 1)[1].strip()
    paper_refs = PAPER.read_text(encoding="utf-8").split("## References\n\n", 1)[1].split(
        "\n## Statements and Declarations", 1
    )[0].strip()
    if refs != paper_refs:
        print("FAIL: Article bibliography and standalone references differ", file=sys.stderr)
        return 1
    entries = [parse_entry(e.strip()) for e in refs.split("\n\n") if e.strip()]
    if len(entries) != 28:
        print(f"FAIL: Expected 28 references, found {len(entries)}", file=sys.stderr)
        return 1
    if len({e["doi"].lower() for e in entries}) != 28:
        print("FAIL: Duplicate DOI", file=sys.stderr)
        return 1
    selected = entries[:args.limit] if args.limit else entries
    rows = []
    for ix, entry in enumerate(selected, 1):
        try:
            row = judge(entry, lookup(entry["doi"]))
        except Exception as ex:
            row = {
                "doi": entry["doi"], "first_author": entry["first_author"],
                "year": entry["year"], "verdict": "unverified",
                "flags": ["metadata_unavailable"], "reason": str(ex),
            }
        rows.append(row)
        print(f"{ix:02d}/{len(selected):02d} {row['verdict'].upper():10s} "
              f"{row['first_author']} ({row['year']}) {row['doi']} "
              f"{'; '.join(row['flags'])}", flush=True)
        time.sleep(0.2)
    counts = {kind: sum(r["verdict"] == kind for r in rows)
              for kind in ("verified", "review", "mismatch", "unverified")}
    audit = {"source": "Crossref automatic metadata, not publisher proof",
             "expected_total": len(entries), "checked": len(selected),
             "counts": counts, "results": rows}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "reference_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# Theoretical Ecology reference metadata cross-check",
          "", "Automated Crossref metadata only; publisher pages are authoritative.",
          "A network failure is not evidence that a reference is wrong.",
          f"Checked {len(rows)}/{len(entries)}: " + ", ".join(f"{k}={v}" for k, v in counts.items()),
          "", "| DOI | Verdict | Notes |", "|---|---|---|"]
    md.extend(f"| {r['doi']} | {r['verdict']} | {', '.join(r['flags']) or 'matched'} |" for r in rows)
    (args.output / "reference_audit.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")
    print("SUMMARY " + json.dumps(counts, sort_keys=True))
    # Flag discrepancies and incomplete metadata, but never auto-correct bibliography.
    return 1 if counts["mismatch"] or counts["review"] or counts["unverified"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
