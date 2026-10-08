# Eight-season Love–Otto panel-composition sensitivity — official YHT

Status (2026-10-08): **outcome-free exploratory measurement audit registered before running the eight-season GPS metrics**. Not a replacement for the frozen Ya Ha Tinda future-recruitment STOP.

The 2026 Love & Otto spatial-cohesion paper reports power to detect spatial redistribution with sparse sampling in simulation. The pinned 2004 YHT teaching mirror has already shown that the CV ratio can change appreciably according to which ten of eleven or twelve collared females are selected. The official archive contains eight autumn years meeting the frozen movement-only gate (2004, 2013–2019), but only six with future recruitment coverage. Thus the primary prospective-demography test remains STOP, independently of this analysis.

This audit asks a narrower ecological measurement question: **does apparent population spatial-cohesion change remain stable when exactly ten tracked animals are repeatedly selected, compared with the geometry of all simultaneously collared animals?**

It uses the same official Movebank DOI `10.5441/001/1.5g4h5t6c`, immutable event SHA-256 `1069cd7531d1d7a519cb817b09d015be91c552ecafab504869a81eb01eff4201`, source-managed GPS/visibility flags, fixed September 15–November 15 window, local-noon ±6.5h rule, minimum ten females per day and minimum 30 days per year. All distances use NAD83/GRS80 UTM11N and the pinned Love–Otto CV_ind/CV_pop formula.

For each eligible day, compare the full-collared ratio with 100 deterministic selections of ten distinct collared females (one unique set when n=10). The output is an **aggregate year-level** set of within-day conditional subset standard deviations, 10%–90% spread, daily changes and signed-change disagreement, plus annual full-collared versus fixed-ten means.

The full collared sample is **not** the true geometry of the entire herd. Randomizing among collars measures instability conditional on monitored animals, not biological observation error for uncollared individuals. The 100 subsamples are not independent ecological replicates. No outcome, alarm threshold, forecast discrimination or ecological collapse label is computed.

Protocol: `experiments/yht_official_panel_sensitivity_protocol.json`. Code: `src/eco_genetic_warning_extensions/yht_official_panel_sensitivity.py`. Runner: `.github/workflows/yht-official-panel-sensitivity.yml`. The workflow downloads raw official locations into a disposable runner and uploads only aggregate JSON. If official source hashes or the eight-year coverage contract disagree, the audit stops.

No inference about future population fate is permitted from this audit alone.
