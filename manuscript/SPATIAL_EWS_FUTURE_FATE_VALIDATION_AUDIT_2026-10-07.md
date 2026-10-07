# Spatial early-warning versus future-fate validation audit

Date: 2026-10-07

## Question

The narrow unresolved claim is not whether spatial structure correlates with ecological condition, nor whether spatial indicators change before a known transition.

It is:

> **Does a spatial fragmentation/cohesion state measured at time t contain incremental information about a later demographic or functional endpoint, beyond the contemporaneous biological state, under genuinely out-of-sample temporal validation?**

This audit distinguishes seven validation requirements:

1. **natural/wild data** rather than simulation only;
2. a **spatial fragmentation/cohesion predictor** measured before the endpoint;
3. an explicit **later demographic/functional endpoint**;
4. a pre-specified or clearly defined **forecast horizon**;
5. a full denominator containing both later deterioration/events and later non-events/relative successes;
6. **held-out temporal or population validation**, rather than fitting and evaluating the same historical transition;
7. an **incremental baseline comparison** showing whether the spatial score adds information beyond current abundance/range/demographic state.

A paper need not satisfy these criteria to be a valid early-warning study. The criteria define the stronger claim of **future-fate validation**.

## Closest literature

| Study | Natural/wild | Spatial warning/state metric | Later fate endpoint | Future temporal direction | Full denominator / controls | Held-out forecast | Adds beyond current state? | What it establishes |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| Kéfi et al. 2014, PLOS ONE | no | yes | model transition | simulated | simulated | no | no | General spatial-EWS toolbox; explicitly says empirical validation lagged theory. |
| Génin et al. 2018, MEE | partial case-study examples | yes | degradation/state transition | mostly monitoring/gradient | not a fate denominator | no | no | Reproducible spatial-EWS workflow; explicitly says out-of-lab spatial evidence remained scarce. |
| Gsell et al. 2016, PNAS | yes, 5 aquatic systems | no: temporal EWIs | known later regime shift | yes, retrospectively | **no comparable non-transition controls** | no prospective holdout | no | Natural EWIs can precede known transitions, but reliability is low; authors explicitly note lack of controls for true negatives. |
| Roberts et al. 2022, Ecological Applications | yes, 23-y prairie-chicken system | yes: grass–woody regime boundary | habitat loss / lek usage | boundary tracked through time | not future fate events/non-events | no rolling future holdout | no | Strong wild spatial-state warning: vegetation boundary strength tracks habitat encroachment and contemporaneous/lagged lek occurrence. |
| Drake et al. 2022, Journal of Animal Ecology | yes, 17-y, 98-patch water-vole metapopulation | yes: dynamic connectivity | occupancy dynamics | dynamic | full occupancy history | model comparison, not frozen EWS forecast | not in the EWS sense | Demographically weighted, time-varying connectivity better describes metapopulation dynamics; connectivity is constructed from occupancy dynamics rather than frozen as an external warning score. |
| Cerini et al. 2025, Ecology | experimental lab | movement speed, morphology, temporal EWS | abundance decline/collapse | yes | replicated perturbations/controls | onset-order analysis, not wild future holdout | partly | Behavioral change can precede abundance decline in a forced collapse, but the sequence was stressor-dependent and is not a spatial-fragmentation warning test. |
| Peled, Kim & Greenbaum 2026, PNAS | empirical network geometry + simulated genetics | network/genetic fragmentation signals | rapid loss of genetic health | simulated future | simulation replicates | simulation proof-of-concept | not demographic baseline | Genetic-monitoring EWS can precede simulated genetic transitions; authors explicitly call empirical application future work. |
| Love & Otto 2026, MEE | yes for caribou/jackdaw demonstrations | **yes: CV_ind, CV_pop, ratio** | spatial splitting/state | no later demographic endpoint | no future event/non-event denominator | no | no | Strong animal spatial-state detector; field examples validate seasonal/behavioral organization, not later demographic fate. |
| Lewis et al. 2023, Ecological Monographs | yes, 18-y songbird demography | range position + climate/demographic process | future viability/extirpation | yes | multiple plots | future projection, not held-out EWS validation | demographic/climate model | A real wild demographic forecast tied to range contraction, but spatial contraction is the response/context rather than a frozen warning statistic. |
| Historical range-contraction/extinction-risk analyses | yes / macroecological | range change | current threat/extinction status | historical-to-current | cross-species | mostly cross-sectional | often range size/body size controls | Range contraction can associate with extinction risk, but this is not short-horizon population-level warning validation. |
| Social-connectedness survival studies (e.g. baboons, giraffes) | yes | individual social-network metrics | survival/longevity | yes | survival denominators | survival models | environmental/demographic covariates vary | Social organization can predict individual fitness; this is not population-level spatial fragmentation/cohesion forecasting. |

## What the strongest natural EWS paper shows—and still leaves open

Gsell et al. (2016) is an important boundary against overclaiming novelty. It used natural long-term time series from five freshwater ecosystems and found some temporal early-warning indicators several years ahead of documented transitions.

However, the authors explicitly state that they lacked comparable records from systems without transitions with which to estimate true-negative behavior. Their design therefore establishes **retrospective temporal precedence before known transitions**, not prospective event/non-event discrimination across future outcomes.

That distinction is directly relevant here:

`precedes observed events` is not the same estimand as `discriminates future events from future non-events`.

The finite EGWE warning audit independently demonstrates that these can separate: a marker can precede every event while also firing in every non-event.

## Why Roberts et al. (2022) is the closest field spatial precedent before Love & Otto

Roberts et al. use 23 years of Greater Prairie-Chicken lek locations and remote-sensed grass–woody regime boundaries. Their spatial regime metric is biologically meaningful and strongly tied to lek occurrence. The woody regime expands inward while the estimated usable grassland core contracts.

This is a genuine empirical **spatial early-warning** application.

But its target is primarily:

`spatial habitat regime at time t -> habitat/lek-use state around time t`.

It does not freeze the boundary metric at time t and ask whether it improves held-out prediction of demographic performance at `t+h` after current lek abundance/state is included.

Thus Roberts et al. narrows the unresolved gap rather than closing it.

## Why Love & Otto (2026) is the closest animal-spatial measurement precedent

Love & Otto move the measurement target from habitat boundaries to the spatial organization of the animals themselves.

Their CV metrics are attractive for future-fate validation because they are:

- threshold-free;
- scale-free;
- estimable from sparse individual locations;
- explicitly designed to distinguish shape change/splitting from uniform density or symmetric range-size change;
- demonstrated in wild caribou and jackdaws.

This makes their metric family a particularly clean candidate for the stronger test:

[
P(F_{t+h} mid 	ext{current state}, 	ext{spatial CV state})
]

versus

[
P(F_{t+h} mid 	ext{current state}).
]

Their published validation does not evaluate this difference.

## Dynamic connectivity is close, but not the same estimand

Drake et al. (2022) show with a 17-year, 98-patch water-vole dataset that connectivity metrics improve when weighted by temporally varying occupancy. This is strong evidence that static landscape geometry is an inadequate description of population connectivity.

However, dynamic connectivity there uses the metapopulation's occupancy process to construct the connectivity variable being fitted to occupancy dynamics. The question is therefore how to represent an ongoing spatially structured process, not whether an independently frozen spatial warning statistic adds future information beyond the current demographic state.

This is a useful mechanistic precedent but not a direct future-warning validation.

## Genetic fragmentation warning does not close the demographic gap

Peled, Kim & Greenbaum (2026) explicitly develop early warning signals for fragmentation. Their tipping target is a rapid deterioration in **genetic monitoring variables** generated by the network-population-genetic model. The warning analysis is a simulation proof-of-concept, including simulations on empirical network structures.

It is an important novelty boundary:

> genetic early warning under fragmentation is already a live literature.

But it does not establish that a spatial fragmentation/cohesion score measured in a wild population predicts later demographic fate.

## The strongest current gap statement

After the targeted search above, the defensible claim is:

> **Spatial early-warning research has progressed from model-based spatial indicators to natural-system state tracking and, most recently, to sparse animal-location metrics. Natural temporal EWS can also precede known ecosystem transitions. However, among the closest studies reviewed here, we did not identify a wild-population test that freezes a population-level spatial fragmentation/cohesion score at time t and demonstrates incremental, held-out prediction of later demography beyond contemporaneous population state.**

This should **not** be shortened to “spatial early warning has never been empirically tested.”

That would be false.

The untested object is specifically **incremental future-fate discrimination/forecasting**.

## Minimum test needed to close the gap

For population-year `t`, define:

- current demographic state `D_t`;
- current spatial scale/range `R_t`;
- frozen spatial cohesion/fragmentation score `C_t`;
- later demographic endpoint `F_{t+h}`.

Compare prospectively or with strict temporal hindcasting:

[
M_0: F_{t+h}sim D_t+R_t
]

against

[
M_1: F_{t+h}sim D_t+R_t+C_t.
]

The spatial score earns **future-warning** status only if it improves genuine held-out forecasting or discrimination, not merely because:

- it changes before known events;
- it correlates with current habitat degradation;
- it distinguishes current behavioral states;
- it correlates with current abundance/range;
- or it is mechanistically plausible.

## Ya Ha Tinda test in this repository

The frozen Ya Ha Tinda protocol is designed to instantiate exactly this missing comparison:

- `C_t`: autumn Love–Otto CV ratio;
- `D_t`: preceding late-winter calf:cow ratio;
- `R_t`: contemporaneous autumn mean pairwise spatial scale;
- `F_{t+1}`: following late-winter calf:cow ratio;
- validation: rolling-origin one-step-ahead;
- score comparison: RMSE and MAE.

The remaining limitation is data availability/temporal replication. Published collar counts leave exactly 11 nominal years capable of meeting the frozen n>=10 requirement, so any failed annual coverage gate stops the primary test.

## Claim boundary if Ya Ha Tinda succeeds

Even a positive result would justify only:

> in one long-term wild elk population, an autumn animal-cohesion statistic supplied incremental one-step-ahead recruitment information beyond the immediately preceding recruitment state and contemporaneous spatial scale.

It would **not** validate spatial EWS generally, establish a universal fragmentation threshold, or prove causal fragmentation-to-decline direction.

## References checked for this audit

- Kéfi et al. (2014), *PLOS ONE*, doi:10.1371/journal.pone.0092097.
- Gsell et al. (2016), *PNAS*, doi:10.1073/pnas.1608242113.
- Génin et al. (2018), *Methods in Ecology and Evolution*, doi:10.1111/2041-210X.13058.
- Roberts et al. (2022), *Ecological Applications*, doi:10.1002/eap.2480.
- Drake et al. (2022), *Journal of Animal Ecology*, doi:10.1111/1365-2656.13783.
- Lewis et al. (2023), *Ecological Monographs*, doi:10.1002/ecm.1559.
- Cerini et al. (2025), *Ecology*, PMID 40953834.
- Peled, Kim & Greenbaum (2026), *PNAS*, PMID 41706903.
- Love & Otto (2026), *Methods in Ecology and Evolution*, doi:10.1111/2041-210x.70375.
