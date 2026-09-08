# Matching eco-genetic summaries can hide different ecological futures

# FROZEN FALLBACK — NOT FOR SIMULTANEOUS SUBMISSION

> The state/propagation results below remain scientifically valid. Their load-bearing representation and horizon-propagation evidence is reused by the active NEE flagship. Process-portability prose is retained here for provenance, but current portability claim ownership is routed to `operator_portability.md`. Any later reactivation of this fallback must first resolve that overlap and can occur only after the flagship is no longer under consideration.


**Publication status:** frozen fallback, not for simultaneous submission. This manuscript historically combines the constructive joint-state, exact next-transition, propagation-horizon, and process-portability results. Its state/propagation evidence is reused by the active NEE flagship; current process-portability development ownership is routed separately in `publication_lanes.json`. Natural systems are used only as ecological background and discussion anchors; they are not treated as external validation of the finite closure. The manuscript does not claim validated predictive genetic warning.

## Abstract

Ecological state variables are often compressed into abundance, interaction, trait and genetic summaries before prediction. We ask when such compression is dynamically valid. For a declared finite multipatch eco-genetic closure, we formalize transition sufficiency and construct two states with identical census, interaction, allele-frequency and trait marginals, `H_alpha`, `H_gamma` and `F_ST`, but opposite cross-layer spatial alignment. Their exact one-generation interaction transitions differ by as much as 0.2543, proving that the coarse representation cannot determine the next transition. A separately prospectively locked 1,500-pair experiment shows that this hidden state distinction later produces approximately five-percentage-point differences in functional-loss risk at generations 20 and 40. Process-specific tests further show that a common scalar connectivity label does not identify distinct movement operators. State representation is therefore a mathematical property of the declared transition and prediction target, not of familiar summaries alone.

## Introduction

Ecological prediction begins before a forecasting algorithm is chosen: it begins with deciding what counts as the present state. If that representation merges biologically different configurations that have different transitions, no downstream model can recover the information already discarded.

This problem is ecological as well as mathematical. Population persistence, realised ecological function, interaction support, mating opportunity, genetic diversity and trait occupancy can respond on different schedules. Interaction-dependent function can weaken before numerical disappearance, while movement or partner reorganization can sometimes compensate local resource loss. Conversely, standing genetic summaries can retain historical information after contemporary interaction or mating processes have changed. These observations motivate a state description based on future-relevant organization rather than on a single disturbance label or a collection of marginal quantities.

Forecasting theory emphasizes explicit prediction targets and horizons (Clark et al. 2001; Petchey et al. 2015; Dietze et al. 2018), and multilayer ecology shows that interlayer organization can matter beyond within-layer summaries (Pilosof et al. 2017). Fragmented eco-evolutionary systems add a further complication because dispersal, interaction, demography and inheritance are represented by different biological operators (Legrand et al. 2017; Govaert et al. 2019). The same numerical value attached to two operators need not mean the same ecological state.

Natural systems make the issue concrete without serving as tests of the model developed here. In urban *Crepis sancta*, reduced local flowering density was associated with reduced pollinator activity and reproduction despite nonzero wider movement (Cheptou & Avendaño 2006; Dornier & Cheptou 2013). On Miyake-jima, volcanic damage reduced local floral resources, but broader *Zosterops* movement and pollen mixing compensated pollination and next-generation mixing (Abe & Hasegawa 2008; Abe et al. 2013). In fragmented *Conospermum undulatum*, contemporary pollen connectivity and reproduction deteriorated while adult neutral genetics retained historical connectivity (Delnevo et al. 2019, 2021, 2026). These examples motivate a general question: which aspects of an ecological configuration must be retained if the state is to determine its future?

We address that question mathematically and numerically. First, we define transition sufficiency for a coarse state representation and give a constructive counterexample in which all declared marginal summaries agree but the exact next transition differs. Second, a separately prospectively locked paired experiment tests whether the same hidden distinction propagates to a later functional-loss endpoint. Third, operator-specific tests ask whether a scalar connectivity label can be transported across distinct movement closures. The paper therefore tests state representation directly; natural examples are used only to interpret why the mathematical distinction matters ecologically.

## Methods

### Complete state, coarse representation and transition sufficiency

Let `X` denote the complete explicit state of the declared finite closure at a fixed time, together with the fixed future forcing required to evaluate the next deterministic interaction update. Let

\[
\phi:X\rightarrow Z
\]

be a coarse representation containing the summaries normally retained for analysis. In the constructive test, `phi(X)` contains habitat area, patch and total census, the interaction-state multiset, allele-frequency multiset, realised high-trait-mass multiset, complete trait-bin totals, `H_alpha`, `H_gamma`, and `F_ST`.

Let

\[
T_I:X\rightarrow Q
\]

be the exact one-generation interaction transition under the declared local interaction map. We call `phi` **transition-sufficient for `T_I`** if there exists a map

\[
g:Z\rightarrow Q
\]

such that

\[
T_I=g\circ\phi
\]

for every admissible state under the declared closure. This definition is deliberately local and exact: it asks whether the retained representation uniquely determines the next interaction field. It does not assert that the complete simulator is a universal model of ecological state.

**Proposition 1 — constructive non-sufficiency certificate.** If two admissible states `X_A` and `X_B` satisfy

\[
\phi(X_A)=\phi(X_B)
\]

but

\[
T_I(X_A)\ne T_I(X_B),
\]

then `phi` is not transition-sufficient for `T_I`.

**Proof.** If `phi` were transition-sufficient, some `g` would satisfy `T_I=g∘phi`. Equality of `phi(X_A)` and `phi(X_B)` would then force `T_I(X_A)=T_I(X_B)`, contradicting the constructed pair. Therefore no such `g` exists. ∎

The empirical burden is therefore reduced to a constructive one: exhibit an admissible pair with identical retained summaries but different exact transitions.

### Aligned and anti-aligned constructive pair

We constructed two two-patch states that hold every component of `phi` fixed while reversing the patchwise alignment between interaction support and the genetic/trait-support bundle. The layer-wise marginals are therefore identical by construction, while cross-layer covariance changes sign.

For the opening certificate, the aligned support signal was

`[0.47, 0.61, 0.75, 0.89]`,

whereas the anti-aligned signal was

`[0.71, 0.69, 0.67, 0.65]`.

The corresponding exact generation-1 interaction fields were

`[0.46350, 0.61863, 0.75283, 0.85116]`

and

`[0.71784, 0.69925, 0.68000, 0.66010]`.

Cross-layer covariance was `+0.025` in the aligned state and `-0.025` in the anti-aligned state. The primary exact certificate is the maximum patchwise difference between the two generation-1 interaction fields.

The exact one-generation certificate was evaluated before a long-horizon outcome was inspected. A single preregistered 60-generation deterioration schedule then compared 500 paired aligned and anti-aligned trajectories. No warning endpoints, replacement seeds, alternative alignment permutations, or altered schedules were opened after the result.

For the paired generation-60 loss contrast, the estimand is anti-aligned minus aligned risk. With 114 aligned-no-loss/anti-loss pairs, 92 aligned-loss/anti-no-loss pairs, and 500 total pairs, the observed paired difference is `(114-92)/500 = 0.044`. A paired large-sample 95% interval uses the variance of `D in {-1,0,1}`, giving approximately `[-0.012, 0.100]`. Relative to the aligned baseline risk of `0.678`, the upper confidence limit corresponds to about a **14.8% relative increase**. This interval is descriptive for the locked campaign and is not a post-result acceptance rule. **Non-significant tests do not establish equivalence.**

### Horizon-specific propagation experiment

After the original state-pair result had been frozen, a separate propagation protocol was locked before its outcomes were opened. It did not change the state values, forcing law, or original result. It extended only readout horizons and paired replication.

Each aligned/anti-aligned pair was followed once to generation 40 under the original linear deterioration rate, truncated rather than rescaled. Outcomes were read at generations 5, 10, 20 and 40. Five master seeds and the original deterministic pair-seed mapping were retained. Nested prefixes of 500, 1,000 and 1,500 paired trajectories were precision diagnostics; the 1,500-pair curve was primary.

For horizon `h`, let `Y_h(X)` indicate realised functional loss by that horizon. The paired experiment estimates

\[
\Delta_h=P[Y_h(X_B)=1]-P[Y_h(X_A)=1]
\]

under the one declared deterioration path. This does not prove a universal horizon law. It tests whether the exact one-step distinction identified by Proposition 1 remains consequential for a coarser later endpoint.

### Operator-specific representation tests

A separate representation problem concerns biological operators. The historical allele-frequency mixer was

`p_i'=(1-m)p_i+m*p_bar`.

It is an allele-frequency composition operator, not demographic movement, whole-individual dispersal, pollen flow, seed dispersal or pollinator movement. One preregistered fresh ensemble retested its historical `m=.10` pattern. Distinct fixed closures then represented post-recruitment whole-individual dispersal and paternal pollen-only gene flow. A matched-expected-support experiment separately compared constant and temporally varying partner architectures.

These tests ask whether one scalar label can be treated as a common state coordinate across different transition maps. They do not test whether movement, gene flow or rewiring is ecologically unimportant.

## Results

### The declared coarse state is mathematically not transition-sufficient

By construction,

\[
\phi(X_A)=\phi(X_B).
\]

The aligned and anti-aligned states therefore agree in habitat area, census, interaction, allele-frequency and trait marginals, complete trait-bin totals, `H_alpha`, `H_gamma`, and `F_ST`. Nevertheless, their exact generation-1 interaction fields differ. The maximum patchwise difference is

\[
\max_j|T_{I,j}(X_A)-T_{I,j}(X_B)|=\mathbf{0.2543}.
\]

Proposition 1 therefore applies directly: no map defined only on the declared coarse summaries can reproduce the exact next interaction field for both states. The failure is not statistical uncertainty, a small-sample result, or a long-horizon simulation pattern. It is an exact identification failure of the coarse representation under the stated transition map.

The original fixed 500-pair generation-60 campaign then provided a finite downstream comparison. Realised functional loss occurred in 339 aligned trajectories (`0.678`) and 361 anti-aligned trajectories (`0.722`), an observed difference of **+4.4 percentage points**. The paired large-sample **95% CI of approximately -1.2 to +10.0 percentage points** and exact McNemar `p=.143` did not establish a signed generation-60 effect. Relative to the aligned baseline, the upper confidence limit corresponds to the same **14.8% relative increase** ceiling noted above. **Non-significant tests do not establish equivalence.**

### The hidden state distinction propagated to a later functional endpoint

In the separately locked 1,500-pair propagation experiment, neither state had realised functional loss by generation 5, so `Delta_5=0`. At generation 10, the anti-aligned minus aligned difference was **+0.33 percentage points** (95% CI **-0.44 to +1.11**). At generation 20 it was **+5.33 points** (**+2.04 to +8.62**), and at generation 40 it was **+5.20 points** (**+1.96 to +8.44**).

The nested prefixes separate magnitude from precision. At generation 20, estimated differences were +5.4 points at 500 pairs, +5.9 at 1,000, and +5.33 at 1,500; intervals narrowed with increasing pair count. At generation 40, the corresponding estimates were +4.4, +6.4 and +5.2 points. The principal effect of replication was therefore improved precision rather than a qualitative reversal of the estimated later-horizon contrast.

Under this one declared deterioration path, the exact state distinction is immediate at the transition level, nearly absent in the coarse functional-loss endpoint at generations 5–10, and visible at about five percentage points by generations 20–40. The result demonstrates propagation across scales of description; it **does not establish generation 20 as a true cutoff**, a universal biological threshold, or a natural-system timescale.

### A scalar connectivity label did not transport across seeds or mechanisms

The historical allele-frequency-mixing screen showed one `m=.10` between-block pattern (`p=.0205`) in its original seed family. The single preregistered fresh Phase-U ensemble did not reproduce it (`p=.745`; paired McNemar `p=.694`).

Whole-individual dispersal at `d=.10` produced pooled loss `.606` and equal-rate `p=.811`; pollen-only paternal gene flow at `g=.20` produced pooled loss `.532` and equal-rate `p=.728`. The historical allele-mixing pattern therefore did not transport to these process-resolved operators. Matched-expected-support partner dynamics likewise did not establish a portable architecture effect.

The mathematical implication is representation-specific: a scalar parameter is meaningful only through the operator that maps the current state to the next one. Equal numerical values or common labels such as “connectivity” do not establish state equivalence across different transition operators.

## Discussion

### State is relational, not only compositional

The main result is an exact non-sufficiency statement. Two ecological configurations can contain the same declared amounts and marginal distributions of interaction, genetic and trait support yet have different next transitions because those components are arranged differently across patches. The relevant distinction is therefore relational: where interaction support occurs relative to genetic/trait support can matter even when every layer-wise summary is unchanged.

This interpretation is narrower than saying that “interactions matter” or that “fragmentation changes networks.” Those statements are already well established. The contribution here is to show constructively that **composition can be held fixed while spatial cross-layer organization alone changes the transition**. In that sense, the state variable is not merely the vector of components but the joint organization required by the transition map.

### Functional vulnerability can be hidden by persistence and marginal summaries

The parent fragmentation programme showed that potential viability, realised occupancy, interaction support, effective size and realised high-trait mass can separate under the same structural change. The present state counterexample adds a different form of hidden vulnerability: even after the component marginals are matched, their spatial coordination can encode different futures.

Natural systems illustrate why this distinction is ecologically plausible without validating the model. In *Crepis sancta*, local resource loss is associated with reduced pollinator activity and reproduction despite nonzero wider movement, illustrating an uncompensated route from local support to function (Cheptou & Avendaño 2006; Dornier & Cheptou 2013). On Miyake-jima, reduced floral resources after volcanic disturbance were accompanied by broader *Zosterops* movement, increased pollen immigration and maintained pollination, illustrating movement-mediated compensation rather than monotone decline (Abe & Hasegawa 2008; Abe et al. 2013). These systems differ not simply in how much habitat or biodiversity remains, but in how movement and interaction reorganize functional support.

The comparison suggests a useful ecological projection of the mathematical result: disturbances may create vulnerability when function-supporting components become spatially separated, but compensation is possible when movement or interaction reorganization restores effective co-occurrence. That projection is a hypothesis for natural systems, not a result of the present finite model.

### Time and cohort can make the relevant state appear to disagree with itself

The propagation experiment shows that a state distinction can be exact at one transition yet become visible in a coarser endpoint only after time has passed. Natural studies show an analogous measurement problem across biological cohorts. In fragmented *Conospermum undulatum*, contemporary pollen movement and reproduction have deteriorated while adult neutral genetic structure still reflects historically greater connectivity (Delnevo et al. 2019, 2021, 2026). In *Spondias purpurea*, interaction, pollen flow, reproductive function and younger-cohort genetics deteriorate in the same fragmentation comparison, while adult genetic responses are less diagnostic of the contemporary process (Cristóbal-Pérez et al. 2021).

These examples do not establish the modelled propagation timescale. They show why a state representation must specify both **which process** and **which temporal layer or cohort** it represents. A standing adult genetic statistic can be an ecological memory variable, whereas offspring parentage or pollen-pool composition may describe the current mating process.

### Urban and island labels are upstream histories, not state variables

The earlier urban–island programme asked whether different fragmentation mechanisms might converge on the same future-relevant state. Within Honshu–Izu, mainland distance did not improve held-out pollen-function prediction after a fixed partial functional state was supplied; within Zurich, source-defined urban/local context did not yield reproducible positive held-out gain after the function-specific pollinator interaction state. These results motivate a process-based comparison, but the two archives do not identify a shared urban–island law because state definitions, endpoints, taxa, protocols and study identity differ.

For the present manuscript, the implication is conceptual. `Urban`, `island`, `forest fragment` and `volcanic disturbance` should be treated as upstream histories that can alter interaction support, movement, mating opportunity and ecological memory. They are not themselves mathematical states unless those labels determine the transition relevant to the prediction target. A future matched comparison would therefore measure the same process coordinates across independently replicated origins rather than test a habitat label as if it were a mechanism.

### Process state is operator-specific

The portability tests reinforce the same principle in a different form. A number such as `0.10` does not have an operator-free ecological meaning. Allele-frequency mixing, whole-individual movement, paternal pollen flow and partner movement change different parts of the state and can therefore generate different transition distributions. Any common lower-dimensional “connectivity” coordinate requires an identification argument showing that it preserves the distinctions relevant to the target.

### Relation to warning validity and natural-data work

The separate full-denominator warning audit addresses another inferential target. Nothing in the constructive state pair shows that the frozen diversity thresholds failed because cross-layer alignment was omitted, and no warning rule was rerun using alignment. The safe connection is therefore conceptual: a marginal component can change consistently without uniquely identifying the future functional trajectory if the target also depends on omitted joint organization. This manuscript **makes no claim that the frozen relative-diversity thresholds are validated predictive warnings**.

Natural-data measurement-gate development also remains outside this submission lane. Its historical local router is `natural_data_four_gate_program.md`, with the authoritative reader-facing programme maintained separately. Natural examples discussed here therefore remain background and ecological interpretation, not a fourth evidence block in the state manuscript.

### Claim boundary

The exact proposition is conditional on the declared transition map and the constructed admissible states. The propagation result is finite and specific to one locked deterioration path. The original 500-pair generation-60 comparison remains imprecise; the later 1,500-pair experiment is a separate prospectively locked extension. The propagation experiment **does not establish generation 20 as a true cutoff**. Failure of one historical connectivity pattern to reproduce or transport does not establish that connectivity is irrelevant. The natural systems discussed above are ecological interpretations and hypothesis-generating analogues, not external validation of the finite closure.

## Conclusion

A coarse ecological state is valid only if it preserves distinctions required by the declared transition. We constructed two eco-genetic states with identical standard marginals and diversity summaries but different exact next interaction fields, proving that the coarse representation is not transition-sufficient. A separately locked paired experiment showed that the same hidden spatial organization later generated an approximately five-percentage-point functional-loss contrast under one deterioration path. The ecological implication is positive: functional vulnerability can reside in the **joint spatial organization** of interaction and trait/genetic support, not only in the amount of each component. Natural collapse, compensation and cohort lag are therefore best treated as hypotheses about how real systems reorganize this joint state, not as validation of the model itself.

## Data and code availability

The original Phase-V result remains fixed by its locked artifact. The constructive certificate is stored in `artifacts/cross_layer_alignment/phase_v_locked_summary.json`. The post-Phase-V propagation protocol, implementation and successful workflow provenance are stored in `experiments/alignment_propagation_protocol.json`, `src/eco_genetic_warning_extensions/alignment_propagation_experiment.py`, `artifacts/alignment_propagation/locked_summary.json`, and `docs/ALIGNMENT_PROPAGATION_RESULT_2026-09-04.md`. Locked negative and portability results, STOP artifacts, workflow identifiers and source-version metadata remain indexed in `manuscript/artifact_index.md`.

The load-bearing external bibliography for this lane is recorded in `manuscript/state_validity_references.md`.