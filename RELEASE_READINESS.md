# Release readiness

This ledger separates repository facts that are already fixed from metadata decisions that require explicit author approval. It does not change the scientific evidence or release version.

## Ready now

- [x] one active EGWE NEE flagship lane plus two frozen non-simultaneous fallbacks are fixed in `manuscript/publication_lanes.json` schema 5
- [x] warning-validity title is **Event-conditioned temporal precedence is not predictive warning validity**
- [x] state-validity title is **Matching eco-genetic summaries can hide different ecological futures**
- [x] state-validity manuscript is separated from warning-validity and migrated natural-data claims
- [x] state-validity external bibliography is isolated in `manuscript/state_validity_references.md`
- [x] state-validity Ecology Letters cover letter is lane-specific and no longer contains warning denominators or natural-data results
- [x] the original Phase-V 500-pair generation-60 contrast remains frozen rather than retrospectively rewritten
- [x] the separately prospectively locked post-Phase-V propagation experiment reports all declared horizons `5, 10, 20, 40` and nested paired prefixes `500, 1000, 1500`
- [x] the primary 1,500-pair propagation curve reports anti-aligned minus aligned loss-risk differences of `0.0`, `+0.33`, `+5.33`, and `+5.20` percentage points at generations 5, 10, 20 and 40
- [x] claim ceiling explicitly prohibits a universal generation-20 cutoff or natural-system timescale
- [x] the former integrated `manuscript/main_text.md` remains a non-submission source archive
- [x] natural-data four-gate reader-facing development is authoritative in `zuizui0223/egwee`
- [x] `manuscript/nee_flagship_submission_metadata.md` contains current flagship availability/governance metadata plus a reviewable AI/automated-tool disclosure draft
- [x] parent evidence pins are explicit: Protocol-002/reproducibility remains at `dd8ee379d0d3518194c767d16402042525bc00dc`, while NEE Question-1 fragmentation evidence is pinned to `b7ee738767c92307d6d23a85a3eeb857faf6ddfb`
- [x] software licence is MIT in both model repositories
- [x] package version is `0.1.0` in both model repositories
- [x] no final immutable citation/release record is created before author approval
- [x] third-party raw data are not committed; source provenance and compact derived results are retained where analyses ran
- [x] scientific stop rules prohibit outcome-informed simulator, warning or empirical retuning
- [x] NEE journal-specific AI-policy ambiguity was rechecked and resolved on 2026-10-06; remaining AI work is disclosure/accountability approval, not eligibility clarification

### Current scientific source of truth

The active submission is the **Nature Ecology & Evolution flagship**, not the historical state-validity fallback.

Its evidence spine is:

1. **Question 1 — state separation under fragmentation:** the fixed-area fragmentation gradient and canonical interaction geometry are pinned to the parent evidence commit `b7ee738...`.
2. **Question 2 — hidden organization and operator balance:** matched-marginal transition insufficiency, q-dependent allele sorting, recruitment buffering, direct recoupling and the density-feedback failure gate are tied to locked finite-model experiments and exact derivations.
3. **Warning/reserve:** frozen marginal diversity thresholds are non-discriminative, whereas the prospectively locked continuous last-refuge margin gives AUC `0.92734` and `+0.02135` AUC beyond co-timed max q in the declared holdout.
4. **Post-hoc audits remain non-load-bearing:** last-refuge component decomposition and headroom effect scaling are explicitly exploratory/descriptive and do not alter preregistered estimands.
5. **Natural evidence is bounded external consistency only:** EGWEE currently contributes five primary clusters / 17 marginal effects with explicit ML001 and covariance-certification limits; the natural strongest-refuge transfer remains a null portability boundary.

The active manuscript, source manifest and machine publication router are the governing reader-facing surfaces. Historical state- and warning-validity manuscripts remain frozen fallbacks.

### Repository validation

The EG-series publication roadmap is merged and assigns distinct ownership to mechanism/state separation (EGC), state representation/propagation (EGWE state), warning validity (EGWE warning), and natural-data measurement gates (EGWEE).

Final NEE flagship validation must be rerun after any title, cover-letter, metadata, reference, policy or release synchronization. Scientific locked outputs are not rerun or retuned by editorial changes.

## Author approval required before citation/release metadata can be finalized

- [ ] final NEE flagship manuscript title approved by all authors
- [ ] complete author names and order
- [ ] affiliations and corresponding author
- [ ] author ORCIDs
- [ ] CRediT contributor statements
- [ ] funding / grant identifiers
- [ ] acknowledgements
- [ ] conflict-of-interest declaration
- [ ] final AI/automated-tool disclosure, including exact materially used tool/model versions as required at submission
- [ ] licence for manuscript text, figures, tables, and other non-software outputs
- [ ] confirm whether release version remains `0.1.0` or is promoted for submission/archive
- [ ] approve repository descriptions/topics/homepage wording

`CITATION.cff` is intentionally not generated before these author-controlled fields are approved. Do not infer author identity, author order, ORCIDs, contributions, funding, conflicts or output licensing from repository ownership or commit metadata.

## After author approval

1. Add coordinated `CITATION.cff` files to parent and extension with explicit repository roles.
2. Confirm package/release version and update version fields only if approved.
3. Apply approved repository descriptions/topics/homepage wording.
4. Run the full two-repository submission workflow on the final metadata commit.
5. Create coordinated immutable Git tags/releases.
6. Deposit the release/submission package in Zenodo or an equivalent archive.
7. Record concept DOI and version DOI(s), then add them to README, citation metadata, cover letter, and manuscript data/code availability.
8. Freeze and record the final release bundle digest.

## Repository roles for future citation metadata

### `eco-genetic-criticality`

Mechanistic evidence parent for **NEE Question 1**: theorem-guided interaction/fragmentation framework, finite-model evidence ledger, and biological-state separation. Its standalone manuscript is retained as provenance/fallback rather than a separate active submission; forecast sufficiency and predictive warning validity belong to NEE Question 2 in EGWE.

### `egwe`

Owns one active NEE flagship submission lane integrating state representation, operator-resolved mechanism and warning representation, with state/warning standalone manuscripts retained as frozen fallbacks. The integrated source archive remains provenance only.

### `egwee`

Owns the independent natural-data measurement/representation/residual-context/identifiability four-gate manuscript.

## Release gate

Do not create a final citation record, immutable release tag, GitHub Release or archive DOI until the author-controlled metadata above are explicitly approved. Remaining immutable-release blockers are authorship/citation metadata, disclosure/licensing decisions and archival approval, not unresolved simulator tuning.
