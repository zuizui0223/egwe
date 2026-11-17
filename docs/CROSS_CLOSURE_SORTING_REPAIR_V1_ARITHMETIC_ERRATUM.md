# Prospective cross-closure v1 — arithmetic erratum (recorded before any outcome-summary inspection)

**First CI run:** https://github.com/zuizui0223/egwe/actions/runs/44011763582

## Failure location

The initial `run()` executed the frozen factorial and halted at the explicit
`Frozen denominator changed` assertion **before calling `analyze()` or writing
any outcome-summary, trajectory CSV or artifact**. No risk difference, effect
direction, AUC or other outcome statistic was shown or used to modify the design.

## Cause

The protocol froze **two closures × two AA/RR arrangements × two selection
strengths × two inheritance weights × six independent master seeds × 160
replicates = 15,360 trajectories**. The prose and
`replication.total_trajectories` had an incorrect arithmetic constant of
`7680` (exactly half the factorial). The full explicit parameter and seed
roster is internally self-consistent and remained unchanged.

## Correction without outcome-conditioned tuning

- Keep the original protocol JSON file byte-for-byte identical to its
  protocol-only freeze commit `efc3baa6868e705974235b35df70d1c3fee5b7a9`.
- Keep every named condition, its update rules, the six master seed keys,
  160 replicates per master and every first-passage endpoint and decision
  criterion **unchanged**.
- Compute the denominator from the immutable condition roster; require
  exactly 15,360 and explicitly record this erratum in the resulting
  summary and provenance.
- Retain the original failed CI record, do not reset the preregistration
  clock or claim that no trajectory was ever simulated; the first run
  calculated trajectories in memory but exposed **no endpoint summary**.
- Run the corrected *same* full factorial once; report all null, reversed,
  feasible or infeasible outcomes. No new parameter/domain search.

This correction fixes a counting error only, not a statistical test,
scientific prediction, effect size target or sign criterion. An independent
reader should cite both the immutable protocol and this erratum.

## Second technical failure (same immutable protocol)

[Run 44011968432](https://github.com/zuizui0223/egwe/actions/runs/44011968432)
executed and summarized the complete 15,360-trajectory roster in memory, then
failed when the report entrypoint expected two return values while the wrapper
mistakenly returned three (`summary, records, records`). No outcome estimates
were printed, exported or inspected, and the run produced no analysis artifact.
The source now returns exactly `(summary, records)` and a static unit test
checks that return tuple **before** the next full computation. This is a
structural code repair, not a change in predeclared parameters, event outcomes
or decision thresholds. Both failures remain public; a third repeated failure
requires diagnosing structural assumptions before any more repairs.
