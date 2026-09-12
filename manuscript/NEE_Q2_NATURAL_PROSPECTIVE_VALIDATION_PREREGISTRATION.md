# Preregistration — natural-system Q2 test of joint local reserve beyond marginal state

**Frozen before project-level inspection of any response value from the locked archive.**

## Purpose

The active NEE manuscript has two logically distinct parts. Question 1 asks whether fragmentation produces one biological deterioration state. Question 2 asks what determines divergent functional futures once biological layers separate. The finite model establishes that marginal ecological/genetic summaries can be transition-insufficient and that a continuous strongest-local-refuge reserve can carry fate information beyond a co-timed marginal interaction summary. Those positive mechanisms remain closure-specific.

This preregistration opens one external natural-system test aimed specifically at the reviewer-facing gap in Question 2:

> **Does the spatial pairing of local resource support and realised pollinator interaction carry held-out information about later reproductive function beyond fragmentation context and the marginal distributions of those same two layers?**

The primary natural estimand is deliberately narrower than the finite model. It does not test q-dependent allele selection, recruitment buffering, direct eco-genetic recoupling, density feedback, or the numerical route-margin threshold. It tests the more portable prediction that **joint local organization / strongest joint reserve can matter beyond layer-wise marginal state**.

## Prospective status

This is a **prospectively locked reanalysis of an existing natural archive**, not prospective field data collection. The source paper is already published and its reported SEM-level conclusions are public. However, before this preregistration the project has not computed the locked cross-layer organization metric, the locked strongest-joint-reserve metric, or their held-out incremental predictive score from this archive.

Published source conclusions may not be used to tune signs, thresholds, species subsets, endpoints, transformations, or validation units.

## Locked source

Primary system:

- Lázaro, Fuster, Alomar & Totland (2020), *Ecological Applications* 30:e02099, doi:`10.1002/eap.2099`;
- Dryad dataset doi:`10.5061/dryad.d51c59zzj`;
- locked file: `Visitation&Seedsetdata_Dryad.xlsx`.

The source study contains 24 habitat fragments in southern Norway and reports pollinator/community measurements together with visitation and seed-production responses for four focal plant species. No alternative natural system may replace this source inside this preregistered test after row-level inspection begins.

## Stage A — response-blind schema gate

Before any data value is read, Stage A may inspect only:

- Dryad dataset/version/file metadata;
- file byte size and digest;
- workbook sheet names;
- the first/header row of each sheet;
- source-paper variable definitions and sampling design;
- row counts only if they can be obtained without reading cell values.

Stage A must not inspect predictor values, response values, effect directions, correlations, missingness patterns conditional on response, model fits, or species-specific outcome performance.

### Stage-A eligibility

The archive advances only if headers/source definitions establish all of the following without inventing a join:

1. an independent habitat-fragment/site identifier;
2. focal-species identity or an equivalent source-defined key;
3. a local resource/support coordinate measured before or during pollination (e.g. focal or local floral abundance);
4. a realised pollinator-interaction coordinate (visitation or an explicitly source-defined visitation rate);
5. a later realised reproductive-function endpoint, with **seed set** the primary endpoint family;
6. a source-defined mapping that permits resource and interaction measurements to be paired at repeated local observation units within `fragment × species`, rather than only as one already-aggregated marginal value.

If items 1–5 are present but item 6 is absent, the decision is:

`joint_local_organization_not_identifiable_from_archive`

and the Q2 natural validation stops. The project must not substitute a between-fragment correlation and call it cross-layer organization.

If the outcome cannot be mapped without a new key or if only a different reproductive endpoint is reusable, the decision is:

`locked_function_endpoint_not_identifiable`

and the test stops. Seed mass is not a rescue endpoint for a failed/missing seed-set representation.

## Stage B — exact analysis contract, frozen before response values

If Stage A passes, a second contract must be committed before any seed-set value is read. Stage B may use predictor-only rows to establish deterministic grouping and effort denominators, but response values remain firewalled until the complete model and scoring contract is committed.

The following scientific structure is already fixed and may not be changed in Stage B.

### Analysis unit and holdout

- biological prediction unit: `fragment × focal species`;
- independent validation unit: **whole habitat fragment**;
- all rows, species and repeated observations from one fragment are held out together;
- no random row split is permitted.

If fewer than 15 independent fragments survive only preregistered structural validity checks, the primary held-out test is classified `insufficient_independent_fragments` rather than repaired by row-level cross-validation.

### Layer definitions

Let local observation unit `j` within fragment-species unit `u` have:

- `D_uj`: source-defined local floral/resource support;
- `I_uj`: source-defined realised pollinator visitation, effort-standardised only by a source-defined observation effort denominator.

No pollinator taxon may be selected after observing reproductive outcomes. If the source defines a legitimate-visit subset independently of outcomes, that definition may be used only if frozen in Stage B before response values.

### Marginal-state baseline

The baseline representation contains fragmentation/context terms declared by the source design plus **unpaired** summaries of the two focal layers. At minimum it contains, for both `D` and `I`, their fragment-species mean and maximum after the fixed Stage-B transformation. If Stage A shows that a variance/dispersion summary is source-identifiable with adequate repeated units, it may be included, but the same summaries must be used in every fold and cannot be selected by performance.

The baseline is deliberately allowed to know the strongest local resource value and strongest local interaction value **separately**. Therefore the organization test cannot win merely because it sees a univariate maximum that the marginal model was denied.

### Primary joint-reserve statistic

The primary additional statistic is the strongest co-located resource–interaction reserve:

`R_joint(u) = max_j min(P_D(D_uj), P_I(I_uj))`

where `P_D` and `P_I` are monotone training-fold empirical percentile transforms estimated from the training fragments only and then applied unchanged to the held-out fragment.

Properties fixed by design:

- `R_joint` is bounded in `[0,1]`;
- high values require at least one local observation unit where **both** resource support and realised interaction are high;
- separate marginal maxima can both be high while `R_joint` is low if they occur in different local units;
- no finite-model operator weights or threshold values are imported into nature.

This is the natural analogue of “strongest remaining local refuge,” not a claim that it is numerically equivalent to the finite route margin.

### Exact marginal-preservation diagnostic

Within each fragment-species unit, a pairing-permutation diagnostic will independently permute `I_uj` labels over the observed local units while leaving the exact `D` and `I` marginal values unchanged. This produces the null distribution of `R_joint` under destroyed cross-layer organization.

This diagnostic is structural only. It cannot be used to choose a favorable transformation or to define the sign of the outcome test.

## Primary predictive comparison

The only confirmatory comparison is:

- `M0`: later seed-set function predicted from species + source-defined fragmentation/context + locked marginal-state summaries;
- `M1`: the identical model plus `R_joint`.

Model family, link, exact seed-set representation, and any exposure denominator must be fixed in the Stage-B contract from source definitions/header types before response values are read.

All preprocessing is fit on training fragments only. Any regularization strength, if needed, must be fixed a priori or selected entirely within nested training data; the held-out fragment cannot tune it.

For each held-out fragment calculate the preregistered proper predictive loss. Define:

`delta_joint = loss(M1) - loss(M0)`.

Negative values favor joint local reserve.

The total primary score is the sum (or equal-fragment-weighted mean, fixed in Stage B according to the response likelihood) of fragment-level `delta_joint` values.

A deterministic fragment bootstrap will resample the independent fragment-level deltas with replacement using seed `20260912` and `10,000` draws.

The confirmatory decision **`joint_local_reserve_adds_heldout_information`** requires both:

1. total/equal-weighted `delta_joint < 0`; and
2. the bootstrap 95% upper bound for `delta_joint < 0`.

Otherwise the decision is **`no_detected_incremental_joint_reserve_information`**.

No p-value, alternative metric, favorable species, or endpoint can replace this decision.

## Secondary descriptive outputs

These are reported regardless of the primary result but cannot rescue it:

- observed `R_joint` by fragment/species;
- within-unit marginal-preserving permutation distribution of `R_joint`;
- held-out predictions from `M0` and `M1`;
- fragment-level score deltas;
- species-stratified deltas shown descriptively with no species cherry-picking;
- a cross-layer organization coefficient, if Stage A supports repeated aligned units, reported as a secondary descriptive statistic rather than a second confirmatory test.

Seed mass and source-reported aggregate visitation–seed associations remain descriptive/source-context material only.

## Hard stop and no-rescue rules

After response values are opened, do not:

- change the natural system;
- redefine the primary reproductive endpoint;
- choose one or more of the four focal species because they perform better;
- replace whole-fragment holdout with row-level CV;
- tune resource/interaction weights against seed set;
- choose a percentile threshold or top-k rule after seeing the outcome;
- drop low-performing fragments or observation units based on outcome magnitude;
- replace realised visitation with richness/evenness or a pollinator subgroup because the primary test is weak;
- import the finite-model q threshold, route-margin coefficients, generation horizon, or AUC benchmark;
- claim that a failure of this archive falsifies the finite mechanism family.

Structural exclusions are allowed only for predeclared invalidity such as missing identifiers, impossible/non-finite values, non-positive required effort denominators, or inability to join source-defined keys. Every exclusion must be recorded before model scoring.

## Claim ceiling

### If positive

A positive primary result would support the following natural-system statement:

> In this fragmented plant–pollinator system, the strongest co-located local resource–interaction reserve carries reproducible held-out information about later reproductive function beyond fragmentation context and the declared marginal summaries of the same layers.

That would be a direct empirical counterpart to NEE Question 2’s state-representation argument: layer-wise marginals need not exhaust fate-relevant information when local cross-layer organization is retained.

It would **not** validate q-dependent allele sorting, recruitment buffering, direct recoupling, density feedback, genetic state variables, or any numerical finite-model threshold/AUC.

### If null/adverse

A null or adverse result would mean only that this predeclared natural representation did not earn incremental held-out predictive information in this archive. It would remain scientifically useful because it limits the external portability of the strongest-refuge idea and prevents the NEE Discussion from implying validation that was not obtained.

## Relationship to EGWEE

EGWEE remains the broad empirical synthesis of fragmentation-driven cross-layer state separation and moderators. This test has a different role: it is a **single-system, held-out, representation-level Q2 validation attempt**. Its result must not be pooled into the EGWEE meta-analysis merely to strengthen the NEE paper, and the EGWEE synthesis must not be used as a fallback if this test fails.
