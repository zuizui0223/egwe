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

## Derived after the first simulation receipt: exact *trait-absent ecological support* gate

This paragraph is an **analytic interpretation added after inspection of the exploratory four-cell output**, not a predeclared simulation hypothesis or an independently discovered mathematical theorem. It specializes the already documented source-exact route-margin identity.

The pinned interaction operator with q memory, trait and resident high allele is

\[
q_{t+1}=\sigma\!\left(\kappa\left[
d_t\left(\alpha q_t+\beta T_t+\gamma p_t\right)-\theta
\right]\right),
\quad
(\alpha,\beta,\gamma)=(0.6,0.3,0.1),
\quad \kappa=4.5.
\]

For the high-allele relative-fitness and endpoint z=1 viability switch \(q^*=0.625\), let \(H=\theta+\operatorname{logit}(0.625)/\kappa=0.6160168053\) at theta=0.5025. **If the currently expressed high trait is absent**, \(T_t=0\), so

\[
q_{t+1}\ge0.625\quad\Longleftrightarrow\quad
d_t(0.6q_t+0.1p_t)\ge0.6160168053.
\]

Since \(q_t,p_t\le1\), even the best possible trait-absent source has support at most \(d_t(0.6+0.1)\). Consequently:

- At density \(d_t=0.5\) (the experiment's initial \(N_0=20,K=40\)), the absolute maximum support is **0.35**, too low to reach 0.61602, *regardless of what q or p is*. The maximum attainable next interaction is only **about 0.335**.
- A **necessary condition** for a trait-absent state to recover q at or above the source allele/endpoint switch, even with q=p=1, is **\(d_t\ge 0.8800240\)**. It is not sufficient unless the actual q and p also provide enough support.
- At full density and maximal q=1, the allele must be at least **\(p_t\ge0.1601681\)** to make the threshold feasible. Therefore initial p=0.04 cannot achieve this q switch even with full density and maximal interaction when T=0.
- At full density and p=0.4, current q must be at least **0.9600280**. The experiment's q=0.8 is insufficient even at density 1.

This is a **conditional next-step feedback gate**, not a universal threshold of long-term high-trait persistence or seed production. The value 0.625 governs the source fitness of high-endpoint z=1 and deterministic high-allele sorting, **not the full high-bin potential-viability topology at every z≥0.7**.

The original full-source experiment made the distinction visible: although q0=.8 gave initially favorable \(W(1;q_0)=1.14\), q at generation 1 was only about **0.236–0.251** depending on p0; the q=.2 cells had q1 about **0.121–0.130**. The high-q arm therefore lost much of its interaction support **before any 12-generation retention comparison**.

`scripts/egc_latent_ecological_support_gate.py` and source-verified tests codify the exact inequality and its impossibility regimes. Its use is to identify why **positive trait expression probability does not automatically constitute restoration of ecological support** in this particular feedback/density setting; the algebra does not license claims about natural pollinator network collapse.


## Executed source-pinned result: 256 seeds per cell, 12 generations

GitHub Actions run [39207813721](https://github.com/zuizui0223/egwe/actions/runs/39207813721) passed **source pin verification, actual source multinomial checks, all four-cell 1,024-trajectory simulation checks, exact trait-absent support gate and seed-group bootstrap integrity tests**. [Artifact 12166353115](https://github.com/zuizui0223/egwe/actions/runs/39207813721/artifacts/12166353115) contains the case-level complete receipt, the exact feedback-gate receipt and the compact descriptive uncertainty table. Permanent text summary with hashes is `artifacts/egc_trait_reappearance/establishment_window_4cell_256seed_20261019_summary.json`.

| Starting `q0 / p0` | High trait expressed at generation 1 | Occupied at generations 1, 2 and 3 | Occupied at generation 12 | Ever joint trait+allele zero |
| --- | ---: | ---: | ---: | ---: |
| **0.20 / 0.04** | 63/256 (24.6%) | 9/256 (3.5%) | 7/256 (2.7%) | 247/256 (96.5%) |
| **0.80 / 0.04** | 86/256 (33.6%) | 10/256 (3.9%) | 4/256 (1.6%) | 251/256 (98.0%) |
| **0.20 / 0.40** | 233/256 (91.0%) | 197/256 (77.0%) | 74/256 (28.9%) | 163/256 (63.7%) |
| **0.80 / 0.40** | 250/256 (97.7%) | 229/256 (89.5%) | 78/256 (30.5%) | 164/256 (64.1%) |

### Descriptive contrasts; not confirmatory tests

For **generation-12 high-trait occupancy**, a same-seed-group 4096-replicate *exploratory* bootstrap gave:

- Raising **latent allele p0 from 0.04 to 0.40** at q0=0.20: **+26.17 percentage points**, descriptive 95% interval **+20.31 to +32.42 pp**.
- Same p contrast at q0=0.80: **+28.91 pp**, descriptive interval **+23.05 to +34.77 pp**.
- Raising **initial q0 from 0.20 to 0.80** with p0=0.04: **−1.17 pp**, descriptive interval **−2.73 to +0.39 pp**.
- Same q contrast with p0=0.40: **+1.56 pp**, descriptive interval **−4.69 to +8.20 pp**.

The 4-cell parameter grid is fixed, but these cross-cell contrasts and bootstrap intervals were calculated **after outcome inspection**. They are descriptive synthetic Monte Carlo uncertainty, not an independently preregistered hypothesis test or a natural ecological treatment effect. Shared seed numbers do not establish perfectly matched random draws between divergent source trajectories; seed IDs, not time steps or individual recruitment events, were bootstrapped.

### How the ecological state changed after removing the expressed trait

The mean q at generation 1 was:

- q0=0.20, p0=0.04/0.40: **0.121 / 0.130**;
- q0=0.80, p0=0.04/0.40: **0.236 / 0.251**.

All next-q values lie far below the model's q=0.625 endpoint-allele switch even though the q0=0.80 cells initially had **\(W(1;q_0)=1.14>1\)**, because initial high-trait mass was zero and density was only 0.5. The derived **\(d\ge0.880024\)** necessary gate for reaching the q switch *from a trait-zero source at any q,p* explains this first-generation collapse. It does not independently explain all changes in p or trait occupancy over generations 2–12, which also involve genetic drift, recruitment and source density feedback.

**Actual scientific conclusion within this bounded model:** a trait can reappear quickly from a latent allele reservoir even as the ecological support coordinate weakens. Starting with a larger latent reservoir is associated with much more repeated trait occupancy and reduced entry into the irreversible joint-zero class in this synthetic parameter setting. Starting with higher q alone helps early reappearance but **does not establish a durable 12-generation high-trait advantage in these four conditions**.

**Strong negative boundary:** model high-bin expression, being present for three snapshots, and even initially favorable high-endpoint trait fitness are not interchangeable with measured effective pollination, multi-year population establishment or naturally observed reversal of a lost reproductive character.
