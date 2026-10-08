# Outcome-blind natural source audit: Pearson 2018 exPt2 and prospective future data

**Date:** 2026-10-08
**Status:** `STOP_EXPT1_JOIN; HOLD_EXPT2_MATCHED_PUBLIC_FORWARD_DATA`. Public metadata assessment only; **no 2018 donor ID or future response values opened**. This is not a null eco-genetic result.

## Question and present inferential boundary

Can the *same* 2018 Echinacea pollen-donor plants in Pearson et al. (2023) be linked to a public, year-2019-or-later individual-level function record in **exPt2**, under an independently verifiable donor identifier, with a valid out-of-sample holdout?

Prior audit established Pearson's 2018 experiment in exPt2 and correctly rejected a proposed match to public **exPt1** Core. This follow-up checks whether the source project already publishes a matched **exPt2** longitudinal panel; it does not attempt to force exPt1 identifiers or secondary study offspring cohorts to match.

## What official project sources actually say

| Evidence layer | Source-derived observation | What cannot be inferred |
| --- | --- | --- |
| Pearson *Big Event* 2018 | Researchers recorded hundreds of bee visits and seed/paternity for the experiment at **exPt2**; original project post says to contact Jennifer Ison for the study data | This does not supply an open, cross-year **same-donor** panel |
| exPt2 2019 annual work | 2,050 positions checked; 1,802 living plants; **654 flowering plants**, about 1,100 heads harvested | Aggregated plot-year totals do not identify the original 2018 donor IDs |
| exPt2 2024 annual work | 1,725 positions checked; 1,190 living; **302 flowering**; 375 heads harvested | Measurements taken does not imply freely downloadable keyed data |
| 2024 exPt2 record locations | Project post describes phenology in `~/cgData/summer2024/exPt02Phenology`, measurements in an SQL database and harvest metadata in Dropbox/SQL | Internal file/database locations are not publicly usable archive member IDs |
| Public project dataset catalogue | Public longitudinal **Core** is listed for **exPt1**; no verified public exPt2 same-donor annual panel was found during this targeted audit | A catalogue gap is **not proof that no exPt2 dataset exists anywhere** |
| Earlier pollinator-effectiveness dataset page | The page still says **“We will post our dataset here soon”** and offers 207 videos | Video collection and a promised dataset are not independently keyed longitudinal genotype/function rows |
| 2025 outcrossing/phenology fitness paper | Its intergenerational design used parents in **exPt01** and progeny in **exPt02** | A distinct cross-generation cohort is not the Pearson 2018 pollen-donor panel |

Evidence: [Pearson exPt2 Big Event](https://echinaceaproject.org/2018-update-pollinators-influencing-male-and-female-fitness-a-k-a-the-big-event/); [2019 common garden](https://echinaceaproject.org/2019-update-common-garden-experiment/); [2024 common garden](https://echinaceaproject.org/2024-update-common-garden-experiments/); [project dataset catalogue](https://echinaceaproject.org/datasets/); [Page et al. data page](https://echinaceaproject.org/datasets/pollinator-effectiveness/).

## Determination

**Source observation**: exPt2 truly has longitudinal *measurements*, including post-2018 flowering and harvest observations. The dataset catalogue does not establish an accessible raw 2019+ exPt2 **plant ID × year** file overlapping Pearson's 2018 donor sample. The older published Page et al. study in P2 contains visitor/genetic analyses in 2013–2014, but its project-hosted dataset page is a placeholder and the earlier cohort is not the Pearson 2018 donors.

**Inference**: no honest donor-level forward fit can be started, because plant identity, observation/response chronology, outcome schema, and independent holdout replication are not jointly known.

**Status**: `STOP_EXPT1_JOIN; HOLD_EXPT2_MATCHED_PUBLIC_FORWARD_DATA`. It is incorrect to say the data *do not exist*; only that the specific public matched source was not verified. No natural H-R success/failure is counted, and 0/5 of the earlier new-source roster remains eligible.

## A new, bounded alternative prior-art check (not H-R evidence)

The 2025 *Asclepias viridiflora* programme [Dryad 10.5061/dryad.pzgmsbd17](https://doi.org/10.5061/dryad.pzgmsbd17), published as [Maton et al., *Annals of Botany*, 10.1093/aob/mcaf287](https://doi.org/10.1093/aob/mcaf287), reports 102 mature sampled plants, 179 progeny genotyped with 19 microsatellites, strong genetic diversity retention, predominantly short-distance pollen flow but occasional events as far as 9 km. Its archived public **file index/README** advertises **one genotype spreadsheet plus README**; no longitudinal trait, co-timed visitation and subsequent functional outcome file is identified there. It is strong prior art that **fragmentation or low landscape connectivity does not automatically imply loss of functional pollen connectivity**, but it is *not* prospective evidence that patchwise interaction–genetic covariance improves later-function prediction.

## Stop rules and next external evidence gate

1. Do **not** match exPt1 Core plants to exPt2 Pearson donor IDs, and do not use a 2025 exPt01-parent/exPt02-progeny pedigree as a surrogate.
2. Do **not** turn published exPt2 plot-year totals or 207 videos into donor-level data.
3. Do **not** convert missing public access into failure of the ecological H-R hypothesis.
4. A future open exPt2 panel would need an explicit `experiment_plot=exPt2` declaration, matching individual donor key, dates after 2018, directly defined functional endpoint, source hashes, matched denominator, and independent holdout units **before** outcome data opening.
5. Search farther afield for a genuinely public independent **multi-year** patch-level interaction × genotyped trait × future-function source, rather than continuing unproductive exPt1/exPt2 joins or upgrading companion evidence as validation.

The machine-readable audit is `artifacts/empirical/expt2_forward_source_eligibility_20261008.json`. This supplement is kept **outside** the frozen NEE flagship manuscript and scientific ledger.
