# Eco-genetic warning extensions

This repository tests **which eco-genetic state representations are future-relevant, and whether candidate measurements preserve enough information for prediction**. It is the condition-recovery, warning-audit, and natural state-sufficiency extension of [`eco-genetic-criticality`](https://github.com/zuizui0223/eco-genetic-criticality), pinned at scientific commit `dd8ee379d0d3518194c767d16402042525bc00dc`.

## Publication routing

There is **one active EGWE submission lane**: [`manuscript/nee_flagship_article.md`](manuscript/nee_flagship_article.md), currently routed to **Nature Ecology & Evolution**. The standalone state-validity and warning-validity manuscripts are **frozen fallback** packages and must not be submitted simultaneously with the overlapping flagship.

The binding machine router is [`manuscript/publication_lanes.json`](manuscript/publication_lanes.json); the human-readable contract is [`manuscript/PUBLICATION_LANES.md`](manuscript/PUBLICATION_LANES.md); the current operational status is [`manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`](manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md).

### Publication crosswalk

| programme layer | scientific question | current surface | status |
|---|---|---|---|
| EGC | what biological states separate under fragmentation? | `zuizui0223/eco-genetic-criticality` | independent parent paper |
| EGWE state | what representation preserves future-relevant distinctions? | evidence incorporated into `nee_flagship_article.md`; standalone state manuscript retained | frozen fallback |
| EGWE warning | when is an early signal actually fate-discriminative? | binary audit + continuous last-refuge holdout in `nee_flagship_article.md`; standalone warning manuscript retained | frozen fallback |
| EGWEE | when does an empirical measurement earn state/proxy status? | `zuizui0223/egwee` | independent empirical programme |
| EGWE flagship | how do representation, operators and strongest-local reserve jointly determine vulnerability and predictability? | `nee_flagship_article.md` | **active primary submission** |

The four-layer series remains a useful **scientific decomposition**. It is not a declaration that all four component manuscripts are simultaneously active. `manuscript/main_text.md` is an integrated source archive, and `manuscript/grand_synthesis_flagship.md` is the superseded initial flagship spine.

## Central result

The current synthesis is:

> **Reproducibility belongs to a loss-generating state, not to a habitat label or a genetic statistic by itself. Candidate empirical state variables must themselves demonstrate endpoint-relevant predictive information.**

Under the declared simulator Markov closure, equality of the complete current explicit state plus the future forcing/stochastic law is future-sufficient. Coarse ecological and genetic marginals are not generally sufficient: two states can share census, interaction and allele-frequency marginals, realised trait-bin state, `H_alpha`, `H_gamma`, and `F_ST`, yet differ in the next transition because cross-layer spatial alignment differs.

The empirical counterpart is therefore ordered as:

```text
candidate-state adequacy
        ↓
residual origin / history test
        ↓
only then: cross-system regime comparison
```

A biologically plausible or spatially proximal variable is not granted state status by assumption.

## Current scientific state

### Functional fragmentation

Fragmenting the same prepared full state lowers interaction, local effective size, and realised high-trait mass before demographic disappearance. In the fixed-area gradient, the first 1→2 split reduced median interaction by about 99.8%, local effective size by 77.9%, and realised high-trait mass by 71.7%.

### Loss-process calibration

**Source feasibility is conditional:** `2,269/3,375` original recurrent-transition source attempts supported preparation/projection. The original R1–R4 block-rate labels remain historical protocol provenance, not biological regimes. High-precision replay separates pooled functional-loss incidence, between-block heterogeneity, and paired trajectory identity.

The recurrent-turnover frontier spans pooled loss from about `.682` at `p_star=.325` through `.407` at `.375` to `.273` at `.400`, without detected excess block heterogeneity at the tested frontier coordinates.

### Connectivity is process-specific

The historical allele-frequency-mixing `m=.10` equal-rate signal did not reproduce in one independent fresh Phase-U ensemble and did not port to whole-individual or pollen-only movement closures. No robust portable connectivity heterogeneity effect is established.

`migration_rate` in the legacy operator means **allele-frequency mixing only**. It is not demographic migration, pollen or seed dispersal, pollinator movement, or recolonisation.

`interaction kappa` is an aggregate positive-feedback/effective-interaction-support parameter. It is **not partner richness**, connectance, pollinator diversity, or network dimensionality.

### State representation matters

A constructive aligned versus anti-aligned pair held the declared coarse marginals fixed while reversing patchwise interaction–genetic/trait alignment. The exact next interaction transition differed by as much as `0.2543`, demonstrating transition-level insufficiency of the coarse summaries. The fixed 60-generation campaign did not establish a directional long-horizon loss-incidence effect (`0.678` versus `0.722`; McNemar `p=.143`).

### Relative warning ordering reproduced but failed discrimination

In the inherited symmetric benchmark, all 35 event trajectories showed baseline-relative `H_alpha/H_gamma` erosion before realised functional loss at each of six 5/10/20% endpoints. A prospectively fixed fresh ensemble reproduced that ordering at **33/33** losses.

The full-denominator audit changed the interpretation: all six thresholds also fired in **48/48** inherited and **49/49** fresh non-event trajectories. Full-horizon specificity was zero and binary-marker AUC was 0.5. This supports replicated **event-conditional ordering**, not predictive warning validity or a universal percentage threshold.

### Closed condition-map invariants retained for release

The historical calibration language is kept explicit so release-facing summaries cannot silently turn screen labels or one finite seed-family result into biology:

- **Historical R3 is not automatically “seed heterogeneity”.** Historical R3/R4 remain warning-blind screen labels, not biological regimes.
- In the aggregate-feedback precision replay, **pooled loss is `.499/.573/.598`** at `kappa=3.0/4.5/6.0` and the tested conditions remained block-homogeneous.
- The **historical `m=.10` connectivity signal did not freshly replicate**. In the independent Phase-U ensemble, **fresh `m=0/.10` equal-rate p values were `.134/.745`**, pooled loss was `.540/.551`, and paired McNemar `p=.694`.
- **No robust portable connectivity heterogeneity effect is established** across the tested allele-only, whole-individual, and pollen-only closures.
- Reduced-form and matched-expected-support partner tests were bounded negative results; the **adaptive-rewiring gate remains closed**.
- **The frozen relative thresholds are not validated predictors**: event-conditional ordering reproduced, but non-event false-positive rate was 1.0 in both ensembles.

## Natural-data programme

Natural systems are not pooled. Each test preserves its own ecological unit and holds out whole ecological units when evaluating transferable prediction.

### Honshu–Izu: residual geography became redundant after a functional partial state

For the 40 network states of Hiraiwa & Ushimaru (2024), the functional-state model using community trait matching and pollinator functional diversity had held-out MSE `1.08774`. Adding mainland distance increased it to `1.13209` (**4.08% worse**) and improved only `3/8` held-out sites.

Decision: `ecological_partial_state_convergence_supported`, with a strong completeness caveat. This does not establish that the measured state is complete.

### Zurich: no reproducible residual urban information

Across six fixed reproductive endpoints and whole-garden validation, `0/6` endpoints met the preregistered positive residual-context rule after the function-specific pollinator interaction state was supplied.

This does not imply that urbanisation is biologically irrelevant.

### Oenothera: a missing mating-connectivity coordinate remained

In *Oenothera harringtonii*, adding standardized maternal spatial isolation after pollinator treatment reduced leave-one-maternal-plant-out MSE from `0.11619` to `0.09187`, a **20.93% improvement**. The treatment-profile-preserving 10,000-permutation test gave `p=0.00130`.

Decision: `residual_isolation_detected`.

This is a `C/G_mating` result, not direct ecological functional loss. It shows that pollinator treatment alone did not close the contemporary mating state.

### Eschscholzia: a plausible pollinator proxy did not earn general state status

Four EIDC products from the same 2015 Hillesden experiment were synchronized prospectively at `Block -> Experimental array -> focal plant -> fruit/progeny`. The candidate array-level pollinator state was fixed as `log1p(pan-trap count) + mean ITD`, with leave-one-array-out validation.

The primary multi-endpoint test was `multi_endpoint_not_identifiable` because the preregistered exact metadata-consistency gate closed the direct seed-function endpoint on `Fallow ground` versus `Fallow graound`. A prospectively declared F-only sensitivity permitted the correction only at `1||3`; pre-model metadata inspection found the same mismatch at `1||4`, so it stopped without fitting F. The primary lock remains unchanged and no sensitivity estimate exists.

For the estimable endpoints, the candidate pan-trap state did not show reproducible held-out gain for either mating (`G_mating`) or outcross pollen movement (`C_pollen`). This is a **measurement boundary**: pan-trap availability/trait summaries are not automatically equivalent to effective interaction.

### Access boundaries are not ecological nulls

Prospectively attractive systems in Southern Norway, *Miconia affinis*, Witheringia, and wild *Antirrhinum* reached archive-access stop rules before the required source snapshot or schema could be reproduced. These are retained as access/non-identifiability results and are not promoted to project-generated ecological findings.

## Empirical search basis

The current candidate natural state is

```text
S_emp(t) = {D, I, T, C, R, G_by_cohort, F_baseline, M, A}_t
```

where the practical sampling unit is population/site × observation window × relevant cohort. The symbols are a search basis, **not assumed sufficient statistics**.

Current natural process anchors include:

- *Crepis sancta*: interaction-limited local fragmentation;
- Miyake-jima *Camellia–Zosterops*: movement-compensated local fragmentation;
- *Conospermum undulatum*: cohort/history lag;
- *Spondias purpurea*: near-synchronised `I -> C -> F -> cohort G` deterioration;
- Honshu–Izu: trait matching and functional diversity rather than richness alone;
- *Oenothera*: residual spatial mating opportunity after pollinator treatment;
- *Eschscholzia*: candidate pollinator availability/ITD proxy not predictively sufficient for the estimable G/C endpoints.

These are process templates and measurement boundaries, not universal numerical classes.

## Urban and island translation

Urban and island systems are contrasting routes through the condition space, not ecological equivalents.

The operational question is not “urban or island?” but:

> **Do different fragmentation mechanisms become predictively equivalent after conditioning on a measured future-relevant ecological state?**

Formally, a candidate cross-system state is supported only when origin/history no longer improves prediction of the future endpoint after that state is supplied. If origin/history still matters, the next task is to search for a missing process, cohort, alignment, compensation, or memory coordinate.

## Scientific sources of truth

For current publication decisions, use this order:

1. `manuscript/publication_lanes.json` — binding submission state, exclusivity and fallback reactivation rules;
2. `manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md` and `manuscript/PUBLICATION_LANES.md` — human-readable operational routing;
3. the active flagship (`nee_flagship_article.md` + `nee_flagship_source_manifest.json`) and its locked artifacts/result notes.

`claim_evidence_map.md`, `artifact_index.md`, hypothesis ledgers and historical phase/status documents remain provenance/evidence maps; they do not override the current submission router. `main_text.md` and `grand_synthesis_flagship.md` are archives, not active competing manuscripts.

## Reproduce and package

The package version is currently `0.1.0`. Start with [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) for the two-repository scientific lock and submission build.

A lightweight local check is:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev,reproducibility]'
python -m pytest
```

Third-party natural raw data are not committed. Where a project-generated empirical analysis was possible, DOI/version or exact member-level provenance and compact derived results are retained.

Release-readiness status is tracked in [`RELEASE_READINESS.md`](RELEASE_READINESS.md) and issue #53.

## Stop rules

- Do not tune simulator parameters, seeds, migration rates, interaction feedback, partner weights, or warning thresholds merely to obtain a preferred result.
- Do not inspect warning/diversity fields while selecting or replicating C2 loss conditions.
- Do not reinterpret historical R1–R4 labels as biological regimes.
- Do not call allele-frequency mixing demographic, pollen, seed, or pollinator movement.
- Do not promote archive-access failure to an ecological null.
- Do not repair a prospectively locked empirical mismatch after seeing its consequence merely to recover identifiability.
- Do not treat any plausible ecological proxy as a sufficient state unless it demonstrates endpoint-relevant predictive information.
- If a result fails to generalise or replicate, report the recovered condition or boundary instead of tuning until the preferred result appears.
