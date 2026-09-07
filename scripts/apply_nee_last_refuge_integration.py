from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


article_path = Path("manuscript/nee_flagship_article.md")
article = article_path.read_text()

old = """Fragmentation can leave ecological components present while altering the processes that keep them functionally coupled. We combine exact results with prospectively locked finite experiments to explain why systems with the same marginal ecological and genetic quantities reach different futures. Fixed-area fragmentation first separates potential viability from realised occupancy. At fixed mean support, cross-layer covariance changes support variance 49-fold and exact next interaction states by 0.2543. We then resolve the route mechanism. Local q-dependent allele selection is an exact spatial sorting operator and a resolved single-edge causal contributor to late functional fate (`DID=+6.883` percentage points, 95% CI `+5.800,+7.967`). Allele-linked recruitment contracts trait–allele mismatch by exactly 50% and buffers the reversed state. Direct eco-genetic feedback contracts interaction–bundle mismatch by 40% at the support stage and preferentially recouples the reversed configuration. Density-to-interaction feedback creates a shrinking demographic headroom boundary and amplifies collapse. Functional vulnerability therefore reflects the balance among **sorting, buffering, recoupling and a failure gate**, not component amounts or alignment alone."""
new = """Fragmentation can leave ecological components present while altering the processes that keep them functionally coupled. We combine exact results with prospectively locked finite experiments to explain why systems with the same marginal ecological and genetic quantities reach different futures. Fixed-area fragmentation separates potential viability from realised occupancy, while matched marginals can still conceal a 49-fold difference in support variance and a 0.2543 difference in exact next interaction state. Local q-dependent allele selection is a resolved single-edge causal contributor to late functional fate (`DID=+6.883` percentage points, 95% CI `+5.800,+7.967`); allele-linked recruitment contracts trait–allele mismatch by 50%; direct eco-genetic feedback recouples interaction state to the local trait/genetic bundle; and density feedback supplies a collapse gate. Marginal diversity thresholds can precede every loss yet remain non-discriminative. By contrast, a prospectively locked continuous last-refuge route margin measured before generation 10 discriminated generation-40 functional loss (AUC `0.9273`, 95% CI `0.9243,0.9304`) and added ranking beyond co-timed maximum interaction state (`+0.02135` AUC, `+0.01770,+0.02501`). Functional vulnerability therefore reflects both operator balance and the reserve of the strongest remaining local functional refuge."""
article = replace_once(article, old, new, "article abstract")

old = """We address those questions in four steps. First, we test whether a single fragmentation gradient corresponds to a single biological deterioration coordinate. Second, we construct matched-marginal states and identify the exact source of their next-transition difference. Third, we prospectively intervene on individual life-cycle edges and derive the exact operators responsible for sorting, buffering, recoupling and collapse entry. Fourth, we test whether early marginal genetic erosion discriminates later functional fate. Natural examples return only in the Discussion as projections of these mechanisms."""
new = """We address those questions in four steps. First, we test whether a single fragmentation gradient corresponds to a single biological deterioration coordinate. Second, we construct matched-marginal states and identify the exact source of their next-transition difference. Third, we prospectively intervene on individual life-cycle edges and derive the exact operators responsible for sorting, buffering, recoupling and collapse entry. Fourth, we separate stress sensitivity from fate information: after testing whether early marginal genetic erosion discriminates later fate, we prospectively test whether the continuous reserve of the strongest remaining local refuge does. Natural examples return only in the Discussion as projections of these mechanisms."""
article = replace_once(article, old, new, "article four steps")

article = replace_once(
    article,
    "### Early genetic erosion did not identify functional fate",
    "### Marginal genetic erosion did not identify fate, but last-refuge reserve did",
    "warning heading",
)

old = """Perfect precedence is therefore compatible with AUC from 0.5 to 1.0. The observed rules occupy the lower endpoint because every non-event fired. Genetic diversity can thus be stress-sensitive and temporally early without identifying whether sorting, buffering, recoupling or failure-gate dynamics currently control functional fate."""
new = """Perfect precedence is therefore compatible with AUC from 0.5 to 1.0. The observed rules occupy the lower endpoint because every non-event fired. Genetic diversity can thus be stress-sensitive and temporally early without identifying whether sorting, buffering, recoupling or failure-gate dynamics currently control functional fate.

We then asked whether this failure meant that no early fate information existed, or only that marginal diversity was the wrong representation. Before opening any new outcome, we froze a full-feedback holdout using twelve entirely new master seeds, 500 replicates per seed and both AA and RR assignments, for **12,000 trajectories**. The observation used only snapshot generation 9 plus the already fixed generation-10 forcing value. For each patch we calculated

\[
M_j=d_j(0.6q_j+0.3T_j+0.1G_j)-\left(\theta_{10}+\frac{\operatorname{logit}(0.625)}{4.5}\right),
\]

and used the strongest local reserve, `max_j M_j`, as a continuous score; lower reserve meant higher risk of realised all-patch high-trait loss by generation 40. No operating threshold was tuned.

The prospectively locked holdout resolved the contrast. Across the twelve master-seed blocks, last-refuge route-margin AUC was **0.92734** (95% CI **0.92433,0.93035**; pooled AUC 0.92718), with AA and RR AUCs 0.92526 and 0.92891. Only **44 of 8,028 eventual losses (0.548%)** had already occurred by the observation snapshot. Co-timed maximum q was itself predictive (AUC 0.90598, 95% CI 0.90078,0.91118), but the prospectively specified paired AUC difference favoured the integrated route margin by **+0.02135** (95% CI **+0.01770,+0.02501**), with all twelve seed-block differences positive. Mean q, mean population and `H_gamma` had lower AUCs of 0.88944, 0.85010 and 0.86223, respectively.

The monitoring conclusion is therefore asymmetric rather than uniformly negative: **marginal erosion reports stress, whereas continuous last-refuge reserve carries fate information in this finite closure**. The result also localizes where that information resides. System-wide averages discard part of the relevant organization; risk is better ordered by how much functional reserve remains in the strongest local patch after interaction, density, trait and allele state are jointly accounted for."""
article = replace_once(article, old, new, "warning result extension")

old = """Monitoring follows the same principle. A warning variable should not be judged only by whether it moves early. The diversity thresholds here responded before every observed loss but could not distinguish event from non-event trajectories. A useful monitoring design for functional collapse should measure direct function, local interaction state, trait and cohort-specific genetic state, process-specific movement or mating connectivity, and the cross-layer relations among them. More importantly, repeated measurements should estimate **rates of sorting, buffering and recoupling**, because the same marginal state can have different futures depending on which operator currently dominates."""
new = """Monitoring follows the same principle. A warning variable should not be judged only by whether it moves early. The diversity thresholds here responded before every observed loss but could not distinguish event from non-event trajectories, whereas the prospectively locked continuous last-refuge route margin separated later loss with AUC 0.927 and retained predictive information beyond co-timed maximum q. The relevant distinction is therefore not simply early versus late, but **stress sensitivity versus fate information**. A useful monitoring design for functional collapse should measure direct function, local interaction state, trait and cohort-specific genetic state, process-specific movement or mating connectivity, and the cross-layer relations among them. Repeated measurements should additionally identify the strongest remaining functional refuge and estimate **rates of sorting, buffering and recoupling**, because the same marginal state can have different futures depending on which operator currently dominates."""
article = replace_once(article, old, new, "discussion monitoring")

old = """The claim remains bounded. The algebraic weights, `q*=0.625` switch, generation horizons, density headroom and intervention effects belong to the declared finite closure. The work does not establish q-dependent allele sorting as a universal natural mechanism, does not assert a universal natural recruitment or recoupling law, and does not equate the model generations with natural timescales. What it establishes is a constructive and prospectively tested possibility: matched marginals can hide different transitions, and those differences can be traced to identifiable life-cycle operators whose competing effects determine functional fate."""
new = """The claim remains bounded. The algebraic weights, `q*=0.625` switch, generation horizons, density headroom, intervention effects and last-refuge warning performance belong to the declared finite closure. The work does not establish q-dependent allele sorting as a universal natural mechanism, does not assert a universal natural recruitment or recoupling law, does not claim a universal natural warning threshold or AUC, and does not equate model generations with natural timescales. What it establishes is a constructive and prospectively tested possibility: matched marginals can hide different transitions, those differences can be traced to identifiable life-cycle operators, and fate information can reside in the strongest local functional reserve even when marginal erosion is non-discriminative."""
article = replace_once(article, old, new, "claim ceiling")

old = """Load-bearing evidence is restricted to the theorem-guided parent framework, the state/transition-validity programme, the prospectively locked relational mechanism experiment, the prospectively locked edge-decomposition experiment, the prospectively locked focused allele-sorting proof, and the frozen full-denominator warning audit. The recruitment, direct-feedback and density-gate theorems are exact derivations of already declared operators; their paired endpoint contrasts are derived only from locked workflow artifacts. Published natural systems and the separate natural-data measurement programme are Discussion-level projections only."""
new = """Load-bearing evidence is restricted to the theorem-guided parent framework, the state/transition-validity programme, the prospectively locked relational mechanism experiment, the prospectively locked edge-decomposition experiment, the prospectively locked focused allele-sorting proof, the frozen full-denominator diversity-warning audit, and the prospectively locked last-refuge warning holdout. The recruitment, direct-feedback and density-gate theorems are exact derivations of already declared operators; their paired endpoint contrasts are derived only from locked workflow artifacts. Published natural systems and the separate natural-data measurement programme are Discussion-level projections only."""
article = replace_once(article, old, new, "methods evidence architecture")

old = """### Warning denominator audit

The six frozen markers were the first post-baseline generations at which `H_alpha` or `H_gamma` declined 5%, 10% or 20% from baseline. The inherited ensemble contained 35 losses and 48 non-events; the independently seeded fresh ensemble contained 33 losses and 49 non-events. Thresholds, eligibility, horizon and event definition were not recalibrated."""
new = """### Warning denominator audit

The six frozen markers were the first post-baseline generations at which `H_alpha` or `H_gamma` declined 5%, 10% or 20% from baseline. The inherited ensemble contained 35 losses and 48 non-events; the independently seeded fresh ensemble contained 33 losses and 49 non-events. Thresholds, eligibility, horizon and event definition were not recalibrated.

### Prospective last-refuge warning holdout

The last-refuge predictor was frozen before implementation and before any holdout outcome. It used full-feedback AA and RR states, twelve entirely new master seeds (`204701`–`204712`), 500 replicates per seed and no migration or mutation, yielding 12,000 trajectories. Observation was restricted to snapshot generation 9 plus the predetermined generation-10 barrier. The primary risk score was the negative of the maximum patchwise route margin `M_j`; the endpoint was realised all-patch high-trait loss by generation 40. ROC AUC was computed separately within each master-seed block and summarized across twelve blocks with a t-based 95% confidence interval. The primary comparator was co-timed maximum q, evaluated on the same blocks. Confirmation required the route-margin AUC lower confidence bound to exceed 0.75, fewer than 5% of eventual losses to have occurred before observation, and—only for the incremental-ranking claim—the lower confidence bound of paired blockwise `AUC_route - AUC_maxq` to exceed zero. No risk threshold, observation time or comparator was tuned after outcome opening."""
article = replace_once(article, old, new, "methods warning holdout")

old = """The focused allele-sorting proof is pinned to workflow `34016797940`, job `101441868527`, artifact `9984306657`, digest `sha256:61a07cc6a8680a59185537b03abdca85d0f172a65d068ee9661dd9f2fb448c2d`. Later theorem and manuscript edits do not generate replacement scientific ensembles."""
new = """The focused allele-sorting proof is pinned to workflow `34016797940`, job `101441868527`, artifact `9984306657`, digest `sha256:61a07cc6a8680a59185537b03abdca85d0f172a65d068ee9661dd9f2fb448c2d`. The last-refuge warning holdout is pinned to workflow `34130457262`, job `101769061070`, artifact `10022340904`, digest `sha256:46a6b03d3d93a0fb5d03c2e9e27b087605b0cf5dda281fd27ed4581ab3640447`, with prospective protocol commit `6377e684799bd4152eec057bfdb78143df0358fc`. Later theorem and manuscript edits do not generate replacement scientific ensembles."""
article = replace_once(article, old, new, "reproducibility holdout")

article_path.write_text(article)

cover_path = Path("manuscript/nee_flagship_cover_letter.md")
cover = cover_path.read_text()
old = """The warning analysis provides a monitoring consequence. Six frozen diversity thresholds precede every observed loss in two independently seeded ensembles but also fire in every non-event, giving specificity zero and binary AUC 0.5. Detecting erosion is therefore not equivalent to identifying which causal route controls fate."""
new = """The warning analysis provides a monitoring consequence with a positive resolution. Six frozen diversity thresholds precede every observed loss in two independently seeded ensembles but also fire in every non-event, giving specificity zero and binary AUC 0.5. We therefore prospectively froze a separate 12,000-trajectory full-feedback holdout around the continuous reserve of the strongest local eco-genetic refuge. Measured before generation 10, that route-margin score discriminated generation-40 functional loss with AUC **0.92734** (95% CI **0.92433–0.93035**) while only **0.548%** of eventual losses had already occurred, and it added **+0.02135 AUC** (95% CI **+0.01770–+0.02501**) beyond co-timed maximum q. Detecting erosion is therefore not equivalent to identifying fate; local functional reserve is."""
cover = replace_once(cover, old, new, "cover warning paragraph")
cover_path.write_text(cover)

meta_path = Path("manuscript/nee_flagship_submission_metadata.md")
meta = meta_path.read_text()
old = """7. EGWE exact warning-denominator identity + frozen full-denominator audit."""
new = """7. EGWE exact warning-denominator identity + frozen full-denominator diversity audit.
8. Prospectively locked 12,000-trajectory last-refuge warning holdout, with continuous route-margin discrimination and co-timed max-q comparator."""
meta = replace_once(meta, old, new, "metadata evidence hierarchy")
old = """6. **Warning consequence.** Frozen diversity thresholds can precede every loss while firing in every non-event; specificity 0 and binary AUC 0.5."""
new = """6. **Warning contrast.** Frozen diversity thresholds can precede every loss while firing in every non-event; specificity 0 and binary AUC 0.5. In a separately prospectively locked 12,000-trajectory holdout, the generation-10 continuous last-refuge route margin discriminated generation-40 functional loss with mean seed-block AUC **0.92734** `[0.92433,0.93035]`. Co-timed max-q AUC was **0.90598** `[0.90078,0.91118]`, and the paired AUC difference was **+0.02135** `[+0.01770,+0.02501]`; only **0.548%** of eventual losses had already occurred at observation. Thus marginal erosion reports stress, whereas strongest-local eco-genetic reserve carries fate information in the finite closure."""
meta = replace_once(meta, old, new, "metadata warning consequence")
old = """- the density headroom threshold and generations are model-specific; density feedback is not claimed to cause the directional sorting advantage.
- natural examples remain Discussion-level projections only."""
new = """- the density headroom threshold and generations are model-specific; density feedback is not claimed to cause the directional sorting advantage.
- last-refuge warning AUC, observation generation and route-margin weights are finite-closure results, not universal natural warning performance or thresholds.
- natural examples remain Discussion-level projections only."""
meta = replace_once(meta, old, new, "metadata warning claim ceiling")
meta_path.write_text(meta)

print("NEE last-refuge integration patch: PASS")
