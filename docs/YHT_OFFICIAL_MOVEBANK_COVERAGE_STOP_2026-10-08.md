# Official Movebank YHT coverage and temporal-overlap STOP

Date: 2026-10-08

Status: **official raw GPS coverage actually executed; demographic outcome rows remain unopened for this gate**.

## New information beyond the nominal study-year screening

The official Movebank DSpace data package was downloaded inside a disposable GitHub Actions runner, with the original CSV SHA-256 verified and only aggregate coverage preserved. See source workflow `37641755074`, job `112862252297`, artifact `11492869551`.

The archive reports 175 animals and 1,585,456 locations. The event CSV SHA-256 is
`1069cd7531d1d7a519cb817b09d015be91c552ecafab504869a81eb01eff4201`.

Under the **unchanged frozen biological gates** (Sep 15–Nov 15, nearest-noon ±6.5h, at least 10 distinct GPS females/day, at least 30 qualifying days/year), the actual movement-eligible years are:

`2004, 2013, 2014, 2015, 2016, 2017, 2018, 2019`

Eight years, not the original eleven nominal years.

The official aggregation exposed a decisive detail: **2005 and 2006 had zero qualifying days**, with maxima of only 6 and 8 simultaneously qualified individuals. In 2004 there were 40 qualifying days; each year 2013–2019 had 62.

## Final primary overlap

The frozen recruitment source `YHT_CalfCowRatioData.csv` (Dryad DOI `10.5061/dryad.6wwpzgmw7`) has a published late-winter calf:cow series ending in 2018. By the locked time direction, autumn year `t` predicts late-winter `t+1`, so the latest eligible autumn year is **2017**.

The intersection is exactly:

`2004, 2013, 2014, 2015, 2016, 2017`

Therefore:

`observed maximum n = 6 < 11 = protocol minimum`.

This is a stronger STOP than the pre-acquisition nominal upper bound of 8. It incorporates the actual source coverage without using any demographic outcome values.

## Scientific interpretation

This result does **not** mean the Love–Otto spatial cohesion metric failed to predict demography. **No future-demography model was fitted**. Rather, long telemetry duration, many raw fixes and many collared animals in total did not translate into enough simultaneous pre-outcome population-years.

A new candidate must pass a two-sided calendar overlap screen (movement sampling *and* later outcome availability) before any score computation.

## Firewall and provenance

- This is a source-validation outcome, not a positive/negative ecological association.
- Original animal locations were not committed or uploaded as workflow artifacts.
- The official movement run performed only yearwise coverage on timestamp, identifier and source-managed quality fields; it did not read recruitment outcomes.
- Source PDF: Ya Ha Tinda Elk Project Annual Report 2018–2019 (late-winter recruitment table through 2018).
- Machine-readable pinned summary: `artifacts/yht_spatial_warning/official_movebank_coverage_overlap_stop.json`.
- The earlier temporal-overlap result using eleven nominal collar-count years remains valid as a pre-acquisition **upper bound**, but must not be presented as the observed matched denominator.

We do **not** extend the frozen Dryad outcome series with later annual reports, relax the annual coverage threshold, lower the n=10 daily threshold or replace the target response after learning this result.
