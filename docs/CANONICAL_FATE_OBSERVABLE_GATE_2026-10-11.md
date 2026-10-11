# Actual canonical operator bridge: identical marginals, different one-step threshold coverage

**2026-10-11.** The preceding PR #225 proved an abstract finite-state Markov lumpability criterion. This follow-up does **not** invent a transition probability matrix for the full simulator. Instead it imports the actual deterministic `next_interaction_from_state` from `src/eco_genetic_warning_extensions/operator_balance_route_margin.py`.

With pinned unit density, area ratio 1, theta 0.5025, kappa 4.5, weights alpha 0.6, beta_trait 0.3, gamma_allele 0.1, four q values (0.65,0.75,0.85,0.95), and trait=allele bundles (0.2,0.4,0.6,0.8), compare aligned and reversed pairings. They have identical separate q, trait and allele marginals.

The resulting next-q fields are:

- Aligned: 0.46350253, 0.61863299, 0.75282757, 0.85116276; **2 of 4** patches meet q_next >= 0.625.
- Reversed: 0.71783546, 0.69925442, 0.67999526, 0.66010227; **4 of 4** patches meet q_next >= 0.625.

Aligned has a higher maximum local q_next (0.85116 versus 0.71784), while reversed has broader threshold coverage and a higher mean (0.68930 versus 0.67153). This is an exact evaluation of the already pinned deterministic update (up to numerical floating precision), not a new independent experiment. It demonstrates **failure of coarse marginal sufficiency for one-step threshold coverage**, even without a stochastic loss model.

**Important scientific boundary:** q_next >= 0.625 is the declared local allele-relative-fitness crossing w(q_next)>=1, not a measured reproductive function or a definition of ecological loss. Counts of patches above it are *not* future persistence probabilities. PR #225's abstract Markov counterexample cannot be promoted to an EGWE-specific multigeneration loss theorem until a fully specified, justified stochastic kernel, absorbing functional-loss set, state discretization and model-validation checks are available.

Reproduce with `python -m pytest -q tests/test_canonical_fate_observable_gate.py` and `python scripts/canonical_fate_observable_gate.py`. No frozen NEE claims or empirical records are modified.
