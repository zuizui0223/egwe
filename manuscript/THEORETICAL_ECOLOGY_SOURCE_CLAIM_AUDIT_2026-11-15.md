# Source-claim and bibliography audit — Theoretical Ecology (2026-11-15)

## Status and scope
Editorial/source-fidelity correction in the single active Theoretical Ecology submission lane. **No simulated trajectories, seed maps, endpoints, model weights, thresholds, AUCs, or natural tests were recalculated.** This audit corrects bibliographic titles and keeps distinct source-defined meanings of two thresholds.

## 1. Three original-paper titles corrected against publishers

| DOI / primary source | Exact published title | Earlier manuscript issue |
| --- | --- | --- |
| [10.1007/s11284-007-0345-4](https://doi.org/10.1007/s11284-007-0345-4), *Ecological Research* 23:141–150 (2008) | **Impact of volcanic activity on a plant-pollinator module in an island ecosystem: the example of the association of Camellia japonica and Zosterops japonica** (Abe H, Hasegawa M) | A shorter, nonmatching title claimed only a generic mutualism |
| [10.1371/journal.pone.0062696](https://doi.org/10.1371/journal.pone.0062696), *PLOS ONE* 8:e62696 (2013) | **Resilient Plant–Bird Interactions in a Volcanic Island Ecosystem: Pollination of Japanese Camellia Mediated by the Japanese White-Eye** (Abe H, Ueno S, Takahashi T, Tsumura Y, Hasegawa M) | Prior title falsely included **seed dispersal** |
| [10.1038/hdy.2013.3](https://doi.org/10.1038/hdy.2013.3), *Heredity* 111:1–7 (2013) | **Inferring contemporary dispersal processes in plant metapopulations: comparison of direct and indirect estimates of dispersal for the annual species Crepis sancta** (Dornier A, Cheptou P-O) | Prior title incorrectly described the study as a genetic-structure paper |

Primary abstracts/records also accessed via [PLOS](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0062696), [Heredity](https://www.nature.com/articles/hdy20133), and the publisher [Ecological Research DOI page](https://esj-journals.onlinelibrary.wiley.com/doi/10.1007/s11284-007-0345-4).

## 2. Endpoint/allele and full high-trait grid viability must not be conflated

The historical focused sorting theorem `docs/ALLELE_SORTING_OPERATOR_THEOREM_2026-09-06.md` correctly derives

```
W(z=1;q) = 0.5 + 0.8q
w_high(q) = 0.75 + 0.4q
q_allele = 0.625
```

Thus the *endpoint* phenotype `z=1` has W≥1 at exactly the q at which a **segregating high-associated allele** ceases being selected against. But endpoint `z=1` is not identical to **any viable high-investment trait bin** in the original 101-bin source grid.

The exact source-pinned follow-up `docs/EGC_GRID_VIABILITY_VS_ALLELE_SORTING_FRONTIER_2026-10-24.md` evaluated all `z≥0.7` and established

```
q_grid ≈ 0.5991975107   (max-performing high bin at z=0.97)
q_allele = 0.625
q_grid < q_allele
```

A high-grid bin can therefore be potentially viable for 0.5992≤q<0.625 even while the z=1-associated allele has a relative fitness multiplier below one. In a monomorphic p=1 state, below-one relative fitness is **not** itself an observed allele-frequency decline; the source-exact follow-up explicitly states this boundary.

Consequences for the manuscript:
- The **Q1 fragmentation gradient**'s original source-supported potential-viability results (1,037/1,037 etc.) remain unchanged.
- The exact deterministic q-dependent allele sorting theorem, focused deletion DID **+6.883 percentage points**, and the continuous last-refuge holdout AUC **0.92734** / incremental **+0.02135** remain valid **for their original predeclared q=0.625 endpoint route**.
- The `M` route-sign audit (zero mismatches in 1,920,000 patch-generations) certifies `sign(q_next−0.625)`, **not** whether *some* high-bin has W(z;q_next)≥1.
- The existing all-patch functional-loss endpoint, event counts, binary marker specificity zero, and H_alpha inversion AUC 0.23253 must not be retroactively redefined to match q_grid.
- A new q_grid-based warning study would require a separate, prospectively declared protocol; **none** is claimed here.

## 3. Natural comparison is an analogy, not a matched experiment

**Urban Crepis:** Cheptou and Avendaño (2006, [DOI](https://doi.org/10.1111/j.1469-8137.2006.01880.x)) documented low-density pollinator-activity and seed-set declines in Montpellier. Dornier and Cheptou (2013, [DOI](https://doi.org/10.1038/hdy.2013.3)) independently estimated seed and pollen dispersal/immigration across urban networks, finding heterogeneity in seed immigration. These **are separate study designs**, and cannot establish that immigration failed to restore pollination function in paired sites/cohorts.

**Miyake-jima Camellia:** Abe and Hasegawa (2008, [DOI](https://doi.org/10.1007/s11284-007-0345-4)) observed pollination compensation under volcanic disturbance; Abe et al. (2013, [DOI](https://doi.org/10.1371/journal.pone.0062696)) reported broader Japanese White-eye movement, increased pollen inflow/donor mixing and seed genetic diversity under floral-resource reduction. These studies illustrate a possible compensation process, **not** proof that a synthetic eco-genetic operator has been validated or that urban/island regimes are equivalent.

## Changed surfaces and nonchanges

- Correct original titles in `theoretical_ecology_article.md` and `theoretical_ecology_references.md`.
- Replace an overbroad high-trait viability equivalence with endpoint/grid distinction in Results and Methods.
- Clarify urban–island passage as a non-matched literature contrast.
- Correct generator labels in `scripts/build_nee_four_operator_figure3.py` and `scripts/build_nee_sorting_buffering_figures.py`; historical filenames are preserved for figure provenance.
- Correct explanatory text in `manuscript/nee_flagship_display_plan.md` (legacy filename, current TE figure source).
- Maintain 22 references in `theoretical_ecology_author_input_packet.md`; citations/simulation endpoints are unchanged.

**Release gate:** require regenerated Figure 3 to identify `z=1 endpoint` and `q_grid≈0.5992`, and require a source-title/threshold assertion in the Theoretical Ecology manuscript checker. Author declarations and publisher submission remain blocked pending human approval.
