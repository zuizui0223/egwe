# Mac Hugh 2026 caribou: prospective-style temporal recruitment audit

Date: 2026-10-08

Status: **analysis route frozen before this project opens row-level recruitment values**; not an outcome-blind preregistration, because the published paper's null conclusion and the authors' AICc comparison were already known.

## Ecological question

Can the spring geographic spread of migration routes predict **the following autumn's calf recruitment**, over and above the preceding autumn recruitment and the number of monitored females?

This is not an interchangeable replacement for Love & Otto's individual-distance CV metrics. It is the nearest available wild, already published ecological connection between spatial organization and later reproductive outcomes.

The source archive is Borealis DOI `10.5683/SP3/0ROESU`, file `Dataset_migration_routes_and_recruitment.txt`. Its MD5, header and row count were inspected without fitting outcomes.

The source paper and author code are known to report no clear recruitment effect; the best fitted model was close to the null model by AICc. The following test instead asks about **year-forward held-out predictive utility**.

## Frozen eligibility

- One herd/year is the unit; routes/females within a year are not extra response replicates.
- Accept unique integer `Annee` entries within 1994–2019.
- `Recrutement_y` is the autumn response, `Variance_long_y` the spring spatial predictor.
- Define `Recrutement_(y-1)` only when calendar year `y-1` actually has a source value.
- No missing-year interpolation or opportunistic feature imputation.
- At least 11 complete lagged years are required, including seven initial training years and at least four genuinely later forecasts.

## Models and predictions

Primary baseline:

`M0: Recrutement_y ~ Recrutement_(y-1) + Nb_femelle_y`

Primary spatial model:

`M1: Recrutement_y ~ Recrutement_(y-1) + Nb_femelle_y + Variance_long_y`

Fit ordinary least squares with an intercept. For each held-out year, compute predictor means and sample SDs from earlier training years only, then predict that year. Use expanding-window rolling-origin training with seven initial eligible observations.

Record RMSE, MAE and the paired squared-error difference on identical held-out years. Claim incremental predictive information only when M1 improves **both RMSE and MAE**. Do not tune any coefficients or thresholds based on held-out outcomes.

After the primary result, one separate sensitivity may replace `Variance_long` with `Moyenne_long`. It cannot replace a failed primary.

## Scientific limits

This is one herd, source-published results are known, and no causal isolation of weather, habitat or behavioural mixing is possible here. A positive finding would support only bounded retrospective temporal predictiveness of a **route-geography coordinate**, not full demographic early-warning validity of Love–Otto IID CV.

If fewer than 11 complete lagged years remain, label `insufficient_temporal_replication` and stop. The previous Ya Ha Tinda outcome STOP remains unchanged.
