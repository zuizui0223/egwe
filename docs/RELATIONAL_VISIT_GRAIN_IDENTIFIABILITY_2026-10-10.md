# What a site-wide visit total cannot identify: sharp local association bounds

**Date:** 2026-10-10. **Status:** exact measurement-identifiability result and *synthetic* illustration only. No natural effect estimated and no new NEE model/selection/trajectory run.

## Immediate empirical motivation

The publicly accessible `Ulex parviflorus` Zenodo archive was read at header-only level in EGWE PR #219 (merged as `159acc901d2694cfa24efea48e9c30e69ad8e625`). Its genotype/flower/fruit records expose **`ind`**; its `pollinator.census.csv` exposes **`year,locality,flowers,tot.visits,Apis,Bombus,other,visits.flower,observations`**, with **no plant ID**. The future H-R hypothesis requires within-locality/patch **co-location** of effective interaction and genotype/trait support. Attaching one locality visit rate to every sampled genotype yields a number, but not a measured joint ecological state.

The following bound quantifies the information destroyed by this missing key. It is a simple linear-programming consequence, **not** a new evolutionary theorem and not an estimate of the Ulex association.

## Exact, sharp bounds when patch-level visit assignments are unknown

Assume a hypothetical fully enumerated set of **n** focal plants/patches in one site and observation window. Pre-outcome state `g_i` and positive exposure/effort `e_i` are observed. Each plant's visitation **count** `v_i >= 0` is *not* labelled, but a common-site total `V = sum(v_i)` is available. If justified from the recording design, a maximum possible count `u_i` may constrain each plant. Equal-weighted population covariance between the latent local visit **rate** and state is

\[
C(I,G)=\frac{1}{n}\sum_{i=1}^n \frac{v_i}{e_i}\left(g_i-\bar g\right),\quad
\bar g=\frac1n\sum_i g_i.
\]

The feasible set is `v_i >= 0`, `sum(v_i)=V`, with optional `v_i <= u_i`. This is a linear objective on a simplex or capped simplex. Define `c_i = (g_i - mean(g))/(n e_i)`. Exact minima and maxima allocate remaining visits greedily to the **smallest** or **largest** coefficient `c_i`, respecting caps. An exchange argument establishes sharpness: if the supposedly minimal allocation assigns visits to a higher-`c` unit while a lower-`c` unit has spare capacity, transferring a positive amount cannot increase feasibility cost and strictly decreases the objective.

With **equal exposures** and no caps, the sharp bounds simplify to

\[
\frac V n(\min_i g_i-\bar g)\ \leq\ C(I,G)\ \leq\
\frac V n(\max_i g_i-\bar g).
\]

No confidence interval, posterior or regression outcome enters this result. It describes **all assignments consistent with the aggregated measurement**. If the allowed interval spans zero, even the sign of the spatial covariance is not identified.

### Frozen synthetic example

This is **not** sourced from Ulex or any observed genotype dataset.

- Four equal-effort local units, \(G=(0.1,0.3,0.7,0.9)\), total visit count **20**, no unit above **8** visits.
- **Anti-aligned allocation:** \(v=(8,8,4,0)\), yielding \(C=-1\).
- **Aligned allocation:** \(v=(0,4,8,8)\), yielding \(C=+1\).
- **Unjustified allocation by the site mean:** \(v=(5,5,5,5)\), yielding \(C=0\).

All three preserve the **identical genetic marginals, total visits, observation units and exposure**. The exact sharp feasible interval is **[-1,+1]** (without the declared caps, **[-2,+2]**). Thus a zero covariance obtained by assigning the site mean equally is not a measurement of absent spatial association; it is the deterministic effect of imposing the same rate on every plant.

The implementation `scripts/visit_allocation_identifiability.py` reports both extremal witness allocations and the naive imputation. `tests/test_visit_allocation_identifiability.py` enumerates **all** feasible integer allocations in multiple small examples (including unequal exposures), verifies the sharp bounds and retains Ulex's no-individual-visit STOP.

## Crucial applicability condition

A study-wide census total is a valid `sum(v_i)` constraint **only if every counted visit can be assigned among exactly the genotyped/tagged focal units** with the same observation window. In Ulex, censuses sampled observation patches, while genetic/fruit files sampled named plants. This membership identity and exposure denominator are **not established**. Therefore **do not plug the reported Ulex total visits into the bound as if they came from its 225 genotyped plants**. The bound is a prospective measurement design tool, not a back-door reanalysis of an invalid join.

If plant-level genetic scores are also absent, the source is even less identifiable; one cannot supply the individual \(g_i\) vector to the bound.

## The smallest field measurement that removes this particular ambiguity

Tag the same plants/patches *before outcome observation*, and record:

1. `site_id, patch_id, plant_id, genotype_sample_id, cohort, pre_state_time, trait_measure` in a unique **pre-outcome state** table; distinguish molecular markers from a treatment label.
2. `site_id, patch_id, plant_id, observation_start, observation_end, effort_seconds, pollinator_guild, direct_visit_count, detection_method` in a **visit exposure** table, including true zero-visit observation intervals. Camera detections need validation to avoid treating classifier sensitivity as encounter rate.
3. `site_id, patch_id, plant_id, outcome_start, outcome_end, initial_flower_count, mature_seed_count` (or independently verified next-year recruitment) in a **later function** table. Mature seed after visits is a valid forward seasonal function; it does *not* equal a multiyear disappearance/early-warning event.
4. `site_id, patch_id, maternal_id, offspring_cohort, paternal_id/posterior` if specific pollen/parentage connectivity is to be claimed; these genetic cohorts must not be substituted for each other.
5. `site_id, patch_id, origin/history/forcing and true spatial coordinates` fixed without outcome-driven selection, so matched marginals can be separated from upstream history.

**Identity gate:** the marked focal-plant census denominator must match genotype/trait sampling (or its probabilistic detection and missingness process must be explicitly modeled). An observation patch with no `plant_id` is not repaired by spreading total visitation across `ind` values.

**Independent holdout gate:** sites or independently replicated landscapes/time cohorts are the validation units, not camera frames, visits, flowers, SNP columns or sibling offspring. Do not invent an exact minimum sample size or declare power from this mathematical example. Empirical design/power would need independent-site heterogeneity and visitor event-rate pilots measured prospectively.

**Prospective comparisons (only after source and time gates):** M0 = marginal interaction/trait/genetic/demographic/effort state; M1 = M0 + *pre-outcome measured* spatial alignment; M2 = M1 + independently measured mating, dispersal or recruitment operator. The current finite simulator's coefficients, threshold and AUC do not transfer to this natural test. Freeze the actual score, endpoint, time split and holdout groups before inspecting biological outcome rows.

## Exact output and interpretation

`python scripts/visit_allocation_identifiability.py --output artifacts/design/synthetic_visit_allocation_bounds.json` creates a deterministic **synthetic** receipt; no internet, biological data or external Python packages are used.

The result is **measurement non-identifiability** when `C_min < 0 < C_max`, not evidence that the biological interaction has zero effect, not H-R failure, and not a real-world negative covariance estimate. If future actual plant-tagged visits are obtained, the role of this bound is to be replaced by an observed same-unit estimate with measurement uncertainty and preregistered later function.

The active NEE paper, its fixed numerical evidence and previous no-incremental-information natural transfer remain unchanged.
