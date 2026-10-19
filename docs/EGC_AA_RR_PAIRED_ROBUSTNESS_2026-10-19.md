# Exploratory AA/RR stochastic robustness extension — 2026-10-19

Following the 4-seed, 12-generation pilot (AA 1/4 vs RR 3/4 temporary global high-trait occupancy loss), this extension predeclares 128 new seeds 20001–20128 and horizons 12 and 24. It uses the exact upstream EGC commit dd8ee379 and the existing pinned runner without changing its model parameters.

Two distinct outcomes are reported: ever entering zero realised high-trait occupancy across all four patches by horizon, and high-trait occupancy at the final snapshot. The former is a first-passage event but **not absorbing**; the latter allows recovery. A paired discordant-count exact sign test is reported descriptively, not as confirmatory preregistered evidence. Pairing seeds does not guarantee that the two configurations consume identical underlying random draws.

This is synthetic model robustness, not ecological field evidence or an extinction probability. Source integrity and independent parameter variation remain prerequisites for stronger claims. The four pilot seeds are excluded from the new block. No previous NEE claims are changed.

## Executed 128-seed result (2026-10-19)

GitHub Actions run [39193070500](https://github.com/zuizui0223/egwe/actions/runs/39193070500), archived artifact **12160906887**. Exact upstream source commit was checked out. Both the dedicated run and protocol-invariant CI succeeded.

| Horizon | Endpoint | AA | RR | AA−RR | Paired discordance exact two-sided p |
| --- | --- | ---: | ---: | ---: | ---: |
| 12 | Ever zero high-trait occupancy | 15/128 (11.72%) | 16/128 (12.50%) | −0.78 pp | 1.000 |
| 24 | Ever zero high-trait occupancy | 100/128 (78.13%) | 104/128 (81.25%) | −3.13 pp | 0.572 |
| 12 | High-trait occupancy at final snapshot | 117/128 (91.41%) | 116/128 (90.63%) | +0.78 pp | 1.000 |
| 24 | High-trait occupancy at final snapshot | 45/128 (35.16%) | 42/128 (32.81%) | +2.34 pp | 0.771 |

The earlier **4-seed** 25%-versus-75% first-passage contrast **does not replicate as a large robust difference** in the fresh 128-seed block. This is a meaningful negative robustness check of that exploratory interpretation, not a negative result for the broader spatial-state sufficiency theorem. The full stochastic closure and the narrow fixed parameter setting remain valid model inputs, but there is no stable large AA superiority under this design.

Both arms exhibit substantially more *ever-loss* by 24 generations than by 12. The event is nonabsorbing and final occupancy is a separate endpoint. Paired seed numbers do not prove common-random-number coupling, and the reported p values are descriptive rather than confirmatory because the parameter setting and motivating contrast were previously explored.

**Interpretation ceiling:** Do not claim that a deeper local refuge necessarily improves stochastic multigeneration high-trait persistence, nor call a temporary absence permanent extinction. A next test would vary independently justified dispersal, recruitment, mutation, initial population and spatial forcing, with a frozen event and replication plan, rather than tune parameters to recover AA superiority.
