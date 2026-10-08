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
