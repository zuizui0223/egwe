# Traine (2026) source-grain audit: plant-level interaction, evolved-lineage context and later seeds

**Status (2026-10-08): source metadata, README and study design reviewed; outcome-blind live archive-header probe now implemented but its CI result is not yet known. This is not an H-R natural test or a new predictive result.**

## Why this source, rather than repeating Witheringia

The repo **already tested** Stone et al.'s *Witheringia solanacea* dataset (Dryad [10.5061/dryad.f8539](https://doi.org/10.5061/dryad.f8539)) in earlier workflows 32802948645 and 32803045668. The first returned API HTTP 401 and public file-stream HTTP 403; the fallback full bundle also returned 403. The existing authoritative record is `manuscript/empirical_witheringia_direct_interaction_access_result.md`, decision **`not_identifiable_from_archive`**. Do not call it newly discovered, redo uncredentialled routes or reinterpret non-access as a biology null.

We instead found a separate **unprobed** source with explicitly documented *individual-plant* flower state, pollinator behaviour and later fitness:

- Traine, Rusman & Schiestl (2026), *New Phytologist* 249:554–568, DOI [10.1111/nph.70705](https://doi.org/10.1111/nph.70705).
- Archived data [Dryad 10.5061/dryad.2ngf1vj15](https://doi.org/10.5061/dryad.2ngf1vj15), released 2025-10-31, latest revision 2026-03-09.
- Target: `data_local_adapt_traits.csv` (Dryad publicly indexes a 288.06 KB current version); also `reaction_norms.csv`, `haldanes.csv` and README.

## Published source contract, **not yet a checked raw join**

The README defines **`plant`** (individual identifier), **`matrix`** (plants assayed together), **`cohort`** (planting/test week), **`rep`** (selection replicate), **`temp_genotype`** (evolved temperature treatment), **`poll_genotype`** (evolved pollination treatment), and `temp_environment` (current growth temperature). Pre-bioassay plant traits include flower number, flowering time, petal size, nectar traits, petal UV/reflection and floral scent. The experiment exposed groups of 24 plants in a 5×5 array to bumblebees; the same documented CSV includes `chosen`, `bee_flower_visits`, `bee_plant_visits`, `bee_seconds_per_plant`, `seed_number`, `fruit_number`, `seeds_per_fruit` and `fruit_set`. Seeds were counted after fruits matured. The README explicitly warns that phenotyped and bioassayed plants were not always the same: complete-case sample size and overlap are **unknown** until the raw access/schema gate passes.

Crucially, `temp_genotype` and `poll_genotype` are **experimental-evolution history labels**, *not* each individual's microsatellite or genome genotype. Treating them as direct `G_j` allele frequencies would manufacture the original H-R mechanism. The study is greenhouse selection, not field fragmentation. Although arrays have a 5×5 arrangement, exact individual spatial coordinates and pre-outcome `I_j × G_j` alignment are not documented in this file, and cannot be inferred from `matrix` alone.

### Candidate **separate** restricted test, not an NEE update

The narrowest test this archive might permit is:

> Conditional on evolved treatment, contemporaneous environment and independently measured flower traits, do **direct observed visits to each plant** improve held-out prediction of its subsequently matured seed production beyond a trait-only baseline, when entire assay matrices are excluded from training?

This is a measurement/partial-operator sufficiency question, **not** prospective landscape collapse forecasting. If already addressed by the source article, the result would be a reproducibility/measurement demonstration, not new ecological discovery.

**Provisional model family, not yet frozen for fitting:**

- M0: evolved treatment and current environment + pre-bioassay flower count and core floral traits, with predeclared cohort/replicate effects where estimable; no future seed/fruit measure as feature.
- M1: M0 + **direct plant-level pollinator visitation measured before seed maturation**.
- Compare proper held-out scoring (e.g. seeds model predictive deviance/NLL) on disjoint **whole `matrix` groups**, never randomly held-out individual plants in the same bee assay.
- Prior to reading outcome rows: verify unique (plant, cohort, matrix) grain, treatment-by-matrix structure, exact temporal semantics, missingness, valid independent blocks and baseline/design differences; freeze score and positive-support threshold after eligibility but **before** values are opened.
- Explicitly track genetic-treatment grouping as a **proxy for prior selection history**, not allele variation, and evaluate how little independent block replication there actually is. If enough matrices or distinct treatment variation do not exist for transfer, report `NOT_IDENTIFIABLE`.

Novelty ceiling: The original source paper already reports that evolution under bee pollination increases flower display and seed set in heat stress, so merely rediscovering a positive direct visit–seed relationship would be weak and should not enter the Nature Ecology & Evolution flagship as a new natural validation.

## Related, separate 2026 figshare source

Traine, Schiestl & Rusman (2026), *Functional Ecology* `10.1111/1365-2435.70435` provides data/code at [figshare 31239511](https://doi.org/10.6084/m9.figshare.31239511). This is a **different experimental evolution programme** with pollinator-community context (bees, butterflies or both) and temperature, with reported non-additive trait evolution. Only public article/file metadata are eligible for exploratory source discovery here; never merge it with the New Phytologist plants by treatment label or presumed individual ID. The published paper has already tested temperature-dependent nonadditivity, so it cannot be the new claim on its own.

## Execution contract

`scripts/probe_traine_plant_source_headers.py` fetches official Dryad/Figshare metadata and, if public source permits, up to **one bounded CSV file/header per archive**. It writes only exact member names/sizes, file SHA-256, first-row **column names**, HTTP stop codes and whether a raw header was obtained. No measured values, genotype frequencies, visitation counts, seed outcomes, coefficients, p values or source rows are printed or fitted. The associated unit tests enforce the source firewall.

Possible results:

- **`RAW_HEADER_VERIFIED`**: continue independently to join/time/replication-key gate; this does *not* admit full H-R and does not authorize outcome opening.
- **`METADATA_VERIFIED`**: only filenames/metadata, no validated rows.
- **`ACCESS_OR_SCHEMA_STOP`**: failure of access/format, not a biological null. Do not endlessly rotate unauthenticated downloads.

This audit stays a **separate external source-screen**. NEE evidence pins, the 0/5 previously screened natural H-R denominator, EGWEE natural synthesis, and the previously recorded natural strongest-refuge null are unchanged.


## 2026-10-08 first executed gate and parser repair

- PR #218 source-gate workflow `37785351727`, job `113338572709` completed successfully **as a safety/metadata workflow**. The saved outcome-blind artifact was `11554925648`, `traine-metadata-header-only`.
- Artifact result: Dryad metadata listed **four files**, with target `data_local_adapt_traits.csv` **288,058 bytes**; `raw_verified=false` and `status=ACCESS_OR_SCHEMA_STOP`, detail `ValueError: target_file_id_missing`. **This was not HTTP 401 or HTTP 403**, and no CSV download was attempted. Figshare metadata listed **two files** (one XLSX, one R source); status `METADATA_VERIFIED`, no CSV header.
- **Failed step:** The first probe expected a numeric `id` directly on each Dryad v2 version-file inventory entry, but the response had no `id` field. It did contain Dryad HAL-style file relations; the probe now derives the numeric file identifier only from the documented `/api/v2/files/<id>` or `/api/v2/files/<id>/download` relation and tests that parsing with a synthetic fixture. This is a transport/schema repair, **not a biological or statistical change**.
- **Remaining live gate:** independent exact-commit CI run of the repaired file-stream acquisition. If actual public CSV bytes are denied or have an unexpected schema, classify `ACCESS_OR_SCHEMA_STOP` or `RAW_HEADER_INCOMPLETE` without trying to infer model outcomes. The separate Figshare XLSX cannot supply an equivalent individual CSV unless independently specified and audited.

The previously declared NEE/EGWEE claim boundaries and the full H-R eligibility count remain unchanged.

## 2026-10-08 final public-access audit — no raw plant records obtained

The repaired header-only CI **completed** in GitHub Actions workflow **37788113341**, job **113348033675**, artifact **11555452012**. The metadata request returned four Dryad file entries and correctly parsed target `data_local_adapt_traits.csv` from the official version **429932**, file **4644044** (288,058 bytes; published SHA-256 `4c9162866b4d90afd31c847e19e9de39514ab168088de4ba57e7f3c70d37af77`). The correctly identified public file-stream request then returned **HTTP 403 Forbidden**. No CSV header, row, genotype, visitation or seed value was opened.

Figshare source 31239511 returned two-file **metadata only** (XLSX and R script); no CSV member or matched source ID was discovered. The separate Figshare study is not an alternative file holding the same New Phytologist plants.

**Outcome:** `ACCESS_OR_SCHEMA_STOP` for Traine Dryad; **0 eligible full H-R** and **0 new biological model outputs**. GitHub's CI reported success because *properly classified access failure* is a supported source-screen outcome, not because the study was analyzed. After an initial metadata parser failure and the repaired 403 request, further unattended unauthenticated retries are stopped. The workflow is switched to **unit tests only on PR**, with source download gated behind explicit manual dispatch when a genuinely authorized route becomes available. This is an access stop, not a test of whether direct interaction adds incremental functional prediction.

**Official Dryad file-index reference:** `https://datadryad.org/api/v2/versions/429932/files`; **reproducibility receipt:** GitHub run 37788113341 / artifact 11555452012.

