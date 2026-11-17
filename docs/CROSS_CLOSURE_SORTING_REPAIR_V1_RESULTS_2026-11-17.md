# Cross-closure sorting × repair v1 — complete result (2026-11-17)

**Decision: no evidence of portable directional modification across the two predeclared closures.** This is a new independent model-analogue experiment and is **not** a reanalysis, replacement or validation of the locked `Theoretical Ecology` flagship results.

## Immutable ex-ante design and execution

- Original prospective protocol-only commit: `efc3baa6868e705974235b35df70d1c3fee5b7a9` (`experiments/cross_closure_sorting_repair_v1_protocol.json`).
- Explicit factorial: 2 non-equivalent closures × 2 AA/RR assignments × 2 selection strengths × 2 recruitment weights × 6 independent master seeds × 160 replicates = **15,360 trajectories**. The protocol's `total_trajectories: 7680` was an **arithmetic error**, not a change in planned cell sizes; see `docs/CROSS_CLOSURE_SORTING_REPAIR_V1_ARITHMETIC_ERRATUM.md`.
- Prior technical run [44011763582](https://github.com/zuizui0223/egwe/actions/runs/44011763582) stopped on that count inconsistency before analysis. The second run [44011968432](https://github.com/zuizui0223/egwe/actions/runs/44011968432) stopped at an API return-arity error before output. No exposed outcome values were used to change a condition, endpoint, test, or sign.
- Successful complete locked run: [44012157673](https://github.com/zuizui0223/egwe/actions/runs/44012157673), artifact [14296518638](https://github.com/zuizui0223/egwe/actions/runs/44012157673/artifacts/14296518638), artifact digest `sha256:90dea2a81c668f77f4bd828977a52aeb37b92ef60b48f58e42d88ebfa17f033b`.
- Output ZIP includes `locked_result.json`, all `all_trajectories.csv` rows, protocol copy and SHA256 manifest. The artifact retention period is finite; the calculation is reproducible from this repository and the original fixed protocol.

## Frozen primary hypothesis and exact result

The primary estimand within each closure was

```text
RD(s,h) = Pr(loss through g40 | RR,s,h) − Pr(loss through g40 | AA,s,h)
D = {RD(1,.75) − RD(0,.75)} − {RD(1,.25) − RD(0,.25)}
```

The **ex ante directional claim** was that D is positive: interaction-conditioned allele selection preferentially increases the RR-minus-AA difference when resident inheritance is higher (i.e. allele-linked recruitment mismatch repair is weaker). **Portability required BOTH model-specific six-block 95% confidence intervals above zero and BOTH point estimates greater than +0.02 absolute loss-risk units.**

| Model (separate finite closure) | D, absolute probability difference | 95% six-block CI | Frozen decision |
|---|---:|---:|---|
| A — aggregate interaction-support analogue | +0.0041667 (+0.42 percentage points) | [−0.015583, +0.023916] | Unresolved |
| B — dynamic partner supply + stochastic visits | −0.0229167 (−2.29 percentage points) | [−0.046626, +0.000793] | Unresolved; negative point sign |

**Main decision: `cross_closure_direction_not_established_no_retuning`.** Both intervals cross zero and the observed point estimates have opposite signs. Do not label B's slightly negative estimate a statistically resolved reversal, and do not label the failure to reject an equivalence result.

## Scientific interpretation

1. The prior EGC–EGWE `+6.883 pp` q-dependent allele-selection **edge DID** is a credible result **within that original pinned finite q-only closure**. The new D above is a **different factorial interaction estimand**: comparison of their magnitudes would be misleading.
2. The broader idea that selection and recruitment repair alone determine the *direction* of functional loss does **not** receive cross-model support from these two separate analogues. This is a failed portability test, not proof that selection or repair never matters.
3. Model B explicitly includes partner availability, stochastic encounters and a different meaning for `q`. The contrast motivates partner/process-level measurement but **does not isolate which of those model changes caused** the cross-model point-sign difference. No natural pollinator or plant fitness data were used.
4. The predeclared first-passage event is **absence of the focal realized high-trait phenotype in all patches**, not demographic extinction and not necessarily an absorbing event. All non-events remain in the risk denominator. Functional opportunity and the t10 ranking comparison remain predeclared **secondary/descriptive** outputs in the artifact; they must not replace the failed primary criterion.
5. **Publication firewall:** this new extension must not silently enter the current *Theoretical Ecology* Results as support for a new ecological law; the existing paper's matched-marginal exact counterexample and single-edge finite causality remain unchanged.

## Next scientifically justified question (not yet answered)

Instead of searching parameter values until D becomes positive, seek a **measurable ecological variable** that can make the two closures comparable: observed partner availability, per-visit effectiveness, pollen compatibility and offspring recruitment in synchronized cohorts. A future test would predeclare whether those processes account for residual prediction differences, separately assess environmental/demographic histories and independently hold out whole populations. Until tested, **there is no demonstrated universal sorting-versus-repair boundary and no natural transfer of the finite warning AUC**.

## Technical verification status

The successful run passed the preregistered six-block primary analysis, fixed cell denominators, full CSV output, protocol SHA/ancestry check, and associated protocol/AA-RR/reproducibility CI. The two preceding technical failures remain public and were repaired without inspecting outcome estimates or changing scientific criteria.
