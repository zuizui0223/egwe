# A latent allele pool makes model trait loss reversible — pinned EGC recruitment mechanism

**19 October 2026 — prospectively fixed, model-internal mechanistic audit.** This extension is a test of the exact `zuizui0223/egc@dd8ee379d0d3518194c767d16402042525bc00dc` life cycle, **not** a result for anthocyanin reactivation, natural pollination, genomic regrowth or true ecological extinction. It does not amend the frozen NEE flagship or its natural null.

## Why this matters after the fresh 128-seed AA/RR null

PR #229 used **128 fresh seeds**, not the motivating four-seed pilot, and found no robust large benefit from aligned (AA) versus reversed (RR) initial spatial state. At 24 generations, *ever* having zero high-trait occupancy was 100/128 for AA and 104/128 for RR, while **the high trait was still present at the final snapshot in 45/128 and 42/128**. These endpoints ask different questions. Neither means adult population extinction (the parent model floors population size at 1), and a temporary absence may be followed by reappearance. The question is not to search for an AA-favouring threshold: **which life-cycle rule determines whether zero realised high-trait abundance is an absorbing or recoverable state?**

## Exact source contract

The pinned `causal_model/multipatch_criticality_dynamics.py` defines the finite high-trait-bin abundance `a_{j,z,t}` over trait-grid values z. In the finite `update_trait_abundance()` mode, recruitment first creates a source distribution, weights it by the positive, floor-bounded `trait_fitness(z,q_{j,t})`, normalizes and samples a multinomial count with **next local population N_{j,t+1}**. It specifically uses **resident `q_{j,t}` and resident `p_{j,t}`**, not selected/migrated/mutated allele `p_{j,t+1}` or interaction `q_{j,t+1}`.

Let `H = {z >= high_trait_cutoff}`. Consider a snapshot at time t with **no** high-bin individuals in any patch (all `a_{j,z,t}=0` for z in H). Resident distributions are then supported only on low bins.

### A. Resident-trait-only recruitment makes this zero set absorbing

If `genotype_trait_recruitment='resident_trait_only'`, the recruit distribution is exactly the resident distribution. Since weighting by finite positive fitness cannot create positive mass in bins that had zero mass, every next high bin has probability 0. A multinomial draw with probability 0 produces no high trait individuals, for every seed and every future generation.

Thus, under this explicitly restricted closure **without direct trait mutation or between-bin introduction**, global zero realised high-trait abundance is an *absorbing trait state*. This does **not** mean demographic extinction; other low-investment trait bins can persist. It does **not** mean all genes are lost.

### B. Two-kernel allele-linked recruitment can restore the trait

With `genotype_trait_recruitment='two_kernel_recruitment'` and inheritance weight h, the recruit distribution in patch j is

\[
R_j(z)=h\,D_j(z)+(1-h)\big[(1-p_{j,t})K_L(z)+p_{j,t}K_H(z)\big].
\]

The pinned kernels `K_L` and `K_H` have disjoint support below/above the high-trait cutoff. If the resident high trait is entirely absent, then the *pre-selection* high trait mass is exactly `(1-h) p_{j,t}`.

Let `w_j(z)=max(trait_selection_floor, trait_fitness(z,q_{j,t}))`, and define the post-selection probability that a **single recruited plant** is high:

\[
s_{j,t}=\frac{\sum_{z\in H}w_j(z)R_j(z)}
{\sum_z w_j(z)R_j(z)}.
\]

Under the pinned finite-recruitment model with high trait occupancy declared when **at least one high-bin recruit exists** (threshold 1), independent conditional multinomial draws across patches yield the exact probability of reappearance **in at least one patch** at t+1:

\[
\boxed{
\Pr(\exists j:\ a_{j,H,t+1}>0\mid X_t,N_{t+1})
=1-\prod_j (1-s_{j,t})^{N_{j,t+1}}.
}
\]

This is an **exact conditional probability for the specified code**, not an estimated ecological parameter. It requires the resident state and next population sizes. It does not assume that different observed generations or seed runs are independent.

If at least one patch has `p_{j,t}>0`, `h<1`, `N_{j,t+1}>=1`, and the high trait kernel remains supported, this probability is **strictly positive**, even though there were zero visible high-trait individuals at time t. But positivity is not certainty: at finite N, re-expression can fail by multinomial sampling.

If all resident p values are zero, or if `h=1`, and resident high trait is zero, next-generation high trait reappearance probability is zero. The source's allele mutation can later create p>0, but does not directly add high trait recruits at the **same** step.

### C. The one-generation genetic-to-phenotype lag

The pinned order is:

1. `q[t+1]` from the current interaction, trait mass, adult allele state and density;
2. selected p using `q[t+1]`, followed by **population-weighted allele-frequency migration, allele mutation and finite drift** to create `p[t+1]`;
3. simultaneously the finite trait-bin recruit update uses the **old** resident p[t] and q[t], and the newly computed N[t+1].

Consequently, if `p[t]=0` and no high trait individuals remain, reappearance at t+1 is impossible even if recurrent mutation makes `p[t+1]>0`. If the latter is positive, then *at t+2* a positive re-expression probability becomes possible. This is a **timing prediction specific to the source life cycle**, not a statement that an anthocyanin molecular pathway is epigenetically reactivated.

## Predeclared model experiment (before outcome inspection)

The new `scripts/egc_high_trait_reappearance.py` uses fresh seeds **30001–30128**, **24 generations**, and exactly the four matched-marginal AA/RR initial conditions and parameter values of PR #229, except for a single, explicitly declared recruitment-mode contrast:

- **Allele-seeded, potentially reversible:** `two_kernel_recruitment`, `inheritance_weight=0.5`;
- **Resident-only, structurally absorbing after zero:** `resident_trait_only`, same resident q/p initial conditions.

The primary descriptive purpose is to count **first global zero**, **at least one 0→1 trait return after a zero episode**, and **present at the final snapshot** separately. We also record how many immediate return opportunities existed, the sum of exact conditional reappearance probabilities at those opportunities, and their actual 0→1 realization. These are model-internal diagnostics and the p-value family is intentionally **not** opened for this mechanistic source-identity test.

**Not permitted:** choosing another seed family, event definition, horizon, or variant after viewing the outcome to recover AA superiority; comparing the two recruitment modes as if the intervention targeted only one naturally measured gene; pooling these new runs into the flagship NEE confirmatory effect, or calling high-trait absence population extinction.

## Sources and reproducibility

- [Pinned EGC stochastic life cycle at the exact commit](https://github.com/zuizui0223/egc/blob/dd8ee379d0d3518194c767d16402042525bc00dc/causal_model/symmetric_allele_mutation_closure.py)
- [Pinned finite trait-bin recruiter](https://github.com/zuizui0223/egc/blob/dd8ee379d0d3518194c767d16402042525bc00dc/causal_model/multipatch_criticality_dynamics.py)
- [Previous exploratory pilot and recovery boundary](../docs/PINNED_EGC_AA_RR_FULL_LIFECYCLE_2026-10-18.md)
- [Previous 128-seed AA/RR nonsupport audit](../docs/EGC_AA_RR_PAIRED_ROBUSTNESS_2026-10-19.md)

Execute only with an exact pinned checkout in `EGC_PINNED_ROOT`. A small source-integrated test checks source-multinomial outcomes against the analytical one-step probability and confirms the one-generation lag. No standalone generic CI is authorized to silently reconstruct the parent package.

**Interpretation:** this closure provides an explicit mechanistic separation between **observable loss of a trait** and **loss of the capacity to recreate it**. Whether natural flowers can recover anthocyanin production or regain effective pollination is an independent evolutionary/genetic/field question that this simulator cannot establish.
