# Theoretical Ecology DOI bibliography audit

This independent QA lane compares all **28** DOI records in the currently active
standalone bibliography with their counterparts embedded in
`manuscript/theoretical_ecology_article.md`.

The audit requests Crossref metadata for each DOI and checks the first author's
family name, title similarity, publication year and volume. It writes
machine-readable JSON and human-readable Markdown under `reference_audit/`
and a GitHub Actions job summary. It does **not** modify references automatically.

Interpretation:

- **verified**: metadata agrees under the declared checks.
- **review**: title variant, year or volume differs; compare the version of record.
- **mismatch**: DOI, first author or article title disagrees strongly; check source.
- **unverified**: Crossref API unavailable; neither positive nor negative evidence.

A clean check is a bibliographic metadata test, **not** proof of the article's
scientific interpretation, full coauthor approval or submission readiness. Metadata
may diverge from published publisher records, which take precedence.

Run locally (network required): `python scripts/audit_theoretical_ecology_references.py --output reference_audit`.

This audit must not rewrite historical frozen simulation results or modify the
single active Theoretical Ecology submission route.

## First audit finding and repair

The first GitHub run (44007063681) returned **27 verified / 1 metadata mismatch**.
The sole flagged record was *Kaiser-Bunbury et al.* (2010), DOI
`10.1111/j.1461-0248.2009.01437.x`. Its publisher version of record
(https://onlinelibrary.wiley.com/doi/10.1111/j.1461-0248.2009.01437.x)
confirms the first-author surname exactly as printed in the existing bibliography.
The scanner mistakenly treated a typographic Unicode hyphen as a different
surname. The reference itself is unchanged; the scanner now normalizes Unicode
dash codepoints before comparison, with an offline regression test.

The initial failure is a **metadata-normalization false positive**, not a new
scientific finding. An updated full-run pass is still required.
