# Route-duration versus endpoint persistence — same-ensemble post-hoc audit

Date: 2026-10-06

Status: **post hoc / descriptive; not preregistered; non-load-bearing.**

## Question

The prospectively locked route-margin experiment asked whether direct full feedback extends the number of generations retaining at least one nonnegative-margin refuge. That primary result resolved in the opposite direction:

- AA full minus q-only: **-0.323 generations**;
- RR full minus q-only: **-1.000 generation**;
- RR-minus-AA DID: **-0.677 generations** [−0.694, −0.660].

Earlier endpoint contrasts from a different locked intervention family had suggested that direct feedback can nevertheless reduce later realised functional loss. Because those results came from different prospective ensembles, they did not establish a within-experiment sign reversal.

We therefore performed a **post-hoc audit of the raw records from the same fresh 12,000-trajectory route-duration experiment**. No simulation, seed, condition, horizon, endpoint or route definition was changed.

## Same-ensemble endpoint result

Generation-40 realised functional-loss rates in the same four conditions were:

| state | full feedback | q-only | endpoint benefit, q-only minus full | seed-block 95% CI | all 6 blocks positive? |
|---|---:|---:|---:|---:|:---:|
| AA | 0.63333 | 0.66300 | **+0.02967** | [+0.00991,+0.04942] | yes |
| RR | 0.68100 | 0.72833 | **+0.04733** | [+0.02040,+0.07427] | yes |

Thus, **within the very same fresh ensemble**, full feedback shortened positive-margin refuge duration while reducing the generation-40 functional-loss rate.

The difference in endpoint benefit between RR and AA was +0.01767 with seed-block 95% CI [-0.02223,+0.05757]. The stronger claim that endpoint benefit was preferentially larger in RR is therefore **not resolved in this fresh ensemble**. The robust post-hoc result is the within-state sign reversal itself.

## Paired trajectory audit

Because all four conditions use the same trajectory seed within each paired key, outcome switches can be counted directly.

### AA

- q-only lost / full survived: **631**
- full lost / q-only survived: **542**
- among the 631 endpoint-rescued trajectories:
  - positive-margin duration shorter under full feedback: **182**
  - unchanged: **449**
  - longer: **0**

### RR

- q-only lost / full survived: **621**
- full lost / q-only survived: **479**
- among the 621 endpoint-rescued trajectories:
  - positive-margin duration shorter under full feedback: **621**
  - unchanged: **0**
  - longer: **0**

This is the sharpest descriptive result:

> **Every paired endpoint rescue occurred without any extension of the positive-margin refuge; in RR, every one of 621 rescues occurred despite shortening that duration by exactly one generation.**

## Interpretation

The route margin is exact for the next interaction transition relative to q*=0.625. The realised endpoint is different: all-patch loss of realised high-trait state by generation 40 after subsequent recruitment, selection, feedback and demographic dynamics.

The same-ensemble reversal therefore shows that:

> **one-step viability, threshold-duration endurance and long-horizon realised persistence are distinct biological estimands.**

A process can reduce final realised loss without prolonging the time for which any patch remains on the positive side of a one-step viability threshold.

This is not evidence that thresholds are unimportant. The route-margin sign remains exact for the declared next transition. It shows instead that **exact local transition status is not a sufficient compression of the later multi-operator trajectory**.

## Relation to the natural interpretation

This strengthens the reason not to equate connectivity, compensation or “repair” with one generic positive quantity. Different processes can improve different levels of the trajectory:

- immediate transition state;
- duration above a viability switch;
- realised phenotype persistence;
- final all-patch functional loss.

Urban and island examples therefore remain projections, not validation. Their useful role is to motivate measuring which process and which endpoint are being rescued rather than assigning one scalar “connectivity benefit”.

## Novelty boundary

Ecological transient-dynamics and resilience theory already establish that short-term and long-term stability measures need not agree, and that resistance, recovery and asymptotic persistence are non-substitutable. This audit therefore does **not** claim that short- versus long-horizon sign reversal is itself a new general ecological principle.

Its narrower contribution is mechanistic and within-closure: the same explicitly defined direct-feedback operator, in the same fresh paired ensemble, is associated with a shorter duration above an exact one-step viability switch while lowering final realised functional loss. The result identifies which stability summaries are non-interchangeable for this fragmentation life cycle and prevents the recoupling mechanism from being described as a generic extension of refuge duration.

## Inferential firewall

This analysis was opened only after the prospectively locked route-duration result was known.

Therefore:

- the preregistered route-duration primary remains **negative**;
- the endpoint comparison is **post hoc descriptive**;
- the post-hoc endpoint result does not replace or reclassify the primary;
- the RR-minus-AA endpoint-benefit DID is not promoted because its block CI includes zero;
- no new confirmatory claim is created.

## Reproducibility

Source artifact:

- workflow run: `34127034037`
- job: `101758021393`
- artifact: `10021317930`
- digest: `sha256:1e5ecb658a66e78ffa0ea7eb0cf073323a2173eca7c55461a11aa91b8bd4eb69`
- raw member: `records.json` (12,000 trajectories)

Run:

```bash
python scripts/summarize_route_duration_endpoint_sign_reversal.py \
  --records records.json \
  --output posthoc_summary.json
```

The committed compact summary is `artifacts/route_duration_endpoint_posthoc/posthoc_summary.json`.
