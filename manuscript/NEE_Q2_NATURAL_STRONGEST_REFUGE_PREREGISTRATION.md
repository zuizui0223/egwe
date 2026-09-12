# Preregistration — natural strongest-interaction-refuge test of future patch occupancy

**Frozen before project-level inspection of raw `intFlex` network/data values.**

## Purpose

The active NEE manuscript contains a closure-specific result in which the strongest remaining local refuge carries prospective fate information beyond a co-timed marginal interaction summary. The absolute finite-model route margin, AUC, threshold and operator sequence are not claimed to be natural constants.

This preregistration opens one external natural-system test of the portable prediction:

> **After current landscape occupancy, average interaction support and the focal patch's current state are represented, does a pollinator species' strongest local interaction-support patch at year `t` add held-out information about its observed patch occupancy at year `t+1`?**

This tests the ecological idea that the depth of the best remaining local refuge may matter beyond average/marginal state. It does not test the finite genetic operators.

## Prospective status

This is a prospectively locked reanalysis of an existing ten-year field archive, not prospective field collection. The source article is already published and reports associations between interaction flexibility and colonization/persistence/occupancy. Those published conclusions motivate source suitability but may not be used to tune this new strongest-refuge metric, model, taxon subset, validation unit or performance criterion.

The project has not inspected the raw values of the locked GitHub data objects before this document is committed.

## Locked source

Primary study:

- Gaiarsa, M. P., Kremen, C. & Ponisio, L. C. (2021), **Pollinator interaction flexibility across scales affects patch colonization and occupancy**, *Nature Ecology & Evolution* 5:787–793, doi:`10.1038/s41559-021-01434-y`.
- public repository: `Magaiarsa/intFlex`;
- repository snapshot locked at commit `41d18084cb8dfbb92cde416cddbd020c567d01a2`.

The source article describes 63 sites, approximately 16,600 bee specimens, 157 bee species, 152 plant species and 251 site-year networks over 2006–2015, with no sampling in 2010. The repository publishes the network and sampling objects needed to reconstruct site-year interaction state.

Locked files before content inspection:

1. `data/networks/all_networks_years.Rdata` — primary site-year plant–pollinator network object; Git blob `3d0ce00843579fc5edec80ebaadac7142b5b4a4b`.
2. `data/samples.csv` — primary source-defined sampling/site-year metadata; Git blob `e9b060758ce3675921b83f1f64a31972c65e3504`.
3. `dataPrep/dataPrep.R` — source-code mapping only; Git blob `09ab4195f0f6213fd18e6e37908266947e827414`.

`allSpecimens.Rdata`, precomputed flexibility objects and precomputed result tables are not confirmatory fallback sources. They may not be substituted because they produce a stronger result.

## Stage A — schema/object gate before raw values

Before raw network values are inspected, Stage A may inspect only:

- repository metadata and locked blob identities;
- `samples.csv` header only;
- R object names/classes/dimensions/element names from `all_networks_years.Rdata`, without printing matrix/data-frame cell values;
- `dataPrep.R` source-code text needed to identify object semantics, site/year naming, network orientation and source-defined sample keys.

Stage A must not inspect interaction matrix cells, species-specific occupancy, colonization/persistence outcomes, strongest-refuge values, associations, effect directions, fitted models or predictive scores.

### Stage-A eligibility

The analysis advances only if the locked objects/source code identify all of the following without inventing a join:

1. site identifier;
2. ordered sampling year;
3. plant identity;
4. pollinator identity;
5. site-year bipartite interaction matrix, with rows/columns orientable from source code;
6. repeated sites permitting at least two observed consecutive-year transitions somewhere in the archive;
7. at least 20 pollinator species with at least one eligible current-year observation and a scorable next-year transition after structural exclusions.

If site-year networks cannot be mapped prospectively, the decision is `site_year_network_not_identifiable_from_locked_source` and the attempt stops.

If the network is only a precomputed flexibility summary rather than raw site-year pair state, the attempt stops. Do not substitute a published flexibility score for the preregistered local-refuge statistic.

## Stage B — exact mapping contract before opening interaction cells

If Stage A passes, a second committed contract must record the concrete object names, site/year parser, matrix orientation and source metadata fields before any interaction matrix cell is read.

The scientific construction below is already frozen.

## Prediction universe

For each pair of **consecutive calendar years** `t` and `t+1` with source-sampled networks, include only sites sampled in both years. Transitions crossing the unsampled year 2010 are not treated as one-year transitions.

For every pollinator species `i` observed in at least one eligible site-year network at current year `t`, and every site `s` sampled in both `t` and `t+1`, define:

`Y_i,s,t+1 = 1`

if species `i` is observed in the site-year plant–pollinator network at `t+1`, otherwise `0`.

A species does not have to be present at focal site `s` at `t` to enter the candidate set; this preserves both persistence and colonization outcomes. Species eligibility is defined using year `t` only, never by requiring detection at `t+1`.

The endpoint is explicitly **observed network occupancy**, not detection-corrected true occupancy, unless the locked source code already defines a detection model independently of this project. No post-hoc occupancy correction may be added.

## Local interaction-support coordinate

Convert each site-year interaction matrix to binary edge presence using source-defined positive interaction frequency/count as `1` and zero as `0`.

For pollinator species `i` in site `s` at year `t`, define local interaction support:

`r_i,s,t = degree_i,s,t / Nplant_s,t`,

where `degree_i,s,t` is the number of distinct plant partners and `Nplant_s,t` is the number of plant taxa represented in that site-year network.

If pollinator `i` is absent from the site-year network, `r_i,s,t = 0`.

This bounded coordinate is used to reduce direct dependence on raw visit counts and sampling-round frequency. It is a representation of realised partner support, not pollinator abundance.

## Current marginal state

For each pollinator species-year using all sites sampled at `t`, compute:

- `occ_i,t`: fraction of sampled sites where species `i` is present;
- `mean_support_i,t`: arithmetic mean of `r_i,s,t` across **all** sampled sites at `t`, including zeros for absence;
- `pooled_partner_i,t`: number of distinct plant partners used by species `i` across all sampled sites at `t`, divided by the number of distinct plant taxa available across those site-year networks.

These are the declared current marginal/landscape summaries.

## Strongest local refuge

The sole confirmatory added predictor is:

`Rmax_i,t = max_s r_i,s,t`

across all sites sampled at year `t`.

`Rmax` is not tuned, thresholded or weighted against the future outcome. It measures the strongest contemporaneous patch-level interaction-support state available to a pollinator species in the sampled landscape.

The baseline is deliberately given `mean_support`, `occ` and pooled partner breadth so the strongest-refuge test cannot win merely by seeing general interaction richness that the marginal model was denied.

## Focal-patch current state and context

For each prediction row `(i,s,t -> t+1)`, the baseline also receives:

- `present_i,s,t`: whether pollinator species `i` is currently observed at focal site `s`;
- `r_i,s,t`: focal-site current support;
- `Nplant_s,t`: current site-year plant richness;
- source-defined site class/restoration status if it is present in the locked metadata and fixed in Stage B before outcomes;
- current-year sampling-effort field only if it is source-defined in the locked metadata and its use can be fixed without inspecting future occupancy;
- categorical transition year.

Future-year sampling effort is not supplied as a biological predictor. Variation in future detectability remains part of the observational claim ceiling.

No other network centrality, nestedness, flexibility or trait variable may be added to the confirmatory baseline after outcomes are read.

## Primary predictive comparison

- `M0`: next-year observed patch occupancy from current marginal state + focal-patch current state + fixed source context;
- `M1`: the identical model plus `Rmax_i,t`.

### Independent holdout

Validation is **leave-one-pollinator-species-out**.

For each held-out species, all of its sites, years and transitions are absent from model fitting. The relation between current state and future occupancy must therefore transfer to a pollinator species not used to fit the coefficients.

Random row-level train/test splitting is forbidden.

### Model family

Primary model: fixed-penalty logistic regression.

- Bernoulli response `Y_i,s,t+1`;
- intercept included;
- continuous predictors standardized from training species only;
- categorical variables encoded from source-defined levels before outcome inspection;
- L2 penalty with `C=1.0`;
- deterministic solver equivalent to scikit-learn `LogisticRegression(penalty="l2", C=1.0, solver="lbfgs", max_iter=10000)`;
- no class weights;
- no hyperparameter tuning;
- identical preprocessing and penalty in `M0` and `M1`.

If a held-out fold cannot be scored because its required source-defined categorical level is absent from training, that fold is marked non-identifiable; the model family is not switched.

## Primary score and decision

For each held-out pollinator species, calculate mean Bernoulli negative log likelihood across all of its eligible site-transition rows. Probabilities are clipped for numerical scoring only at `1e-12` and `1-1e-12`.

Define species-level:

`delta_refuge = mean_NLL(M1) - mean_NLL(M0)`.

Negative values favor strongest local refuge.

The primary total is the equal-species mean of `delta_refuge` across all identifiable held-out species. Thus common species do not dominate solely by contributing more site-year rows.

A deterministic species bootstrap resamples held-out species deltas with replacement using seed `20260912` and `10,000` draws.

The confirmatory decision **`strongest_local_refuge_adds_future_occupancy_information`** requires both:

1. equal-species mean `delta_refuge < 0`; and
2. bootstrap 95% upper bound for the equal-species mean `< 0`.

Otherwise the decision is **`no_detected_incremental_strongest_refuge_information`**.

AUC, accuracy, a regression p-value, one favorable transition, or the source paper's original flexibility coefficients cannot replace this decision.

## Prespecified secondary diagnostics

Reported regardless of primary direction and unable to rescue it:

1. species-level `delta_refuge` distribution;
2. persistence rows (`present_i,s,t=1`) and colonization rows (`present_i,s,t=0`) scored separately, descriptive only;
3. transition-year deltas, descriptive only;
4. calibration of M0 and M1;
5. sensitivity replacing `degree/Nplant` with binary degree rank percentile within each site-year, using the same fixed M0/M1 logic; secondary only;
6. correlation among `Rmax`, `mean_support`, `occ` and pooled partner breadth, reported to show how much nonredundant representation exists but not used to redefine predictors.

## Hard stop and no-rescue rules

After interaction cells are opened, do not:

- switch from pollinators to plants because results are stronger;
- restrict to the 31 species from the source paper's flexibility analysis unless that exact restriction is required structurally before outcome inspection;
- choose only hedgerows, controls, common species or long-duration sites because they improve the score;
- condition species eligibility on presence at `t+1`;
- bridge the unsampled 2010 as a one-year transition;
- replace `Rmax` with a favorable quantile, top-k mean or fitted weight;
- replace relative binary degree with visit strength as the confirmatory support coordinate;
- tune regularization;
- replace leave-one-species-out with row-level CV;
- replace log loss with AUC because it is more favorable;
- add source flexibility, centrality, nestedness, abundance or traits to M1 only;
- import the finite-model route-margin weights, `q*=0.625`, time horizon or AUC benchmark;
- call a null/adverse result a falsification of the finite closure.

Structural exclusions are allowed only for invalid site/year keys, impossible matrix dimensions, exact duplicate source objects, nonpositive plant richness, or source-documented non-comparable samples. Every exclusion must be recorded before scoring.

## Claim ceiling

### If positive

A positive result supports the natural-system statement:

> In this decade-long plant–pollinator field system, a pollinator species' strongest contemporaneous patch-level interaction support carries reproducible held-out information about its next-year observed patch occupancy beyond current occupancy, average landscape support, pooled partner breadth and focal-patch state.

That would be a direct natural counterpart to the NEE strongest-refuge idea: **future fate can depend on the depth of the best remaining local state, not only on the average state.**

It would not validate the finite route-margin formula, its AUC, q-dependent allele sorting, recruitment buffering, direct eco-genetic recoupling, density thresholds or genetic warning.

### If null/adverse

A null or adverse result means the preregistered strongest-refuge representation did not earn incremental held-out future information in this archive. It prevents the NEE manuscript from presenting the strongest-refuge mechanism as naturally supported by this system.

## Relationship to EGWEE

EGWEE remains the broad fragmentation multilayer synthesis. This is a separate single-system temporal validation attempt for one NEE Q2 prediction. It is not pooled or selected to rescue the EGWEE meta-analysis.
