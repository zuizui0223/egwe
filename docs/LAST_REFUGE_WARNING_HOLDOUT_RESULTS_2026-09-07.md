# Prospective last-refuge warning holdout — locked result

Status: **completed from a prospectively locked fresh holdout**.

## Question

Can a continuous last-refuge reserve discriminate later realised functional loss when marginal genetic erosion and saturated binary warning markers cannot, and does the full eco-genetic route margin add predictive ranking beyond the strongest local interaction state alone?

## Prospective provenance

The scientific protocol was frozen before implementation and before any holdout outcome at commit:

- protocol commit: `6377e684799bd4152eec057bfdb78143df0358fc`
- branch: `agent/last-refuge-warning-holdout`
- workflow run: `34130457262`
- job: `101769061070`
- artifact: `10022340904`
- artifact digest: `sha256:46a6b03d3d93a0fb5d03c2e9e27b087605b0cf5dda281fd27ed4581ab3640447`

The discovery ensemble from PR #162 was excluded. Holdout master seeds were `204701..204712`.

## Frozen design

- full-feedback `AA` and `RR` only;
- 12 entirely fresh master seeds x 500 replicates x 2 assignments;
- 12,000 trajectories total;
- observation at snapshot generation 9, immediately before the generation-10 update;
- target: realised all-patch high-trait loss by generation 40;
- no migration or mutation;
- no post-outcome threshold selection.

For each patch, the predeclared route margin was

\[
M_j=d_j(0.6q_j+0.3T_j+0.1G_j)-\left(\theta_{10}+\frac{\operatorname{logit}(0.625)}{4.5}\right).
\]

The primary risk score was `-max_j M_j`: lower strongest-refuge reserve means higher risk.

## Primary result — last-refuge reserve discriminates later functional loss

Across the 12 master-seed blocks, the continuous last-refuge route-margin AUC was

- mean AUC: **0.92734**;
- 95% CI: **[0.92433, 0.93035]**;
- pooled AUC: **0.92718**;
- AA AUC: **0.92526**;
- RR AUC: **0.92891**.

The lower confidence bound exceeds the prospectively frozen confirmation threshold `0.75`.

Only **44 / 8,028 = 0.548%** of eventual generation-40 losses had already occurred by the observation snapshot, below the frozen timeliness ceiling `5%`.

Therefore the candidate is prospectively confirmed as an **early functional-fate discriminator within the declared finite full-feedback closure**.

## Primary comparison — the eco-genetic margin adds ranking beyond current max-q

The co-timed current maximum interaction state alone was already informative:

- mean max-q AUC: **0.90598**;
- 95% CI: **[0.90078, 0.91118]**;
- pooled AUC: **0.90586**.

However, the paired master-seed-block AUC difference was

\[
AUC_{route\ margin}-AUC_{max\ q}=\mathbf{+0.02135},
\]

with 95% CI **[+0.01770, +0.02501]**. All 12 block differences were positive.

The predeclared incremental-ranking rule is therefore satisfied. The locked decision is:

`confirmed_route_margin_adds_ranking_beyond_q`.

This resolves an ambiguity left by the q-only exploratory analysis: under full feedback, density, trait and allele state contribute predictive ranking beyond the strongest local q alone.

## Frozen comparator performance

All scores were evaluated on the same observation snapshot and full event/non-event denominator.

| score | mean block AUC | 95% CI | pooled AUC |
|---|---:|---:|---:|
| continuous last-refuge route margin | **0.92734** | **[0.92433, 0.93035]** | **0.92718** |
| current max q | 0.90598 | [0.90078, 0.91118] | 0.90586 |
| current mean q | 0.88944 | [0.88327, 0.89561] | 0.88902 |
| mean population | 0.85010 | [0.84427, 0.85594] | 0.84976 |
| H_gamma | 0.86223 | [0.85357, 0.87090] | 0.86226 |
| H_alpha | 0.23253 | [0.22337, 0.24169] | 0.23232 |

The `H_alpha` result is **directionally inverted** relative to the predeclared lower-is-higher-risk score convention in this ensemble: event trajectories had higher mean `H_alpha` at the observation time than non-events, yielding AUC **0.23253** in the frozen direction. We do **not** flip its sign post hoc to manufacture a successful warning comparator. This does not alter the earlier frozen-threshold result; it records a recovered directional boundary and reinforces that marginal diversity state and functional-fate information are not interchangeable.

## Interpretation

The warning result now separates two ideas that were previously conflated:

1. **stress sensitivity** — marginal genetic erosion may occur early and even precede every loss, yet fail to discriminate events from non-events;
2. **fate information** — the continuous reserve of the strongest remaining local functional refuge can discriminate later system-wide functional loss.

The finite-model statement is therefore not “genetic warning fails.” It is:

> **System-wide marginal erosion is not sufficient fate information; later functional loss is better identified by the continuous reserve of the strongest remaining local eco-genetic refuge.**

The result also sharpens the state-sufficiency argument. Predictive information is relational and local: the route margin combines interaction state, density and the trait/genetic bundle in the patch with the greatest remaining reserve. Averaging those components, or tracking diversity erosion alone, discards part of the fate-relevant organization.

## Claim ceiling

This is a prospectively confirmed predictive-discrimination result **only for the declared finite full-feedback closure, forcing path, observation time and endpoint**. It does not establish a universal natural warning variable, universal AUC, natural collapse threshold, or portability across taxa, landscapes or timescales. Natural systems remain Discussion-level projections until independently measured.