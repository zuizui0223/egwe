# Last-refuge score-component decomposition — post-hoc exploratory audit

Date: 2026-10-06

Status: **post hoc / exploratory; not preregistered; not part of the locked primary comparator family.**

## Purpose

The prospectively locked holdout compared the continuous strongest-local route margin only against co-timed maximum interaction state, `max q`. After that outcome was opened, we decomposed the observed incremental ranking to ask whether the gain was attributable mainly to density or to the trait/genetic terms in the local eco-genetic support.

This audit does **not** modify the holdout protocol, add a new confirmatory comparator, or upgrade the original claim. It is a diagnostic decomposition of an already confirmed within-closure result.

## Independent full rerun

The complete last-refuge holdout was independently rerun for all 12 master seeds and all 12,000 trajectories. It reproduced the locked publication values to five decimal places:

| score | mean seed-block AUC | 95% CI |
|---|---:|---:|
| route margin, `max M` | 0.92734 | [0.92433, 0.93035] |
| co-timed `max q` | 0.90598 | [0.90078, 0.91118] |
| paired difference | +0.02135 | [+0.01770, +0.02501] |
| `H_alpha` under the frozen lower-is-higher-risk orientation | 0.23253 | — |

The rerun contained 8,028 generation-40 loss events, including 44 trajectories whose loss had already occurred by the observation snapshot, matching the locked result.

## Component decomposition

For each patch at the frozen observation state, define

[
S_j = 0.6q_j + 0.3T_j + 0.1G_j,
]

[
D_j = d_jq_j,
]

and the locked route margin

[
M_j = d_jS_j - left(	heta_{10}+rac{operatorname{logit}(0.625)}{4.5}ight).
]

The following comparisons were computed with the same 12 master-seed blocks and the same lower-score = higher-risk orientation:

| exploratory comparison | mean paired AUC difference | 95% CI | all 12 blocks positive? |
|---|---:|---:|:---:|
| `max(d*q) - max(q)` | +0.00618 | [+0.00513, +0.00722] | yes |
| `max(S) - max(q)` | +0.01915 | [+0.01512, +0.02319] | yes |
| `max(M) - max(d*q)` | +0.01518 | [+0.01189, +0.01847] | yes |
| `max(M) - max(S)` | +0.00220 | [+0.00148, +0.00292] | no |

The route-margin advantage over `max q` is therefore not explained primarily by density. The trait/genetic support terms account for most of the additional ranking, whereas density adds a smaller increment after support is included.

This is descriptive decomposition, not an additive variance partition: the maxima can be attained by different patches and the AUC contrasts are not algebraically additive.

## Patch identity and density state

The patch attaining `max M` was also the patch attaining `max q` in **90.8%** of trajectories. Thus, the improvement is usually a refinement of the same strongest local refuge rather than a wholesale switch to a different patch.

At the observation snapshot, every trajectory had `d < 1` in every patch. Density therefore remained active rather than saturated in this holdout, but its incremental ranking contribution was still much smaller than the contribution from adding the trait/genetic support terms.

## Structural boundary of the holdout

The holdout used `migration_rate = 0` and defined the endpoint as realised **all-patch** high-trait loss. Under this endpoint, the fate of the system is naturally governed by the last surviving local refuge, so a max-over-patches score is structurally aligned with the question. The result should therefore be read as:

> within the predeclared strongest-refuge framing, an integrated local eco-genetic margin ranks fate better than strongest-local interaction state alone.

It should **not** be generalized into a claim that max-type summaries outperform mean-type summaries for arbitrary endpoints or connected landscapes.

Initial conditions were also restricted to the two fixed AA/RR arrangements. The 12,000 trajectories are stochastic repetitions of those two state constructions, not a broad sample of arbitrary initial eco-genetic configurations.

## Exploratory interpretation of the H_alpha inversion

Under the frozen orientation, `H_alpha` was directionally inverted (AUC 0.23253). One mechanism-compatible post-hoc interpretation is that q-dependent sorting can drive local fixation inside the most functional refugia, lowering within-patch alpha diversity while preserving rather than undermining function. This is an exploratory interpretation only. The comparator remains a failed preregistered warning direction and its sign is not reversed post hoc.

## Reproducibility

Run:

```bash
python scripts/run_last_refuge_posthoc_decomposition.py \
  --summary posthoc_last_refuge_components.json
```

The script deliberately re-runs the frozen ensemble rather than editing the locked holdout output. It emits the component AUCs, paired seed-block differences, argmax agreement and density-saturation audit with an explicit `post_hoc_exploratory_not_preregistered` status.

The original locked holdout remains authoritative for confirmatory inference.
