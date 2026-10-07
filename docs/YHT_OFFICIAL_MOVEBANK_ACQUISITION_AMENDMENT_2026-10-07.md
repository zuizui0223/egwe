# YHT official Movebank acquisition amendment — 2026-10-07

Status: **locked before official raw-event acquisition and before any demographic outcome join.**

The original protocol required timestamps with an explicit UTC offset in the local CSV coverage checker. Official Movebank event exports may serialize the canonical `timestamp` field without an explicit suffix even though the Movebank timestamp field is defined in UTC.

For the **official Movebank Data Repository DOI only** (`10.5441/001/1.5g4h5t6c`), the acquisition workflow therefore interprets timezone-naive canonical `timestamp` values as UTC before converting them to `America/Edmonton`.

This is a source-format normalization, not a change to:

- the Sep 15–Nov 15 window;
- nearest-noon logic;
- 6.5-hour offset;
- n>=10 daily gate;
- >=30-day annual gate;
- fixed-n metric design;
- primary endpoint;
- forecast model;
- or STOP rule.

The workflow downloads the deposit through the anonymous Movebank Data Repository DSpace REST API, checks for exactly one event CSV containing the four frozen fields, computes movement-only coverage, records the source-file SHA256, and uploads **only the aggregate coverage JSON**. Raw locations are not committed or retained as a GitHub Actions artifact.
