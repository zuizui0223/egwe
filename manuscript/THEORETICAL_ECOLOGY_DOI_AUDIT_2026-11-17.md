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
