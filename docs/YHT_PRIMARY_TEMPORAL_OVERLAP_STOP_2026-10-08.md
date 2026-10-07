# Ya Ha Tinda primary temporal-overlap STOP

Date: 2026-10-08

Status: **primary stopped before demographic outcome rows were parsed or any future-demography model was fit.**

## Decision

`insufficient_temporal_replication_stop_before_outcome_fit`

The frozen Ya Ha Tinda design requires at least **11** annual observations so that the first seven form the initial training set and at least four later years are genuinely out-of-sample.

That requirement cannot be met by the frozen sources, even if every nominal GPS year passes the movement-coverage gate.

## Why

The primary demographic source was frozen to Dryad DOI `10.5061/dryad.6wwpzgmw7`, file `YHT_CalfCowRatioData.csv`.

The project report underlying that release explicitly describes the late-winter recruitment series as **2001–2018**, with the tabulated calf:cow series running 2002–2018 and no usable 2008 estimate.

The movement-side pre-acquisition audit identified eleven years that nominally have at least ten GPS-collared females:

`2004–2006, 2013–2020`.

But the frozen forecast maps autumn year `t` to late-winter calf:cow at `t+1`. With the frozen demographic series ending in 2018, the latest admissible autumn year is therefore 2017.

The maximum possible primary rows are only:

`2004, 2005, 2006, 2013, 2014, 2015, 2016, 2017`

for a **maximum nominal n=8**, before applying the stricter daily movement-coverage rule.

Thus:

[
n_{max}=8 < 11=n_{min}.
]

No full Movebank download can change this arithmetic.

## Firewall

This decision uses only:

- the predeclared mapping of autumn `t` to outcome `t+1`;
- the frozen Dryad source/time extent;
- published annual GPS collar counts.

It uses **zero row-level calf:cow outcome values** and fits no model.

The public 2017–2021 final report extends field recruitment summaries beyond 2018. It is not added to the frozen primary because the protocol explicitly forbids substituting a different demographic source to rescue sample size after the analysis contract is fixed.

Likewise we do not:

- lower the 11-observation requirement;
- lower the n=10 movement gate;
- shift the autumn window;
- shorten or redefine the forecast horizon;
- promote the minimum-count or adult-survival secondary endpoints.

## Scientific meaning

This is not evidence that Love–Otto spatial cohesion lacks future demographic information.

It means the selected Ya Ha Tinda archive cannot identify the requested strong test under the frozen temporal-validation contract.

That result is useful because it prevents an apparently attractive 20-year telemetry system from becoming a weak retrospective regression with only a handful of true forecast years.

## What remains valuable

The completed movement-side code remains useful:

- the original Love–Otto IID-CV definitions are pinned;
- the fixed-n sampling pipeline is operational;
- the 2004 teaching subset reproduces a real annual spatial state;
- the rolling-origin forecast engine is frozen.

The next empirical system should therefore be selected **first by temporal overlap**: at least 11 population-years with simultaneous individual locations and a genuinely later demographic endpoint, before any outcome is inspected.

## Claim ceiling

The project may state:

> The first locked wild-system candidate stopped before outcome fitting because the available movement and demographic archives did not provide enough temporally aligned forecast years.

It must not call this a null validation of the spatial-warning hypothesis.
