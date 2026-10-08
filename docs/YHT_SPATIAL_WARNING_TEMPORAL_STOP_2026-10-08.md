# Ya Ha Tinda: frozen primary stops at source–outcome temporal overlap

Date: 2026-10-08

Status: **STOP_PRIMARY_NOT_IDENTIFIABLE_ARCHIVE_TEMPORAL_OVERLAP**. No demographic outcomes, official Movebank events, or future-demography prediction model were opened or fitted to reach this decision.

## Decision

The originally frozen Ya Ha Tinda protocol requires **at least 11 eligible annual forecasts**. It fixes:

- an autumn spatial state in calendar year `t` (September 15–November 15);
- an outcome consisting of the **observed** calf:cow ratio in February–March of calendar year `t+1`;
- the calf:cow series in Dryad `10.5061/dryad.6wwpzgmw7` as the **only primary demographic source**.

The Dryad version referenced by this protocol was **published July 21, 2020**. Source: [the dataset's version listing](https://datadryad.org/dataset/doi%3A10.5061/dryad.6wwpzgmw7).

Consequently, observations from February–March **2021** cannot be part of this 2020 archive version. The spatial year **2020** is impossible as a paired `t -> t+1` forecast in the frozen protocol, regardless of whether full 2020 GPS data can eventually be downloaded.

The nominal GPS years identified from the published annual collar summaries were:

`2004–2006, 2013–2020` (11 candidate years).

Removing 2020 leaves a **strict upper bound of 10 candidate years**:

`2004–2006, 2013–2019`.

The frozen protocol requires 11. Hence it is mathematically impossible for this fixed pair of source versions to meet the predeclared denominator.

This is a source-alignment **STOP**, not a demographic forecast null and not an ecological statement that the Love–Otto spatial metric lacks predictive value.

## Why acquiring official GPS does not solve this primary

The candidate-year bound is already **optimistic**: it assumes every nominal year through 2019 has enough qualifying adult-female autumn GPS fixes *and* a valid matching calf:cow observation. The actual row-level date and join gates can only remove years, not create the missing 2021 observation.

The public teaching subset `EliGurarie/BrazilMove2024` independently contains only 2001–2005 and is already excluded as an official 2001–2020 replacement. Its mirror-only diagnostic found one eligible year (2004) but cannot rescue the registered primary.

Therefore **do not request an official Movebank export from the user to rescue this specific registered analysis**.

## Root-cause audit

1. **Failure location:** independent source periods and the frozen lagged outcome were not joined at the metadata stage.
2. **Cause:** the original pre-acquisition feasibility check counted nominal GPS years only, giving 11, without removing years whose *following-year demographic observations* did not exist in the pinned 2020 archival release.
3. **Correction:** a deterministic metadata-only temporal gate checks the source publication date against the complete February–March response window.
4. **Revalidation:** the corrected upper bound is 10 (< 11), so the primary ends at `STOP_PRIMARY_NOT_IDENTIFIABLE_ARCHIVE_TEMPORAL_OVERLAP` without inspecting response values.

## Scientific claim ceiling

Love & Otto (2026) demonstrably detects within-population spatial reorganization, but this Ya Ha Tinda protocol has **not tested** whether that score predicts later recruitment. No positive or negative prediction-performance conclusion is possible.

A later release containing post-2020 recruitment observations, or a different long-term wild dataset, would need a **distinct prospectively declared source/validation route**. It must not be used to retroactively pass this original experiment by changing the date/source/replication rule.

## Reproduction

```bash
python scripts/check_yht_temporal_overlap.py \
  --protocol experiments/yht_spatial_warning_protocol.json \
  --output artifacts/yht_spatial_warning/primary_temporal_overlap_stop.json
```

Code: `src/eco_genetic_warning_extensions/yht_temporal_overlap_gate.py`.

Committed result: `artifacts/yht_spatial_warning/primary_temporal_overlap_stop.json`.

No outcomes, GPS coordinates or demographic values are read by this calculation.
