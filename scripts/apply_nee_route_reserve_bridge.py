from __future__ import annotations

import json
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {n}")
    return text.replace(old, new, 1)


# -----------------------------------------------------------------------------
# Main article
# -----------------------------------------------------------------------------
article_path = Path("manuscript/nee_flagship_article.md")
article = article_path.read_text(encoding="utf-8")

old = """We tested the endpoint consequence with **6,000 paired AA/RR keys per condition** using twelve entirely new master seeds. Baseline local allele selection produced `RR-AA = +6.65 points` at generation 40 (95% CI `+5.07,+8.23`). Deleting only `q -> allele selection` reduced the contrast to **-0.23 points** (`-1.80,+1.34`). The preregistered primary DID was **+6.883** percentage points with 95% CI **`+5.800,+7.967`**. The generation-20 DID was +6.783 points (`+5.478,+8.088`). Local q-dependent allele sorting is therefore a **resolved single-edge causal contributor** to late functional fate in this finite closure."""
new = old + """

A separate prospectively locked follow-up then asked whether the same edge changes the **continuous reserve of the strongest remaining local refuge** before the late endpoint. Twelve new master seeds, 500 replicates per seed, AA/RR pairing and the two fixed allele-selection conditions yielded **24,000 trajectories**. Both preregistered requirements passed: the generation-40 endpoint DID replicated at **+8.60 percentage points** (95% CI **+7.48,+9.72**), and deleting local q-dependent allele selection removed a small but precise generation-20 maximum-headroom advantage (`DID=+0.0007906`, 95% CI **+0.0007038,+0.0008775**). The number of positive-headroom patches was already saturated at that horizon, whereas continuous maximum headroom still differed. Thus, within the q-only closure, the sorting edge is prospectively linked not only to later fate but to the **depth of last-refuge reserve** that precedes it."""
article = replace_once(article, old, new, "sorting-headroom result")

old = """The prospectively locked six-condition experiment used identical trajectory seeds across conditions, allowing a secondary paired contrast without opening a new ensemble. Direct-feedback benefit, defined as q-only loss minus full-feedback loss, was +0.60 points for AA (`-2.71,+3.91`) but **+8.53 points** for RR (`+5.21,+11.85`) at generation 20; the RR-minus-AA buffering-benefit contrast was **+7.93 points** (`+3.29,+12.58`). At generation 40 the benefits were +1.47 points for AA (`-1.72,+4.65`) and **+7.80 points** for RR (`+4.79,+10.81`), with a difference of **+6.33 points** (`+1.85,+10.82`). These are derived paired contrasts from an already prospectively locked intervention family, not a separately predeclared primary estimand. They nevertheless match the operator: direct feedback preferentially recoupled the reversed arrangement."""
new = old + """

A later fresh, prospectively locked route-duration test sharpened that interpretation rather than strengthening it indiscriminately. The exact full-feedback route-margin shift remained the recoupling term `0.4ad(B-q)`, but full feedback did **not** extend the number of generations retaining a nonnegative-margin refuge. Full-minus-q-only extension was `-0.323` generations in AA and `-1.000` in RR, giving a preregistered RR-minus-AA DID of **-0.677 generations** (95% CI **-0.694,-0.660**). Direct feedback can therefore improve the realised endpoint in one locked intervention family while failing to extend above-switch route duration in another fresh ensemble. Recoupling, route endurance and endpoint persistence are distinct estimands."""
article = replace_once(article, old, new, "recoupling route-duration boundary")

old = """Perfect precedence is therefore compatible with AUC from 0.5 to 1.0. The observed rules occupy the lower endpoint because every non-event fired. Genetic diversity can thus be stress-sensitive and temporally early without identifying whether sorting, buffering, recoupling or failure-gate dynamics currently control functional fate.

We then asked whether this failure meant that no early fate information existed, or only that marginal diversity was the wrong representation."""
new = """Perfect precedence is therefore compatible with AUC from 0.5 to 1.0. The observed rules occupy the lower endpoint because every non-event fired. Genetic diversity can thus be stress-sensitive and temporally early without identifying whether sorting, buffering, recoupling or failure-gate dynamics currently control functional fate.

The same distinction survives even for a mechanistically exact transition coordinate. For full feedback define

\\[
M=d(0.6q+0.3T+0.1G)-\\left(\\theta+\\frac{\\operatorname{logit}(0.625)}{4.5}\\right).
\\]

Its sign exactly determines whether the next interaction state lies above or below `q*=0.625`, and the canonical prospective audit found **0 mismatches across 1,920,000 patch-generations**. Yet the frozen generation-20 binary marker `all M<0` preceded all **3,943** generation-40 losses and also fired in all **2,057** non-events, again giving sensitivity 1, specificity 0 and AUC 0.5. **Transition-exactness therefore does not imply fate-predictiveness.** Thresholding can discard the relevant reserve depth even when the underlying coordinate is mechanistically exact.

We then asked whether these failures meant that no early fate information existed, or only that marginal and thresholded representations were the wrong summaries."""
article = replace_once(article, old, new, "transition exactness warning bridge")

old = """Load-bearing evidence is restricted to the theorem-guided parent framework, the state/transition-validity programme, the prospectively locked relational mechanism experiment, the prospectively locked edge-decomposition experiment, the prospectively locked focused allele-sorting proof, the frozen full-denominator diversity-warning audit, and the prospectively locked last-refuge warning holdout. The recruitment, direct-feedback and density-gate theorems are exact derivations of already declared operators; their paired endpoint contrasts are derived only from locked workflow artifacts. Published natural systems and the separate natural-data measurement programme are Discussion-level projections only."""
new = """Load-bearing evidence is restricted to the theorem-guided parent framework, the state/transition-validity programme, the prospectively locked relational mechanism experiment, the prospectively locked edge-decomposition experiment, the prospectively locked focused allele-sorting proof, the prospectively locked sorting–headroom follow-up, the exact operator-balance route-margin theorem with its prospectively locked route-duration and full-denominator test, the frozen diversity-warning audit, and the prospectively locked continuous last-refuge warning holdout. The recruitment, direct-feedback and density-gate theorems are exact derivations of already declared operators; their paired endpoint contrasts are derived only from locked workflow artifacts. Published natural systems and the separate natural-data measurement programme are Discussion-level projections only."""
article = replace_once(article, old, new, "methods evidence architecture")

old = """### Exact buffering, recoupling and failure-gate derivations

For two-kernel recruitment, the high-trait mass identity follows because the low and high kernels have disjoint support relative to the declared high-trait cutoff. With inheritance weight 0.5, recruit high-trait mass is the arithmetic mean of resident high-trait mass and high-allele frequency."""
new = """### Prospective sorting–headroom follow-up

The sorting–headroom experiment retained the q-only closure, existing AA/RR states, forcing path and realised all-patch functional-loss endpoint. It compared baseline local q-dependent allele selection with the identical life cycle in which only allele selection used spatial-mean q. Twelve entirely fresh master seeds with 500 replicates each yielded 6,000 paired AA/RR keys per condition and 24,000 trajectories. The two preregistered requirements were a positive generation-40 endpoint DID and a positive generation-20 DID in maximum patchwise pre-update headroom `H=dq-theta-logit(0.625)/4.5`. No alternative mediator horizon, threshold, endpoint or intervention was opened after outcomes.

### Exact buffering, recoupling and failure-gate derivations

For two-kernel recruitment, the high-trait mass identity follows because the low and high kernels have disjoint support relative to the declared high-trait cutoff. With inheritance weight 0.5, recruit high-trait mass is the arithmetic mean of resident high-trait mass and high-allele frequency."""
article = replace_once(article, old, new, "methods sorting headroom")

old = """For the density gate, `d=min(1,N/K)` gives a strictly positive q response to N below carrying capacity. Combining this with the smooth pre-rounding demographic derivative gives a positive q–N–q loop. Solving the q update for the target `q*=0.625` yields `dq >= theta + 0.1135168053`. Paired risk reductions are derived from the already locked density-edge intervention.

### Warning denominator audit"""
new = """For the density gate, `d=min(1,N/K)` gives a strictly positive q response to N below carrying capacity. Combining this with the smooth pre-rounding demographic derivative gives a positive q–N–q loop. Solving the q update for the target `q*=0.625` yields `dq >= theta + 0.1135168053`. Paired risk reductions are derived from the already locked density-edge intervention.

### Exact route margin and prospective route-duration test

For full feedback, the operator-balance margin is `M=d(0.6q+0.3T+0.1G)-theta-logit(0.625)/4.5` at unit area ratio. Monotonicity of the logistic update makes `sign(M)=sign(q_next-0.625)` exact. The prospectively locked route-duration test used six new master seeds, 500 replicates per seed and four AA/RR full/q-only conditions, yielding 12,000 trajectories. It audited the sign identity at every patch-generation, compared full-versus-q-only generations with at least one nonnegative-margin patch, and evaluated the frozen generation-20 all-negative binary marker against generation-40 loss on the full denominator. No route threshold, horizon, endpoint or feedback weight was tuned after outcomes.

### Warning denominator audit"""
article = replace_once(article, old, new, "methods route margin")

old = """All load-bearing finite results are version controlled with locked protocols, machine-readable summaries and workflow artifacts. The relational mechanism decomposition is pinned to workflow `34012983845`, job `101431872354`, artifact `9983093178`, digest `sha256:843a6bdc4a4d4e9de10ce6346cca27a1a863b1780573f000c0f1ab164a81c7ac`. The pathway edge decomposition is pinned to workflow `34014537015`, artifact `9983623440`, digest `sha256:45b38de7514dac8df356579156d994fbc5728e8924308299b2b73571b3595842`. The focused allele-sorting proof is pinned to workflow `34016797940`, job `101441868527`, artifact `9984306657`, digest `sha256:61a07cc6a8680a59185537b03abdca85d0f172a65d068ee9661dd9f2fb448c2d`. The last-refuge warning holdout is pinned to workflow `34130457262`, job `101769061070`, artifact `10022340904`, digest `sha256:46a6b03d3d93a0fb5d03c2e9e27b087605b0cf5dda281fd27ed4581ab3640447`, with prospective protocol commit `6377e684799bd4152eec057bfdb78143df0358fc`. Later theorem and manuscript edits do not generate replacement scientific ensembles."""
new = """All load-bearing finite results are version controlled with locked protocols, machine-readable summaries and workflow artifacts. The relational mechanism decomposition is pinned to workflow `34012983845`, job `101431872354`, artifact `9983093178`, digest `sha256:843a6bdc4a4d4e9de10ce6346cca27a1a863b1780573f000c0f1ab164a81c7ac`. The pathway edge decomposition is pinned to workflow `34014537015`, artifact `9983623440`, digest `sha256:45b38de7514dac8df356579156d994fbc5728e8924308299b2b73571b3595842`. The focused allele-sorting proof is pinned to workflow `34016797940`, job `101441868527`, artifact `9984306657`, digest `sha256:61a07cc6a8680a59185537b03abdca85d0f172a65d068ee9661dd9f2fb448c2d`. The sorting–headroom follow-up is pinned to workflow `34029794984`, artifact `9988541984`, digest `sha256:f8150ea9c7bc8e6e68aff3fbf3a572267204fc7882af11280f360f576fc01f2c`, with prospective protocol commit `07a5d792cf774f08d5495a5f50012b12753e87b4`. The operator-balance route-margin test is pinned to workflow `34127034037`, job `101758021393`, artifact `10021317930`, digest `sha256:1e5ecb658a66e78ffa0ea7eb0cf073323a2173eca7c55461a11aa91b8bd4eb69`, with prospective protocol commit `7d5ae677f5f36d279aae1a7af9707410925ec132`. The last-refuge warning holdout is pinned to workflow `34130457262`, job `101769061070`, artifact `10022340904`, digest `sha256:46a6b03d3d93a0fb5d03c2e9e27b087605b0cf5dda281fd27ed4581ab3640447`, with prospective protocol commit `6377e684799bd4152eec057bfdb78143df0358fc`. Later theorem and manuscript edits do not generate replacement scientific ensembles."""
article = replace_once(article, old, new, "reproducibility pins")

article_path.write_text(article, encoding="utf-8")


# -----------------------------------------------------------------------------
# Cover letter
# -----------------------------------------------------------------------------
cover_path = Path("manuscript/nee_flagship_cover_letter.md")
cover = cover_path.read_text(encoding="utf-8")
old = """It is strictly increasing in q, switches at `q*=0.625`—the same threshold as declared high-trait potential viability—and strictly increases q–allele spatial sorting whenever q varies among patches. In a separately locked **6,000-pair** focused experiment, generation-40 `RR-AA` functional-loss risk was **+6.65 percentage points** with local selection retained but **-0.23 points** when only that edge was deleted. The preregistered DID was **+6.883 percentage points** (95% CI **+5.800 to +7.967**), resolving a single-edge causal contribution to late functional fate."""
new = old + """

A fresh **24,000-trajectory** follow-up then connected that causal edge to the route-reserve coordinate itself: the generation-40 sorting-effect DID replicated at **+8.60 percentage points** `[+7.48,+9.72]`, while the preregistered generation-20 maximum-headroom DID was **+0.0007906** `[+0.0007038,+0.0008775]`. Thus q-dependent sorting changes the depth of the strongest remaining local refuge before the late functional endpoint."""
cover = replace_once(cover, old, new, "cover sorting bridge")

old = """Direct eco-genetic feedback supplies a distinct recoupling route. Defining `B=0.75T+0.25G`, the full support signal is `S=0.6q+0.4B`, so interaction–bundle mismatch contracts by exactly **40%** at the support stage. Relative to q-only, the next-q log-odds shift is `1.8 d(B-q)` under the locked weights. In secondary paired contrasts from the already prospectively locked six-condition experiment, direct feedback benefited the reversed state by **8.53 points** at generation 20 and **7.80 points** at generation 40; the RR-minus-AA buffering-benefit contrasts were **+7.93** (`+3.29,+12.58`) and **+6.33 points** (`+1.85,+10.82`). These are derived paired contrasts, not separately preregistered primary endpoints."""
new = old + """ A separately locked fresh route-duration test prevented over-interpretation: full feedback did not extend above-switch refuge duration (`RR-AA DID=-0.677` generations, 95% CI `-0.694,-0.660`). Recoupling and endpoint persistence are therefore distinct biological estimands."""
cover = replace_once(cover, old, new, "cover recoupling boundary")

old = """The warning analysis provides a monitoring consequence with a positive resolution. Six frozen diversity thresholds precede every observed loss in two independently seeded ensembles but also fire in every non-event, giving specificity zero and binary AUC 0.5. We therefore prospectively froze a separate 12,000-trajectory full-feedback holdout around the continuous reserve of the strongest local eco-genetic refuge. Measured before generation 10, that route-margin score discriminated generation-40 functional loss with AUC **0.92734** (95% CI **0.92433–0.93035**) while only **0.548%** of eventual losses had already occurred, and it added **+0.02135 AUC** (95% CI **+0.01770–+0.02501**) beyond co-timed maximum q. Detecting erosion is therefore not equivalent to identifying fate; local functional reserve is."""
new = """The warning analysis provides a monitoring consequence with a positive resolution. Six frozen diversity thresholds precede every observed loss in two independently seeded ensembles but also fire in every non-event, giving specificity zero and binary AUC 0.5. Even an exact route coordinate showed the same limitation when thresholded: its sign matched the next interaction transition in **1,920,000/1,920,000 patch-generations**, yet the generation-20 all-negative marker again had sensitivity 1, specificity 0 and AUC 0.5 for generation-40 loss. We therefore prospectively froze a separate 12,000-trajectory full-feedback holdout around the **continuous** reserve of the strongest local eco-genetic refuge. Measured before generation 10, that score discriminated generation-40 functional loss with AUC **0.92734** (95% CI **0.92433–0.93035**) while only **0.548%** of eventual losses had already occurred, and it added **+0.02135 AUC** (95% CI **+0.01770–+0.02501**) beyond co-timed maximum q. Being early—or even transition-exact—is therefore not the same as carrying fate information; continuous local reserve is."""
cover = replace_once(cover, old, new, "cover warning representation")
cover_path.write_text(cover, encoding="utf-8")


# -----------------------------------------------------------------------------
# Submission metadata
# -----------------------------------------------------------------------------
meta_path = Path("manuscript/nee_flagship_submission_metadata.md")
meta = meta_path.read_text(encoding="utf-8")
old = """5. Exact q-dependent allele-sorting theorem + prospectively locked focused 6,000-pair single-edge proof.
6. Exact recruitment-buffer, direct-feedback-recoupling and density-gate derivations, each tied only to already locked intervention artifacts.
7. EGWE exact warning-denominator identity + frozen full-denominator diversity audit.
8. Prospectively locked 12,000-trajectory last-refuge warning holdout, with continuous route-margin discrimination and co-timed max-q comparator."""
new = """5. Exact q-dependent allele-sorting theorem + prospectively locked focused 6,000-pair single-edge proof.
6. Prospectively locked 24,000-trajectory sorting–headroom follow-up linking the causal sorting edge to continuous strongest-refuge reserve.
7. Exact operator-balance route-margin theorem + prospectively locked 12,000-trajectory route-duration/full-denominator test.
8. Exact recruitment-buffer, direct-feedback-recoupling and density-gate derivations, each tied only to already locked intervention artifacts.
9. EGWE exact warning-denominator identity + frozen full-denominator diversity audit.
10. Prospectively locked 12,000-trajectory last-refuge warning holdout, with continuous route-margin discrimination and co-timed max-q comparator."""
meta = replace_once(meta, old, new, "metadata evidence hierarchy")

old = """2. **Sorting.** The exact local operator is `logit(p+) - logit(p)=log(0.75+0.4q)`. It switches at `q*=0.625` and increases q–allele spatial sorting whenever q varies. In the separately locked 6,000-pair proof, the g40 baseline `RR-AA` contrast was `+6.65 pp`; deleting only local q-dependent allele selection reduced it to `-0.23 pp`; preregistered DID **+6.883 pp**, 95% CI **+5.800,+7.967**."""
new = old + """ A fresh 24,000-trajectory follow-up replicated the g40 endpoint DID at **+8.60 pp** `[+7.48,+9.72]` and resolved a preregistered g20 maximum-headroom DID of **+0.0007906** `[+0.0007038,+0.0008775]`, linking the same edge to continuous last-refuge reserve."""
meta = replace_once(meta, old, new, "metadata sorting bridge")

old = """4. **Direct recoupling.** Define `B=.75T+.25G`; then `S=.6q+.4B`, so q–bundle mismatch contracts 40% at the support stage. Relative to q-only, the exact next-q logit shift is `1.8*d*(B-q)` under locked weights. Secondary paired contrasts from the prospectively locked six-condition experiment show RR direct-feedback benefits of **+8.53 pp** at g20 and **+7.80 pp** at g40, with RR-minus-AA benefit differences **+7.93 pp** `[+3.29,+12.58]` and **+6.33 pp** `[+1.85,+10.82]`. These are derived contrasts, not separately preregistered primary estimands."""
new = old + """ In a separate fresh prospective route-duration test, however, full feedback shortened rather than extended positive-margin refuge duration: RR-minus-AA extension DID **-0.677 generations** `[-0.694,-0.660]`. Recoupling, route endurance and endpoint persistence are therefore distinct estimands."""
meta = replace_once(meta, old, new, "metadata recoupling boundary")

old = """6. **Warning contrast.** Frozen diversity thresholds can precede every loss while firing in every non-event; specificity 0 and binary AUC 0.5. In a separately prospectively locked 12,000-trajectory holdout, the generation-10 continuous last-refuge route margin discriminated generation-40 functional loss with mean seed-block AUC **0.92734** `[0.92433,0.93035]`. Co-timed max-q AUC was **0.90598** `[0.90078,0.91118]`, and the paired AUC difference was **+0.02135** `[+0.01770,+0.02501]`; only **0.548%** of eventual losses had already occurred at observation. Thus marginal erosion reports stress, whereas strongest-local eco-genetic reserve carries fate information in the finite closure."""
new = """6. **Warning representation contrast.** Frozen diversity thresholds can precede every loss while firing in every non-event; specificity 0 and binary AUC 0.5. The exact operator-balance route margin reproduced its next-transition sign in **1,920,000/1,920,000 patch-generations**, yet its frozen generation-20 all-negative binary marker also had sensitivity 1, specificity 0 and AUC 0.5 for generation-40 loss. In a separately prospectively locked 12,000-trajectory holdout, however, the earlier **continuous** last-refuge route margin discriminated generation-40 functional loss with mean seed-block AUC **0.92734** `[0.92433,0.93035]`. Co-timed max-q AUC was **0.90598** `[0.90078,0.91118]`, and the paired AUC difference was **+0.02135** `[+0.01770,+0.02501]`; only **0.548%** of eventual losses had already occurred at observation. Thus early or transition-exact signals need not be fate-discriminative, whereas strongest-local continuous reserve carries fate information in the finite closure."""
meta = replace_once(meta, old, new, "metadata warning contrast")

old = """- direct-feedback paired benefit contrasts are secondary derivations from an already prospectively locked intervention family, not separately preregistered primary estimands.
- the density headroom threshold and generations are model-specific; density feedback is not claimed to cause the directional sorting advantage.
- last-refuge warning AUC, observation generation and route-margin weights are finite-closure results, not universal natural warning performance or thresholds."""
new = """- direct-feedback paired benefit contrasts are secondary derivations from an already prospectively locked intervention family, not separately preregistered primary estimands.
- the fresh route-duration result explicitly rejects the stronger claim that direct recoupling generically extends above-switch refuge duration.
- the operator-balance route margin is exact for the declared one-step switch but is not a long-horizon sufficient statistic; its generation-20 binary marker is non-discriminative.
- the sorting–headroom pathway is prospectively resolved only in the declared q-only closure and is not a universal natural mediation law.
- the density headroom threshold and generations are model-specific; density feedback is not claimed to cause the directional sorting advantage.
- last-refuge warning AUC, observation generation and route-margin weights are finite-closure results, not universal natural warning performance or thresholds."""
meta = replace_once(meta, old, new, "metadata claim ceilings")
meta_path.write_text(meta, encoding="utf-8")


# -----------------------------------------------------------------------------
# Display plan
# -----------------------------------------------------------------------------
display_path = Path("manuscript/nee_flagship_display_plan.md")
display = display_path.read_text(encoding="utf-8")
display = replace_once(
    display,
    "`cross-layer covariance -> sorting <-> repair (buffering + recoupling) -> density-feedback collapse gate`",
    "`cross-layer covariance -> sorting <-> (trait–allele buffering + interaction–bundle recoupling) -> density-feedback collapse gate`",
    "display central synthesis",
)
display = replace_once(display, "### Panel C — two repair operators", "### Panel C — two mismatch-restoring processes", "display panel C")

old = """- preregistered DID **+6.883 pp** `[+5.800,+7.967]`.

Take-home: q-dependent allele sorting is an exact operator and a resolved single-edge causal contributor."""
new = """- preregistered DID **+6.883 pp** `[+5.800,+7.967]`.
- fresh 24,000-trajectory sorting–headroom follow-up:
  - g40 endpoint DID **+8.60 pp** `[+7.48,+9.72]`;
  - g20 maximum-headroom DID **+0.0007906** `[+0.0007038,+0.0008775]`.

Take-home: q-dependent allele sorting is an exact operator, a resolved single-edge causal contributor, and a prospectively resolved contributor to continuous last-refuge reserve."""
display = replace_once(display, old, new, "display sorting bridge")

old = """Secondary paired contrasts from the prospectively locked six-condition experiment:
- g20 RR direct-feedback benefit **+8.53 pp** `[+5.21,+11.85]`, RR-minus-AA benefit **+7.93 pp** `[+3.29,+12.58]`;
- g40 RR benefit **+7.80 pp** `[+4.79,+10.81]`, benefit difference **+6.33 pp** `[+1.85,+10.82]`.

Take-home: recruitment repairs trait–allele mismatch; direct feedback repairs interaction–bundle mismatch and preferentially buffers the reversed configuration in the locked ensemble."""
new = """Secondary paired contrasts from the prospectively locked six-condition experiment:
- g20 RR direct-feedback benefit **+8.53 pp** `[+5.21,+11.85]`, RR-minus-AA benefit **+7.93 pp** `[+3.29,+12.58]`;
- g40 RR benefit **+7.80 pp** `[+4.79,+10.81]`, benefit difference **+6.33 pp** `[+1.85,+10.82]`.

Fresh prospectively locked route-duration boundary:
- AA full-minus-q-only positive-margin duration **-0.323 generations**;
- RR **-1.000**;
- RR-minus-AA DID **-0.677** `[-0.694,-0.660]`.

Take-home: recruitment buffers trait–allele mismatch; direct feedback recouples interaction toward the local bundle, but that one-step recoupling does not imply generic extension of above-switch refuge duration."""
display = replace_once(display, old, new, "display recoupling boundary")

start = display.index("## Figure 4 — A perfectly early marginal marker can fail to distinguish fate")
end = display.index("## Extended Data / Supplementary information")
new_fig4 = """## Figure 4 — Transition-exact sign can saturate while continuous last-refuge reserve predicts fate

The figure separates **mechanistic exactness, temporal precedence and predictive discrimination**.

### Panel A — marginal erosion is early but non-discriminative

Frozen diversity-warning audit:
- inherited: event leads 35/35; non-event firing 48/48;
- fresh: event leads 33/33; non-event firing 49/49;
- sensitivity = 1, specificity = 0, binary AUC = 0.5.

Take-home: being early is not the same as distinguishing fate.

### Panel B — even an exact route sign can saturate

Operator-balance route margin:

`M=d(0.6q+0.3T+0.1G)-(theta+0.1135168053)`.

Show:
- exact prospective audit: **1,920,000 patch-generations, 0 sign mismatches** for `sign(M)=sign(q_next-.625)`;
- frozen g20 `all M<0` marker -> g40 loss:
  - events 3,943/3,943 marker-positive;
  - non-events 2,057/2,057 marker-positive;
  - sensitivity 1, specificity 0, AUC 0.5.

Take-home: **transition-exactness does not imply fate-predictiveness**.

### Panel C — continuous strongest-refuge depth recovers fate information

Fresh prospectively locked full-feedback holdout, observed before generation 10:
- route-margin AUC **0.92734** `[0.92433,0.93035]`;
- co-timed max-q AUC **0.90598** `[0.90078,0.91118]`;
- paired AUC gain **+0.02135** `[+0.01770,+0.02501]`;
- only **0.548%** of eventual losses had already occurred.

Take-home: the continuous depth of the strongest remaining local eco-genetic refuge retains fate information that marginal and thresholded summaries discard.

### Panel D — representation hierarchy

Conceptual sequence:

`marginal erosion -> stress signal`

`exact route sign -> next-transition state`

`continuous strongest-local reserve -> later-fate ranking`

No single row is a universal natural warning variable; each statement is bounded to the declared finite closure and its frozen observation/endpoint contract.

"""
display = display[:start] + new_fig4 + display[end:]

old = """10. Exact density-feedback headroom theorem and locked paired risk reductions.
11. All six warning endpoints and full-denominator metrics.
12. Evidence-role map and literature-based ecological projection table: limited buffering, movement recoupling, temporal memory and coordinated deterioration."""
new = """10. Exact density-feedback headroom theorem and locked paired risk reductions.
11. Exact operator-balance route-margin theorem, 1.92-million-transition audit and fresh route-duration falsification.
12. Fresh 24,000-trajectory sorting–headroom follow-up and continuous-reserve mediator trajectories.
13. All six diversity-warning endpoints and full-denominator metrics.
14. Fresh continuous last-refuge warning holdout, max-q comparator and seed-block AUC differences.
15. Evidence-role map and literature-based ecological projection table: limited buffering, movement recoupling, temporal memory and coordinated deterioration."""
display = replace_once(display, old, new, "display extended data")
display_path.write_text(display, encoding="utf-8")


# -----------------------------------------------------------------------------
# Source manifest
# -----------------------------------------------------------------------------
manifest_path = Path("manuscript/nee_flagship_source_manifest.json")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["schema_version"] = 7
layers = {entry["layer"] for entry in manifest["load_bearing_sources"]}
new_entries = [
    {
        "layer": "prospective_operator_balance_route_margin",
        "source_type": "prospectively_locked_workflow_artifact_materialized_in_flagship_repository",
        "workflow_run": 34127034037,
        "job": 101758021393,
        "artifact_id": 10021317930,
        "artifact_digest": "sha256:1e5ecb658a66e78ffa0ea7eb0cf073323a2173eca7c55461a11aa91b8bd4eb69",
        "prospective_protocol_commit": "7d5ae677f5f36d279aae1a7af9707410925ec132",
        "scientific_head": "d8b7bf1da9c7f73d872cb93d7ea21547a429d6a6",
        "required_flagship_paths": [
            "experiments/operator_balance_margin_fate_protocol.json",
            "artifacts/operator_balance_route_margin/locked_result.json",
            "docs/OPERATOR_BALANCE_ROUTE_MARGIN_THEOREM_2026-09-06.md",
            "docs/OPERATOR_BALANCE_ROUTE_MARGIN_RESULT_2026-09-07.md",
            "src/eco_genetic_warning_extensions/operator_balance_route_margin.py"
        ],
        "claim_boundary": "The route margin is exact for the declared one-step transition. The fresh route-duration primary result resolved opposite to generic refuge extension, and the generation-20 binary marker had specificity 0/AUC 0.5."
    },
    {
        "layer": "prospective_sorting_headroom_followup",
        "source_type": "prospectively_locked_workflow_artifact_materialized_in_flagship_repository",
        "workflow_run": 34029794984,
        "artifact_id": 9988541984,
        "artifact_digest": "sha256:f8150ea9c7bc8e6e68aff3fbf3a572267204fc7882af11280f360f576fc01f2c",
        "prospective_protocol_commit": "07a5d792cf774f08d5495a5f50012b12753e87b4",
        "scientific_head": "2ef7b256192c63518c6d143e954dadd77527ec82",
        "required_flagship_paths": [
            "experiments/headroom_mediation_followup_protocol.json",
            "artifacts/headroom_mediation_followup/locked_result.json",
            "docs/HEADROOM_MEDIATION_FOLLOWUP_RESULT_2026-09-06.md",
            "src/eco_genetic_warning_extensions/headroom_mediation_followup.py"
        ],
        "claim_boundary": "Both frozen primary requirements resolve selection-to-continuous-headroom-to-fate propagation only in the declared q-only closure; this is not a universal natural mediation law."
    },
    {
        "layer": "prospective_continuous_last_refuge_warning_holdout",
        "source_type": "prospectively_locked_workflow_artifact_materialized_in_flagship_repository",
        "workflow_run": 34130457262,
        "job": 101769061070,
        "artifact_id": 10022340904,
        "artifact_digest": "sha256:46a6b03d3d93a0fb5d03c2e9e27b087605b0cf5dda281fd27ed4581ab3640447",
        "prospective_protocol_commit": "6377e684799bd4152eec057bfdb78143df0358fc",
        "required_flagship_paths": [
            "experiments/last_refuge_warning_holdout_protocol.json",
            "docs/LAST_REFUGE_WARNING_HOLDOUT_RESULTS_2026-09-07.md",
            "src/eco_genetic_warning_extensions/last_refuge_warning_holdout.py",
            "scripts/run_last_refuge_warning_holdout.py",
            "tests/test_last_refuge_warning_holdout.py"
        ],
        "claim_boundary": "The AUC, observation time, route-margin weights and incremental ranking result apply only to the frozen full-feedback finite holdout and endpoint."
    }
]
for entry in new_entries:
    if entry["layer"] not in layers:
        manifest["load_bearing_sources"].append(entry)

firewalls = manifest["claim_firewalls"]
for statement in [
    "The operator-balance route margin is exact for the declared one-step switch but is not a long-horizon sufficient statistic.",
    "The fresh route-duration experiment rejects the stronger claim that direct recoupling generically extends positive-margin refuge duration; recoupling, route endurance and endpoint persistence are distinct estimands.",
    "A transition-exact generation-20 all-negative route marker can have sensitivity 1, specificity 0 and AUC 0.5; transition exactness is not fate predictiveness.",
    "The sorting-headroom follow-up supports q-dependent selection to continuous-reserve to fate propagation only in the declared q-only closure.",
    "The continuous last-refuge warning AUC and incremental ranking beyond max q are bounded to the prospectively frozen full-feedback holdout, observation time and endpoint."
]:
    if statement not in firewalls:
        firewalls.append(statement)

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print("NEE route-reserve causal bridge integration: PASS")
