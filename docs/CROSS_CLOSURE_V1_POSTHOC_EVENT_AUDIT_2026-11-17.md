# Cross-closure sorting × repair v1 — post-outcome event-grain audit
## 2026-11-17, evidence from the original 15,360 trajectories

**Result category: descriptive post-outcome diagnostic, NOT independent confirmation.**

Source preregistration: `efc3baa6868e705974235b35df70d1c3fee5b7a9`.
Original successful simulation: [run 44012157673](https://github.com/zuizui0223/egwe/actions/runs/44012157673), original artifact `14296518638`, digest `sha256:90dea2a81c668f77f4bd828977a52aeb37b92ef60b48f58e42d88ebfa17f033b`.

Diagnostic rerun (no new trajectories): [run 44013478477](https://github.com/zuizui0223/egwe/actions/runs/44013478477), artifact `14296914926`, digest `sha256:5d14005848d531403e23cf78491072572023b12025729ac3eccd1a3e766b40eb`. The workflow downloads the **exact original artifact**, checks every member SHA256 and confirms all 15,360 unique complete factorial keys plus match to the originally locked cell-level summaries.

## Main diagnostic finding: rare, partly recoverable trait-absence events

| Model analogue | First focal-trait absence by g40 | Incidence |
|---|---:|---:|
| A — aggregate support | **132 / 7,680** | **1.72%** |
| B — dynamic partner / stochastic encounter | **90 / 7,680** | **1.17%** |
| Combined, both models | **222 / 15,360** | **1.45%** |

**95 of the 222 first-passage events** (42.8%) were followed by later high-trait re-expression within the observation window. This is not an absorbing-state extinction endpoint; it must not be described as lasting ecological dysfunction or population extinction. All **16** condition×arrangement cells had first-passage rates between **0 and 4.1%**; two cells had zero events. Across all cells there were **zero first-passage events by generation 10**, while the preregistered prediction outcome was first loss by generation 40.

**All 960 trajectories per cell and all six master-seed blocks were retained.** The 960 repeated trajectories are not 960 independent ecological landscapes; formal original uncertainty used six master-seed blocks.

## Original eight arrangement-paired contrasts, not selected for significance

| Closure | Allele selection strength | Resident inheritance h | AA first loss | RR first loss | RR−AA (percentage points) |
|---|---:|---:|---:|---:|---:|
| A | 0 | 0.25 | 0/960 | 1/960 | +0.10 |
| A | 0 | 0.75 | 3/960 | 3/960 | +0.00 |
| A | 1 | 0.25 | 33/960 | 39/960 | +0.62 |
| A | 1 | 0.75 | 22/960 | 31/960 | +0.94 |
| B | 0 | 0.25 | 1/960 | 1/960 | +0.00 |
| B | 0 | 0.75 | 0/960 | 4/960 | +0.42 |
| B | 1 | 0.25 | 19/960 | 27/960 | +0.83 |
| B | 1 | 0.75 | 24/960 | 14/960 | −1.04 |

Original **preregistered** six-block factorial D (not any single cell) remains:

- A: +0.00417 [−0.01558, +0.02392];
- B: −0.02292 [−0.04663, +0.00079].

Both CIs cross zero. Low first-passage event incidence explains why the locked design carries little information about a directional effect, but it does **not** prove that rare events are the sole cause of failure or that A/B are equivalent. The negative B point estimate is not a confirmed sign reversal.

## Secondary direct-function analogue — bounded interpretation

The original protocol separately fixed a generation-40 `modeled_opportunity_g40` metric, defined as population-weighted `N×m×q` divided by population. It is **not** compatible-pollen receipt, measured seed set or reproductive fitness. Across the locked cells, modeled-opportunity means fell around **0.258–0.306 in A** and **0.322–0.368 in B**. They cannot be interpreted on an equal biological measurement scale: `q` means aggregate sigmoid support in A and observed stochastic encounter fraction in B. The secondary means are archived in the JSON diagnostic, not used to replace or rescue the failed primary criterion.

## Scientific judgment

**The failed portability test is largely a low-event-information / endpoint-semantics problem; it is not empirical evidence that real partner-specific sorting cannot transport between systems.** Two biologically different closures were compared without matching the interpretation of `q`, so the model design does not isolate partner availability, visitation effectiveness or compatible mating as individual causal sources. The next test must measure / hold fixed the same downstream functional endpoint while varying one bottleneck at a time, rather than introducing additional arbitrary synthetic parameters.

Existing sources already establish that visits are not equivalent to functional pollination and that genetically limited mate compatibility can suppress seeds despite pollen delivery:

- Young & Pickup (2010), *Journal of Applied Ecology*, DOI [10.1111/j.1365-2664.2010.01798.x](https://doi.org/10.1111/j.1365-2664.2010.01798.x): seven self-incompatible plant populations with S-alleles, compatible mating, pollen loads, seed set.
- Aizen & Harder (2007), *Ecology*, DOI [10.1890/06-1017](https://doi.org/10.1890/06-1017): quantity and quality components of pollen limitation.
- Review 2026, DOI [10.1146/annurev-environ-121224-092446](https://doi.org/10.1146/annurev-environ-121224-092446): interacting effects of encounter probability, efficiency, compatibility and reproduction.

These are precedents, not validation of either synthetic model. The genuinely unresolved empirical question is **whether a synchronized, cohort-matched process state actually removes residual context/history dependence in future functional prediction across more than one independent system**. Existing EGWEE Honshu–Izu vs Zurich archives cannot yet identify that cross-origin equality because treatment, measurement and study identity are confounded.

## Governance

- No extra seed, model run, threshold, cherry-picked domain or redefined primary endpoint.
- No new p-value or post-hoc confirmatory interpretation.
- The historical arithmetic erratum (original JSON 7680, actual 15360) remains documented and unmodified.
- The active *Theoretical Ecology* manuscript and its original EGC/EGWE finite model estimates are unchanged.
