# Ya Ha Tinda prospective-style spatial-warning test

Date: 2026-10-07

Status: **primary analysis STOPPED before demographic outcome fitting** — official Movebank GPS coverage permits 8 movement years, but only 6 overlap the frozen recruitment series, below the required 11. The original pre-outcome contract remains frozen.

This is deliberately not called an outcome-blind preregistration. Public reports already reveal broad Ya Ha Tinda population history and some annual counts. The important firewall is narrower: the exact Love–Otto metric construction, movement sampling rules, primary demographic endpoint, forecast model, validation scheme and STOP rules are fixed before this project opens the row-level GPS × calf:cow outcome join.

## Final primary execution decision (2026-10-08)

The official Movebank GPS archive was downloaded to ephemeral GitHub Actions runners and subjected to the **unchanged** Sep 15–Nov 15 / nearest-noon ±6.5h / daily n≥10 / ≥30-day annual coverage gate. Two independent successful workflow runs recovered the same event CSV SHA256 (`1069cd7531d1d7a519cb817b09d015be91c552ecafab504869a81eb01eff4201`) and the same eight eligible movement years: 2004 and 2013–2019.

The frozen Dryad `YHT_CalfCowRatioData.csv` has a published series through late winter 2018. Under the original autumn t → late-winter t+1 forecast, the true movement–outcome overlap is just **2004 and 2013–2017: 6 years**. This is less than the locked minimum of 11, so **no demographic outcome rows were inspected and no future-prediction model was fitted**.

The original analysis specification below is preserved as an auditable pre-result contract. It is not reopened or relaxed. Provenance and the machine-readable final decision are at `docs/YHT_OFFICIAL_MOVEBANK_COVERAGE_STOP_2026-10-08.md` and `artifacts/yht_spatial_warning/official_movebank_coverage_overlap_stop.json`.

## Question

Love & Otto (2026) show that inter-individual-distance CV metrics detect changes in population spatial organization and explicitly motivate them as early warning signals of population fragmentation.

The unresolved test is:

> **Does autumn spatial fragmentation/cohesion contain information about later demography after the immediately preceding demographic state and contemporaneous spatial scale are already known?**

Ya Ha Tinda is unusually suitable because the same long-term project provides:

- public GPS tracks of adult females from 2001–2020;
- annual calf:cow ratio data;
- minimum winter population counts;
- adult-female survival data;
- source-defined migratory classifications.

The test remains one herd through time, so even a positive result would be a first wild temporal validation rather than cross-population generality.

## Source locks

### Love–Otto metric

- Love & Otto (2026), *Methods in Ecology and Evolution*, DOI `10.1111/2041-210x.70375`.
- package repository: `nicolalove/shapeshiftr`.
- pinned source commit: `e38982570c76161593a44b70569aad70f283b5aa`.
- exact functions mirrored locally:
  - `cvpop = sd(all pairwise distances) / mean(all pairwise distances)`;
  - `cvind = sd(individual mean distance to all others) / mean(individual mean distance)`;
  - `cvratio = cvind/cvpop`.

The published simulation code evaluates sample sizes `10, 50, 75, 100, 500`. Therefore **10 individuals is the frozen minimum**. It is not adjusted to preserve more Ya Ha Tinda years.

### Movement

Movebank DOI: `10.5441/001/1.5g4h5t6c`.

The public archive contains approximately 1.58 million GPS locations from 175 female elk over 2001–2020.

### Demography

Dryad DOI: `10.5061/dryad.6wwpzgmw7`.

Primary file:

- `YHT_CalfCowRatioData.csv`.

Secondary files:

- `YHT_MinimumCountWinterElkSurveys.csv`;
- `YHT_AdultFemaleSurvivalRate.csv`.

## Frozen movement snapshot

The primary spatial state is measured **15 September–15 November** of calendar year `t`.

For every individual-day:

1. convert timestamps to `America/Edmonton`;
2. take the location nearest 12:00 local;
3. require an absolute offset no greater than 6.5 h;
4. if two fixes are equally close, take the earlier one;
5. do not interpolate missing fixes;
6. project coordinates to EPSG:26911.

A day is eligible only with at least **10 unique females**.

A year is eligible only with at least **30 eligible days**.

## Fixed-n sampling

Changing collar numbers are a major confound because early Ya Ha Tinda years have far fewer GPS animals than recent years.

Primary metrics therefore use exactly **10 females per eligible day**.

When more than 10 are available, take 100 deterministic subsamples. For replicate `b`, sort individual IDs by the SHA256 value of

`date | b | individual_id`

and retain the first 10. Average the metric over the 100 subsamples.

This makes sample size identical among years without outcome-dependent rarefaction.

The primary spatial score is **Love–Otto `cvratio`**. `cvpop` and `cvind` are frozen secondary metrics and cannot replace it after results.

The annual score is the arithmetic mean of daily scores across the autumn window, matching the seasonal-averaging logic used in the Love–Otto caribou case study.

The same fixed-n samples also yield mean pairwise distance, used as a contemporaneous **spatial-scale baseline**. This matters because the Love–Otto CVs are intentionally scale-free; any forecast gain should not simply be attributed to a larger current range.

## Primary demographic endpoint

The primary endpoint is the **calf:cow ratio measured in February–March after the autumn movement window**.

Thus autumn `t` predicts recruitment state in late winter `t+1`.

The immediately preceding February–March calf:cow ratio is available before the movement window and is treated as the current demographic baseline.

This endpoint is preferred to the minimum population count for the first test because the source documents annual aerial-count gaps in 2015 and 2018. Count growth remains a prespecified secondary outcome rather than being used opportunistically when available.

## Primary predictive comparison

Let `R_next` be the following late-winter calf:cow ratio, `R_previous` the prior late-winter ratio, `S` the autumn mean pairwise-distance scale, and `C` the autumn Love–Otto cvratio.

Baseline:

[
M_0: R_{next} sim R_{previous} + log S.
]

Spatial-warning model:

[
M_1: R_{next} sim R_{previous} + log S + C.
]

No hyperparameters are tuned.

Predictors are standardized using training years only.

Validation is **rolling-origin one-step-ahead**:

- the first seven eligible annual observations form the initial training set;
- predict the next eligible outcome;
- then add that year to training and repeat;
- no future year can enter an earlier forecast.

The primary analysis runs only if there are at least **11 eligible annual observations**, giving at least four true out-of-sample forecasts.

Primary scores:

- forecast RMSE;
- forecast MAE;
- paired yearly squared-error difference `M0 - M1`.

The frozen decision is:

- `detected_incremental_future_information` only if M1 improves **both** RMSE and MAE;
- otherwise `no_detected_incremental_future_information`.

Because this is one herd with a small annual denominator, a positive result is not upgraded into a universal effect or a calibrated population-collapse threshold.

## Prespecified sensitivities

Only after the primary result is recorded:

1. repeat M1 separately with `cvpop` and `cvind`;
2. repeat metrics using all eligible collared females instead of fixed n=10;
3. on years with a current minimum count, add `log(N_current)` to both models;
4. if source-defined migration classifications join cleanly, add current resident fraction to both models.

The fourth test is important biologically. Ya Ha Tinda has undergone major changes in migratory tactics. If cvratio loses forecast gain after resident fraction is supplied, the spatial metric may primarily be a compression of known migration composition rather than an independent warning coordinate.

## Secondary endpoints

### Minimum population count growth

[
g = log(N_{next}/N_{current}).
]

Run only if at least six complete consecutive count transitions survive all movement gates. Missing aerial-survey years are not interpolated. This endpoint remains secondary and cannot replace a failed primary recruitment test.

### Adult female survival

Use only a source-defined herd-level annual survival field if the file contains one. Do not create a post-hoc weighted mean across migration tactics merely to obtain another response.

## Fail-closed rules

Do not:

- lower the 10-animal daily gate;
- lower the 30-day annual gate;
- move the autumn window;
- choose a different clock time after seeing outcomes;
- switch from cvratio to whichever metric works;
- substitute ground-count reports for the frozen demographic source to rescue sample size;
- use future observations in a rolling forecast;
- create a binary decline threshold after looking at the continuous result;
- fit the primary model if fewer than 11 annual observations survive.

A STOP is an informative result: the available public telemetry may simply be insufficient to test the Love–Otto future-demography claim with the required temporal discipline.

## Literature-bounded identification ceiling

A targeted literature audit completed after the original protocol lock identified an important boundary: classical metapopulation studies already show that habitat-patch area/connectivity and prior occupancy or population size can predict later colonization and extinction. The novelty target is therefore **not** “space predicts demography”.

The present Ya Ha Tinda primary asks a narrower incremental question: does within-population animal-location geometry add one-step-ahead recruitment information beyond the immediately preceding recruitment state and contemporaneous spatial scale?

The primary model does **not** condition on a source-independent landscape-connectivity index. No such index was frozen in the original protocol, and one will not be invented after outcomes. Therefore even a positive primary result must not be described as information beyond conventional habitat connectivity.

A future multi-population or explicitly patch-structured replication can test the stronger hierarchy:

[
F_{t+h} \sim D_t + R_t + L_t
]

versus

[
F_{t+h} \sim D_t + R_t + L_t + C_t,
]

where `L_t` is a prospectively defined conventional landscape-connectivity coordinate and `C_t` is the within-population Love–Otto cohesion/fragmentation state.

This paragraph is a **claim-ceiling clarification only**. It does not change the frozen Ya Ha Tinda predictor, outcome, sampling gates, forecast horizon or decision rule.

## Claim ceiling

If positive:

> within one long-term wild elk population, an autumn Love–Otto spatial-cohesion score improved out-of-sample prediction of subsequent recruitment beyond the preceding recruitment state and contemporaneous spatial scale.

If null:

> no incremental future-demography information was detected under the frozen metric, season, sampling and rolling-forecast design.

Neither result establishes a general cross-species early-warning law.

### Source-managed GPS quality gate

Because the Love–Otto IID metrics are sensitive to isolated coordinate errors, the primary movement state respects Movebank's source-managed QC rather than inventing an outcome-facing threshold. Records with `visible=false` are excluded when the field is present, and non-GPS sensor rows are excluded when `sensor-type` is present. No `gps:dop` threshold is added to the primary analysis. Any stricter DOP-based filter can only be a predeclared sensitivity and cannot replace the primary result.
