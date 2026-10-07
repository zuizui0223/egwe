# Ya Ha Tinda timestamp-semantics amendment

Date: 2026-10-08

Status: **source-format amendment frozen before official Ya Ha Tinda event-table content was opened and before any movement–demography model fit.**

Movebank's official API documentation states that all dates in Movebank are stored in UTC. Archived CSV exports can represent that source semantic without an explicit ISO timezone suffix.

The frozen parser therefore keeps two distinct rules:

1. timestamps with an explicit timezone/offset are parsed normally;
2. timezone-naive timestamps are interpreted as UTC **only** when the analyst explicitly enables `--official-movebank-utc-semantics` for the official Movebank archive.

Mirrors and other inputs with timezone-naive timestamps continue to fail closed.

This amendment does not change the Sep 15–Nov 15 window, noon snapshot, 6.5-hour tolerance, n=10 daily gate, 30-day annual gate, Love–Otto metric, demographic endpoint, forecast horizon, model, or STOP rule. It prevents a file-format representation detail from being confused with uncertainty about the underlying time standard.
