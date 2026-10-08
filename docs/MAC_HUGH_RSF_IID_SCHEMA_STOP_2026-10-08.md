# Mac Hugh raw RSF archive — Love–Otto simultaneous-position schema gate

Date: 2026-10-08

**Decision: `not_identifiable_from_rsf_schema`.** No raw observation row or recruitment response was read.

## Official source

- Borealis DOI: `10.5683/SP3/0ROESU`.
- File: `Dataset_RSF_1994-2019.txt`, ID `984868`; published manifest MD5 `82900917b0d53024209540df9aea2845` (manifest only, not independently verified against all 106 MB).
- Successful response-firewalled GitHub Actions header probe: run `37725949373`, job `113144017431`, source-schema-only artifact `11527988583`.
- Machine snapshot: `artifacts/mac_hugh_recruitment/rsf_iid_schema_gate.json`.

## Exact header result

The file exposes 12 columns: `annee`, `y_var`, `altitude`, `precipitations`, `neige`, `Hab_Water`, `Hab_Shrub_tundra`, `Hab_Erect_shrub_tundra`, `Hab_Tundra`, `Hab_Other`, `Hab_Forest`, `Hab_Lichen_heaths`.

The only recognized temporal coordinate is the calendar year `annee`.

The header has **no recognizable individual ID, timestamp/clock, or explicit X/Y position fields**, so the essential three-way join for instantaneous inter-individual-distance calculations is unavailable.

A generic outcome variable (`y_var`) is not treated as latitude/y-coordinate, and `annee` cannot establish co-timed animal locations.

## Biological interpretation and firewall

This file cannot directly reproduce Love & Otto's `CV_ind/CV_pop` from contemporaneous individual positions. The result is **schema insufficiency**, not a failure of the Love–Otto indicator or a negative biological forecast result. It does not prove that no other companion file contains usable locations.

The independent Mac Hugh source-defined **longitude-variance** temporal forecast already showed no incremental recruitment gain (baseline RMSE 13.30886, augmented RMSE 13.81488), but that statistic is different from Love & Otto's CV and cannot substitute for it.

No dataset outcome values, recruitment records, fitted coefficients or animal GPS observations were processed by this probe. Official raw data are not redistributed.
