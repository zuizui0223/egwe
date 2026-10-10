# Multigeneration sorting, allele-frequency saturation and network homogenization

**10 October 2026. Status:** independent mathematical extension after PR #223. The current result **does not supply a necessary/sufficient long-horizon functional-fate condition**, re-run frozen NEE simulations, or claim natural validation. The scope is a deterministic allele-selection/mixing component and an independent network interaction-mixing upper bound. It is not claimed that the matrix kernels are fitted to actual pollen, bee movement or plant dispersal.

The one-step result in `docs/ALLELE_SORTING_OPERATOR_THEOREM_2026-09-06.md` states that a pinned local selection operator gives
\[
u_i^+=u_i+h(q_i),\quad u_i=\operatorname{logit}p_i,
\qquad h(q)=\log(0.75+0.4q).
\]
Hence \(\operatorname{Cov}(q,u^+)-\operatorname{Cov}(q,u)=\operatorname{Cov}(q,h(q))>0\) for spatially variable q. That theorem is exact, but **u and p are different state coordinates**. Ordinary genetic migration averages *allele frequencies p*, not log odds u; moreover multi-generation fixation can remove frequency variation even while u differences keep growing. The present analysis resolves these distinct operations before asking whether a spatial signature survives.

## Theorem 1 — direction of the isolated selection edge under *actual* allele-frequency mixing

Fix n≥2 local interaction values \(q_i\in[0,1]\) and initial allele frequencies \(p_i\in[0,1]\). For any positive relative fitness function w(q), the deterministic frequency selection operator is
\[
S(p,q)=\frac{p\,w(q)}{1-p+p\,w(q)}.
\]

Let \(\bar q\) be the current patch mean. Compare two counterfactual selection calculations with **the identical pre-state, downstream mixing and follow-up observation**:

- **Full local edge:** \(s_i=S(p_i,q_i)\).
- **Common-q reference:** \(s_i^0=S(p_i,\bar q)\).

After selection, allele-frequency mixing and ecological interaction homogenization have rates m,r in [0,1]:
\[
p_i^+=(1-m)s_i+m\bar s,\qquad
q_i^+=(1-r)q_i+r\bar q .
\]

The control uses \(s_i^0\) and **the same** m, r and q⁺. Define the direct-edge covariance contrast
\[
D=\operatorname{Cov}(q^+,p^+)
-\operatorname{Cov}(q^+,p^+_0).
\]
Then the following identity is exact:
\[
\boxed{
D=(1-r)(1-m)\operatorname{Cov}
\!\left(q,\;S(p_i,q_i)-S(p_i,\bar q)\right).
}
\]

If w(q) is nondecreasing, then **D ≥ 0 for arbitrary heterogeneous initial p_i**. For q below the mean, the response to local versus common-q fitness is nonpositive; for q above it, the response is nonnegative. Thus every term \((q_i-\bar q)[S(p_i,q_i)-S(p_i,\bar q)]\) is nonnegative. For strictly increasing w, variable q, strictly interior p, and m,r both strictly below 1, D>0. If w is nonincreasing, D≤0. Full mixing in **either layer** (m=1 or r=1) sets D=0.

The calculation preserves correct **post-selection allele-frequency averaging**. It does not replace it with \(\operatorname{logit}(p)\) averaging, and neither mixing rate is automatically interpretable as whole-individual dispersal or pollinator movement. In particular, the common-q arm is a mathematical one-edge intervention, not a viable claim that nature randomly resets local ecological conditions.

**Crucial distinction:** this sign applies to the **isolated q-dependent selection edge**, not the total one-generation change \(\operatorname{Cov}(q^+,p^+)-\operatorname{Cov}(q,p)\). The latter can have the opposite sign due to pre-existing heterogeneity in the initial allele frequencies.

### Constructive failure of the “selection always raises frequency covariance” shortcut

Use EGWE's exact relative fitness \(w(q)=0.75+0.4q\), with two patches \(q=(0.7,0.9)\) and \(p=(0.5,0.999)\), m=r=0. Both local w values are **above 1** (w=1.03,1.11), meaning high alleles are selected upward in both patches. Yet:

| Quantity | Exact evaluated result |
| --- | ---: |
| Initial \(\operatorname{Cov}(q,p)\) | 0.024950000 |
| One-step \(\operatorname{Cov}(q,p^+)\) | 0.024585492 |
| Total covariance change | **−0.000364508** |
| Direct selection edge D relative to common-q control | **+0.000477635** |

The local edge still has the mathematically predicted **positive** causal covariance contribution; the total *p* covariance decreases because the high-q patch is already almost at allele fixation. This is a same-update-coordinate counterexample, not an empirical effect or a stochastic outcome.

## Theorem 2 — multigeneration fixation can erase \(p\)-covariance while log-odds sorting grows

Under constant, externally held \(q_i\) and strictly interior \(0<p_i(0)<1\), with **no mutation, no migration, no drift, and no recruitment feedback**, repeat only the local fitness update. The exact t-generation solution is
\[
\boxed{
u_i(t)=u_i(0)+t\log w(q_i),\qquad
p_i(t)=\sigma\big(u_i(t)\big).
}
\]

Therefore
\[
\boxed{
\operatorname{Cov}(q,u(t))=
\operatorname{Cov}(q,u(0))+
t\operatorname{Cov}(q,\log w(q)).
}
\]

For strictly increasing w and nonconstant q the slope is positive. But if **every** \(w(q_i)>1\), each local allele frequency converges to **1**; if all \(0<w(q_i)<1\), each converges to **0**. In either same-direction fixation/loss case, the actual allele-frequency covariance obeys
\[
\boxed{\operatorname{Cov}(q,p(t))\longrightarrow 0}
\]
even though the log-odds covariance may continue to grow linearly.

Proof of the frequency limit follows immediately from the logistic solution. A quantitative bound follows from the classical Grüss inequality \(|\operatorname{Cov}(X,Y)|\le \operatorname{range}(X)\operatorname{range}(Y)/4\). When every w>1,
\[
1-p_i(t)\le \frac{1-p_i(0)}{p_i(0)}w(q_i)^{-t},
\]
so
\[
|\operatorname{Cov}(q,p(t))|
\le \frac{\operatorname{range}(q)}4
\min\left\{1,\max_i\frac{1-p_i(0)}{p_i(0)}w(q_i)^{-t}\right\}.
\]
The analogous w<1 bound replaces \(1-p\) by p and the factor by \(\frac{p_i(0)}{1-p_i(0)}w(q_i)^t\).

With \(q=(0.7,0.9)\), \(p(0)=(0.5,0.999)\), the exact generated audit shows diminishing \(\operatorname{Cov}(q,p(t))\) toward 0 by generation 1,000, while \(\operatorname{Cov}(q,u(t))\) increases linearly. These generations are a **mathematical illustration**, not estimates of actual ecological generations or population persistence.

This answers one of the key mechanism questions: **sorting pressure can remain positive while the observable genetic frequency contrast disappears through saturation**. Consequently a natural observation of low standing neutral/frequency divergence does not establish that there was no current or previous selection; neither does growing log-odds contrast guarantee preserved function.

## Theorem 3 — network mixing and bounded regeneration of spatial state

Now separate ecological interaction q from allele-frequency p, and suppose n patches follow a nonnegative, **row-stochastic** spatial mixing kernel P:
\[
q_{t+1}=P q_t+\eta_t .
\]

Here \(\eta_t\) is an abstract local **spatial heterogeneity source**, which could stand for net effects of feedback/forcing only after those components are independently justified. The theorem assumes resulting q remains in [0,1], but does **not** constrain p's updating process beyond \(p_t\in[0,1]^n\). Define range \(R_t=\max_i q_{i,t}-\min_i q_{i,t}\).

The classical Dobrushin coefficient for **row-stochastic** P is
\[
\delta(P)=\frac12\max_{i,j}
\sum_k |P_{ik}-P_{jk}|\in[0,1].
\]

For all input vectors q,
\[
\operatorname{range}(Pq)\le\delta(P)\operatorname{range}(q).
\]
Adding \(\eta_t\) gives an exact general upper recursion
\[
\boxed{
R_{t+1}\le\delta(P)R_t+\operatorname{range}(\eta_t).
}
\]

Iterating,
\[
\boxed{
R_t\le \delta^t R_0+
\sum_{s=0}^{t-1}\delta^{t-1-s}
\operatorname{range}(\eta_s).
}
\]

Because every \(p_{i,t}\in[0,1]\), the same classical Grüss bound supplies
\[
\boxed{
|\operatorname{Cov}(q_t,p_t)|\le R_t/4\le
\frac14\left[\delta^tR_0+
\sum_{s=0}^{t-1}\delta^{t-1-s}R(\eta_s)\right].
}
\]

**Proof (nonuniform networks).** Each difference \((Pq)_i-(Pq)_j=\sum_k(P_{ik}-P_{jk})q_k\) has zero-sum weights because P is row-stochastic. Concentrating the positive coefficients at \(\max q\) and negative coefficients at \(\min q\) bounds its absolute value by half the row L¹ distance times \(R(q)\). Taking the maximum i,j gives the Dobrushin bound. The range triangle inequality yields the source term; induction and Grüss finish the proof. No linearization or threshold expansion is used.

**Meaning of the regimes:**

- If \(\delta<1\) and \(\eta_t\equiv0\), then **all frequency-scale q–p covariance must vanish asymptotically**, regardless of how the bounded p's are locally selected/mixed, because the ecological q spatial range vanishes.
- If \(R(\eta_t)\le\epsilon\) and \(\delta<1\), then
  \[
  |\operatorname{Cov}(q_t,p_t)|\le\frac14
  \left[\delta^tR_0+
  \epsilon\frac{1-\delta^t}{1-\delta}\right].
  \]
  The asymptotic **upper** level is \(\epsilon/[4(1-\delta)]\). This is **not** a lower bound on nonzero covariance: positive source heterogeneity merely makes persistence *possible*, not necessary.
- If \(\delta=1\), the bound supplies no mixing contraction; it does **not** prove association persists.
- A later functional survival or collapse event can behave independently of these covariance bounds if ecological life-cycle state, thresholds or stochasticity differ.

The proof covers *any* row-stochastic directed/heterogeneous mixing network, not just mean-field migration. The matrix moves a scalar **interaction state**, not necessarily a pollinator, whole plant, seed, gamete or paternal allele. That biological operator identity must be established separately from a real model or field dataset.

### How far this extends to feedback and recruitment

If a more complete local system has an ecological transition `q[t+1] = P f_t(q[t],p[t],trait[t],density[t],...) `, write
\[
\eta_t=P\left(f_t(q_t,p_t,\ldots)-q_t\right).
\]
The same bound is algebraically valid **conditional on knowing/controlling \(R(\eta_t)\)** and keeping q in [0,1]. It does NOT prove that any arbitrary positive sorting, recruitment or recoupling operator keeps \(\eta_t\) small enough to be erased or large enough to persist. Without those operator-specific Lipschitz/heterogeneity bounds, this is a **conditional decomposition**, not a universal persistence theorem.

A mathematically tractable sufficient condition for asymptotic q homogenization is \(\delta<1\) together with \(R(\eta_t)\to0\) sufficiently fast (or at minimum \(R(\eta_t)\to0\), by stability of the linear inequality); positive long-term heterogeneity is not guaranteed by a nonzero upper source bound. No claim of an exact universal critical migration threshold is licensed.

## Empirical and editorial interpretation

The results now distinguish *three* mechanisms of disappearance of an observed relational signal:

1. **Allele-frequency saturation:** local selection drives all p toward fixation or loss, despite continuing differences in per-capita/log-odds selection.
2. **Mixing of q across patches:** even an independently evolving allele-frequency state cannot maintain \(\operatorname{Cov}(q,p)\) when the ecological coordinate becomes spatially uniform.
3. **Measure choice and missing units:** a locality visit mean assigned to all individuals sets an apparent interaction variation to zero by construction (the separate PR #220 Ulex measurement-identifiability result).

Only the first two are actual life-cycle **mathematical dynamics**; the third is an observational/representation failure. They must not be conflated as causes of loss of future ecological function.

### Classical mathematical ingredients and priority

The covariance factorization, selection odds identity and exact counterfactual follow from algebra. The network range contraction uses the classic **Dobrushin ergodicity coefficient**, and the bounded-covariance consequence uses the **Grüss inequality**. We do not claim to invent these results. Relevant sources:

- [Rhodius (1997), Dobrushin coefficient and products of stochastic matrices, *Linear Algebra and its Applications*](https://doi.org/10.1016/0024-3795(95)00706-7).
- [Grüss's bounded covariance inequality and later discussion](https://link.springer.com/article/10.1186/s13660-015-0942-7).

The ecological contribution of this extension is a clear conditional mechanism map showing **when spatial state may be generated, saturated or diluted** under explicitly distinguished selection/mixing operators, and which tempting universal statements are false.

## Reproducibility and no-claim boundary

`scripts/multigeneration_sorting_mixing.py` uses only Python's standard library. It generates two-patch selection counterexamples, analytic up to 1,000-generation fixed-q trajectories, and 30-step heterogeneous-network mixing examples with and without additive heterogeneity source. `tests/test_multigeneration_sorting_mixing.py` checks the exact true-frequency mixing counterfactual, sign reversal under decreasing fitness, fixation-loss endpoints, Dobrushin constants, time-step bounds, kernel validation and non-support of future-fate claims.

This mathematical extension has **not** measured effective plant/pollen dispersal, run the original NEE simulator on a new seed ensemble, identified an ecological risk threshold, or shown the natural H-R hypothesis holds. It does not modify the active NEE manuscript or any frozen quantitative evidence. A genuine general **long-horizon fate** theorem would require explicit restrictions on the ecological/trait/demographic update, mutation, stochastic drift, recruitment and the functional endpoint; this document alone cannot provide one.
