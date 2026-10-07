# Ya Ha Tinda public-mirror acquisition boundary

Date: 2026-10-07

Status: **acquisition/provenance audit only; no demographic outcome values opened and no Love–Otto future-demography model fit.**

## Purpose

The frozen Ya Ha Tinda spatial-warning protocol requires the full 2001–2020 female GPS archive. The official Movebank study is publicly listed as:

- study ID `897981076`;
- 175 animals;
- 1,585,430 valid GPS locations;
- 2001–2020;
- public visibility `data`.

Direct automated event download remains blocked by the Movebank login/license-acceptance interface in the present execution environment. This audit records two public redistributions that were found while attempting to recover the data without weakening provenance.

## Researcher teaching mirror

Repository:

`EliGurarie/BrazilMove2024`

Pinned commit:

`447d2882e8d14a67db429a6ef74c307dd2354866`

File:

`data/Elk_GPS_data.csv`

Pinned Git blob:

`2d5e8b124bc02b63a7b2f171004c7027b412cbe3`

The course page explicitly identifies this file as elk data also available from Movebank study `897981076` and thanks the Ya Ha Tinda project investigators.

Direct blob inspection gives:

- 138,433 rows;
- 31 unique GPS individuals;
- years 2001–2005 only;
- row counts:
  - 2001: 130
  - 2002: 11,194
  - 2003: 36,323
  - 2004: 88,097
  - 2005: 2,689

Therefore this is a **teaching subset**, not an admissible replacement for the official 2001–2020 archive.

The CSV timestamp strings themselves are timezone-naive, but a second researcher teaching source in the same Ya Ha Tinda/Movebank workflow (`EliGurarie/MovementEcologyBook`) explicitly parses Ya Ha Tinda timestamps with `tz="UTC"`, including the U.S.-style `mdy_hms(..., tz="UTC")` case. This supports a **mirror-only UTC diagnostic** without changing the primary protocol, which still requires an official or provenance-complete full archive.

### 2004 strict frozen-window diagnostic

Treating the mirrored timestamps as UTC exactly as documented in that teaching workflow, then converting to `America/Edmonton` and applying the frozen 15 September–15 November, nearest-local-noon (<=6.5 h), and >=10-individual rules gives:

- days with any accepted mirrored fix in the window: **62**;
- eligible days with >=10 unique females: **43**;
- maximum accepted daily individuals: **12**;
- mean accepted individuals across eligible days: **10.88**;
- first eligible day: **2004-09-15**;
- last eligible day: **2004-10-31**.

Thus **2004 passes the frozen >=30-day movement-side gate in this teaching mirror**. However the mirror contains only 2001–2005, and 2002/2003 never reach 10 individuals under the same gate. It therefore supplies only one eligible annual state and remains unusable for the >=11-year primary forecast.

## Zenodo COVID-19 spatial redistribution

The supplementary materials for Tucker et al. (2023), *Science*, list Ya Ha Tinda elk study `897981076` as available in Zenodo record `10.5281/zenodo.7704108`.

Independent repository documentation identifies the open spatial file as:

`Tucker_Road_Spatial.rds`

and states that the contributed records cover **February–May 2019 and 2020** for the COVID-19 analysis.

This redistribution is useful provenance confirmation but does not span the frozen September–November window across enough years and therefore cannot run the long-term future-demography test.

## Consequence

Neither public redistribution replaces the official long-term archive:

- the BrazilMove2024 file is temporally restricted to 2001–2005 and loses timezone metadata;
- the Tucker spatial redistribution is restricted to the COVID comparison window in 2019–2020.

The main protocol therefore remains unchanged and unopened with respect to future demographic outcomes.

## Remaining admissible acquisition routes

1. official Movebank export after accepting the study license/terms;
2. an author-provided export explicitly documented as the same study/version;
3. another immutable public redistribution only if it contains the required 2001–2020 events with timestamp timezone/UTC semantics and can be tied unambiguously to study `897981076`.

Do **not** concatenate the teaching subset and COVID subset to manufacture long-term coverage.
