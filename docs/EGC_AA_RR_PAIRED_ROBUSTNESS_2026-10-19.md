# Exploratory AA/RR stochastic robustness extension — 2026-10-19

Following the 4-seed, 12-generation pilot (AA 1/4 vs RR 3/4 temporary global high-trait occupancy loss), this extension predeclares 128 new seeds 20001–20128 and horizons 12 and 24. It uses the exact upstream EGC commit dd8ee379 and the existing pinned runner without changing its model parameters.

Two distinct outcomes are reported: ever entering zero realised high-trait occupancy across all four patches by horizon, and high-trait occupancy at the final snapshot. The former is a first-passage event but **not absorbing**; the latter allows recovery. A paired discordant-count exact sign test is reported descriptively, not as confirmatory preregistered evidence. Pairing seeds does not guarantee that the two configurations consume identical underlying random draws.

This is synthetic model robustness, not ecological field evidence or an extinction probability. Source integrity and independent parameter variation remain prerequisites for stronger claims. The four pilot seeds are excluded from the new block. No previous NEE claims are changed.
