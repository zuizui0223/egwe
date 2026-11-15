# From eco-genetic state separation to conservation, molecular mechanism and phylogeography
## Prospective bridge and empirical decision design — 2026-11-15

**Status:** prospective conceptual and measurement bridge, **not** a result of the finite EGC–EGWE model, not an empirically supported transport of the AUC or q thresholds, and **not** a new submission lane. This document supports the single active *Theoretical Ecology* manuscript and points natural evidence collection to the separately authoritative `zuizui0223/egwee` programme.

### 1. The core question

**Can two populations with similar neutral genomic diversity, adult abundance, or geographical isolation have different future reproductive function because functional genotypes, expression, partner encounters, mating opportunities and local demography are differently aligned?**

The model supplies a constructive answer of *possibility* in one declared finite closure, not a field-confirmed claim. Its distinctive empirical prediction is incremental: after demography, ancestry, neutral population structure and current ecological marginals are held constant, synchronized **local joint-state/process measurements** may still predict future functional outcomes.

Do not equate (a) demographic occupancy, (b) current realised floral phenotype, (c) high-bin potential viability, (d) endpoint allele relative selection, or (e) future breeding and recruitment success. These differ even in the pinned model: the original high-grid viability threshold is approximately **q_grid=0.5991975107**, whereas **q_allele=0.625** is the `z=1` endpoint/allele-relative-selection switch. Neither is a universal field threshold.

### 2. Conservational interpretation: monitor ecological function and genetic risk separately

Genetic diversity remains important to conservation; however, `H_alpha`, `H_gamma`, `pi`, `F_ST` or `N_e` alone cannot be assumed to identify *which local interaction-dependent function will fail next*. A 2026 cross-species study found molecular diversity was a poor predictor of trait evolvability across taxa, but this does not imply nucleotide diversity is irrelevant to inbreeding, genetic load or long-term adaptive potential. The EGC–EGWE negative six-threshold result similarly concerns predictive discrimination for one **specified functional endpoint**, not the utility of genetic diversity as a conservation target.

**Proposed management comparison (to test; no current estimates):**

| Observed pre-state | Alternative causal explanations | Competing interventions to compare with matched baselines | Direct outcome |
|---|---|---|---|
| Adult heterozygosity remains high; compatible pollen and seeds decline | Interaction bottleneck or cohort lag | Improve pollinator effectiveness / flowering habitat versus population supplementation | Compatible pollen receipt, viable seed production, next seedling cohort |
| Neutral diversity low but reproduction currently functions | Historical founder effect / drift; inbreeding risk not yet apparent | Habitat/population reinforcement and genetic rescue *where safe* rather than declaring no risk | Short-term function **and** longer-term inbreeding, fitness, recruitment |
| Pollen/seed immigrants increase, reproduction still weak | Movement without compatible mate/functional recoupling; density or microsite bottleneck | Restore compatible mating context / resources and compare assisted gene flow | Effective siring, seeds reaching viable establishment, recruits |
| Similar ancestry and density; opposite reproductive outcomes | Different functional alleles or expression, partner matching, developmental history | Common-garden/controlled pollination, partner-exclusion/addition and local habitat treatment | Matched genotype × environment/interaction effects on fitness components |

Never equate non-significant predictive gain with equality, and do not endorse translocation without outbreeding, disease, provenance, permissions and management assessment. **Functional recovery is not guaranteed by gene flow or increased heterozygosity.** Conversely, improving function does not remove the need to monitor genomic erosion.

**Core conservation estimand:** improvement in prospective function/recruitment under predeclared intervention `do(R=r)`, compared with a matched no-intervention or alternative-treatment counterfactual, with genomic risks reported as separate outcomes. The present simulator has not directly estimated these natural causal treatment effects.

### 3. Molecular biology: from a synthetic allele state to a measurable trait mechanism

The simulator's `p` is an **effective high-trait-associated state frequency**. It is **not a measured one-locus SNP**, a transcript level, epigenetic switching rate, expression of a single flower-colour gene, or standing phenotypic heritability. Its `q` is aggregate effective interaction support, not automatically pollinator richness or network connectance.

Do not simply substitute RAD-seq SNP frequency for `p`. An empirical bridge must establish a chain:

`ancestry / neutral genome -> candidate functional variant(s) -> tissue/stage-specific expression -> phenotype (T) -> interaction/mate compatibility (I, C) -> viable offspring/recruitment (F)`.

Practical tiers:

- **Tier M1 — population genomic baseline:** ddRAD/RAD/MIG-seq or whole-genome SNPs for individual ancestry, kinship, `F_ST`, heterozygosity, reproductive cohort, and structure-adjusted genotype–environment/interaction association. RAD-based SNPs do not require a reference genome for de novo locus calling, but a reference improves annotation and causal interpretation; sparse markers cannot reliably measure ROH or strongly polygenic causal architecture.
- **Tier M2 — molecular candidate:** functionally annotated genomic regions, QTL/GWAS (subject to design and power), RNA-seq of matched floral developmental stages and treatment environments, and where justified allele-specific expression or targeted regulatory assays. Expression associations can be environmentally induced; they do **not** prove heritable local adaptation.
- **Tier M3 — mechanism validation:** replicated common garden, reciprocal transplant/reciprocal pollination, compatible-mating and visitor manipulations, genotype-by-environment estimates, and phenotypic fitness (compatible pollen receipt, viable seeds or successful juveniles). An independent perturbation or segregating family is needed for stronger causal claims.
- **Tier M4 — longitudinal sorting and repair:** sample adults, maternal parents, embryos/seeds and seedlings to estimate allele-frequency change through recruitment and mating; pair genetic shifts with measured `I/T/D` in the *same* patch/cohort/time window. This directly tests the qualitative sorting/buffering hypotheses.

A tempting shortcut is to interpret `q_allele=0.625` as an empirically identifiable selection threshold. **Do not do this**: the numerical threshold belongs to the frozen model. Estimate the empirical interaction-by-genotype reaction norm first, with a field-defined, predeclared scale. Functional genotype–interaction association is not proven merely by a significant GEA.

### 4. Phylogeography: ancestry/history is memory, not current function

The phylogeographic bridge is especially strong for **islands, postglacial refugia, volcanically reset landscapes and urban remnants**, because similar present-day genetic diversity may reflect radically different histories.

**History layer `H_history`:**
- Deep lineage relationships, colonization sources/routes and timing (with explicit model uncertainty)
- Historical bottlenecks, expansion, admixture/introgression and effective population sizes
- Nuclear SNP population structure and isolation by distance/resistance/environment
- Organellar haplotypes where available (maternal plastid inheritance gives a seed-flow-biased comparison only when confirmed; exceptions must be tested)
- Pollen/seed paternity of a *current offspring cohort* as a contemporary movement measure, not a replacement for ancestry history

**Present-state layer `S_t`:** `D, I, T, C_pollen, C_seed, C_partner, R, G_adult, G_offspring, A` as in `manuscript/natural_state_field_protocol.md`.

**Future endpoint `F_{t+1}`:** direct reproductive/functional output and follow-up establishment; adult neutral genetic state is neither contemporaneous mating state nor subsequent reproductive function.

Three competing explanations must remain separate:

1. **Historical filtering / drift:** similar present-day floral or genetic variation reflects a common founder, refugial ancestry, or demographic bottleneck.
2. **Current ecological sorting / selection:** local interactions and climate are actively changing genotype-specific survival, flowering or mating success.
3. **Genotype-independent plasticity / cohort lag:** environment affects trait expression and function without a matching contemporary allele-frequency response, or adult genomic state retains earlier history.

Organellar–nuclear topology discordance is compatible with, but does not itself prove, chloroplast capture/introgression; incomplete lineage sorting and sampling/model error are alternative explanations. Likewise, population trees or `F_ST` alone cannot distinguish historical isolation from functional disconnection. Joint demography–selection inference remains challenging even with whole genomes.

A clean test uses ancestry/demography as an **upstream confounder and history covariate**, not as a biological warning signal by fiat. If the lineage label still improves held-out future function after all measured present processes, the proposed state is incomplete or there is an unmeasured historical/functional mechanism; **do not** declare intrinsic lineage-specific fate from that residual.

### 5. Exact field test: same ecological unit, cohorts and time windows

Sampling grain: `landscape/island -> site -> patch -> maternal plant -> seed cohort -> seedling cohort`, linked by coordinates, dates and original specimen/sequence IDs. A 10–20-site pilot across replicated fragmentation gradients may test feasibility, but confirmatory sample sizes and follow-up duration **must be powered from expected patch-level variance and independence**, not copied from the 12,000 simulated trajectories.

At time `t` in each independent patch:

`D`: flower density, reproductive-adult density, microhabitat and stage structure.

`I`: visitor-specific visitation **and** pollination effectiveness, compatible pollen receipt / exclusion controls.

`T`: focal functional trait and matching with visitors (for *Campanula*, size, colour and visitor accessibility are candidates; colour alone is not a direct seed-function measure).

`C`: parentage-inferred pollen movement, seed movement, partner movement (separate these; legacy model `migration_rate` was only allele-frequency mixing).

`G`: genotypes of reproductive adults, maternal seed arrays and new juveniles; adaptive candidates only when linked to phenotype/fitness.

`M/H`: colonization age, disturbance/fragmentation date, neutral lineage history, parental cohort age, seed-bank legacy.

`A`: the within-site **co-location/covariance** of effective interaction, trait/mating support and local genetic states; retain individual patch vectors, not only marginals.

At `t+\Delta`: compatible seed set, viable germination and new recruits **not already used** to construct the pre-state. The relevant lead time is defined in flowering/seedling cohort units rather than equated with a model generation.

**Predeclare nested predictive models:**

- `S0`: fragmentation geometry, site history, ancestry and neutral adult diversity/kinship, census and measured baseline function if available;
- `S1`: S0 + synchronized realized interaction effectiveness, functional traits, current paternity/offspring mating state and alternative routes;
- `S2`: S1 + preregistered patchwise cross-layer alignment and measured sorting/recruitment/recoupling proxies.

Primary comparison: **held-out site-/island-/year-block predictive loss** for `F_future`, and (if meaningful) full-denominator discrimination for predeclared functional-loss events. Compare S2 against S1, not just against an implausibly weak neutral-only baseline. Preserve sample unit/horizon, censoring and calibration; do not tune ancestry strata, proxy choice or warning threshold after seeing future outcomes.

**Competing predictions / falsifiers:**
- If `S1` predicts as well as `S2`, the proposed *incremental relational* bridge is not supported at that measurement scale.
- If adult neutral diversity predicts when offspring/interaction state is controlled, it may have independent information; do not insist a particular metric must fail.
- If genetic differences disappear in a common garden but field function differs, plasticity or current biotic context becomes a stronger candidate than fixed adaptive divergence.
- If translocation increases neutral diversity but does not improve viable offspring, genetic movement did not resolve the tested functional bottleneck.
- If a candidate functional locus predicts trait expression but not fitness, its conservation priority needs further endpoint evidence.

### 6. Most direct candidate systems and publication boundary

**Candidate A — Campanula punctata / island-mainland:** pair a synchronized subset of floral phenotypes and known lineages with live visitor effectiveness, same-year maternal progeny/parentage and later recruitment. Previous photographic color records and historical population SNP structure are not sufficient without the matched-site year and cohort bridge. This is a *proposed* test, not an assertion that the present paper has natural validation.

**Candidate B — island Cirsium:** RAD-based phylogeny/phylogeography could supply lineage/colonization history; orientation, head morphology and bracts/spines are candidate **different functional mechanisms**. Test visitor access versus herbivore damage as **separate** endpoints, with controlled environmental expression and ancestry control. Do not infer adaptive evolution from a phylogenetic trait shift alone.

**Candidate C — existing published multisystem datasets:** the EGWEE empirical synthesis is the authoritative publication lane for natural fragmentation layers. Any reuse here must remain a *prospectively defined, external* adequacy test, not a model weight/threshold recalibration.

**Paper scope:** the active *Theoretical Ecology* manuscript may discuss these as prospective, falsifiable implications only. Its positive numerical claims remain fully finite-model results. Building a natural-data series, genomic mechanism paper, or phylogeographic analysis requires separate source/permission/data and non-overlapping publication claims.

### 7. Literature anchors (verified publisher/PubMed metadata)

- Aitken SN, Jordan R, Tumas HR (2024). Conserving Evolutionary Potential: Combining Landscape Genomics with Established Methods to Inform Plant Conservation. *Annual Review of Plant Biology* 75:707–736. https://doi.org/10.1146/annurev-arplant-070523-044239
- Cruzan MB, Hendrickson EC (2020). Landscape Genetics of Plants: Challenges and Opportunities. *Plant Communications* 1:100100. https://doi.org/10.1016/j.xplc.2020.100100
- Abson KL, Zijmers L, Mittell EA, Young EA, Postma E, Eyre-Walker A, Hadfield JD (2026). Nucleotide diversity is a poor predictor of short-term adaptive potential. *PNAS* 123:e2536181123. https://doi.org/10.1073/pnas.2536181123
- Lotterhos KE (2024). Interpretation issues with “genomic vulnerability” arise from conceptual issues in local adaptation and maladaptation. *Evolution Letters* 8:331–339. https://doi.org/10.1093/evlett/qrae004
- Steinrücken M, [verify complete author list in final citation if used] (2024). Population Genomic Scans for Natural Selection and Demography. *Annual Review of Genetics* 58:319–339. https://doi.org/10.1146/annurev-genet-111523-102651

The last source is included as a reading lead but should **not** be copied into a submission bibliography until its exact authorship is verified. The first four records above have explicit author/year/title/volume/DOI metadata from publisher or PubMed records.
