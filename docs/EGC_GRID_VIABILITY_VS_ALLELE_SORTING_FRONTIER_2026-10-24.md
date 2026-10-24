# A transient high-trait viability window can precede positive allele selection — source-exact EGC frontier

**24 October 2026 — prospective source-pinned numerical/analytical boundary, not natural ecological data.** This is a bounded extension of [PR #233's t≥3 demographic-trap proof](EGC_TRAIT_ABSENCE_DEMOGRAPHIC_FEEDBACK_TRAP_2026-10-24.md) and [PR #234's sharp q=0.625 endpoint-growth frontier](EGC_DEMOGRAPHIC_TRAP_ESCAPE_FRONTIER_2026-10-24.md). All source-level formulas are checked against `zuizui0223/egc@dd8ee379d0d3518194c767d16402042525bc00dc`. Nothing in this protocol changes the frozen NEE evidence or asserts field validation.

## The ecological distinction the previous frontier left unresolved

The pinned life cycle has **two different conditions**:

1. **Potential viability anywhere within the high-investment trait grid**: at least one original source trait bin `z>=0.7` has `W(z;q)>=1`. This is how `trait_space_summary(q).high_trait_component_present` is calculated.
2. **Nonnegative deterministic selection on the high-associated allele**: in the source, the selected allele's relative fitness is based on the **endpoint** `W(z=1;q)`, so `w_high=0.75+0.4q>=1` only if `q>=0.625`.

The two are **not mathematically equivalent** because a high-investment bin with `z<1` can have greater trait fitness than the endpoint `z=1`. A conclusion about `q=0.625` cannot automatically be substituted for full-grid potential viability.

### Exact grid-derived threshold

The original 101-point trait grid `z=0,0.01,...,1` and high subset `z>=0.7` use

\[
W(z;q)=1.1-0.8z^2+(0.2+0.8q)\exp[-((z-1)/0.15)^2].
\]

For each high-bin z, this expression is affine with **positive slope in q**, hence its viability threshold is

\[
q_z=\frac{1}{0.8}\left[
\frac{1-(1.1-0.8z^2)}{\exp[-((z-1)/0.15)^2]}-0.2
\right].
\]

The full-grid threshold is `q_grid=min_{z>=0.7}q_z`, over the **pinned discrete grid**, not a new continuous optimum. Exact evaluation through the *original source's* `trait_fitness`, `trait_grid` and `trait_space_summary` gives

\[
\boxed{q_{\mathrm{grid}}\approx0.5991975107\ (z=0.97)}
\quad<\quad
\boxed{q_{\mathrm{allele}}=0.625}.
\]

The difference is approximately 0.02580249 in q. Thus an interaction state may support a **potentially viable high-investment phenotype bin** while the modeled allele associated with the high endpoint is still being selected against.

That is a bounded **source representation/selection-rule property**, not a general biological discovery about genotype/trait mismatches.

## Theorem: two distinct sharp population-growth attainability frontiers at generation 2

Keep the original source settings of PR #234: area ratio 1, density capacity `K=40`, interaction feedback `4.5`, constant barrier `theta=0.5025`, weights `alpha=.6,beta=.3,gamma=.1`, population growth terms `r+.4q+.1p-N/K`, allele-seeded two-kernel recruitment `h=.5`, mutation zero, no demographic immigration. At initial time, **all expressed high-trait mass is zero**, and starting `q0,p0` may be any values in [0,1] with any positive integer starting population `N0`.

As PR #234 established, the **attainable simultaneous first-step maxima** occur at `q0=p0=1,N0=K=40`. They include

\[
Q=q_{1,\max}=\sigma\{4.5[(.6+.1)-.5025]\}
=0.7086321491.
\]

If at generation 1 all the recruited trait bins are high and the allele is still p1=1, the maximal second-step support given next population `N1` is

\[
d_1(0.6Q+0.3+0.1),\qquad d_1=\min(1,N_1/40).
\]

For either target interaction `q_target`, define `H(q_target)=.5025+logit(q_target)/4.5`. The minimum integer `N1` required for *possibility* of `q2>=q_target` is

\[
N_{\rm req}(q_{\rm target})
=\left\lceil\frac{40H(q_{\rm target})}{0.6Q+0.4}\right\rceil,
\]

provided `N_req<=40`. The maximum first-generation population is the actual **nearest-integer-rounded** source growth from `N0=40`:

\[
N_{1,\max}=\max\{1,\mathrm{round}[
40\exp(r+0.4Q+0.1-1)]\}.
\]

To permit that required count, the sharp strict-growth boundary is

\[
r_{\rm crit}(q_{\rm target})
=\log[(N_{\rm req}-0.5)/40]+1-0.4Q-0.1.
\]

The equality boundary depends on source Python nearest-even rounding. The ecological theorem uses **strict r below/above** the respective value, rather than claiming robust biological meaning at the exact rounding tie.

| Generation-2 target | Minimum N1 | Sharp baseline-growth boundary r |
| --- | ---: | ---: |
| **Any high-grid bin potentially viable** (`q2>=q_grid`) | **29** | **0.2775717735** |
| **High-associated endpoint allele not selected against** (`q2>=0.625`) | **30** | **0.3120579496** |

For **r below 0.27757**, neither target is reachable at t=2 in this fixed closure. For **0.27757 < r < 0.31206**, the grid viability target has a positive-probability path, while nonnegative allele selection at t=2 is impossible. For r above the higher frontier, both targets become *attainable*, but neither is guaranteed or necessarily common.

**Proof of sharpness.** The upper bound on q1 follows from T0=0 and maximal q0=p0=1. Maximizing the source Ricker-type integer population update over initial N0 gives N0=K. The resulting q1 and N1 bounds are attained simultaneously at the same extreme source state. Given that extreme state and resident p1=1, two-kernel recruitment assigns positive probability to every high trait bin; therefore the event *all N1 recruited trait bins are high* has nonzero probability. Such a draw attains the maximal possible q2 at the specified N1, proving attainability when the upper support crosses. If even the maximal N1 falls short of the support threshold, no allowed initial state or random trait draw can cross. □

## A transient viable-bin window at the pinned baseline r=0.30

At r=0.30, the original EGC source gives `N1=29` and maximal `q2=0.6060879465`. Because

\[
q_{\mathrm{grid}}\approx0.59920<0.60609<0.625,
\]

the event **all 29 first-generation recruits land in high bins** yields a potentially viable high-trait bin at generation 2, while the high-associated allele remains selected against. The exact source first-generation high-bin marginal probability is approximately `s=0.49546180155`, giving

\[
\Pr(\text{high-grid potential viability at }t=2)
=s^{29}\approx\boxed{1.43\times10^{-9}}.
\]

At the same setting, the probability that `q2>=0.625` is **exactly zero**.

This is a **real but extraordinarily unlikely mathematical path** under the declared source. Finding zero instances in 512 or even millions of finite stochastic draws is not a contradiction. More importantly, PR #233 independently certified that **all** these paths, including the rare temporarily viable one, enter a region without potentially viable high-investment bins by **t≥3** under r=0.30. Thus this is not sustained ecological rescue.

### Why trait-grid viability and the allele can disagree

At the allowed maximal q2≈0.60609, the pinned source predicts a high bin z≈0.97 has W(z;q2)>1, but the source's high-associated allele is selected via the **z=1 endpoint fitness**, with `w_high=0.75+0.4*q2<1`.

This is not a contradiction in the simulation code: the two-kernel high-trait distribution spans multiple high bins, whereas allele selection uses its designated extreme z=1 high-trait route. It is, however, an important reminder that **coarse phenotype performance, allele-fitness proxies and multi-generation persistence must not be conflated**.

## Source-exact probabilistic verification

`scripts/egc_grid_viability_vs_allele_sorting_frontier.py` imports the existing PR #234 one-step source runner and the exact original EGC `trait_space_summary` rather than reconstructing the transition law.

- The grid threshold is calculated by the source's `trait_fitness(z,0)` and `trait_fitness(z,1)` across *all high bins*.
- For the extreme attainable witness `q0=p0=1,N0=40,T0=0`, the source's high-bin offspring count `K1\sim Binomial(N1,s)` gives exact probabilities of (i) grid viability, (ii) allele nonnegative selection and (iii) their **difference event** where a potentially viable high-bin coexists with unfavorable allele selection.
- Frozen analytic growth cells: `r=0.27`, `r_gridcrit ±.001`, `r=.30`, `r_allelecrit ±.001`, `r=.35,.45,.50,.55,.65`. Only the six nominal r settings are used for stochastic calibration.
- **512 new source trajectories 90001–90512** for each of the six nominal r values, 2 generations each. The actual EGC simulator supplies `snapshot.trait_space[0].high_trait_component_present` and q2 endpoint status. The script checks each source row against its implied first-generation high recruit count before aggregating.
- The tests confirm the separate critical-population integer steps and exact source conditional probability. No model outcome is used to revise r, grid thresholds or bin definitions after the fact.

The evidence ceiling is **attainable versus probable at generation 2** for the pinned extreme initial state. Neither a temporary high-trait-bin viability certificate nor a probability of positive allele selection is a field estimate of floral reproductive function, a long-horizon establishment rate, natural trait re-evolution or the NEE flagship's future-loss AUC.

## Ecological interpretation

The combined PR #232–#235 results now distinguish four logically separate ecological states:

1. **Latent ability:** the model has high-associated allele p>0 even without expressed high trait.
2. **Expressed high trait:** allele-linked multinomial recruitment can restore high-bin individuals.
3. **Potentially viable high trait:** at least one source high-investment bin can meet `W(z;q)>=1` in the current ecological state.
4. **Favorable genetic selection / durable ecological regime:** high-endpoint allele relative fitness may still be <1, and the actual full life cycle may then enter an irreversible low-support region.

The two intermediate properties (3) and (4) have distinct critical conditions in the pinned source, and (3) does **not** guarantee continued occupancy or later function. That is a useful *model-specific conceptual refinement* for studying latent biological capacity and functional fragmentation, not a universal trait-recovery law.

The existing natural H-R generalization remains **unverified**, and earlier exploratory AA superiority remains **unsupported** after the 128-seed replication. This work changes neither the canonical one-NEE-paper submission lane nor the frozen empirical evidence.

## Executed original-source result — two distinct trait/genetic frontiers

The source-pinned EGC GitHub Actions [run 40070853094](https://github.com/zuizui0223/egwe/actions/runs/40070853094) completed successfully. It ran the exact pinned source's original two-generation stochastic loop for **512 new seeds 90001–90512 at each nominal r** and checked, *for every simulated source trajectory*, that the source's `trait_space_summary` grid-viability indicator and `q2>=0.625` classification agree with the exact source first-generation high-bin recruitment count threshold. The full [artifact 12551142466](https://github.com/zuizui0223/egwe/actions/runs/40070853094/artifacts/12551142466) has uncompressed SHA-256 `e8370e4083047c48e6badd58adc3ac19c40f201c8f82c033a12f952c3f391cf9`. The durable machine summary is `artifacts/theory/egc_grid_viability_allele_selection_20261024.json`.

| Growth r | Probability any high bin is potentially viable at t2 | Probability high allele endpoint relative fitness ≥1 at t2 | **Viable high bin but allele endpoint fitness below 1** | Source checks (grid / endpoint out of 512) |
| ---: | ---: | ---: | ---: | ---: |
| **0.30** | **1.43×10⁻⁹** | **0** | 1.43×10⁻⁹ | 0 / 0 |
| 0.35 | 0.037% | 0.00018% | 0.0365% | 1 / 0 |
| 0.45 | **18.14%** | **2.55%** | 15.59% | 91 / 18 |
| 0.50 | **78.17%** | **28.98%** | **49.19%** | 408 / 142 |
| 0.55 | **89.65%** | **60.74%** | 28.91% | 465 / 318 |
| 0.65 | 99.97% | 99.32% | 0.65% | 512 / 509 |

These percentages are **analytical binomial probabilities conditional on the artificially extreme, fixed initial source** `q0=p0=1,N0=40,T0=0`; the counts are a 512-seed consistency check of the *same* stochastic source. They are not confidence-supported predictions for ordinary fragmented populations. The rare r=.30 route is far too improbable for 512 source draws to be expected to see it. Its mathematical possibility is nevertheless explicitly proven by the positive probability of all 29 offspring being in high trait bins.

The difference event is not a statistical contrast of independently sampled mechanisms: the high-bin threshold and endpoint allele threshold are **nested classifications of the same q2 draw**. For r=.50, the source generated **266/512** trajectories with a viable high grid bin *and* high-associated endpoint relative fitness below one (against exact conditional probability 0.491867); both numbers refer to the same finite model, not an independent ecological confirmation.

### Interpret the phrase “allele selected against” carefully

In the **sharp mathematical attainability witness** p0=p1=1, so the high-associated allele is already fixed. Although its *relative fitness coefficient* `w(q2)=.75+.4q2` can be below 1, **the realized allele frequency cannot decrease through selection while the low allele is absent**: the pinned selection map sends `p=1` to `p'=1` for any positive relative fitness. The discrepancy being proven is between (a) the viability of some **z≈.97** high-trait bin and (b) the sign of the **z=1 high-associated allele's fitness advantage if it competed with a low allele**. It is **not observed high-allele frequency decline in these monomorphic source trajectories**.

At an interior allele frequency, w<1 would indeed lower p under the pinned source's local selection step. Testing the observed frequency consequence in a source population with competing alleles would be a distinct, prospectively specified experiment; it is not estimated by this sharp p=1 attainability witness.

### The temporal limitation is decisive

At the pinned **r=.30**, PR #233 already proves that for any initial source state with T0=0, the source state enters a forward-invariant no-high-grid-viability region by **generation 3** and remains there. The r=.30 rare chance of grid viability at t2 therefore describes a **transient one-generation viability window**, not restoration of a sustainable life-history route. Growth values beyond .30 in the table test **two-generation attainment only**: whether their potentially viable q2 state persists through t3,t12 or beyond is **not established** by this analysis.

The scientific take-away from the bounded source is that the **phenotypic viability frontier, genetic relative-selection frontier, and persistent ecological regime** are three distinguishable conditions. In the inspected growth settings, the grid/allele disagreement rises then falls as r increases; this is an observation of the predefined grid, not proof that the difference is unimodal over all r.

This output is a *source-specific mathematical and synthetic finite-population result*. The natural H-R question, the actual genetic regulation of flower colour, true pollen transfer and species-level evolutionary trait recovery remain unvalidated.
