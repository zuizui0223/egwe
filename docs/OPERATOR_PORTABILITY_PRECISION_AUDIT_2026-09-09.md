# Operator-portability precision audit — 2026-09-09

## Purpose

This is a deterministic, post-result precision characterization of the already locked Phase U/R/S equal-rate tests. It opens no new simulation, seed, condition, endpoint, alpha level or operator parameter. It is not a post-hoc equivalence test and does not change any preregistered decision.

## Equal-rate effect size

For five seed blocks with eligible counts `n_i`, loss rates `p_i`, total `N=sum_i n_i` and pooled rate `p_bar`, define the Pearson homogeneity effect size

`w^2 = sum_i (n_i/N) * (p_i-p_bar)^2 / [p_bar*(1-p_bar)]`.

For the five-block Pearson equal-rate test, `df=4` and the asymptotic noncentrality parameter under an alternative is `lambda=N*w^2`. At two-sided omnibus alpha `0.05`, the chi-square critical value is `9.487729`.

Solving `Pr[ChiSquare_df4(lambda) > 9.487729] = 0.80` gives:

- `N=447` (the shared historical Phase R/S denominator): `w_80 = 0.163404`;
- `N=452` (the fresh Phase U paired denominator): `w_80 = 0.162498`.

At a pooled rate near `0.5`, these standardized effects correspond to a weighted RMS block-rate deviation of `w*sqrt(p*(1-p))`, or approximately **8.17 percentage points** for `N=447` and **8.12 percentage points** for `N=452`.

For 90% power the corresponding values are:

- `N=447`: `w_90 = 0.185643`, approximately **9.28 pp weighted RMS** at `p=0.5`;
- `N=452`: `w_90 = 0.184613`, approximately **9.23 pp weighted RMS** at `p=0.5`.

These values are power benchmarks, not significance thresholds. A realized sample can reject at a smaller observed `w`, as happened for the historical allele-only `m=.10` condition.

## Observed standardized heterogeneity

Using `w_obs=sqrt(X^2/N)` from the locked Pearson statistics/block counts:

| evidence block | condition | N | equal-rate p | observed `w` |
|---|---|---:|---:|---:|
| fresh Phase U | `m=0` | 452 | 0.13421 | 0.12473 |
| fresh Phase U | allele-only `m=.10` | 452 | 0.74513 | 0.06567 |
| shared historical R/S | no connectivity | 447 | 0.70964 | 0.06923 |
| shared historical R/S | allele-only `m=.10` | 447 | 0.020549 | 0.16112 |
| Phase R substitution | whole-individual `d=.10` | 447 | 0.81131 | 0.05957 |
| Phase S substitution | pollen-only `g=.20` | 447 | 0.72820 | 0.06757 |

The non-significant process-resolved conditions therefore showed observed heterogeneity well below the approximately `w=0.16` 80%-power benchmark. This supports a **precision-bounded null**: the tested design had high power for heterogeneity on the order of about eight percentage points weighted RMS near a 0.5 loss rate, but smaller heterogeneity remains compatible with the data. No equivalence margin was preregistered, so equivalence is not claimed.

## Shared-reference structure of Phases R and S

Phase R and Phase S are **not independent replications of the historical comparator contrast**. Their locked summaries contain exactly the same five `no_connectivity` blocks and exactly the same five `allele_only_m010` blocks:

- no connectivity: `[[47,88],[48,89],[58,93],[46,86],[51,91]]`;
- allele-only `m=.10`: `[[45,88],[48,89],[66,93],[42,86],[48,91]]`.

Both use master seeds `20290410–20290414`. The independent evidence structure is therefore:

1. **one fresh independent replication** (Phase U; new master seeds `20291010–20291014`) of the historical allele-only `m=.10` heterogeneity claim; plus
2. **two process substitutions on one shared historical reference ensemble**: whole-individual dispersal (Phase R) and pollen-only paternal gene flow (Phase S).

The R and S process arms are biologically distinct closures, but the common reference evidence must not be counted twice.

## R3/R4 labels

`R3_highrep` and `R4_highrep` are deterministic screen labels calculated from the same realized block-rate vector used in the equal-rate analysis. They are not randomized conditions, covariates, latent regimes or independent explanatory variables. In Phase R/S the only `R3_highrep` condition is the historical allele-only `m=.10` block vector because that vector itself contains the detected between-block heterogeneity. The labels should be reported only as protocol provenance or outcome summaries.

## Evidence sources

- `artifacts/fresh_connectivity_replication/phase_u_locked_summary.json`
- `artifacts/process_resolved_movement/phase_r_locked_summary.json`
- `artifacts/process_resolved_pollen/phase_s_locked_summary.json`
- `src/eco_genetic_warning_extensions/fresh_connectivity_replication_phase_u_runner.py`
- `src/eco_genetic_warning_extensions/process_resolved_movement_phase_r_runner.py`
- `src/eco_genetic_warning_extensions/process_resolved_pollen_phase_s_runner.py`

## Claim boundary

This audit characterizes the resolution of the already performed five-block Pearson tests. It does not retroactively preregister a power analysis, does not prove equivalence, and does not establish a universal biologically meaningful eight-percentage-point threshold.