# Operator-balance route margin — canonical prospective result

Status: **completed from the prospectively locked protocol**.

## Provenance

- protocol: `experiments/operator_balance_margin_fate_protocol.json`
- prospective protocol commit: `7d5ae677f5f36d279aae1a7af9707410925ec132`
- scientific head: `d8b7bf1da9c7f73d872cb93d7ea21547a429d6a6`
- workflow run: `34127034037`
- job: `101758021393`
- artifact: `10021317930`
- artifact digest: `sha256:1e5ecb658a66e78ffa0ea7eb0cf073323a2173eca7c55461a11aa91b8bd4eb69`
- compact materialization: `artifacts/operator_balance_route_margin/locked_result.json`

The protocol fixed 6 fresh master seeds x 500 paired keys x 4 conditions = **12,000 trajectories** before outcomes.

## 1. Exact transition audit passed

The route margin

\[
M=d(0.6q+0.3T+0.1G)-\left(\theta+\frac{\operatorname{logit}(0.625)}{4.5}\right)
\]

was checked against the next-q side of `0.625` for every patch-generation.

- patch-generations checked: **1,920,000**
- mismatches: **0**

The exact one-step theorem is therefore numerically reproduced over the full locked ensemble.

## 2. Direct recoupling did not extend positive-margin refuge duration

The prospective primary long-horizon estimand compared the number of generations retaining at least one nonnegative-margin patch under full feedback versus q-only.

- AA full minus q-only: **-0.323 generations**, 95% CI `[-0.3397,-0.3063]`
- RR full minus q-only: **-1.000 generations**, 95% CI `[-1.000,-1.000]`
- RR-minus-AA DID: **-0.677 generations**, 95% CI **`[-0.6937,-0.6603]`**
- locked decision: **`resolved_opposite_direction`**

This is a useful falsification. Direct eco-genetic feedback is an exact one-step recoupling operator, but it is **not** supported as a generic or preferential extender of above-switch refuge duration in this fresh ensemble.

The full-feedback RR-minus-AA upward recoupling-wedge count was exactly zero. The main asymmetry instead appeared as more suppression-wedge patch-generations in AA than RR.

## 3. Binary route status was an excellent precursor and useless discriminator

The frozen generation-20 marker asked whether all four full-feedback route margins were negative, with generation-40 realised functional loss as target.

Pooled full-feedback denominator:

- events: **3,943**
- non-events: **2,057**
- event-side precedence: **1.0**
- sensitivity: **1.0**
- specificity: **0.0**
- false-positive rate: **1.0**
- binary AUC: **0.5**

The same saturation held separately in AA and RR.

Therefore:

> **Transition-exactness does not imply fate-predictiveness.**

The route-margin sign is exact for the next transition, yet the generation-20 all-negative binary state contains zero event/non-event discrimination by generation 40.

## 4. Relation to the later continuous last-refuge result

This negative binary result does not contradict the later PR #163 holdout. The later test changed the statistical representation, not the scientific endpoint:

- it observed the system earlier, at snapshot generation 9 before the generation-10 update;
- it used the **continuous maximum patchwise route margin**, not a saturated all-negative threshold;
- it used 12 entirely new master seeds and a prospectively frozen full-feedback holdout.

That continuous strongest-refuge reserve achieved mean block AUC **0.92734** and added **+0.02135 AUC** beyond co-timed maximum q.

The combined conclusion is sharper than either result alone: the **depth** of remaining local reserve can retain fate information after the **sign** of a transition-exact coordinate becomes non-discriminative.

## Claim ceiling

The exact margin, route-duration result and binary-marker failure belong only to the declared finite closure and locked forcing path. The negative route-duration DID does not mean direct feedback universally worsens function; earlier locked endpoint contrasts show functional benefit in the same model family. It means only that one-step recoupling, above-switch duration and final functional persistence are distinct estimands and must not be collapsed into one generic notion of repair.
