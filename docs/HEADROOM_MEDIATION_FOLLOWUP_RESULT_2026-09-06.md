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

## Later descriptive scale audit (post hoc)

The preregistered DID and CI above are unchanged. A later audit of the immutable 24,000-trajectory workflow artifact was used only to describe magnitude on the observed generation-20 headroom scale.

- pooled raw SD of generation-20 maximum headroom: **0.0039362**;
- pooled within-cell SD: **0.0039295**;
- DID / pooled raw SD: **0.2009 SD**;
- paired-key DID SD: **0.0034323**, giving a paired standardized effect of **0.2303 SD**;
- positive-headroom patch count at generation 20: **0 in all 24,000 trajectories**.

Thus `+0.0007906` is a small-to-moderate shift relative to contemporaneous headroom variation, not a large absolute reserve shift. By generation 20 every trajectory was already below the `H=0` branch boundary; the resolved effect is a difference in **continuous depth below that boundary**, while the binary route-status count contains no variation. This scaling is post hoc and descriptive and does not alter the prospectively locked mediator test.

Machine-readable values are in `artifacts/headroom_effect_scale/posthoc_summary.json`; they can be regenerated from the locked workflow `records.json` with `scripts/summarize_headroom_effect_scale.py`.

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
