# Reproducibility guide

This repository is the **independent condition-recovery extension and flagship-first submission orchestrator with two frozen fallback manuscripts** for the eco-genetic warning study. It depends on a fixed scientific state of `eco-genetic-criticality` but does not rewrite the parent evidence ledger.  The active manuscripts and disjoint claim ownership are declared in `manuscript/publication_lanes.json`; `manuscript/main_text.md` is an integrated source archive only.

The parent scientific commit is fixed at `dd8ee379d0d3518194c767d16402042525bc00dc`.

## Reproduction levels

### Level 1 — package and invariant tests

```bash
git clone https://github.com/zuizui0223/eco-genetic-warning-extensions.git
git clone https://github.com/zuizui0223/eco-genetic-criticality.git upstream
git -C upstream checkout dd8ee379d0d3518194c767d16402042525bc00dc

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e upstream
python -m pip install -e '.[dev,reproducibility]'
python -m pytest
python scripts/verify_reproducibility_contract.py --upstream upstream
```

### Level 2 — rebuild the publication package

The paper-completion workflow regenerates publication outputs from locked evidence, retains finite-horizon censoring, resamples whole trajectories for secondary intervals and builds checksummed submission bundles. Historical artifacts remain immutable.

### Level 3 — reproduce condition campaigns

Warning-blind campaigns can be rerun independently, including recurrent-turnover calibration, historical Phase E/F/G conditions, high-precision Phases K–Q, process-resolved R/S, dynamic partner Phase T, and the preregistered Phase-U fresh connectivity replication.

A rerun with new seeds creates a **new finite evidence set** and must not overwrite any locked historical or replication result. Phase U itself is closed: replacement seeds or repeated fresh ensembles are not permitted under the same generation merely to recover significance.

## Historical screen and precision protocol

The preregistered R1–R4 classifier is retained exactly for historical reproducibility. Its R3/R4 labels are not interpreted as biological estimands by themselves.

The precision-validation protocol is:

1. preserve the relevant declared biological closure;
2. use 100 attempted replicates per seed block for load-bearing high-precision contrasts;
3. when replaying historical families, require exact first-20 eligible/loss prefix reproduction;
4. retain the historical `[0.30,0.70]` screen unchanged for provenance;
5. report pooled functional-loss incidence separately;
6. report an equal-rate diagnostic across high-precision blocks;
7. for paired perturbations, report bidirectional switches and exact McNemar evidence;
8. when an effect becomes load-bearing and an independent replication is declared, fix fresh seeds and the decision rule before outcomes and do not replace the ensemble after inspection.

## Locked precision and robustness evidence

- Phase K seed-family replay: run `32557289628`, artifact `9471883061`.
- Phase L cross-campaign R3 audit: run `32557903970`, artifact `9471949092`.
- Phase M historical-family connectivity: run `32558147960`, artifact `9472067167`, digest `sha256:0b15ca5a3b7f40a24332f8bcc14fad01036ed2d3fb4c0ff7ff181208a5d940d6`.
- Phase N partner loss: run `32558466157`, artifact `9472148035`, digest `sha256:c55654b556280c5caa63ee1b9febe62a0b545da6227104799014484f65dc25c0`.
- Phase O immediate frontier: run `32558742101`, artifact `9472838181`, digest `sha256:4b39d7df5d60b08bef0f78eb59524510c5549bae9199064f5a9841164db9a610`.
- Phase P outer frontier: scientific run `32562175464`; seed artifact IDs/digests are committed in `artifacts/high_precision_condition_map.json`.
- Phase Q aggregate interaction support: run `32559058069`, artifact `9472941879`, digest `sha256:7ccaf8efd253499f047de2a40a35eaab6007292005814fc2f9539b66891d3df7`.
- Phase R whole-individual movement: run `32613357637`, artifact `9486225034`, digest `sha256:13474765636fe839f4953a94618cfdf1dc7bd145f029ae97df26ced32443c143`.
- Phase S pollen-only gene flow: run `32613877695`, artifact `9486401100`, digest `sha256:a320527fbb737209c23cbf3376172f15c189e6c76125c69e90f135a74f70bc04`.
- Phase T dynamic partner architecture: run `32614486507`, artifact `9486577103`, digest `sha256:44f54e4b8ac313e01ea43444a84351012f308a69ccbcc4d0bf253cfa8ed9dc1c`.
- Phase U fresh connectivity replication: run `32615044162`, artifact `9486740313`, digest `sha256:f561cb23d8040469db673acbdb329ec0e89bcefef30572dfb63bc8c829801756`; decision `historical_m010_heterogeneity_not_freshly_replicated`.

## Current reproducible condition conclusions

**Recurrent turnover:** pooled loss declines from about `.682` at `p_star=.325` through intermediate `.350–.375` conditions to `.273` at `.400`; no tested high-precision frontier condition shows detected excess block heterogeneity.

**Connectivity:** the historical Phase-M seed family showed `m=.10` equal-rate `p=.0205`, but one preregistered independent Phase-U ensemble gave fresh `m=.10 p=.745` with paired McNemar `p=.694`. The historical observation is therefore not supported as independently reproducible. Whole-individual and pollen-only movement closures also did not show the historical-family heterogeneity pattern. No robust portable connectivity heterogeneity effect is established.

**Aggregate feedback:** all three predeclared `kappa=3.0/4.5/6.0` remain intermediate at high precision with no detected block heterogeneity.

**Partner architecture:** reduced-form partner loss and matched-expected-support temporal partner variability are precision-bounded nulls, not equivalence results; the adaptive-rewiring gate remains closed.

**Warning validity:** the post-review audit uses all baseline-eligible saved trajectories from parent run `28500796310` and Phase-V run `32636847803`. Each of the six frozen thresholds led all 35/35 and 33/33 losses but also fired in all 48/48 and 49/49 non-events. Full-horizon specificity is zero and binary-marker AUC is 0.5. The compact 1,200-row record table is checksummed in `artifacts/warning_validity/source_manifest.json`.

## Interpretation safeguards

Reproduction must preserve that:

- parent trajectories and extension trajectories are separate evidence;
- historical Protocol 002 remains 15/15 `no_domain_selected` under its original screen;
- historical R1–R4 labels are calibration outcomes, not latent biological classes;
- the historical Phase-M `m=.10` p=.0205 result is a seed-family observation, not an independently replicated connectivity threshold;
- Phase U is one independent non-replication, not proof that no other seed family can ever show heterogeneity;
- Phase M/U `migration_rate` is allele-frequency mixing, not demographic, pollinator, pollen, seed or recolonisation movement;
- R/S movement closures are distinct model operators;
- Phase Q `interaction kappa` is aggregate positive feedback, not partner richness/connectance;
- Phase N/T do not represent a full dynamic multispecies network;
- no outcome-informed parameter, seed or precision refinement is opened to recover a preferred result;
- Protocol 003 tests bounded portability across non-matched calibrated domains, not a single-factor effect of transition direction;
- finite-horizon non-events remain right-censored;
- event-conditional warning pairs are not used as the full performance denominator;
- non-significant paired risk differences are not described as equivalence;
- `p_star` is an effective recurrent-transition equilibrium, not an estimated biological mutation rate;
- a successful build does not convert finite Type S results into a theorem.

## Archival release checklist

Before final deposition, merge only after protocol/manuscript/figure/bundle checks pass; run the paper-completion workflow from merged `main`; verify checksums and final figure rendering; create immutable releases for both repositories; archive the release pair and bundle; and add author-approved DOI, authorship, funding, licence and CRediT metadata.
