# Future functional-loss identifiability under finite Markov coarse-graining

For a finite Markov transition matrix P and coarse partition c, strong lumpability requires that for every pair i,j in the same coarse block A, and every target block B, the transition sums Σ(k in B)P[i,k] and Σ(k in B)P[j,k] are equal. If loss is a union of coarse blocks, this guarantees equal finite-horizon first-hitting probabilities for all initial microstates in A.

This condition is necessary and sufficient for a valid coarse Markov transition for all initial distributions, but only sufficient—not necessary—for equality of a particular endpoint's future loss risk.

Exact counterexample: five states A1,A2,B1,B2,LOSS. A1→B1→LOSS, whereas A2→B2→B2. A1 and A2 have identical coarse label A and equal one-step loss risk 0, but their two-step first-hit loss risks are respectively 1 and 0. Thus one-step agreement does not guarantee equal longer-term fate.

This is classical finite-state lumpability mathematics, not an empirical or full-EGWE-simulator result. Next: construct and validate an actual transition kernel and block-measurable loss endpoint for the full life-cycle model before promoting the result.