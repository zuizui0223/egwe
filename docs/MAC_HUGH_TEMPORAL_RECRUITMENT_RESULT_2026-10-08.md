# Mac Hugh caribou: year-forward recruitment result

Date: 2026-10-08

**Decision: `no_incremental_temporal_forecast_gain_detected`**

## What was done

We audited the **source-defined longitude variance of spring migration routes** as a predictor of **calf recruitment in the following autumn** of the same calendar year, in the Rivière-aux-Feuilles caribou herd.

The official Borealis source `10.5683/SP3/0ROESU` was MD5-matched (`3ac1d2d5c7f64b182567829c0f2e28ac`). Before this project's row-level outcome opening, the comparison and STOP rules were fixed in `experiments/mac_hugh_recruitment_temporal_protocol.json` (commit `66ea48a7844135e0305129b25a4535ab8b2e6e57`). We already knew the published original paper's weak/null AICc finding; the new result is a **constrained retrospective temporal holdout**, not outcome-blind independent preregistration.

The source has 26 annual records. Requiring the actual previous calendar year's recruitment and complete current-year spatial/effort fields left **23 valid lagged observations**. Starting from the first seven training observations, 16 future years (2004–2019) were predicted sequentially, without leakage or missing-year imputation.

### Frozen comparison

- `M0: Recrutement_y ~ Recrutement_(y-1) + Nb_femelle_y`
- `M1: M0 + Variance_long_y`

Both models used expanding-window OLS, training-fold-only predictor standardization and identical held-out years.

## Results

| error measure | M0 (past recruitment + observation effort) | M1 (+ spring-route longitude variance) |
|---|---:|---:|
| RMSE | **13.30886** | 13.81488 |
| MAE | **11.46473** | 11.51439 |

The mean paired yearly squared-error improvement `M0−M1` was **−13.72499**, also favouring the baseline.

The predeclared positive criterion required improvement in both RMSE and MAE. **Neither improved.** No spatial-predictive gain was detected.

No p-value or cross-herd uncertainty is claimed; this is one herd and 16 temporally held-out years. No row-level recruitment values or predictions were redistributed.

## Ecological interpretation

For this herd and this published geographic coordinate, spring migration-route longitude variance did **not** convey additional transferable information about fall recruitment after preceding-year recruitment and monitoring effort were supplied.

This finding agrees with Mac Hugh et al.'s original conclusion that route geography was not clearly linked to recruitment, but applies an additional **time-forward out-of-sample comparison** rather than same-series candidate-model AICc.

It does **not** show that migration, cohesion or dispersal are ecologically irrelevant. The movement route may respond to environmental conditions without containing usable information for this specific reproductive outcome at an annual horizon.

Crucially, `Variance_long` is **not Love & Otto's `CV_ind/CV_pop`**. It measures one geography/dispersion aspect of migration routes, not instantaneous inter-individual distance structure. The Love–Otto wild future-demography validation question remains open.

## Provenance and inferential firewalls

- Official data: Borealis `10.5683/SP3/0ROESU`, file ID `984869`, MD5 `3ac1d2d5c7f64b182567829c0f2e28ac`.
- Source study: Mac Hugh et al. (2026), *Ecosphere* 17:e70553, DOI `10.1002/ecs2.70553`.
- Protocol locked before outcome analysis: commit `66ea48a7844135e0305129b25a4535ab8b2e6e57`.
- Analysis workflow `37725277766`, artifact `11527433443`, ZIP digest `sha256:00431c80be5c733160d56bc1a02856bc35148c5e3ce7a26536d92f60bfba3210`.
- Machine-readable compact result: `artifacts/mac_hugh_recruitment/temporal_result_locked.json`.

No source row-level outcome data are committed. The data license is CC BY-NC 4.0. The NEE finite-model evidence is not reclassified; this is an independent, bounded empirical nearest-neighbor audit.
