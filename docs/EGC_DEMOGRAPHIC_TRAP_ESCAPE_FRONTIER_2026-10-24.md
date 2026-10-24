# A sharp demographic-growth escape frontier: possibility versus probability of ecological support

**24 October 2026. Source-specific Type T parameter boundary with exact, pinned EGC one-generation stochastic trait kernel.** This is a follow-up to [the all-state demographic-trap certificate](EGC_TRAIT_ABSENCE_DEMOGRAPHIC_FEEDBACK_TRAP_2026-10-24.md), not a natural general law or a retrospective search for an AA-favouring configuration.

## Why the boundary matters

The fixed EGC source at commit `dd8ee379d0d3518194c767d16402042525bc00dc` with baseline demographic growth **r=0.30** provably cannot restore the high-trait potential viability region from generation 3 onward once initial high-trait mass is zero. That is a rigorous result *at a fixed parameter setting*. The next question is whether it describes a general structural limitation or a fragile parameter inequality.

We vary **only the demographic baseline growth r**, leaving the full q-feedback rule (κ=4.5, θ=0.5025, α/β/γ=.6/.3/.1), carrying capacity K=40, population interaction/allele growth .4/.1, trait fitness and recruitment parameters otherwise unchanged. The claim being tested is **one event at generation 2**: can q₂ reach the fixed high-trait endpoint and allele-relative-fitness switch q*=0.625 from a generation-0 phenotype-absent state? It is explicitly **not** an inference about later population persistence or re-established flowering function.

## Theorem — sharp attainable/nonattainable switch as r changes

Under the fixed EGC growth rule (unit patch area and area reference, no demographic immigration), assume initial high-trait mass T₀=0 but allow *arbitrary* initial positive integer N₀ and any q₀,p₀∈[0,1]. The original update satisfies:

\[
q_1\le Q=\sigma\{4.5[0.7-0.5025]\}=0.7086321491,
\]

and, with the variable demographic baseline r,

\[
N_1\le \max\{1,\mathrm{round}[40\exp(r+0.4Q+0.1-1)]\}.
\]

The bound is **sharp** because its maximum is jointly attained by the extreme admissible source state \(N_0=40,q_0=1,p_0=1,T_0=0\). Setting p₀=1 makes post-selection allele frequency and p₁ equal 1 when allele mutation is zero. A two-kernel recruit update with inheritance weight h=.5 then provides a *positive* chance that each of the N₁ recruited trait bins is high.

If T₁=p₁=1, the most favorable possible next interaction is

\[
Q_{2,\max}(N_1)=\sigma\left\{4.5\left[
\min(1,N_1/40)(0.6Q+0.4)-0.5025
\right]\right\}.
\]

To make q₂≥0.625 possible, an integer N₁ must satisfy

\[
N_1\ge\left\lceil
\frac{40[0.5025+\operatorname{logit}(0.625)/4.5]}{0.6Q+0.4}
\right\rceil
=\boxed{30}.
\]

The **critical baseline growth** at which the maximal *unrounded* N₁ reaches the nearest-integer threshold 29.5 is

\[
\boxed{
r_c=\ln(29.5/40)+1-0.4Q-0.1
\approx0.31205795.
}
\]

Thus under this fixed family, **r below r_c makes q₂≥0.625 impossible for all admissible initial q₀,p₀,N₀ and all stochastic trait draws**, while **r strictly above r_c makes it possible with nonzero probability** for the extreme source state just described. The exact tie convention *at* r=r_c belongs to Python's nearest-even rounding and should not be confused with a robust biological critical point.

The sufficiency-for-possibility argument is constructive: for r>r_c, N₁≥30 at q₀=p₀=1,N₀=40. Since source `two_kernel_recruitment` with h=.5 supplies each recruit a strictly positive probability of a high bin, the event *every one of N₁ recruits is high* has a strictly positive probability and yields T₁=1. Therefore q₂≥0.625 has nonzero chance. This proves only an **attainability frontier**, not a likely recovery, local population viability, or durable high-trait maintenance.

## Exact probability can remain negligible just above the frontier

The source's actual multinomial high-trait recruit probability `s` is computed by its original `recruit_trait_distribution`, `trait_fitness` and grid, not a reimplemented transition kernel.

For the fixed extreme witness (q₀=p₀=1, N₀=40, T₀=0), the first-step allele remains exactly p₁=1 (no mutation). Let `K₁` be the number of high-bin recruits from the original finite trait source in generation 1. Then

\[
K_1\mid X_0,N_1\sim \mathrm{Binomial}(N_1,s).
\]

The exact minimum high-bin count required for q₂ to cross 0.625 is the first integer k that meets

\[
\min(1,N_1/40)
\left(0.6Q+0.3\frac{k}{N_1}+0.1\right)
\ge 0.5025+\frac{\operatorname{logit}(0.625)}{4.5}.
\]

Therefore the **original source's exact conditional crossing chance** is

\[
\Pr(q_2\ge0.625\mid X_0,r)
=\sum_{k=k_{\rm req}}^{N_1}
{N_1\choose k}s^k(1-s)^{N_1-k}.
\]

The model's high-bin probability at q₀=p₀=1 is approximately **0.49546**. At r just above the sharp boundary, *all thirty recruits must be high*, so probability is positive but approximately \(7.08\times10^{-10}\). The jump from mathematically impossible to possible is **not** a discontinuous jump to high establishment probability: the source population is finite, and there may be very few successful trait recruits.

## Fixed source validation settings — no post-outcome parameter search

The analytical boundary was derived before the actual source draw test. The code locks the explanatory comparisons to r = 0.30, r_c−0.001, r_c+0.001, 0.35, 0.45, 0.50, 0.55, 0.65, all using the same extreme attainable witness q₀=p₀=1, N₀=K=40, T₀=0. For the six nominal parameter values, source simulations use **512 new seeds 80001–80512** each for two generations; the two immediately adjacent r_c values are analytical-only.

The test compares the source-conditioned exact binomial crossing probability to the empirical fraction of crossing events in the **original pinned EGC stochastic simulator**, without inserting pseudo-local q updates or independent Gaussian noise. Each observation is a separate two-generation source trajectory, not a repeated plant frame or an independent time step inside a trajectory.

This is a **descriptive internal calibration**, not a hypothesis test against nature or a robust long-horizon rescue experiment. Even at high r, a successful q₂ crossing says nothing by itself about q₃, the subsequent potential high-trait component, high-trait realised occupancy, or the probability of later persistence.

## What this adds to the overall ecological story

The previous strong fixed-parameter result was not wrong; this sharper **parameter frontier states exactly what it does and does not cover**.

1. The biological model can preserve a latent high-trait allele and repeatedly express high-trait recruits without reopening the source's potential high-trait niche, as PRs #230–233 established.
2. The impossibility of reopening ecological support is contingent on **demographic supply and feedback**. A modest shift in a specified growth parameter can remove the mathematical impossibility, while the probability of actually crossing that frontier can remain exceptionally small.
3. Thus the nontrivial issue is not simply whether a phenotype can reappear or whether a latent allele is present. It is whether the **demographic and interaction regime supplies enough support for re-expression to become potentially viable**, and how rare the needed multivariate trait configuration is.

The precise critical number \(r_c\) is a property of **this fixed finite EGC source, its rounding convention and parameter values**, not a universal ecological demographic growth rate. No molecular mechanism of anthocyanin reactivation, pollinator species response, island–urban equivalence, or natural-functional-fate outcome has been verified.

## Exact provenance

- Frozen source: [EGC pinned life cycle](https://github.com/zuizui0223/egc/blob/dd8ee379d0d3518194c767d16402042525bc00dc/causal_model/symmetric_allele_mutation_closure.py).
- [Previous full-population feedback trap certificate](EGC_TRAIT_ABSENCE_DEMOGRAPHIC_FEEDBACK_TRAP_2026-10-24.md).
- Executable: `scripts/egc_demographic_trap_escape_frontier.py` imports the same pinned source and computes the exact analytic and finite-binomial probabilities.
- `tests/test_egc_demographic_trap_escape_frontier.py` verifies critical rounding, source recruitment probabilities, and original two-generation stochastic trajectories.
- A separate GitHub Actions workflow pins the upstream commit, saves a machine-readable receipt and checks source fidelity. NEE original evidence remains unchanged.
