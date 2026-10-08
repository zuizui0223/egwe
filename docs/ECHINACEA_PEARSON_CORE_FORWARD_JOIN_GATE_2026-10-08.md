# Echinacea plot provenance correction and forward-data eligibility (2026-10-08)

**Decision: STOP the proposed Pearson 2018 × exPt1 Core linkage.** This is a documented **plot mismatch**, not just a missing individual-ID crosswalk. No outcome records were opened, no data were joined, and no new ecological model was fitted.

## 1. Identified error and definitive source check

Previous proposal treated the publicly downloadable exPt1 Core panel as a potential 2019+ response table for the 2018 Pearson donor-visit experiment, contingent on an unknown study-plot match. That contingency has now been resolved **against** the proposal.

- [Echinacea Project's original 2018 Big Event report](https://echinaceaproject.org/2018-update-pollinators-influencing-male-and-female-fitness-a-k-a-the-big-event/) explicitly records **Location: exPt2**, **Start year: 2018**. It describes the multi-pollinator restriction experiment on individual pollen donors and direct reproductive measurements that underlie Pearson et al. (2023).
- [Pearson et al. (2023) source data and methods](https://openworks.wooster.edu/facpub/418/) belong to that 2018 experiment. The published paper [DOI 10.1002/ajb2.16190](https://doi.org/10.1002/ajb2.16190) discusses a 60 × 80 m experimental common garden but the site's dimensions alone do not establish study-plot identity.
- [Echinacea Project exPt1 Core documentation](https://echinaceaproject.org/datasets/expt1-core/) explicitly states its panel is **experimental plot 1** (not exPt2). Core keys are `cgPlaId`, `row`, `pos`, `yrPlanted` and yearly `ld`, `fl`, `hdCt`, `achCt`. The **2024-12-11 documented version** has survival/flowering through 2024 but achene/seed-head counts through 2017 (with partial heads); one cannot claim 2019+ achene success even for exPt1 from that release.
- [2024 common-garden project update](https://echinaceaproject.org/category/experimental-plot-management/) shows exPt02 annual measurements and harvests are actually collected, but places row-level phenology in a project `cgData` repository, measurements in a SQL database and harvest metadata in project Dropbox. Its public summary **does not provide** a verified freely downloadable 2019+ exPt2 longitudinal plant-key panel.

**Plot identity is now known and false for the proposed join: exPt2 != exPt1.** Numeric identifiers, if present in both CSVs, must never be matched across distinct plots.

## 2. Independent forward-outcome check

The 2022 [Reed et al. genetic variation in flowering time](https://doi.org/10.1002/ajb2.16072) reports phenology of parental cohorts in 2005–2006 and offspring in **2014–2017**. It does not by itself supply a 2019+ within-exPt2 outcome for the Pearson 2018 donor sample. Long-term exPt2 observations are described in annual project reports, but their existence is not equivalent to public individual records with a documented crosswalk.

The original Pearson 2018 within-season donor-visitation to offspring-paternity comparison also does **not** become a future-year test by using offspring germination as a later processing date; the ecological fertilisation/siring event happened in 2018.

## 3. Fail-closed scientific decision

| Question | Current decision | Consequence |
|---|---|---|
| Does Pearson's 2018 experiment use exPt1? | **No: exPt2** | **STOP exPt1 cross-archive join** |
| Does public exPt1 Core provide a 2019+ achene endpoint? | **Not established; 2024-12-11 release documents counts to 2017** | Do not claim post-2018 achene success from that file |
| Are exPt2 plant-level measurements made after 2018? | **Yes, reported operationally** | Does not establish public access or exact donor crosswalk |
| Is an exPt2 2019+ raw annual panel with linked Pearson plant IDs publicly verified? | **No** | `HOLD_EXPT2_PUBLIC_FORWARD_PANEL_SEARCH` |
| Did the programme test H-R or its natural warning predictor? | **No** | Maintain 0/5 confirmed full H-R datasets |

## 4. Correct prospective route (conditional, not executed)

Only a genuinely exPt2-specific 2019+ archived panel, with verified `plot=exPt2` and exact donor key crosswalk, would allow a *new and narrower* individual temporal forecast. The future endpoint, observation time, sampling effort, pre-outcome covariates and independent holdout units must be frozen before response values are opened. Even a successful join would not automatically identify local interaction × genetic co-location or show generality across independently fragmented landscapes.

**No author contact or private-source upload requested at this stage.** The published exPt2 information can be preserved as context; the exPt1 route is permanently closed absent a demonstrably corrected source identity rather than by mere renaming.

## 5. Related prior-art boundary

Published Pearson et al. already demonstrated that pollinator visitation and pollen removal are not interchangeable with direct male fitness. Ison & Wagenius (2014) tested flowering time × conspecific spacing on reproduction, and Reed et al. (2022) documented genetic variation in flowering phenology. Therefore neither "spatial mate opportunity matters" nor "pollinator taxon affects mating" is itself a new contribution of EGWE.

### Exact source references

- Pearson experiment exPt2: https://echinaceaproject.org/2018-update-pollinators-influencing-male-and-female-fitness-a-k-a-the-big-event/
- Pearson archived source files: https://openworks.wooster.edu/facpub/418/
- exPt1 Core documented columns/coverage: https://echinaceaproject.org/datasets/expt1-core/
- Project exPt02 longitudinal operations: https://echinaceaproject.org/category/experimental-plot-management/
- Reed et al. 2022: https://doi.org/10.1002/ajb2.16072
- Ison & Wagenius 2014: https://doi.org/10.1111/1365-2745.12262
