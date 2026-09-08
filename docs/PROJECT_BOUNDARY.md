# Project boundary

## Relationship to `eco-genetic-criticality`

This repository is a successor project, not a continuation branch. The completed
repository remains the canonical record for its own declared finite closure.
This project may cite its design lessons, but it must not silently modify any of
its conclusions.

### Imported design principles

1. Keep potential trait viability, realised trait occupancy, allele persistence,
   and diversity statistics as separate states.
2. Preserve full state when transferring an H1-conditioned source into a
   fragmentation scenario; do not reconstruct a reduced proxy state.
3. Use a trait-loss-only calibration before inspecting H-alpha or H-gamma
   warning outcomes.
4. Hold out fresh master seeds for validation after calibration.
5. Retain source failures, projection failures, missing warnings, and missing
   trait-loss events as explicit records; do not silently drop censoring.
6. Distinguish Type S finite evidence from theorems, empirical findings, or
   biological parameter estimates.

### Not imported as a default claim

- No numerical outcome from the predecessor is evidence for this repository.
- The symmetric mutation rule is not assumed.
- The selected `ramp 30 + hold 90` schedule is not assumed.
- The H2-R selected domain is not assumed.
- A fixed absolute diversity threshold is not restored as a canonical rule.

## What counts as an extension

An extension must change at least one explicitly declared biological or
mathematical closure, such as:

- mutation directionality or state dependence;
- genotype-to-trait map;
- demographic regulation and carrying-capacity feedback;
- trait-dependent dispersal or migration;
- interaction-support deterioration mechanism; or
- the warning statistic itself.

Every extension needs a protocol that states its changed closure, unchanged
components, calibration outcome, validation outcome, and evidence label.

## Publication boundary inside this repository

The repository exposes **one active EGWE submission manuscript**, `manuscript/nee_flagship_article.md`. The standalone warning- and state-validity manuscripts are frozen fallback packages. They remain valid provenance/reproducibility surfaces but cannot be simultaneously submitted with the overlapping flagship.

The binding router is `manuscript/publication_lanes.json` (schema 4). Fallback reactivation requires the flagship to be no longer under consideration plus the author-controlled gates recorded there. In particular, the warning fallback must incorporate or explicitly report the later last-refuge holdout before reactivation.

`manuscript/main_text.md` is an integrated archive and `manuscript/grand_synthesis_flagship.md` is a superseded initial spine. Neither is an active submission.

## Prohibited shortcuts

This repository will not:

- tune a threshold, mutation rate, horizon, or schedule after inspecting warning
  success;
- report only trajectories with both events while omitting the censored
  denominator;
- treat a finite replicated result as a proof or empirical result;
- overwrite the predecessor's final ledger; or
- generalize from one selected domain to untested closures.
