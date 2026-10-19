# From latent genetic capacity to transient expression and repeated occupancy

**Date: 2026-10-19. Status: frozen exploratory full-source simulation design, BEFORE looking at these new seed outcomes.** No human field measurements, anthocyanin genetics, or actual functional pollination endpoints.

## Why another experiment?

EGWE PRs #230–231 established that high-trait abundance can recover from global zero when its model allele is retained and two-kernel recruitment remains active; zero trait **and** zero allele are jointly absorbing without mutation/import. Crucially, a high-trait individual can be recruited even where the source's potential high-trait fitness is below its viability threshold. This leaves a biologically important gap:

> Does a **chance to express a trait** imply **repeated occupancy**, and does an initially favorable interaction environment keep favoring it once the expressed trait itself is absent?

The previous 128-seed AA/RR results do not demonstrate uniform alignment superiority. We do not vary alignment here, re-use past favorable seeds, or retrofit a future-loss endpoint to select a positive result.

## Frozen source and design

- Exact EGC `zuizui0223/egc@dd8ee379d0d3518194c767d16402042525bc00dc` via existing source-pinned `simulate_with_symmetric_allele_mutation`.
- **One tagged model patch**, initial population N0=20, density capacity K=40, **zero initial high-trait individuals**, high trait represented by the z=1 model bin (low z=0 has all starting trait mass).
- **Two initial ecological states**: q0 = **0.20** and **0.80**, straddling the source potential high-trait fitness threshold q*=0.625.
- **Two initial latent allele reservoirs**: p0 = **0.04** and **0.40**. Neither p is molecular regulatory capacity measured in a plant; each is a simulated high allele frequency.
- Four declared cells: (q0,p0) in `{(.2,.04),(.2,.4),(.8,.04),(.8,.4)}`.
- **256 new seeds** 50001–50256, **12 generations** for each cell. No overlapping seed from prior studies.
- Exact unchanged previously used q feedback (4.5, alpha=.6, beta_trait=.3, gamma_allele=.1), barrier=.5025, inheritance weight=.5, two-kernel recruitment, finite trait-bin occupancy, allele mutation=0, allele migration=0 in this one-patch scenario.
- The entire original stochastic update is executed: finite-bin recruit draws, finite high-allele drift, q/trait/genetic feedback and population dynamics. No independent reimplementation of EGC.

### Four distinct outcome concepts

1. **Next-generation expression:** model high-investment trait is present at generation 1 despite its absence at generation 0.
2. **Two- and three-consecutive-snapshot presence:** high trait is present at generations 1–2 and 1–3 respectively. These are narrowly defined *short-term occupancy retention* statistics, **not evolutionary establishment**.
3. **Twelve-generation endpoint occupancy:** high trait is present at generation 12 regardless of intermediate losses/returns.
4. **Loss of genetic potential:** the joint state **no high trait + no high allele** is reached (an absorbing class because mutation/import are both zero). This tracks closing of the *model-defined recoverability window* rather than extinction of the plant population.

In addition, report high-trait expression at least once, expressed snapshot count, and snapshots with **latent high allele present but high phenotype absent**. These distinguish an expression episode from the retained genetic source state.

### Exact one-step calibration

For **any** current resident trait distribution (not only an all-low distribution), compute the exact source-conditional probability of next-generation high-trait occupancy:

\[
P(H_{t+1}>0\mid X_t,N_{t+1})
=1-\prod_j [1-s_j(X_t)]^{N_{j,t+1}},
\]

where \(s_j\) is the source-weighted probability of a high-bin recruit under pinned `recruit_trait_distribution`, `trait_fitness` and `trait_grid`. No biological responses are fitted or used to choose weights. The test verifies its prediction against repeated independent draws from the **actual source** `update_trait_abundance`.

This source-conditional probability is computed from full known model state and computed next N; it is not a natural predictive estimator or guarantee that a high trait survives subsequent generations.

### Important source-specific feedback complication

At q0=.8, the source high-trait endpoint fitness \(W(1;q_0)=1.14>1\); at q0=.2 it is \(W(1;q_0)=.66<1\). However, **the trait is absent at t=0 in all cells**. The subsequent interaction update depends on q0, latent p0, current high-trait mass=0, density=20/40, and the barrier. Hence the initial high-q condition need **not** remain above q*=.625 once selection/recruitment begins. The script outputs **q1 and q2**, rather than silently treating q0 as a clamped constant environmental regime.

An observed difference between q0 cells is therefore the difference between entire subsequent feedback trajectories initiated by different interactions, not simply an isolated per-capita fitness manipulation.

### Stops and inference ceiling

The experiment is source-internal, exploratory and **not an independent confirmation** of a universal "recoverability window closes after X generations" law. The binomial finite genetic drift may remove the high allele and close the capacity window; the source model may also allow transient expression without effective biological pollination.

No prospective ecological-function outcome, empirical seed set, pollinator visit, anthocyanin locus, regulatory reactivation or geographic urban/island contrast is observed. Do not label any high-trait snapshot alone as plant-pollinator functional restoration or evolutionary establishment. No frozen NEE numerical result, source manifest or natural negative transfer is modified.

A valuable scientific outcome **even if no strong q0 association is observed** is to quantify how often the source passes through these distinguishable states and whether an initially favorable q0 can cease to be favorable before the expressed trait has persisted.

## Reproduce

The standard-library runner `scripts/egc_reexpression_establishment_gate.py` must import the pinned source and requires `EGC_PINNED_ROOT` with matching commit. It emits the exact four-cell, per-seed receipt and concise human-checkable summary; dedicated tests cover absence/allele state classification and the source multinomial formula. GitHub Actions stores the unrounded case-level receipt separately from a future summary ledger.

This extension complements, rather than supersedes, the prior [full recruitment recovery result](EGC_TRAIT_REAPPEARANCE_RECRUITMENT_2026-10-19.md) and [joint gene–trait absorption theorem](EGC_JOINT_TRAIT_GENE_ABSORPTION_2026-10-19.md).
