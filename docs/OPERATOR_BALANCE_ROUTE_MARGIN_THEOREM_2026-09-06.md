# Exact operator-balance route-margin theorem

Status: **exact one-step theorem for the declared finite closure**, linked to already locked endpoint-level causal results for the component operators. This theorem identifies the local sign condition that simultaneously determines the interaction side of the shared switch, the direction of high-allele selection, and potential high-trait viability.

## 1. Define the route margin

The declared interaction update is

\[
q^+=\sigma\{\kappa(a d S-\theta)\},
\]

where `a=A/A_ref`, `d=min(1,N/K)`, and under the locked full-feedback weights

\[
S=0.6q+0.3T+0.1G.
\]

Let the shared switch be

\[
c=q^*=0.625.
\]

Define

\[
H(\theta;c)=\theta+\frac{\operatorname{logit}(c)}{\kappa}
\]

and the **operator-balance route margin**

\[
\boxed{M=a d S-H(\theta;c)}.
\]

For the locked `kappa=4.5` and `c=.625`,

\[
\frac{\operatorname{logit}(0.625)}{4.5}=0.1135168053,
\]

so for unit area ratio

\[
\boxed{M=d(0.6q+0.3T+0.1G)-(\theta+0.1135168053)}.
\]

Because the logistic map is strictly increasing,

\[
\boxed{\operatorname{sign}(q^+-0.625)=\operatorname{sign}(M)}.
\]

Thus `M` is not a fitted risk score; it is an exact algebraic coordinate for the next interaction transition relative to the declared switch.

## 2. The same sign also controls allele sorting and potential trait viability

The high-allele selection operator is

\[
p_s=\frac{p(0.75+0.4q^+)}{1-p+p(0.75+0.4q^+)}.
\]

For interior `0<p<1`,

\[
p_s>p \iff 0.75+0.4q^+>1 \iff q^+>0.625.
\]

Likewise the pinned high-trait fitness is

\[
W(1;q^+)=0.5+0.8q^+,
\]

so potential high-trait viability at threshold one satisfies

\[
W(1;q^+)\ge1 \iff q^+\ge0.625.
\]

Therefore, away from the equality boundary,

\[
\boxed{
M>0
\Rightarrow
q^+>0.625,
\quad p_s>p,
\quad W(1;q^+)>1
}
\]

and

\[
\boxed{
M<0
\Rightarrow
q^+<0.625,
\quad p_s<p,
\quad W(1;q^+)<1.
}
\]

One signed margin therefore determines the one-step side of **three coupled biological coordinates** in the declared closure.

## 3. Exact repair wedge

Define the normalized eco-genetic bundle

\[
B=0.75T+0.25G,
\]

so

\[
S=0.6q+0.4B=q+0.4(B-q).
\]

The q-only route margin is

\[
M_0=a d q-H.
\]

Full feedback changes that margin by

\[
\boxed{M-M_0=0.4 a d(B-q)}.
\]

Hence direct eco-genetic feedback creates an exact **repair wedge** whenever

\[
M_0<0\le M.
\]

Equivalently, for positive `a*d`, a q-only state below the switch is rescued by full feedback iff

\[
\boxed{
B\ge B_{\rm crit}
=\frac{H/(ad)-0.6q}{0.4}.
}
\]

There is a symmetric suppression wedge when `M<0<=M_0`: a sufficiently low bundle can pull an otherwise above-switch q-only state below the next-step switch. Thus direct feedback is genuinely recoupling, not universally positive.

A rescue is impossible even at `B=1` if

\[
a d(0.6q+0.4)<H,
\]

which gives an exact limit to compensatory headroom.

## 4. Exact opening coverage–reserve trade-off

For the original four-patch matched-marginal construction,

\[
q=(0.65,0.75,0.85,0.95)
\]

and the common bundle values `(0.20,0.40,0.60,0.80)` are either aligned (`AA`) or reversed (`RR`). Initial population equals carrying capacity, so `d=1`. At generation 1,

\[
\theta_1=0.5025,
\qquad
H(\theta_1)=0.6160168053.
\]

The support and margin fields are exactly:

| condition | support S | route margin M | M>=0 patches | max M | min M |
|---|---|---|---:|---:|---:|
| AA | `.47,.61,.75,.89` | `-.1460,-.0060,.1340,.2740` | **2/4** | **0.27398** | -0.14602 |
| RR | `.71,.69,.67,.65` | `.0940,.0740,.0540,.0340` | **4/4** | **0.09398** | +0.03398 |

Both conditions have the same mean support `0.68` and therefore the same mean route margin `0.0639832`, but their support and route-margin variances differ **49-fold**.

This reveals an exact **coverage–reserve trade-off**:

- `RR` spreads shallow positive margin across all four patches;
- `AA` begins with only two positive-margin patches, but its strongest patch has almost three times the reserve of RR (`0.27398` versus `0.09398`).

So the opening relational difference is not merely “more versus less support”. It redistributes the same mean headroom between **how many patches are currently above the switch** and **how deep the strongest local reserve is**.

## 5. Frozen-state endurance benchmark

Under the locked forcing path

\[
\theta_g=0.50+0.0025g,
\]

if support and density are frozen only as an analytic benchmark, a patch with support `S` reaches zero margin at

\[
\boxed{
g^*(S)=\frac{S-0.50-0.1135168053}{0.0025}.
}
\]

The exact first positive integer generation with negative frozen-state margin is therefore:

- AA: `(1,1,55,111)`;
- RR: `(39,31,23,15)`.

Thus the shallow RR coverage is exhausted sequentially under the moving barrier, whereas AA's two strong reserves would remain above the switch beyond generation 40 if the opening state were frozen. At generation 40 the static support boundary is `0.7135168053`: RR's maximum opening support `0.71` is already below it, while AA still has opening supports `0.75` and `0.89` above it.

This is not a dynamic trajectory prediction. It isolates what the opening spatial organization alone contributes before sorting, recruitment, recoupling, density feedback and finite stochasticity modify the state.

## 6. How this closes the previously resolved operators

The exact margin organizes already established pieces:

1. **q-dependent allele sorting**: exact local sorting operator; its focused 6,000-pair deletion gives generation-40 DID `+6.883 pp`, 95% CI `[+5.800,+7.967]`.
2. **allele-linked recruitment buffering**: exact 50% trait–allele mismatch contraction; deleting it enlarges the reversed-state disadvantage by about `8–9 pp`.
3. **direct eco-genetic recoupling**: exact 40% q–bundle support-stage contraction; in the locked paired intervention family the reversed arrangement receives `+8.53 pp` and `+7.80 pp` loss-risk benefit at generations 20 and 40, with RR-minus-AA buffering-benefit DIDs `+7.93 pp` and `+6.33 pp`.
4. **density-feedback failure gate**: exact shrinking headroom `d*q >= theta+0.1135168053` in q-only and positive q->N->q loop; deleting `N->q` removes all generation-20 losses and cuts generation-40 risk by `57.47/59.60 pp` in AA/RR.

The new synthesis is that these operators alter a common moving route margin. The opening configuration chooses a coverage–reserve allocation; subsequent life-cycle operators then sort, repair or consume that margin through time.

## 7. Ecological interpretation

At a given patch and time, the margin can be decomposed into

\[
\underbrace{adq-H}_{\text{ecological/demographic headroom}}
+
\underbrace{0.4ad(B-q)}_{\text{recoupling contribution}}.
\]

The first term says how far the current interaction–density state lies from the moving forcing boundary. The second says how much the eco-genetic bundle repairs or suppresses that deficit before the nonlinear interaction update. Once the resulting q crosses the common switch, local allele sorting and potential trait viability change direction together.

This is the closest finite-model analogue to a “route flag”: it is an exact one-step switching condition, not an analogy to strategic game theory.

## Claim ceiling

`M` is exact for the declared transition, weights, trait fitness surface and high-allele selection closure. It is **not asserted as a universal natural state variable**, universal collapse threshold, or **long-horizon sufficient statistic**. The frozen-state crossing generations are benchmarks, not trajectory forecasts. Long-horizon functional fate remains generated by repeated updates, stochastic recruitment/drift, buffering and density feedback. Published natural systems remain ecological projections rather than validation of this margin.
