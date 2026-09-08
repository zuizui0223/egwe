# ACTIVE DEVELOPMENT LANE — NOT YET SUBMISSION-READY

# Connectivity is an operator, not a scalar: a finite-model portability test

**Publication status:** active development, independent non-overlap candidate. **Provisional target:** *Ecological Modelling*, Short Communication. This manuscript owns the process-specific portability question only. It is not an active submission while the Nature Ecology & Evolution flagship is under consideration. Development may proceed in parallel because the claim is intentionally separated from the flagship's state-alignment, sorting, buffering, recoupling, density-gate and last-refuge claims. Submission still requires a fresh overlap audit, author approval and a live journal-policy check.

## Central question

Can one numerical “connectivity” label be transported across biologically different movement operators without first showing that the operators preserve the same target-relevant transition law?

The finite-model answer is **no for the tested closures**. A historical allele-frequency-mixing pattern failed one prospectively locked replication on new master seeds and did not appear when the historical reference ensemble was subjected to two different movement operators. This does not show that connectivity is unimportant, or that all connectivity processes are non-equivalent. It identifies a narrower modelling boundary: a scalar label does not by itself make distinct biological operators dynamically exchangeable.

## Position relative to existing connectivity literature

The semantic problem is not new. Landscape connectivity has long been separated into structural and functional meanings, genetic connectivity has been distinguished from demographic connectivity, and recent frameworks explicitly separate movement, dispersal and gene flow across ecological and generational timescales (Tischendorf & Fahrig 2000; Lowe & Allendorf 2010; Cramer et al. 2023; Liczner et al. 2024). The novelty here is therefore **not** the claim that “connectivity means different things.”

The finite-model contribution is a controlled portability audit. A stochastic pattern originally attached to one allele-frequency-mixing parameter is tested in two ways: first by repeating that same operator on a new seed ensemble, and second by replacing the operator while holding the historical reference ensemble fixed. This separates **replicability of a parameter-specific pattern** from **transportability of that pattern across biological operators**.

## Evidence structure and statistical design

The evidence consists of **one independent fresh replication plus two process substitutions on a shared historical reference ensemble**.

**Independent replication — Phase U.** Five new master seeds (`20291010–20291014`) were fixed prospectively, with 100 attempts per seed, and only `m=0` versus allele-only `m=.10` were compared. These seeds are independent of the historical Phase-M/R/S family.

**Shared-reference operator substitutions — Phases R and S.** Both experiments reused historical master seeds `20290410–20290414`. Their `no_connectivity` blocks are exactly `[[47,88],[48,89],[58,93],[46,86],[51,91]]`, and their `allele_only_m010` blocks are exactly `[[45,88],[48,89],[66,93],[42,86],[48,91]]`. Phase R adds whole-individual post-recruitment dispersal; Phase S adds paternal-gamete pollen input. The R and S process arms are distinct closures, but the two historical reference conditions are the **same observations** and are counted once conceptually. R and S are therefore not two independent replications of the baseline contrast.

For each condition, between-block heterogeneity was evaluated with the preregistered five-block Pearson equal-rate test. The historical `R3_highrep` and `R4_highrep` labels are deterministic classifications of the same realised block-rate vectors used by that test. They are outcome summaries retained for protocol provenance, **not randomized conditions, covariates or explanatory regimes**. In particular, the historical allele-only `m=.10` vector is labelled `R3_highrep` because that vector itself contains the detected heterogeneity; the label is not an independent cause of it.

Paired marginal-risk comparisons use exact McNemar tests on trajectories eligible under both compared conditions. Equal-rate heterogeneity and paired marginal-risk change are separate estimands.

## Evidence block A — the historical allele-mixing pattern was not independently reproducible

In the historical high-precision Phase-M seed family, allele-frequency mixing at `m=.10` produced detectable excess between-block heterogeneity (`equal-rate p=.020549`) while pooled loss remained close to the no-connectivity comparator. That observation remains valid for its original seed family.

Phase U then repeated only `m=0` and allele-only `m=.10` on the five new master seeds. Every opening gate passed. Fresh pooled loss was `0.539823` for `m=0` and `0.550885` for `m=.10`; equal-rate p values were `.134212` and `.745130`, respectively. Across 452 comparable paired trajectories, exact McNemar `p=.693686` showed no detected directional marginal-risk difference.

The preregistered decision was therefore

`historical_m010_heterogeneity_not_freshly_replicated`.

This is a failed replication of a **parameter-specific stochastic pattern**, not evidence that heterogeneity at `m=.10` is impossible.

## Evidence block B — two operator substitutions on one shared reference ensemble

### Whole-individual dispersal

Phase R replaced direct post-selection allele-frequency mixing with whole-individual post-recruitment dispersal while preserving the historical source/seed reference structure. The operator was active: mean realised mover fraction was `0.092262`, with mean `568.267` realised movement events per trajectory across 120 generations.

On the shared historical reference ensemble, pooled loss was `0.559284` with no connectivity and `0.557047` under allele-only `m=.10`; the whole-individual `d=.10` arm had pooled loss `0.606264`. Equal-rate p values were `.709643`, `.020549` and `.811309`, respectively. Paired marginal-risk comparisons were unresolved (`p=.143389` versus no connectivity; `p=.131417` versus allele-only `m=.10`).

This test does **not** claim that `d=.10` and `m=.10` represent equivalent realised gene flow. It tests whether the historical stochastic interpretation attached to `m=.10` can simply be inherited by a different life-cycle operator at a nominally similar scalar value. It cannot in this closure.

### Pollen-only paternal gene flow

Phase S used the same historical no-connectivity and allele-only reference blocks, but substituted a paternal-gamete gene-flow operator. Because maternal and paternal gamete pools each contribute half of expected zygotic allele frequency, the protocol used external-pollen fraction `g=.20` as a mechanistically motivated nominal comparison; this is not a calibrated equivalence to `m=.10`.

The pollen operator was active: mean realised external-pollen fraction was `0.199850`, with mean `1266.284` external paternal contributions per trajectory. Pooled loss in the pollen arm was `0.532438`, with equal-rate `p=.728205`. Paired marginal-risk contrasts were unresolved (`p=.311231` versus no connectivity; `p=.266412` versus allele-only `m=.10`).

Thus the historical block-dependence attached to the allele-only operator did not appear under either tested process substitution. Because R and S share their historical reference conditions, this is evidence from **two substituted operators against one common comparator ensemble**, not two independent baseline replications.

## Precision boundary of the negative results

Non-significance is not equivalence. We therefore characterized the resolution of the already completed equal-rate tests without opening new simulations or changing the preregistered decisions.

For block counts `n_i`, block loss rates `p_i`, total `N` and pooled rate `p_bar`, define the Pearson homogeneity effect size

`w^2 = sum_i (n_i/N) (p_i-p_bar)^2 / [p_bar(1-p_bar)]`.

With five blocks (`df=4`) and alpha `.05`, an asymptotic noncentral-chi-square calculation gives an 80%-power benchmark of `w=0.163404` for the `N=447` R/S design and `w=0.162498` for the `N=452` Phase-U design. Near a pooled loss rate of `.5`, these correspond to weighted RMS block-rate deviations of approximately **8.17** and **8.12 percentage points**, respectively. At 90% power the corresponding RMS deviations are about **9.28** and **9.23 points**.

Observed standardized heterogeneity was `w=0.06567` for fresh Phase-U `m=.10`, `0.05957` for whole-individual `d=.10`, and `0.06757` for pollen-only `g=.20`; fresh `m=0` was `0.12473`. The historical allele-only reference had `w=0.16112` and was significant in that realized sample. The power benchmark is therefore not a significance threshold; it describes design sensitivity.

The defensible negative statement is consequently **precision-bounded**: these experiments had high power for block heterogeneity on the order of roughly eight percentage points weighted RMS near a 0.5 loss rate, but smaller heterogeneity remains compatible with the data. No equivalence margin was preregistered, so no equivalence claim is made. Full derivation and values are recorded in `docs/OPERATOR_PORTABILITY_PRECISION_AUDIT_2026-09-09.md`.

## Interpretation

The methodological point is narrower than “connectivity effects are context dependent.” A quantity called connectivity does not become a transportable state variable merely because different mechanisms can be assigned similar numbers. Allele-frequency averaging, whole-individual dispersal and paternal-gamete input enter different locations in the life cycle, move different biological entities and preserve different information.

This matters whenever comparative analyses combine migration, dispersal, pollen flow, recolonisation or partner movement into one latent connectivity axis. Such a reduction may be scientifically useful, but it requires an identification argument: the mapping between processes must preserve the prediction target or establish calibrated equivalence on the relevant transition. Shared terminology or nominal scale is not sufficient.

The three evidence pieces play different roles. Phase U asks whether the historical allele-only pattern replicates under new stochastic realization. Phases R and S ask whether that pattern transports when the operator is changed while the historical comparator ensemble is held fixed. The first failed; the latter two also failed at the tested closures. Together they support an operator-identification boundary without pretending that the three experiments are independent repetitions of one test.

## Relationship to the active NEE flagship

This development lane is deliberately **not** a compressed version of the flagship. It excludes the state-alignment, horizon-propagation, warning-denominator, operator-balance and last-refuge evidence owned by the active flagship; the binding exclusion set is the flagship evidence registry in `publication_lanes.json`.

Its sole publication claim is operator portability / semantic identification of connectivity. The state-validity fallback still contains historical portability prose for provenance, but current claim ownership is here. If the state fallback is ever reactivated, its portability section must be removed, subordinated or explicitly reconciled so that the same claim is not submitted twice.

## Development target

The provisional outlet is ***Ecological Modelling* — Short Communication**. That format matches the current size and the modelling-specific claim better than expanding the note into a full methods paper. *Methods in Ecology and Evolution* is not the primary target because this work does not introduce a broadly applicable new method or software tool; its contribution is a finite-model identification/portability result.

The exact live author instructions must still be rechecked at submission. The manuscript should remain concise rather than being padded to full-article length. Additional words are justified only where they sharpen statistical precision, operator definitions, literature positioning or reproducibility.

## Evidence sources

- `docs/FRESH_CONNECTIVITY_REPLICATION_PHASE_U.md`
- `docs/FRESH_CONNECTIVITY_REPLICATION_PHASE_U_RESULT.md`
- `artifacts/fresh_connectivity_replication/phase_u_locked_summary.json`
- `docs/PROCESS_RESOLVED_MOVEMENT_PHASE_R_RESULT.md`
- `artifacts/process_resolved_movement/phase_r_locked_summary.json`
- `docs/PROCESS_RESOLVED_POLLEN_PHASE_S_RESULT.md`
- `artifacts/process_resolved_pollen/phase_s_locked_summary.json`
- `docs/HIGH_PRECISION_CONDITION_REASSESSMENT.md`
- `docs/OPERATOR_PORTABILITY_PRECISION_AUDIT_2026-09-09.md`
- `manuscript/operator_portability_references.md`

## Claim ceiling

This finite programme does **not** prove that biological connectivity processes are universally non-equivalent, does not identify a universal dispersal or gene-flow scale, does not rank `m`, `d` and `g` as equivalent doses, and does not establish that heterogeneity smaller than the present precision boundary is absent. Phase U is one independent replication. Phases R and S each test one declared process arm but share the same historical no-connectivity and allele-only reference blocks. The supported statement is that the historical allele-only heterogeneity signal was not independently reproduced and cannot be transported to the tested whole-individual or pollen-only closures merely because the mechanisms are all called “connectivity.”

## Development gate

Before submission, this lane still requires:

1. a fresh claim-overlap audit against the then-current flagship and any reactivated fallback;
2. final reference checking and nearest-neighbour positioning at the target journal;
3. a live *Ecological Modelling* Short Communication policy/format check;
4. an independent cover letter, display plan and submission bundle;
5. author approval of whether the bounded negative portability result warrants standalone submission.
