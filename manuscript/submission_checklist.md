# Submission readiness checklist

## Publication routing

- [x] Exactly **one active EGWE submission lane** is declared in `publication_lanes.json`: the NEE flagship.
- [x] `nee_flagship_article.md` is the active primary manuscript.
- [x] `warning_validity.md` is a **frozen fallback**, not a simultaneous active submission.
- [x] `state_validity_and_empirical_measurement_gates.md` is a **frozen fallback**, not a simultaneous active submission.
- [x] The flagship overlap contract explicitly registers reused state evidence (`0.2543`, `+5.33`, `+5.20`) and reused warning evidence (`35/35`, `48/48`, `33/33`, `49/49`, specificity 0, AUC 0.5).
- [x] Flagship-only load-bearing evidence is explicitly registered: sorting-edge DID, sorting–headroom follow-up, exact route-margin audit, and continuous last-refuge holdout.
- [x] The exclusivity policy blocks simultaneous submission of the overlapping state/warning fallbacks while the flagship is under consideration.
- [x] `main_text.md` remains an integrated source archive, not another submission.
- [x] `grand_synthesis_flagship.md` is a historical initial spine, superseded by `nee_flagship_article.md`.

## Warning-evidence completeness

- [x] Frozen binary thresholds retain their full event/non-event denominators and specificity/AUC boundary.
- [x] The later prospectively locked last-refuge holdout is part of the active flagship evidence base.
- [x] Route-margin AUC `0.92734` `[0.92433,0.93035]` and incremental AUC `+0.02135` `[+0.01770,+0.02501]` are reported.
- [x] The full predeclared comparator panel is reported, including `H_alpha` AUC `0.23253` under the frozen lower-is-higher-risk orientation.
- [x] The `H_alpha` result is described as **directionally inverted**; its sign is not flipped post hoc to create a successful warning score.
- [x] A standalone warning manuscript cannot be reactivated without incorporating or explicitly reporting this later holdout evidence.

## Scientific integrity

- [x] Frozen endpoints, seeds, schedules, thresholds and operator weights are unchanged.
- [x] Parent and extension trajectories are not pooled.
- [x] Non-significant results are not treated as equivalence.
- [x] Natural datasets are not used as validation of the finite closure.
- [x] Access failures and `not_identifiable`/`not_estimable` outcomes remain visible.
- [x] Natural-data development is authoritative in `zuizui0223/egwee`.

## NEE flagship package

- [x] Article, references, cover letter, display plan, source manifest and submission metadata exist.
- [x] NEE compliance checker passes the working abstract/main-text/display/reference limits.
- [x] Four main figures are generated from locked evidence.
- [x] Figure 4 separates marginal stress sensitivity, transition-exact binary saturation and continuous reserve-based fate ranking.
- [x] Load-bearing route-margin, headroom and last-refuge artifacts are materialized with workflow provenance.
- [x] Two-repository reproducibility contract passes.
- [x] Submission bundle build passes.

## Fallback reactivation gates

- [x] State fallback cover letter is marked **FROZEN FALLBACK** and cannot be used while the flagship is under consideration.
- [x] State fallback reactivation requires the flagship to be withdrawn/rejected/abandoned plus a fresh exclusivity and journal-policy check.
- [x] Warning fallback is marked **FROZEN FALLBACK**.
- [x] Warning fallback reactivation additionally requires integration/reporting of the last-refuge holdout and `H_alpha` directional inversion.

## Author-controlled items before portal submission

- [ ] Author list/order approved.
- [ ] Affiliations and ORCIDs approved.
- [ ] Corresponding-author contact approved.
- [ ] CRediT statement approved.
- [ ] Funding and acknowledgements approved.
- [ ] Competing-interests statement approved.
- [ ] AI/automated-tool disclosure reviewed and approved.
- [ ] Permanent archive DOI / reviewer-accessible code and evidence snapshots created.
- [ ] Current Nature Ecology & Evolution policy checked immediately before submission.
- [ ] Final portal files inspected after journal-template conversion.
