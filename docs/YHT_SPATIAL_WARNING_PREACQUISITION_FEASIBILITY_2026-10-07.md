# Ya Ha Tinda spatial-warning pre-acquisition feasibility audit

Date: 2026-10-07

Status: **movement-sample feasibility only; no row-level GPS data or demographic outcomes opened.**

## Purpose

Before obtaining official raw bytes, ask whether the frozen Love–Otto `n>=10` daily sampling rule is even plausible from published annual telemetry summaries.

This is not the protocol's actual coverage test. The actual test still requires daily timestamps and the frozen nearest-noon / >=30 eligible-days rules.

## Published annual GPS sample counts

The Ya Ha Tinda 2018–2019 annual report gives the following total numbers of GPS-collared adult female elk:

| year | GPS-collared females |
|---:|---:|
| 2002 | 4 |
| 2003 | 8 |
| 2004 | 25 |
| 2005 | 11 |
| 2006 | 14 |
| 2007 | 9 |
| 2008 | 0 |
| 2009 | 7 |
| 2010 | 6 |
| 2011 | 6 |
| 2012 | 3 |
| 2013 | 22 |
| 2014 | 30 |
| 2015 | 25 |
| 2016 | 48 |
| 2017 | 47 |
| 2018 | 50 |
| 2019 | 45 |

The 2017–2021 final report gives **54 active GPS collars in 2020**.

Thus the years that can *possibly* satisfy the frozen daily `n>=10` gate are:

`2004, 2005, 2006, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020`.

That is exactly **11 nominal candidate years**.

## Consequence for the frozen protocol

The primary protocol requires at least 11 eligible annual observations.

Therefore there is **zero nominal slack** in the annual sample count:

> if any one of these eleven years fails the raw daily nearest-noon / >=30 eligible-days coverage gate, the primary Ya Ha Tinda rolling-origin test stops for insufficient temporal replication.

We do not lower the daily n threshold, annual-day threshold, initial training size or total-year requirement to rescue the analysis.

## Why later years are likely but not guaranteed to pass

Published telemetry summaries report thousands of GPS fixes per elk-year in many early GPS years. Since 2017, deployed GPS collars were generally scheduled at approximately one location every 13 hours. This makes repeated autumn snapshots plausible.

But annual collar count is not equivalent to simultaneous daily coverage. Collar failure, deployment/retrieval timing and missing fixes can reduce the actual number of unique females within the frozen noon window. Only the raw movement-side checker can decide eligibility.

## Sources

- Ya Ha Tinda Elk Project Annual Report 2018–2019, telemetry Table 3.
- Ya Ha Tinda Elk Final Report 2017–2021, telemetry Table 1.4.
- Official Movebank archive study: `study897981076`, DOI `10.5441/001/1.5g4h5t6c`.

## Acquisition boundary

The official Movebank study is marked public `data`, but automated raw-event retrieval in the current execution environment did not complete. Dryad binary download similarly failed at the environment/network layer.

No unofficial data mirror will be substituted. Once official raw bytes are available, the first permitted computation is:

```bash
python scripts/check_yht_spatial_warning_coverage.py \
  --movebank-csv <official_movebank_csv> \
  --output artifacts/yht_spatial_warning/movement_coverage.json
```

This checker does not read demographic outcomes.
