# Connectivity is an operator, not a scalar: a finite-model portability test

## Abstract

Ecological connectivity is often represented by a scalar even when the underlying biological process differs. We tested whether a stochastic result attached to one connectivity operator could be reproduced on new stochastic realizations or transported to different movement operators in a finite eco-genetic model. A historical allele-frequency-mixing condition (`m=.10`) showed between-block heterogeneity in one seed family (`p=.020549`). A prospectively locked fresh replication on five new master seeds did not reproduce that pattern (`p=.745130`; exact paired McNemar `p=.693686`). Two further prospective process substitutions reused the same historical no-connectivity and allele-only reference blocks but replaced the update with whole-individual dispersal or paternal-gamete pollen flow; neither process arm showed the historical heterogeneity (`p=.811309` and `.728205`). The two substitutions are not independent baseline replications because their historical reference observations are identical. A post-result precision audit shows that the five-block tests had approximately 80% power for standardized heterogeneity `w≈0.163`, about 8.1–8.2 percentage points weighted RMS block-rate deviation near a pooled rate of 0.5. The result therefore supports a precision-bounded portability failure, not equivalence: a shared connectivity label does not by itself identify a transportable ecological operator.

## Keywords

connectivity; dispersal; gene flow; ecological modelling; transportability; replication; operator identification

## 1. Introduction

Connectivity is routinely reduced to a scalar in ecological models, yet the entities moved and the life-cycle stages affected can differ substantially. Landscape connectivity can mean structural or functional linkage, genetic connectivity can differ from demographic connectivity, and recent frameworks distinguish movement, dispersal and gene flow across ecological and generational scales (Tischendorf & Fahrig 2000; Lowe & Allendorf 2010; Cramer et al. 2023; Liczner et al. 2024). The semantic distinction is therefore established. The unresolved modelling question is narrower: when a stochastic result is attached to one numerical connectivity parameter, what evidence is needed before that result can be transported to another biological operator carrying a similar label?

We use a finite multipatch eco-genetic model to separate two questions that are often conflated. First, does a parameter-specific stochastic pattern replicate under new stochastic realization when the operator is unchanged? Second, does that pattern persist when the biological operator is changed while the historical reference ensemble is held fixed? The first is a replication question; the second is an operator-portability question.

## 2. Methods

### 2.1 Evidence structure

The evidence consists of one independent fresh replication and two process substitutions on one shared historical reference ensemble.

**Phase U — independent replication.** Five prospectively fixed master seeds (`20291010–20291014`) were used, with 100 attempts per seed, under only two conditions: no allele-frequency mixing (`m=0`) and allele-only mixing at `m=.10`. These seeds are distinct from the historical family used below.

**Phases R and S — shared-reference operator substitutions.** Both use historical master seeds `20290410–20290414`. Their no-connectivity blocks are exactly `[[47,88],[48,89],[58,93],[46,86],[51,91]]`, and their allele-only `m=.10` blocks are exactly `[[45,88],[48,89],[66,93],[42,86],[48,91]]`. Phase R adds whole-individual post-recruitment dispersal (`d=.10`). Phase S adds paternal-gamete pollen input (`g=.20`). Thus R and S test two distinct process arms against the same historical reference observations; they are not two independent replications of the baseline contrast.

### 2.2 Test statistics and screen labels

For each condition, between-block heterogeneity was evaluated with the preregistered five-block Pearson equal-rate test. Historical `R3_highrep` and `R4_highrep` labels are deterministic classifications of the realized block-rate vectors used by that test. They are retained for protocol provenance but are not randomized treatments, independent covariates or explanatory regimes. In particular, the historical allele-only `m=.10` vector receives `R3_highrep` because that vector itself contains the detected heterogeneity; the label does not explain it.

Paired marginal-risk comparisons use exact McNemar tests on trajectories eligible under both compared conditions. Equal-rate heterogeneity and paired marginal-risk change are different estimands.

### 2.3 Precision audit

Because the prospective decisions were based on null-hypothesis tests rather than equivalence tests, we quantified the resolution of the completed designs without changing any seed, condition, endpoint, alpha or decision. For block loss rates `p_i`, block sizes `n_i`, total `N` and pooled rate `p_bar`, we use the Pearson homogeneity effect size

`w^2 = sum_i (n_i/N) (p_i-p_bar)^2 / [p_bar(1-p_bar)]`.

With five blocks (`df=4`) and alpha `.05`, the 80% and 90% power benchmarks were obtained from the noncentral chi-square distribution. Near `p_bar=.5`, `w` converts to a weighted RMS block-rate deviation as `0.5w`.

## 3. Results

### 3.1 The historical allele-mixing pattern did not replicate on fresh seeds

In the historical seed family, allele-only `m=.10` had pooled loss `0.557047` and detectable between-block heterogeneity (`equal-rate p=.020549`). That observation remains valid for that seed family.

Phase U repeated the same operator on new seeds. Fresh pooled loss was `0.539823` for `m=0` and `0.550885` for `m=.10`; equal-rate p values were `.134212` and `.745130`, respectively. Across 452 comparable paired trajectories, exact McNemar `p=.693686` detected no directional marginal-risk difference. The preregistered decision was `historical_m010_heterogeneity_not_freshly_replicated`.

This is a failed replication of a parameter-specific stochastic pattern, not evidence that heterogeneity at `m=.10` is impossible.

### 3.2 Whole-individual dispersal did not inherit the historical pattern

In Phase R, the process arm was active: mean realized mover fraction was `0.092262`, with mean `568.267` realized movement events per trajectory across 120 generations. On the shared historical reference ensemble, pooled loss was `0.559284` with no connectivity and `0.557047` under allele-only `m=.10`; the whole-individual `d=.10` arm had pooled loss `0.606264`. Equal-rate p values were `.709643`, `.020549` and `.811309`, respectively. Paired marginal-risk comparisons were unresolved (`p=.143389` versus no connectivity; `p=.131417` versus allele-only `m=.10`).

The test does not equate `d=.10` with `m=.10` as realized biological gene flow. It tests whether the stochastic interpretation attached to the allele-only scalar can simply be inherited by a different life-cycle operator. It was not inherited in this closure.

### 3.3 Pollen-only gene flow did not inherit the historical pattern

Phase S used the same historical reference blocks but substituted paternal-gamete gene flow. The external-pollen fraction `g=.20` was chosen as a mechanistically motivated nominal comparison because maternal and paternal gamete pools each contribute half of expected zygotic allele frequency; it is not a calibrated equivalence to `m=.10`.

The pollen operator was active: mean realized external-pollen fraction was `0.199850`, with mean `1266.284` external paternal contributions per trajectory. Pooled loss in the pollen arm was `0.532438`, with equal-rate `p=.728205`. Paired marginal-risk contrasts were unresolved (`p=.311231` versus no connectivity; `p=.266412` versus allele-only `m=.10`).

Because Phases R and S share their historical reference conditions, these results provide two operator substitutions against one common comparator ensemble, not two independent baseline replications.

### 3.4 The negative results are precision-bounded

The completed five-block designs have an 80% power benchmark of `w=0.163404` at `N=447` and `w=0.162498` at `N=452`. Near a pooled loss rate of `.5`, these correspond to weighted RMS block-rate deviations of approximately `8.17` and `8.12` percentage points. At 90% power the corresponding deviations are approximately `9.28` and `9.23` points.

Observed standardized heterogeneity was `w=0.06567` for fresh Phase-U `m=.10`, `0.05957` for whole-individual `d=.10`, and `0.06757` for pollen-only `g=.20`; fresh `m=0` was `0.12473`. The historical allele-only reference had `w=0.16112` and was significant in that realized sample. The power benchmark is a design-sensitivity statement, not a post-hoc significance threshold.

The supported negative conclusion is therefore bounded: the experiments had high power for between-block heterogeneity of roughly eight percentage points weighted RMS near a 0.5 loss rate, while smaller heterogeneity remains compatible with the data. No equivalence margin was preregistered, so equivalence is not claimed.

## 4. Discussion

The central result is not that connectivity has multiple meanings; that is already established. The contribution is a controlled test of whether a stochastic result attached to one connectivity operator is both replicable and portable. It was neither independently reproduced on fresh seeds nor recovered under the two tested process substitutions.

The three evidence pieces have different inferential roles. Phase U asks whether the historical allele-only pattern recurs under new stochastic realization. Phases R and S ask whether that pattern transports when the operator is changed while the historical comparator ensemble is held fixed. Treating all three as independent replications would overstate the evidence because the two substitution experiments reuse exactly the same historical reference blocks.

The result also clarifies what a scalar connectivity variable can and cannot mean in model comparison. Allele-frequency averaging, whole-individual dispersal and paternal-gamete input enter different parts of the life cycle, move different biological entities and preserve different information. Similar numerical settings therefore do not establish dynamic interchangeability. A reduction to one latent connectivity axis requires an explicit mapping that preserves the prediction target or a calibrated equivalence on the relevant transition.

The claim is intentionally finite. The analysis does not prove universal non-equivalence among connectivity processes, does not identify a universal dispersal or gene-flow scale, and does not show that smaller heterogeneity is absent. It establishes that the historical allele-only pattern cannot be treated as portable to the tested whole-individual or pollen-only closures merely because all three mechanisms are described as connectivity.

## Data and code availability

All load-bearing results are repository-locked. Phase-U, Phase-R and Phase-S summaries are stored under `artifacts/fresh_connectivity_replication/`, `artifacts/process_resolved_movement/` and `artifacts/process_resolved_pollen/`. The deterministic post-result precision audit is stored in `artifacts/operator_portability_precision/derived_summary.json` and is recomputed by `scripts/operator_portability_precision.py`. No new simulation is required to reproduce the precision boundary.
