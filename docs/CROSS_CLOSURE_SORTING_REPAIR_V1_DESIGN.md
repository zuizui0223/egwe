# Frozen prospective cross-closure test: mechanism direction under sorting versus repair

**Protocol ID:** `cross_closure_sorting_repair_v1` (see `experiments/cross_closure_sorting_repair_v1_protocol.json`). **Status:** model comparison prescribed before looking at new outcomes. This is a separate analytic extension and does **not** reopen the active *Theoretical Ecology* manuscript or its original finite simulation.

## Question

Can the **sign** of an alignment-related functional loss effect be forecast from the balance between local allele sorting and recruitment-mediated repair, or does the sign disappear when effective interaction is represented through explicit stochastic partner encounters?

## Predeclared paired experiment

All four patches begin with the same marginal distributions: q=(.65,.75,.85,.95), high-allele p and high-trait mass m each (.20,.40,.60,.80), assigned either aligned with q (AA) or in reverse order (RR), census N=40, identical partner availability .8, and no exchange. Two non-identical closures share allele selection, recruitment, viability, and finite demographic/trait/allele sampling: (A) an **aggregate-feedback analogue** related to the old eco-genetic model, and (B) a **partner-encounter limited model** with dynamic partner availability and stochastic observed visits. Neither is asserted to be a replay of original source code.

At fixed high-allele selection strength s∈{0,1} and resident inheritance weight h∈{.25,.75}, measure the risk difference RD=Pr(loss by g40 | RR) − Pr(loss | AA), and define D=(RD(s=1,h=.75)−RD(s=0,h=.75))−(RD(s=1,h=.25)−RD(s=0,h=.25)). A positive D suggests the sorting edge's contribution to arrangement differences is stronger with **weaker** allele-linked recruitment repair (higher resident h). This directional prediction is **motivated, not a theorem**; it can be false.

## Main decision and falsifiers

The result is called *cross-closure directional portability* only if **both** closures have a positive six-seed-block 95% CI for D and both point effects exceed 0.02. A negative effect in B is a sign failure; CI crossing zero is unresolved, not evidence of equivalence. Use six new independent master-seed blocks and 160 fixed replicates each; no additional seeds. The first all-patch absence of the realised focal high trait is the primary cumulative endpoint; a generation-40 quantitative interaction opportunity index is a secondary direct modeled readout (not actual seed production). At t10, compare the max joint-state score with contemporaneous max-q for future loss among not-yet-lost trajectories, but do not promote this secondary comparison to a new warning claim.

The two closures have different semantics and may produce uninformative event proportions. **Do not calibrate until one gives positive results.** Report nonidentifiability as such and retain adverse or null signs. The test is not a field study, does not confirm universal mechanisms, and is not itself publication approval.

## Provenance

This prospective text and JSON are committed **before** implementing or running the new trajectory engine. A separate run must pin the exact protocol-only commit and verify that its bytes are identical; a later outcome-opening changes neither this protocol nor its decision rule. Original evidence still belongs to the pinned EGC/EGWE programme, with natural analyses in EGWEE.
