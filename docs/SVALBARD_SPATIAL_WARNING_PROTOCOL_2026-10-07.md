# Svalbard reindeer test of Love–Otto future-demography warning

Date: 2026-10-07

Status: **locked retrospective temporal-validation contract before row-level GPS/annual-abundance joining or model fitting.**

## Why this system

Love & Otto (2026) validate inter-individual-distance CV metrics as indicators of spatial fragmentation/cohesion, but their wild examples do not ask whether the score predicts a later demographic outcome.

The Svalbard reindeer archive is unusually close to the missing test. One Dryad deposit contains:

- GPS locations from adult females during 2009–2023;
- 135 tracked individuals and 419 animal-years;
- 319,774 locations;
- 12–48 GPS-collared females per year;
- independent annual population estimates `N.tot` derived from long-term capture–mark–recapture plus summer census information.

The deposit therefore allows a temporal test within one wild population rather than a cross-sectional state-classification exercise.

The published abstract already states that abundance increased strongly during the study period. This analysis is consequently **not outcome-blind**. The firewall is narrower: exact annual `N.tot`, row-level GPS positions, Love–Otto annual metrics and their predictive relationship are not inspected before this contract.

## Frozen spatial state

Source: Dryad `10.5061/dryad.4qrfj6qkx`.

GPS file: `ReindeerGPSloc_2009_2024.csv`.

The README documents UTC timestamps and x/y coordinates in UTM zone 33. Published coordinates have reduced spatial precision; that coarsening is retained exactly.

For each calendar year:

1. retain 15 September–15 November;
2. for each individual-day, choose the recorded fix nearest 12:00 UTC;
3. require absolute distance from noon <=6 h;
4. do not interpolate;
5. day eligible only with >=10 unique females;
6. year eligible only with >=30 eligible days.

Love & Otto explicitly simulated sample size 10, so 10 is the fixed minimum rather than a threshold chosen from these data.

For every eligible day with >10 females, create 100 deterministic n=10 subsamples. IDs are ordered by SHA256 of `date|replicate|id`, and the first 10 are used.

Primary metric:

[
C_t = operatorname{mean}_{days}left(CV_{ind}/CV_{pop}ight).
]

The exact formulas are already pinned in `love_otto_spatial_metrics.py` to `nicolalove/shapeshiftr@e3898257`.

The same subsamples yield mean pairwise distance, averaged across days as the contemporaneous spatial-scale baseline.

## Frozen demographic endpoint

The workbook `SvalbardReindeerGrazingData_ArcticSceince2024.xlsx` contains `N.tot`, the annual estimated reindeer abundance in the study area.

For each calendar year, the extractor must find exactly one unique finite positive `N.tot` after deduplicating repeated plot rows. Multiple distinct values within a year are an ambiguity STOP.

For predictor year `t`, the endpoint is:

[
g_{t+1}=log(N_{t+1}/N_t).
]

Only adjacent calendar years are valid transitions.

## Primary predictive test

Baseline:

[
M_0:g_{t+1}sim log N_t+log(	ext{spatial scale}_t).
]

Spatial-warning model:

[
M_1:g_{t+1}sim log N_t+log(	ext{spatial scale}_t)+C_t.
]

The models are ordinary least squares with intercept and no tuning.

Validation is rolling-origin, one-year ahead. Predictors are standardized from training years only. The first seven eligible transitions form the initial training set; each later transition is forecast using only earlier eligible transitions.

Primary analysis requires >=11 eligible adjacent-year transitions, yielding >=4 held-out forecasts.

A positive decision requires **both** lower RMSE and lower MAE for M1. Otherwise the frozen result is `no_detected_incremental_future_information`.

## Prespecified sensitivities

Only after the primary result is written:

- substitute `cvpop` and `cvind` separately for the ratio;
- recompute spatial metrics using all eligible collared females rather than fixed n=10;
- add previous annual growth to both models where available;
- add a linear calendar-year term to both models.

None may replace a failed primary.

## Interpretation

A positive result would answer the specific gap left by Love & Otto:

> a spatial-cohesion metric measured before the outcome adds information about later wild-population growth beyond the current population level and contemporaneous spatial scale.

A null is equally informative: a metric can detect spatial organization without earning predictive early-warning status.

Neither result establishes causality or cross-species generality.
