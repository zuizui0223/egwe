# Can restoring population density stabilize an unexpressed high trait? Source-locked EGC factorial

**Frozen source-screen and experiment specification, 2026-10-28, before any new outcome receipt was inspected.** This is a mathematical and synthetic stochastic-life-cycle study. It is *not* a field-demonstrated ecological rescue, an anthocyanin gene-regulation study, or a confirmatory NEE manuscript endpoint.

## Where the parent study ended

PR #232 is merged in main. Source-fixed `egc@dd8ee379d0d3518194c767d16402042525bc00dc` results for 256 seeds/cell, 12 generations, all beginning without high-trait plants, showed that latent high-allele frequency p0=.40 supported more repeated and final high-trait occupancy than p0=.04, while changing initial q0=.20 to .80 did not yield a clear final advantage. At initial N0/K=.5, even q=p=1 is insufficient for the next high-allele fitness switch q1=.625 when current high trait is zero.

The exact pinned update is

\[
q_{t+1}=\sigma\!\left(4.5\left[d_t(0.6q_t+0.3T_t+0.1p_t)-0.5025\right]\right),
\]

where \(T_t\) is the **resident** high-trait mass and \(d_t=\min(1,N_t/K)\). At trait absence \(T_t=0\), a necessary and sufficient **one-step state** criterion is

\[
q_{t+1}\ge0.625
\quad\iff\quad
d_t(0.6q_t+0.1p_t)\ge
0.5025+\frac{\operatorname{logit}(0.625)}{4.5}
\approx0.6160168053.
\]

The threshold q1=.625 switches the source's selected high allele's relative fitness across 1 and source z=1 high-trait potential viability. It is NOT an absorbing persistence threshold for a natural population.

## One purpose, three prespecified axes, eight cells

Keep **source parameters fixed** to the established PR #232 one-patch stochastic life cycle, with initial zero high-trait-bin abundance, two-kernel recruitment, inheritance weight .5, no mutation, no migration, trait-grid size 101, q feedback 4.5 with weights .6/.3/.1, barrier .5025, K=40, and all other original default settings unchanged. The runner imports `source_params()` from merged PR #232 and changes **only `initial_population`** for the density intervention.

| Input factor | Values | Biological interpretation ceiling |
| --- | --- | --- |
| Initial q0 | **0.80, 0.98** | both high z=1 initial fitnesses exceed 1, but only .98 can satisfy the trait-absent next-q switch at p=.4 and full density |
| Resident allele p0 | **0.04, 0.40** | simulated standing high allele reservoir; not measured genetic capacity or a molecular mechanism |
| Initial N0 | **20, 40** | density .5 versus 1.0 at K=40; **also changes census abundance, demographic growth and finite drift**, so not a pure q-feedback intervention |

This yields exactly **2×2×2 = 8** combinations. Use **256 independent new seeds 70001–70256**, **12 generations**. Seeds are the same labels in every cell, and resampling must stay grouped by seed, but full stochastic RNG trajectories can diverge between cells. Previous 50001–50256 and other seed blocks are *excluded*.

### One-step analytical prediction, fixed before outcomes

There is **exactly one** initial trait-zero cell in which q1 meets 0.625:

- q0=.98, p0=.40, N0=40: at t=0 density is **d0=1.0**, with support .6×.98+.1×.4=.628, exceeding .6160168.
- q0=.80, p0=.40, N0=40: support .52, **fails**.
- q0=.98, p0=.04, N0=40: support .592, **fails**.
- All four N0=20 conditions: d0=.5, and support is at most .35, **fail**.

The source uses **density d0** to update q1; the computed N1 is used later in the recruitment multinomial. q1's crossing at one time point does not prove q2 is above 0.625 or later trait occupancy remains positive.

### Frozen endpoints and descriptive comparisons

Primary outcome for this follow-up is high-trait occupancy **at generation 12**, operationally `high_at_final_generation`. In addition, report `expressed_at_generation_1`, `three_consecutive_high_snapshots` (generations 1–3), and `ever_joint_trait_allele_zero`. For each cell report both q1 and q2 as state diagnostics. An earlier q1 switch can be followed by q2 decline if feedback/density conditions deteriorate.

Report four predeclared **N40 − N20** contrasts, one within every q×p stratum, for all four endpoints. Compute a *descriptive* 95% percentile interval by resampling **256 entire seed IDs as groups** within the eight-cell experiment for 2,048 bootstrap replicates (seed 20261028). Unlike the earlier PR #232's post-hoc contrasts, these comparisons are listed in advance. But the experiment itself was motivated by prior simulated outcomes and the design remains exploratory: do NOT treat these intervals as independent confirmatory evidence or multiply time points as independent replicates.

As a source-integrity gate, q1 from the original pinned EGC simulator must agree at machine precision with the independent algebraic `viability_gate(q0,p0,N0/40,T=0)` implementation. A test independently replays the original PR #232 parameters at q=.8,p=.04,N0=20 and checks identical q1, expression and final state.

## Interpretive decision rules

1. **If the sole q1-crossing cell has little long-run advantage**, record that achieving an immediate q switch is insufficient to stabilize the trait within the current stochastic closure. Do not move the threshold post hoc.
2. **If density 40 improves occupancy broadly**, report a composite **initial-population intervention**, not evidence that density-feedback alone causes recovery; increasing N also changes the number of recruited individuals and finite genetic sampling.
3. **If high p is the dominant modifier**, distinguish increased *probability of trait expression* from the separate possibility of self-sustaining feedback. A high simulated p is not proof that a lost biological flower color can reappear via a real genomic mechanism.
4. **If all cells frequently lose joint allele+trait state**, report closure of the model's recoverability window, not natural population extinction. Source population is floored at 1.
5. A one-patch experiment cannot establish H-R's across-patch matched-marginal spatial alignment mechanism and cannot support city/island generality.

## Execution/verification

New runner `scripts/egc_latent_support_density_factorial.py` uses only the exact external `egc` checkout and the merged PR #232 functions. Test fixture checks the eight-source-gate predictions, a source-pinned first-q match, a backward-compatible PR #232 cell, seed pairing and bootstrap integrity. GitHub Actions publishes the exact unrounded, per-seed synthetic result artifact. On completion, append a locked summary ledger with the run ID, source commit, all eight cell counts, N-contrast uncertainty and the q1/q2 mechanism interpretation.

This new branch does not edit the NEE flagship manuscript or replace its prior synthetic and natural-data evidential boundaries.
