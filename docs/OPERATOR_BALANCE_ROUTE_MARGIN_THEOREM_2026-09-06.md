# Exact operator-balance route-margin theorem

Status: **exact one-step theorem for the declared finite closure**, now linked to the canonical prospective route-margin experiment and to the later fresh headroom-mediation and last-refuge-warning tests.

The theorem identifies the signed local coordinate that simultaneously determines the next interaction state relative to the shared switch, the direction of deterministic high-allele selection, and potential high-trait viability. It is not a fitted warning score and is not assumed to be a long-horizon sufficient statistic.

## 1. Route margin

The declared interaction update is

\[
q^+=\sigma\{\kappa(a d S-\theta)\},
\]

where `a=A/A_ref`, `d=min(1,N/K)`, and under the locked full-feedback weights

\[
S=0.6q+0.3T+0.1G.
\]

Let the shared switch be `c=q*=0.625`. Define

\[
H(\theta;c)=\theta+\frac{\operatorname{logit}(c)}{\kappa}
\]

and

\[
\boxed{M=a d S-H(\theta;c)}.
\]

For locked `kappa=4.5`,

\[
\frac{\operatorname{logit}(0.625)}{4.5}=0.1135168053,
\]

so at unit area ratio

\[
\boxed{M=d(0.6q+0.3T+0.1G)-(\theta+0.1135168053)}.
\]

Because the logistic map is strictly increasing,

\[
\boxed{\operatorname{sign}(q^+-0.625)=\operatorname{sign}(M)}.
\]

The canonical prospective audit checked **1,920,000 patch-generations** and found **0 sign mismatches**.

## 2. The same sign controls allele sorting and potential trait viability

The pinned high-allele selection operator is

\[
p_s=\frac{p(0.75+0.4q^+)}{1-p+p(0.75+0.4q^+)}.
\]

For interior `0<p<1`,

\[
p_s>p \iff q^+>0.625.
\]

The pinned high-trait fitness is

\[
W(1;q^+)=0.5+0.8q^+,
\]

so

\[
W(1;q^+)\ge1 \iff q^+\ge0.625.
\]

Away from equality,

\[
M>0 \Rightarrow q^+>0.625,\quad p_s>p,\quad W(1;q^+)>1,
\]

and all three inequalities reverse when `M<0`.

Thus one signed local margin determines the one-step side of three coupled biological coordinates in the declared closure.

## 3. Exact recoupling wedge

Define

\[
B=0.75T+0.25G,
\]

so

\[
S=0.6q+0.4B=q+0.4(B-q).
\]

The q-only margin is

\[
M_0=a d q-H.
\]

Full feedback shifts the margin by

\[
\boxed{M-M_0=0.4 a d(B-q)}.
\]

This is a **recoupling shift**, not a universally positive repair effect. When `B>q`, it moves the next transition upward relative to q-only; when `B<q`, it moves it downward.

An exact upward **recoupling wedge** occurs when

\[
M_0<0\le M.
\]

For positive `a*d`, the critical bundle is

\[
\boxed{B_{\rm crit}=\frac{H/(ad)-0.6q}{0.4}}.
\]

There is a symmetric suppression wedge when `M<0<=M_0`.

The later canonical long-horizon experiment is essential here: despite this exact one-step recoupling identity, direct full feedback **did not extend positive-margin refuge duration** in the fresh 12,000-trajectory test. The predeclared RR-minus-AA extension DID was **-0.677 generations**, 95% CI **[-0.6937,-0.6603]**, resolving the opposite direction. Therefore one-step recoupling and long-horizon refuge-duration benefit are empirically distinct claims.

## 4. Opening coverage–reserve trade-off

For the original four-patch matched-marginal construction,

\[
q=(0.65,0.75,0.85,0.95)
\]

and bundle values `(0.20,0.40,0.60,0.80)` are aligned in `AA` and reversed in `RR`. At generation 1, `theta_1=0.5025` and the density-one boundary is `0.6160168053`.

| condition | support S | route margin M | M>=0 patches | max M |
|---|---|---|---:|---:|
| AA | `.47,.61,.75,.89` | `-.1460,-.0060,.1340,.2740` | **2/4** | **0.27398** |
| RR | `.71,.69,.67,.65` | `.0940,.0740,.0540,.0340` | **4/4** | **0.09398** |

Both have mean support `0.68` and the same mean margin, but support and margin variances differ **49-fold**.

This yields an exact **coverage–reserve trade-off**: RR distributes shallow positive margin across all four patches, whereas AA has fewer initially positive patches but much deeper strongest-local reserve.

## 5. Frozen-state endurance benchmark

Under the locked forcing path

\[
\theta_g=0.50+0.0025g,
\]

if support and density are frozen only for an analytic benchmark, zero margin occurs at

\[
\boxed{g^*(S)=\frac{S-0.50-0.1135168053}{0.0025}}.
\]

The first positive integer generations with negative frozen-state margin are:

- AA: `(1,1,55,111)`;
- RR: `(39,31,23,15)`.

This is **not a dynamic trajectory prediction**. It isolates the opening spatial organization before sorting, recruitment, recoupling, density feedback and stochasticity alter the state.

## 6. Transition-exactness is not fate-predictiveness

The canonical prospective route-margin experiment preserved the exact one-step theorem but falsified two stronger shortcuts.

First, the predeclared direct-feedback refuge-duration interpretation resolved in the opposite direction, as above.

Second, the generation-20 binary marker `all four margins < 0` preceded every generation-40 loss but also fired in every non-event:

- pooled full-feedback events: 3,943/3,943 marker-positive;
- pooled full-feedback non-events: 2,057/2,057 marker-positive;
- sensitivity 1;
- specificity 0;
- binary AUC 0.5.

Thus an exact transition coordinate can saturate as a thresholded long-horizon marker.

The later prospective holdout resolved what remains informative: the **continuous depth of the strongest local margin before generation 10**, rather than the binary sign at generation 20, discriminated generation-40 functional fate with AUC 0.92734 and added ranking beyond co-timed maximum q.

## 7. Causal connection to sorting

A separate fresh 24,000-trajectory q-only follow-up tested whether the resolved q-dependent allele-selection edge changes the continuous last-refuge reserve itself. Both predeclared conditions passed:

- generation-40 endpoint DID `(RR-AA)_baseline-(RR-AA)_deletion`: **+0.0860**, 95% CI **[+0.07484,+0.09716]**;
- generation-20 maximum-headroom DID `(AA-RR)_baseline-(AA-RR)_deletion`: **+0.0007906**, 95% CI **[+0.0007038,+0.0008775]**.

This supports a bounded causal route `q-dependent allele sorting -> deeper continuous last-refuge reserve -> late functional fate` within the declared q-only closure. It is not a universal natural mediation law.

## Claim ceiling

`M` is exact for the declared transition, weights, trait-fitness surface and high-allele selection closure. It is **not asserted as a universal natural state variable**, universal collapse threshold, or **long-horizon sufficient statistic**. The frozen-state crossing generations are benchmarks, not trajectory forecasts. The generation-20 binary sign marker is explicitly non-discriminative in the canonical test. The positive continuous-warning result is specific to its frozen full-feedback holdout, observation time and endpoint. Natural systems remain ecological projections rather than validation data.
