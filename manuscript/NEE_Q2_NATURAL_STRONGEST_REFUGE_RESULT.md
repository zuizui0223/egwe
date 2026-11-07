# Locked result — natural strongest-local-refuge test in intFlex

**Run date:** 2026-09-12  
**Workflow:** `intFlex natural Q2 confirmatory run`, run `34670582049`  
**Artifact:** `intflex-natural-q2-confirmatory`, artifact `10290847002`  
**Contract:** `NEE_Q2_NATURAL_STRONGEST_REFUGE_STAGE_B_CONTRACT.md`

## Decision

The preregistered primary decision is:

`no_detected_incremental_strongest_refuge_information`

The strongest current local pollinator interaction-support coordinate did **not** earn robust held-out predictive information about next-year patch occupancy beyond the locked marginal/current-state baseline.

This is a confirmatory null under the preregistered operationalization. It is not an access failure, model-identifiability failure, or post-hoc negative.

## Locked primary numbers

- source networks: **140**;
- source sites: **39**;
- retained consecutive site-year transitions: **75**;
- transitions excluded for current-year effort failure: **0**;
- candidate / identifiable held-out pollinator species: **123 / 123**;
- prediction rows: **4,411**;
- next-year occupancy prevalence: **0.1645885**;
- equal-species mean NLL, M0: **0.2185665286**;
- equal-species mean NLL, M1: **0.2182454431**;
- preregistered `delta_refuge = NLL(M1)-NLL(M0)`: **-0.0003210855**;
- species-bootstrap 95% interval: **[-0.0009824985, +0.0003421676]**;
- bootstrap draws: **10,000**;
- bootstrap seed: **20260912**.

The point estimate is in the predicted direction, but the preregistered positive gate required both `delta_refuge < 0` and the bootstrap 97.5th percentile `< 0`. The second condition failed.

## Secondary locked outputs

These outputs were prespecified as descriptive/secondary and do not alter the primary decision.

- persistence-only equal-species mean delta: **-0.0021722284**;
- colonization-only equal-species mean delta: **+0.0006574423**.

Transition-specific equal-species mean deltas:

- 2006→2007: +0.00256571
- 2007→2008: -0.00266383
- 2008→2009: +0.00120015
- 2011→2012: -0.00249336
- 2012→2013: +0.00119368
- 2013→2014: -0.00018253
- 2014→2015: +0.00043439

The strongest-refuge coordinate was highly correlated with the locked marginal predictors:

- `corr(Rmax, mean_support) = 0.8426`;
- `corr(Rmax, occupancy) = 0.8246`;
- `corr(Rmax, pooled_partner) = 0.8701`.

Thus the confirmatory question was genuinely an incremental-information test against a strong, collinear marginal baseline rather than a comparison against an intentionally weak model.

## Interpretation

This result does **not** externally validate the finite NEE strongest-refuge result. Under this natural operationalization, maximum current patch-level pollinator degree fraction did not add robust species-held-out information about next-year occupancy once current occupancy, mean support, pooled partner breadth, focal-patch support, plant richness, sampling effort and transition were supplied.

It also does not falsify every possible natural analogue of the finite route-margin statistic. The finite NEE coordinate is a mechanistically defined headroom-to-failure quantity, whereas `Rmax` here is a deliberately simple observational analogue based on current realized interaction degree. The preregistration forbids replacing it after seeing the result.

The persistence/colonization split is suggestive but remains secondary: the incremental direction was favorable for persistence and unfavorable for colonization. No post-hoc persistence-only paper-level claim is opened from this run.

## Consequence for NEE venue framing

The empirical programme now gives a sharper claim ceiling:

- **Q1 / state separation** remains the strongest portable natural prediction and is being tested independently in EGWEE's multilayer meta-analysis.
- **Q2 / strongest local refuge** has now received one genuine prospective natural test and did **not** pass its confirmatory incremental-information gate.
- Therefore the NEE paper should not imply that its strongest-refuge predictor is already supported as a general natural warning variable.
- The natural result is still useful because it converts an untested external-validity objection into a bounded empirical statement: one decade-long pollinator-network system was compatible with, but did not robustly support, incremental strongest-refuge prediction under a strict species-held-out design.

## No-rescue closure

Per the Stage-B contract, this result is closed. It will not be repaired by selecting common pollinators, the published 31 species, persistence-only rows, specific years/sites, another refuge quantile, weighted interaction strength, AUC, another regularization constant, or row-level cross-validation.
