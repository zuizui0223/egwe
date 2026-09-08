# ACTIVE DEVELOPMENT LANE — NOT YET SUBMISSION-READY

# Connectivity is an operator, not a scalar: a finite-model portability test

**Publication status:** active development, independent non-overlap candidate. This manuscript owns the process-specific portability question only. It is not an active submission while the Nature Ecology & Evolution flagship is under consideration. Development may proceed in parallel because the sole claim is intentionally separated from the flagship's state-alignment, sorting, buffering, recoupling, density-gate and last-refuge claims. Submission requires a fresh overlap audit, author approval and a live journal-policy check.

## Central question

Can one numerical “connectivity” label be transported across biologically different movement operators without first showing that the operators preserve the same target-relevant transition law?

The finite-model answer from the locked programme is **no for the tested closures**. A historical allele-frequency-mixing signal was seed-family contingent, failed one prospectively locked fresh replication, and did not appear under prospectively declared whole-individual dispersal or pollen-only gene-flow operators. The result does not establish that connectivity is unimportant. It establishes an identification boundary: a shared scalar label does not make distinct movement operators dynamically exchangeable.

## Result 1 — the historical allele-mixing signal was not independently reproducible

In the historical high-precision Phase-M seed family, allele-frequency mixing at `m=.10` produced detectable excess between-block heterogeneity (`equal-rate p=.0205`) while pooled loss remained near the same intermediate range as the no-connectivity comparator. That observation remained valid for the original seed family but was not treated as a universal biological regime.

Phase U then froze five entirely new master seeds (`20291010–20291014`), 100 attempts per seed, the same model anchor and deterioration schedule, and only two paired conditions: `m=0` and allele-only `m=.10`. Every opening gate passed. In the fresh ensemble, pooled loss was `0.5398` for `m=0` and `0.5509` for `m=.10`; equal-rate p values were `.134` and `.745`, respectively. Across 452 comparable paired trajectories, the exact McNemar test gave `p=.694`.

The preregistered decision was therefore

`historical_m010_heterogeneity_not_freshly_replicated`.

The claim is not that heterogeneity is impossible at `m=.10`. The supported boundary is that one historical seed family showed it and one independent fresh ensemble did not.

## Result 2 — whole-individual dispersal did not inherit the historical pattern

Phase R kept the historical Phase-E/M source and seed structure fixed while replacing direct post-selection allele-frequency mixing with whole-individual post-recruitment dispersal. The process-resolved operator was active: the mean realised mover fraction was `0.0923`, with a mean `568.3` realised movement events per trajectory across the 120-generation schedule.

At the historical seed family, pooled loss was `0.559` with no connectivity, `0.557` under allele-only `m=.10`, and `0.606` under whole-individual `d=.10`. Equal-rate p values were `.710`, `.0205`, and `.811`, respectively. Thus the between-block heterogeneity seen under the allele-only operator was absent under whole-individual dispersal. Paired marginal-risk comparisons were also unresolved (`p=.143` versus no connectivity; `p=.131` versus allele-only `m=.10`).

This test does **not** equate `d=.10` with `m=.10` as realised biological gene flow. It asks whether a nominally similar scalar setting can simply inherit the same stochastic interpretation across a different operator. It did not.

## Result 3 — pollen-only gene flow also did not inherit the historical pattern

Phase S replaced the legacy allele-only update with a paternal-gamete gene-flow closure. Because maternal and paternal gamete pools each contribute half of expected zygotic allele frequency, the protocol used an external-pollen fraction `g=.20` as a mechanistically motivated nominal comparison, not a calibrated equivalence to `m=.10`.

The pollen operator was active: mean realised external-pollen fraction was `0.19985`, with a mean `1266.3` external paternal contributions per trajectory. Pooled loss was `0.532`, and the equal-rate diagnostic gave `p=.728`, compared with `.0205` for historical allele-only `m=.10`. Paired marginal-risk contrasts were unresolved (`p=.311` versus no connectivity; `p=.266` versus allele-only `m=.10`).

Combined with Phase R, the historical `m=.10` block-dependence therefore did not port to either the tested demographic/trait movement representation or the tested gametic movement representation.

## Interpretation

The methodological point is narrower and cleaner than a generic statement that “connectivity effects are context dependent.” The quantity called connectivity is not a state variable until its biological operator is identified. Allele-frequency averaging, movement of whole individuals and paternal-gamete input act on different parts of the life cycle and preserve different information. Assigning them similar scalar values does not create an identification argument.

This distinction matters whenever a comparative analysis treats migration, dispersal, pollen flow, recolonisation or partner movement as exchangeable measurements of one latent axis. Such a reduction may be justified, but the justification must come from a mapping that preserves the prediction target, not from a shared label or numerical scale.

## Relationship to the active NEE flagship

This development lane is deliberately **not** a compressed version of the flagship. It excludes the state-alignment, horizon-propagation, warning-denominator, operator-balance and last-refuge evidence owned by the active flagship; the binding exclusion set is the flagship evidence registry in `publication_lanes.json`.

Its sole publication claim is operator portability / semantic identification of connectivity. The state-validity fallback still contains historical portability prose for provenance, but current claim ownership is here. If the state fallback is ever reactivated, its portability section must be removed, subordinated or explicitly reconciled so that the same claim is not submitted twice.

## Evidence sources

- `docs/FRESH_CONNECTIVITY_REPLICATION_PHASE_U.md`
- `docs/FRESH_CONNECTIVITY_REPLICATION_PHASE_U_RESULT.md`
- `artifacts/fresh_connectivity_replication/phase_u_locked_summary.json`
- `docs/PROCESS_RESOLVED_MOVEMENT_PHASE_R_RESULT.md`
- `artifacts/process_resolved_movement/phase_r_locked_summary.json`
- `docs/PROCESS_RESOLVED_POLLEN_PHASE_S_RESULT.md`
- `artifacts/process_resolved_pollen/phase_s_locked_summary.json`
- `docs/HIGH_PRECISION_CONDITION_REASSESSMENT.md`

## Claim ceiling

This finite programme does **not** prove that biological connectivity processes are universally non-equivalent, does not identify a universal dispersal or gene-flow scale, and does not rank `m`, `d` and `g` as equivalent doses. Phase U is one independent replication; Phases R and S each test one declared operator closure. The supported statement is that the historical allele-only heterogeneity signal was not independently reproduced and cannot be transported to the tested whole-individual or pollen-only closures merely because the mechanisms are all called “connectivity.”

## Development gate

Before submission, this lane requires:

1. a claim-overlap audit against the then-current flagship and any reactivated fallback;
2. a literature/nearest-neighbour audit focused on operator identification and transportability rather than generic fragmentation effects;
3. a journal-fit and article-type check;
4. an independent cover letter, reference set, display plan and submission bundle;
5. author approval of whether a negative finite-model portability note is worth a standalone submission.
