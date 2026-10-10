# Which plants should receive scarce visit cameras? An exact minimax identification design

**10 October 2026 — mathematical / synthetic design only.** This result extends `docs/RELATIONAL_VISIT_GRAIN_IDENTIFIABILITY_2026-10-10.md`. It has **not** used observed Ulex/Asclepias/Cirsium visitor counts, nor any subsequent reproductive outcomes. It does **not** validate H-R or establish biological field efficacy.

## 1. Field problem and estimand

Suppose a sampling design truly enumerates n tagged plants *within the same site and time window*, measures an individual pre-outcome state `g_i` (genetic or trait score, with its biological origin explicitly identified), positive observation efforts `e_i`, the complete visit total V across exactly those n plants, and **pre-outcome** defensible visit caps `u_i`.

A limited number of camera stations can be assigned to a subset S of tagged plants. For a camera-monitored plant i, the idealized event count `v_i` is learned exactly. Unmonitored counts are unknown but must satisfy `v_i >= 0`, `v_i <= u_i`, and `sum(v_i)=V`. The target is the empirical covariance at plant grain

\[
C=\frac1n\sum_{i=1}^{n}(g_i-\bar g)\frac{v_i}{e_i}.
\]

This is **not** a future reproductive outcome and is **not** an estimate of visitation effectiveness, pollen deposition or genetic effects. It measures how current counted visits and a pre-observed state *could* be locally aligned when the full census membership assumption holds.

## 2. Exact worst-case design, not sampling after seeing outcomes

For a proposed monitored set S, set

\[
w_i=\frac{g_i-\bar g}{n e_i},\quad
R=V-\sum_{i\in S}v_i .
\]

Once exact camera counts on S have been observed, their contribution \(\sum_{i\in S}w_i v_i\) is known. The remaining covariance interval width is

\[
W_S(R)=
\max_{\{v_i\}_{i\notin S},\ \sum v_i=R}\sum_{i\notin S}w_i v_i-
\min_{\{v_i\}_{i\notin S},\ \sum v_i=R}\sum_{i\notin S}w_i v_i .
\]

With the prespecified visit caps, the remaining total R **before cameras run** can lie anywhere in

\[
R\in[\max(0,V-\sum_{i\in S}u_i),\ 
        \min(V,\sum_{i\notin S}u_i)].
\]

The **minimax camera allocation** is

\[
S^*=\arg\min_{|S|=k}\ \max_R W_S(R).
\]

The exact maximum does *not* require enumerating possible future visit counts. For each fixed S, the lower and upper covariance bounds are continuous piecewise-linear in R, with breakpoints at cumulative caps when unmonitored units are sorted in ascending or descending w. Hence the maximum of their difference occurs at one of those finitely many breakpoints or the feasible R endpoints. The script tests every subset of cardinality k and every required breakpoint; each result is therefore *globally minimax optimal* under the declared assumptions (until the preset search-complexity limit, in which case it stops rather than reporting a heuristic as exact).

Proof sketch: for either bound, if a candidate optimum allocates positive visits to a lower-priority weight while a higher-priority unit is below its cap, moving mass between them increases the objective while respecting feasibility. Thus greedy extremal allocations are sharp. The piecewise-linearity result then follows because the active set only changes when a unit fills its cap.

This is a robust **uncertainty-width criterion**, not an expected biological-information objective. No assumed probability distribution of visit counts or response values is smuggled into the design.

## 3. Executable, fully synthetic results

All numeric states/counts here are **invented mathematical examples**, not published Ulex measurements or a five-camera field pilot.

### Four tagged plants; total visit count 20; each count capped at 8

State score `G=(0.1,0.3,0.7,0.9)`, equal effort.

| Camera budget | Best worst-case residual covariance width | Robust selection |
| ---: | ---: | --- |
| 0 | 2.0 | no plant-specific observations |
| 1 | 1.2 | lowest-score or highest-score plant |
| 2 | **0.4** | the two lowest-score **or** the two highest-score plants |
| 3 | 0 | any three plants, because total counts are known |
| 4 | 0 | full census |

The **two extreme plants** (lowest and highest) are not optimal for k=2: their worst-case width is 0.8, twice the optimum of 0.4. The intuitive rule "monitor the two endpoints of G" therefore need not minimize what remains unidentified. With only a bounded visit total and equal caps, the best robust subset can lie on one **same-side tail** of a trait gradient.

### Eight tagged plants, five hypothetical camera stations

With eight invented plant scores `(0,0.143,0.286,0.429,0.571,0.714,0.857,1)`, common per-plant cap 8, visit total 40, and five perfectly synchronized individual-visit counters:

- Baseline width before monitoring: **2.142**.
- Exact minimum of the worst-case width after five measurements: **0.285**.
- One minimax plan: **P01, P02, P03, P07, P08** (ties exist).
- This does **not** mean five real cameras can capture all visits within an eight-plant population. The complete same-window total V must be independently counted or otherwise justified; only then is the bound usable.

The exact script emits all competing candidate sets, the minimax-optimal tied sets, a possible worst-case residual visit total, the pre/post widths, and the synthetic-only provenance. Exhaustive small-integer allocation tests confirm the output against all compatible complete visit vectors, including unequal effort. For continuous counts and caps, the proof relies on the breakpoint argument above.

## 4. Requirements before using this for a real pollinator-camera design

**Hard source/coverage gate:** A global V is usable *only if it covers exactly the same tagged plants and observation window* as the individual g/effort records. A locality-wide flower census that samples unknown plants (such as the Ulex archive) does not meet this assumption. Do not put its observed count into this algorithm and call the resulting bounds an empirical result.

**Hard camera gate:** Exact counts in this derivation mean independently validated, direct pollinator visits to the *tagged focal plant*, with true zero-visit observation windows and equivalent effort. Camera event detections are not automatically true visits: detection probability, false positives, skipped frames, overlapping flower heads and unobserved flowers create interval or probabilistic uncertainty. The current algorithm does **not** account for that measurement error; this is a blocking stage before field inference.

**Other necessary checks:**

- Tag `site_id / patch_id / plant_id / cohort` and co-register the genetics/traits, cameras and later seed/recruitment observations using the separate field contract in `artifacts/design/relational_visit_grain_contract_20261010.json`.
- Prespecify genetic/trait score orientation and caps from genuine prior biological/physical information. Do **not** derive them from a later seed/fruit response. Genotype must refer to a validated assay or independently justified trait; an evolution-treatment label is not automatically a molecular genotype.
- Source animals should be classified at least by ecologically meaningful functional group when inference depends on different per-visit efficacy; one aggregate visit counter is insufficient to claim pollen transfer.
- Cameras/flowers/individual SNP sites are repeated measurements; **independent replication is across whole sites, spatial landscapes or properly independent cohort-years**, not 5 camera stations.
- For a true H-R generalization, continue to a genuine *future* independently held-out ecological function after complete pre-outcome state measurement. A positive visit–G covariance cannot establish a successful fate forecast on its own.

## 5. Outputs and falsifiable next measurement

`python scripts/plan_visit_monitoring.py --output synthetic_monitoring_placement.json` saves two **synthetic** design cases and explicit no-ecological-fit flags.

The **next physical task** is not re-running different archive URLs: before field deployment, register candidate tagged plants and existing assay-defined g (or a biologically justified pre-outcome trait), show that the same-window total census is possible, and calibrate each camera's detectable flower coverage and event counts against human-annotated true visits. If only camera counts on some plants are available but no global V, **this particular sharp-covariance design does not apply**. A separate detection/missing-total identification model is needed rather than substituting site means.

Even a successful real partial identification result would remain independent of the existing NEE finite-model thresholds, the zero-specificity historical genetic warning, and the natural strongest-refuge null. Nothing here updates those scientific locks.
