# Ulex public-genomics / visit / fruit source — prospective schema screen (2026-10-08)

**Status: live Zenodo README/header gate implemented; no biological outcome rows opened, no ecological coefficient estimated, and no H-R natural validation claimed.**

## Why this source is the next practical gate

Castellanos et al. (2023), [*Quantitative genetic analysis of floral traits shows current limits but potential evolution in the wild*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10130720/), used *Ulex parviflorus* and estimated genomic relatedness and contemporary floral-trait selection in a wild plant population. The paper provides a valuable negative-claim boundary: not every heritable floral trait is currently selected; stabilizing selection, environmental variation and heritability can all limit observed evolutionary response.

The associated [public Zenodo record 7761289](https://zenodo.org/records/7761289) is a mirror/index for original Dryad DOI [10.5061/dryad.9zw3r22jp](https://doi.org/10.5061/dryad.9zw3r22jp). Its published file list includes:

- `SNP.genotypes.csv`: individual genomic markers;
- `relatedness.matrix.csv`: genomic relatedness;
- `floral.traits.csv`: focal floral phenotypes;
- `fruits.and.mean.floral.traits.csv`: reproduction and individual-mean flower traits;
- `pollinator.census.csv`: visit observations;
- `README.md`: source-defined field labels and observational units;
- `Scripts.txt`: source analysis provenance.

Unlike the recent Dryad 401/403 cases, this is an archived **Zenodo file-list surface**, so its actual public file/README/header accessibility can be tested independently. File-list visibility is NOT yet successful raw archive acquisition.

## High-value ecological constraint already apparent from the paper

The publication reports **569** 3-minute pollinator censuses at six Ulex sites, **364** visits to **22,522** censused flowers over approximately **28 hours**. Of the visitors, 331 were *Apis mellifera*; 25 were *Bombus*. These are observation/census counts. The fact that the study also genotyped plants and recorded fruit production does not establish that each visit/census is assigned to the same *individual genotyped plant*.

The primary H-R hypothesis requires measured **patchwise covariance of effective interaction and trait/genetic support**, plus independent future function. It is not permissible to attach each site's pollinator visitation average to all plants and then claim newly observed patchwise relational state.

The publication also analyses contemporary selection and genomic heritability. A regression reproducing a floral-trait/fruit association would be **prior-art replication**, not proof of a new causal operator.

## Frozen outcome-blind schema requirements

First inspect only public source metadata, README text and each CSV's *first physical header line*. The separate current `scripts/probe_ulex_zenodo_schema.py` limits reads accordingly; it exports no biological observations.

Classify exact unit/ID compatibility without opening values:

1. `pollinator.census.csv`: identify whether headers support surveyed **site**, **3-min observation/flower**, or **identified focal plant**. A site- or flower-count census cannot become same-plant pollination exposure without explicit source keys.
2. `fruits.and.mean.floral.traits.csv`: determine whether plant ID, site, sampling date and fruit endpoint are distinguishable from the phenotype records.
3. `SNP.genotypes.csv` and `relatedness.matrix.csv`: identify individual label scheme; marker columns and similarity matrix indices are not independent samples.
4. `floral.traits.csv`: identify flower versus plant replication, and plant-to-fruit shared-key *possibility*. Header matching alone is not actual row-level join coverage.
5. Source dates: contemporary reproductive success is not automatically a future-year warning endpoint. Do not invent `t -> t+1` forecasting without documented temporal order and independent later outcome.

After the source-grain probe, admissibility requires a separate, prospective decision before any actual biological row opens. **Do not tune proxies, choose favourable plants or infer significance from published p-values.**

### Possible outcomes

- `METADATA_OR_ACCESS_STOP`: published record exists but schema could not be inspected. Not an ecological null.
- `PARTIAL_G_T_F_DATA_ONLY`: genomic relatedness + flower/fruit keys plausibly align but visitation is site/census-grain, not individual: may support a limited trait/genetic baseline, **not** H-R relational state.
- `SCHEMA_POTENTIAL_FULL_G_I_F`: all relevant components expose compatible plant/patch IDs and biologically ordered endpoints: still **not admitted** until raw identifier coverage, effort, longitudinal alignment and holdout groups are checked prospectively.

The model's finite synthetic source, NEE paper, and previous natural transfer null are not modified. No claim of geographic urban/island convergence can be inferred from this dataset.

## Sources

- [Zenodo source file inventory](https://zenodo.org/records/7761289)
- [Castellanos et al. (2023) article and published site-level visitor counts](https://pmc.ncbi.nlm.nih.gov/articles/PMC10130720/)
- [Original Dryad source DOI](https://doi.org/10.5061/dryad.9zw3r22jp)

Machine source contract: `artifacts/empirical/ulex_zenodo_source_gate_20261008.json`. Executable first-header-only audit: `scripts/probe_ulex_zenodo_schema.py`. No outcome model has been specified, calibrated or executed in this branch.

## Executed 2026-10-08 Zenodo schema result — prospective H-R STOP

GitHub Actions run **37791651946**, job **113360323100**, source-only artifact **11556532768**, verified the public Zenodo record and successfully read the original README plus the first physical headers of four CSVs. No biological data rows were inspected. The initial `SNP.genotypes.csv` header exceeded the bounded 65,536-byte width, which is a **schema-reader limit** rather than an access denial; a revised one-header-only reader uses a 1-MB cap, but its result is independent of the decisive interaction ID absence.

Exact header evidence:

| Source file | Published raw header fields | Unit inference and limits |
| --- | --- | --- |
| `pollinator.census.csv` | `year, locality, flowers, tot.visits, Apis, Bombus, other, visits.flower, observations` | **No focal `ind` or `plant` key**; separate 3-minute pollinator censuses of an observation patch per README |
| `fruits.and.mean.floral.traits.csv` | `site, ind, elev, weight, area, scars, fruits, nofruit` | Plant-level phenotype/reproductive counts, with `ind` |
| `floral.traits.csv` | `site, ind, flower, weight, area, elev` | Replicate flowers nested within plants, with `ind` |
| `relatedness.matrix.csv` | `ind` plus 225 plant-ID columns (226 columns total) | Individual genomic relatedness, **not** 225 independent field populations |
| `SNP.genotypes.csv` | First line too wide for initial 65 KB header cap | README describes 10,421 SNP loci for 225 individual plants; actual matrix orientation remains to be checked |

The README itself says `pollinator.census.csv` rows are individual **3-minute censuses on Ulex plants**, with `flowers` and `tot.visits` counted in the **observation patch**, not individually tagged genetic plants. This matters even though the census describes observations 'on plants': its recorded header has no `ind` or plant ID.

### Scientific decision

**`NOT_IDENTIFIABLE_NO_POLLINATOR_PLANT_ID` for full H-R.** The source does not directly identify the interaction × genotype/trait alignment required by the flagship's natural transfer hypothesis. Substituting the `locality` mean visitation for the same source's plant-level genomic observations would be ecological pseudo-precision; it does not estimate local cross-layer covariance.

A **partial G–T–F** (genetic relatedness, floral phenotype and contemporaneous fruit set) key structure is plausible because the plant-level trait and fruit tables expose `ind` and the relatedness matrix exposes plant-labelled columns. **Actual value-level overlap, joins, missingness and genome/fruit outcome relationships were NOT tested.** The original publication already used these data to estimate heritability and contemporary selection, so that partial pathway does not constitute a new natural validation of the full H-R hypothesis.

**An improved SNP header does not rescue the missing pollinator `ind` field.** The SNP header-width correction is retained to make the archive audit reproducible, not as a mechanism to reopen or tune a negative eligibility gate. The following stages remain closed: future function prediction, experimental operator causality, urban/island regime convergence, NEE AUC natural transfer.

The machine-readable source decision is recorded in `artifacts/empirical/ulex_zenodo_source_gate_20261008.json`. Source-side access and structure were **successfully tested**; this is a measurement-grain exclusion, not an HTTP failure and not a biological null.
