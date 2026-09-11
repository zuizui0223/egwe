# EG-series submission status — 2026-09-08

This file is the current **operational submission-status source of truth**. It supersedes `EG_SERIES_SUBMISSION_STATUS_2026-09-05.md` for submission routing. Older status files remain historical provenance only.

## Decision now in force

There is **one active EGWE submission lane**: the Nature Ecology & Evolution flagship `manuscript/nee_flagship_article.md`.

The standalone EGWE state-validity and warning-validity manuscripts are **frozen fallback** packages. They remain scientifically and computationally reproducible, but they are not simultaneously submittable while the flagship is under consideration.

This routing change follows PR #165, merged on 2026-09-08 JST as `aa579f5262cf1403e4a6fc4e3937d64fbb1f2a80`. That merge turned the flagship from an optional synthesis spine into a complete load-bearing Article with its own cover letter, source manifest, figures, CI and prospectively locked evidence not contained in the old standalone lanes.

## Why this is not simply a fifth paper

The four-layer programme remains the scientific decomposition:

1. **EGC:** biological-state separation under fragmentation;
2. **EGWE state:** whether a representation preserves future-relevant distinctions;
3. **EGWE warning:** whether an early signal discriminates later fate;
4. **EGWEE:** whether a natural measurement earns state/proxy status before residual context is interpreted.

But the current submission execution is different. The NEE flagship is explicitly a **two-question paper**: Question 1 imports the EGC state-separation evidence, and Question 2 combines EGWE representation, operator and warning/reserve evidence. The state and warning fallback papers therefore cannot remain concurrently active, and EGC is not a separate active submission in this programme.

## Current route

| component | repository | current status | submission role |
|---|---|---|---|
| EGC | `zuizui0223/egc` | **load-bearing NEE Question 1 evidence source** | absorbed into the active NEE flagship; standalone manuscript retained only as provenance/fallback |
| EGWE NEE flagship | `zuizui0223/egwe` | **active primary submission** | **Nature Ecology & Evolution** |
| EGWE state validity | `zuizui0223/egwe` | **frozen fallback** | reactivate only after flagship is no longer under consideration and portability overlap is resolved |
| EGWE operator portability | `zuizui0223/egwe` | **package-ready development candidate; not yet authorised for submission** | independent Short Communication candidate; author/policy gate remains |
| EGWE warning validity | `zuizui0223/egwe` | **frozen fallback; evidence update required before reactivation** | must incorporate/report later last-refuge holdout before any standalone submission |
| EGWEE natural-data gates | `zuizui0223/egwee` | independent empirical programme | Ecological Indicators route remains separate |

## Portability is not orphaned

Freezing the state-validity manuscript would otherwise leave the process-portability result without a current publication owner. That was not intended. `manuscript/operator_portability.md` now owns the distinct question of whether a scalar connectivity label can be transported across allele-frequency mixing, whole-individual dispersal and pollen-only closures.

This is **not** a second active submission. It is a package-ready development candidate. The claim is deliberately separated from the flagship's alignment, sorting, buffering, recoupling, density-gate and last-refuge results. The evidence is explicitly counted as **one independent fresh replication plus two process substitutions sharing one historical reference ensemble**, not three independent replications. A deterministic precision audit bounds the non-significant equal-rate results: the present five-block designs have an 80%-power benchmark near `w=0.163` (about **8.1–8.2 pp weighted RMS block-rate deviation near p=.5**), so equivalence is not claimed. The submission-facing `operator_portability_short_communication.md`, references, highlights, cover letter, two figures, metadata, overlap audit and fail-closed bundle/CI are now materialized for ***Ecological Modelling* — Short Communication**. Actual submission remains blocked by author metadata/declarations, author approval, and a final live reference/overlap/journal-policy check.

## Evidence that changed the routing decision

The flagship reuses the former standalone evidence:

- state: exact next-transition difference `0.2543`; later propagation `+5.33` pp at generation 20 and `+5.20` pp at generation 40;
- warning: `35/35` and `33/33` event-side precedence paired with `48/48` and `49/49` non-event firings; specificity 0 and binary AUC 0.5.

It also contains evidence that is not merely a restatement of those papers:

- q-dependent allele-selection single-edge DID `+6.883` pp;
- prospectively locked sorting–headroom follow-up;
- exact operator-balance transition audit over `1,920,000` patch-generations with zero sign mismatch;
- prospectively locked continuous strongest-refuge route-margin AUC `0.92734` `[0.92433,0.93035]`;
- paired gain over co-timed max q `+0.02135` AUC `[+0.01770,+0.02501]`.

These results make the flagship scientifically stronger than an optional four-paper summary and make the old warning-only negative manuscript incomplete if presented as the full warning evidence base.

## Comparator-reporting correction

The locked last-refuge artifact contains the full predeclared comparator panel. Under the frozen orientation “lower state = higher later-loss risk”, co-timed `H_alpha` had AUC `0.23253`. This means the predeclared direction was strongly **directionally inverted**. We do not flip the sign post hoc and call it a successful warning. The value must remain visible in the flagship/result documentation as a recovered interpretation boundary.

## Exclusivity rule

While the NEE flagship is under consideration:

- do not submit the standalone state-validity manuscript;
- do not submit the standalone warning-validity manuscript;
- do not use their old cover-letter exclusivity language as though they were active submissions.

A fallback may be reactivated only after the flagship is withdrawn, rejected without transfer, or explicitly abandoned, and after author-controlled exclusivity/policy checks.

For warning validity specifically, reactivation additionally requires incorporating or explicitly reporting the last-refuge holdout and the `H_alpha` directional inversion. The pre-holdout pure-negative version is not current-evidence complete.

## What remains unchanged

No scientific protocol is reopened by this governance change. Frozen simulations, seeds, thresholds, endpoints, schedules, operator weights, natural-data gates and claim ceilings remain unchanged. `zuizui0223/egwee` remains the authoritative empirical-gate repository. The standalone EGWE manuscripts remain recoverable and reproducible as fallback packages.

## Next submission work

The scientific routing decision is now made. Remaining flagship blockers are author-controlled metadata, archive DOI/reviewer-accessible snapshots, live NEE policy recheck and portal submission. The fallbacks require no work unless they are later reactivated.
