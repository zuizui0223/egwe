# Natural relational-state: new public-source scout (2026-10-08)

**Research status:** 5 additional public source programmes screened at **published archive-description/README level**. Their raw ZIP/CSV/XLSX bytes, headers, unique keys, dates, join coverage, missingness, and endpoint values have **not** yet been inspected in this audit. The prospective H-R programme remains untested in nature.

**Primary question:** does locally matched interaction–trait/genetic organization improve *held-out later ecological function* over marginal state? Merely finding field visitation, markers, and offspring in the same study is not sufficient. In particular, individual/genetic data joined to one *site-wide visitation average* do not identify patchwise I–T/G covariance.

The machine registry is `artifacts/empirical/relational_source_scout_20261008.json`; `python scripts/validate_relational_source_scout.py` independently enforces fail-closed admission.

## Priority 1 — Leventhal et al. (2026), Brassica rapa: near-complete modules, wrong interaction grain for primary H-R

- Paper: *Evolution* 80, 1217–1229, DOI [10.1093/evolut/qpag047](https://doi.org/10.1093/evolut/qpag047).
- Public Dryad archive (published **2026-09-15**): [10.5061/dryad.tdz08kqdr](https://doi.org/10.5061/dryad.tdz08kqdr), `Leventhal_et_al_2026.zip` and a detailed README.
- Published methods/data index: four experimental populations B30/Comp and Track/FarWest, two spatial configurations, two seasonal runs *within one 2011 season*; 854 mapped flowering pollen donors, 180 sequential male-sterile recipient traps, 1,970 genotyped offspring and 10 microsatellite loci.
- The archive index gives individual `id`, `X`, `Y`, `ft`, `dur`, `tot_flwrs`, `timevar`; processed genotype files; offspring-to-father pedigree assignments `P.1`, `P.2`, `P.3`, `prob`; and pollinator observations `Site`, `DOY`, `Date`, `Batch`, `Total pollinator visits` plus guild codes.
- **Primary H-R blocker:** published visitation is site × observation date/batch. It does not document *local within-site* interaction `I_j` matched to donor or local genetic/trait support. Attaching that site average to every plant would create apparent co-location without a measured interaction contrast.
- **Separate partial opportunity:** prospective *within-season male fitness* prediction using only donor flowering state measured by time t and paternity assigned to a later gene-trap batch. However, the current publication already analyzes seasonal variation in male selection and spacing effects; any new analysis needs a distinct preregistered predictive estimand, honest independent units (four plots, two run windows, not 1,970 independent populations), and a raw ID/time audit. Do **not** infer future predictivity from existing selection coefficients or leak full-season flower counts into early-time predictors.
- Decision: **primary H-R not identifiable at declared interaction grain; raw-schema check highest priority for a distinct temporal subquestion**. No new fitness score estimated.

## Priority 2 — Cisternas-Fuentes & Koski (2024), Argentina anserina: a direct prior-art constraint

- Paper: *Proceedings B* 291:20231519, [10.1098/rspb.2023.1519](https://doi.org/10.1098/rspb.2023.1519).
- Archive: [10.5061/dryad.98sf7m0pk](https://doi.org/10.5061/dryad.98sf7m0pk). README lists `Pollinator_data_inputR2.xlsx`, `polpist_final2019-2021.xlsx`, `pop_level_dataset.xlsx`, and controlled-cross data.
- The paper directly studies 13 populations, effective population size (genetic), visitation (ecological), pollen quantity/quality limitation, fruit and seed output. Interaction between effective size and visitation in pollen quality is already published. The documented three-year span is **not** evidence of matched t→t+1 prediction.
- **Primary blocker:** effective size and visitation are analysed as population-level states, not patchwise alignment of effective interaction and genetic support; site means cannot resolve spatial covariance. Reproductive outputs are studied as downstream association, not a locked new future holdout.
- Decision: **not full H-R at published grain; cite as strong prior art**, not as our empirical validation or novelty.

## Priority 3 — Nakanishi et al. (2019), Camellia japonica: temporal pollen-pool compensation, not a forward-function dataset

- [Dryad 10.5061/dryad.17q550q](https://doi.org/10.5061/dryad.17q550q), one listed `Camellia_japonica_Data.xlsx`.
- 1,323 genotyped seeds, 19 mothers, two reproductive years, eight microsatellite loci; flowering density linked with pollen-pool diversity. The proposed bird-foraging expansion is an ecological interpretation; the displayed archive description does not establish synchronized visitation at each maternal patch.
- Decision: **not primary H-R**: local interaction exposure and genuinely later functional output are not documented.

## Priority 4 — Pearson et al. (2023), Echinacea angustifolia: experimentally measured operator but no proven longitudinal join

- *American Journal of Botany* 110:e16190, [10.1002/ajb2.16190](https://doi.org/10.1002/ajb2.16190).
- [Public analysis/data files](https://openworks.wooster.edu/facpub/418/) describe visit-specific pollen removal, bee-taxon restricted pollination, genotyped offspring/paternity, and experimental donor siring success.
- The study *already* shows that pollen removal and pollinator visitation are unreliable proxies for realised male fitness; this is prior art for operator–bottleneck mismatch. Documentation reviewed here does not establish independent ecological time-series with matched local I–T/G and later F.
- Decision: **hold for raw key/time screen only**, not presumed eligible.

## Priority 5 — Delnevo Conospermum undulatum paired archives: do not join by taxon alone

- [Reproductive output archive](https://doi.org/10.5061/dryad.4cg374r): fruits/seed set, germination in 12 remnant populations.
- [2026 genotype/parentage archive](https://doi.org/10.5061/dryad.95x69p907): adults and seedlings GenAlEx microsatellite data.
- Neither shared species name nor geographic fragmentation context supplies proof of identical plants, population-years, cohorts, accessions or forward outcome.
- Decision: **cross-archive lineage HOLD** until raw identities and temporal alignment are independently confirmed; no pseudo-longitudinal merged dataset.

## Count and interpretation

| source class | count | scientific meaning |
| --- | ---: | --- |
| Newly indexed source programmes | **5** | Archive metadata and file index reviewed |
| New raw ZIP/XLSX/CSV payloads opened | **0** | No direct source-schema validation in this screening pass |
| Full H-R prospective natural datasets confirmed | **0** | No new positive *or* negative biological finding |
| Highest-value next schema probe | **1** | `Brassica` for donor IDs, visitation grain, batch times, paternity mapping |

Existing three already audited systems remain separately documented in `RELATIONAL_TRANSFER_SOURCE_ELIGIBILITY_2026-10-08.md`. Combining the counts does not create eight independent ecological experiments; it is merely eight **candidate programmes** surveyed across two evidence levels.

## Next action, respecting the outcome firewall

Acquire the **exact Dryad 2026 Brassica archive** using documented public download endpoints; record source file hash; inspect only member paths, headers, types, join-key candidate names and observation timestamp coverage, without printing/fitting pollen-siring or reproductive outcome values. Confirm that plant/patch-specific interaction visits do not exist in another unindexed file before declaring the H-R spatial gate closed at raw-schema level. Freeze an *entirely separate* within-season male-fitness prediction protocol only if independent forward batches and source-key integrity pass. Do not adjust the frozen NEE flagship model, source pins, AUC, or claim ownership.

## External references and provenance

- [Dryad published Brassica index and README](https://datadryad.org/dataset/doi%3A10.5061/dryad.tdz08kqdr)
- [Evolution Brassica paper](https://doi.org/10.1093/evolut/qpag047)
- [Dryad Argentina index and README](https://datadryad.org/dataset/doi%3A10.5061/dryad.98sf7m0pk)
- [Proceedings B Argentina paper](https://doi.org/10.1098/rspb.2023.1519)
- [Camellia archive](https://datadryad.org/dataset/doi%3A10.5061/dryad.17q550q)
- [Echinacea analytical files](https://openworks.wooster.edu/facpub/418/)
- [Conospermum reproductive data](https://datadryad.org/dataset/doi%3A10.5061/dryad.4cg374r)
- [Conospermum genetic data](https://datadryad.org/dataset/doi%3A10.5061/dryad.95x69p907)
