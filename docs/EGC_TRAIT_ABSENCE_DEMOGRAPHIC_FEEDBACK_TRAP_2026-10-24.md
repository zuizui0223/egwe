# A source-specific demographic–ecological trap after loss of the expressed high trait

**24 October 2026. Type T: conditional mathematical certificate for a fixed EGC source and parameter regime.** This is NOT a new universal biological law, a natural flower-colour result, or a proof of the full NEE manuscript's empirical claims.

## Why this follows the executed 256-seed study

EGWE PR #232 (merged `03bf38d`) used the fixed complete stochastic EGC source at commit `dd8ee379d0d3518194c767d16402042525bc00dc` and 256 new seeds in four initial state cells. Increasing the retained high-allele frequency from 0.04 to 0.40 strongly increased *expressed high trait present at generation 12* (q0=0.2: 7/256→74/256; q0=0.8: 4/256→78/256). An initially high interaction state q0=0.8, however, collapsed by generation 1 to q1≈0.236–0.251. These source results prompted the following **post hoc mathematical generalization**, which is independently verifiable for every allowed initial q,p,N in the declared fixed closure, not fitted to those outcomes.

The main new question is stronger than the original q=0.625 endpoint check: *can the ecological system re-establish a potentially viable high-investment trait component after the high trait has disappeared, even if allele-linked recruitment repeatedly makes high-trait individuals?*

## Exact parameters and source update

Consider **any finite number of area-1 patches** with density capacity K=40, area reference 1, constant barrier θ=0.5025, interaction feedback κ=4.5, q coefficients (α,β,γ)=(0.6,0.3,0.1), and demographic growth (baseline 0.3, interaction 0.4, high-allele growth 0.1). These correspond to the source-pinned exploratory EGC configuration in PR #232, not all admissible EGC parameterizations.

For each patch and generation t, write q∈[0,1] for effective interaction, p∈[0,1] for high-allele frequency, T∈[0,1] for high-trait abundance fraction and n≥1 integer for the local plant population. The original source calculates:

\[
q_{t+1} = \sigma\!\left(4.5\left[\min(1,n_t/40)
(0.6q_t+0.3T_t+0.1p_t)-0.5025\right]\right).
\]

The same source computes local allele selection with \(0\le p_{t,\mathrm{selected}}\le1\), followed by population update

\[
n_{t+1}=\max\{1,\operatorname{round}[
n_t\exp(0.3+0.4q_{t+1}+0.1p_{t,\mathrm{selected}}-n_t/40)]\}.
\]

Subsequent finite trait-bin recruitment, allele-frequency migration, mutation and binomial drift may change T or p, but all their state values remain in [0,1]. The proof does not assume allele frequencies are constant, prevent stochastic trait reappearance, or treat finite population size 1 as demographic extinction. It *does* assume no additional immigration of whole plants or direct exogenous forcing to the interaction/population updates and the fixed area, barrier and demographic coefficients above.

## Theorem — phenotype absence entails irreversible loss of potential high-bin viability in this particular feedback regime

**Assume at generation 0 all patches have high-trait mass T₀=0.** Initial q₀,p₀ may take **any** values in [0,1], and every initial n₀ may be **any positive integer**. Under the pinned source update and parameters above:

1. Every patch satisfies q₁≤0.70863215 and n₁≤29;
2. Every patch satisfies q₂≤0.60608795 and n₂≤27;
3. Every patch satisfies q₃≤0.51458219 and n₃≤25;
4. For **all** t≥3, every patch remains in the forward-invariant region \(q_t\le0.59,\ n_t\le29\).
5. The source's **entire 101-point high-investment trait grid** z≥0.7 has fitness \(W(z;q_t)<1\) for all t≥3. Thus **no potentially viable high-trait component** exists after the third generation under this condition, even when stochastic allele-seeded recruitment later expresses high-trait individuals.

This is a *pathwise, source-specific* upper bound. There is **no probability qualifier** on the bound within the declared closure: it holds for every allele/trait stochastic draw because the derivation allows the most favourable possible future allele frequency and high-trait fraction (both 1).

### Proof: from T₀=0 to three-generation entry

Since q₀,p₀≤1, density≤1 and T₀=0, the interaction's maximum possible support at the first update is 0.6+0.1=0.7. Therefore

\[
q_1\le\sigma[4.5(0.7-0.5025)]=0.7086321491.
\]

For **any positive n**, and any fixed A, the function \(f(n)=n\exp(A-n/40)\) has global maximum at n=40 and value \(40\exp(A-1)\). Setting \(A=0.3+0.4(0.7086321491)+0.1\), the **unrounded** n₁ is at most 29.14642646, strictly below 29.5. Hence the original nearest-integer rounding rule plus floor of one yields **n₁≤29**, regardless of n₀.

At time 1 we deliberately give the recovering phenotype and allele *every possible advantage*, T₁=p₁=1. The interaction can still reach at most

\[
q_2\le\sigma\left\{4.5\left[
\frac{29}{40}(0.6\times0.7086321491+0.4)-0.5025
\right]\right\}
=0.6060879465.
\]

Because 1≤n₁≤29<40, the function n exp(A−n/40) is increasing over this restricted range. Using q₂'s bound, n₂'s unrounded maximum is 26.70180079, which yields **n₂≤27**. The same best-case T₂=p₂=1 then gives

\[
q_3\le\sigma\left\{4.5\left[
\frac{27}{40}(0.6\times0.6060879465+0.4)-0.5025
\right]\right\}
=0.5145821842.
\]

Similarly the unrounded upper n₃ is 25.19560916, hence n₃≤25. These inequalities hold separately in every patch and under arbitrary allele-only migration, finite drift and symmetric mutation that preserve p∈[0,1].

### Proof: no reopening after generation 3

Define \(\mathcal R=\{(n,q):1\le n\le29,\ 0\le q\le0.59\}\). For *any* T,p∈[0,1] and a state in \(\mathcal R\),

\[
q_{\mathrm{next}}\le\sigma\!\left[
4.5\left(\frac{29}{40}(0.6\times0.59+0.4)-0.5025\right)
\right]
=0.5495060163<0.59.
\]

The same monotone demographic bound at n=29 and this upper q gives unrounded n_next≤26.10425261, rounded to **n_next≤26<29**. Thus \(\mathcal R\) is forward invariant and contains all t≥3 states. □

### Why this is a whole high-trait-grid result, not only q*=0.625

The previously reported q*=0.625 switch checks the **endpoint** z=1 performance \(W(1;q)=0.5+0.8q\) and allele relative fitness; it is not automatically equivalent to viability at every high-trait z≥0.7.

We therefore check the source's actual potential-viability definition directly. On the **pinned 101-point trait grid**, the trait surface is

\[
W(z;q)=1.1-0.8z^2+(0.2+0.8q)
\exp[-((z-1)/0.15)^2].
\]

For all q≤0.59, the high-region maximum is attained below 1 at z=0.97:

\[
\max_{z\in\{0.70,\ldots,1.00\}}W(z;0.59)
=\mathbf{0.9929305031}<1.
\]

Each high-grid fitness is nondecreasing in q, so the same strict inequality holds at every q≤0.59. The source's potential high-trait component is **absent** from t≥3.

This result does **not** require the observed high-trait *abundance* to be zero. In fact, the finite, allele-seeded two-kernel recruitment operator assigns positive probability to high-trait recruits even when their trait fitness is below the potential-viability threshold. The result is exactly the ecological distinction now visible in the full-source experiment: **phenotypic reappearance without restoration of the ecological regime that would sustain a viable high-investment component**.

## What this changes—and what it does not

- It clarifies the PR #232 pattern: high retained p strongly increased 12-generation expressed occupancy, but that does **not** indicate that the model's high-trait potential-viability region had reopened.
- It is a genuine **conditional impossibility certificate** about this fixed model, not just an average of finite simulations; it still does not assert a universal ecological law.
- It is stronger than saying q<0.625 in a snapshot: it bounds q at every later generation and checks the entire high-trait grid, using a forward-invariant region.
- It is **not** a theorem under other barriers, densities/carrying capacities, non-unit patch areas, changes in demographic growth, whole-individual demographic inflow, altered feedback weights or a barrier schedule that can decrease. These could break the invariant region.
- It is **not** a biological claim that white-flowered thistles retain anthocyanin capacity, that a flower phenotype is genetically recoverable, or that pollinator function is irreversibly lost in nature.
- It is **not** a claim that the population went extinct. The EGC source explicitly floors population counts at 1.
- It does not alter any frozen Nature Ecology & Evolution flagship simulations or source claims. These are post hoc theoretical investigations of a declared auxiliary source-pinned parameter regime.

## Reproducibility

`scripts/egc_trait_absence_demographic_trap.py` emits deterministic, source-specific bounds and the fixed-grid high-trait fitness maximum.

`tests/test_egc_trait_absence_demographic_trap.py` checks the analytic steps and proof's invariants, verifies the source's original fitness formula and parameters, then runs the **actual pinned EGC stochastic simulator** across numerous extreme initial population sizes, allele and interaction values. A multi-patch test includes high allele-only migration and symmetric mutation to ensure the result is not an artifact of artificially fixing p. A separate source test checks that realised high-trait individuals **can still exist at t≥3**, despite high-trait *potential viability* having vanished.

This is an observable positive model-mechanism insight, **not** an empirical result or ecological field validation. The critical next biological question is how to distinguish transient expressed traits from ecologically viable and persistently functional traits in a population-specific observation design.
