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

### Source-managed GPS quality gate

Because the Love–Otto IID metrics are sensitive to isolated coordinate errors, the primary movement state respects Movebank's source-managed QC rather than inventing an outcome-facing threshold. Records with `visible=false` are excluded when the field is present, and non-GPS sensor rows are excluded when `sensor-type` is present. No `gps:dop` threshold is added to the primary analysis. Any stricter DOP-based filter can only be a predeclared sensitivity and cannot replace the primary result.
