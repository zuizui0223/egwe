# Preregistration — natural temporal-network test of cross-layer organization beyond marginals

**Frozen before project-level inspection of any raw network value from the locked archive.**

## Purpose

The active NEE manuscript makes a constructive state-representation result: two present states can share declared ecological/genetic marginals while differing in their exact next interaction state. The numerical finite-model transition difference and the positive operator mechanisms remain closure-specific.

This preregistration opens one external natural-system test of the portable part of that argument:

> **Does observed plant–pollinator pairing at time `t` carry transferable information about interaction occurrence at `t+1` beyond the plant and pollinator marginal interaction state, network size/context and island fragmentation context measured at `t`?**

A positive result would test cross-layer organization directly in nature. It would not validate the finite q-dependent allele-selection, recruitment, recoupling, density-feedback or last-refuge operators.

## Prospective status

This is a prospectively locked reanalysis of an already published archive, not prospective field data collection. The source paper and its published conclusions are public. However, before this preregistration the project has not computed the locked next-year held-out predictive comparison below from the raw archive.

Published source conclusions may not be used to choose taxa, islands, transformations, time transitions, outcome definitions, penalties or performance metrics.

## Locked source

Primary study:

- Ren, Peng; Si, Xingfeng; Ding, Ping (2022), **Stable species and interactions in plant–pollinator networks deviate from core position in fragmented habitats**, *Ecography*, doi:`10.1111/ecog.06102`.
- Dryad dataset doi:`10.5061/dryad.rv15dv484`.
- machine-access mirror: Zenodo record `6519751`, CC0.

The public metadata states that the study contains observations of 42 plant–pollinator networks in a fragmented island landscape over 3 years and that the deposited archive contains three packages.

The source files are locked before content inspection as follows:

1. `2_null_model_background_data.rar` — **primary raw-network/source-code package**; public MD5 `40d028ed6a72d35e37d06b1b5240a72d`.
2. `3_span_1CV.rar` — **temporal-index/stability source-code package only if required to decode year/site indexing already present in package 1**; public MD5 `6239f2eeebd4b7e7387cd6bde515c6ed`.

`1_linner_regression.rar` is not a fallback raw-data source for the confirmatory analysis. It may be cited for source context but is not opened to rescue a missing raw temporal network representation.

## Stage A — archive/schema gate without data values

Before any raw network value is inspected, Stage A may inspect only:

- Zenodo/Dryad metadata;
- fixed file sizes and digests;
- archive member paths;
- names of R scripts or other code files;
- source-code text needed to identify file roles, site/year keys and matrix orientation;
- the first/header line of tabular files only when the source format clearly has a header.

Stage A must not inspect matrix cells, interaction counts, species-specific persistence, next-year outcomes, fitted coefficients, correlations, effect directions, model scores or published per-island numerical results beyond source metadata/methods.

### Stage-A eligibility

The archive advances only if the fixed source/package roles identify all of the following without inventing a key:

1. an independent island/site identifier;
2. at least three ordered sampling years or time points;
3. plant identity;
4. pollinator identity;
5. a year-specific bipartite edge representation as binary interaction occurrence or nonnegative interaction count;
6. a source-defined mapping that permits the same site to be followed across at least two `t -> t+1` transitions;
7. at least 20 independent sites after structural validity checks, unless source metadata demonstrate that the mainland reference must be excluded from island holdout, in which case the remaining island count must still be at least 20.

If a usable year-specific edge representation is absent, the decision is:

`prospective_next_interaction_not_identifiable_from_archive`

and the attempt stops. Do not substitute the published interaction-stability aggregate or a spatial-only outcome.

If site/year/species identities cannot be decoded from source code/member naming without inspecting outcome-dependent summaries, the decision is:

`temporal_network_key_not_identifiable_from_archive`

and the attempt stops.

## Stage B — exact analysis contract before raw edge values

If Stage A passes, a second contract must be committed before any interaction matrix cell or edge value is read. The following scientific structure is already fixed and cannot be changed in Stage B.

### Prediction universe

For each eligible site `s` and non-final year `t`, define the candidate pair universe **using only year `t`**:

`U_s,t = P_s,t × A_s,t`,

where `P_s,t` is the set of plant taxa observed in the year-`t` network and `A_s,t` is the set of pollinator taxa observed in the year-`t` network.

For each pair `(i,j)` in `U_s,t`, the future outcome is:

`Y_i,j,s,t+1 = 1`

if the same plant–pollinator pair is observed interacting at the same site in year `t+1`, and `0` otherwise.

A pair remains an eligible zero if one or both year-`t` taxa are not detected at `t+1`. Conditioning the candidate universe on year-`t+1` taxon presence is forbidden because it uses future information to define eligibility.

If source sampling is not comparable across ordered years and the source code does not supply a fixed effort representation, the attempt must stop rather than introduce a post-hoc effort correction.

### Current marginal representation

For each candidate pair, the baseline may know the complete **layer-wise marginal interaction state at time `t`**, but not the identity of whether that particular pair is currently linked.

If the archive contains source-defined interaction counts, the primary marginals are:

- `log1p(plant_strength_i,s,t)` — row sum at time `t`;
- `log1p(pollinator_strength_j,s,t)` — column sum at time `t`.

If the source archive is strictly binary, replace these with plant and pollinator binary degrees. This choice is determined from Stage-A schema/source code only and cannot depend on predictive performance.

The baseline also contains the following if source-identifiable without outcome-dependent construction:

- number of plant taxa at time `t`;
- number of pollinator taxa at time `t`;
- network connectance at time `t`;
- source-defined log island area;
- source-defined log island isolation;
- a categorical transition indicator (`year1 -> year2` versus `year2 -> year3`).

No other network statistic may be added after observing outcomes.

### Cross-layer organization variable

The primary additional organization variable is simply the realised current pair assignment:

`A_i,j,s,t = 1`

if plant `i` and pollinator `j` are linked at time `t`, and `0` otherwise.

This is intentionally minimal. Given fixed row and column marginals, `A_t` records **which plant is paired with which pollinator**. It is the natural-network analogue of retaining cross-layer organization after marginal summaries are fixed.

If interaction counts are available, weighted pair count is secondary only and cannot replace the binary current-edge primary variable.

## Primary predictive comparison

The confirmatory comparison is:

- `M0`: future pair occurrence from current marginal state + fixed site/network context;
- `M1`: the identical model plus current pair assignment `A_t`.

### Validation unit

Validation is **leave-one-site-out**.

All years, taxa and candidate pairs from one island/site are held out together. Random pair-level or edge-level train/test splitting is forbidden.

If mainland observations are structurally different from islands, the mainland may be retained as training/context only or omitted according to a rule fixed in Stage B from source design before raw edge values. It cannot be treated as another independent island merely to increase the denominator.

### Model family

Primary model: fixed-penalty logistic regression.

- Bernoulli response: `Y_i,j,s,t+1`.
- intercept included;
- continuous predictors standardized using the training sites only;
- L2 penalty with `C=1.0`;
- deterministic solver equivalent to scikit-learn `LogisticRegression(penalty="l2", C=1.0, solver="lbfgs", max_iter=10000)`;
- no class weights;
- no hyperparameter search;
- the exact same preprocessing and penalty apply to `M0` and `M1`.

If the locked design matrix is non-identifiable for a held-out fold because a categorical level is absent from training, the fold is recorded non-identifiable; no alternate encoding or model family is substituted after response inspection.

### Primary score

Within each held-out site, calculate mean Bernoulli negative log likelihood over all preregistered candidate pairs and both eligible transitions. Each site therefore receives equal weight regardless of network size.

Probabilities are clipped only for numerical evaluation at `1e-12` and `1-1e-12`.

Define per site:

`delta_pair = mean_NLL(M1) - mean_NLL(M0)`.

Negative values favor cross-layer organization.

The primary total is the equal-site mean of `delta_pair` over all identifiable held-out sites.

A deterministic site bootstrap uses seed `20260912` and `10,000` draws, resampling independent site deltas with replacement.

The confirmatory decision **`current_pair_organization_adds_future_information`** requires both:

1. equal-site mean `delta_pair < 0`; and
2. bootstrap 95% upper bound for the equal-site mean `< 0`.

Otherwise the decision is **`no_detected_incremental_pair_organization_information`**.

AUC, accuracy, precision/recall or a favorable taxon subset cannot replace the proper-scoring-rule decision.

## Secondary exact-marginal diagnostic

A degree-preserving binary rewiring diagnostic will test the structural interpretation without becoming a second confirmatory endpoint.

Within every eligible site-year network, generate degree-preserving bipartite double-edge-swap rewires of `A_t` using a deterministic seed fixed in Stage B. These rewires retain the binary plant and pollinator degrees exactly while destroying most pair identity.

The primary model is **not** refit to choose a favorable rewire. The diagnostic compares the future-prediction contribution of the observed `A_t` with the distribution obtained after replacing it by preregistered degree-preserving rewires.

If the source network is weighted, this remains a binary-degree diagnostic; no weighted null algorithm is introduced after results.

This diagnostic cannot rescue a failed primary `M0` versus `M1` comparison.

## Secondary descriptive outputs

Report regardless of primary direction:

- per-site `delta_pair`;
- transition-specific deltas (`year1 -> year2`, `year2 -> year3`) descriptively;
- observed prevalence of next-year interaction among current edges and current non-edges;
- predicted calibration curves for `M0` and `M1`;
- the degree-preserving rewiring diagnostic;
- sensitivity using current pair interaction count if that field is source-defined, clearly secondary to binary `A_t`.

No plant, pollinator, island-size or persistence subset may be promoted to confirmatory status after seeing results.

## Hard stop and no-rescue rules

After raw edge values are opened, do not:

- switch to another Ren archive package because it gives a stronger result;
- replace next-year pair occurrence with the authors' published stability index;
- define pair eligibility using year-`t+1` species presence;
- choose only persistent/common/core species;
- exclude small or isolated islands because they weaken transfer;
- tune logistic penalty strength;
- choose weighted versus binary current-pair organization by performance;
- replace site holdout with pair-level CV;
- change score from log loss to AUC because one is more favorable;
- tune a threshold for interaction presence after inspecting outcomes;
- import the finite-model `q*=0.625`, route-margin weights, generation horizon or AUC benchmark;
- claim that a null result falsifies the finite model family.

Structural exclusions are allowed only for missing/invalid source keys, impossible negative counts, exact duplicate records under source identity, or source-documented non-comparable sampling. Every exclusion must be logged before model scoring.

## Claim ceiling

### If positive

A positive result supports only this natural-system statement:

> In this three-year fragmented island plant–pollinator system, knowing the realised plant–pollinator pairing at time `t` improves whole-site held-out prediction of pair occurrence at `t+1` beyond the declared current marginal interaction state and site/network context.

This would directly support the portable state-representation claim behind NEE Question 2: **layer-wise marginals can fail to exhaust fate-relevant information because cross-layer organization matters.**

It would not establish that the model-specific next-state difference `0.2543`, 49-fold support-variance contrast, q-dependent allele sorting, recruitment buffering, direct recoupling, density-feedback gate or last-refuge AUC generalize to nature.

### If null/adverse

A null or adverse result means this preregistered representation did not earn incremental held-out future information in this archive. It remains a bounded external test and prevents the NEE Discussion from implying natural support not obtained.

## Relationship to EGWEE

EGWEE remains the broad multilayer fragmentation synthesis testing whether demographic/resource, interaction, movement, reproductive and genetic layers diverge across natural systems. This preregistered Ren analysis is a separate **single-system temporal Q2 validation attempt** focused on marginal-state sufficiency versus cross-layer pair organization. Its result is not selected or weighted to rescue the EGWEE meta-analysis.
