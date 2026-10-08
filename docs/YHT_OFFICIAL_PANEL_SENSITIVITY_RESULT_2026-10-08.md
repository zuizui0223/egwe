# Official Ya Ha Tinda panel-composition sensitivity result — 2026-10-08

**Status: exploratory, outcome-free measurement result. Not a future-demography test or an early-warning validation.**

## Source and execution

- Official Movebank DOI `10.5441/001/1.5g4h5t6c`, original GPS CSV SHA-256 `1069cd7531d1d7a519cb817b09d015be91c552ecafab504869a81eb01eff4201`.
- Pre-outcome/source-locked protocol: `experiments/yht_official_panel_sensitivity_protocol.json`.
- Successful GitHub Actions run [37727336975](https://github.com/zuizui0223/egwe/actions/runs/37727336975), job `113148401737`, aggregate-only artifact `11530501862`, ZIP SHA-256 `0d70640fb9a1d0807646802f3959180d7a698406b8285cb2b31b1b170b53e25b`.
- Pinned machine-readable summary: `artifacts/yht_spatial_warning/official_panel_sensitivity_result.json`.
- The original 11-year future-recruitment minimum remains **STOP**; the official archive provides only six eligible GPS/outcome-overlap years. No demographic outcomes were opened by this measurement audit.

## Outcome-free result

**474 qualifying days across eight autumn seasons**; in **460 days** there were more than ten collared females, making the identity of the ten selected animals consequential.

Across days with a panel choice, the median **within-day SD across deterministic ten-animal subsets** was **0.09926** in the Love–Otto CV_ind/CV_pop ratio. This is conditional on which collared animals happened to be observed, not an uncertainty estimate for the entire herd.

The sign of consecutive eligible-day change disagreed between the average fixed-ten metric and the all-collared metric in **39.1%** of comparisons. This includes arbitrarily small daily changes: a sign disagreement does **not** by itself demonstrate a biologically important false signal, and there was no frozen minimum-change threshold.

The descriptive correlation between eight annual fixed-ten and all-collared means was **0.666** (n=8, not eight independent population replicates).

## Year-level results

| Autumn year | Qualifying days | Mean collared females/day | Mean fixed-ten CV ratio | Mean all-collared CV ratio | Adjacent-day direction disagreement | Median timestamp spread |
|---:|---:|---:|---:|---:|---:|---:|
| 2004 | 40 | 10.9 | 0.568 | 0.568 | 23.1% | 2.0h |
| 2013 | 62 | 16.1 | 0.559 | 0.583 | 21.3% | 7.0h |
| 2014 | 62 | 25.1 | 0.605 | 0.653 | 27.9% | 8.0h |
| 2015 | 62 | 17.6 | 0.638 | 0.696 | 44.3% | 5.0h |
| 2016 | 62 | 41.9 | 0.566 | 0.686 | 42.6% | 4.0h |
| 2017 | 62 | 34.4 | 0.611 | 0.667 | 45.9% | 6.0h |
| 2018 | 62 | 25.9 | 0.605 | 0.681 | 62.3% | 5.5h |
| 2019 | 62 | 26.8 | 0.584 | 0.656 | 39.3% | 7.0h |

Individual GPS fixes were selected within ±6.5 h of local noon. Their median **earliest-to-latest spread within a single accepted day** was **6.03 h**, with 90th percentile **9.03 h**. The data therefore describe approximately co-timed rather than truly simultaneous positions. The snapshot-time discrepancy is measured, but its contribution to CV error is **not isolated** by the panel comparison.

## Interpretation and limits

The finite result is: under the real Ya Ha Tinda collar architecture, the value and even the direction of changes in a Love–Otto inter-individual-distance CV ratio can depend noticeably on which **ten instrumented females** are chosen. This is a caution against treating a sparse panel's apparent spatial response as an error-free description of the collared group.

It is **not** a claim that Love & Otto's paper predicted future demographic loss; nor does this analysis disprove that possibility. No calf recruitment, survival, abundance, decline threshold, ROC, warning specificity or held-out demographic outcome was analyzed.

Other sampling-design papers (e.g. He et al. 2023 and Janousek et al. 2026) already establish general collar-sampling effects. Here the specific contribution is an exact metric-specific sensitivity audit using an immutable wild GPS dataset and a prespecified ten-animal design.

Crucially, **all-collared is not whole-herd ground truth**. Most monitored animals do not constitute a random sample of the full elk herd, and 100 deterministic panels are not independent ecological replication. The temporal alignment of GPS fixes and the 2004/2013–2019 season differences also limit interpretation.

## Validation

The dedicated source-hashed GitHub Actions run passed the module tests, official-source checksum check, eight-year coverage check, and aggregate-only output restriction. The same branch's Protocol invariant CI and Two-repository reproducibility contract also passed. No raw coordinates or individual IDs were committed.
