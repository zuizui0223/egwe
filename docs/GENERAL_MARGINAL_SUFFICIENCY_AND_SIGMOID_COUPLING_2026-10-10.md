# Exact one-step marginal sufficiency and the sign of spatial eco-genetic coupling

**10 October 2026. Status: new general mathematical bridge derived from classical mixed differences / rearrangement theory.** No new stochastic loss experiment, natural joint-state fit, ecological coefficient, or update to the frozen NEE manuscript. The code in `scripts/general_marginal_sufficiency.py` verifies finite exact tables, nonlinear curvature signs and the original declared q-support example.

## Biological question and a necessary distinction

The NEE flagship [`manuscript/nee_flagship_article.md`](../manuscript/nee_flagship_article.md) constructed two **identical-marginal but differently aligned** four-patch configurations. Their *labelled local next-q fields* differed by up to 0.2543. That counterexample is exact within the declared finite closure. The natural-generalization question is which **classes of local transition rule** can hide information in cross-layer spatial matching.

This extension distinguishes three observables that cannot be conflated:

1. **Patch-labelled transition vector** `(F(x_i,y_i))_i`: a marginal summary that forgets the association of x and y usually cannot recover this *even for additive F*.
2. **Sum / equally-weighted mean of the next local states** `T(pi) = sum_i F(x_i,y_pi(i))`: matching can matter only when F has nonzero cross-layer *mixed differences*. This is the exact main theorem below.
3. **Later ecological persistence/loss**: stochasticity, spatial coupling, dispersal, selection, recruitment, density and the future endpoint determine this. A one-step aggregate comparison does **not** establish a long-horizon fate ordering.

The equal-weight and free-pairing assumptions in (2) are mathematically material. Nonuniform patch weights `sum w_i F(x_i,y_pi(i))` can depend on pi **even if F is additive**, because the y component is reweighted by patch. If patch capacities, geometry, density or sampling effort differ, they must be held fixed and explicitly included in the state or a separate weighted theorem.

## Theorem 1 — exact if-and-only-if aggregate marginal sufficiency

Let x and y take values in sets X and Y. For any n ≥ 2, every vector `x=(x_1,...,x_n)`, every vector `y=(y_1,...,y_n)`, and permutation pi, define the one-step aggregate

\[
T_{F}(x,y;\pi)=\sum_{i=1}^n F(x_i,y_{\pi(i)}).
\]

No derivative, sigmoid, linearity, stochastic assumptions or threshold is required of the real-valued local rule F.

**Equivalence.** The following are equivalent:

1. `T_F` is invariant to every permutation pi for **all possible** matched marginals (already n=2 suffices).
2. Every rectangle mixed difference vanishes, i.e. for every x1,x2 in X and y1,y2 in Y,

\[
\boxed{\Delta_F =
 F(x_1,y_1)+F(x_2,y_2)
 -F(x_1,y_2)-F(x_2,y_1)=0.}
\]

3. There exist a function A on X and B on Y such that

\[
\boxed{F(x,y)=A(x)+B(y)\quad\text{for all }(x,y)\in X\times Y.}
\]

**Proof.** (1) ⇒ (2): take n=2 and exchange the two y labels, retaining both marginal multisets; the difference in aggregates is precisely Δ. (2) ⇒ (3): choose arbitrary anchors x0,y0, define A(x)=F(x,y0) and B(y)=F(x0,y)−F(x0,y0). The anchor rectangle identity gives F(x,y)=A(x)+B(y) for every pair. (3) ⇒ (1): `T=sum_i A(x_i)+sum_i B(y_i)`, which cannot depend on pi. □

**Corollary (constructive coarse-state failure).** If even *one* admissible rectangle has Δ≠0, there exist two equal-marginal two-patch configurations with **different aggregate next states**. Therefore separate x and y marginals cannot be a globally sufficient aggregate transition description for that F. For a particular finite observed pair of marginal vectors, a nonzero rectangle elsewhere in the state domain does not imply a difference; check their actual admissible swaps.

**Smooth version.** If F is C² on an open connected rectangle, then

\[
\Delta_F=\int_{x_1}^{x_2}\int_{y_1}^{y_2}
\frac{\partial^2 F}{\partial x\partial y}(u,v)\,dv\,du.
\]

Thus F is additively separable on that rectangle **iff** `F_xy=0` everywhere. This gives a test of when nonlinear ecological/trait feedback can affect *aggregate* next-step function through matching.

**Important caveat about the word “nonlinear.”** An additive but nonlinear rule `F(x,y)=x²+sin(y)` leaves the aggregate invariant; a positive linear combination `F(x,y)=a x+b y` also leaves the aggregate invariant. **Nonlinearity in itself is not enough**; the mixed rectangle effect is what matters.

### The stronger labelled-vector counterexample

For x=(0,1), y=(1,2), `F(x,y)=x+y`: aligned next vector is (1,3) while reversed is (2,2). Both sum to 4. Hence Theorem 1 governs aggregate sufficiency **only**. It neither weakens nor replaces the original EGWE result about patch-specific transition maps.

## Theorem 2 — sign and bounds from increasing/decreasing differences

For x1<x2, y1<y2, define positive aligned-minus-reversed Δ as above. If `F_xy>=0` on the entire rectangle, then Δ≥0; if `F_xy<=0`, then Δ≤0. Strict inequalities throughout give strict signs.

For n patches, any inverted permutation pair can be swapped while conserving x and y marginals. Each such swap changes the aggregate by the corresponding Δ. Repeating swaps proves the classical **rearrangement result**:

- With globally nonnegative mixed differences, positively sorted matching maximizes the aggregate and reverse sorting minimizes it.
- With globally nonpositive mixed differences, positively sorted matching **minimizes** the aggregate and reverse sorting maximizes it.
- When the mixed-partial sign changes within the admissible state rectangle, neither alignment direction is generally optimal. A particular finite matching may still have a signed effect, which must be checked rather than assumed.

These are classical complementarity/supermodularity arguments, not a newly invented theorem. Sources: [Rabah Amir, *Supermodularity and complementarity in economics: an elementary survey*](https://www.laits.utexas.edu/~mbs31415/Amir_Supermodularity_Survey.pdf), and Topkis, *Supermodularity and Complementarity* (1998), as a standard reference for increasing differences. The contribution of this note is applying the distinction to the **declared eco-genetic update and to its ecology-facing interpretation**, not claiming priority for the rearrangement theory.

## Corollary 2A — a sigmoid interaction changes the value of spatial alignment with regime

Consider a family of local eco-genetic update rules

\[
F(x,y)=\sigma\big[\kappa(\alpha x+\beta y-\theta)\big],
\quad \alpha,\beta,\kappa>0,
\quad \sigma(z)=(1+e^{-z})^{-1}.
\]

Then, writing f=F(x,y),

\[
\boxed{
F_{xy}=\kappa^2\alpha\beta f(1-f)(1-2f).
}
\]

So `F_xy>0` when `alpha*x+beta*y < theta` (output below 1/2), and `F_xy<0` when `alpha*x+beta*y > theta` (output above 1/2).

This identifies a **mechanistic sign boundary**: near the sigmoid's accelerating lower limb, two high supports can be complementary for the aggregate update, whereas on the saturating upper limb the same positive supports can become aggregate substitutes. **Do not call this boundary q*=0.625.** The sigmoid's curvature inflection is at the *next-q output of 0.5*, whereas the parent model's allele/trait selection-viability switch at next-q=0.625 is a separate equation (`w(q)=1`). The two are not interchangeable ecological thresholds.

### Identical marginals, sign-reversed one-step aggregate

With completely synthetic x=(0.2,0.4), y=(0.2,0.4), coefficients `alpha=.6,beta=.4,kappa=4.5`, changing only the declared forcing/threshold theta:

| Local regime | theta | Exact paired contrast Δ = aligned minus reversed |
| --- | ---: | ---: |
| Saturating (all support > theta) | 0.10 | approximately **−0.01642856** |
| Accelerating (all support < theta) | 0.80 | approximately **+0.01356005** |

Both examples retain the same x and y marginal vectors and the same positive coefficients. Thus one **cannot** elevate “aligned eco-genetic states always raise realised interaction” to a universal ecological law. This sign change can occur without negative genotype/interactor coefficients: it results from curvature.

This is an **aggregate one-step** result, not a prediction that alignment reverses long-term functional-loss risk. Theorem 2 states sufficient orientation conditions for a particular update rule and state range; mixed-range cases require a direct Δ computation.

### Anchoring the existing four-patch q/bundle example

With the flagship's declared values

`q=(.65,.75,.85,.95)`, `B=(.2,.4,.6,.8)`,
`F(q,B)=sigmoid(4.5*(.6*q+.4*B-.5025))`

at fixed **unit area and density**, the original AA alignment yields mean one-step q⁺ **0.67153146** whereas the RR reversed pairing yields **0.68929685**. Accordingly, the AA−RR mean is **−0.01776539**, *despite* AA retaining much deeper maximum local support/margin. The local fields differ by up to the preexisting `0.2543` magnitude; our new mean value is a deterministic calculation from the same fixed inputs, **not** a newly run simulation, a freshly preregistered endpoint, or a biological fitness difference.

This reconciles, rather than overturns, the existing [coverage–reserve trade-off](OPERATOR_BALANCE_ROUTE_MARGIN_THEOREM_2026-09-06.md): reversal can improve *average immediate interaction* while alignment retains a larger *maximum local refuge margin*. The average next-q and strongest-local-margin objectives are not equivalent.

For the actual four-patch state the rectangle spans both sides of the sigmoid's inflection. Hence the global super/submodular sorted optimum theorem alone does not determine the orientation; the code **enumerates all 24 pairings** to check the realized one-step values.

## Theorem 3 — a transferable one-step sorting identity, but only under local selection

For any independent local log-odds selection operator satisfying

\[
u_i^+=u_i+h(q_i),\qquad u_i=\operatorname{logit}(p_i),
\]

the exact change in covariance is

\[
\boxed{
\operatorname{Cov}(q,u^+)-\operatorname{Cov}(q,u)
=\operatorname{Cov}(q,h(q))
=\frac{1}{2n^2}\sum_{i,j}
(q_i-q_j)(h(q_i)-h(q_j)).
}
\]

For any **nondecreasing** h, this change is nonnegative; if h is strictly increasing across at least two different q's, it is strictly positive. If h is constant it is exactly zero, and if h is decreasing it is nonpositive. The result needs no specific 0.625 allele switch or logistic fitness form; it follows directly from monotone local selection.

For conventional relative-fitness selection `p_i^+=p_i*w(q_i)/(1-p_i+p_i*w(q_i))`, `h(q)=log w(q)`. When relative fitness w is increasing in q and strictly positive, local selection **sorts allele log-odds with the interaction state**. The EGWE pinned `w(q)=0.75+0.4 q` satisfies this condition. A model with decreasing w reverses the covariance effect; one with constant w has none.

**Not implied:** that neutral diversity necessarily falls, that allele-frequency covariance rises after drift, that immigration can be ignored, that next ecological interaction always increases or that later functional-loss risk is reduced. The identity is for the deterministic **one local selection log-odds step before drift, recurrent mutation, dispersal or recruitment**.

## What has now generalized—and what has not

| Scientific claim | Status |
| --- | --- |
| Aggregate one-step state independent of cross-layer pairing **iff** additively separable local rule | **Mathematically general, exact** within freely permutable equal-weight-patch setting |
| Direction of sorted pairing determined by sign of mixed differences on applicable state range | **Classical rigorous result**, now connected to eco-genetic local update |
| Sigmoid positive interactions always benefit aligned spatial states | **False**; rigorous below/above-inflection sign reversal |
| Increasing relative fitness in interaction causes a nonnegative local selection-induced q–log-odds covariance increment | **Exact under local log-odds selection** |
| Same aggregate implies same labelled patch state or same ecological long-term fate | **False / not derived** |
| General stochastic long-horizon necessity/sufficiency of q–genetics covariance or full natural H-R verification | **Open; not asserted** |

The next theoretical extension requiring separate assumptions would characterize operator compositions (selection + mating, drift, recruitment, dispersal) or contraction/expansion bounds under migration. No universal ecological prediction can be inferred merely by composing positive one-step local mixed-difference signs.

## Reproducibility

The pure-standard-library script `scripts/general_marginal_sufficiency.py` outputs an algebra-only JSON receipt. The test suite

```bash
python -m pytest -q tests/test_general_marginal_sufficiency.py
```

checks rational exact grid identities, nonseparable counterexamples, differentiable logistic cross partials, sorted extrema across **all permutations** in small patch sets, the precise original four-patch mean one-step update, increasing/decreasing/constant selection fitness maps and the explicit no-long-horizon/no-natural-validation flags.

The active `manuscript/nee_flagship_article.md`, previously frozen numeric outcomes, source hashes, natural negative results and publication lanes are **unchanged**. This is an independently auditable theorem bridge to be considered editorially, not silently merged into the paper as if preregistered prospective ecological evidence.
