# Urban and island tests of interaction-mediated functional fragmentation

> Novelty boundary: see `manuscript/URBAN_ISLAND_NOVELTY_AUDIT_2026-10-06.md` for the distinction between established functional/persistence results and the compensation-architecture claim.

## Central question

Urban and island systems are **contrasting causal routes through the same condition map, not ecological equivalents**.

> **Do different fragmentation mechanisms converge on the same future-relevant functional-fragmentation regime?**

Matching habitat category, occupancy, mean interaction, mean genetic diversity, or even separate marginal distributions is not enough if hidden spatial alignment or ecological memory still changes subsequent functional loss.

Because `functional fragmentation` is already used for organism-centred functional connectivity, manuscript prose should use **interaction-mediated functional fragmentation** for the focal process here: weakening or destabilisation of biotic interaction support required for realised ecological function while focal populations or patches may remain present. Structural fragmentation must not be equated with **network simplification**.

## What the completed model programme establishes

### 1. Function can be lost before population disappearance

The parent model establishes a high-function interaction-supported state and shows that equal isolation of the same prepared state lowers interaction, local effective size and realised high-trait mass before demographic disappearance. The fixed-area 1–16-patch sensitivity shows that the first split already produces most of the interaction/Ne disruption.

### 2. Recurrent turnover changes source feasibility and loss incidence

The extension separates source feasibility from post-establishment loss. The high-precision recurrent-turnover frontier changes pooled functional-loss incidence from about `.682` at `p_star=.325` to `.273` at `.400`, with no detected excess block heterogeneity at the tested frontier coordinates. Historical R1–R4 labels are calibration screens, not biological regimes.

### 3. Connectivity is operator- and ensemble-dependent

The historical allele-only Phase-M `m=.10` equal-rate signal (`p=.0205`) did not reproduce in one preregistered fresh **Phase U** ensemble (`m=.10 p=.745`; McNemar `p=.694`). It also did not port to whole-individual dispersal (**Phase R**) or pollen-only paternal gene flow (**Phase S**) in the historical seed family.

**Current claim ceiling:** no robust portable connectivity heterogeneity effect was established across the tested seed ensembles and biological operators. `migration_rate` remains allele-frequency mixing only and must not be translated directly into demographic, pollen, seed, pollinator or recolonisation movement.

### 4. Aggregate and partner perturbations do not define a universal network boundary

High-precision `kappa=3.0,4.5,6.0` conditions remained intermediate and block-homogeneous. Reduced-form partner loss and **Phase T** matched-expected-support temporal partner variability changed some trajectory identities but produced no detected population-level incidence, block-heterogeneity or paired marginal-risk effect. The preregistered adaptive-rewiring gate stayed closed.

These are bounded negative results, not evidence that real partner identity, functional diversity or rewiring are irrelevant.

### 5. Genetic warning is downstream and conditional

Only after the loss process was fixed warning-blind did baseline-relative `H_alpha/H_gamma` erosion precede observed losses in one calibrated benchmark. Absolute thresholds were not robust, and warning behaviour was not fully portable across independently calibrated domains.

## State-sufficiency result

The parent repository state-sufficiency audit was merged in `eco-genetic-criticality` PR #70.

### Full-state sufficiency under the declared closure

The finite simulator is Markov in its explicit state—patch population, interaction state, high-associated allele frequency and realised trait-bin state—together with fixed future forcing and stochastic law. Under this model closure, different histories that arrive at exactly the same full state have the same future trajectory distribution. With the same RNG seed they produce the same realised trajectory.

This is a **model theorem**, not a claim that real ecological systems have no memory. Any omitted ecological-memory variable must become part of the state if it changes the future.

### Coarse-state insufficiency

A constructive two-patch counterexample holds constant:

- patch and total census;
- the marginal distribution and weighted mean of interaction state;
- the marginal distribution and weighted mean of allele frequency;
- `H_alpha`, `H_gamma`, `F_ST`;
- realised trait state.

Only patchwise interaction–genetic alignment changes. One state aligns high interaction with high allele support; the other anti-aligns them. Because the interaction update is local, the next interaction field differs despite the coarse summaries being identical.

**Consequence:** a functional-fragmentation regime cannot be defined only by averages, occupancy, genetic diversity, or separate marginals. It must retain the future-relevant **joint spatial alignment**, or use a lower-dimensional statistic whose predictive sufficiency has been demonstrated.

## Why urban and island routes should differ upstream

### Urban route

Cities are heterogeneous, human-connected mosaics rather than simple oceanic islands. Recent urban plant genetics synthesis shows that genetic diversity can remain comparable to non-urban populations and gene flow can remain high despite fragmentation. At the same time, plant–pollinator interactions can turn over strongly with urbanisation and season: in Bengaluru, interaction turnover was more strongly structured by local urbanisation and season than by spatial distance, with plant turnover and rewiring important.

**Urban implication:** neutral genetic isolation is not a safe proxy for interaction-mediated functional isolation.

### Island route

Oceanic-island pollination networks are often smaller and lower in interaction diversity than mainland or continental-island networks, but area and isolation do not explain every network property. Mutualist availability is a plausible establishment filter, while reproductive assurance can maintain demographic persistence after the original interaction-dependent function weakens.

**Island implication:** geographic isolation alone does not specify the functional-loss regime; mutualist availability, interaction identity, functional redundancy, reproductive assurance and stepping-stone movement are separate coordinates.

### Fragmentation and network literature

A 2025 global meta-analysis of 80 insect-pollinator studies found negative fragmentation associations but identified reduced habitat area as the strongest component. A 2025 plant–vertebrate network study likewise found habitat loss rather than fragmentation per se associated with network change; about 90% of interaction dissimilarity between strongly contrasting landscapes arose from species turnover, while rewiring became relatively more important where species pools overlapped.

Recent longitudinal network work further shows that interaction dynamics carry information beyond richness: an eight-year, 12-site study found most interaction changes arose from species turnover, while rewiring among persistent species was especially important for pollinator persistence.

## Natural inversion pair: geography does not determine the functional regime

Existing natural programmes already supply a useful bounded contrast, even though they do not identify a universal urban–island convergence law.

### Urban *Crepis sancta*: movement without local functional rescue

In the Montpellier pavement system, low local flowering density was associated with lower pollinator activity and seed set. Separate parentage work in the same urban programme nevertheless showed nonzero pollen/seed immigration and movement among patches. The defensible state is therefore **interaction-limited local fragmentation embedded in a still-connected metapopulation**. Wider movement did not imply maintenance of local interaction-dependent function.

### Miyake-jima *Camellia japonica*: local resource loss with movement-mediated compensation

After volcanic disturbance on Miyake-jima, local floral resources and pollinator density declined, but *Zosterops* movement broadened and pollen immigration/donor mixing increased. Pollination was maintained or enhanced and next-generation genetic mixing did not collapse. The defensible state is therefore **movement-compensated local disruption** rather than monotone functional deterioration.

### Consequence

These two programmes point in opposite directions:

`urban Crepis: local support loss -> interaction loss -> function loss despite nonzero movement`

`Miyake Camellia: local support loss -> broader partner/pollen movement -> function maintained`

This contrast changes the biological interpretation of “fragmentation.” The informative distinction is not city versus island, or connected versus isolated, but whether movement and interaction reorganisation **recouple the process that is locally limiting function**. Movement that occurs in the wrong layer or at the wrong spatial scale need not rescue the focal function.

That inference remains bounded because the two programmes are not synchronized matched-origin experiments. It is a mechanistic natural-history contrast, not evidence that one universal compensation axis has already been estimated.

## Revised convergence hypothesis

The correct cross-system hypothesis is neither `cities and islands have the same fragmentation effect` nor `similar mean interaction/genetic diversity means the same regime`.

> **Distinct fragmentation mechanisms converge only if, after conditioning on a candidate future-relevant joint functional state, system origin and fragmentation history no longer add predictive information about subsequent realised functional loss.**

This is the operational falsification rule.

## Convergence test

For repeated populations or population-years:

1. measure candidate state variables before the outcome window;
2. estimate subsequent realised functional loss independently of genetic warning variables;
3. fit a common loss model using the candidate regime state;
4. add `urban/island` origin and fragmentation-history terms;
5. test whether origin/history improves out-of-sample prediction or changes calibrated loss probabilities.

- **If origin/history adds no information:** the candidate state is sufficient at the tested scale, supporting convergence.
- **If origin/history still predicts loss:** the proposed regime is incomplete; add the missing process or memory variable rather than declaring cities and islands intrinsically different regimes.

## Minimum candidate state

Retain, at minimum, candidate measurements of:

1. spatial support — habitat amount, configuration and matrix quality/resistance;
2. local demographic state — abundance/density and effective size where estimable;
3. realised interaction support — interaction strength and partner identity;
4. interaction architecture — functional diversity, contribution evenness, specialisation, turnover and rewiring;
5. **joint spatial alignment** — whether demographic/genetic/trait support and interaction support occur in the same patches;
6. biological connectivity by process — pollen, seed/propagule, demographic and partner movement separately;
7. alternative functional routes — reproductive assurance or compensatory partners;
8. realised function through time;
9. genetic state through time, distinguishing neutral from adaptive/functional information where possible;
10. plausible history/memory variables.

The goal is not to require all ten forever. It is to find the smallest representation for which origin/history ceases to improve future functional-loss prediction.

## Practical implications of the present results

**Persistence is not function.** Similar occupancy can conceal different realised interaction support and performance.

**Establishment and deterioration are separate filters.** Urban interaction filtering and island colonisation/mutualist filtering may alter whether a high-function state can be established without necessarily changing the same downstream loss axis.

**Connectivity must be process-specific.** Genetic connectivity, whole-organism movement, pollen flow and partner movement cannot be collapsed into one scalar without validation.

**Monitoring must preserve joint spatial structure.** Averaging interaction and genetic variables across sites can erase alignment information that determines local feedback and future function even when standard diversity summaries are unchanged.

## Manuscript-level synthesis

> **Fragmentation does not define functional risk by geometry alone. Different fragmentation mechanisms can become dynamically equivalent only when they produce the same future-relevant joint ecological state. Genetic warning is interpretable only downstream of that state-defined loss process.**

## Key references

- Alaasam, V. et al. (2026). *Nature Reviews Biodiversity* 2:170–185. doi:10.1038/s44358-026-00138-0.
- Hardion, L., Sotillo, A. & Muratet, A. (2026). *Perspectives in Plant Ecology, Evolution and Systematics* 70:125920. doi:10.1016/j.ppees.2025.125920.
- Marcacci, G. et al. (2023). *Ecology Letters*. doi:10.1111/ele.14324.
- Olhnuud, A. et al. (2025). *Journal of Applied Ecology* 62:2502–2514. doi:10.1111/1365-2664.70161.
- Gama, M. et al. (2025). *Biological Conservation* 311:111419. doi:10.1016/j.biocon.2025.111419.
- Traveset, A. et al. (2016). *Global Ecology and Biogeography*. doi:10.1111/geb.12362.
- Wang, X.-P. et al. (2025). *Biotropica* 57:e70027. doi:10.1111/btp.70027.
- Delavaux, C.S. et al. (2024). *Nature* 627:335–339. doi:10.1038/s41586-024-07110-y.
- Hiraiwa, M.K. & Ushimaru, A. (2024). *Functional Ecology* 38:1296–1308. doi:10.1111/1365-2435.14527.
- Domínguez-Garcia, V. et al. (2026). *Ecology Letters*. doi:10.1111/ele.70293.
- Ward, C.A. et al. (2026). *Nature Reviews Biodiversity* 2:355–369. doi:10.1038/s44358-026-00159-9.
- Marjakangas, E.-L., Dalsgaard, B. & Ordonez, A. (2025). *Ecology Letters* 28:e70146. doi:10.1111/ele.70146.
- Peled, O., Kim, J. & Greenbaum, G. (2026). *PNAS* 123:e2515033123. doi:10.1073/pnas.2515033123.
