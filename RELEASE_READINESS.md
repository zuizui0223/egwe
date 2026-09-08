# Release readiness

This ledger separates repository facts that are already fixed from metadata decisions that require explicit author approval. It does not change the scientific evidence or release version.

## Ready now

- [x] one active EGWE NEE flagship lane plus two frozen non-simultaneous fallbacks are fixed in `manuscript/publication_lanes.json` schema 4
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
- [x] `manuscript/submission_metadata.md` contains lane-specific state-validity availability wording plus a reviewable AI/automated-tool disclosure draft
- [x] parent scientific commit used by the extension is pinned: `dd8ee379d0d3518194c767d16402042525bc00dc`
- [x] software licence is MIT in both model repositories
- [x] package version is `0.1.0` in both model repositories
- [x] no final immutable citation/release record is created before author approval
- [x] third-party raw data are not committed; source provenance and compact derived results are retained where analyses ran
- [x] scientific stop rules prohibit outcome-informed simulator, warning or empirical retuning

### Current scientific source of truth

The state-validity lane uses two explicitly separate evidence layers.

1. **Original Phase V:** fixed 500 paired trajectories at generation 60; anti-aligned minus aligned loss-risk difference `+4.4` percentage points with paired 95% CI approximately `[-1.2, +10.0]`. This remains an imprecise frozen result, not an equivalence claim.
2. **Post-Phase-V propagation experiment:** separately locked before outcome access; one common forcing path, fixed readouts at generations 5/10/20/40, and nested 500/1000/1500 paired prefixes. In the primary 1,500-pair curve, the generation-20 and generation-40 contrasts are `+5.33` pp [2.04, 8.62] and `+5.20` pp [1.96, 8.44].

The propagation protocol and result are recorded in `experiments/alignment_propagation_protocol.json`, `artifacts/alignment_propagation/locked_summary.json`, and `docs/ALIGNMENT_PROPAGATION_RESULT_2026-09-04.md`.

### Repository validation

The EG-series publication roadmap is merged and assigns distinct ownership to mechanism/state separation (EGC), state representation/propagation (EGWE state), warning validity (EGWE warning), and natural-data measurement gates (EGWEE).

Final validation for this state-validity submission branch must be rerun after title, cover-letter, metadata and reference synchronization. The scientific propagation outputs themselves are already locked and are not rerun by editorial changes.

## Author approval required before citation/release metadata can be finalized

- [ ] final state-validity manuscript title approved by all authors
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

Mechanistic parent: theorem-guided interaction/fragmentation framework, finite-model evidence ledger, and biological-state separation. Its standalone manuscript does not own forecast sufficiency or predictive warning validity.

### `eco-genetic-warning-extensions`

Owns one active NEE flagship submission lane integrating state representation, operator-resolved mechanism and warning representation, with state/warning standalone manuscripts retained as frozen fallbacks. The integrated source archive remains provenance only.

### `egwee`

Owns the independent natural-data measurement/representation/residual-context/identifiability four-gate manuscript.

## Release gate

Do not create a final citation record, immutable release tag, GitHub Release or archive DOI until the author-controlled metadata above are explicitly approved. Remaining immutable-release blockers are authorship/citation metadata, disclosure/licensing decisions and archival approval, not unresolved simulator tuning.
