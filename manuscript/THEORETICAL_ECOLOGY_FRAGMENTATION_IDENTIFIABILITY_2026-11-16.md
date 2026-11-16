# Fixed-area subdivision is not a configuration-only fragmentation effect
## Independent methodological audit — 2026-11-16

**Status:** exact algebra for the already declared canonical map plus a reviewer-facing causal estimand clarification. **No re-run, reparameterization, new seed, new ecological observation, figure alteration, threshold change or new submission lane.** The single active manuscript remains `theoretical_ecology_article.md`, routed to *Theoretical Ecology*.

### 1. What Question 1 actually intervenes on

The original gradient divides a fixed total area into `n=1,2,3,4,6,8,12,16` isolated equal patches and reprojects 1,037 supported source states. It fixes the summed area but necessarily changes **per-patch area** `A_n=A_tot/n` and the number of non-exchanging compartments. The reported disappearance of high-trait *potential viability* at every subdivision, together with persistence of realised occupancy, is a result for **this joint intervention and closure**.

This is **not** an independently identified effect of landscape configuration, connectivity, patch edge, or isolation at equal local patch area. It must not be described as a replicated estimate of a universal effect of fragmentation per se. The 1,037 projections reuse the same area-scaled operator, rather than representing independent ecological threshold mechanisms.

### 2. Model-exact canonical geometry

The declared canonical map is

```text
f_n(q) = sigmoid[kappa (A_n/A_ref * q - theta)]
A_n = A_tot/n
K_n = kappa A_n/A_ref = (kappa A_tot/A_ref)/n = K_1/n
```

For `q in [0,1]`, `f'_n(q)=K_n f_n(q)(1-f_n(q))<=K_n/4`.

* If `K_n<4`, `f_n` is a contraction on `[0,1]`, with one attracting fixed point.
* If `K_n=4`, the derivative is at most one and equals one only at an isolated argument, so the fixed-point equation cannot have three branches.
* If `K_n>4`, multiple fixed points become **possible** only for an appropriate forcing `theta`; this inequality alone does not prove bistability.
* If `K_1<=8`, **all** tested `n>=2` have `K_n<=4` in the canonical equal-area subdivision map. This last statement is conditional on `K_1`; we do **not** assert the source's actual `K_1` without its parameter provenance.

Crucially, lack of canonical bistability is **not logically equivalent** to failure of any high-investment trait-grid bin, low realised trait occupancy, loss of the entire population, or positive predictive warning. Those endpoints depend on different model components and were evaluated separately.

### 3. Causal estimand and feasible checks

Present evidence estimates response to the joint projection
`do(n, A_n=A_tot/n, exchange=0, original source projection)`.
It does not provide independent estimates of `do(exchange)`, `do(patch layout)` or `do(local interaction support)`. Total area alone being fixed is insufficient to claim identification of a single mechanism, especially because area explicitly enters the interaction operator.

A distinct, **new preregistered sensitivity campaign** would be needed to disaggregate mechanisms. At a fixed `n` and `A_tot`, compare (i) exchange operators across the same patches, (ii) alternative layouts/edges with equal patch-area distribution, and (iii) interaction support laws with the same demographic/source initialization. Predefine viability, occupancy, trait mass, functional loss and time horizon **separately** and do not select regimes using warning outcomes. This design is proposed only; no such results are claimed in the current manuscript.

### 4. Consequence for the flagship narrative

Question 1: under one explicit fixed-total-area **joint subdivision** and area-dependent feedback, potential support and realised occupancy separate. This is not a claim that patch geometry alone destroys viability.

Question 2: independently constructed matched-marginal states and prospective life-cycle interventions identify how **local cross-layer alignment and operator balance** affect subsequent transitions and fate. The paper does not claim that Question 1's subdivision produces the exact AA/RR arrangement used in Question 2.

Monitoring: the negative binary diversity thresholds and positive finite-closure continuous last-refuge holdout remain exactly as recorded. No numerical predictor, natural AUC or causal natural translocation implication is transported from this derivation.

### 5. Verified literature

* Fahrig L (2017). Ecological responses to habitat fragmentation per se. *Annual Review of Ecology, Evolution, and Systematics* 48:1–23. https://doi.org/10.1146/annurev-ecolsys-110316-022612
* Riva F, Koper N, Fahrig L (2024). Overcoming confusion and stigma in habitat fragmentation research. *Biological Reviews* 99:1411–1424. https://doi.org/10.1111/brv.13073

These sources distinguish landscape configuration from habitat-amount and patch-size confounding. They do not supply any new eco-genetic simulation result.
