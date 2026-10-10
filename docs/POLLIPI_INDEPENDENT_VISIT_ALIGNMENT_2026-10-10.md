# EGWE × PolliPi: independently verified plant-level visits — measurement eligibility gate

**10 October 2026 — source-contract compatibility and synthetic workflow. No field Pi sessions or real plant genetics were analyzed.**

## What is already available in the existing camera repository

The independent visit-event truth contract in [zuizui0223/pollipi](https://github.com/zuizui0223/pollipi/blob/main/docs/VISIT_EVENT_TRUTH_CONTRACT.md) explicitly requires a `visits.csv` with columns

```
event_id,start,end,truth_source
```

Optional `visitor_group`, `reviewer_id`, `confidence`, `reference_file` and `notes` support quality and taxonomic evidence. Allowed truth sources are `continuous_reference_video`, `high_frequency_reference_video`, `controlled_event_schedule`, `independent_sensor`. Start/end are seconds from the **first probe timestamp** or explicitly clock-aligned ISO times. `PolliPi`-selected images, candidate windows or shadow metadata **must not be used as event truth**.

In the current [PolliPi field-readiness protocol](https://github.com/zuizui0223/pollipi/blob/main/docs/FIELD_READINESS_CHECKLIST.md), capture is fixed-interval high-resolution JPEG with shadow-mode advisory metadata; live adaptation is disabled. The [TNOA annotation contract](https://github.com/zuizui0223/pollipi/blob/main/docs/TNOA_FIELD_ANNOTATION_PHASE_B.md) also separates reference event truth, coupled flower responses, exogenous nuisance and observability, keeps calibration unfrozen and forbids inferring biological events from algorithm scores. **These restrictions remain active; EGWE cannot reinterpret still captures as counted insect visits.**

The existing PolliPi `visits.csv` has no focal plant identifier because it represents **one independently annotated run**. To connect that reference to EGWE's patch/genetic state requires a **separately frozen run→plant identity table**. Appending an arbitrary plant ID to detected stills after observing outcomes is not an acceptable substitute.

## New fail-closed bridge

`scripts/audit_pollipi_independent_visits.py` ingests:

1. A JSON `--manifest` declaring `analysis_unit` site, cohort and common UTC start/end, plus the fully enumerated set of candidate focal plants, their patch/plant IDs, genetic-assay labels, pre-state scores, pre-state measurement times, complete common observation opportunity and externally declared visit caps.
2. A `reference_runs` section binding each independent `visits.csv` file to **exactly one** tagged plant and its exact patch/cohort, one synchronized reference window and an independent reference recording.
3. The original event files via `--visits-dir`, using PolliPi's required `event_id,start,end,truth_source` columns.

The run manifest requires assertions of:

- independent full-window reference coverage **including true zero-visit intervals**;
- every focal flower on the tagged plant visible to the independent reference;
- no unresolved independent-reference interval in that window;
- a clock-origin that equals the declared common window start (seconds from the first reference probe, an intentionally strict subset of PolliPi's permitted timing formats);
- event intervals entirely inside the independent recording, no duplicate event IDs *within* a run;
- no JPEG/PNG as independent truth and no candidate/shadow/selected-still label as `truth_source`;
- independently justified per-plant caps and genetics/trait measurements predating observations.

On any unresolved identity, clock, coverage, event or source contradiction the bridge stops with `STOP_SOURCE_ID_TIME_OR_REFERENCE_TRUTH`; it never fabricates an observed absence. A `visits.csv` with header and **no event rows** is an eligible *zero count* only if the run independently covered the complete interval and focal flowers.

When structurally consistent, counts are passed to `conditional_bounds_without_site_total()` from the exact PR #221 algorithm; the result is merely a **mathematical conditional interval** for the supplied score. It remains **unlicensed for natural ecological effects** until the independent annotations, camera detection/false-positive and cap assumptions are validated outside this self-reported manifest. Real seed, fruit, fitness or future loss data are never opened by this script.

Critically, this is the **no-complete-site-total** route. Five Raspberry Pi cameras looking at five of eight tagged plants do not supply the six/eight-plant population's visit total. This bridge does not infer, fabricate or silently substitute such a total. If a true complete census is later measured, that is a separate contract and analysis branch.

## Runnable synthetic-only end-to-end example

The files `tests/fixtures/pollipi_truth_bridge/synthetic_manifest.json`, `visits_R1.csv` and `visits_R4.csv` are entirely **fabricated** and do not represent real Pi videos or verified reference-event annotations.

```bash
python scripts/audit_pollipi_independent_visits.py \
  --manifest tests/fixtures/pollipi_truth_bridge/synthetic_manifest.json \
  --visits-dir tests/fixtures/pollipi_truth_bridge \
  --output /tmp/synthetic_pollipi_alignment.json
```

Four hypothetical plants have scores `[0.1,0.3,0.7,0.9]`, 600 seconds of common effort, at most 8 potential visits per plant, and two plants' **independently invented** true-visit files contain 3 and 7 events. Only these two observed plant counts enter a sharp conditional interval; the other two plant counts remain unknown. The interval width is **0.8/600** in visits/second covariance units (not the unscaled 0.8 of the unit-effort mathematical illustration). The bridge reports `uses_synthetic_state=true`, `field_effect_inference_licensed=false`, `site_total_imputed=false`, `natural_HR_validated=false`.

The unit test suite also tests false positives from wrong plant/patch/cohort, missing reference video coverage, inaccessible flowers, unresolved truth windows, clock drift, source-prohibited JPEGs, illegal event times, future state leakage, invalid caps, duplicates and missing columns.

## What still needs real measurements

This bridge **does not remotely access or redeploy PolliPi devices**. It modifies no Pi capture policy. The five existing devices remain under the PolliPi field protocol; their deployment state cannot be inferred from this repository.

A genuine field test needs:

- individual `plant_id` tags fixed before seeing reproductive outcomes, with mapped flower/patch IDs and independently assayed or appropriately designated pre-state genetic/trait scores;
- separate independent full-window visit-event truth for each monitored plant (reference video or independently validated equivalent; not sparse JPEGs);
- credible prior physical/event-cap information for **all unmonitored plants** if using the no-total sharp-interval method;
- predeclared error calibration, missingness and human observer reliability;
- independent replicated sites/landscapes/cohorts for prospective H-R prediction, then **later** seed/fruit/recruitment outcomes with frozen time and scoring rules.

Until those are actually collected, the current result is a reproducible **measurement eligibility tool**, not positive or negative ecological evidence.
