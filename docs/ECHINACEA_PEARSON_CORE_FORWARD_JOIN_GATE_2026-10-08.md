# Echinacea independent natural-data bridge: source-join gate (2026-10-08)

**Status:** prospective source-eligibility design only. No new file downloaded, joined, fitted or outcome inspected in this route. No result is claimed for H-R, H-O or H-P.

## Why this follows the Brassica access stop

The archived Pearson et al. (2023) experiment on *Echinacea angustifolia* measures pollinator visits to **individual pollen-donor plants** over a few days in July 2018, the donor's permitted pollinator taxon, and direct male fitness from offspring paternity. This directly exposes how visitation and effective siring can differ; that ecological finding belongs to the published paper, not this extension.

Separately, the Echinacea Project states that the **exPt1 Core** public dataset contains annual survival and reproductive/fitness measurements for approximately 10,000 mapped common-garden plants, updated over time. This is a *potential* forward endpoint source, not evidence of matched ID or sample membership. Pearson et al. describe a Minnesota common garden approximately 60 × 80 m but its match to the **exPt1 Core** data product has not been independently verified from plant identifiers.

- [Pearson et al. source page with CSVs](https://openworks.wooster.edu/facpub/418/).
- [Pearson et al. peer-reviewed study](https://doi.org/10.1002/ajb2.16190).
- [Echinacea Project dataset catalogue](https://echinaceaproject.org/datasets/).
- [exPt1 Core cited dataset page](https://echinaceaproject.org/datasets/expt1-core/).

## Outcome-blind source gate — must be executed in order

1. Obtain the actual, permitted `SiringSuccessData.csv`, source README and core year-panel metadata. Hash each source independently. Confirm their row grain *only* from headers, candidate identifiers, year/date support and documented schema.
2. **Plot identity**: independently show the source 2018 experimental plot corresponds to exPt1 Core, using source identifiers or published plot provenance, not geographic resemblance alone.
3. **Identifier identity**: document explicit `2018 donor key <-> core plant key` crosswalk, matching key type, unique coverage, multiplicity, duplicates, ambiguous codes, and exclusions. Never fuzzy-match surnames/sites/positions.
4. **Temporal separation**: fix 2018 donor exposure predictors and a pre-specified 2019+ fitness endpoint before viewing any outcome values. For male siring vs future maternal seed set, document the non-equivalence; pollen-donor success in 2018 does not automatically imply the same individual's seed set in 2019.
5. **Exposure independence and confounding**: Pearson's visits come from **one 2018 season**, four observation periods, and a deliberately altered pollinator-access experiment. Distinct donors are not independent experimental landscapes, and a 2018->2019 environmental contrast may reflect burn schedules, large flowering-year fluctuations or unmeasured site processes. Whole-period/plot holdouts may be impossible with one exposure season; declare that as insufficient portability design, not try random row folds.
6. **Ecological interpretation**: if and only if gates pass, formulate a separate limited natural forecast of later *individual* function. It is not a test of patchwise `I_j` × `T_j/G_j` covariance without independently observed joint patch/genetic organization, and not evidence for a universal model coefficient.

## Claim ownership and prior art

Published Pearson et al. already show that pollinator visitation and pollen removal can misrank male fitness. Separately, long-term phenology and reproductive outcomes have been studied in Echinacea. The innovative hypothesis in EGWE remains **matched-marginal spatial relational state + identifiable process + future function**. A simple re-analysis of visits versus contemporaneous siring would replicate known questions and should not be presented as independent novelty.

### Decision today

`HOLD_ID_AND_FUTURE_ENDPOINT_JOIN`. No eligibility promotion until original file keys, plot identity, prospective timescale, and at least one defensible validation unit are verified. The current source-scout registry remains 0/5 full H-R confirmed; Echinacea is a possible narrower natural bridge only.
