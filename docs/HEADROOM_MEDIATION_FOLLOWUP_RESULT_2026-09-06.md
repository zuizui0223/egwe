# Prospective sorting–headroom–fate follow-up — locked result

Status: **resolved from a prospectively locked fresh-seed experiment**.

## Question

Does the already resolved local q-dependent allele-selection edge contribute to late functional fate by maintaining a deeper **continuous last-refuge headroom** through the demographic-density path?

This is deliberately narrower than a universal mediation claim. It asks whether the causal sorting edge changes the continuous route-reserve coordinate in the declared q-only closure and whether the endpoint effect replicates simultaneously.

## Prospective provenance

- protocol: `experiments/headroom_mediation_followup_protocol.json`
- prospective protocol commit: `07a5d792cf774f08d5495a5f50012b12753e87b4`
- scientific head: `2ef7b256192c63518c6d143e954dadd77527ec82`
- workflow run: `34029794984`
- artifact: `9988541984`
- artifact digest: `sha256:f8150ea9c7bc8e6e68aff3fbf3a572267204fc7882af11280f360f576fc01f2c`
- compact materialization: `artifacts/headroom_mediation_followup/locked_result.json`

Design: 12 entirely fresh master seeds x 500 replicates x AA/RR x baseline/deletion = **24,000 trajectories**. The only deleted edge replaced local q with spatial-mean q during allele selection; trait selection, recruitment, demography, density feedback, forcing and endpoint were unchanged.

## Exact coordinate

In the q-only closure,

\[
H_{tj}=d_{tj}q_{tj}-\theta_t-\frac{\operatorname{logit}(0.625)}{4.5}.
\]

`H>0` iff the next q is above 0.625, which is also the sign switch for deterministic high-allele selection. The predeclared mediator was **maximum patchwise H at generation 20**.

## Two predeclared requirements both passed

### 1. Late endpoint replication

Primary generation-40 loss DID:

\[
(RR-AA)_{baseline}-(RR-AA)_{delete\ local\ allele\ selection}
=\mathbf{+0.0860}.
\]

95% paired CI: **[+0.07484,+0.09716]**, `n=6,000` paired keys.

Thus the single-edge endpoint effect replicated on a new, larger seed ensemble.

### 2. Continuous last-refuge headroom mediator

Primary generation-20 max-headroom DID:

\[
(AA-RR)_{baseline}-(AA-RR)_{deletion}
=\mathbf{+0.0007906}.
\]

95% paired CI: **[+0.0007038,+0.0008775]**, `n=6,000` paired keys.

Deleting local q-dependent allele selection therefore removed a small but extremely precise AA-versus-RR advantage in the **depth of the strongest remaining q-only refuge**.

The locked decision was:

`resolved_selection_headroom_fate_pathway`.

## Why the small headroom effect is biologically meaningful in the finite closure

The headroom coordinate is measured on the density-weighted support scale immediately before a steep logistic interaction update. Its absolute numerical size is therefore not comparable to a percentage-point endpoint effect. The important evidence is directional and paired: the same single-edge deletion that removes the late functional-fate contrast also removes the continuous strongest-refuge advantage on a fresh ensemble.

The positive-headroom **count** was already saturated by generation 20 (`DID=0`), whereas continuous max headroom remained different. This is exactly the representation distinction later exploited by the last-refuge warning holdout: binary route status can lose information while continuous reserve depth remains informative.

## Secondary trajectory pattern

The max-headroom baseline-minus-deletion DID remained positive at every predeclared readout:

- g5: +0.0005630
- g10: +0.0006849
- g20: **+0.0007906**
- g40: +0.0006756

The mean-population DID also grew in the same direction, reaching +0.0862 individuals at g20 and +0.0874 at g40 on the patch-mean scale. These are secondary readouts; the primary mediator remains g20 max headroom.

## Mechanistic consequence

Together with the earlier exact allele-sorting theorem and focused single-edge endpoint proof, this fresh follow-up supports the bounded chain

`local q-dependent allele sorting -> deeper continuous last-refuge reserve -> later functional fate`.

This does **not** mean headroom alone mediates the entire endpoint effect, nor that the path is universal in natural systems. Recruitment buffering and density feedback remain active in the q-only closure, and full-feedback recoupling changes the route coordinate differently.

## Relation to the full-feedback warning result

This experiment is the discovery/provenance source for the later independent PR #163 holdout; none of its seeds were reused there. The later holdout tested a more complete full-feedback margin combining q, density, trait and allele state and confirmed prospective fate discrimination with AUC 0.92734.

The combined interpretation is therefore causal plus predictive:

- q-dependent allele sorting changes the continuous reserve coordinate;
- continuous reserve measured early can predict later loss;
- thresholded/saturated versions of the same coordinate need not discriminate fate.

## Claim ceiling

The result supports selection-to-headroom-to-fate propagation **only in the declared finite q-only closure**. It is not a formal natural-system mediation analysis, does not identify a universal threshold or effect size, and does not make H a sufficient long-horizon predictor. Natural systems remain Discussion-level projections until the corresponding processes are measured directly.
