# Stage-B contract — concrete intFlex mapping before interaction-value access

**This contract is committed after Stage A passed and before any interaction matrix cell or next-year occupancy value is read by the project analysis.**

## Stage-A receipt

Locked source:

- `Magaiarsa/intFlex` commit `41d18084cb8dfbb92cde416cddbd020c567d01a2`;
- `data/networks/all_networks_years.Rdata` Git blob verified as `3d0ce00843579fc5edec80ebaadac7142b5b4a4b`.

Value-blind object inspection established:

- loaded object: `nets` only;
- class: `list`;
- length: `140`;
- every element: matrix;
- every matrix has row names and column names;
- source-defined network dimensions are all at least `5 × 5`;
- list element names follow the source `Site.Year` convention;
- 39 distinct site names are represented;
- list-name structure alone yields 77 numerically consecutive site-year pairs, of which 75 do not involve 2010;
- 30 distinct sites contribute at least one of those 75 retained transitions.

The source article states that the focal longitudinal sampling did not occur in 2010. Although the locked network object contains a small number of auxiliary `.2010` networks, the preregistration already forbids treating the unsampled 2010 as part of the focal one-year trajectory. Therefore `2009 -> 2010` and `2010 -> 2011` transitions are excluded structurally before any matrix value is read.

The published article reports 31 pollinator species satisfying its stronger repeated-year analysis criterion, so the preregistered minimum of 20 potentially scorable pollinator species is structurally plausible before outcome opening. The actual confirmatory candidate set remains defined by the frozen current-year rule below, not by selecting the published 31 after results.

## Source-code mapping

The pinned source `dataPrep/dataPrep.R` and `dataPrep/src/prepNets.R` fix the semantics:

1. `breakNet(spec, 'Site', 'Year')` aggregates specimen interactions by pollinator (`GenusSpecies`), plant (`PlantGenusSpecies`), site and year;
2. within each site-year plant–pollinator pair, interaction frequency is the mean across sampling rounds after the first aggregation;
3. `samp2site.spp(site = PlantGenusSpecies, spp = GenusSpecies, abund = abund)` constructs each matrix;
4. rows are plant taxa;
5. columns are pollinator taxa;
6. `dropNet()` removes networks with either dimension below the source threshold `num.dim = 5`;
7. the resulting list is saved as `nets` in `all_networks_years.Rdata`.

These source-defined filters are inherited. They are not re-tuned.

## Concrete name parser

Each network name is parsed at its **final period**:

- prefix before final `.` = `site`;
- final token = four-digit integer `year`.

The parser must reject a name that does not match `^.+\.[0-9]{4}$` rather than guessing.

No network involving year 2010 is used in a current-to-next-year transition.

Eligible transition `(site, t, t+1)` requires both exact network names to exist and `t+1 == t + 1`.

## Matrix mapping

For network matrix `M_s,t`:

- plants = `rownames(M_s,t)`;
- pollinators = `colnames(M_s,t)`;
- binary edge `E[p,i,s,t] = 1` iff the stored interaction frequency is strictly `> 0`, otherwise `0`;
- `Nplant_s,t = nrow(M_s,t)`;
- pollinator local degree = column sum of binary `E`;
- local support `r_i,s,t = degree_i,s,t / Nplant_s,t`;
- a pollinator absent from a site-year matrix is assigned `present=0` and `r=0` for that sampled site-year.

No threshold above zero is introduced.

## Sampling metadata

`data/samples.csv` is source-generated as a site × year table of sampling-round counts plus `nYears`.

The confirmatory baseline will include **current-year sampling rounds at focal site** as `sample_rounds_s,t` when a finite positive value exists for the parsed site/year. This is fixed now before occupancy outcomes.

- future-year sampling rounds are not supplied as a predictor;
- site/restoration class is omitted because it is not present in the locked confirmatory metadata table;
- missing current-year effort for an otherwise eligible network is a structural exclusion for that prediction row and is logged before scoring.

## Species-year marginal construction

At current year `t`, let `S_t` be all site-year networks present in the locked `nets` object for year `t`, excluding year 2010.

For every pollinator species observed in at least one `S_t` network:

- `occ_i,t = number of S_t sites containing i / number of S_t sites`;
- `mean_support_i,t = mean_s r_i,s,t` over every network in `S_t`, assigning zero when absent;
- `pooled_partner_i,t = |union of plant partners with E=1 for i across S_t| / |union of all plant taxa available across S_t|`;
- `Rmax_i,t = max_s r_i,s,t` over every network in `S_t`.

These use only current-year information.

## Prediction rows

For each retained consecutive transition `(site s, t, t+1)` and each pollinator species `i` observed in **at least one site anywhere in year t**:

- `present_i,s,t` = current focal-site presence;
- `r_i,s,t` = current focal-site support;
- `Nplant_s,t` = current focal-site plant richness;
- `sample_rounds_s,t` = current focal-site source effort;
- current species-year marginal predictors are joined by `(i,t)`;
- outcome `Y_i,s,t+1 = 1` iff `i` is a column name of `M_s,t+1`, otherwise `0`.

Species are not required to occur in the focal site at `t`; both colonization and persistence rows remain.

Species are not required to occur anywhere at `t+1`; next-year absence remains a valid zero.

## Fixed model matrices

### M0

Continuous/numeric predictors:

1. `present_i,s,t`;
2. `r_i,s,t`;
3. `Nplant_s,t`;
4. `sample_rounds_s,t`;
5. `occ_i,t`;
6. `mean_support_i,t`;
7. `pooled_partner_i,t`.

Categorical predictor:

8. `transition = paste0(t, '_to_', t+1)`.

### M1

All M0 predictors plus:

9. `Rmax_i,t`.

No interaction terms, splines, polynomial terms, traits, abundance, flexibility metrics, centrality, nestedness, site identity or future effort are added.

## Holdout and preprocessing

Validation is leave-one-pollinator-species-out.

For each held-out species:

- all rows of that species are test rows;
- all other species are training rows;
- require both response classes in training data;
- all continuous means/scales are estimated from training rows only;
- categorical transition levels are estimated from training rows only;
- if a held-out row contains a transition level absent from training, that held-out species fold is non-identifiable and omitted with a recorded reason;
- no species identity variable is supplied to the model.

## Fixed model implementation

Python/scikit-learn equivalent:

- `ColumnTransformer`: `StandardScaler()` for numeric columns, `OneHotEncoder(drop=None, handle_unknown='error')` for transition;
- `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=10000, class_weight=None, random_state=None)`;
- intercept on (default);
- identical preprocessing and estimator settings for M0 and M1.

No hyperparameter search is permitted.

## Score and bootstrap

For held-out species `i`, calculate mean Bernoulli negative log likelihood across all its eligible rows, clipping predicted probabilities only for score arithmetic to `[1e-12, 1-1e-12]`.

`delta_refuge_i = NLL_i(M1) - NLL_i(M0)`.

Primary total = arithmetic mean of `delta_refuge_i` over identifiable held-out species.

Bootstrap:

- resampling unit = held-out species delta;
- draws = `10,000`;
- RNG = NumPy `default_rng(20260912)`;
- report percentile 2.5% and 97.5% bounds of the bootstrapped equal-species mean.

Primary positive decision:

`strongest_local_refuge_adds_future_occupancy_information`

iff:

- observed equal-species mean delta `< 0`; and
- bootstrap 97.5th percentile `< 0`.

Otherwise:

`no_detected_incremental_strongest_refuge_information`.

## Secondary locked outputs

Without altering the confirmatory decision, report:

- number of networks, sites, retained transitions, prediction rows and held-out species;
- class prevalence;
- per-species M0/M1 NLL and delta;
- M0/M1 equal-species mean NLL;
- persistence-only and colonization-only per-species deltas where each stratum is present;
- transition-specific deltas;
- M0/M1 calibration bins;
- predictor correlation matrix for `occ`, `mean_support`, `pooled_partner`, `Rmax`;
- sensitivity with site-year pollinator degree rank percentile replacing `degree/Nplant`, preserving the same model/holdout/decision as a clearly secondary analysis.

## No-rescue rule restated

Once the next workflow reads matrix cells, this contract is closed. A weak/null/adverse primary result cannot be repaired by selecting plants, common pollinators, the published 31 species, specific sites/years, a different refuge quantile, weighted interaction strength, AUC, a different regularization constant or row-level CV.
